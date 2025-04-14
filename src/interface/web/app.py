import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Iterable

import psutil
from dw_shared_kernel import (
    Container,
    SharedKernelInfrastructureLayer,
    get_di_container,
)
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client.asgi import make_asgi_app

from application.layer import ApplicationLayer
from infrastructure.layer import InfrastructureLayer
from infrastructure.monitoring.metrics import system_usage
from infrastructure.settings.application import ApplicationSettings
from interface.web.middlewares.container import DIContainerProviderMiddleware
from interface.web.middlewares.exception import ExceptionHandlerMiddleware
from interface.web.middlewares.metrics import PrometheusMetricsMiddleware
from interface.web.routes.callback_request.endpoints import router as callback_request_router
from interface.web.routes.order.endpoints import router as order_router


class WebApplication:
    def __init__(
        self,
        container: Container,
        routes: Iterable[APIRouter],
    ):
        self._container = container
        self._app = self._create_application(
            routes=routes,
        )

        self._mount_metrics_endpoint()
        self._set_middlewares()

    def _create_application(
        self,
        routes: Iterable[APIRouter],
    ) -> FastAPI:
        settings = self._container[ApplicationSettings]

        app = FastAPI(
            title=settings.TITLE,
            debug=settings.DEBUG,
            version=settings.VERSION,
            description=f"**{settings.TITLE}** OpenAPI documentation.",
            docs_url="/docs" if settings.DEBUG else None,
            lifespan=self._app_lifespan,
        )

        for route in routes:
            app.include_router(route)

        return app

    def _mount_metrics_endpoint(self) -> None:
        self._app.mount("/metrics/", make_asgi_app())

    def _set_middlewares(self) -> None:
        self._app.add_middleware(
            DIContainerProviderMiddleware,  # type: ignore
            container=self._container,  # type: ignore
        )
        self._app.add_middleware(
            ExceptionHandlerMiddleware,  # type: ignore
            container=self._container,  # type: ignore
        )
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self._app.add_middleware(PrometheusMetricsMiddleware)

    @staticmethod
    @asynccontextmanager
    async def _app_lifespan(app: FastAPI) -> AsyncGenerator[None]:  # noqa: ARG004
        async def _collect_system_usage_metrics() -> None:
            process = psutil.Process()
            process.cpu_percent()

            while True:
                system_usage.labels("CPU").set(process.cpu_percent())
                system_usage.labels("Memory").set(process.memory_info().rss)
                await asyncio.sleep(15)

        asyncio.create_task(_collect_system_usage_metrics())
        yield

    def __call__(self):
        return self._app


web_app = WebApplication(
    container=get_di_container(
        layers=(
            SharedKernelInfrastructureLayer(),
            InfrastructureLayer(),
            ApplicationLayer(),
        ),
    ),
    routes=(
        order_router,
        callback_request_router,
    ),
)
