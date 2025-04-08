import json
from collections.abc import Awaitable, Callable

import jsonschema
import pytest
from aio_pika import IncomingMessage
from dw_shared_kernel import CommandBus, Container

from application.commands.start_order_processing.command import StartOrderProcessingCommand
from domain.order.entity.order import Order
from domain.order.entity.order_status import BuiltInOrderStatus, OrderStatus
from domain.order.repository.order import OrderRepository
from domain.order.repository.order_status import OrderStatusRepository
from infrastructure.settings.rabbitmq import RabbitMQSettings


@pytest.mark.asyncio
async def test_command_marks_order_as_processing_and_saves_it(
    di_container: Container,
    order_status_entity_factory: Callable[[BuiltInOrderStatus | str], OrderStatus],
    order_entity_factory: Callable[[BuiltInOrderStatus | str], Order],
    get_messages_from_queue: Callable[[str], Awaitable[list[IncomingMessage]]],
    purge_rabbitmq_queues: None,  # noqa: ARG001
    clean_db: None,  # noqa: ARG001
) -> None:
    order_repository = di_container[OrderRepository]
    order_status_repository = di_container[OrderStatusRepository]

    new_order_status_entity = order_status_entity_factory(BuiltInOrderStatus.NEW)
    processing_order_status_entity = order_status_entity_factory(BuiltInOrderStatus.PROCESSING)

    order_entity = order_entity_factory(BuiltInOrderStatus.NEW)
    order_entity.status = new_order_status_entity

    await order_status_repository.save(entity=new_order_status_entity)
    await order_status_repository.save(entity=processing_order_status_entity)
    await order_repository.save(entity=order_entity)

    await di_container[CommandBus].handle(
        command=StartOrderProcessingCommand(
            order_id=order_entity.id,
        ),
    )

    messages = await get_messages_from_queue(di_container[RabbitMQSettings].CATALOG_RESERVATION_QUEUE.NAME)

    assert len(messages) == 1

    order_processing_event_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "event_type": {"type": "string"},
            "created_at": {"type": "string"},
            "data": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "product_id": {"type": "string"},
                        "quantity": {"type": "integer"},
                    },
                },
            },
        },
    }

    event = json.loads(messages[0].body)
    try:
        jsonschema.validate(event, order_processing_event_schema)
    except Exception as e:
        pytest.fail(str(e))

    order_entity = await order_repository.get_by_id(id_=order_entity.id)
    orders = await order_repository.get_all()

    assert len(orders) == 1
    assert order_entity is not None
    assert order_entity.status.is_processing
