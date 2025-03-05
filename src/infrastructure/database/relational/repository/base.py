from abc import ABC, abstractmethod
from typing import Any
from functools import cached_property

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from dw_shared_kernel import (
    Entity,
    CRUDRepository,
)

from infrastructure.database.relational.connection import SQLDatabaseConnectionManager


class SQLAlchemyRepository(ABC):
    def __init__(
        self,
        connection_manager: SQLDatabaseConnectionManager,
    ):
        self._connection_manager = connection_manager


class CRUDSQLAlchemyRepository[ID, ENTITY: Entity](
    SQLAlchemyRepository,
    CRUDRepository,
    ABC,
):
    async def get(self, id_: ID) -> ENTITY | None:
        stmt = select(self.entity_class).where(self.entity_class.id == id_)
        return await self._scalar(stmt)

    async def save(self, entity: ENTITY) -> None:
        session: AsyncSession

        async with self._connection_manager.session() as session:
            session.add(entity)
            await session.flush()

    async def delete(self, id_: ID) -> None:
        session: AsyncSession

        async with self._connection_manager.session() as session:
            await session.execute(delete(self.entity_class).where(self.entity_class.id == id_))
            await session.flush()

    async def _scalars(self, *args, **kwargs) -> list[ENTITY]:
        session: AsyncSession

        async with self._connection_manager.session() as session:
            return (await session.scalars(*args, **kwargs)).unique().all()  # type: ignore

    async def _scalar(self, *args, **kwargs) -> Any:
        session: AsyncSession

        async with self._connection_manager.session() as session:
            return await session.scalar(*args, **kwargs)

    async def _execute(self, *args, **kwargs) -> None:
        session: AsyncSession

        async with self._connection_manager.session() as session:
            await session.execute(*args, **kwargs)

    @cached_property
    @abstractmethod
    def entity_class(self) -> type[ENTITY]: ...
