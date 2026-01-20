from fastapi import FastAPI, Request
from app.core.logging import setup_logging
from app.core.request_id import request_id_middleware
from app.core.observability import observability_middleware
from app.api import health, ingest, query, metrics

setup_logging()

app = FastAPI(title="Applied AI System")

app.middleware("http")(observability_middleware)
app.middleware("http")(request_id_middleware)

app.include_router(health.router)
app.include_router(ingest.router)
app.include_router(query.router)
app.include_router(metrics.router)