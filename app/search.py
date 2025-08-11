from typing import List, Dict, Any, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class SearchEngine:
    def __init__(self, vector_store, embedding_model):
        self.vector_store = vector_store
        self.embedding_model = embedding_model
        self.similarity_threshold = 0.1
    
    def validate_query(self, query: str) -> Tuple[bool, str]:
        """Validate query and return (is_valid, message)"""
        words = query.strip().split()
        if len(words) < 3:
            return False, "Query too short. Please provide at least 3 words."
        return True, ""
    
    def calculate_similarity_percentage(self, cosine_distance: float) -> float:
        """Convert cosine distance to similarity percentage"""
        # ChromaDB returns cosine distance (1 - cosine_similarity)
        # Convert to similarity percentage
        similarity = 1 - cosine_distance
        return max(0, similarity * 100)
    
    def search_documents(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Search for relevant document chunks"""
        # Validate query
        is_valid, message = self.validate_query(query)
        if not is_valid:
            return [{"error": message}]
        
        # Generate query embedding
        query_embedding = self.embedding_model.embed_query(query)
        
        # Search vector store
        results = self.vector_store.search(query_embedding, n_results=top_k)
        
        if not results['documents'] or not results['documents'][0]:
            return [{"error": "No relevant section found."}]
        
        # Process results
        search_results = []
        for i in range(len(results['documents'][0])):
            distance = results['distances'][0][i]
            similarity_percentage = self.calculate_similarity_percentage(distance)
            
            # Filter by similarity threshold
            if similarity_percentage >= (self.similarity_threshold * 100):
                result = {
                    "text": results['documents'][0][i],
                    "similarity_percentage": round(similarity_percentage, 2),
                    "metadata": results['metadatas'][0][i],
                    "chunk_id": results['ids'][0][i]
                }
                search_results.append(result)
        
        if not search_results:
            return [{"error": "No relevant section found."}]
        
        # Sort by similarity percentage (descending)
        search_results.sort(key=lambda x: x['similarity_percentage'], reverse=True)
        
        return search_results