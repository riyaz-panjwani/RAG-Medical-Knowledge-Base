import logging
from typing import List, Dict
from pathlib import Path
import PyPDF2

logger = logging.getLogger(__name__)


class PDFScraper:
    """Extract text and metadata from PDF documents."""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract all text from a PDF file.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Extracted text content
        """
        text = ""
        try:
            with open(pdf_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text()
                logger.info(f"Extracted {len(text)} characters from {pdf_path}")
        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {str(e)}")
        return text

    def process_pdfs(self, pdf_directory: str) -> List[Dict]:
        """
        Process all PDFs in a directory.

        Args:
            pdf_directory: Directory containing PDF files

        Returns:
            List of document chunks with metadata
        """
        documents = []
        pdf_files = list(Path(pdf_directory).glob("*.pdf"))

        for pdf_file in pdf_files:
            logger.info(f"Processing: {pdf_file.name}")
            text = self.extract_text_from_pdf(str(pdf_file))

            if text:
                chunks = self._chunk_text(text)
                for i, chunk in enumerate(chunks):
                    documents.append({
                        "content": chunk,
                        "source": pdf_file.name,
                        "page": i,
                        "metadata": {
                            "filename": pdf_file.name,
                            "chunk_id": i
                        }
                    })

        logger.info(f"Created {len(documents)} document chunks")
        return documents

    def _chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start = end - self.chunk_overlap

        return chunks

    def extract_metadata(self, pdf_path: str) -> Dict:
        """Extract metadata from PDF."""
        metadata = {}
        try:
            with open(pdf_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)
                if pdf_reader.metadata:
                    metadata = dict(pdf_reader.metadata)
                metadata["page_count"] = len(pdf_reader.pages)
        except Exception as e:
            logger.error(f"Error extracting metadata from {pdf_path}: {str(e)}")
        return metadata
