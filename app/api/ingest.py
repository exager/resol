import logging
from fastapi import APIRouter, HTTPException, Request
from app.schemas.ingest import IngestRequest, IngestResponse
from app.core.retry import retry
from app.core.limits import enforce_size_limit
from app.core.search.dummy_internet import DummyInternetSearchProvider
import uuid
import hashlib
from typing import List
from app.core.documents.models import Document
from app.core.documents.chunker import chunk_document

router = APIRouter()
logger = logging.getLogger(__name__)

search_provider = DummyInternetSearchProvider()


@router.post("/ingest", response_model=IngestResponse)
async def ingest(req: IngestRequest, request: Request):
    await enforce_size_limit(request)
    request_id = request.state.request_id

    documents: List[Document] = []

    if req.source == "internet":
        if not req.search_query:
            raise HTTPException(
                status_code=400,
                detail="search_query is required when source=internet"
            )

        results = retry(
            lambda:search_provider.search(req.search_query),
            retries = 3,
        )
        # discovered_docs = len(results)
        for result in results:
            # Stable ID derived from source URL
            source_doc_id = hashlib.sha256(result.url.encode()).hexdigest()

            documents.append(
                Document(
                    document_id=source_doc_id,
                    content=result.content,
                    metadata={
                        "source": "internet",
                        "url": result.url,
                        "title": result.title,
                    },
                )
            )
        logger.info(
            "internet_documents_discovered",
            extra={
                "request_id": request_id,
                "query": req.search_query,
                "documents_found": discovered_docs,
            }
        )

    elif req.source == "local":
        if not req.content:
            raise HTTPException(
                status_code=400,
                detail="content is required when source=local"
            )

        local_doc_id = str(uuid.uuid4())
        documents.append(
            Document(
                document_id=local_doc_id,
                content=req.content,
                metadata={
                    "source": "local",
                    **(req.metadata or {}),
                },
            )
        )
        logger.info(
            "local_document_received",
            extra={
                "request_id": request_id,
                "document_id": local_doc_id,
            },
        )
    else:
        raise HTTPException(status_code=400, detail="invalid source")

    # Chunking docs
    chunks = []

    for document in documents:
        parts = chunk_document(document)
        chunks.extend(parts)

    # Vectorization and Persistence 

    logger.info(
        "document_chunked",
        extra={
            "request_id": request_id,
            "document_id": document.document_id,
            "chunk_count": len(chunks),
        },
    )

    return IngestResponse(
        document_id="batch",
        status="accepted",
        discovered_docs=len(documents),
    )

