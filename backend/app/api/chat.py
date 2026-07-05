"""Chat API endpoints"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime

from app.ai.factory import get_current_provider
from app.memory import get_memory
from app.db import get_db
from app.db.models import Conversation, Message as DBMessage
from app.utils import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chat"])


class MessageRequest(BaseModel):
    """Chat message request"""
    content: str


class MessageResponse(BaseModel):
    """Chat message response"""
    role: str
    content: str


class ChatRequest(BaseModel):
    """Chat request with message history"""
    messages: List[MessageResponse]
    conversation_id: str = None


class ChatResponse(BaseModel):
    """Chat response"""
    conversation_id: str
    message: MessageResponse
    model: str


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    """
    Send a chat message and get a response.
    
    Args:
        request: Chat request with message history
        db: Database session
    
    Returns:
        Chat response with model name
    """
    try:
        # Get or create conversation
        conversation_id = request.conversation_id or str(uuid4())
        
        if request.conversation_id:
            conversation = db.query(Conversation).filter_by(id=conversation_id).first()
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conversation = Conversation(
                id=conversation_id,
                title="New Conversation",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(conversation)
            db.commit()
        
        # Convert messages to provider format
        from app.ai.base import Message
        messages = [Message(role=m.role, content=m.content) for m in request.messages]
        
        # Get response from AI provider
        provider = get_current_provider()
        response_text = await provider.chat(messages)
        
        # Store message and response in database
        user_message = DBMessage(
            id=str(uuid4()),
            conversation_id=conversation_id,
            role="user",
            content=request.messages[-1].content,
            created_at=datetime.utcnow()
        )
        
        assistant_message = DBMessage(
            id=str(uuid4()),
            conversation_id=conversation_id,
            role="assistant",
            content=response_text,
            created_at=datetime.utcnow()
        )
        
        db.add(user_message)
        db.add(assistant_message)
        
        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        db.commit()
        
        # Store in semantic memory
        memory = get_memory()
        memory.add(
            documents=[response_text],
            metadatas=[{"conversation_id": conversation_id, "type": "response"}]
        )
        
        return ChatResponse(
            conversation_id=conversation_id,
            message=MessageResponse(role="assistant", content=response_text),
            model=provider.model_name
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations")
async def get_conversations(db: Session = Depends(get_db)):
    """Get all conversations"""
    try:
        conversations = db.query(Conversation).all()
        return conversations
    except Exception as e:
        logger.error(f"Error fetching conversations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str, db: Session = Depends(get_db)):
    """Get specific conversation with messages"""
    try:
        conversation = db.query(Conversation).filter_by(id=conversation_id).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        messages = db.query(DBMessage).filter_by(conversation_id=conversation_id).all()
        
        return {
            "conversation": conversation,
            "messages": messages
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))
