from dw_shared_kernel import (
    CommandBus,
    Container,
    EventBus,
    IntegrationEventRepository,
    Layer,
    LifecycleComponentRepository,
    MessageBrokerPublisher,
)

from domain.order.events.order_created import OrderCreated
from domain.order.events.order_submitted_for_processing import OrderSubmittedForProcessing
from domain.order.repository.order import OrderRepository
from domain.order.repository.order_status import OrderStatusRepository
from domain.order.service.mail import OrderMailService
from domain.order.service.order import OrderService
from domain.service.repository.callback_request import CallbackRequestRepository
from domain.service.service.mail import ServiceMailService
from infrastructure.bus.middleware.event_dispatcher import ModelEventDispatcherMiddleware
from infrastructure.bus.middleware.transaction import TransactionMiddleware
from infrastructure.clients.catalog.client import CatalogClient
from infrastructure.clients.http_ import HTTPClient
from infrastructure.clients.iac.client import IACClient
from infrastructure.clients.smtp import SMTPClient
from infrastructure.database.base.transaction import DatabaseTransactionManager
from infrastructure.database.relational.connection import SQLConnectionManager
from infrastructure.database.relational.mapper.callback_request import CallbackRequestEntityMapper
from infrastructure.database.relational.mapper.order import OrderEntityMapper
from infrastructure.database.relational.mapper.order_status import OrderStatusEntityMapper
from infrastructure.database.relational.repository.callback_request import SQLCallbackRequestRepository
from infrastructure.database.relational.repository.order import SQLOrderRepository
from infrastructure.database.relational.repository.order_status import SQLOrderStatusRepository
from infrastructure.database.relational.transaction import SQLTransactionManager
from infrastructure.message_broker.rabbitmq.connection import RabbitMQConnectionManager
from infrastructure.message_broker.rabbitmq.destination import RabbitMQEventDestination
from infrastructure.message_broker.rabbitmq.publisher import RabbitMQPublisher
from infrastructure.service.mail import SMTPMailService
from infrastructure.settings.application import ApplicationSettings
from infrastructure.settings.catalog import CatalogServiceSettings
from infrastructure.settings.database import DatabaseSettings
from infrastructure.settings.iac import IACSettings
from infrastructure.settings.rabbitmq import RabbitMQSettings
from infrastructure.settings.smtp import SMTPSettings


class InfrastructureLayer(Layer):

    def setup(
        self,
        container: Container,
    ) -> None:
        container[ApplicationSettings] = ApplicationSettings()  # type: ignore
        container[DatabaseSettings] = DatabaseSettings()  # type: ignore
        container[RabbitMQSettings] = RabbitMQSettings()  # type: ignore
        container[SMTPSettings] = SMTPSettings()  # type: ignore
        container[IACSettings] = IACSettings()  # type: ignore
        container[CatalogServiceSettings] = CatalogServiceSettings()  # type: ignore

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

        container[SMTPClient] = SMTPClient(
            smtp_settings=container[SMTPSettings],
        )
        container[HTTPClient] = HTTPClient()

        container[IACClient] = IACClient(
            http_client=container[HTTPClient],
            iac_settings=container[IACSettings],
        )
        container[CatalogClient] = CatalogClient(
            http_client=container[HTTPClient],
            catalog_settings=container[CatalogServiceSettings],
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
        container[CallbackRequestEntityMapper] = CallbackRequestEntityMapper()

        container[OrderStatusRepository] = SQLOrderStatusRepository(
            order_status_mapper=container[OrderStatusEntityMapper],
            connection_manager=container[SQLConnectionManager],
        )
        container[OrderRepository] = SQLOrderRepository(
            order_entity_mapper=container[OrderEntityMapper],
            connection_manager=container[SQLConnectionManager],
        )
        container[CallbackRequestRepository] = SQLCallbackRequestRepository(
            callback_request_entity_mapper=container[CallbackRequestEntityMapper],
            connection_manager=container[SQLConnectionManager],
        )

        container[OrderService] = OrderService(
            event_bus=container[EventBus],
            order_status_repository=container[OrderStatusRepository],
            order_repository=container[OrderRepository],
        )
        container[OrderMailService] = container[ServiceMailService] = SMTPMailService(
            smtp_client=container[SMTPClient],
            iac_client=container[IACClient],
            catalog_client=container[CatalogClient],
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

        container[LifecycleComponentRepository].add(
            component=container[HTTPClient],
        )
