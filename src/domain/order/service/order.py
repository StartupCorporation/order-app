from dw_shared_kernel import ModelEventBus

from domain.order.entity.order import Order
from domain.order.entity.order_status import BuiltInOrderStatus
from domain.order.exception.order_status_not_found import OrderStatusNotFound
from domain.order.repository.order import OrderRepository
from domain.order.repository.order_status import OrderStatusRepository
from domain.order.value_object.customer_personal_info import CustomerPersonalInformation
from domain.order.value_object.order_product import OrderedProduct


class OrderService:
    def __init__(
        self,
        order_status_repository: OrderStatusRepository,
        order_repository: OrderRepository,
        event_bus: ModelEventBus,
    ):
        self._order_status_repository = order_status_repository
        self._order_repository = order_repository
        self._event_bus = event_bus

    async def create_new_order(
        self,
        customer_personal_information: CustomerPersonalInformation,
        ordered_products: list[OrderedProduct],
        message_customer: bool,
        customer_comment: str,
    ) -> None:
        order_status = await self._order_status_repository.get_by_code(code=BuiltInOrderStatus.NEW)

        if not order_status:
            raise OrderStatusNotFound(f"Unable to find '{BuiltInOrderStatus.NEW}' order status.")

        new_order = Order.new(
            status=order_status,
            customer_personal_info=customer_personal_information,
            ordered_products=ordered_products,
            customer_comment=customer_comment,
            message_customer=message_customer,
        )

        new_order.reserve_ordered_products()

        for event in new_order.flush_events():
            await self._event_bus.publish(event=event)

        await self._order_repository.save(entity=new_order)

    async def mark_order_as_failed_for_products_reservation(
        self,
        order: Order,
    ) -> None:
        order_status = await self._order_status_repository.get_by_code(
            code=BuiltInOrderStatus.PRODUCTS_RESERVATION_FAILED,
        )

        if not order_status:
            raise OrderStatusNotFound(
                f"Unable to find '{BuiltInOrderStatus.PRODUCTS_RESERVATION_FAILED}' order status.",
            )

        order.mark_as_failed_for_products_reservation(order_status=order_status)

    async def start_order_processing(
        self,
        order: Order,
    ) -> None:
        order_status = await self._order_status_repository.get_by_code(code=BuiltInOrderStatus.PROCESSING)

        if not order_status:
            raise OrderStatusNotFound(f"Unable to find '{BuiltInOrderStatus.PROCESSING}' order status.")

        order.start_processing(order_status=order_status)

        for event in order.flush_events():
            await self._event_bus.publish(event=event)

        await self._order_repository.save(entity=order)
