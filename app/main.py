from fastapi import FastAPI, Request
from app.core.logging import setup_logging
from app.core.request_id import request_id_middleware
from app.api import health, ingest, query

setup_logging()

app = FastAPI(title="Applied AI System")

app.middleware("http")(request_id_middleware)

app.include_router(health.router)
app.include_router(ingest.router)
app.include_router(query.router)
