from time import perf_counter
from typing import Callable

from fastapi import Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

REQUEST_COUNT = Counter(
    "hr_workforce_http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status_code"],
)
REQUEST_LATENCY = Histogram(
    "hr_workforce_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path"],
)


async def metrics_middleware(request: Request, call_next: Callable) -> Response:
    start = perf_counter()
    response = await call_next(request)
    elapsed = perf_counter() - start
    route = request.scope.get("route")
    path = getattr(route, "path", request.url.path)
    REQUEST_COUNT.labels(request.method, path, str(response.status_code)).inc()
    REQUEST_LATENCY.labels(request.method, path).observe(elapsed)
    return response


def metrics_response() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
