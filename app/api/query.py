from fastapi import APIRouter
from app.schemas.query import QueryRequest, QueryResponse

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    return QueryResponse(
        answer="LLM not wired yet",
        sources=[]
    )
