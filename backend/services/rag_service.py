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
        history_file = Path(settings.history_file_path).resolve()
        
        for filepath in data_path.rglob('*'):
            # Skip history.txt file
            if filepath.resolve() == history_file:
                log_info(f"Skipping history file: {filepath}")
                continue
                
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
                            'file_hash': self._get_file_hash(str(filepath)),
                            'file_path': str(filepath)
                        })
        
        return documents, metadata
    
    def _get_changed_files(self) -> Tuple[List[str], List[str], List[str]]:
        """
        Identify new, modified, and deleted files
        Returns: (new_files, modified_files, deleted_files)
        """
        # Load saved file hashes
        saved_hashes = {}
        if os.path.exists(settings.file_hash_path):
            with open(settings.file_hash_path, 'r') as f:
                saved_hashes = json.load(f)
        
        # Get current files
        data_path = Path(settings.data_folder)
        supported_extensions = ['.txt', '.md', '.pdf', '.docx']
        history_file = Path(settings.history_file_path).resolve()
        
        current_files = {}
        for filepath in data_path.rglob('*'):
            if filepath.resolve() == history_file:
                continue
            if filepath.is_file() and filepath.suffix in supported_extensions:
                file_path = str(filepath)
                current_files[file_path] = self._get_file_hash(file_path)
        
        # Identify changes
        new_files = [f for f in current_files if f not in saved_hashes]
        modified_files = [f for f in current_files if f in saved_hashes and current_files[f] != saved_hashes[f]]
        deleted_files = [f for f in saved_hashes if f not in current_files]
        
        return new_files, modified_files, deleted_files
    
    def _save_file_hashes(self):
        """Save current file hashes to disk"""
        data_path = Path(settings.data_folder)
        supported_extensions = ['.txt', '.md', '.pdf', '.docx']
        history_file = Path(settings.history_file_path).resolve()
        
        file_hashes = {}
        for filepath in data_path.rglob('*'):
            if filepath.resolve() == history_file:
                continue
            if filepath.is_file() and filepath.suffix in supported_extensions:
                file_path = str(filepath)
                file_hashes[file_path] = self._get_file_hash(file_path)
        
        # Create storage directory if needed
        storage_path = Path(settings.file_hash_path).parent
        if not storage_path.exists():
            storage_path.mkdir(parents=True)
        
        with open(settings.file_hash_path, 'w') as f:
            json.dump(file_hashes, f, indent=2)
    
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
        """Initialize or load FAISS index with incremental updates"""
        try:
            # Create storage directory if it doesn't exist
            storage_path = Path(settings.faiss_index_path).parent
            if not storage_path.exists():
                storage_path.mkdir(parents=True)
            
            # Check for file changes
            new_files, modified_files, deleted_files = self._get_changed_files()
            files_to_embed = new_files + modified_files
            
            has_changes = len(files_to_embed) > 0 or len(deleted_files) > 0
            index_exists = os.path.exists(settings.faiss_index_path) and os.path.exists(settings.metadata_path)
            
            # If force rebuild or no existing index, rebuild from scratch
            if force_rebuild or not index_exists:
                log_info("🔄 Building embeddings from scratch...")
                self._build_full_index()
                return
            
            # If no changes, load existing index
            if not has_changes:
                log_info("✅ No file changes detected. Loading existing embeddings...")
                self._load_index()
                log_success(f"✅ Loaded index with {len(self.documents)} chunks from {len(set(m['source'] for m in self.metadata))} files")
                return
            
            # Incremental update
            log_info(f"🔄 Incremental update: {len(new_files)} new, {len(modified_files)} modified, {len(deleted_files)} deleted files")
            
            # Load existing index
            self._load_index()
            
            # Remove chunks from deleted/modified files
            files_to_remove = set(deleted_files + modified_files)
            if files_to_remove:
                self._remove_files_from_index(files_to_remove)
            
            # Add new/modified files
            if files_to_embed:
                self._add_files_to_index(files_to_embed)
            
            # Save updated index
            self._save_index()
            self._save_file_hashes()
            
            log_success(f"✅ Index updated! Now contains {len(self.documents)} chunks from {len(set(m['source'] for m in self.metadata))} files")
                
        except Exception as e:
            log_error(f"Error initializing index: {str(e)}")
            # Create empty index as fallback
            self.index = faiss.IndexFlatL2(self.embedding_dim)
            self.documents = []
            self.metadata = []
    
    def _build_full_index(self):
        """Build complete index from all documents"""
        # Load documents
        self.documents, self.metadata = self._load_documents_from_folder()
        
        if not self.documents:
            log_info("No documents found. Creating empty index.")
            self.index = faiss.IndexFlatL2(self.embedding_dim)
            self._save_index()
            self._save_file_hashes()
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
        self._save_file_hashes()
        log_success(f"✅ Embeddings ready! Indexed {len(self.documents)} chunks from {len(set(m['source'] for m in self.metadata))} files")
    
    def _remove_files_from_index(self, file_paths: set):
        """Remove chunks from specified files"""
        # Find indices to keep
        new_documents = []
        new_metadata = []
        new_embeddings = []
        
        for i, meta in enumerate(self.metadata):
            if meta.get('file_path') not in file_paths:
                new_documents.append(self.documents[i])
                new_metadata.append(meta)
                # We'll need to re-encode kept documents
        
        if not new_documents:
            # All documents removed
            self.index = faiss.IndexFlatL2(self.embedding_dim)
            self.documents = []
            self.metadata = []
            log_info("All documents removed from index")
            return
        
        # Re-encode the kept documents
        log_info(f"Re-encoding {len(new_documents)} kept chunks after removing {len(self.documents) - len(new_documents)} chunks...")
        embeddings = self.model.encode(new_documents, show_progress_bar=False)
        embeddings = np.array(embeddings).astype('float32')
        
        # Create new index with kept embeddings
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.index.add(embeddings)
        
        self.documents = new_documents
        self.metadata = new_metadata
    
    def _add_files_to_index(self, file_paths: List[str]):
        """Add chunks from specified files to index"""
        log_info(f"Processing {len(file_paths)} files...")
        
        new_documents = []
        new_metadata = []
        
        for filepath in file_paths:
            path = Path(filepath)
            log_info(f"Loading file: {path}")
            
            text = ""
            if path.suffix in ['.txt', '.md']:
                text = self._load_text_file(str(path))
            elif path.suffix == '.pdf':
                text = self._load_pdf_file(str(path))
            elif path.suffix == '.docx':
                text = self._load_docx_file(str(path))
            
            if text:
                chunks = self._chunk_text(text)
                for i, chunk in enumerate(chunks):
                    new_documents.append(chunk)
                    new_metadata.append({
                        'source': str(path.name),
                        'chunk_id': i,
                        'file_hash': self._get_file_hash(str(path)),
                        'file_path': str(path)
                    })
        
        if not new_documents:
            log_info("No new content to add")
            return
        
        # Generate embeddings for new documents
        log_info(f"Encoding {len(new_documents)} new chunks...")
        new_embeddings = self.model.encode(new_documents, show_progress_bar=True)
        new_embeddings = np.array(new_embeddings).astype('float32')
        
        # Add to index
        self.index.add(new_embeddings)
        self.documents.extend(new_documents)
        self.metadata.extend(new_metadata)
        
        log_success(f"✅ Added {len(new_documents)} new chunks")
    
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
