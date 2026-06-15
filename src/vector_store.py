"""
Lightweight vector store using numpy cosine similarity.
No third-party vector DB needed — persists to disk as .npy + .json files.
Works on any Python version and any platform.
"""

import json
import logging
import os
from typing import List, Dict

import numpy as np

logger = logging.getLogger(__name__)

PERSIST_DIR = "data/vector_store"
VECTORS_FILE = "vectors.npy"
META_FILE    = "metadata.json"


class VectorStore:
    """
    Cosine-similarity vector store backed by numpy arrays on disk.

    On first run it builds from scratch; subsequent runs reload from disk
    so ingestion only happens once per deployment.
    """

    def __init__(self, persist_dir: str = PERSIST_DIR):
        self.persist_dir  = persist_dir
        self._vectors_path = os.path.join(persist_dir, VECTORS_FILE)
        self._meta_path    = os.path.join(persist_dir, META_FILE)
        os.makedirs(persist_dir, exist_ok=True)

        self._vectors: np.ndarray | None = None   # shape (N, dim)
        self._metadata: List[Dict]        = []

        self._load()
        logger.info(f"VectorStore ready — {self.count()} vectors in '{persist_dir}'")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def upsert(self, chunks: List[Dict]) -> int:
        """Add chunks (with 'embedding' key) to the store and persist."""
        new_vecs, new_meta = [], []

        for chunk in chunks:
            if "embedding" not in chunk:
                logger.warning(f"Chunk '{chunk.get('id')}' has no embedding — skipped.")
                continue
            new_vecs.append(chunk["embedding"])
            new_meta.append({
                "id":          chunk.get("id", ""),
                "content":     chunk.get("content", ""),
                "source":      chunk.get("source", ""),
                "chunk_index": chunk.get("chunk_index", 0),
                "word_count":  chunk.get("word_count", 0),
            })

        if not new_vecs:
            return 0

        arr = np.array(new_vecs, dtype=np.float32)

        if self._vectors is None:
            self._vectors = arr
        else:
            self._vectors = np.vstack([self._vectors, arr])

        self._metadata.extend(new_meta)
        self._save()

        logger.info(f"Upserted {len(new_vecs)} vectors (total: {self.count()})")
        return len(new_vecs)

    def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict]:
        """Return top_k most similar chunks via cosine similarity."""
        if self._vectors is None or len(self._metadata) == 0:
            return []

        q = np.array(query_vector, dtype=np.float32)
        q_norm = q / (np.linalg.norm(q) + 1e-10)

        # Normalise stored vectors row-wise
        norms = np.linalg.norm(self._vectors, axis=1, keepdims=True) + 1e-10
        normed = self._vectors / norms

        scores = normed @ q_norm          # cosine similarity for each stored vec
        top_k  = min(top_k, len(scores))
        top_idx = np.argsort(scores)[::-1][:top_k]

        results = []
        for idx in top_idx:
            meta = self._metadata[idx]
            results.append({
                "id":          meta["id"],
                "content":     meta["content"],
                "source":      meta["source"],
                "chunk_index": meta["chunk_index"],
                "score":       round(float(scores[idx]), 4),
            })

        return results

    def delete_all(self) -> bool:
        """Wipe all stored vectors and metadata."""
        self._vectors  = None
        self._metadata = []
        for path in [self._vectors_path, self._meta_path]:
            if os.path.exists(path):
                os.remove(path)
        logger.info("VectorStore cleared.")
        return True

    def count(self) -> int:
        return len(self._metadata)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _save(self):
        if self._vectors is not None:
            np.save(self._vectors_path, self._vectors)
        with open(self._meta_path, "w") as f:
            json.dump(self._metadata, f)

    def _load(self):
        if os.path.exists(self._vectors_path) and os.path.exists(self._meta_path):
            self._vectors  = np.load(self._vectors_path)
            with open(self._meta_path) as f:
                self._metadata = json.load(f)
            logger.info(f"Loaded {len(self._metadata)} vectors from disk.")

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def print_summary(self, n_upserted: int) -> None:
        print("\n" + "=" * 65)
        print("🗄️   VECTOR STORE SUMMARY")
        print("=" * 65)
        print(f"  Backend          : numpy cosine similarity  (local, free)")
        print(f"  Persist path     : {self.persist_dir}")
        print(f"  Vectors upserted : {n_upserted}")
        print(f"  Total in store   : {self.count()}")
        print("=" * 65 + "\n")


def get_vector_store(db_type: str = "numpy") -> "VectorStore":
    return VectorStore()
