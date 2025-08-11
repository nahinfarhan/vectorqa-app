import streamlit as st
import os
import sys
from pathlib import Path

# Add app directory to path
sys.path.append(str(Path(__file__).parent))

def main():
    st.set_page_config(
        page_title="Vector QA App",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 Document-Based Question Answering")
    st.markdown("Upload PDF or text documents and ask questions in Bangla or English")
    
    # Initialize components with caching
    @st.cache_resource
    def load_components():
        from ingest import DocumentIngestor
        from embed import EmbeddingModel
        from vector_store import VectorStore
        from search import SearchEngine
        
        vector_store = VectorStore()
        embedding_model = EmbeddingModel()
        document_ingestor = DocumentIngestor()
        search_engine = SearchEngine(vector_store, embedding_model)
        return vector_store, embedding_model, document_ingestor, search_engine
    
    try:
        vector_store, embedding_model, document_ingestor, search_engine = load_components()
        st.success("✅ All components loaded successfully!")
        
    except Exception as e:
        st.error(f"❌ Error loading components: {str(e)}")
        st.info("Please ensure all dependencies are installed: pip install chromadb sentence-transformers pdfplumber tiktoken scikit-learn")
        st.stop()
    
    # Sidebar for document upload
    with st.sidebar:
        st.header("📄 Document Upload")
        
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'txt'],
            help="Upload PDF or plain text files (Bangla/English supported)"
        )
        
        if uploaded_file is not None:
            if st.button("Process Document"):
                with st.spinner("Processing document..."):
                    try:
                        # Save uploaded file
                        filepath = document_ingestor.save_uploaded_file(uploaded_file)
                        
                        # Check if document already exists
                        if vector_store.document_exists(uploaded_file.name):
                            st.warning("Document already processed. Skipping duplicate.")
                        else:
                            # Process document
                            chunks, metadatas, file_hash = document_ingestor.process_document(filepath)
                            
                            # Generate embeddings
                            embeddings = embedding_model.embed_texts(chunks)
                            
                            # Create IDs for chunks
                            ids = [f"{uploaded_file.name}_{i}" for i in range(len(chunks))]
                            
                            # Store in vector database
                            vector_store.add_chunks(chunks, embeddings, metadatas, ids)
                            
                            st.success(f"✅ Processed {len(chunks)} chunks from {uploaded_file.name}")
                            
                    except Exception as e:
                        st.error(f"Error processing document: {str(e)}")
        
        # Display collection stats
        st.markdown("---")
        st.subheader("📊 Collection Stats")
        try:
            total_chunks = vector_store.get_collection_count()
            st.metric("Total Chunks", total_chunks)
        except:
            st.metric("Total Chunks", "N/A")
        
        # Clear all documents button
        if st.button("🗑️ Clear All Documents", type="secondary"):
            if st.session_state.get('confirm_clear', False):
                try:
                    vector_store.clear_all_documents()
                    st.success("✅ All documents cleared successfully!")
                    st.session_state.confirm_clear = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Error clearing documents: {str(e)}")
            else:
                st.session_state.confirm_clear = True
                st.warning("⚠️ Click again to confirm clearing all documents")
        
        # View all chunks button
        if st.button("📋 View All Chunks"):
            try:
                all_chunks = vector_store.get_all_chunks()
                if all_chunks and all_chunks.get('documents'):
                    st.session_state.show_chunks = True
                    st.rerun()
                else:
                    st.info("No chunks found")
            except Exception as e:
                st.error(f"Error retrieving chunks: {str(e)}")
    
    # Main area for questions
    st.header("❓ Ask Questions")
    
    query = st.text_input(
        "Enter your question (Bangla or English):",
        placeholder="আপনার প্রশ্ন লিখুন বা Enter your question here...",
        help="Ask questions about your uploaded documents"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        search_button = st.button("🔍 Search", type="primary")
    with col2:
        top_k = st.slider("Number of results", 1, 20, 5)
    
    if search_button and query:
        with st.spinner("Searching..."):
            try:
                results = search_engine.search_documents(query, top_k=top_k)
                
                if results and "error" in results[0]:
                    st.warning(results[0]["error"])
                else:
                    st.success(f"Found {len(results)} relevant chunks")
                    
                    # Display results
                    for i, result in enumerate(results, 1):
                        with st.expander(
                            f"📄 Result {i} - {result['similarity_percentage']}% match "
                            f"({result['metadata']['filename']})",
                            expanded=i <= 3
                        ):
                            # Similarity score with color coding
                            score = result['similarity_percentage']
                            if score >= 80:
                                score_color = "🟢"
                            elif score >= 60:
                                score_color = "🟡"
                            else:
                                score_color = "🟠"
                            
                            st.markdown(f"**{score_color} Similarity Score:** {score}%")
                            
                            # Metadata
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.markdown(f"**📁 Document:** {result['metadata']['filename']}")
                            with col2:
                                st.markdown(f"**🔢 Chunk ID:** {result['metadata']['chunk_id']}")
                            with col3:
                                st.markdown(f"**📝 Words:** {result['metadata']['word_count']}")
                            
                            # Text content
                            st.markdown("**📖 Content:**")
                            st.markdown(f"```\n{result['text']}\n```")
                            
                            st.markdown("---")
            except Exception as e:
                st.error(f"Search error: {str(e)}")
    
    # Display all chunks if requested
    if st.session_state.get('show_chunks', False):
        st.header("📋 All Document Chunks")
        try:
            all_chunks = vector_store.get_all_chunks()
            if all_chunks and all_chunks.get('documents') and len(all_chunks['documents']) > 0:
                st.write(f"Total chunks: {len(all_chunks['documents'])}")
                for i, (doc, metadata, chunk_id) in enumerate(zip(all_chunks['documents'], all_chunks['metadatas'], all_chunks['ids'])):
                    with st.expander(f"Chunk {i+1}: {metadata.get('filename', 'Unknown')} (ID: {chunk_id})", expanded=False):
                        st.write(f"**Words:** {metadata.get('word_count', 'N/A')}")
                        st.text_area("Content:", doc, height=150, disabled=True, key=f"chunk_{i}")
                if st.button("Hide Chunks"):
                    st.session_state.show_chunks = False
                    st.rerun()
            else:
                st.info("No chunks found in the database")
                if st.button("Hide Chunks"):
                    st.session_state.show_chunks = False
                    st.rerun()
        except Exception as e:
            st.error(f"Error displaying chunks: {str(e)}")
            if st.button("Hide Chunks"):
                st.session_state.show_chunks = False
                st.rerun()
    
    # Instructions
    with st.expander("ℹ️ How to use this app"):
        st.markdown("""
        ### 📋 Instructions:
        1. **Upload Documents**: Use the sidebar to upload PDF or text files
        2. **Ask Questions**: Type your question in Bangla or English
        3. **View Results**: See matching chunks with similarity scores
        
        ### 🔍 Features:
        - **Bangla & English Support**: Full Unicode support for both languages
        - **Smart Chunking**: Documents split into ~500-word overlapping sections
        - **Similarity Scoring**: Results ranked by cosine similarity
        - **Duplicate Detection**: Skips already processed documents
        - **Edge Case Handling**: Handles scanned PDFs, short chunks, etc.
        
        ### 📊 Similarity Scores:
        - **🟢 80%+**: Highly relevant
        - **🟡 60-79%**: Moderately relevant  
        - **🟠 50-59%**: Somewhat relevant
        - **Below 50%**: Filtered out
        """)

if __name__ == "__main__":
    main()