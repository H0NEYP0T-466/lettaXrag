import os
import json
import pickle
from typing import List, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from config import settings
from utils.logger import log_info, log_success, log_error
import hashlib
from pathlib import Path
from PyPDF2 import PdfReader
from docx import Document


class RAGService:
    """FAISS-based RAG service for document retrieval"""
    
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.documents = []
        self.metadata = []
        self.embedding_dim = 384  # Dimension for all-MiniLM-L6-v2
        
    def _get_file_hash(self, filepath: str) -> str:
        """Calculate hash of file for change detection"""
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            hasher.update(f.read())
        return hasher.hexdigest()
    
    def _load_text_file(self, filepath: str) -> str:
        """Load text from .txt or .md file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _load_pdf_file(self, filepath: str) -> str:
        """Load text from PDF file"""
        try:
            reader = PdfReader(filepath)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            log_error(f"Error loading PDF {filepath}: {str(e)}")
            return ""
    
    def _load_docx_file(self, filepath: str) -> str:
        """Load text from DOCX file"""
        try:
            doc = Document(filepath)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text
        except Exception as e:
            log_error(f"Error loading DOCX {filepath}: {str(e)}")
            return ""
    
    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
        return chunks
    
    def _load_documents_from_folder(self) -> Tuple[List[str], List[dict]]:
        """Load all supported documents from data folder"""
        documents = []
        metadata = []
        
        data_path = Path(settings.data_folder)
        if not data_path.exists():
            data_path.mkdir(parents=True)
            log_info(f"Created data folder: {settings.data_folder}")
            return documents, metadata
        
        supported_extensions = ['.txt', '.md', '.pdf', '.docx']
        
        for filepath in data_path.rglob('*'):
            if filepath.is_file() and filepath.suffix in supported_extensions:
                log_info(f"Loading file: {filepath}")
                
                text = ""
                if filepath.suffix in ['.txt', '.md']:
                    text = self._load_text_file(str(filepath))
                elif filepath.suffix == '.pdf':
                    text = self._load_pdf_file(str(filepath))
                elif filepath.suffix == '.docx':
                    text = self._load_docx_file(str(filepath))
                
                if text:
                    chunks = self._chunk_text(text)
                    for i, chunk in enumerate(chunks):
                        documents.append(chunk)
                        metadata.append({
                            'source': str(filepath.name),
                            'chunk_id': i,
                            'file_hash': self._get_file_hash(str(filepath))
                        })
        
        return documents, metadata
    
    def _should_rebuild_index(self) -> bool:
        """Check if index needs to be rebuilt"""
        # Check if index files exist
        if not os.path.exists(settings.faiss_index_path):
            return True
        if not os.path.exists(settings.metadata_path):
            return True
        
        # Load saved metadata
        with open(settings.metadata_path, 'r') as f:
            saved_metadata = json.load(f)
        
        # Get current files
        _, current_metadata = self._load_documents_from_folder()
        
        # Compare file hashes
        saved_hashes = set(m['file_hash'] for m in saved_metadata)
        current_hashes = set(m['file_hash'] for m in current_metadata)
        
        return saved_hashes != current_hashes
    
    def initialize_index(self, force_rebuild: bool = False):
        """Initialize or load FAISS index"""
        try:
            # Create storage directory if it doesn't exist
            storage_path = Path(settings.faiss_index_path).parent
            if not storage_path.exists():
                storage_path.mkdir(parents=True)
            
            # Check if rebuild is needed
            if force_rebuild or self._should_rebuild_index():
                log_info("🔄 Generating embeddings...")
                
                # Load documents
                self.documents, self.metadata = self._load_documents_from_folder()
                
                if not self.documents:
                    log_info("No documents found. Creating empty index.")
                    self.index = faiss.IndexFlatL2(self.embedding_dim)
                    self._save_index()
                    return
                
                # Generate embeddings
                log_info(f"Encoding {len(self.documents)} document chunks...")
                embeddings = self.model.encode(self.documents, show_progress_bar=True)
                embeddings = np.array(embeddings).astype('float32')
                
                # Create FAISS index
                self.index = faiss.IndexFlatL2(self.embedding_dim)
                self.index.add(embeddings)
                
                # Save index and metadata
                self._save_index()
                log_success(f"✅ Embeddings ready! Indexed {len(self.documents)} chunks from {len(set(m['source'] for m in self.metadata))} files")
            else:
                log_info("✅ Loading existing embeddings...")
                self._load_index()
                log_success(f"✅ Loaded index with {len(self.documents)} chunks from {len(set(m['source'] for m in self.metadata))} files")
                
        except Exception as e:
            log_error(f"Error initializing index: {str(e)}")
            # Create empty index as fallback
            self.index = faiss.IndexFlatL2(self.embedding_dim)
            self.documents = []
            self.metadata = []
    
    def _save_index(self):
        """Save FAISS index and metadata to disk"""
        # Save FAISS index
        faiss.write_index(self.index, settings.faiss_index_path)
        
        # Save metadata
        with open(settings.metadata_path, 'w') as f:
            json.dump(self.metadata, f)
        
        # Save documents
        docs_path = settings.metadata_path.replace('.json', '_docs.pkl')
        with open(docs_path, 'wb') as f:
            pickle.dump(self.documents, f)
    
    def _load_index(self):
        """Load FAISS index and metadata from disk"""
        # Load FAISS index
        self.index = faiss.read_index(settings.faiss_index_path)
        
        # Load metadata
        with open(settings.metadata_path, 'r') as f:
            self.metadata = json.load(f)
        
        # Load documents
        docs_path = settings.metadata_path.replace('.json', '_docs.pkl')
        with open(docs_path, 'rb') as f:
            self.documents = pickle.load(f)
    
    def retrieve_context(self, query: str, k: int = 3) -> List[str]:
        """Retrieve top-k relevant document chunks for query"""
        try:
            if not self.documents or self.index.ntotal == 0:
                log_info("No documents in index for retrieval")
                return []
            
            # Encode query
            query_embedding = self.model.encode([query])
            query_embedding = np.array(query_embedding).astype('float32')
            
            # Search
            k = min(k, len(self.documents))  # Don't search for more than we have
            distances, indices = self.index.search(query_embedding, k)
            
            # Get relevant documents
            results = []
            for idx in indices[0]:
                if idx < len(self.documents):
                    results.append(self.documents[idx])
            
            return results
        except Exception as e:
            log_error(f"Error retrieving context: {str(e)}")
            return []
    
    def get_stats(self) -> dict:
        """Get RAG statistics"""
        return {
            'indexed_documents': len(set(m['source'] for m in self.metadata)) if self.metadata else 0,
            'total_chunks': len(self.documents),
            'index_size': self.index.ntotal if self.index else 0
        }


# Global RAG service instance
rag_service = RAGService()
