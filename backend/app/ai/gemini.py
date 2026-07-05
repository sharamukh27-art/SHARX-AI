"""Google Gemini AI Provider Implementation"""

import importlib
import logging
from typing import List, AsyncGenerator
from .base import AIProvider, Message

logger = logging.getLogger(__name__)


class GeminiProvider(AIProvider):
    """Google Gemini AI provider"""
    
    def __init__(self, api_key: str, model: str):
        """
        Initialize Gemini provider.
        
        Args:
            api_key: Google Gemini API key
            model: Model name to use (e.g., gemini-pro)
        """
        if not api_key:
            raise ValueError("Gemini API key is required")
        
        self._api_key = api_key
        self._model = model
        self.client = None
        self._setup_client(model)

    def _setup_client(self, model: str):
        try:
            genai = importlib.import_module("google.generativeai")
            genai.configure(api_key=self._api_key)
            self.client = genai
            self.model = self.client.GenerativeModel(model)
        except ImportError as exc:
            logger.error("google.generativeai package is required for the Gemini provider.")
            raise ImportError(
                "google.generativeai package is required for the Gemini provider. "
                "Install it or choose a different provider."
            ) from exc

    async def chat(self, messages: List[Message], **kwargs) -> str:
        """
        Send a chat message to Gemini and get response.
        
        Args:
            messages: List of messages
            **kwargs: Additional arguments
        
        Returns:
            Response text
        """
        try:
            # Convert messages to Gemini format
            history = []
            for msg in messages[:-1]:
                history.append({
                    "role": "user" if msg.role == "user" else "model",
                    "parts": [{"text": msg.content}]
                })
            
            # Start chat with history
            chat = self.model.start_chat(history=history)
            response = chat.send_message(messages[-1].content)
            return response.text
        except Exception as e:
            logger.error(f"Gemini chat error: {e}")
            raise
    
    async def stream_chat(self, messages: List[Message], **kwargs) -> AsyncGenerator[str, None]:
        """
        Stream chat response from Gemini.
        
        Args:
            messages: List of messages
            **kwargs: Additional arguments
        
        Yields:
            Chunks of response text
        """
        try:
            # Convert messages to Gemini format
            history = []
            for msg in messages[:-1]:
                history.append({
                    "role": "user" if msg.role == "user" else "model",
                    "parts": [{"text": msg.content}]
                })
            
            # Start chat with history
            chat = self.model.start_chat(history=history)
            response = chat.send_message(messages[-1].content, stream=True)
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            logger.error(f"Gemini stream error: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check if Gemini API is available"""
        if not self.client:
            return False

        try:
            self.client.generate(
                model=self._model,
                prompt="ping",
                max_output_tokens=1,
            )
            return True
        except Exception as e:
            logger.warning(f"Gemini health check failed: {e}")
            return False
    
    @property
    def model_name(self) -> str:
        """Get model name"""
        return self._model
