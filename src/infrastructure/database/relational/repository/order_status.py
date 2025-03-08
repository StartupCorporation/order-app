from domain.order.entity.order_status import OrderStatus
from domain.order.repository.order_status import OrderStatusRepository
from infrastructure.database.relational.repository.base import AbstractSQLRepository


class SQLOrderRepository(AbstractSQLRepository, OrderStatusRepository):
    async def get_by_code(
        self,
        code: str,
    ) -> OrderStatus | None:
        pass
