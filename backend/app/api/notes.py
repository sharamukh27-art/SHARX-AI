"""Notes API endpoints"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime
from typing import List

from app.db import get_db
from app.db.models import Note
from app.utils import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/notes", tags=["notes"])


class NoteCreate(BaseModel):
    """Create note request"""
    title: str
    content: str
    tags: List[str] = []


class NoteUpdate(BaseModel):
    """Update note request"""
    title: str = None
    content: str = None
    tags: List[str] = None


class NoteResponse(BaseModel):
    """Note response"""
    id: str
    title: str
    content: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime


@router.post("/", response_model=NoteResponse)
async def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    """Create a new note"""
    try:
        db_note = Note(
            id=str(uuid4()),
            title=note.title,
            content=note.content,
            tags=note.tags,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(db_note)
        db.commit()
        db.refresh(db_note)
        return db_note
    except Exception as e:
        logger.error(f"Error creating note: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[NoteResponse])
async def get_notes(db: Session = Depends(get_db)):
    """Get all notes"""
    try:
        notes = db.query(Note).all()
        return notes
    except Exception as e:
        logger.error(f"Error fetching notes: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: str, db: Session = Depends(get_db)):
    """Get specific note"""
    try:
        note = db.query(Note).filter_by(id=note_id).first()
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        return note
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching note: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(note_id: str, note_update: NoteUpdate, db: Session = Depends(get_db)):
    """Update a note"""
    try:
        note = db.query(Note).filter_by(id=note_id).first()
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        
        if note_update.title is not None:
            note.title = note_update.title
        if note_update.content is not None:
            note.content = note_update.content
        if note_update.tags is not None:
            note.tags = note_update.tags
        
        note.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(note)
        return note
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating note: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{note_id}")
async def delete_note(note_id: str, db: Session = Depends(get_db)):
    """Delete a note"""
    try:
        note = db.query(Note).filter_by(id=note_id).first()
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        
        db.delete(note)
        db.commit()
        return {"message": "Note deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting note: {e}")
        raise HTTPException(status_code=500, detail=str(e))
