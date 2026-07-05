"""AI Provider factory"""

import logging
from app.config import settings
from .base import AIProvider

logger = logging.getLogger(__name__)


def get_provider() -> AIProvider:
    """
    Get AI provider based on configuration.
    
    Returns:
        Configured AI provider instance
    
    Raises:
        ValueError: If provider is not configured or unsupported
    """
    provider_name = settings.ai_provider.lower()
    
    if provider_name == "ollama":
        from .ollama import OllamaProvider

        logger.info(f"Using Ollama provider: {settings.ollama_model}")
        return OllamaProvider(settings.ollama_base_url, settings.ollama_model)
    
    elif provider_name == "gemini":
        if not settings.gemini_api_key:
            raise ValueError("Gemini API key not configured")
        from .gemini import GeminiProvider

        logger.info(f"Using Gemini provider: {settings.gemini_model}")
        return GeminiProvider(settings.gemini_api_key, settings.gemini_model)
    
    elif provider_name == "openai":
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key not configured")
        from .openai import OpenAIProvider

        logger.info(f"Using OpenAI provider: {settings.openai_model}")
        return OpenAIProvider(settings.openai_api_key, settings.openai_model)
    
    else:
        raise ValueError(f"Unsupported AI provider: {provider_name}")


# Global provider instance
_provider = None


def init_provider() -> AIProvider:
    """Initialize global provider instance"""
    global _provider
    if _provider is None:
        _provider = get_provider()
    return _provider


def get_current_provider() -> AIProvider:
    """Get current provider, initializing if needed"""
    return init_provider()
