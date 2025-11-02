"""
Backwards compatibility wrapper for OpenAI service.
This module maintains the old OpenAI-specific API while delegating to the new LLM provider system.
"""

from mealie.services.llm_providers import (
    LLMDataInjection as OpenAIDataInjection,
    LLMImageBase as OpenAIImageBase,
    LLMImageExternal as OpenAIImageExternal,
    LLMLocalImage as OpenAILocalImage,
)
from mealie.services.llm_providers.providers import OpenAIProvider as OpenAIService

__all__ = [
    "OpenAIDataInjection",
    "OpenAIImageBase",
    "OpenAIImageExternal",
    "OpenAILocalImage",
    "OpenAIService",
]
