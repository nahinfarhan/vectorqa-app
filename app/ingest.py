import pdfplumber
import hashlib
import os
import shutil
from typing import List, Tuple, Dict, Any

class DocumentIngestor:
    def __init__(self, upload_dir: str = "data/uploaded_docs"):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)
        self.chunk_size = 300
        self.overlap = 50
        self.min_chunk_words = 20
    
    def save_uploaded_file(self, uploaded_file) -> str:
        """Save uploaded file and return filepath"""
        filepath = os.path.join(self.upload_dir, uploaded_file.name)
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return filepath
    
    def get_file_hash(self, filepath: str) -> str:
        """Generate hash for file content"""
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def extract_text_from_pdf(self, filepath: str) -> Tuple[str, bool]:
        """Extract text from PDF, return (text, is_scanned)"""
        text = ""
        is_scanned = False
        
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    else:
                        # Check if page has images (potential scanned content)
                        if page.images:
                            is_scanned = True
            
            if not text.strip():
                is_scanned = True
                
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            is_scanned = True
        
        return text.strip(), is_scanned
    
    def extract_text_from_txt(self, filepath: str) -> str:
        """Extract text from plain text file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try different encodings
            for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
                try:
                    with open(filepath, 'r', encoding=encoding) as f:
                        return f.read()
                except UnicodeDecodeError:
                    continue
        return ""
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        lines = [line.strip() for line in text.split('\n')]
        lines = [line for line in lines if line]
        return '\n'.join(lines)
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk_words = words[i:i + self.chunk_size]
            if len(chunk_words) >= self.min_chunk_words:
                chunks.append(' '.join(chunk_words))
        
        return chunks
    
    def process_document(self, filepath: str) -> Tuple[List[str], List[Dict[str, Any]], str]:
        """Process document and return chunks with metadata"""
        filename = os.path.basename(filepath)
        file_hash = self.get_file_hash(filepath)
        
        # Extract text based on file type
        if filepath.lower().endswith('.pdf'):
            text, is_scanned = self.extract_text_from_pdf(filepath)
            if is_scanned and not text.strip():
                raise ValueError("Scanned image detected; OCR not supported yet")
        elif filepath.lower().endswith('.txt'):
            text = self.extract_text_from_txt(filepath)
        else:
            raise ValueError("Unsupported file format")
        
        if not text.strip():
            raise ValueError("No text could be extracted from the document")
        
        # Clean and chunk text
        cleaned_text = self.clean_text(text)
        chunks = self.chunk_text(cleaned_text)
        
        if not chunks:
            raise ValueError("Document too short to create meaningful chunks")
        
        # Create metadata for each chunk
        metadatas = []
        for i, chunk in enumerate(chunks):
            metadatas.append({
                "filename": filename,
                "chunk_id": i + 1,
                "file_hash": file_hash,
                "word_count": len(chunk.split())
            })
        
        return chunks, metadatas, file_hash