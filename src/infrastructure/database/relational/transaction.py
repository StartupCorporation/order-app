import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from contextvars import ContextVar

from infrastructure.database.relational.connection import SQLConnectionManager


class SQLTransactionManager:
    def __init__(
        self,
        connection_manager: SQLConnectionManager,
    ):
        self._connection_manager = connection_manager
        self._is_transaction_running = ContextVar("_is_transaction_running")

    @asynccontextmanager
    async def begin(self) -> AsyncIterator[None]:
        current_task = asyncio.current_task()
        if not current_task:
            raise

        task_context = current_task.get_context()
        if self._is_transaction_running in task_context:
            yield
        else:
            async with self._connection_manager.connect() as connection:
                async with connection.transaction():
                    self._is_transaction_running.set(True)
                    yield
                    self._is_transaction_running.set(None)
