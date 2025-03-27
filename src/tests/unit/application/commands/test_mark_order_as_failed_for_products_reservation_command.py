from collections.abc import Callable
from uuid import uuid4

import pytest

from application.commands.mark_order_as_failed_for_products_reservation.command import (
    MarkOrderAsFailedForProductsReservationCommand,
)
from application.commands.mark_order_as_failed_for_products_reservation.handler import (
    MarkOrderAsFailedForProductsReservationCommandHandler,
)
from domain.order.entity.order import Order
from domain.order.entity.order_status import BuiltInOrderStatus, OrderStatus
from domain.order.repository.order import OrderRepository
from domain.order.repository.order_status import OrderStatusRepository
from domain.order.service.order import OrderService


@pytest.mark.asyncio
async def test_if_no_order_found_do_nothing(
    order_service: OrderService,
    order_repository: OrderRepository,
) -> None:
    handler = MarkOrderAsFailedForProductsReservationCommandHandler(
        order_repository=order_repository,
        order_service=order_service,
    )

    await handler(
        command=MarkOrderAsFailedForProductsReservationCommand(
            order_id=uuid4(),
        ),
    )


@pytest.mark.asyncio
async def test_command_handler_marks_order_as_reservation_failed(
    order_service: OrderService,
    order_repository: OrderRepository,
    order_status_repository: OrderStatusRepository,
    order_status_entity_factory: Callable[[BuiltInOrderStatus | str], OrderStatus],
    order_entity_factory: Callable[[BuiltInOrderStatus | str], Order],
) -> None:
    order_entity = order_entity_factory(BuiltInOrderStatus.NEW)
    reservation_failed_status_entity = order_status_entity_factory(BuiltInOrderStatus.PRODUCTS_RESERVATION_FAILED)

    await order_repository.save(entity=order_entity)
    await order_status_repository.save(entity=reservation_failed_status_entity)

    handler = MarkOrderAsFailedForProductsReservationCommandHandler(
        order_repository=order_repository,
        order_service=order_service,
    )

    await handler(
        command=MarkOrderAsFailedForProductsReservationCommand(
            order_id=order_entity.id,
        ),
    )

    records = await order_repository.get_all()

    assert len(records) == 1
    assert records[0].status.is_products_reservation_failed
