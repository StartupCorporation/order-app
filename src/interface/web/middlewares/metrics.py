from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from infrastructure.monitoring.metrics import request_duration, requests


class PrometheusMetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        labels = {
            "method": request.method,
            "path": request.url.path,
        }
        with request_duration.labels(**labels).time():
            response = await call_next(request)
            requests.labels(**labels, status_code=response.status_code).inc()
            return response
