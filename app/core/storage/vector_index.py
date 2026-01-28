import faiss
import numpy as np
from typing import List, Tuple


class InMemoryVectorIndex:
    def __init__(self, dim: int = 768):
        self.index = faiss.IndexFlatIP(dim)
        self.chunk_ids: List[str] = []

    def add(self, embeddings: np.ndarray, chunk_ids: List[str]):
        self.index.add(embeddings)
        self.chunk_ids.extend(chunk_ids)

    def search(self, query_embedding: np.ndarray, top_k: int) -> List[Tuple[str, float]]:
        scores, indices = self.index.search(query_embedding, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            results.append((self.chunk_ids[idx], float(score)))

        return results
