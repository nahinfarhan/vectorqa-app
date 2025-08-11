from sentence_transformers import SentenceTransformer
import tiktoken
from typing import List
import torch

class EmbeddingModel:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        torch.set_default_device('cpu')
        try:
            # Try offline first
            self.model = SentenceTransformer(model_name, device='cpu', local_files_only=True)
        except:
            # Fallback to online download
            self.model = SentenceTransformer(model_name, device='cpu')
        self.model.eval()
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.max_tokens = 256
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.tokenizer.encode(text))
    
    def truncate_text(self, text: str) -> str:
        """Truncate text to max_tokens"""
        tokens = self.tokenizer.encode(text)
        if len(tokens) <= self.max_tokens:
            return text
        
        truncated_tokens = tokens[:self.max_tokens]
        return self.tokenizer.decode(truncated_tokens)
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        # Truncate texts that exceed token limit
        truncated_texts = [self.truncate_text(text) for text in texts]
        embeddings = self.model.encode(truncated_texts, convert_to_tensor=False)
        return embeddings.tolist()
    
    def embed_query(self, query: str) -> List[float]:
        """Generate embedding for a single query"""
        truncated_query = self.truncate_text(query)
        embedding = self.model.encode([truncated_query], convert_to_tensor=False)
        return embedding[0].tolist()