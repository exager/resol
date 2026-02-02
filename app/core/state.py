from app.core.storage.chunk_store import InMemoryChunkStore
from app.core.storage.vector_index import InMemoryVectorIndex
from app.core.embeddings.embedder import Embedder, InMemoryEmbeddingCache
from app.core.retrieval.evaluator import RetrievalEvaluator
from app.core.config import Settings, RetrievalConfig
from app.core.metrics import MetricsStore, RetrievalMetrics

class AppState:
    def __init__(self):
        self.settings = Settings()
        self.chunk_store = InMemoryChunkStore()
        self.embedder = Embedder()
        self.embedding_cache = InMemoryEmbeddingCache()
        self.vector_index = None
        self.retrieval_config = RetrievalConfig()
        self.retrieval_evaluator = RetrievalEvaluator(
            min_top_score = self.retrieval_config.min_top_score,
            min_chunks_above_threshold = self.retrieval_config.min_chunks_above_threshold,
        )
        self.metrics_store = MetricsStore()
        self.retrieval_metrics = RetrievalMetrics()

state = AppState()
