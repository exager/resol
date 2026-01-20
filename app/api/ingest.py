import logging
from fastapi import APIRouter, HTTPException, Request

from app.schemas.ingest import IngestRequest, IngestResponse
from app.core.search.dummy_internet import DummyInternetSearchProvider

router = APIRouter()
logger = logging.getLogger(__name__)

search_provider = DummyInternetSearchProvider()


@router.post("/ingest", response_model=IngestResponse)
def ingest(req: IngestRequest, request: Request):
    request_id = request.state.request_id

    discovered_docs = 0

    if req.source == "internet":
        if not req.search_query:
            raise HTTPException(
                status_code=400,
                detail="search_query is required when source=internet"
            )

        results = search_provider.search(req.search_query)
        discovered_docs = len(results)

        logger.info(
            "internet_documents_discovered",
            extra={
                "request_id": request_id,
                "query": req.search_query,
                "documents_found": discovered_docs,
            }
        )

    else:
        logger.info(
            "local_document_ingested",
            extra={"request_id": request_id}
        )

    return IngestResponse(
        document_id="dummy-doc-id",
        status="accepted",
        discovered_docs=discovered_docs,
    )
