import json
from datetime import datetime
from uuid import UUID, uuid4

import jsonschema
import pytest
from aio_pika import Channel, IncomingMessage, Queue
from dw_shared_kernel import Container
from httpx import AsyncClient

from domain.order.repository.order import OrderRepository
from infrastructure.settings.rabbitmq import RabbitMQSettings


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "customer_note",
    [
        "some note",
        None,
    ],
)
async def test_create_order_endpoint_works_correctly_without_mock(
    customer_note: str,
    api_client: AsyncClient,
    di_container: Container,
    rabbitmq_connection: Channel,
    order_created_event_schema: dict[str, dict | str],
    purge_rabbitmq_queues: None,  # noqa: ARG001
    clean_db: None,  # noqa: ARG001
) -> None:
    repository = di_container[OrderRepository]

    orders = await repository.get_all()
    assert not orders

    request_data = {
        "messageCustomer": True,
        "customerComment": customer_note,
        "products": [
            {
                "productId": str(uuid4()),
                "quantity": 5,
            },
        ],
        "personalInformation": {
            "name": "John",
            "email": "email@email.com",
            "phoneNumber": "+380664887607",
        },
    }
    response = await api_client.post(
        url="/order/",
        json=request_data,
    )

    assert response.status_code == 201
    assert response.json() is None

    orders = await repository.get_all()

    assert len(orders) == 1
    assert orders[0].message_customer == request_data["messageCustomer"]
    assert (
        orders[0].customer_note.content == request_data["customerComment"]  # type: ignore
        if customer_note
        else orders[0].customer_note is None
    )
    assert orders[0].customer_personal_info.name == request_data["personalInformation"]["name"]
    assert orders[0].customer_personal_info.email == request_data["personalInformation"]["email"]
    assert orders[0].customer_personal_info.phone_number == request_data["personalInformation"]["phoneNumber"]
    assert len(orders[0].ordered_products) == 1
    assert orders[0].ordered_products[0].product_id == UUID(request_data["products"][0]["productId"])
    assert orders[0].ordered_products[0].quantity == request_data["products"][0]["quantity"]

    rabbitmq_settings = di_container[RabbitMQSettings]
    queue: Queue = await rabbitmq_connection.get_queue(rabbitmq_settings.CATALOG_RESERVATION_QUEUE.NAME)  # type: ignore

    messages: list[IncomingMessage] = []
    while True:
        message = await queue.get(
            no_ack=True,
            fail=False,
        )
        if not message:
            break
        messages.append(message)

    assert len(messages) == 1

    event = json.loads(messages[0].body)
    try:
        jsonschema.validate(event, order_created_event_schema)
    except Exception as e:
        pytest.fail(str(e))

    UUID(event["id"])
    UUID(event["data"]["order_id"])
    assert event["event_type"] == "ORDER_CREATED"
    assert datetime.fromisoformat(event["created_at"])
    assert len(event["data"]["products"]) == 1
    assert event["data"]["products"][0]["quantity"] == request_data["products"][0]["quantity"]
    assert event["data"]["products"][0]["product_id"] == request_data["products"][0]["productId"]
