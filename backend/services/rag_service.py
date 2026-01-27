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
        self.embeddings = None  # ✅ Store embeddings to avoid re-encoding
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
    
    def _load_documents_from_folder(self, include_history: bool = False) -> Tuple[List[str], List[dict]]:
        """Load all supported documents from data folder
        
        Args:
            include_history: If True, include history.txt in loading. Default is False.
        """
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
            # Skip history.txt file unless include_history is True
            if filepath.resolve() == history_file:
                if not include_history:
                    log_info(f"Skipping history file: {filepath}")
                    continue
                else:
                    log_info(f"Including history file in initial load: {filepath}")
                
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
    
    def _check_history_file_changed(self) -> bool:
        """
        Check if history.txt has changed since last indexing
        Returns: True if history file is new or modified, False otherwise
        """
        history_file = Path(settings.history_file_path).resolve()
        
        # If history file doesn't exist, no change
        if not history_file.exists():
            return False
        
        # Load saved file hashes
        saved_hashes = {}
        if os.path.exists(settings.file_hash_path):
            try:
                with open(settings.file_hash_path, 'r') as f:
                    saved_hashes = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                log_error(f"Error loading file hashes: {str(e)}")
                return True  # Treat as changed to trigger re-indexing
        
        # Check if history file is in saved hashes and if hash changed
        history_path_str = str(history_file)
        if history_path_str not in saved_hashes:
            # History file is new
            return True
        
        # Check if hash changed
        try:
            current_hash = self._get_file_hash(history_path_str)
            return current_hash != saved_hashes[history_path_str]
        except Exception as e:
            log_error(f"Error getting history file hash: {str(e)}")
            return True  # Treat as changed to trigger re-indexing
    
    def _get_changed_files(self) -> Tuple[List[str], List[str], List[str]]:
        """
        Identify new, modified, and deleted files (excluding history.txt)
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
        history_path_str = str(history_file)
        
        current_files = {}
        for filepath in data_path.rglob('*'):
            if filepath.resolve() == history_file:
                continue
            if filepath.is_file() and filepath.suffix in supported_extensions:
                file_path = str(filepath)
                current_files[file_path] = self._get_file_hash(file_path)
        
        # Identify changes (excluding history.txt from saved_hashes for deletion check)
        new_files = [f for f in current_files if f not in saved_hashes]
        modified_files = [f for f in current_files if f in saved_hashes and current_files[f] != saved_hashes[f]]
        deleted_files = [f for f in saved_hashes if f not in current_files and f != history_path_str]
        
        return new_files, modified_files, deleted_files
    
    def _save_file_hashes(self):
        """Save current file hashes to disk (including history.txt)"""
        data_path = Path(settings.data_folder)
        supported_extensions = ['.txt', '.md', '.pdf', '.docx']
        history_file = Path(settings.history_file_path).resolve()
        history_path_str = str(history_file)
        
        file_hashes = {}
        for filepath in data_path.rglob('*'):
            if filepath.resolve() == history_file:
                continue
            if filepath.is_file() and filepath.suffix in supported_extensions:
                file_path = str(filepath)
                file_hashes[file_path] = self._get_file_hash(file_path)
        
        # Also save history.txt hash if it exists
        if history_file.exists():
            file_hashes[history_path_str] = self._get_file_hash(history_path_str)
        
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
    
    def initialize_index(self, force_rebuild: bool = False, check_history: bool = True):
        """Initialize or load FAISS index with incremental updates
        
        Args:
            force_rebuild: If True, rebuild the entire index from scratch
            check_history: If True, check if history.txt has changed (only at startup)
        """
        try:
            # Create storage directory if it doesn't exist
            storage_path = Path(settings.faiss_index_path).parent
            if not storage_path.exists():
                storage_path.mkdir(parents=True)
            
            # Check for file changes (excluding history.txt)
            new_files, modified_files, deleted_files = self._get_changed_files()
            files_to_embed = new_files + modified_files
            
            # Check if history.txt changed (only on startup, not during file watching)
            history_changed = False
            if check_history:
                history_changed = self._check_history_file_changed()
                if history_changed:
                    log_info("📝 History.txt has been updated since last startup")
            
            has_changes = len(files_to_embed) > 0 or len(deleted_files) > 0 or history_changed
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
            
            # Handle history.txt if it changed
            if history_changed:
                history_file = Path(settings.history_file_path).resolve()
                history_path_str = str(history_file)
                
                # Check if history.txt chunks exist in the index
                has_history_chunks = any(meta.get('file_path') == history_path_str for meta in self.metadata)
                
                if has_history_chunks:
                    log_info("📝 Updating history.txt in index...")
                    self._remove_files_from_index({history_path_str})
                else:
                    log_info("📝 Adding history.txt to index for the first time...")
                
                # Add updated history.txt
                if history_file.exists():
                    self._add_files_to_index([history_path_str])
            
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
            self.embeddings = np.array([]).astype('float32').reshape(0, self.embedding_dim)
    
    def _build_full_index(self):
        """Build complete index from all documents"""
        # Load documents (including history.txt on initial startup)
        self.documents, self.metadata = self._load_documents_from_folder(include_history=True)
        
        if not self.documents:
            log_info("No documents found. Creating empty index.")
            self.index = faiss.IndexFlatL2(self.embedding_dim)
            self.embeddings = np.array([]).astype('float32').reshape(0, self.embedding_dim)
            self._save_index()
            self._save_file_hashes()
            return
        
        # Generate embeddings
        log_info(f"Encoding {len(self.documents)} document chunks...")
        self.embeddings = self.model.encode(self.documents, show_progress_bar=True)
        self.embeddings = np.array(self.embeddings).astype('float32')
        
        # Create FAISS index
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.index.add(self.embeddings)
        
        # Save index and metadata
        self._save_index()
        self._save_file_hashes()
        log_success(f"✅ Embeddings ready! Indexed {len(self.documents)} chunks from {len(set(m['source'] for m in self.metadata))} files")
    
    def _remove_files_from_index(self, file_paths: set):
        """Remove chunks from specified files WITHOUT re-encoding everything"""
        # Find indices to remove and keep
        indices_to_remove = []
        indices_to_keep = []
        
        for i, meta in enumerate(self.metadata):
            meta_file_path = meta.get('file_path') or meta.get('source') or ''
            if meta_file_path in file_paths:
                indices_to_remove.append(i)
            else:
                indices_to_keep.append(i)
        
        if not indices_to_remove:
            log_info("No chunks to remove")
            return
        
        log_info(f"🗑️  Removing {len(indices_to_remove)} chunks from index (keeping {len(indices_to_keep)} chunks)...")
        
        if not indices_to_keep:
            # All documents removed
            self.index = faiss.IndexFlatL2(self.embedding_dim)
            self.documents = []
            self.metadata = []
            self.embeddings = np.array([]).astype('float32').reshape(0, self.embedding_dim)
            log_info("All documents removed from index")
            return
        
        # ✅ Keep embeddings without re-encoding
        self.embeddings = self.embeddings[indices_to_keep]
        self.documents = [self.documents[i] for i in indices_to_keep]
        self.metadata = [self.metadata[i] for i in indices_to_keep]
        
        # Rebuild FAISS index with kept embeddings (no encoding needed!)
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.index.add(self.embeddings)
        
        log_success(f"✅ Removed {len(indices_to_remove)} chunks without re-encoding")
    
    def _add_files_to_index(self, file_paths: List[str]):
        """Add chunks from specified files to index"""
        log_info(f"Processing {len(file_paths)} files...")
        
        new_documents = []
        new_metadata = []
        
        for filepath in file_paths:
            path = Path(filepath)
            log_info(f"📄 Loading file: {path.name}")
            
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
        
        # Generate embeddings for new documents only
        log_info(f"🔢 Encoding {len(new_documents)} new chunks...")
        new_embeddings = self.model.encode(new_documents, show_progress_bar=True)
        new_embeddings = np.array(new_embeddings).astype('float32')
        
        # Add to index
        self.index.add(new_embeddings)
        
        # ✅ Append embeddings to stored embeddings
        if self.embeddings is None or self.embeddings.shape[0] == 0:
            self.embeddings = new_embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, new_embeddings])
        
        self.documents.extend(new_documents)
        self.metadata.extend(new_metadata)
        
        log_success(f"✅ Added {len(new_documents)} new chunks")
    
    def _save_index(self):
        """Save FAISS index, embeddings, and metadata to disk"""
        # Save FAISS index
        faiss.write_index(self.index, settings.faiss_index_path)
        
        # Save metadata
        with open(settings.metadata_path, 'w') as f:
            json.dump(self.metadata, f)
        
        # Save documents
        docs_path = settings.metadata_path.replace('.json', '_docs.pkl')
        with open(docs_path, 'wb') as f:
            pickle.dump(self.documents, f)
        
        # ✅ Save embeddings separately
        embeddings_path = settings.metadata_path.replace('.json', '_embeddings.npy')
        np.save(embeddings_path, self.embeddings)
    
    def _load_index(self):
        """Load FAISS index, embeddings, and metadata from disk"""
        # Load FAISS index
        self.index = faiss.read_index(settings.faiss_index_path)
        
        # Load metadata
        with open(settings.metadata_path, 'r') as f:
            self.metadata = json.load(f)
        
        # Load documents
        docs_path = settings.metadata_path.replace('.json', '_docs.pkl')
        with open(docs_path, 'rb') as f:
            self.documents = pickle.load(f)
        
        # ✅ Load embeddings
        embeddings_path = settings.metadata_path.replace('.json', '_embeddings.npy')
        if os.path.exists(embeddings_path):
            self.embeddings = np.load(embeddings_path)
        else:
            # Fallback: embeddings file doesn't exist (old version)
            log_info("⚠️  Embeddings file not found. This is expected on first run with new code.")
            self.embeddings = np.array([]).astype('float32').reshape(0, self.embedding_dim)
    
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
    
rag_service = RAGService()