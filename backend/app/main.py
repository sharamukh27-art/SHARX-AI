"""Main FastAPI application"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.db import init_database, close_database
from app.ai.factory import init_provider
from app.memory import init_memory
from app.api.chat import router as chat_router
from app.api.system import router as system_router
from app.api.notes import router as notes_router
from app.api.memory import router as memory_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting SHAR-X AI application...")
    init_database()
    init_provider()
    init_memory()
    logger.info("Application initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down SHAR-X AI application...")
    close_database()
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="SHAR-X AI",
    description="The Future of Intelligent Assistance. A Machine-Mind, Awakened.",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router)
app.include_router(system_router)
app.include_router(notes_router)
app.include_router(memory_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": "SHAR-X AI",
        "tagline": "The Future of Intelligent Assistance",
        "version": "1.0.0",
        "status": "running"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
