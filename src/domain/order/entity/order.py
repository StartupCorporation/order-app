from dataclasses import dataclass
from datetime import datetime
from enum import auto
from typing import ClassVar, cast
from uuid import uuid4

from dw_shared_kernel import (
    ChangeTrackerMixin,
    Entity,
    EventMixin,
    Change,
    ValueCreatedChange,
    ValueNameEnum,
)

from domain.order.exception.string_can_be_emtpy import StringCantBeEmpty
from domain.order.exception.string_value_too_big import StringValueTooBig
from domain.order.exception.order_cant_contain_no_products import OrderCantContainNoProducts
from domain.order.exception.only_new_order_can_be_marked_as_processing import OnlyNewOrderCanBeMarkedAsProcessing
from domain.order.exception.invalid_order_status import InvalidOrderStatus
from domain.order.exception.not_new_order_cant_fail_products_reservation import NotNewOrderCantFailProductsReservation
from domain.order.events.order_submitted_for_processing import OrderSubmittedForProcessing
from domain.order.events.order_created import OrderCreated
from domain.order.entity.order_status import BuiltInOrderStatus, OrderStatus
from domain.order.value_object.customer_personal_info import CustomerPersonalInformation
from domain.order.value_object.order_product import OrderedProduct


@dataclass(kw_only=True)
class Order(Entity, EventMixin, ChangeTrackerMixin):
    customer_comment: str | None
    message_customer: bool
    customer_personal_info: CustomerPersonalInformation
    ordered_products: list[OrderedProduct]
    status: OrderStatus
    created_at: datetime

    @classmethod
    def new(
        cls,
        customer_comment: str | None,
        message_customer: bool,
        customer_personal_info: CustomerPersonalInformation,
        ordered_products: list[OrderedProduct],
        status: OrderStatus,
    ) -> "Order":
        cls._check_customer_comment(customer_comment=customer_comment)
        cls._check_order_has_products(ordered_products=ordered_products)

        new_order = cls(
            id=uuid4(),
            customer_comment=customer_comment,
            message_customer=message_customer,
            customer_personal_info=customer_personal_info,
            ordered_products=ordered_products,
            status=status,
            created_at=datetime.now(),
        )
        new_order._add_change(
            change=ValueCreatedChange(),
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
                order_id=self.id,
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
        if not self._has_change(change_name=OrderEntityChangeName.INITIAL_STATUS_REPLACED):
            self._add_change(
                change=InitialStatusReplacedChange(
                    initial_status=self.status,
                ),
            )

        self.status = order_status

    @staticmethod
    def _check_customer_comment(customer_comment: str | None) -> None:
        if not (customer_comment is None or customer_comment.strip()):
            raise StringCantBeEmpty("Order comment can't be empty.")

        if len(cast(str, customer_comment)) > 512:
            raise StringValueTooBig("Order comment too long.")

    @staticmethod
    def _check_order_has_products(ordered_products: list[OrderedProduct]) -> None:
        if not ordered_products:
            raise OrderCantContainNoProducts()


class OrderEntityChangeName(ValueNameEnum):
    INITIAL_STATUS_REPLACED = auto()


@dataclass(kw_only=True, frozen=True)
class InitialStatusReplacedChange(Change):
    name: ClassVar[str] = OrderEntityChangeName.INITIAL_STATUS_REPLACED
    initial_status: OrderStatus
