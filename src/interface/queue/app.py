from typing import Iterable

from faststream import FastStream, ContextRepo, ExceptionMiddleware
from faststream.broker.router import BrokerRouter
from faststream.rabbit import RabbitBroker
from dw_shared_kernel import (
    DomainException,
    Container,
    SharedKernelInfrastructureLayer,
    get_di_container,
)

from application.layer import ApplicationLayer
from infrastructure.layer import InfrastructureLayer
from infrastructure.settings.application import ApplicationSettings
from infrastructure.settings.rabbitmq import RabbitMQSettings
from interface.queue.routes.order.endpoints import router as order_router


class QueueApplication:
    def __init__(
        self,
        container: Container,
        routes: Iterable[BrokerRouter],
    ):
        self._container = container
        self._app = self._create_application(
            routes=routes,
        )

    def _create_application(
        self,
        routes: Iterable[BrokerRouter],
    ) -> FastStream:
        settings = self._container[ApplicationSettings]

        broker = RabbitBroker(
            url=self._container[RabbitMQSettings].connection_url,
            middlewares=[
                ExceptionMiddleware(
                    handlers={
                        DomainException: self._domain_exception_handler,
                    },
                ),
            ],
        )
        app = FastStream(
            broker=broker,
            title=settings.TITLE,
            version=settings.VERSION,
            description=f"**{settings.TITLE}** AsyncAPI documentation.",
        )

        for route in routes:
            broker.include_router(route)

        @app.on_startup
        def set_container_context(context: ContextRepo):
            context.set_global("container", self._container)

        return app

    @staticmethod
    def _domain_exception_handler(exc: DomainException) -> None:
        print(f'The domain exception has occurred. Details: "{str(exc)}"')  # noqa: T201
        raise exc

    def __call__(self):
        return self._app


queue_app = QueueApplication(
    container=get_di_container(
        layers=(
            SharedKernelInfrastructureLayer(),
            InfrastructureLayer(),
            ApplicationLayer(),
        ),
    ),
    routes=(order_router,),
)
