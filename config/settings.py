import os
from dotenv import load_dotenv

load_dotenv()


def _get(key: str, default: str = "") -> str:
    """
    Read a config value — checks .env first, then Streamlit secrets (cloud).
    Falls back to default if neither is set.
    """
    val = os.getenv(key, "")
    if val:
        return val
    # On Streamlit Cloud there's no .env — read from st.secrets instead
    try:
        import streamlit as st
        return st.secrets.get(key, default)
    except Exception:
        return default


class Settings:
    # --- Free stack (primary) ---
    GROQ_API_KEY  = _get("GROQ_API_KEY")
    GROQ_MODEL    = _get("GROQ_MODEL", "llama-3.1-8b-instant")
    EMBED_MODEL   = _get("EMBED_MODEL", "all-MiniLM-L6-v2")
    VECTOR_DB     = _get("VECTOR_DB",   "chroma")

    # --- Optional paid alternatives ---
    OPENAI_API_KEY      = _get("OPENAI_API_KEY")
    PINECONE_API_KEY    = _get("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = _get("PINECONE_INDEX_NAME", "medical-rag")
    WEAVIATE_URL        = _get("WEAVIATE_URL", "http://localhost:8080")
    WEAVIATE_API_KEY    = _get("WEAVIATE_API_KEY")

    # --- Document processing ---
    CHUNK_SIZE    = int(_get("CHUNK_SIZE",    "512"))
    CHUNK_OVERLAP = int(_get("CHUNK_OVERLAP", "64"))
    TOP_K_RESULTS = int(_get("TOP_K_RESULTS", "5"))

    # --- Paths ---
    PDF_DATA_PATH        = "data/medical_pdfs"
    CHROMA_PERSIST_PATH  = "data/vector_store"   # numpy-based store
    PROCESSED_DATA_PATH  = "data/processed"


settings = Settings()
