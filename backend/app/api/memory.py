"""Memory API endpoints"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from uuid import uuid4
from datetime import datetime

from app.memory import get_memory
from app.utils import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/memory", tags=["memory"])


class MemoryDocument(BaseModel):
    """Memory document"""
    content: str
    category: str = "general"


class MemoryQuery(BaseModel):
    """Memory query"""
    query: str
    n_results: int = 5


@router.post("/add")
async def add_to_memory(doc: MemoryDocument):
    """Add a document to semantic memory"""
    try:
        memory = get_memory()
        doc_id = str(uuid4())
        memory.add(
            documents=[doc.content],
            metadatas=[{"category": doc.category, "created_at": datetime.utcnow().isoformat()}],
            ids=[doc_id]
        )
        return {
            "id": doc_id,
            "message": "Document added to memory"
        }
    except Exception as e:
        logger.error(f"Error adding to memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query")
async def query_memory(query: MemoryQuery):
    """Query semantic memory"""
    try:
        memory = get_memory()
        results = memory.query(query.query, n_results=query.n_results)
        return results
    except Exception as e:
        logger.error(f"Error querying memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all")
async def get_all_memory():
    """Get all documents in memory"""
    try:
        memory = get_memory()
        documents = memory.get_all()
        return documents
    except Exception as e:
        logger.error(f"Error retrieving memory: {e}")
        raise HTTPException(status_code=500, detail=str(e))
