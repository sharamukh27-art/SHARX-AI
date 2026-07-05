"""SQLAlchemy models for SHAR-X AI"""

from sqlalchemy import Column, String, Text, DateTime, Integer, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Conversation(Base):
    """Conversation history model"""
    __tablename__ = "conversations"
    
    id = Column(String(36), primary_key=True)
    title = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    meta = Column(JSON, default={})


class Message(Base):
    """Message model for conversations"""
    __tablename__ = "messages"
    
    id = Column(String(36), primary_key=True)
    conversation_id = Column(String(36), nullable=False)
    role = Column(String(20), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    meta = Column(JSON, default={})


class Memory(Base):
    """Long-term memory model"""
    __tablename__ = "memories"
    
    id = Column(String(36), primary_key=True)
    content = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)  # "semantic", "episodic", etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    meta = Column(JSON, default={})


class Note(Base):
    """User notes model"""
    __tablename__ = "notes"
    
    id = Column(String(36), primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tags = Column(JSON, default=[])
    meta = Column(JSON, default={})


class Reminder(Base):
    """User reminders model"""
    __tablename__ = "reminders"
    
    id = Column(String(36), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    scheduled_at = Column(DateTime, nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    meta = Column(JSON, default={})


class Settings(Base):
    """Application settings model"""
    __tablename__ = "settings"
    
    key = Column(String(100), primary_key=True)
    value = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
