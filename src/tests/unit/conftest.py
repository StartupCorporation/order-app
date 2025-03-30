from collections.abc import Awaitable, Callable

import pytest
from dw_shared_kernel import EventBus, EventHandler, ModelEvent, ModelEventBus

from domain.order.repository.order import OrderRepository
from domain.order.repository.order_status import OrderStatusRepository
from domain.order.service.order import OrderService
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
