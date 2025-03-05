from dw_shared_kernel import (
    Container,
    Layer,
    CommandBus,
)

from domain.comment.repository import CommentRepository
from infrastructure.bus.middleware.transaction import TransactionMiddleware
from infrastructure.database.base.transaction import DatabaseTransactionManager
from infrastructure.database.relational.connection import SQLDatabaseConnectionManager
from infrastructure.database.relational.mapper import DatabaseToEntityMapper
from infrastructure.database.relational.repository.comment import SQLAlchemyCommentRepository
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

        container[CommentRepository] = SQLAlchemyCommentRepository(
            connection_manager=container[SQLDatabaseConnectionManager],
        )

        container[DatabaseToEntityMapper] = DatabaseToEntityMapper()

        container[CommandBus].add_middlewares(
            middlewares=[
                container[TransactionMiddleware],
            ],
        )

        self._run_entity_to_database_mapping(
            mapper=container[DatabaseToEntityMapper],
        )

    @staticmethod
    def _run_entity_to_database_mapping(mapper: DatabaseToEntityMapper):
        mapper.map()
