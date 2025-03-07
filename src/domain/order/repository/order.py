from abc import ABC, abstractmethod
from uuid import UUID

from domain.order.entity.order import Order


class OrderRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id_: UUID) -> Order: ...

    @abstractmethod
    async def save(self, entity: Order) -> None: ...
