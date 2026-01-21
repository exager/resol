import time
import logging

logger = logging.getLogger(__name__)


def retry(
    fn,
    *,
    retries: int = 2,
    delay_seconds: float = 0.2,
):
    last_exc = None

    for attempt in range(1, retries + 2):
        try:
            return fn()
        except Exception as exc:
            last_exc = exc
            logger.warning(
                "retry_failed_attempt",
                extra={
                    "attempt": attempt,
                    "error": str(exc),
                },
            )
            time.sleep(delay_seconds)

    raise last_exc
