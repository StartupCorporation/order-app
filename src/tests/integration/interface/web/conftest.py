from collections.abc import AsyncIterator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from interface.web.app import web_app


@pytest_asyncio.fixture
async def api_client() -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=web_app._app),
        base_url="http://test",
    ) as ac:
        yield ac
