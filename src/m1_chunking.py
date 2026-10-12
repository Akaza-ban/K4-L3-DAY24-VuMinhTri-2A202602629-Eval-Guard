"""Module 1: Chunking & Document Loading."""
from __future__ import annotations

import os
from pathlib import Path
from types import SimpleNamespace
from config import DATA_DIR, HIERARCHICAL_PARENT_SIZE, HIERARCHICAL_CHILD_SIZE


def load_documents(data_dir: str = DATA_DIR) -> list[dict]:
    """Load text and markdown documents from data_dir."""
    docs = []
    data_path = Path(data_dir)
    if not data_path.exists():
        return docs

    for file_path in data_path.glob("*"):
        if file_path.suffix.lower() in (".md", ".txt"):
            try:
                text = file_path.read_text(encoding="utf-8")
                docs.append({
                    "text": text,
                    "metadata": {"source": file_path.name, "path": str(file_path)},
                })
            except Exception:
                pass
    return docs


def chunk_hierarchical(text: str, metadata: dict = None) -> tuple[list[SimpleNamespace], list[SimpleNamespace]]:
    """Hierarchical chunking into parent and child chunks."""
    if metadata is None:
        metadata = {}

    parents = []
    children = []
    parent_size = HIERARCHICAL_PARENT_SIZE
    child_size = HIERARCHICAL_CHILD_SIZE

    step_parent = parent_size - 200 if parent_size > 200 else parent_size
    step_child = child_size - 50 if child_size > 50 else child_size

    parent_idx = 0
    start = 0
    while start < len(text):
        end = min(start + parent_size, len(text))
        parent_text = text[start:end]
        parent_id = f"{metadata.get('source', 'doc')}_p{parent_idx}"
        parent_obj = SimpleNamespace(
            id=parent_id,
            text=parent_text,
            metadata={**metadata, "parent_id": parent_id},
        )
        parents.append(parent_obj)

        child_start = start
        child_idx = 0
        while child_start < end:
            child_end = min(child_start + child_size, end)
            child_text = text[child_start:child_end]
            if child_text.strip():
                child_obj = SimpleNamespace(
                    id=f"{parent_id}_c{child_idx}",
                    text=child_text,
                    metadata={**metadata, "child_index": child_idx},
                    parent_id=parent_id,
                )
                children.append(child_obj)
            child_idx += 1
            child_start += step_child
            if child_start >= end:
                break

        parent_idx += 1
        start += step_parent
        if start >= len(text):
            break

    if not children and text:
        p_id = f"{metadata.get('source', 'doc')}_p0"
        parents.append(SimpleNamespace(id=p_id, text=text, metadata=metadata))
        children.append(SimpleNamespace(id=f"{p_id}_c0", text=text, metadata=metadata, parent_id=p_id))

    return parents, children
