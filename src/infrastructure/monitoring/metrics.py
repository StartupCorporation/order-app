from prometheus_client import Counter, Gauge, Summary


requests = Counter(
    "requests",
    "Requests number received by the application.",
    labelnames=["path", "method", "status_code"],
)

request_duration = Summary(
    "request_duration",
    "Amount of time for request processing.",
    labelnames=["path", "method"],
)

system_usage = Gauge(
    "system_usage",
    "Usage of system resources.",
    labelnames=["resource_type"],
)
