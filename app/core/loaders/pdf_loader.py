from typing import Tuple, Dict
from pypdf import PdfReader
from io import BytesIO

from app.core.loaders.base import DocumentLoader


class PDFLoader(DocumentLoader):
    def load(self, file_bytes: bytes) -> Tuple[str, Dict]:
        reader = PdfReader(BytesIO(file_bytes))

        extracted_text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_text += page_text + "\n"

        metadata = {
            "page_count": len(reader.pages),
            "extracted_length": len(extracted_text),
            "loader": "pdf",
        }

        return extracted_text.strip(), metadata
