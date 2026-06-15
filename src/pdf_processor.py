import logging
import re
from typing import List, Dict
from pathlib import Path
import PyPDF2

logger = logging.getLogger(__name__)


class PDFProcessor:
    """
    Robust PDF text extraction and chunking pipeline.

    Produces clean, semantically-aware chunks with rich metadata
    ready for embedding into a vector store.
    """

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 64):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process_directory(self, pdf_dir: str) -> List[Dict]:
        """
        Process all PDFs in a directory and return a flat list of chunks.

        Each chunk dict has:
            id          : "<filename>_chunk_<n>"
            content     : cleaned text
            source      : filename
            chunk_index : position in document
            total_chunks: total chunks for that document
            char_count  : length of content
            word_count  : word count of content
        """
        pdf_files = sorted(Path(pdf_dir).glob("*.pdf"))
        all_chunks: List[Dict] = []

        for pdf_path in pdf_files:
            logger.info(f"Processing {pdf_path.name}")
            chunks = self.process_single_pdf(str(pdf_path))
            all_chunks.extend(chunks)
            logger.info(f"  → {len(chunks)} chunks")

        logger.info(f"Total chunks produced: {len(all_chunks)}")
        return all_chunks

    def process_single_pdf(self, pdf_path: str) -> List[Dict]:
        """Extract, clean, chunk, and annotate one PDF."""
        raw_text = self._extract_text(pdf_path)
        if not raw_text:
            logger.warning(f"No text extracted from {pdf_path}")
            return []

        clean = self._clean_text(raw_text)
        raw_chunks = self._chunk(clean)
        total = len(raw_chunks)
        filename = Path(pdf_path).name

        chunks = []
        for idx, text in enumerate(raw_chunks):
            chunks.append({
                "id": f"{filename}_chunk_{idx}",
                "content": text,
                "source": filename,
                "chunk_index": idx,
                "total_chunks": total,
                "char_count": len(text),
                "word_count": len(text.split()),
            })

        return chunks

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _extract_text(self, pdf_path: str) -> str:
        """Extract raw text from every page of a PDF."""
        pages = []
        try:
            with open(pdf_path, "rb") as fh:
                reader = PyPDF2.PdfReader(fh)
                for page in reader.pages:
                    page_text = page.extract_text() or ""
                    pages.append(page_text)
        except Exception as e:
            logger.error(f"Extraction failed for {pdf_path}: {e}")
        return "\n".join(pages)

    def _clean_text(self, text: str) -> str:
        """Normalise whitespace and remove artefacts."""
        # Collapse runs of whitespace / blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        # Strip leading/trailing whitespace per line
        lines = [line.strip() for line in text.splitlines()]
        text = "\n".join(lines)
        return text.strip()

    def _chunk(self, text: str) -> List[str]:
        """
        Split on sentence/paragraph boundaries wherever possible,
        falling back to hard character limits.
        Overlapping window keeps context across chunk boundaries.
        """
        # Prefer splitting at paragraph breaks first
        paragraphs = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]

        chunks: List[str] = []
        current = ""

        for para in paragraphs:
            # If adding this paragraph keeps us under the limit, accumulate
            if len(current) + len(para) + 1 <= self.chunk_size:
                current = (current + "\n" + para).strip()
            else:
                # Flush what we have
                if current:
                    chunks.append(current)
                # If the paragraph itself is too big, hard-split it
                if len(para) > self.chunk_size:
                    sub_chunks = self._hard_split(para)
                    # Keep last sub-chunk as start of next window
                    chunks.extend(sub_chunks[:-1])
                    current = sub_chunks[-1] if sub_chunks else ""
                else:
                    current = para

        if current:
            chunks.append(current)

        # Apply overlap: prepend tail of previous chunk to each chunk
        if self.chunk_overlap > 0 and len(chunks) > 1:
            overlapped: List[str] = [chunks[0]]
            for i in range(1, len(chunks)):
                tail = chunks[i - 1][-self.chunk_overlap:]
                overlapped.append((tail + " " + chunks[i]).strip())
            chunks = overlapped

        return [c for c in chunks if c]

    def _hard_split(self, text: str) -> List[str]:
        """Hard character-limit split for oversized paragraphs."""
        step = max(1, self.chunk_size - self.chunk_overlap)
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            start += step
        return chunks

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def print_summary(self, chunks: List[Dict]) -> None:
        """Print a human-readable processing report."""
        if not chunks:
            print("No chunks to report.")
            return

        sources = {}
        for c in chunks:
            sources.setdefault(c["source"], []).append(c)

        print("\n" + "=" * 65)
        print("📄 PDF PROCESSING SUMMARY")
        print("=" * 65)
        print(f"  Total documents : {len(sources)}")
        print(f"  Total chunks    : {len(chunks)}")
        avg_words = sum(c["word_count"] for c in chunks) / len(chunks)
        print(f"  Avg words/chunk : {avg_words:.0f}")
        print()
        print(f"  {'File':<40} {'Chunks':>6}  {'Avg words':>9}")
        print(f"  {'-'*40}  {'-'*6}  {'-'*9}")
        for src, src_chunks in sorted(sources.items()):
            avg = sum(c["word_count"] for c in src_chunks) / len(src_chunks)
            print(f"  {src:<40} {len(src_chunks):>6}  {avg:>9.0f}")
        print("=" * 65 + "\n")
