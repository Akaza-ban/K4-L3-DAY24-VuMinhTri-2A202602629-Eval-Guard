"""Module 2: Hybrid Search (BM25 + Dense)."""
from __future__ import annotations

from types import SimpleNamespace
from rank_bm25 import BM25Okapi


class HybridSearch:
    def __init__(self):
        self.chunks: list[dict] = []
        self.bm25: BM25Okapi | None = None
        self.tokenized_corpus: list[list[str]] = []

    def index(self, chunks: list[dict]) -> None:
        self.chunks = list(chunks)
        if not self.chunks:
            return
        self.tokenized_corpus = [
            chunk["text"].lower().split() for chunk in self.chunks
        ]
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def search(self, question: str, top_k: int = 10) -> list[SimpleNamespace]:
        if not self.chunks or self.bm25 is None:
            return []
        tokenized_query = question.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

        results = []
        for idx in ranked_indices:
            results.append(SimpleNamespace(
                text=self.chunks[idx]["text"],
                score=float(scores[idx]),
                metadata=self.chunks[idx].get("metadata", {}),
            ))
        return results
