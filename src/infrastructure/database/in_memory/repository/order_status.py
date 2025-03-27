from domain.order.entity.order_status import OrderStatus
from domain.order.repository.order_status import OrderStatusRepository


class InMemoryOrderStatusRepository(OrderStatusRepository):
    def __init__(self) -> None:
        self._storage: set[OrderStatus] = set()

    async def save(
        self,
        entity: OrderStatus,
    ) -> None:
        self._storage.add(entity)

    async def get_by_code(
        self,
        code: str,
    ) -> OrderStatus | None:
        return next(
            filter(lambda entity: entity.code == code, self._storage),
            None,
        )
