from mealie.core.config import get_app_settings

from .base import BaseLLMService
from .providers import ClaudeProvider, GeminiProvider, OpenAIProvider


def is_llm_provider_enabled() -> bool:
    """
    Check if any LLM provider is enabled.
    
    Returns:
        True if at least one LLM provider is configured and enabled
    """
    settings = get_app_settings()
    return (
        settings.OPENAI_ENABLED
        or getattr(settings, "CLAUDE_ENABLED", False)
        or getattr(settings, "GEMINI_ENABLED", False)
    )


def is_llm_image_services_enabled() -> bool:
    """
    Check if any LLM provider with image services is enabled.
    
    Returns:
        True if at least one LLM provider with image services is configured and enabled
    """
    settings = get_app_settings()
    return (
        (settings.OPENAI_ENABLED and settings.OPENAI_ENABLE_IMAGE_SERVICES)
        or (getattr(settings, "CLAUDE_ENABLED", False) and getattr(settings, "CLAUDE_ENABLE_IMAGE_SERVICES", False))
        or (getattr(settings, "GEMINI_ENABLED", False) and getattr(settings, "GEMINI_ENABLE_IMAGE_SERVICES", False))
    )


def get_active_provider_name() -> str | None:
    """
    Get the name of the active LLM provider.
    
    Returns:
        The name of the active provider ('OpenAI', 'Claude', 'Gemini') or None if none are enabled
    """
    settings = get_app_settings()
    
    provider = getattr(settings, "LLM_PROVIDER", None)
    if provider:
        provider = provider.lower()
        if provider == "openai" and settings.OPENAI_ENABLED:
            return "OpenAI"
        elif provider == "claude" and getattr(settings, "CLAUDE_ENABLED", False):
            return "Claude"
        elif provider == "gemini" and getattr(settings, "GEMINI_ENABLED", False):
            return "Gemini"
    
    # Fall back to auto-detection
    if settings.OPENAI_ENABLED:
        return "OpenAI"
    elif getattr(settings, "CLAUDE_ENABLED", False):
        return "Claude"
    elif getattr(settings, "GEMINI_ENABLED", False):
        return "Gemini"
    
    return None


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
