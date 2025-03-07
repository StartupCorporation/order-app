from abc import ABC, abstractmethod

from domain.order.entity.order_status import OrderStatus


class OrderStatusRepository(ABC):
    @abstractmethod
    async def get_by_code(self, code: str) -> OrderStatus | None: ...
