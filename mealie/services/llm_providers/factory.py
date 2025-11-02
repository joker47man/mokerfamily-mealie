from mealie.core.config import get_app_settings

from .base import BaseLLMService
from .providers import ClaudeProvider, GeminiProvider, OpenAIProvider


def get_llm_service() -> BaseLLMService:
    """
    Factory function to get the appropriate LLM service based on configuration.
    
    Returns the configured LLM provider, with priority:
    1. If LLM_PROVIDER is set, use that specific provider
    2. Otherwise, use OpenAI if enabled (for backwards compatibility)
    3. Otherwise, use Claude if enabled
    4. Otherwise, use Gemini if enabled
    5. If none are enabled, raise an error
    """
    settings = get_app_settings()
    
    # Check if a specific provider is configured
    provider = getattr(settings, "LLM_PROVIDER", None)
    
    if provider:
        provider = provider.lower()
        if provider == "openai":
            return OpenAIProvider()
        elif provider == "claude":
            return ClaudeProvider()
        elif provider == "gemini":
            return GeminiProvider()
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")
    
    # Fall back to auto-detection for backwards compatibility
    if settings.OPENAI_ENABLED:
        return OpenAIProvider()
    elif hasattr(settings, "CLAUDE_ENABLED") and settings.CLAUDE_ENABLED:
        return ClaudeProvider()
    elif hasattr(settings, "GEMINI_ENABLED") and settings.GEMINI_ENABLED:
        return GeminiProvider()
    else:
        raise ValueError("No LLM provider is enabled. Please configure OpenAI, Claude, or Gemini.")
