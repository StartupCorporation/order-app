from types import TracebackType

from dw_shared_kernel import LifecycleComponent
from httpx import URL, AsyncClient


class HTTPClient(LifecycleComponent):

    def __init__(self) -> None:
        self._client = AsyncClient(
            timeout=3,
        )

    async def get(
        self,
        url: URL,
        headers: dict | None = None,
    ) -> tuple[bytes, int]:
        response = await self._client.get(
            url=url,
            headers=headers,
        )
        return response.content, response.status_code

    async def __aenter__(self) -> None:
        await self._client.__aenter__()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._client.__aexit__(exc_type, exc_val, exc_tb)
