import hashlib
from typing import List
from app.core.documents.models import Document, Chunk


def chunk_document(
    document: Document,
    *,
    chunk_size: int = 500,
    overlap: int = 50,
) -> List[Chunk]:
    """
    Deterministically split a document into overlapping chunks.
    """

    text = document.content
    chunks: List[Chunk] = []

    start = 0
    index = 0

    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end]

        raw_id = f"{document.document_id}:{index}:{chunk_text}"
        chunk_id = hashlib.sha256(raw_id.encode()).hexdigest()

        chunks.append(
            Chunk(
                chunk_id=chunk_id,
                document_id=document.document_id,
                content=chunk_text,
                metadata={
                    **document.metadata,
                    "chunk_index": index,
                    "chunk_start": start,
                    "chunk_end": end,
                },
            )
        )

        index += 1
        start += chunk_size - overlap

    return chunks
