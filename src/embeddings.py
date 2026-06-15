import logging
from typing import List, Dict
from langchain_openai import OpenAIEmbeddings
from config.settings import settings

logger = logging.getLogger(__name__)


class EmbeddingsManager:
    """Manage text embeddings using OpenAI."""

    def __init__(self, model: str = "text-embedding-3-small"):
        """
        Initialize embeddings manager.

        Args:
            model: OpenAI embedding model to use
        """
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")

        self.embeddings = OpenAIEmbeddings(
            api_key=settings.OPENAI_API_KEY,
            model=model
        )
        self.model = model
        logger.info(f"Initialized embeddings with model: {model}")

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        """
        Embed a list of documents.

        Args:
            documents: List of text documents to embed

        Returns:
            List of embedding vectors
        """
        try:
            embeddings = self.embeddings.embed_documents(documents)
            logger.info(f"Successfully embedded {len(documents)} documents")
            return embeddings
        except Exception as e:
            logger.error(f"Error embedding documents: {str(e)}")
            return []

    def embed_query(self, query: str) -> List[float]:
        """
        Embed a query string.

        Args:
            query: Query text to embed

        Returns:
            Embedding vector
        """
        try:
            embedding = self.embeddings.embed_query(query)
            logger.info(f"Successfully embedded query")
            return embedding
        except Exception as e:
            logger.error(f"Error embedding query: {str(e)}")
            return []

    def embed_documents_with_metadata(
        self,
        documents: List[Dict]
    ) -> List[Dict]:
        """
        Embed documents while preserving metadata.

        Args:
            documents: List of document dicts with 'content' and 'metadata'

        Returns:
            Documents with added 'embedding' field
        """
        texts = [doc["content"] for doc in documents]
        embeddings = self.embed_documents(texts)

        for doc, embedding in zip(documents, embeddings):
            doc["embedding"] = embedding

        return documents
