from typing import Tuple, Dict
from docx import Document as DocxDocument
from io import BytesIO

from app.core.loaders.base import DocumentLoader


class DocxLoader(DocumentLoader):
    def load(self, file_bytes: bytes) -> Tuple[str, Dict]:
        doc = DocxDocument(BytesIO(file_bytes))

        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        extracted_text = "\n".join(paragraphs)

        metadata = {
            "paragraph_count": len(paragraphs),
            "extracted_length": len(extracted_text),
            "loader": "docx",
        }

        return extracted_text, metadata
