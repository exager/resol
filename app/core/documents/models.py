from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Document:
    document_id: str
    content: str
    metadata: Dict


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    document_id: str
    content: str
    metadata: Dict
