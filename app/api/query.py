from fastapi import APIRouter, HTTPException, Request
from app.core.embeddings.embedder import Embedder
from app.core.state import state
from app.core.retrieval.decisions import RetrievalDecision
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
        state.retrieval_metrics.record(RetrievalDecision.REFUSE_EMPTY.value)
        logger.info(
            "retrieval_decision",
            extra={
                "request_id": request_id,
                "decision": decision,
                "metrics_snapshot": state.retrieval_metrics.snapshot(),
                **details,
            },
        )

        return {
            "decision": RetrievalDecision.REFUSE_EMPTY,
            "reason": "no_documents_indexed",
        }

    query_embedding = state.embedder.embed_texts([query_text])
    top_k = payload.get("top_k")
    if not top_k:
        top_k = 5

    results = state.vector_index.search(
        query_embedding=query_embedding,
        top_k=top_k,
    )

    decision, details = state.retrieval_evaluator.evaluate(results)
    state.retrieval_metrics.record(decision.value)

    logger.info(
        "retrieval_decision",
        extra={
            "request_id": request_id,
            "decision": decision.value,
            "metrics_snapshot": state.retrieval_metrics.snapshot(),
            **details,
        },
    )

    if decision != RetrievalDecision.ANSWERABLE:
        return {
            "query": query_text,
            "decision": decision.value,
            "details": details,
            "retrieved_chunks": [],
        }

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
        "decision": decision,
        "details": details,
        "retrieved_chunks": retrieved_chunks,
    }
