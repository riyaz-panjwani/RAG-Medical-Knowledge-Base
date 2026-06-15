import sys
import os
import warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

st.set_page_config(
    page_title="Medical Knowledge Base",
    page_icon="🏥",
    layout="wide",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Chat bubbles */
.user-bubble {
    background: #1a73e8;
    color: white;
    padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0 8px 20%;
    font-size: 15px;
}
.bot-bubble {
    background: #f1f3f4;
    color: #1a1a1a;
    padding: 12px 16px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px 20% 8px 0;
    font-size: 15px;
    line-height: 1.6;
}
/* Source cards */
.source-card {
    background: #fff;
    border: 1px solid #e0e0e0;
    border-left: 4px solid #1a73e8;
    border-radius: 6px;
    padding: 10px 14px;
    margin: 6px 0;
    font-size: 13px;
}
.score-badge {
    background: #e8f0fe;
    color: #1a73e8;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
}
/* Header */
.header-bar {
    background: linear-gradient(90deg, #1a73e8 0%, #0d47a1 100%);
    color: white;
    padding: 18px 24px;
    border-radius: 10px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)


# ── Cached resource loading ───────────────────────────────────────────────────

@st.cache_resource(show_spinner="Loading embedding model…")
def load_embedder():
    from src.embeddings import EmbeddingsManager
    return EmbeddingsManager()


@st.cache_resource(show_spinner="Connecting to knowledge base…")
def load_store():
    from src.vector_store import VectorStore
    from config.settings import settings
    return VectorStore(persist_dir=settings.CHROMA_PERSIST_PATH)


@st.cache_resource(show_spinner="Connecting to Groq LLM…")
def load_llm(model: str):
    from src.llm import LLMClient
    return LLMClient(model=model)


# ── Session state ─────────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []   # list of {role, content, sources}


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## ⚙️ Settings")

    model_choice = st.selectbox(
        "Groq model",
        ["llama-3.1-8b-instant", "llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
        index=0,
        help="Faster = 8b · Smarter = 70b"
    )

    top_k = st.slider("Documents to retrieve", 1, 8, 3)

    st.markdown("---")
    st.markdown("### 📚 Knowledge Base")

    store_check = load_store()
    n_docs = store_check.count()
    if n_docs > 0:
        st.success(f"✅ {n_docs} chunks indexed")
    else:
        st.error("❌ No documents indexed.\nRun `python run_pipeline.py` first.")

    st.markdown("**Topics covered:**")
    topics = ["Diabetes", "Hypertension", "Heart Disease", "Mental Health", "Respiratory"]
    for t in topics:
        st.markdown(f"• {t}")

    st.markdown("---")
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        "<small>**Stack:** sentence-transformers · ChromaDB · Groq Llama 3</small>",
        unsafe_allow_html=True,
    )


# ── Header ────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="header-bar">
    <h2 style="margin:0">🏥 Medical Knowledge Base</h2>
    <p style="margin:4px 0 0 0; opacity:0.85; font-size:14px">
        RAG-powered Q&A · sentence-transformers · ChromaDB · Groq Llama 3 · 100% free
    </p>
</div>
""", unsafe_allow_html=True)


# ── Chat history ──────────────────────────────────────────────────────────────

chat_area = st.container()

with chat_area:
    if not st.session_state.messages:
        st.markdown("""
        **Ask me anything about:**
        - 🩺 Symptoms of common diseases
        - 💊 Treatment and management options
        - ❤️ Prevention and lifestyle advice
        - 🧠 Mental health conditions
        - 🫁 Respiratory health
        """)
    else:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(
                    f'<div class="user-bubble">🧑 {msg["content"]}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="bot-bubble">🤖 {msg["content"]}</div>',
                    unsafe_allow_html=True,
                )
                # Show sources in expander
                if msg.get("sources"):
                    with st.expander(f"📄 {len(msg['sources'])} source document(s)"):
                        for src in msg["sources"]:
                            st.markdown(
                                f"""<div class="source-card">
                                    <strong>{src['source']}</strong>
                                    <span class="score-badge" style="float:right">
                                        relevance {src['score']:.2f}
                                    </span><br/>
                                    <small>{src['content'][:200]}…</small>
                                </div>""",
                                unsafe_allow_html=True,
                            )


# ── Input ─────────────────────────────────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)
query = st.chat_input("Ask a medical question…")

if query:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": query})

    # Load components
    embedder = load_embedder()
    store    = load_store()

    try:
        llm = load_llm(model_choice)
    except ValueError as e:
        st.error(str(e))
        st.stop()

    # RAG
    with st.spinner("Searching knowledge base…"):
        query_vec = embedder.embed_query(query)
        hits      = store.search(query_vec, top_k=top_k)

    with st.spinner("Generating answer…"):
        answer = llm.generate(query, hits)

    # Add bot message
    st.session_state.messages.append({
        "role":    "assistant",
        "content": answer,
        "sources": hits,
    })

    st.rerun()
