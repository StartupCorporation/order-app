from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from dw_shared_kernel import (
    Entity,
    EventMixin,
)

from domain.order.entity.order_status import BuiltInOrderStatus, OrderStatus
from domain.order.events.order_created import OrderCreated
from domain.order.events.order_submitted_for_processing import OrderSubmittedForProcessing
from domain.order.exception.invalid_order_status import InvalidOrderStatus
from domain.order.exception.not_new_order_cant_fail_products_reservation import NotNewOrderCantFailProductsReservation
from domain.order.exception.only_new_order_can_be_marked_as_processing import OnlyNewOrderCanBeMarkedAsProcessing
from domain.order.exception.order_cant_contain_no_products import OrderCantContainNoProducts
from domain.order.value_object.ordered_product import OrderedProduct
from domain.service.value_object.customer_personal_info import CustomerPersonalInformation
from domain.service.value_object.note import Note
from domain.service.value_object.time_info import TimeInfo


@dataclass(kw_only=True, slots=True)
class Order(Entity, EventMixin):
    __hash__ = Entity.__hash__

    status: OrderStatus
    ordered_products: list[OrderedProduct]
    customer_personal_info: CustomerPersonalInformation
    customer_note: Note | None
    message_customer: bool
    time_info: TimeInfo

    @classmethod
    def new(
        cls,
        customer_note: str | None,
        message_customer: bool,
        customer_personal_info: CustomerPersonalInformation,
        ordered_products: list[OrderedProduct],
        status: OrderStatus,
    ) -> "Order":
        cls._check_order_has_products(ordered_products=ordered_products)

        new_order = cls(
            id=uuid4(),
            customer_note=None if customer_note is None else Note.new(content=customer_note),
            message_customer=message_customer,
            customer_personal_info=customer_personal_info,
            ordered_products=ordered_products,
            status=status,
            time_info=TimeInfo.new(
                created_at=datetime.now(),
            ),
        )

        return new_order

    def reserve_ordered_products(self) -> None:
        if not self.status.is_new:
            raise InvalidOrderStatus("Only a new order can reserve its products.")

        self._add_event(
            event=OrderCreated(
                order_id=self.id,
                products=self.ordered_products,
            ),
        )

    def start_processing(
        self,
        order_status: OrderStatus,
    ) -> None:
        if not self.status.is_new:
            raise OnlyNewOrderCanBeMarkedAsProcessing()

        if not order_status.is_processing:
            raise InvalidOrderStatus(
                f"You have to provide {BuiltInOrderStatus.PROCESSING} status to mark order as processing.",
            )

        self.set_status(order_status=order_status)

        self._add_event(
            event=OrderSubmittedForProcessing(
                products=self.ordered_products,
            ),
        )

    def mark_as_failed_for_products_reservation(
        self,
        order_status: OrderStatus,
    ) -> None:
        if not self.status.is_new:
            raise NotNewOrderCantFailProductsReservation()

        if not order_status.is_products_reservation_failed:
            raise InvalidOrderStatus(
                f"You have to provide {BuiltInOrderStatus.PRODUCTS_RESERVATION_FAILED} "
                "status for failed products reservation.",
            )

        self.set_status(order_status=order_status)

    def set_status(
        self,
        order_status: OrderStatus,
    ) -> None:
        self.status = order_status

    @staticmethod
    def _check_order_has_products(ordered_products: list[OrderedProduct]) -> None:
        if not ordered_products:
            raise OrderCantContainNoProducts()
