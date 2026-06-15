#!/usr/bin/env python3
"""
End-to-end ingestion pipeline — 100% free stack:
  PDF files  →  chunks  →  local embeddings  →  ChromaDB

Run:
    source venv/bin/activate
    python run_pipeline.py                  # full ingest
    python run_pipeline.py --dry-run        # chunk + embed, skip DB write
    python run_pipeline.py --reset          # wipe ChromaDB and re-ingest
"""

import argparse
import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.pdf_processor import PDFProcessor
from src.embeddings import EmbeddingsManager
from src.vector_store import VectorStore
from config.settings import settings

logging.basicConfig(
    level=logging.WARNING,          # suppress noisy library logs
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logging.getLogger("src").setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def parse_args():
    p = argparse.ArgumentParser(description="RAG ingestion pipeline (free stack)")
    p.add_argument("--pdf-dir",  default=settings.PDF_DATA_PATH)
    p.add_argument("--dry-run",  action="store_true",
                   help="Skip writing to ChromaDB")
    p.add_argument("--reset",    action="store_true",
                   help="Wipe ChromaDB before ingesting")
    return p.parse_args()


def main():
    args = parse_args()

    print("\n" + "=" * 65)
    print("🏥  RAG Medical Knowledge Base — Free Stack Pipeline")
    print("=" * 65)
    print(f"  Embeddings   : sentence-transformers ({settings.EMBED_MODEL})")
    print(f"  Vector DB    : ChromaDB  (local)")
    print(f"  LLM          : Groq  (llama-3.1-8b-instant)")
    print(f"  PDF dir      : {args.pdf_dir}")
    print(f"  Dry run      : {args.dry_run}")
    print("=" * 65 + "\n")

    # ── Step 1: PDF processing ────────────────────────────────────────
    print("📄  Step 1/3  —  PDF Processing")
    processor = PDFProcessor(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
    )
    chunks = processor.process_directory(args.pdf_dir)
    processor.print_summary(chunks)

    if not chunks:
        print(f"❌  No chunks produced. Add PDFs to  {args.pdf_dir}  and re-run.")
        sys.exit(1)

    # ── Step 2: Embeddings ────────────────────────────────────────────
    print("🔢  Step 2/3  —  Generating Embeddings  (local, free)")
    embedder = EmbeddingsManager(model_name=settings.EMBED_MODEL)
    embedded = embedder.embed_chunks(chunks)
    embedder.print_summary(embedded)

    if args.dry_run:
        print("ℹ️   Dry-run — skipping ChromaDB write.\n")
        sys.exit(0)

    # ── Step 3: ChromaDB upsert ───────────────────────────────────────
    print("🗄️   Step 3/3  —  Storing in ChromaDB  (local, free)")
    store = VectorStore(persist_dir=settings.CHROMA_PERSIST_PATH)

    if args.reset:
        print("   ⚠️  Resetting ChromaDB collection…")
        store.delete_all()

    n = store.upsert(embedded)
    store.print_summary(n)

    print("=" * 65)
    print("✅  Pipeline complete — knowledge base is ready.")
    print("=" * 65)
    print("\n👉  Next: add your Groq key to .env, then run:")
    print("       streamlit run app.py\n")


if __name__ == "__main__":
    main()
