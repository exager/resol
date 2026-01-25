from abc import ABC, abstractmethod
from typing import Tuple, Dict


class DocumentLoader(ABC):
    @abstractmethod
    def load(self, file_bytes: bytes) -> Tuple[str, Dict]:
        """
        Returns:
        - extracted_text
        - metadata (extraction stats, warnings)
        """
        pass
