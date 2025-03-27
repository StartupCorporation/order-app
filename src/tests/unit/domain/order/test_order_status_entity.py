from uuid import uuid4

import pytest

from domain.order.entity.order_status import BuiltInOrderStatus, OrderStatus
from domain.order.exception.new_order_status_code_duplicates_builtin_codes import (
    NewOrderStatusCodeDuplicatesBuiltInCode,
)
from domain.order.exception.order_status_code_cant_be_empty import OrderStatusCodeCantBeEmpty
from domain.order.exception.order_status_code_is_long import OrderStatusCodeIsLong
from domain.order.exception.order_status_description_cant_be_empty import OrderStatusDescriptionCantBeEmpty
from domain.order.exception.order_status_description_is_long import OrderStatusDescriptionIsLong
from domain.order.exception.order_status_name_cant_be_empty import OrderStatusNameCantBeEmpty
from domain.order.exception.order_status_name_is_long import OrderStatusNameIsLong


def test_order_status_can_be_created_with_valid_data() -> None:
    OrderStatus.new(
        code="code",
        name="some name",
        description="some desc",
    )


def test_order_status_cant_be_created_if_code_is_empty_string() -> None:
    with pytest.raises(OrderStatusCodeCantBeEmpty):
        OrderStatus.new(
            code="",
            name="some name",
            description="some desc",
        )


def test_order_status_cant_be_created_if_code_is_longer_128_chars() -> None:
    with pytest.raises(OrderStatusCodeIsLong):
        OrderStatus.new(
            code="1" * 129,
            name="some name",
            description="some desc",
        )


def test_order_status_cant_be_created_if_code_is_builtin() -> None:
    for status in BuiltInOrderStatus:
        with pytest.raises(NewOrderStatusCodeDuplicatesBuiltInCode):
            OrderStatus.new(
                code=status,
                name="some name",
                description="some desc",
            )


def test_order_status_cant_be_created_if_name_is_longer_128_chars() -> None:
    with pytest.raises(OrderStatusNameIsLong):
        OrderStatus.new(
            code="code",
            name="2" * 129,
            description="some desc",
        )


def test_order_status_cant_be_created_if_name_is_empty_string() -> None:
    with pytest.raises(OrderStatusNameCantBeEmpty):
        OrderStatus.new(
            code="code",
            name="",
            description="some desc",
        )


def test_order_status_cant_be_created_if_description_is_empty_string() -> None:
    with pytest.raises(OrderStatusDescriptionCantBeEmpty):
        OrderStatus.new(
            code="code",
            name="name",
            description="",
        )


def test_order_status_cant_be_created_if_description_is_longer_512_chars() -> None:
    with pytest.raises(OrderStatusDescriptionIsLong):
        OrderStatus.new(
            code="code",
            name="name",
            description="3" * 513,
        )


def test_order_status_can_be_created_without_description() -> None:
    OrderStatus.new(
        code="code",
        name="name",
        description=None,
    )


def test_order_status_is_new_if_code_is_builtin_new() -> None:
    entity = OrderStatus(
        id=uuid4(),
        code=BuiltInOrderStatus.NEW,
        name="name",
        description=None,
    )

    assert entity.is_new


def test_order_status_is_processing_if_code_is_builtin_processing() -> None:
    entity = OrderStatus(
        id=uuid4(),
        code=BuiltInOrderStatus.PROCESSING,
        name="name",
        description=None,
    )

    assert entity.is_processing


def test_order_status_is_products_reservation_failed_if_code_is_builtin_products_reserveation_failed() -> None:
    entity = OrderStatus(
        id=uuid4(),
        code=BuiltInOrderStatus.PRODUCTS_RESERVATION_FAILED,
        name="name",
        description=None,
    )

    assert entity.is_products_reservation_failed
