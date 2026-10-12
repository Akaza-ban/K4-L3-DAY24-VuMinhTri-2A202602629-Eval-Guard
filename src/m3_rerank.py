"""Module 3: Reranker."""
from __future__ import annotations

from types import SimpleNamespace


class CrossEncoderReranker:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name

    def rerank(self, question: str, docs: list[dict], top_k: int = 3) -> list[SimpleNamespace]:
        """Rerank search results; returns list of objects with .text attribute."""
        if not docs:
            return []
        selected = docs[:top_k]
        return [
            SimpleNamespace(
                text=d.get("text", "") if isinstance(d, dict) else getattr(d, "text", ""),
                score=float(d.get("score", 0.0)) if isinstance(d, dict) else float(getattr(d, "score", 0.0)),
                metadata=d.get("metadata", {}) if isinstance(d, dict) else getattr(d, "metadata", {}),
            )
            for d in selected
        ]
