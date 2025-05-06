from abc import ABC, abstractmethod

from domain.order.entity.order import Order


class OrderMailService(ABC):
    @abstractmethod
    async def send_order_created_mail(self, order: Order) -> None: ...

    @abstractmethod
    async def send_order_processing_mail(self, order: Order) -> None: ...

    @abstractmethod
    async def send_order_failed_to_reserve_products_mail(self, order: Order) -> None: ...

    @abstractmethod
    async def send_order_completed_mail(self, order: Order) -> None: ...
