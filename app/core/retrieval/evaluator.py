from typing import List, Tuple
from app.core.retrieval.decisions import RetrievalDecision


class RetrievalEvaluator:
    def __init__(
        self,
        *,
        min_top_score: float = 0.6,
        min_chunks_above_threshold: int = 1,
    ):
        self.min_top_score = min_top_score
        self.min_chunks_above_threshold = min_chunks_above_threshold

    def evaluate(
        self,
        results: List[Tuple[str, float]],
    ) -> tuple[RetrievalDecision, dict]:
        """
        results: List of (chunk_id, similarity_score)
        """

        if not results:
            return (
                RetrievalDecision.REFUSE_EMPTY,
                {"reason": "no_chunks_retrieved"},
            )

        scores = [score for _, score in results]
        top_score = max(scores)

        strong_chunks = [s for s in scores if s >= self.min_top_score]

        if top_score < self.min_top_score:
            return (
                RetrievalDecision.REFUSE_WEAK,
                {
                    "reason": "top_score_below_threshold",
                    "top_score": top_score,
                    "threshold": self.min_top_score,
                },
            )
        
        if len(strong_chunks) < self.min_chunks_above_threshold:
            return (
                RetrievalDecision.REFUSE_WEAK,
                {
                    "reason": "insufficient_strong_chunks",
                    "strong_chunks": len(strong_chunks),
                    "required": self.min_chunks_above_threshold,
                },
            )

        return (
            RetrievalDecision.ANSWERABLE,
            {
                "top_score": top_score,
                "strong_chunks": len(strong_chunks),
            },
        )
