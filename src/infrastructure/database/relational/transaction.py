from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from infrastructure.database.relational.connection import SQLConnectionManager


class SQLTransactionManager:
    def __init__(
        self,
        connection_manager: SQLConnectionManager,
    ):
        self._connection_manager = connection_manager

    @asynccontextmanager
    async def begin(self) -> AsyncIterator[None]:
        async with self._connection_manager.connect() as connection:
            async with connection.transaction():
                yield
