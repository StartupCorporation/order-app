from collections.abc import Callable
from uuid import uuid4

import pytest

from domain.order.entity.order import Order
from domain.order.entity.order_status import BuiltInOrderStatus, OrderStatus
from domain.order.value_object.ordered_product import OrderedProduct
from domain.service.value_object.customer_personal_info import CustomerPersonalInformation


@pytest.fixture
def order_status_entity_factory() -> Callable[[BuiltInOrderStatus | str], OrderStatus]:
    def factory(order_status: BuiltInOrderStatus | str) -> OrderStatus:
        code = order_status.value if isinstance(order_status, BuiltInOrderStatus) else order_status
        name = order_status.name if isinstance(order_status, BuiltInOrderStatus) else order_status

        return OrderStatus(
            id=uuid4(),
            code=code,
            name=name,
            description=None,
        )

    return factory


@pytest.fixture
def customer_personal_info_value_object() -> CustomerPersonalInformation:
    return CustomerPersonalInformation.new(
        name="Test",
        email="some@email.com",
        phone_number="+380661234567",
    )


@pytest.fixture
def ordered_product_value_object() -> OrderedProduct:
    return OrderedProduct.new(
        product_id=uuid4(),
        quantity=2,
    )


@pytest.fixture
def order_entity_factory(
    order_status_entity_factory: Callable[[BuiltInOrderStatus | str], OrderStatus],
    customer_personal_info_value_object: CustomerPersonalInformation,
    ordered_product_value_object: OrderedProduct,
) -> Callable[[BuiltInOrderStatus | str], Order]:
    def factory(order_status: BuiltInOrderStatus | str) -> Order:
        return Order.new(
            customer_note="Note",
            message_customer=True,
            customer_personal_info=customer_personal_info_value_object,
            ordered_products=[ordered_product_value_object],
            status=order_status_entity_factory(order_status),
        )

    return factory
