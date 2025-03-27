from collections.abc import Awaitable, Callable

import pytest
from dw_shared_kernel import EventBus, EventHandler

from domain.order.entity.order import Order
from domain.order.entity.order_status import BuiltInOrderStatus, OrderStatus
from domain.order.events.order_created import OrderCreated
from domain.order.events.order_submitted_for_processing import OrderSubmittedForProcessing
from domain.order.exception.order_status_not_found import OrderStatusNotFound
from domain.order.repository.order import OrderRepository
from domain.order.repository.order_status import OrderStatusRepository
from domain.order.service.order import OrderService
from domain.order.value_object.ordered_product import OrderedProduct
from domain.service.value_object.customer_personal_info import CustomerPersonalInformation


@pytest.mark.asyncio
async def test_creating_new_order_raises_exception_if_new_order_status_not_exist(
    order_service: OrderService,
    ordered_product_value_object: OrderedProduct,
    customer_personal_info_value_object: CustomerPersonalInformation,
) -> None:
    with pytest.raises(OrderStatusNotFound):
        await order_service.create_new_order(
            customer_personal_information=customer_personal_info_value_object,
            ordered_products=[ordered_product_value_object],
            customer_note=None,
            message_customer=True,
        )


@pytest.mark.asyncio
async def test_create_new_order_stores_order_and_publishes_event(
    order_service: OrderService,
    order_status_entity_factory: Callable[[BuiltInOrderStatus | str], OrderStatus],
    order_repository: OrderRepository,
    order_status_repository: OrderStatusRepository,
    ordered_product_value_object: OrderedProduct,
    customer_personal_info_value_object: CustomerPersonalInformation,
    event_handler_factory: Callable[[Callable[[OrderCreated], Awaitable[None]]], EventHandler[OrderCreated]],
    model_event_bus: EventBus,
) -> None:
    async def event_handler(event: OrderCreated) -> None:
        nonlocal submited_event
        submited_event = event

    submited_event = None

    assert not await order_repository.get_all()
    model_event_bus.register(
        event=OrderCreated,
        handler=event_handler_factory(event_handler),
    )

    await order_status_repository.save(entity=order_status_entity_factory(BuiltInOrderStatus.NEW))
    await order_service.create_new_order(
        customer_personal_information=customer_personal_info_value_object,
        ordered_products=[ordered_product_value_object],
        customer_note=None,
        message_customer=True,
    )

    orders = await order_repository.get_all()

    assert orders
    assert len(orders) == 1
    assert isinstance(submited_event, OrderCreated)
    assert submited_event.order_id == orders[0].id
    assert submited_event.products == orders[0].ordered_products


@pytest.mark.asyncio
async def test_mark_order_as_failed_raises_exception_if_corresponding_status_not_exist(
    order_service: OrderService,
    order_entity_factory: Callable[[BuiltInOrderStatus | str], Order],
) -> None:
    order_entity = order_entity_factory("code")

    with pytest.raises(OrderStatusNotFound):
        await order_service.mark_order_as_failed_for_products_reservation(order=order_entity)


@pytest.mark.asyncio
async def test_mark_order_as_failed_changes_its_status_and_stores_updated_order(
    order_service: OrderService,
    order_status_entity_factory: Callable[[BuiltInOrderStatus | str], OrderStatus],
    order_repository: OrderRepository,
    order_status_repository: OrderStatusRepository,
    order_entity_factory: Callable[[BuiltInOrderStatus | str], Order],
) -> None:
    order_entity = order_entity_factory(BuiltInOrderStatus.NEW)
    failed_order_status_entity = order_status_entity_factory(BuiltInOrderStatus.PRODUCTS_RESERVATION_FAILED)

    await order_repository.save(entity=order_entity)
    await order_status_repository.save(entity=failed_order_status_entity)

    await order_service.mark_order_as_failed_for_products_reservation(order=order_entity)

    orders = await order_repository.get_all()

    assert orders
    assert len(orders) == 1
    assert orders[0].status.is_products_reservation_failed


@pytest.mark.asyncio
async def test_start_order_processing_raises_exception_if_corresponding_status_not_exist(
    order_service: OrderService,
    order_entity_factory: Callable[[BuiltInOrderStatus | str], Order],
) -> None:
    order_entity = order_entity_factory("code")

    with pytest.raises(OrderStatusNotFound):
        await order_service.start_order_processing(order=order_entity)


@pytest.mark.asyncio
async def test_start_order_processing_stores_order_and_publishes_events(
    order_service: OrderService,
    order_entity_factory: Callable[[BuiltInOrderStatus | str], Order],
    order_status_entity_factory: Callable[[BuiltInOrderStatus | str], OrderStatus],
    order_repository: OrderRepository,
    order_status_repository: OrderStatusRepository,
    event_handler_factory: Callable[
        [Callable[[OrderSubmittedForProcessing], Awaitable[None]]],
        EventHandler[OrderSubmittedForProcessing],
    ],
    model_event_bus: EventBus,
) -> None:
    async def event_handler(event: OrderSubmittedForProcessing) -> None:
        nonlocal submited_event
        submited_event = event

    submited_event = None

    order_entity = order_entity_factory(BuiltInOrderStatus.NEW)
    processing_order_status_entity = order_status_entity_factory(BuiltInOrderStatus.PROCESSING)

    await order_repository.save(entity=order_entity)
    await order_status_repository.save(entity=processing_order_status_entity)

    model_event_bus.register(
        event=OrderSubmittedForProcessing,
        handler=event_handler_factory(event_handler),
    )

    await order_service.start_order_processing(order=order_entity)

    orders = await order_repository.get_all()

    assert orders
    assert len(orders) == 1
    assert orders[0].status.is_processing
    assert isinstance(submited_event, OrderSubmittedForProcessing)
    assert submited_event.order_id == order_entity.id
