from collections.abc import Callable
from uuid import uuid4

import pytest

from application.commands.create_order.command import CreateOrderCommand, CustomerPersonalInfoInput, ProductInput
from application.commands.create_order.handler import CreateOrderCommandHandler
from domain.order.entity.order_status import BuiltInOrderStatus, OrderStatus
from domain.order.repository.order import OrderRepository
from domain.order.repository.order_status import OrderStatusRepository
from domain.order.service.order import OrderService


@pytest.mark.asyncio
async def test_command_handler_stores_callback_request(
    order_repository: OrderRepository,
    order_service: OrderService,
    order_status_repository: OrderStatusRepository,
    order_status_entity_factory: Callable[[BuiltInOrderStatus | str], OrderStatus],
) -> None:
    handler = CreateOrderCommandHandler(
        order_service=order_service,
    )

    await order_status_repository.save(
        entity=order_status_entity_factory(BuiltInOrderStatus.NEW),
    )

    assert not await order_repository.get_all()

    await handler(
        command=CreateOrderCommand(
            message_customer=True,
            customer_note=None,
            customer_personal_information=CustomerPersonalInfoInput(
                name="name",
                email="email@email.com",
                phone_number="+380661234567",
            ),
            ordered_products=[
                ProductInput(
                    product_id=uuid4(),
                    quantity=1,
                ),
            ],
        ),
    )

    records = await order_repository.get_all()
    assert len(records) == 1
    assert records[0].status.is_new
