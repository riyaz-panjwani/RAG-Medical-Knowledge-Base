import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

    # Vector Database
    VECTOR_DB = os.getenv("VECTOR_DB", "pinecone")  # pinecone or weaviate

    # Pinecone Configuration
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "medical-rag")

    # Weaviate Configuration
    WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
    WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

    # Mistral Configuration
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

    # Document Processing
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 500))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 100))

    # RAG Pipeline
    TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", 5))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", 1000))

    # File Paths
    PDF_DATA_PATH = "data/medical_pdfs"
    PROCESSED_DATA_PATH = "data/processed"
    EMBEDDINGS_CACHE_PATH = "models/embeddings_cache"


settings = Settings()
