from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import aio_pika
from aio_pika.abc import AbstractChannel

from infrastructure.settings.rabbitmq import RabbitMQSettings


class RabbitMQConnectionManager:
    def __init__(
        self,
        settings: RabbitMQSettings,
    ):
        self._settings = settings

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AbstractChannel]:
        connection = await aio_pika.connect_robust(self._settings.connection_url, timeout=5)
        async with connection:
            yield await connection.channel()
