"""Module 5: Metadata & Context Enrichment."""
from __future__ import annotations

from types import SimpleNamespace


def enrich_chunks(chunks: list[dict]) -> list[SimpleNamespace]:
    """Enrich chunks or return empty list as official fallback to raw chunks.

    See doc/PIPELINE_INTERFACE.md:
    '[] là fallback dùng chunks gốc'
    """
    return []
