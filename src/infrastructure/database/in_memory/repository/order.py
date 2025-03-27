from uuid import UUID

from domain.order.entity.order import Order
from domain.order.repository.order import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    def __init__(self) -> None:
        self._storage: set[Order] = set()

    async def get_all(self) -> list[Order]:
        return list(self._storage)

    async def save(
        self,
        entity: Order,
    ) -> None:
        self._storage.add(entity)

    async def get_by_id(
        self,
        id_: UUID,
    ) -> Order | None:
        return next(
            filter(lambda entity: entity.id == id_, self._storage),
            None,
        )
