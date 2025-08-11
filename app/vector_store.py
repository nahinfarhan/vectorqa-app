import chromadb
import os
from typing import List, Dict, Any

class VectorStore:
    def __init__(self, persist_directory: str = "data/vectors"):
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_chunks(self, chunks: List[str], embeddings: List[List[float]], 
                   metadatas: List[Dict[str, Any]], ids: List[str]):
        """Add document chunks with embeddings to the vector store"""
        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(self, query_embedding: List[float], n_results: int = 10) -> Dict[str, Any]:
        """Search for similar chunks"""
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results
    
    def document_exists(self, filename: str) -> bool:
        """Check if document already exists in the collection"""
        results = self.collection.get(
            where={"filename": filename}
        )
        return len(results['ids']) > 0
    
    def get_collection_count(self) -> int:
        """Get total number of chunks in collection"""
        return self.collection.count()
    
    def clear_all_documents(self):
        """Clear all documents from the collection"""
        # Delete the collection and recreate it
        self.client.delete_collection(name="documents")
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def get_all_chunks(self):
        """Get all chunks from the collection"""
        results = self.collection.get()
        return results