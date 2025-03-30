from collections.abc import Callable

import pytest
from dw_shared_kernel import CommandBus, Container

from application.commands.mark_order_as_failed_for_products_reservation.command import (
    MarkOrderAsFailedForProductsReservationCommand,
)
from domain.order.entity.order import Order
from domain.order.entity.order_status import BuiltInOrderStatus, OrderStatus
from domain.order.repository.order import OrderRepository
from domain.order.repository.order_status import OrderStatusRepository


@pytest.mark.asyncio
async def test_command_marks_order_as_failed_to_reserve_and_saves_it(
    di_container: Container,
    order_status_entity_factory: Callable[[BuiltInOrderStatus | str], OrderStatus],
    order_entity_factory: Callable[[BuiltInOrderStatus | str], Order],
    clean_db: None,  # noqa: ARG001
) -> None:
    order_repository = di_container[OrderRepository]
    order_status_repository = di_container[OrderStatusRepository]

    new_order_status_entity = order_status_entity_factory(BuiltInOrderStatus.NEW)
    failed_to_reserve_order_status_entity = order_status_entity_factory(BuiltInOrderStatus.PRODUCTS_RESERVATION_FAILED)

    order_entity = order_entity_factory(BuiltInOrderStatus.NEW)
    order_entity.status = new_order_status_entity

    await order_status_repository.save(entity=new_order_status_entity)
    await order_status_repository.save(entity=failed_to_reserve_order_status_entity)
    await order_repository.save(entity=order_entity)

    await di_container[CommandBus].handle(
        command=MarkOrderAsFailedForProductsReservationCommand(
            order_id=order_entity.id,
        ),
    )

    order_entity = await order_repository.get_by_id(id_=order_entity.id)
    orders = await order_repository.get_all()

    assert len(orders) == 1
    assert order_entity is not None
    assert order_entity.status.is_products_reservation_failed
