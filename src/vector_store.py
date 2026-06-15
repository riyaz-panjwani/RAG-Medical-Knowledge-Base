"""
Vector store using ChromaDB — fully local, no account or API key needed.
Data persists in  data/chroma_db/  between runs.
"""

import logging
from typing import List, Dict
import chromadb
from chromadb.config import Settings as ChromaSettings

logger = logging.getLogger(__name__)

PERSIST_DIR = "data/chroma_db"
COLLECTION  = "medical_knowledge"


class VectorStore:
    """
    ChromaDB-backed vector store.

    Persists to disk so you only need to ingest once.
    Supports upsert, semantic search, delete, and count.
    """

    def __init__(self, persist_dir: str = PERSIST_DIR):
        self.client = chromadb.PersistentClient(
            path=persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION,
            metadata={"hnsw:space": "cosine"},   # cosine similarity
        )
        logger.info(
            f"ChromaDB ready at '{persist_dir}' "
            f"— collection '{COLLECTION}' has {self.collection.count()} vectors"
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def upsert(self, chunks: List[Dict]) -> int:
        """
        Insert or update chunks.  Chunks without 'embedding' are skipped.

        Returns the number of vectors successfully upserted.
        """
        ids, embeddings, documents, metadatas = [], [], [], []

        for chunk in chunks:
            if "embedding" not in chunk:
                logger.warning(f"Chunk '{chunk.get('id')}' has no embedding — skipped.")
                continue
            ids.append(chunk["id"])
            embeddings.append(chunk["embedding"])
            documents.append(chunk["content"])
            metadatas.append({
                "source":      chunk.get("source", ""),
                "chunk_index": chunk.get("chunk_index", 0),
                "word_count":  chunk.get("word_count", 0),
            })

        if not ids:
            return 0

        # ChromaDB upsert handles duplicates automatically
        self.collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )
        logger.info(f"Upserted {len(ids)} vectors into ChromaDB")
        return len(ids)

    def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict]:
        """
        Return the top_k most similar chunks to query_vector.

        Returns list of dicts: id, content, source, chunk_index, score.
        """
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=min(top_k, self.collection.count()),
            include=["documents", "metadatas", "distances"],
        )

        hits = []
        for i, doc_id in enumerate(results["ids"][0]):
            distance = results["distances"][0][i]
            hits.append({
                "id":          doc_id,
                "content":     results["documents"][0][i],
                "source":      results["metadatas"][0][i].get("source", ""),
                "chunk_index": results["metadatas"][0][i].get("chunk_index", 0),
                "score":       round(1 - distance, 4),   # cosine distance → similarity
            })

        return hits

    def delete_all(self) -> bool:
        """Wipe and recreate the collection."""
        try:
            self.client.delete_collection(COLLECTION)
            self.collection = self.client.get_or_create_collection(
                name=COLLECTION,
                metadata={"hnsw:space": "cosine"},
            )
            logger.info("ChromaDB collection cleared.")
            return True
        except Exception as e:
            logger.error(f"Failed to clear collection: {e}")
            return False

    def count(self) -> int:
        return self.collection.count()

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def print_summary(self, n_upserted: int) -> None:
        total = self.collection.count()
        print("\n" + "=" * 65)
        print("🗄️   VECTOR STORE SUMMARY")
        print("=" * 65)
        print(f"  Backend          : ChromaDB  (local, free)")
        print(f"  Persist path     : {PERSIST_DIR}")
        print(f"  Collection       : {COLLECTION}")
        print(f"  Vectors upserted : {n_upserted}")
        print(f"  Total in store   : {total}")
        print("=" * 65 + "\n")


# Keep factory function so run_pipeline.py doesn't need changes
def get_vector_store(db_type: str = "chroma") -> VectorStore:
    return VectorStore()
