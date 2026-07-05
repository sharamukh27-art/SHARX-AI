"""Application settings and configuration"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application configuration loaded from environment variables"""
    
    # FastAPI Configuration
    fastapi_env: str = Field(default="development", alias="FASTAPI_ENV")
    debug: bool = Field(default=True)
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    api_cors_origins: List[str] = Field(
        default=["http://localhost:5173", "http://localhost:3000"],
        alias="API_CORS_ORIGINS"
    )
    
    # AI Provider Configuration
    ai_provider: str = Field(default="ollama", alias="AI_PROVIDER")
    
    # Ollama Configuration
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="neural-chat", alias="OLLAMA_MODEL")
    
    # Gemini Configuration
    gemini_api_key: str = Field(default="", alias="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-pro", alias="GEMINI_MODEL")
    
    # OpenAI Configuration
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4-turbo-preview", alias="OPENAI_MODEL")
    
    # Database Configuration
    database_url: str = Field(default="sqlite:///./sharx_ai.db", alias="DATABASE_URL")
    
    # ChromaDB Configuration
    chroma_persist_dir: str = Field(default="./chroma_data", alias="CHROMA_PERSIST_DIR")
    
    # Security (Phase 2+)
    secret_key: str = Field(default="dev-secret-key-change-in-production", alias="SECRET_KEY")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.fastapi_env == "production"


settings = Settings()
