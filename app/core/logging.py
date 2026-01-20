import logging
import json
from datetime import datetime
from app.core.config import settings
from contextvars import ContextVar

request_id_ctx = ContextVar("request_id", default=None)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        request_id = getattr(record, "request_id", None) or request_id_ctx.get()
        if request_id:
            payload["request_id"] = record.request_id

        return json.dumps(payload)


def setup_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    root = logging.getLogger()
    root.setLevel(settings.log_level)
    root.handlers = [handler]
