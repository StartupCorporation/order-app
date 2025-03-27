from collections.abc import Awaitable, Callable
from uuid import uuid4

import pytest
from dw_shared_kernel import EventBus, EventHandler, ModelEvent, ModelEventBus

from domain.order.entity.order import Order
from domain.order.entity.order_status import BuiltInOrderStatus, OrderStatus
from domain.order.repository.order import OrderRepository
from domain.order.repository.order_status import OrderStatusRepository
from domain.order.service.order import OrderService
from domain.order.value_object.ordered_product import OrderedProduct
from domain.service.value_object.customer_personal_info import CustomerPersonalInformation
from infrastructure.database.in_memory.repository.callback_request import InMemoryCallbackRequestRepository
from infrastructure.database.in_memory.repository.order import InMemoryOrderRepository
from infrastructure.database.in_memory.repository.order_status import InMemoryOrderStatusRepository


@pytest.fixture
def order_service(
    order_status_repository: OrderStatusRepository,
    order_repository: OrderRepository,
    model_event_bus: ModelEventBus,
) -> OrderService:
    return OrderService(
        order_status_repository=order_status_repository,
        order_repository=order_repository,
        event_bus=model_event_bus,
    )


@pytest.fixture
def model_event_bus() -> EventBus:
    return EventBus()


@pytest.fixture
def order_status_repository() -> InMemoryOrderStatusRepository:
    return InMemoryOrderStatusRepository()


@pytest.fixture
def order_repository() -> InMemoryOrderRepository:
    return InMemoryOrderRepository()


@pytest.fixture
def callback_request_repository() -> InMemoryCallbackRequestRepository:
    return InMemoryCallbackRequestRepository()


@pytest.fixture
def event_handler_factory[EVENT: ModelEvent]() -> Callable[[Callable[[EVENT], Awaitable[None]]], EventHandler[EVENT]]:
    class TestEventHandler(EventHandler[EVENT]):
        def __init__(
            self,
            body: Callable[[EVENT], Awaitable[None]],
        ) -> None:
            self._body = body

        async def __call__(self, event: EVENT) -> None:
            return await self._body(event)

    def factory(body: Callable[[EVENT], Awaitable[None]]) -> EventHandler[EVENT]:
        return TestEventHandler(
            body=body,
        )

    return factory


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
