from app.core.storage.chunk_store import InMemoryChunkStore
from app.core.storage.vector_index import InMemoryVectorIndex
from app.core.embeddings.embedder import Embedder, InMemoryEmbeddingCache
from app.core.retrieval.evaluator import RetrievalEvaluator

class AppState:
    def __init__(self):
        self.chunk_store = InMemoryChunkStore()
        self.embedder = Embedder()
        self.embedding_cache = InMemoryEmbeddingCache()
        self.retrieval_evaluator = RetrievalEvaluator()
        self.vector_index = None

state = AppState()
