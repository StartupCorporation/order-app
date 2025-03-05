from asyncio import current_task
from contextlib import asynccontextmanager
from functools import cached_property
from typing import AsyncContextManager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

from infrastructure.settings.database import DatabaseSettings


class SQLDatabaseConnectionManager:
    def __init__(
        self,
        settings: DatabaseSettings,
    ) -> None:
        self._settings = settings

    @asynccontextmanager
    async def session(self) -> AsyncContextManager[AsyncSession]:
        explicit_session_key = "explicit_session"
        session = self._session()
        explicit_session = session.info.get(explicit_session_key, False)
        session.info[explicit_session_key] = True

        try:
            yield session
        finally:
            if not explicit_session:
                await session.close()
                del session.info[explicit_session_key]

    @cached_property
    def _engine(self) -> AsyncEngine:
        return create_async_engine(self._settings.get_database_url("postgresql+asyncpg"))

    @cached_property
    def _session_factory(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            bind=self._engine,
            expire_on_commit=True,
        )

    @cached_property
    def _session(self) -> async_scoped_session[AsyncSession]:
        return async_scoped_session(
            session_factory=self._session_factory,
            scopefunc=current_task,
        )
