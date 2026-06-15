# RAG Medical Knowledge Base

A retrieval-augmented generation (RAG) system for medical knowledge that demonstrates modern LLM architecture and production patterns.

## Overview

This project builds an end-to-end RAG pipeline that:
- Scrapes and processes medical PDFs
- Embeds documents into a vector database
- Retrieves relevant medical information for LLM queries
- Provides a user-friendly Streamlit interface for medical knowledge lookup

## Tech Stack

- **LLM Framework**: LangChain
- **Vector DB**: Pinecone or Weaviate
- **LLM Provider**: OpenAI (GPT-4) or Mistral
- **UI**: Streamlit
- **PDF Processing**: PyPDF2, Langchain document loaders
- **Embeddings**: OpenAI embeddings or open-source alternatives

## Project Structure

```
RAG-Medical-Knowledge-Base/
├── src/
│   ├── pdf_scraper.py          # PDF extraction and processing
│   ├── vector_store.py         # Vector DB initialization & operations
│   ├── embeddings.py           # Embedding pipeline
│   ├── rag_pipeline.py         # Core RAG retrieval & generation
│   └── utils.py                # Helper utilities
├── data/
│   ├── medical_pdfs/           # Raw PDF documents
│   └── processed/              # Processed chunks
├── models/
│   └── embeddings_cache/       # Cached embeddings
├── config/
│   ├── settings.py             # Configuration management
│   └── prompts.py              # LLM prompt templates
├── app.py                      # Main Streamlit application
├── requirements.txt            # Dependencies
└── README.md                   # Project documentation
```

## Features

- **PDF Document Processing**: Extract and chunk medical PDFs intelligently
- **Vector Embeddings**: Convert text chunks into dense vector representations
- **Semantic Search**: Find relevant medical information using similarity search
- **LLM Integration**: Generate contextual answers from retrieved documents
- **Interactive UI**: Streamlit dashboard for real-time medical knowledge lookup
- **Production Ready**: Error handling, caching, and performance optimization

## Setup & Installation

1. Clone and navigate to the project:
```bash
cd RAG-Medical-Knowledge-Base
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys:
# OPENAI_API_KEY=your_key_here
# PINECONE_API_KEY=your_key_here
# PINECONE_ENVIRONMENT=your_env_here
```

4. Run the Streamlit app:
```bash
streamlit run app.py
```

## Usage

1. **Upload Medical PDFs**: Use the sidebar to upload PDF documents
2. **Process Documents**: System automatically chunks and embeds PDFs
3. **Query**: Enter your medical question in the search box
4. **Get Answers**: Receive AI-generated answers with document citations

## Next Steps

- [ ] Implement PDF scraper with multiple document sources
- [ ] Set up vector database connection (Pinecone/Weaviate)
- [ ] Build RAG pipeline with LangChain
- [ ] Create Streamlit UI with live demo
- [ ] Add document citations and source tracking
- [ ] Implement caching and performance optimization
- [ ] Deploy to cloud (Streamlit Cloud, AWS, etc.)
