import asyncio
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.logging import request_id_ctx


class TimeoutMiddleware:
    def __init__(self, timeout_seconds: float):
        self.timeout = timeout_seconds

    async def __call__(self, request: Request, call_next):
        try:
            return await asyncio.wait_for(
                call_next(request),
                timeout=self.timeout,
            )
        except asyncio.TimeoutError:
            return JSONResponse(
                status_code=504,
                content={
                    "error": "request_timeout",
                    "request_id": request_id_ctx.get(),
                },
            )
