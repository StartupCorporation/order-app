from collections.abc import Callable

import pytest

from domain.order.entity.order import Order
from domain.order.entity.order_status import BuiltInOrderStatus, OrderStatus
from domain.order.events.order_created import OrderCreated
from domain.order.events.order_submitted_for_processing import OrderSubmittedForProcessing
from domain.order.exception.invalid_order_status import InvalidOrderStatus
from domain.order.exception.not_new_order_cant_fail_products_reservation import NotNewOrderCantFailProductsReservation
from domain.order.exception.only_new_order_can_be_marked_as_processing import OnlyNewOrderCanBeMarkedAsProcessing
from domain.order.exception.order_cant_contain_no_products import OrderCantContainNoProducts
from domain.order.value_object.ordered_product import OrderedProduct
from domain.service.value_object.customer_personal_info import CustomerPersonalInformation


def test_order_is_created(
    order_status_entity_factory: Callable[[BuiltInOrderStatus | str], OrderStatus],
    customer_personal_info_value_object: CustomerPersonalInformation,
    ordered_product_value_object: OrderedProduct,
) -> None:
    order_status_entity = order_status_entity_factory(BuiltInOrderStatus.NEW)

    order_entity = Order.new(
        customer_note="Some note",
        message_customer=True,
        customer_personal_info=customer_personal_info_value_object,
        ordered_products=[ordered_product_value_object],
        status=order_status_entity,
    )

    assert order_entity.time_info.created_at


def test_order_is_instantiated_without_customer_note(
    order_status_entity_factory: Callable[[BuiltInOrderStatus | str], OrderStatus],
    customer_personal_info_value_object: CustomerPersonalInformation,
    ordered_product_value_object: OrderedProduct,
) -> None:
    order_status_entity = order_status_entity_factory(BuiltInOrderStatus.NEW)

    order_entity = Order.new(
        customer_note=None,
        message_customer=True,
        customer_personal_info=customer_personal_info_value_object,
        ordered_products=[ordered_product_value_object],
        status=order_status_entity,
    )

    assert order_entity.time_info.created_at


def test_order_is_failed_to_instantiate_with_no_products(
    order_status_entity_factory: Callable[[BuiltInOrderStatus | str], OrderStatus],
    customer_personal_info_value_object: CustomerPersonalInformation,
) -> None:
    order_status_entity = order_status_entity_factory(BuiltInOrderStatus.NEW)

    with pytest.raises(OrderCantContainNoProducts):
        Order.new(
            customer_note=None,
            message_customer=True,
            customer_personal_info=customer_personal_info_value_object,
            ordered_products=[],
            status=order_status_entity,
        )


def test_order_can_reserve_products_if_it_is_new(
    order_entity_factory: Callable[[BuiltInOrderStatus | str], Order],
) -> None:
    order_entity = order_entity_factory(BuiltInOrderStatus.NEW)
    order_entity.reserve_ordered_products()

    events = order_entity.flush_events()

    assert len(events) == 1
    assert isinstance(events[0], OrderCreated)
    assert events[0].order_id == order_entity.id
    assert events[0].products == order_entity.ordered_products


@pytest.mark.parametrize(
    "order_status",
    [
        BuiltInOrderStatus.PROCESSING,
        BuiltInOrderStatus.FAILED,
        BuiltInOrderStatus.PRODUCTS_RESERVATION_FAILED,
        BuiltInOrderStatus.COMPLETED,
        "some_code",
    ],
)
def test_order_cant_reserve_products_if_not_new(
    order_status: BuiltInOrderStatus | str,
    order_entity_factory: Callable[[BuiltInOrderStatus | str], Order],
) -> None:
    order_entity = order_entity_factory(order_status)

    with pytest.raises(InvalidOrderStatus):
        order_entity.reserve_ordered_products()


def test_order_can_start_processing_if_products_are_reserved(
    order_status_entity_factory: Callable[[BuiltInOrderStatus | str], OrderStatus],
    order_entity_factory: Callable[[BuiltInOrderStatus | str], Order],
) -> None:
    processing_order_status_entity = order_status_entity_factory(BuiltInOrderStatus.PROCESSING)

    order_entity = order_entity_factory(BuiltInOrderStatus.NEW)
    order_entity.start_processing(
        order_status=processing_order_status_entity,
    )

    events = order_entity.flush_events()

    assert len(events) == 1
    assert isinstance(events[0], OrderSubmittedForProcessing)
    assert events[0].order_id == order_entity.id


@pytest.mark.parametrize(
    "order_status",
    [
        BuiltInOrderStatus.NEW,
        BuiltInOrderStatus.FAILED,
        BuiltInOrderStatus.PRODUCTS_RESERVATION_FAILED,
        BuiltInOrderStatus.COMPLETED,
        "some_code",
    ],
)
def test_order_cant_start_processing_if_invalid_order_status_passed(
    order_status: BuiltInOrderStatus | str,
    order_status_entity_factory: Callable[[BuiltInOrderStatus | str], OrderStatus],
    order_entity_factory: Callable[[BuiltInOrderStatus | str], Order],
) -> None:
    order_status_entity = order_status_entity_factory(order_status)

    order_entity = order_entity_factory(BuiltInOrderStatus.NEW)

    with pytest.raises(InvalidOrderStatus):
        order_entity.start_processing(
            order_status=order_status_entity,
        )


@pytest.mark.parametrize(
    "order_status",
    [
        BuiltInOrderStatus.PROCESSING,
        BuiltInOrderStatus.FAILED,
        BuiltInOrderStatus.PRODUCTS_RESERVATION_FAILED,
        BuiltInOrderStatus.COMPLETED,
        "some_code",
    ],
)
def test_order_cant_start_processing_if_it_is_not_new(
    order_status: BuiltInOrderStatus | str,
    order_status_entity_factory: Callable[[BuiltInOrderStatus | str], OrderStatus],
    order_entity_factory: Callable[[BuiltInOrderStatus | str], Order],
) -> None:
    order_status_entity = order_status_entity_factory(BuiltInOrderStatus.PROCESSING)

    order_entity = order_entity_factory(order_status)

    with pytest.raises(OnlyNewOrderCanBeMarkedAsProcessing):
        order_entity.start_processing(
            order_status=order_status_entity,
        )


def test_order_can_be_marked_as_failed_for_products_reservation_if_new(
    order_status_entity_factory: Callable[[BuiltInOrderStatus | str], OrderStatus],
    order_entity_factory: Callable[[BuiltInOrderStatus | str], Order],
) -> None:
    products_reservation_failed_order_status_entity = order_status_entity_factory(
        BuiltInOrderStatus.PRODUCTS_RESERVATION_FAILED,
    )

    order_entity = order_entity_factory(BuiltInOrderStatus.NEW)
    order_entity.mark_as_failed_for_products_reservation(
        order_status=products_reservation_failed_order_status_entity,
    )


@pytest.mark.parametrize(
    "order_status",
    [
        BuiltInOrderStatus.PROCESSING,
        BuiltInOrderStatus.FAILED,
        BuiltInOrderStatus.PRODUCTS_RESERVATION_FAILED,
        BuiltInOrderStatus.COMPLETED,
        "some_code",
    ],
)
def test_order_can_be_marked_as_failed_for_products_reservation_if_not_new(
    order_status: BuiltInOrderStatus | str,
    order_status_entity_factory: Callable[[BuiltInOrderStatus | str], OrderStatus],
    order_entity_factory: Callable[[BuiltInOrderStatus | str], Order],
) -> None:
    products_reservation_failed_order_status_entity = order_status_entity_factory(
        BuiltInOrderStatus.PRODUCTS_RESERVATION_FAILED,
    )

    order_entity = order_entity_factory(order_status)

    with pytest.raises(NotNewOrderCantFailProductsReservation):
        order_entity.mark_as_failed_for_products_reservation(
            order_status=products_reservation_failed_order_status_entity,
        )
