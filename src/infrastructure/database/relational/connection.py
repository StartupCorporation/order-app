import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from contextvars import ContextVar

from asyncpg import Connection
import asyncpg

from infrastructure.settings.database import DatabaseSettings


class SQLConnectionManager:
    def __init__(
        self,
        database_settings: DatabaseSettings,
    ):
        self._database_settings = database_settings
        self._current_connection = ContextVar("_current_connection")

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[Connection]:
        current_task = asyncio.current_task()
        if not current_task:
            raise

        task_context = current_task.get_context()

        if self._current_connection in task_context:
            yield task_context[self._current_connection]
        else:
            connection = await asyncpg.connect(self._database_settings.connection_url)
            self._current_connection.set(connection)
            yield connection
            self._current_connection.set(None)
            await connection.close()
