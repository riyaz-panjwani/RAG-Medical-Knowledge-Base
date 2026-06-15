import os
import logging
from typing import List, Dict
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_directories(paths: List[str]) -> None:
    """Create directories if they don't exist."""
    for path in paths:
        Path(path).mkdir(parents=True, exist_ok=True)
        logger.info(f"Directory ready: {path}")


def get_pdf_files(directory: str) -> List[str]:
    """Get all PDF files from a directory."""
    pdf_files = []
    if os.path.exists(directory):
        pdf_files = [
            os.path.join(directory, f)
            for f in os.listdir(directory)
            if f.lower().endswith(".pdf")
        ]
    logger.info(f"Found {len(pdf_files)} PDF files in {directory}")
    return pdf_files


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """
    Split text into overlapping chunks.

    Args:
        text: Text to chunk
        chunk_size: Size of each chunk in characters
        overlap: Overlap between chunks in characters

    Returns:
        List of text chunks
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks


def format_retrieved_docs(docs: List[Dict]) -> str:
    """Format retrieved documents for display."""
    formatted = ""
    for i, doc in enumerate(docs, 1):
        formatted += f"\n**Document {i}:**\n"
        formatted += f"{doc.get('content', '')}\n"
        formatted += f"*Source: {doc.get('source', 'Unknown')}*\n"
    return formatted


def validate_api_keys(required_keys: List[str]) -> bool:
    """Check if required API keys are set."""
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    if missing_keys:
        logger.warning(f"Missing API keys: {', '.join(missing_keys)}")
        return False
    return True
