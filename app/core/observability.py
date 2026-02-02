import time
import logging
from fastapi import Request
from app.core.state import state

logger = logging.getLogger(__name__)


async def observability_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    request_id = request.state.request_id

    status_code = 500
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        latency_ms = (time.perf_counter() - start_time) * 1000
        is_error = status_code >= 400

        state.metrics_store.record(latency_ms, is_error)

        logger.info(
            "request_completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": status_code,
                "latency_ms": round(latency_ms, 2),
            },
        )
