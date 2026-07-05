"""Base AI provider interface"""

from abc import ABC, abstractmethod
from typing import List, Optional, AsyncGenerator
from pydantic import BaseModel


class Message(BaseModel):
    """Message structure"""
    role: str  # "user", "assistant", "system"
    content: str


class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    async def chat(self, messages: List[Message], **kwargs) -> str:
        """
        Send a chat message and get a response.
        
        Args:
            messages: List of message objects
            **kwargs: Additional provider-specific arguments
        
        Returns:
            Response text
        """
        pass
    
    @abstractmethod
    async def stream_chat(self, messages: List[Message], **kwargs) -> AsyncGenerator[str, None]:
        """
        Send a chat message and stream the response.
        
        Args:
            messages: List of message objects
            **kwargs: Additional provider-specific arguments
        
        Yields:
            Chunks of response text
        """
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check if the provider is available and healthy.
        
        Returns:
            True if provider is ready, False otherwise
        """
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Get the model name being used"""
        pass
