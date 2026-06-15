# 🏥 RAG Medical Knowledge Base

> **Live Demo:** [rag-medical-knowledge-base-dny9j4bzqcr7pddap97kwb.streamlit.app](https://rag-medical-knowledge-base-dny9j4bzqcr7pddap97kwb.streamlit.app)

An end-to-end **Retrieval-Augmented Generation (RAG)** system for medical knowledge — built with a 100% free stack. Ask natural language questions and get AI-generated answers grounded in source medical documents, with citations.

---

## 🎥 Demo

![Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-red?style=for-the-badge&logo=streamlit)

**Try it:** [Click here to open the live app](https://rag-medical-knowledge-base-dny9j4bzqcr7pddap97kwb.streamlit.app)

Example questions:
- *"What are the symptoms of diabetes?"*
- *"How do you prevent heart disease?"*
- *"What medications are used for hypertension?"*
- *"What is the difference between Type 1 and Type 2 diabetes?"*

---

## 🏗️ Architecture

```
Medical PDFs
     │
     ▼
PDF Processor          → Extracts & chunks text (PyPDF2)
     │
     ▼
Embedding Model        → sentence-transformers/all-MiniLM-L6-v2 (local, free)
     │
     ▼
Vector Store           → Numpy cosine similarity search (no DB needed)
     │
     ▼
Retriever              → Top-K most relevant chunks
     │
     ▼
Groq LLM               → llama-3.1-8b-instant (free API)
     │
     ▼
Streamlit UI           → Chat interface with source citations
```

---

## 🛠️ Tech Stack

| Component | Technology | Cost |
|-----------|-----------|------|
| **Embeddings** | `sentence-transformers` (all-MiniLM-L6-v2) | Free — runs locally |
| **Vector Search** | Numpy cosine similarity | Free — no DB needed |
| **LLM** | Groq API — Llama 3.1 8B Instant | Free tier (~14k req/day) |
| **UI** | Streamlit | Free |
| **PDF Processing** | PyPDF2 + ReportLab | Free |
| **Deployment** | Streamlit Cloud | Free |

**Total monthly cost: $0**

---

## 📄 Knowledge Base

5 medical PDF documents covering:
- **Diabetes** — Types, symptoms, management, complications
- **Hypertension** — Blood pressure categories, treatment options
- **Heart Disease** — Risk factors, prevention strategies
- **Mental Health** — Conditions, therapy options, self-care
- **Respiratory Health** — Asthma, COPD, pneumonia, prevention

---

## 🚀 Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/riyaz-panjwani/RAG-Medical-Knowledge-Base.git
cd RAG-Medical-Knowledge-Base
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your free Groq API key
Get a free key at [console.groq.com](https://console.groq.com) — no credit card needed.

```bash
cp .env.example .env
# Edit .env and add your key:
# GROQ_API_KEY=your_key_here
```

### 5. Ingest PDFs into the vector store
```bash
python run_pipeline.py
```

### 6. Launch the app
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
RAG-Medical-Knowledge-Base/
├── app.py                      # Streamlit chat UI
├── run_pipeline.py             # Ingestion pipeline CLI
├── requirements.txt
├── runtime.txt                 # Python 3.11 for Streamlit Cloud
│
├── src/
│   ├── pdf_processor.py        # PDF extraction & chunking
│   ├── embeddings.py           # sentence-transformers wrapper
│   ├── vector_store.py         # Numpy cosine similarity store
│   └── llm.py                  # Groq LLM client
│
├── config/
│   ├── settings.py             # Env config (local .env + st.secrets)
│   └── prompts.py              # LLM prompt templates
│
└── data/
    └── medical_pdfs/           # Source PDF documents
```

---

## 🔑 Key Features

- **No paid APIs required** — fully functional with free-tier services only
- **Semantic search** — finds relevant chunks by meaning, not just keywords
- **Source citations** — every answer links back to the source document
- **Adjustable retrieval** — tune top-K and model via sidebar
- **Auto-ingestion** — knowledge base builds automatically on first run
- **Persistent store** — embeddings saved to disk, no re-indexing on restart

---

## 📈 What This Demonstrates

- End-to-end RAG pipeline design and implementation
- Document processing and intelligent chunking strategies
- Vector embeddings and cosine similarity search from scratch
- LLM prompt engineering for grounded, citation-aware answers
- Streamlit app development and cloud deployment
- Production patterns: caching, error handling, secrets management

---

## 🧑‍💻 Author

**Riyaz Panjwani** — [GitHub](https://github.com/riyaz-panjwani)
