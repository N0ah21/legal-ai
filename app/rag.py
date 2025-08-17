from __future__ import annotations

import os
import pickle
from pathlib import Path
from typing import List

import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except Exception:  # pragma: no cover - handled in testing
    SentenceTransformer = None  # type: ignore

MODEL_NAME = os.getenv("EMBEDDING_MODEL", "paraphrase-MiniLM-L3-v2")
DATA_DIR = Path(os.getenv("DATA_DIR", "data/legal"))
INDEX_PATH = Path(os.getenv("INDEX_PATH", DATA_DIR / "index.pkl"))


def get_model():
    """Return embedding model; use stub when STUB_EMBEDDINGS is set."""

    if os.getenv("STUB_EMBEDDINGS"):

        class StubModel:
            def encode(self, texts):
                if isinstance(texts, str):
                    texts = [texts]
                return np.array([[float(len(t))] for t in texts])

        return StubModel()
    if SentenceTransformer is None:
        raise ImportError("sentence-transformers is required for embeddings")
    return SentenceTransformer(MODEL_NAME)


class LocalRAG:
    """Minimal local RAG over legal text files."""

    def __init__(
        self, model=None, data_dir: Path = DATA_DIR, index_path: Path = INDEX_PATH
    ):
        self.data_dir = Path(data_dir)
        self.index_path = Path(index_path)
        self.model = model or get_model()
        self.index = self._load_or_build_index()

    def _load_or_build_index(self):
        if self.index_path.exists():
            with self.index_path.open("rb") as fh:
                return pickle.load(fh)
        texts: List[str] = []
        for path in sorted(self.data_dir.glob("*.txt")):
            content = path.read_text(encoding="utf-8")
            for chunk in content.split("\n\n"):
                chunk = chunk.strip()
                if chunk:
                    texts.append(chunk)
        if texts:
            embeddings = self.model.encode(texts)
            data = [{"text": t, "embedding": emb} for t, emb in zip(texts, embeddings)]
        else:
            data = []
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        with self.index_path.open("wb") as fh:
            pickle.dump(data, fh)
        return data

    def search(self, query: str, top_k: int = 3) -> List[str]:
        if not self.index:
            return []
        query_vec = self.model.encode([query])[0]
        scores = []
        for item in self.index:
            emb = item["embedding"]
            score = float(
                np.dot(emb, query_vec)
                / (np.linalg.norm(emb) * np.linalg.norm(query_vec))
            )
            scores.append((score, item["text"]))
        scores.sort(key=lambda x: x[0], reverse=True)
        return [t for _, t in scores[:top_k]]

    def summarize(self, query: str) -> dict:
        fragments = self.search(query, top_k=3)
        summary = " ".join(fragments)
        return {"fragments": fragments, "summary": summary}
