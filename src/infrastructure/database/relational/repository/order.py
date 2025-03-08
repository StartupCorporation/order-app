from uuid import UUID

from domain.order.entity.order import Order
from domain.order.repository.order import OrderRepository
from infrastructure.database.relational.repository.base import AbstractSQLRepository


class SQLOrderRepository(AbstractSQLRepository, OrderRepository):
    async def get_by_id(
        self,
        id_: UUID,
    ) -> Order | None:
        pass

    async def save(
        self,
        entity: Order,
    ) -> None:
        pass
