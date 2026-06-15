#!/usr/bin/env python3
"""
Example usage of the RAG Medical Knowledge Base pipeline.
"""

import logging
from src.pdf_scraper import PDFScraper
from src.rag_pipeline import RAGPipeline
from config.settings import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Example of using the RAG pipeline."""

    print("🏥 Medical RAG Knowledge Base - Example Usage\n")

    # Step 1: Initialize PDF Scraper
    print("Step 1: Scraping medical PDFs...")
    scraper = PDFScraper(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )

    # Process PDFs from the data directory
    documents = scraper.process_pdfs(settings.PDF_DATA_PATH)
    print(f"✅ Processed {len(documents)} document chunks\n")

    # Step 2: Initialize RAG Pipeline
    print("Step 2: Initializing RAG pipeline...")
    rag = RAGPipeline(
        vector_db="pinecone",  # or "weaviate"
        llm_provider="openai",  # or "mistral"
        temperature=0.7,
        top_k=settings.TOP_K_RESULTS
    )
    print("✅ RAG pipeline initialized\n")

    # Step 3: Index Documents
    print("Step 3: Indexing documents...")
    if documents:
        success = rag.index_documents(documents)
        if success:
            print(f"✅ Indexed {len(documents)} documents to vector database\n")
        else:
            print("❌ Failed to index documents\n")
            return
    else:
        print("⚠️  No documents found. Add PDFs to data/medical_pdfs/\n")
        return

    # Step 4: Query the RAG Pipeline
    print("Step 4: Querying the knowledge base...")
    test_queries = [
        "What are the symptoms of diabetes?",
        "How is hypertension treated?",
        "What is the role of insulin in the body?",
    ]

    for query in test_queries:
        print(f"\n❓ Question: {query}")
        print("-" * 50)

        # Query the RAG pipeline
        answer, retrieved_docs = rag.query(query)

        # Display answer
        print(f"\n📄 Answer:\n{answer}")

        # Display sources
        print(f"\n📚 Retrieved {len(retrieved_docs)} source documents:")
        for i, doc in enumerate(retrieved_docs, 1):
            print(f"\n  Document {i}:")
            print(f"  - Source: {doc.get('source', 'Unknown')}")
            print(f"  - Relevance Score: {doc.get('score', 'N/A'):.3f}")
            print(f"  - Content Preview: {doc.get('content', '')[:100]}...")

        print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
