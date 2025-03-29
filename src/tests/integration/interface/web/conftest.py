from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from dw_shared_kernel import Container
from httpx import ASGITransport, AsyncClient

from interface.web.app import WebApplication
from interface.web.routes.callback_request.endpoints import router as callback_request_router
from interface.web.routes.order.endpoints import router as order_router


@pytest.fixture(scope="session")
def web_application(di_container: Container) -> WebApplication:
    return WebApplication(
        container=di_container,
        routes=(
            callback_request_router,
            order_router,
        ),
    )


@pytest_asyncio.fixture
async def api_client(web_application: WebApplication) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=web_application._app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
def order_created_event_schema() -> dict[str, dict | str]:
    return {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "event_type": {"type": "string"},
            "created_at": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"},
                    "products": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "product_id": {"type": "string"},
                                "quantity": {"type": "integer"},
                            },
                        },
                    },
                },
            },
        },
    }
