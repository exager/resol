from abc import ABC, abstractmethod
from typing import List, Dict


class SearchResult:
    def __init__(self, title: str, url: str, content: str):
        self.title = title
        self.url = url
        self.content = content


class SearchProvider(ABC):

    @abstractmethod
    def search(self, query: str, limit: int = 5) -> List[SearchResult]:
        pass
