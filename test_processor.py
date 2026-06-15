#!/usr/bin/env python3
"""Quick test of the PDF processing pipeline."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.pdf_processor import PDFProcessor

proc = PDFProcessor(chunk_size=512, chunk_overlap=64)
chunks = proc.process_directory("data/medical_pdfs")
proc.print_summary(chunks)

if chunks:
    c = chunks[0]
    print("=== Sample Chunk ===")
    print(f"id          : {c['id']}")
    print(f"source      : {c['source']}")
    print(f"chunk_index : {c['chunk_index']} / {c['total_chunks']}")
    print(f"word_count  : {c['word_count']}")
    print(f"char_count  : {c['char_count']}")
    print(f"content:\n{c['content'][:400]}")
    print("====================")
