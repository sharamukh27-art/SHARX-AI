"""ChromaDB vector database integration for semantic memory"""

import chromadb
import logging
import uuid
from typing import List, Dict, Any
from app.config import settings

logger = logging.getLogger(__name__)


class ChromaDBMemory:
    """Semantic memory using ChromaDB vector database"""
    
    def __init__(self):
        """Initialize ChromaDB client"""
        self.client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        self.collection = self.client.get_or_create_collection(
            name="sharx_ai_memory",
            metadata={"hnsw:space": "cosine"}
        )
        logger.info(f"ChromaDB initialized with collection: sharx_ai_memory")
    
    def add(self, documents: List[str], metadatas: List[Dict[str, Any]] = None, ids: List[str] = None):
        """
        Add documents to semantic memory.
        
        Args:
            documents: List of document texts
            metadatas: Optional metadata for each document
            ids: Optional custom IDs for documents
        """
        try:
            if ids is None:
                ids = [str(uuid.uuid4()) for _ in documents]
            self.collection.add(
                documents=documents,
                metadatas=metadatas or [{} for _ in documents],
                ids=ids
            )
            logger.info(f"Added {len(documents)} documents to memory")
        except Exception as e:
            logger.error(f"Error adding documents to memory: {e}")
            raise
    
    def query(self, query_text: str, n_results: int = 5) -> Dict[str, Any]:
        """
        Query semantic memory.
        
        Args:
            query_text: Text to search for
            n_results: Number of results to return
        
        Returns:
            Query results with documents, distances, and metadatas
        """
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            return results
        except Exception as e:
            logger.error(f"Error querying memory: {e}")
            raise
    
    def update(self, ids: List[str], documents: List[str], metadatas: List[Dict[str, Any]] = None):
        """
        Update documents in memory.
        
        Args:
            ids: Document IDs to update
            documents: New document texts
            metadatas: New metadata
        """
        try:
            self.collection.update(
                ids=ids,
                documents=documents,
                metadatas=metadatas or [{} for _ in documents]
            )
            logger.info(f"Updated {len(ids)} documents in memory")
        except Exception as e:
            logger.error(f"Error updating memory: {e}")
            raise
    
    def delete(self, ids: List[str]):
        """
        Delete documents from memory.
        
        Args:
            ids: Document IDs to delete
        """
        try:
            self.collection.delete(ids=ids)
            logger.info(f"Deleted {len(ids)} documents from memory")
        except Exception as e:
            logger.error(f"Error deleting from memory: {e}")
            raise
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get all documents in memory.
        
        Returns:
            All documents with their metadata
        """
        try:
            return self.collection.get()
        except Exception as e:
            logger.error(f"Error retrieving all documents: {e}")
            raise


# Global memory instance
_memory = None


def get_memory() -> ChromaDBMemory:
    """Get or create global memory instance"""
    global _memory
    if _memory is None:
        _memory = ChromaDBMemory()
    return _memory


def init_memory() -> ChromaDBMemory:
    """Initialize global memory instance"""
    return get_memory()
