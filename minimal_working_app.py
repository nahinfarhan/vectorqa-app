import streamlit as st
import os
import sys
from pathlib import Path

# Add app directory to path
sys.path.append(str(Path(__file__).parent / "app"))

def main():
    st.set_page_config(
        page_title="Vector QA App",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 Document-Based Question Answering")
    st.markdown("Upload PDF or text documents and ask questions in Bangla or English")
    
    # Try to load components with better error handling
    try:
        st.info("🔄 Loading components...")
        
        # Import components one by one to identify issues
        from vector_store import VectorStore
        st.success("✅ VectorStore loaded")
        
        from embed import EmbeddingModel
        st.success("✅ EmbeddingModel loaded")
        
        from ingest import DocumentIngestor
        st.success("✅ DocumentIngestor loaded")
        
        from search import SearchEngine
        st.success("✅ SearchEngine loaded")
        
        # Initialize components
        vector_store = VectorStore()
        embedding_model = EmbeddingModel()
        document_ingestor = DocumentIngestor()
        search_engine = SearchEngine(vector_store, embedding_model)
        
        st.success("🎉 All components initialized successfully!")
        
        # Simple UI
        with st.sidebar:
            st.header("📄 Document Upload")
            uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'txt'])
            if uploaded_file:
                st.success(f"File uploaded: {uploaded_file.name}")
        
        st.header("❓ Ask Questions")
        query = st.text_input("Enter your question:")
        if st.button("🔍 Search") and query:
            st.info("Search functionality working!")
            
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("Components failed to load. This might be due to dependency conflicts.")
        
        # Show basic UI anyway
        st.header("📄 Basic Upload Interface")
        uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'txt'])
        if uploaded_file:
            st.success(f"File uploaded: {uploaded_file.name}")
        
        query = st.text_input("Enter your question:")
        if st.button("🔍 Search") and query:
            st.warning("Components not loaded, but UI is working!")

if __name__ == "__main__":
    main()