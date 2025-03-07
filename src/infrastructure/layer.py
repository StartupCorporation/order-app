from dw_shared_kernel import Container, Layer, CommandBus

from domain.order.repository.order import OrderRepository
from domain.order.repository.order_status import OrderStatusRepository
from domain.order.service.order import OrderService
from infrastructure.bus.middleware.transaction import TransactionMiddleware
from infrastructure.database.base.transaction import DatabaseTransactionManager
from infrastructure.database.relational.connection import SQLDatabaseConnectionManager
from infrastructure.database.relational.transaction import SQLDatabaseTransactionManager
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

        container[SQLDatabaseConnectionManager] = SQLDatabaseConnectionManager(
            settings=container[DatabaseSettings],
        )
        container[DatabaseTransactionManager] = SQLDatabaseTransactionManager(
            connection_manager=container[SQLDatabaseConnectionManager],
        )
        container[TransactionMiddleware] = TransactionMiddleware(
            transaction_manager=container[DatabaseTransactionManager],
        )

        container[CommandBus].add_middlewares(
            middlewares=[
                container[TransactionMiddleware],
            ],
        )

        container[OrderService] = OrderService(
            order_status_repository=container[OrderStatusRepository],
            order_repository=container[OrderRepository],
        )
