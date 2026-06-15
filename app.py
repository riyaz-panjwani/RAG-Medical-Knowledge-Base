import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Medical Knowledge RAG",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .query-box {
        border: 2px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        background-color: #f9f9f9;
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    st.title("🏥 Medical Knowledge Base RAG")
    st.markdown("AI-powered medical information retrieval system")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        add_vertical_space(1)
        st.subheader("Vector Database")
        vector_db = st.selectbox(
            "Select Vector Database",
            ["Pinecone", "Weaviate"],
            help="Choose your vector database backend"
        )

        add_vertical_space(2)
        st.subheader("LLM Provider")
        llm_provider = st.selectbox(
            "Select LLM Provider",
            ["OpenAI (GPT-4)", "Mistral"],
            help="Choose your language model provider"
        )

        add_vertical_space(2)
        st.subheader("RAG Parameters")
        top_k = st.slider(
            "Top K Results",
            min_value=1,
            max_value=10,
            value=5,
            help="Number of documents to retrieve"
        )

        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Control response randomness"
        )

        add_vertical_space(3)
        st.subheader("📁 Document Management")
        if st.button("🔄 Load Documents", use_container_width=True):
            st.info("Document loading feature coming soon...")

        if st.button("🗑️ Clear Vector Store", use_container_width=True):
            st.warning("Vector store clearing feature coming soon...")

        add_vertical_space(2)
        st.markdown("---")
        st.markdown(
            "Built with LangChain, Streamlit, and modern LLM architecture",
            help="RAG Medical Knowledge Base v1.0"
        )

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("🔍 Query Medical Knowledge")
        user_query = st.text_area(
            "Ask a medical question:",
            placeholder="e.g., What are the symptoms of diabetes?",
            height=100,
            label_visibility="collapsed"
        )

    with col2:
        st.subheader("Status")
        st.info("🟢 System Ready", icon="ℹ️")
        st.metric("Vector DB", vector_db, delta="Connected")
        st.metric("LLM Provider", llm_provider.split()[0], delta="Active")

    if user_query:
        st.markdown("---")

        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["Answer", "Retrieved Documents", "Metadata"])

        with tab1:
            st.subheader("Generated Answer")
            with st.spinner("🤔 Thinking..."):
                st.info(
                    "RAG pipeline not yet implemented. "
                    "This is where the AI-generated answer will appear based on retrieved medical documents.",
                    icon="ⓘ"
                )

        with tab2:
            st.subheader("Retrieved Source Documents")
            st.info(
                "Document retrieval from vector store coming soon. "
                "Up to {} most relevant documents will be shown here.".format(top_k),
                icon="ⓘ"
            )

        with tab3:
            st.subheader("Pipeline Metadata")
            col_meta1, col_meta2, col_meta3 = st.columns(3)
            with col_meta1:
                st.metric("Top K", top_k)
            with col_meta2:
                st.metric("Temperature", temperature)
            with col_meta3:
                st.metric("Query Tokens", len(user_query.split()))

    # Footer
    add_vertical_space(3)
    st.markdown("---")
    st.markdown(
        """
        **How to use:**
        1. Enter your medical question in the query box
        2. System retrieves relevant documents from the medical knowledge base
        3. AI generates an answer with citations from source documents
        4. Adjust parameters in the sidebar for different response styles
        """
    )


if __name__ == "__main__":
    main()
