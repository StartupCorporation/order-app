from contextlib import asynccontextmanager

from infrastructure.database.base.transaction import DatabaseTransactionManager
from infrastructure.database.relational.connection import SQLDatabaseConnectionManager


class SQLDatabaseTransactionManager(DatabaseTransactionManager):

    def __init__(
        self,
        connection_manager: SQLDatabaseConnectionManager,
    ):
        self._connection_manager = connection_manager

    @asynccontextmanager
    async def begin(self) -> None:
        explicit_transaction_key = 'explicit_transaction'

        async with self._connection_manager.session() as session:
            explicit_transaction = session.info.get(explicit_transaction_key, False)
            session.info[explicit_transaction_key] = True

            try:
                if not (session.in_transaction() or explicit_transaction):
                    await session.begin()
                yield
            except Exception as e:
                await session.rollback()
                raise e

            if session.in_transaction() and not explicit_transaction:
                await session.commit()
                del session.info[explicit_transaction_key]
