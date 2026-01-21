from fastapi import Request, HTTPException


MAX_CONTENT_LENGTH = 50_000  # character-limit set


async def enforce_size_limit(request: Request):
    body = await request.body()
    if len(body) > MAX_CONTENT_LENGTH:
        raise HTTPException(
            status_code=413,
            detail="payload_too_large",
        )
