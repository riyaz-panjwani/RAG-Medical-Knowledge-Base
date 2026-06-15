import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # --- Free stack (primary) ---
    GROQ_API_KEY  = os.getenv("GROQ_API_KEY")        # console.groq.com — free
    GROQ_MODEL    = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

    EMBED_MODEL   = os.getenv("EMBED_MODEL", "all-MiniLM-L6-v2")   # local, free
    VECTOR_DB     = os.getenv("VECTOR_DB", "chroma")                 # local, free

    # --- Optional paid alternatives ---
    OPENAI_API_KEY     = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY   = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "medical-rag")
    WEAVIATE_URL       = os.getenv("WEAVIATE_URL", "http://localhost:8080")
    WEAVIATE_API_KEY   = os.getenv("WEAVIATE_API_KEY")

    # --- Document processing ---
    CHUNK_SIZE    = int(os.getenv("CHUNK_SIZE", 512))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 64))
    TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", 5))

    # --- Paths ---
    PDF_DATA_PATH        = "data/medical_pdfs"
    CHROMA_PERSIST_PATH  = "data/chroma_db"
    PROCESSED_DATA_PATH  = "data/processed"


settings = Settings()
