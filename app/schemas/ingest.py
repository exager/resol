from pydantic import BaseModel
from typing import Optional, Literal


class IngestRequest(BaseModel):
    content: Optional[str] = None
    metadata: dict | None = None

    source: Literal["local", "internet"] = "local"
    search_query: Optional[str] = None


class IngestResponse(BaseModel):
    document_id: str
    status: str
    discovered_docs: int = 0
