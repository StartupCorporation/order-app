from dw_shared_kernel import Container, DomainException
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from infrastructure.settings.application import ApplicationSettings


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        *args,
        container: Container,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._container = container

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            return self._handle_exception(exception=e)

    def _handle_exception(self, exception: Exception) -> JSONResponse:
        match exception:
            case DomainException():
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": str(exception)},
                )
            case Exception():
                if self._container[ApplicationSettings].DEBUG:
                    print(exception)  # noqa: T201
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={"detail": "Something went wrong..."},
                )
