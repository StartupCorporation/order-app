from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from aio_pika import Channel
from aio_pika.abc import AbstractChannel
from asyncpg import Connection
from dw_shared_kernel import Container, SharedKernelInfrastructureLayer, get_di_container

from application.layer import ApplicationLayer
from infrastructure.database.relational.connection import SQLConnectionManager
from infrastructure.layer import InfrastructureLayer
from infrastructure.message_broker.rabbitmq.connection import RabbitMQConnectionManager
from infrastructure.settings.rabbitmq import RabbitMQSettings


@pytest_asyncio.fixture
async def clean_db(db_connection: Connection) -> AsyncIterator[None]:
    yield
    await db_connection.execute("""
    TRUNCATE callback_request, order_;
    """)


@pytest_asyncio.fixture
async def purge_rabbitmq_queues(
    rabbitmq_connection: Channel,
    di_container: Container,
) -> AsyncIterator[None]:
    yield
    rabbitmq_settings = di_container[RabbitMQSettings]
    queue = await rabbitmq_connection.get_queue(rabbitmq_settings.CATALOG_RESERVATION_QUEUE.NAME)
    await queue.purge()


@pytest_asyncio.fixture
async def db_connection(di_container: Container) -> AsyncIterator[Connection]:
    connection_manager = di_container[SQLConnectionManager]

    async with connection_manager.connect() as con:
        yield con


@pytest_asyncio.fixture
async def rabbitmq_connection(di_container: Container) -> AsyncIterator[AbstractChannel]:
    rabbitmq_connection_manager = di_container[RabbitMQConnectionManager]
    async with rabbitmq_connection_manager.connect() as connection:
        yield connection


@pytest.fixture(scope="session")
def di_container() -> Container:
    return get_di_container(
        layers=(
            SharedKernelInfrastructureLayer(),
            InfrastructureLayer(),
            ApplicationLayer(),
        ),
    )
