from fastapi import APIRouter, HTTPException, Request
from app.core.embeddings.embedder import Embedder
from app.core.state import state
import numpy as np
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/query")
async def query(payload: dict, request: Request):
    request_id = request.state.request_id
    query_text = payload.get("query")

    if not query_text:
        raise HTTPException(status_code=400, detail="query_required")

    if state.vector_index is None:
        raise HTTPException(status_code=400, detail="no_documents_indexed")

    query_embedding = state.embedder.embed_texts([query_text])

    results = state.vector_index.search(
        query_embedding=query_embedding,
        top_k=5,
    )

    logger.info(
        "retrieval_performed",
        extra={
            "request_id": request_id,
            "top_k": 5,
            "results_found": len(results),
            "scores": [score for _, score in results],
        },
    )

    retrieved_chunks = [
        {
            "chunk_id": cid,
            "score": score,
            "text": state.chunk_store.get(cid).content,
        }
        for cid, score in results
        if state.chunk_store.get(cid) is not None
    ]

    return {
        "query": query_text,
        "retrieved_chunks": retrieved_chunks,
    }
