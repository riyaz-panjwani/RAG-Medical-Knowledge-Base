import logging
from typing import List, Dict, Tuple
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config.settings import settings
from src.embeddings import EmbeddingsManager
from src.vector_store import get_vector_store

logger = logging.getLogger(__name__)


MEDICAL_RAG_PROMPT = """You are a helpful medical knowledge assistant. Based on the provided medical documents, answer the user's question accurately and helpfully. If the information is not available in the documents, say so clearly.

Medical Documents:
{context}

Question: {question}

Answer: """


class RAGPipeline:
    """End-to-end RAG pipeline for medical knowledge retrieval."""

    def __init__(
        self,
        vector_db: str = "pinecone",
        llm_provider: str = "openai",
        temperature: float = 0.7,
        top_k: int = 5
    ):
        """
        Initialize RAG pipeline.

        Args:
            vector_db: Vector database to use ('pinecone' or 'weaviate')
            llm_provider: LLM provider to use ('openai' or 'mistral')
            temperature: Temperature for LLM responses
            top_k: Number of documents to retrieve
        """
        self.embeddings = EmbeddingsManager()
        self.vector_store = get_vector_store(vector_db)
        self.top_k = top_k
        self.temperature = temperature

        # Initialize LLM
        if llm_provider.lower() == "openai":
            self.llm = ChatOpenAI(
                api_key=settings.OPENAI_API_KEY,
                model=settings.OPENAI_MODEL,
                temperature=temperature
            )
        else:
            raise ValueError(f"Unknown LLM provider: {llm_provider}")

        # Initialize prompt template and chain
        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=MEDICAL_RAG_PROMPT
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
        logger.info(f"Initialized RAG pipeline with {vector_db} and {llm_provider}")

    def index_documents(self, documents: List[Dict]) -> bool:
        """
        Index documents in the vector store.

        Args:
            documents: List of documents with 'content' and 'metadata'

        Returns:
            Success status
        """
        try:
            # Embed documents
            embedded_docs = self.embeddings.embed_documents_with_metadata(documents)

            # Add to vector store
            success = self.vector_store.add_documents(embedded_docs)

            if success:
                logger.info(f"Successfully indexed {len(documents)} documents")
            return success
        except Exception as e:
            logger.error(f"Error indexing documents: {str(e)}")
            return False

    def retrieve(self, query: str) -> List[Dict]:
        """
        Retrieve relevant documents for a query.

        Args:
            query: Query string

        Returns:
            List of relevant documents
        """
        try:
            # Embed query
            query_embedding = self.embeddings.embed_query(query)

            if not query_embedding:
                logger.warning("Failed to embed query")
                return []

            # Search vector store
            results = self.vector_store.search(query_embedding, self.top_k)
            logger.info(f"Retrieved {len(results)} documents for query")
            return results
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            return []

    def generate(self, query: str, retrieved_docs: List[Dict]) -> str:
        """
        Generate an answer based on retrieved documents.

        Args:
            query: Original query
            retrieved_docs: Retrieved documents from vector store

        Returns:
            Generated answer
        """
        try:
            # Format context from retrieved documents
            context = self._format_context(retrieved_docs)

            # Generate answer
            answer = self.chain.run(context=context, question=query)
            logger.info("Successfully generated answer")
            return answer
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            return "Unable to generate an answer at this time."

    def query(self, query: str) -> Tuple[str, List[Dict]]:
        """
        Complete RAG pipeline: retrieve and generate.

        Args:
            query: User query

        Returns:
            Tuple of (generated_answer, retrieved_documents)
        """
        # Retrieve documents
        retrieved_docs = self.retrieve(query)

        # Generate answer
        answer = self.generate(query, retrieved_docs)

        return answer, retrieved_docs

    def _format_context(self, documents: List[Dict]) -> str:
        """Format retrieved documents as context for the LLM."""
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(
                f"[Document {i} - {doc.get('source', 'Unknown')}]\n"
                f"{doc.get('content', '')}"
            )
        return "\n\n".join(context_parts)

    def clear_index(self) -> bool:
        """Clear the vector store."""
        return self.vector_store.delete_all()
