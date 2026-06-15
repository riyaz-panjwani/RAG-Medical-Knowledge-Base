"""
Local embeddings using sentence-transformers.
No API key required — model downloads once and runs on CPU/GPU.
"""

import logging
from typing import List, Dict
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

# Small but high-quality model: 384-dim, ~90 MB download
DEFAULT_MODEL = "all-MiniLM-L6-v2"


class EmbeddingsManager:
    """
    Embed text chunks locally using sentence-transformers.
    First call downloads the model (~90 MB); subsequent calls use cache.
    """

    def __init__(self, model_name: str = DEFAULT_MODEL):
        logger.info(f"Loading embedding model '{model_name}' (downloads once if not cached)…")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.dim = self.model.get_embedding_dimension()
        logger.info(f"Model ready — dimension: {self.dim}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def embed_chunks(self, chunks: List[Dict]) -> List[Dict]:
        """
        Add an 'embedding' key (List[float]) to every chunk dict.

        Args:
            chunks: list of chunk dicts with a 'content' key

        Returns:
            Same list with 'embedding' added to each dict.
        """
        texts = [c["content"] for c in chunks]
        vectors = self.model.encode(texts, show_progress_bar=True)

        for chunk, vector in zip(chunks, vectors):
            chunk["embedding"] = vector.tolist()

        logger.info(f"Embedded {len(chunks)} chunks (dim={self.dim})")
        return chunks

    def embed_query(self, query: str) -> List[float]:
        """Return the embedding vector for a single query string."""
        return self.model.encode(query).tolist()

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def print_summary(self, chunks: List[Dict]) -> None:
        embedded = [c for c in chunks if "embedding" in c]
        print("\n" + "=" * 65)
        print("🔢  EMBEDDING SUMMARY")
        print("=" * 65)
        print(f"  Model        : {self.model_name}  (local, free)")
        print(f"  Dimensions   : {self.dim}")
        print(f"  Chunks done  : {len(embedded)}/{len(chunks)}")
        if embedded:
            s = embedded[0]["embedding"]
            print(f"  Sample vec   : [{s[0]:.4f}, {s[1]:.4f}, {s[2]:.4f} …]")
        print("=" * 65 + "\n")
