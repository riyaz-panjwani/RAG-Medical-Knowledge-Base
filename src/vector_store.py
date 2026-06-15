import logging
from typing import List, Dict, Optional
from config.settings import settings

logger = logging.getLogger(__name__)


class VectorStoreBase:
    """Base class for vector store implementations."""

    def add_documents(self, documents: List[Dict]) -> bool:
        """Add documents to the vector store."""
        raise NotImplementedError

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
        """Search for similar documents."""
        raise NotImplementedError

    def delete_all(self) -> bool:
        """Clear all documents from the vector store."""
        raise NotImplementedError


class PineconeVectorStore(VectorStoreBase):
    """Pinecone vector store implementation."""

    def __init__(self, index_name: str = "medical-rag"):
        """
        Initialize Pinecone vector store.

        Args:
            index_name: Name of the Pinecone index
        """
        try:
            import pinecone

            pinecone.init(
                api_key=settings.PINECONE_API_KEY,
                environment=settings.PINECONE_ENVIRONMENT
            )
            self.index = pinecone.Index(index_name)
            self.index_name = index_name
            logger.info(f"Connected to Pinecone index: {index_name}")
        except Exception as e:
            logger.error(f"Error initializing Pinecone: {str(e)}")
            raise

    def add_documents(self, documents: List[Dict]) -> bool:
        """Add documents with embeddings to Pinecone."""
        try:
            vectors = []
            for i, doc in enumerate(documents):
                if "embedding" not in doc:
                    logger.warning(f"Document {i} missing embedding, skipping")
                    continue

                vectors.append((
                    f"doc-{i}",
                    doc["embedding"],
                    {
                        "content": doc.get("content", ""),
                        "source": doc.get("source", ""),
                        "page": doc.get("page", 0)
                    }
                ))

            if vectors:
                self.index.upsert(vectors=vectors)
                logger.info(f"Added {len(vectors)} documents to Pinecone")
                return True
            return False
        except Exception as e:
            logger.error(f"Error adding documents to Pinecone: {str(e)}")
            return False

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
        """Search for similar documents in Pinecone."""
        try:
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )

            documents = []
            for match in results.get("matches", []):
                doc = {
                    "id": match["id"],
                    "score": match["score"],
                    "content": match["metadata"].get("content", ""),
                    "source": match["metadata"].get("source", ""),
                    "page": match["metadata"].get("page", 0)
                }
                documents.append(doc)

            logger.info(f"Retrieved {len(documents)} documents from Pinecone")
            return documents
        except Exception as e:
            logger.error(f"Error searching Pinecone: {str(e)}")
            return []

    def delete_all(self) -> bool:
        """Delete all documents from the index."""
        try:
            self.index.delete(delete_all=True, namespace="")
            logger.info("Cleared all documents from Pinecone index")
            return True
        except Exception as e:
            logger.error(f"Error clearing Pinecone index: {str(e)}")
            return False


class WeaviateVectorStore(VectorStoreBase):
    """Weaviate vector store implementation."""

    def __init__(self, url: str = "http://localhost:8080"):
        """
        Initialize Weaviate vector store.

        Args:
            url: Weaviate instance URL
        """
        try:
            import weaviate

            self.client = weaviate.Client(
                url=url,
                auth_client_secret=weaviate.AuthApiKey(
                    api_key=settings.WEAVIATE_API_KEY
                ) if settings.WEAVIATE_API_KEY else None
            )
            self.url = url
            logger.info(f"Connected to Weaviate at {url}")
        except Exception as e:
            logger.error(f"Error initializing Weaviate: {str(e)}")
            raise

    def add_documents(self, documents: List[Dict]) -> bool:
        """Add documents to Weaviate."""
        try:
            for i, doc in enumerate(documents):
                if "embedding" not in doc:
                    logger.warning(f"Document {i} missing embedding, skipping")
                    continue

                self.client.data_object.create(
                    data_object={
                        "content": doc.get("content", ""),
                        "source": doc.get("source", ""),
                        "page": doc.get("page", 0)
                    },
                    class_name="MedicalDocument",
                    vector=doc["embedding"]
                )

            logger.info(f"Added {len(documents)} documents to Weaviate")
            return True
        except Exception as e:
            logger.error(f"Error adding documents to Weaviate: {str(e)}")
            return False

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
        """Search for similar documents in Weaviate."""
        try:
            results = self.client.query.get(
                "MedicalDocument",
                ["content", "source", "page", "_additional {vector distance}"]
            ).with_near_vector(
                {"vector": query_embedding}
            ).with_limit(top_k).do()

            documents = []
            for item in results.get("data", {}).get("Get", {}).get("MedicalDocument", []):
                doc = {
                    "content": item.get("content", ""),
                    "source": item.get("source", ""),
                    "page": item.get("page", 0),
                    "score": item.get("_additional", {}).get("distance", 0)
                }
                documents.append(doc)

            logger.info(f"Retrieved {len(documents)} documents from Weaviate")
            return documents
        except Exception as e:
            logger.error(f"Error searching Weaviate: {str(e)}")
            return []

    def delete_all(self) -> bool:
        """Delete all documents from Weaviate."""
        try:
            self.client.batch.delete_objects(
                class_name="MedicalDocument",
                where={"path": ["id"], "operator": "Like", "valueString": "*"}
            )
            logger.info("Cleared all documents from Weaviate")
            return True
        except Exception as e:
            logger.error(f"Error clearing Weaviate: {str(e)}")
            return False


def get_vector_store(db_type: str = "pinecone") -> VectorStoreBase:
    """
    Factory function to get the appropriate vector store.

    Args:
        db_type: Type of vector store ('pinecone' or 'weaviate')

    Returns:
        VectorStore instance
    """
    if db_type.lower() == "pinecone":
        return PineconeVectorStore(settings.PINECONE_INDEX_NAME)
    elif db_type.lower() == "weaviate":
        return WeaviateVectorStore(settings.WEAVIATE_URL)
    else:
        raise ValueError(f"Unknown vector store type: {db_type}")
