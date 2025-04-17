from dw_shared_kernel import Container
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class DIContainerProviderMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        *args,
        container: Container,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._container = container

    async def dispatch(self, request: Request, call_next):
        request.state.container = self._container
        return await call_next(request)
