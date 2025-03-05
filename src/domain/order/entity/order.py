from dataclasses import dataclass
from typing import cast
from uuid import uuid4

from dw_shared_kernel import (
    Entity,
    EventMixin,
)

from domain.order.exception.order_cant_contain_no_products import OrderCantContainNoProducts
from domain.order.exception.order_comment_cant_be_empty import OrderCommentCantBeEmtpy
from domain.order.exception.order_comment_too_long import OrderCommentTooLong
from domain.order.exception.only_new_order_can_be_marked_as_processing import OnlyNewOrderCanBeMarkedAsProcessing
from domain.order.exception.invalid_order_status import InvalidOrderStatus
from domain.order.exception.not_new_order_cant_fail_products_reservation import NotNewOrderCantFailProductsReservation
from domain.order.events.order_submitted_for_processing import OrderSubmittedForProcessing
from domain.order.events.order_created import OrderCreated
from domain.order.entity.order_status import BuiltInOrderStatus, OrderStatus
from domain.order.value_object.client_personal_info import ClientPersonalInformation
from domain.order.value_object.order_product import OrderedProduct


@dataclass(kw_only=True)
class Order(Entity, EventMixin):
    client_comment: str | None
    contact_client: bool
    client_personal_info: ClientPersonalInformation
    ordered_products: list[OrderedProduct]
    status: OrderStatus

    @classmethod
    def new(
        cls,
        client_comment: str | None,
        contact_client: bool,
        client_personal_info: ClientPersonalInformation,
        ordered_products: list[OrderedProduct],
        status: OrderStatus,
    ) -> "Order":
        cls._check_client_comment(client_comment=client_comment)
        cls._check_ordered_products(ordered_products=ordered_products)

        return cls(
            id=uuid4(),
            client_comment=client_comment,
            contact_client=contact_client,
            client_personal_info=client_personal_info,
            ordered_products=ordered_products,
            status=status,
        )

    def reserve_ordered_products(self) -> None:
        if not self.status.is_new:
            raise InvalidOrderStatus("Only a new order can reserve its products.")

        self._add_event(
            event=OrderCreated(
                order_id=self.id,
                products=self.ordered_products,
            ),
        )

    def mark_for_processing(
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

        if order_status.is_products_reservation_failed:
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
    def _check_client_comment(client_comment: str | None) -> None:
        if not (client_comment is None or client_comment):
            raise OrderCommentCantBeEmtpy()

        if len(cast(str, client_comment)) > 512:
            raise OrderCommentTooLong()

    @staticmethod
    def _check_ordered_products(ordered_products: list[OrderedProduct]) -> None:
        if not ordered_products:
            raise OrderCantContainNoProducts()
