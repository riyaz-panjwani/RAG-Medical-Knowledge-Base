#!/usr/bin/env python3
"""
End-to-end ingestion pipeline:
  PDF files → chunks → embeddings → vector store

Run:
    source venv/bin/activate
    python run_pipeline.py                        # uses settings from .env
    python run_pipeline.py --db weaviate          # override vector DB
    python run_pipeline.py --dry-run              # chunk + embed, skip upsert
"""

import argparse
import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.pdf_processor import PDFProcessor
from src.embeddings import EmbeddingsManager
from config.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def parse_args():
    p = argparse.ArgumentParser(description="RAG ingestion pipeline")
    p.add_argument("--pdf-dir", default=settings.PDF_DATA_PATH,
                   help="Directory containing PDF files")
    p.add_argument("--db", default=settings.VECTOR_DB,
                   choices=["pinecone", "weaviate"],
                   help="Vector database backend")
    p.add_argument("--dry-run", action="store_true",
                   help="Stop before writing to the vector store")
    return p.parse_args()


def main():
    args = parse_args()

    print("\n" + "=" * 65)
    print("🏥  RAG Medical Knowledge Base — Ingestion Pipeline")
    print("=" * 65)
    print(f"  PDF directory : {args.pdf_dir}")
    print(f"  Vector store  : {args.db}")
    print(f"  Dry run       : {args.dry_run}")
    print("=" * 65 + "\n")

    # ------------------------------------------------------------------
    # Step 1 — PDF processing
    # ------------------------------------------------------------------
    print("📄  Step 1/3  —  PDF Processing")
    processor = PDFProcessor(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
    )
    chunks = processor.process_directory(args.pdf_dir)
    processor.print_summary(chunks)

    if not chunks:
        print("❌  No chunks produced. Check that PDFs exist in", args.pdf_dir)
        sys.exit(1)

    # ------------------------------------------------------------------
    # Step 2 — Embeddings
    # ------------------------------------------------------------------
    print("🔢  Step 2/3  —  Generating Embeddings")

    if not settings.OPENAI_API_KEY:
        print("❌  OPENAI_API_KEY is not set. Add it to your .env file and re-run.")
        sys.exit(1)

    embedder = EmbeddingsManager()
    embedded_chunks = embedder.embed_chunks(chunks)
    embedder.print_summary(embedded_chunks)

    if not embedded_chunks:
        print("❌  Embedding failed for all chunks.")
        sys.exit(1)

    if args.dry_run:
        print("ℹ️   Dry-run mode — skipping vector store upsert.\n")
        sys.exit(0)

    # ------------------------------------------------------------------
    # Step 3 — Vector store
    # ------------------------------------------------------------------
    print(f"🗄️   Step 3/3  —  Upserting into {args.db.capitalize()}")

    if args.db == "pinecone" and not settings.PINECONE_API_KEY:
        print("❌  PINECONE_API_KEY is not set. Add it to your .env file and re-run.")
        sys.exit(1)

    from src.vector_store import get_vector_store
    store = get_vector_store(args.db)
    n = store.upsert(embedded_chunks)
    total_in_store = store.count()

    print("\n" + "=" * 65)
    print("✅  Pipeline Complete")
    print("=" * 65)
    print(f"  Chunks processed  : {len(chunks)}")
    print(f"  Chunks embedded   : {len(embedded_chunks)}")
    print(f"  Vectors upserted  : {n}")
    print(f"  Vectors in store  : {total_in_store}")
    print("=" * 65 + "\n")
    print("👉  Next: run  streamlit run app.py  to start the UI.")


if __name__ == "__main__":
    main()
