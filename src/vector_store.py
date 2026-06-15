"""
Vector store abstraction supporting Pinecone and Weaviate.

Usage:
    store = get_vector_store("pinecone")   # or "weaviate"
    store.upsert(embedded_chunks)
    results = store.search(query_vector, top_k=5)
"""

import logging
from abc import ABC, abstractmethod
from typing import List, Dict
from config.settings import settings

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Shared interface
# ---------------------------------------------------------------------------

class VectorStore(ABC):
    """Minimal interface every vector store must implement."""

    @abstractmethod
    def upsert(self, chunks: List[Dict]) -> int:
        """
        Insert or update chunks in the store.

        Args:
            chunks: list of dicts with at least 'id', 'embedding', 'content',
                    'source', and 'chunk_index' keys.

        Returns:
            Number of vectors successfully upserted.
        """

    @abstractmethod
    def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict]:
        """
        Return the top_k most similar chunks.

        Returns:
            List of dicts with 'id', 'content', 'source', 'score'.
        """

    @abstractmethod
    def delete_all(self) -> bool:
        """Wipe the entire collection / index."""

    @abstractmethod
    def count(self) -> int:
        """Return the number of vectors currently stored."""


# ---------------------------------------------------------------------------
# Pinecone implementation
# ---------------------------------------------------------------------------

class PineconeStore(VectorStore):
    """
    Pinecone serverless vector store.

    Requires environment variables:
        PINECONE_API_KEY
        PINECONE_INDEX_NAME   (default: medical-rag)
    """

    DIMENSION = 1536          # text-embedding-3-small
    METRIC = "cosine"
    NAMESPACE = "medical"

    def __init__(self):
        try:
            from pinecone import Pinecone, ServerlessSpec
        except ImportError:
            raise ImportError("Run: pip install pinecone-client")

        if not settings.PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY not set in .env")

        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        index_name = settings.PINECONE_INDEX_NAME

        # Create index if it doesn't exist
        existing = [idx.name for idx in pc.list_indexes()]
        if index_name not in existing:
            logger.info(f"Creating Pinecone index '{index_name}'…")
            pc.create_index(
                name=index_name,
                dimension=self.DIMENSION,
                metric=self.METRIC,
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )

        self.index = pc.Index(index_name)
        self.index_name = index_name
        logger.info(f"Connected to Pinecone index '{index_name}'")

    # ------------------------------------------------------------------

    def upsert(self, chunks: List[Dict]) -> int:
        """Batch-upsert chunks into Pinecone."""
        vectors = []
        for chunk in chunks:
            if "embedding" not in chunk:
                logger.warning(f"Chunk {chunk.get('id')} has no embedding — skipped.")
                continue
            vectors.append({
                "id": chunk["id"],
                "values": chunk["embedding"],
                "metadata": {
                    "content": chunk["content"],
                    "source": chunk["source"],
                    "chunk_index": chunk.get("chunk_index", 0),
                    "word_count": chunk.get("word_count", 0),
                },
            })

        if not vectors:
            return 0

        # Pinecone recommends batches of ≤100
        BATCH = 100
        upserted = 0
        for i in range(0, len(vectors), BATCH):
            batch = vectors[i: i + BATCH]
            self.index.upsert(vectors=batch, namespace=self.NAMESPACE)
            upserted += len(batch)
            logger.info(f"Upserted batch {i // BATCH + 1}: {len(batch)} vectors")

        logger.info(f"Total upserted to Pinecone: {upserted}")
        return upserted

    def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict]:
        response = self.index.query(
            vector=query_vector,
            top_k=top_k,
            namespace=self.NAMESPACE,
            include_metadata=True,
        )
        results = []
        for match in response.get("matches", []):
            meta = match.get("metadata", {})
            results.append({
                "id": match["id"],
                "score": round(match["score"], 4),
                "content": meta.get("content", ""),
                "source": meta.get("source", ""),
                "chunk_index": meta.get("chunk_index", 0),
            })
        return results

    def delete_all(self) -> bool:
        try:
            self.index.delete(delete_all=True, namespace=self.NAMESPACE)
            logger.info("Pinecone index cleared.")
            return True
        except Exception as e:
            logger.error(f"Failed to clear Pinecone index: {e}")
            return False

    def count(self) -> int:
        try:
            stats = self.index.describe_index_stats()
            ns = stats.get("namespaces", {}).get(self.NAMESPACE, {})
            return ns.get("vector_count", 0)
        except Exception as e:
            logger.error(f"Could not get count: {e}")
            return -1


# ---------------------------------------------------------------------------
# Weaviate implementation
# ---------------------------------------------------------------------------

class WeaviateStore(VectorStore):
    """
    Weaviate vector store (local Docker or Weaviate Cloud).

    Requires environment variables:
        WEAVIATE_URL          (e.g. http://localhost:8080)
        WEAVIATE_API_KEY      (leave blank for local Docker)
    """

    CLASS_NAME = "MedicalDocument"

    def __init__(self):
        try:
            import weaviate
        except ImportError:
            raise ImportError("Run: pip install weaviate-client")

        url = settings.WEAVIATE_URL or "http://localhost:8080"
        auth = None
        if settings.WEAVIATE_API_KEY:
            auth = weaviate.auth.AuthApiKey(settings.WEAVIATE_API_KEY)

        self.client = weaviate.Client(url=url, auth_client_secret=auth)
        self._ensure_schema()
        logger.info(f"Connected to Weaviate at {url}")

    def _ensure_schema(self):
        """Create the schema class if it doesn't exist."""
        existing = [c["class"] for c in self.client.schema.get().get("classes", [])]
        if self.CLASS_NAME in existing:
            return

        self.client.schema.create_class({
            "class": self.CLASS_NAME,
            "description": "Medical document chunks for RAG",
            "vectorizer": "none",          # we supply our own vectors
            "properties": [
                {"name": "chunk_id",    "dataType": ["string"]},
                {"name": "content",     "dataType": ["text"]},
                {"name": "source",      "dataType": ["string"]},
                {"name": "chunk_index", "dataType": ["int"]},
                {"name": "word_count",  "dataType": ["int"]},
            ],
        })
        logger.info(f"Created Weaviate class '{self.CLASS_NAME}'")

    # ------------------------------------------------------------------

    def upsert(self, chunks: List[Dict]) -> int:
        upserted = 0
        with self.client.batch as batch:
            batch.batch_size = 50
            for chunk in chunks:
                if "embedding" not in chunk:
                    continue
                batch.add_data_object(
                    data_object={
                        "chunk_id":    chunk["id"],
                        "content":     chunk["content"],
                        "source":      chunk["source"],
                        "chunk_index": chunk.get("chunk_index", 0),
                        "word_count":  chunk.get("word_count", 0),
                    },
                    class_name=self.CLASS_NAME,
                    vector=chunk["embedding"],
                )
                upserted += 1
        logger.info(f"Upserted {upserted} chunks into Weaviate")
        return upserted

    def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict]:
        response = (
            self.client.query
            .get(self.CLASS_NAME, ["chunk_id", "content", "source", "chunk_index"])
            .with_near_vector({"vector": query_vector})
            .with_limit(top_k)
            .with_additional(["distance"])
            .do()
        )
        items = (
            response.get("data", {})
            .get("Get", {})
            .get(self.CLASS_NAME, [])
        )
        results = []
        for item in items:
            dist = item.get("_additional", {}).get("distance", 1.0)
            results.append({
                "id":          item.get("chunk_id", ""),
                "score":       round(1 - dist, 4),   # convert distance → similarity
                "content":     item.get("content", ""),
                "source":      item.get("source", ""),
                "chunk_index": item.get("chunk_index", 0),
            })
        return results

    def delete_all(self) -> bool:
        try:
            self.client.schema.delete_class(self.CLASS_NAME)
            self._ensure_schema()
            logger.info("Weaviate class cleared and recreated.")
            return True
        except Exception as e:
            logger.error(f"Failed to clear Weaviate: {e}")
            return False

    def count(self) -> int:
        try:
            result = (
                self.client.query
                .aggregate(self.CLASS_NAME)
                .with_meta_count()
                .do()
            )
            return (
                result.get("data", {})
                .get("Aggregate", {})
                .get(self.CLASS_NAME, [{}])[0]
                .get("meta", {})
                .get("count", 0)
            )
        except Exception as e:
            logger.error(f"Could not get count: {e}")
            return -1


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def get_vector_store(db_type: str = "pinecone") -> VectorStore:
    """
    Return a ready-to-use vector store instance.

    Args:
        db_type: "pinecone" or "weaviate"
    """
    db_type = db_type.lower().strip()
    if db_type == "pinecone":
        return PineconeStore()
    if db_type == "weaviate":
        return WeaviateStore()
    raise ValueError(f"Unknown vector store type: '{db_type}'. Choose 'pinecone' or 'weaviate'.")
