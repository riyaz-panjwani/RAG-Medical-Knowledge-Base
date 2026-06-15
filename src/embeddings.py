import logging
import time
from typing import List, Dict
from openai import OpenAI
from config.settings import settings

logger = logging.getLogger(__name__)

EMBED_MODEL = "text-embedding-3-small"
EMBED_DIM = 1536
BATCH_SIZE = 100          # OpenAI allows up to 2048 inputs per call
RETRY_LIMIT = 3
RETRY_DELAY = 2           # seconds between retries


class EmbeddingsManager:
    """
    Embed text chunks via the OpenAI embeddings API.

    Handles batching, retries, and attaches the vector back onto each
    chunk dict so it can flow directly into the vector store.
    """

    def __init__(self, model: str = EMBED_MODEL):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in your .env file.")
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = model
        self.dim = EMBED_DIM
        logger.info(f"EmbeddingsManager initialised with model={model}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def embed_chunks(self, chunks: List[Dict]) -> List[Dict]:
        """
        Add an 'embedding' key to every chunk dict.

        Args:
            chunks: list of chunk dicts (must have a 'content' key)

        Returns:
            Same list with 'embedding': List[float] added to each dict.
            Chunks that fail embedding are dropped and logged.
        """
        texts = [c["content"] for c in chunks]
        vectors = self._embed_texts(texts)

        embedded: List[Dict] = []
        for chunk, vector in zip(chunks, vectors):
            if vector is not None:
                chunk["embedding"] = vector
                embedded.append(chunk)
            else:
                logger.warning(f"Dropping chunk {chunk.get('id')} — embedding failed.")

        logger.info(f"Embedded {len(embedded)}/{len(chunks)} chunks successfully.")
        return embedded

    def embed_query(self, query: str) -> List[float]:
        """Return the embedding vector for a single query string."""
        vectors = self._embed_texts([query])
        if vectors and vectors[0] is not None:
            return vectors[0]
        raise RuntimeError("Failed to embed query.")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _embed_texts(self, texts: List[str]) -> List[List[float] | None]:
        """
        Embed a list of strings in batches, with retry logic.
        Returns None in position of any text that ultimately failed.
        """
        results: List[List[float] | None] = [None] * len(texts)

        # Process in batches
        for batch_start in range(0, len(texts), BATCH_SIZE):
            batch = texts[batch_start: batch_start + BATCH_SIZE]
            batch_vectors = self._embed_batch_with_retry(batch)
            for i, vec in enumerate(batch_vectors):
                results[batch_start + i] = vec

        return results

    def _embed_batch_with_retry(self, texts: List[str]) -> List[List[float] | None]:
        """Call the OpenAI API for one batch, retrying on transient errors."""
        for attempt in range(1, RETRY_LIMIT + 1):
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=texts,
                )
                # API returns results in the same order as input
                return [item.embedding for item in response.data]
            except Exception as e:
                logger.warning(f"Embedding attempt {attempt}/{RETRY_LIMIT} failed: {e}")
                if attempt < RETRY_LIMIT:
                    time.sleep(RETRY_DELAY * attempt)

        # All retries exhausted — return None for every item in batch
        return [None] * len(texts)

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def print_summary(self, chunks: List[Dict]) -> None:
        """Print embedding stats after embed_chunks() has been called."""
        embedded = [c for c in chunks if "embedding" in c]
        print("\n" + "=" * 65)
        print("🔢 EMBEDDING SUMMARY")
        print("=" * 65)
        print(f"  Model           : {self.model}")
        print(f"  Dimensions      : {self.dim}")
        print(f"  Chunks embedded : {len(embedded)}/{len(chunks)}")
        if embedded:
            sample = embedded[0]["embedding"]
            print(f"  Sample vector   : [{sample[0]:.4f}, {sample[1]:.4f}, ... ]")
        print("=" * 65 + "\n")
