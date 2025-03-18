from dw_shared_kernel import Container, IntegrationEventRepository, Layer, CommandBus, EventBus, MessageBrokerPublisher

from domain.order.repository.order import OrderRepository
from domain.order.events.order_created import OrderCreated
from domain.order.events.order_submitted_for_processing import OrderSubmittedForProcessing
from domain.order.repository.order_status import OrderStatusRepository
from domain.order.service.order import OrderService
from infrastructure.bus.middleware.event_dispatcher import ModelEventDispatcherMiddleware
from infrastructure.bus.middleware.transaction import TransactionMiddleware
from infrastructure.database.base.transaction import DatabaseTransactionManager
from infrastructure.database.relational.connection import SQLConnectionManager
from infrastructure.database.relational.mapper.order import OrderEntityMapper
from infrastructure.database.relational.mapper.order_status import OrderStatusEntityMapper
from infrastructure.database.relational.repository.order import SQLOrderRepository
from infrastructure.database.relational.repository.order_status import SQLOrderStatusRepository
from infrastructure.database.relational.transaction import SQLTransactionManager
from infrastructure.message_broker.connection import RabbitMQConnectionManager
from infrastructure.message_broker.destination import RabbitMQEventDestination
from infrastructure.message_broker.publisher import RabbitMQPublisher
from infrastructure.settings.application import ApplicationSettings
from infrastructure.settings.database import DatabaseSettings
from infrastructure.settings.rabbitmq import RabbitMQSettings


class InfrastructureLayer(Layer):
    def setup(
        self,
        container: Container,
    ) -> None:
        container[ApplicationSettings] = ApplicationSettings()  # type: ignore
        container[DatabaseSettings] = DatabaseSettings()  # type: ignore
        container[RabbitMQSettings] = RabbitMQSettings()  # type: ignore

        container[RabbitMQConnectionManager] = RabbitMQConnectionManager(
            settings=container[RabbitMQSettings],
        )
        container[MessageBrokerPublisher] = RabbitMQPublisher(
            connection_manager=container[RabbitMQConnectionManager],
        )
        container[SQLConnectionManager] = SQLConnectionManager(
            database_settings=container[DatabaseSettings],
        )
        container[DatabaseTransactionManager] = SQLTransactionManager(
            connection_manager=container[SQLConnectionManager],
        )
        container[TransactionMiddleware] = TransactionMiddleware(
            transaction_manager=container[DatabaseTransactionManager],
        )
        container[ModelEventDispatcherMiddleware] = ModelEventDispatcherMiddleware(
            integration_event_repository=container[IntegrationEventRepository],
            message_broker_publisher=container[MessageBrokerPublisher],
        )

        container[CommandBus].add_middlewares(
            middlewares=[
                container[TransactionMiddleware],
            ],
        )
        container[EventBus].add_middlewares(
            middlewares=[
                container[ModelEventDispatcherMiddleware],
            ],
        )

        container[OrderEntityMapper] = OrderEntityMapper()
        container[OrderStatusEntityMapper] = OrderStatusEntityMapper()

        container[OrderStatusRepository] = SQLOrderStatusRepository(
            order_status_mapper=container[OrderStatusEntityMapper],
            connection_manager=container[SQLConnectionManager],
        )
        container[OrderRepository] = SQLOrderRepository(
            order_entity_mapper=container[OrderEntityMapper],
            connection_manager=container[SQLConnectionManager],
        )

        container[OrderService] = OrderService(
            event_bus=container[EventBus],
            order_status_repository=container[OrderStatusRepository],
            order_repository=container[OrderRepository],
        )

        container[IntegrationEventRepository].add_event_destination(
            event=OrderCreated,
            destination=RabbitMQEventDestination(
                routing_key=container[RabbitMQSettings].CATALOG_RESERVATION_QUEUE.NAME,
                exchange=container[RabbitMQSettings].CATALOG_RESERVATION_QUEUE.EXCHANGE,
            ),
        )
        container[IntegrationEventRepository].add_event_destination(
            event=OrderSubmittedForProcessing,
            destination=RabbitMQEventDestination(
                routing_key=container[RabbitMQSettings].CATALOG_RESERVATION_QUEUE.NAME,
                exchange=container[RabbitMQSettings].CATALOG_RESERVATION_QUEUE.EXCHANGE,
            ),
        )
