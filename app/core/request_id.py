import uuid
from fastapi import Request
from app.core.logging import request_id_ctx


async def request_id_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.request_id = request_id
    request_id_ctx.set(request_id)

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response
