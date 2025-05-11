from contextlib import asynccontextmanager
from typing import AsyncGenerator, Iterable

from dw_shared_kernel import (
    Container,
    DomainException,
    LifecycleComponentManager,
    SharedKernelInfrastructureLayer,
    get_initialized_di_container,
)
from faststream import ExceptionMiddleware, FastStream
from faststream.broker.router import BrokerRouter
from faststream.rabbit import RabbitBroker

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
            lifespan=self._app_lifespan,
        )

        for route in routes:
            broker.include_router(route)

        return app

    @asynccontextmanager
    async def _app_lifespan(self, *args, **kwargs) -> AsyncGenerator[None]:  # noqa: ARG002
        self._app.context.set_global("container", self._container)

        async with self._container[LifecycleComponentManager].start():
            yield

    @staticmethod
    def _domain_exception_handler(exc: DomainException) -> None:
        print(f'The domain exception has occurred. Details: "{str(exc)}"')  # noqa: T201
        raise exc

    def __call__(self):
        return self._app


queue_app = QueueApplication(
    container=get_initialized_di_container(
        layers=(
            SharedKernelInfrastructureLayer(),
            InfrastructureLayer(),
            ApplicationLayer(),
        ),
    ),
    routes=(order_router,),
)
