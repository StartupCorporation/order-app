from aio_pika import Message
from aio_pika.abc import AbstractExchange, DeliveryMode
from dw_shared_kernel import MessageBrokerPublisher
from infrastructure.message_broker.connection import RabbitMQConnectionManager
from infrastructure.message_broker.destination import RabbitMQEventDestination


class RabbitMQPublisher(MessageBrokerPublisher[RabbitMQEventDestination]):
    def __init__(
        self,
        connection_manager: RabbitMQConnectionManager,
    ):
        self._connection_manager = connection_manager

    async def publish(
        self,
        message: bytes,
        destination: RabbitMQEventDestination,
    ) -> None:
        async with self._connection_manager.connect() as channel:
            exchange: AbstractExchange = await channel.get_exchange(destination.exchange)
            await exchange.publish(
                message=Message(
                    body=message,
                    delivery_mode=DeliveryMode.PERSISTENT,
                ),
                routing_key=destination.routing_key,
            )
