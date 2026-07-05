"""Database connection and session management"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings
from .models import Base
import logging

logger = logging.getLogger(__name__)


class Database:
    """Database connection manager"""
    
    def __init__(self):
        """Initialize database connection"""
        self.engine = create_engine(
            settings.database_url,
            connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {},
            echo=settings.debug
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        Base.metadata.create_all(bind=self.engine)
        logger.info("Database initialized successfully")
    
    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()
    
    def close(self):
        """Close database connection"""
        self.engine.dispose()


# Global database instance
_db = None


def get_db() -> Session:
    """
    Dependency injection for database session.
    
    Usage in FastAPI:
        @app.get("/")
        def index(db: Session = Depends(get_db)):
            ...
    """
    global _db
    if _db is None:
        _db = Database()
    return _db.get_session()


def init_database():
    """Initialize global database instance"""
    global _db
    if _db is None:
        _db = Database()
    return _db


def close_database():
    """Close global database connection"""
    global _db
    if _db is not None:
        _db.close()
        _db = None
