from fastapi import APIRouter
from app.core.state import state

router = APIRouter()


@router.get("/metrics")
def metrics():
    return state.metrics_store.snapshot()
