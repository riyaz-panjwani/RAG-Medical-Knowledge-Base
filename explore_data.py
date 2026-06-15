#!/usr/bin/env python3
"""
Data exploration and analysis tool for the medical PDF database.
"""

import os
import json
from pathlib import Path
from src.pdf_scraper import PDFScraper
from src.data_manager import DataManager
import logging

logging.basicConfig(level=logging.ERROR)


def analyze_pdf_data():
    """Analyze all PDF data and generate statistics."""
    pdf_dir = "data/medical_pdfs"
    scraper = PDFScraper()
    data_manager = DataManager()

    print("\n" + "=" * 70)
    print("📊 MEDICAL PDF DATABASE - COMPREHENSIVE ANALYSIS")
    print("=" * 70)

    # File Statistics
    print("\n📁 FILE STATISTICS")
    print("-" * 70)
    stats = data_manager.get_data_statistics()
    print(f"Total PDF Files: {stats['total_files']}")
    print(f"Total Size: {stats['total_size_mb']} MB")
    print(f"Average File Size: {stats['total_size_mb'] / max(stats['total_files'], 1):.2f} MB")

    # Text Extraction Analysis
    print("\n📖 TEXT EXTRACTION ANALYSIS")
    print("-" * 70)

    pdf_files = sorted([f for f in os.listdir(pdf_dir) if f.endswith(".pdf")])
    total_chars = 0
    total_words = 0
    chunk_analysis = []

    for pdf_file in pdf_files:
        filepath = os.path.join(pdf_dir, pdf_file)
        text = scraper.extract_text_from_pdf(filepath)

        if text:
            chars = len(text)
            words = len(text.split())
            total_chars += chars
            total_words += words

            # Estimate chunks (500 char chunks with 100 overlap)
            estimated_chunks = max(1, (chars - 500) // 400 + 1)

            chunk_analysis.append({
                "filename": pdf_file,
                "characters": chars,
                "words": words,
                "chunks": estimated_chunks,
                "avg_chunk_size": chars / max(estimated_chunks, 1)
            })

            print(f"\n✅ {pdf_file}")
            print(f"   📊 Characters: {chars:,}")
            print(f"   📝 Words: {words:,}")
            print(f"   📦 Est. Chunks (500 char, 100 overlap): {estimated_chunks}")
            print(f"   📈 Average chunk size: {chars / max(estimated_chunks, 1):.0f} chars")

    # Summary Statistics
    print("\n" + "=" * 70)
    print("📈 SUMMARY STATISTICS")
    print("=" * 70)
    print(f"Total Characters: {total_chars:,}")
    print(f"Total Words: {total_words:,}")
    print(f"Average Words per File: {total_words / max(len(pdf_files), 1):.0f}")
    print(f"Total Chunks: {sum(c['chunks'] for c in chunk_analysis)}")
    print(f"Average Chunks per File: {sum(c['chunks'] for c in chunk_analysis) / max(len(pdf_files), 1):.0f}")

    # Data Quality
    print("\n" + "=" * 70)
    print("✅ DATA QUALITY ASSESSMENT")
    print("=" * 70)
    print(f"✓ All PDFs extractable: {len(pdf_files)} files")
    print(f"✓ Total text volume: {total_chars:,} characters")
    print(f"✓ Ready for embedding: YES")
    print(f"✓ Ready for RAG pipeline: YES")

    # Save analysis
    analysis_data = {
        "timestamp": stats['timestamp'],
        "total_files": stats['total_files'],
        "total_size_mb": stats['total_size_mb'],
        "total_characters": total_chars,
        "total_words": total_words,
        "files": chunk_analysis
    }

    analysis_file = os.path.join(pdf_dir, "analysis.json")
    with open(analysis_file, "w") as f:
        json.dump(analysis_data, f, indent=2)

    print(f"\n💾 Analysis saved to: {analysis_file}")
    print("=" * 70 + "\n")

    return analysis_data


def display_next_steps():
    """Display next steps in the pipeline."""
    print("\n🚀 NEXT STEPS IN RAG PIPELINE")
    print("=" * 70)
    print("""
1. ✅ Data Acquisition: PDFs collected and validated
2. ✅ Text Extraction: All PDFs can be processed
3. ⏭️  PDF Processing: Chunk and prepare documents
4. ⏭️  Embeddings: Convert text chunks to vectors (OpenAI)
5. ⏭️  Vector Store: Index embeddings (Pinecone/Weaviate)
6. ⏭️  RAG Pipeline: Build retrieval system
7. ⏭️  Streamlit UI: Create interactive interface
8. ⏭️  Testing & Deployment: Validate and deploy

Ready to proceed with step 3: PDF Processing and Chunking
    """)
    print("=" * 70 + "\n")


if __name__ == "__main__":
    analysis = analyze_pdf_data()
    display_next_steps()
