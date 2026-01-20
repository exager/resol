from app.core.search.base import SearchProvider, SearchResult


class DummyInternetSearchProvider(SearchProvider):

    def search(self, query: str, limit: int = 5):
        # This simulates "internet discovery"
        # No external calls yet – intentional
        return [
            SearchResult(
                title="Dummy Document",
                url="https://example.com/dummy",
                content=f"Simulated content relevant to: {query}"
            )
        ]
