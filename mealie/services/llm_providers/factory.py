from mealie.core.config import get_app_settings

from .base import BaseLLMService
from .providers import ClaudeProvider, GeminiProvider, OpenAIProvider


def _get_provider_states(settings) -> dict[str, bool]:
    """
    Helper function to get the enabled state of all providers.
    
    Args:
        settings: AppSettings instance
        
    Returns:
        Dictionary with provider names as keys and their enabled state as values
    """
    return {
        "openai": settings.OPENAI_ENABLED,
        "claude": getattr(settings, "CLAUDE_ENABLED", False),
        "gemini": getattr(settings, "GEMINI_ENABLED", False),
    }


def is_llm_provider_enabled() -> bool:
    """
    Check if any LLM provider is enabled.
    
    Returns:
        True if at least one LLM provider is configured and enabled
    """
    settings = get_app_settings()
    provider_states = _get_provider_states(settings)
    return any(provider_states.values())


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
    provider_states = _get_provider_states(settings)
    
    # Check if a specific provider is configured
    configured_provider = getattr(settings, "LLM_PROVIDER", None)
    if configured_provider:
        provider_key = configured_provider.lower()
        if provider_key in provider_states and provider_states[provider_key]:
            return configured_provider.capitalize()
    
    # Fall back to auto-detection (priority order: OpenAI, Claude, Gemini)
    if provider_states["openai"]:
        return "OpenAI"
    elif provider_states["claude"]:
        return "Claude"
    elif provider_states["gemini"]:
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
    provider_states = _get_provider_states(settings)
    
    # Check if a specific provider is configured
    configured_provider = getattr(settings, "LLM_PROVIDER", None)
    
    if configured_provider:
        provider_key = configured_provider.lower()
        if provider_key == "openai":
            return OpenAIProvider()
        elif provider_key == "claude":
            return ClaudeProvider()
        elif provider_key == "gemini":
            return GeminiProvider()
        else:
            raise ValueError(f"Unknown LLM provider: {configured_provider}")
    
    # Fall back to auto-detection for backwards compatibility
    if provider_states["openai"]:
        return OpenAIProvider()
    elif provider_states["claude"]:
        return ClaudeProvider()
    elif provider_states["gemini"]:
        return GeminiProvider()
    else:
        raise ValueError("No LLM provider is enabled. Please configure OpenAI, Claude, or Gemini.")
