"""
Backwards compatibility wrapper for OpenAI parser.
This now delegates to the generic LLM parser.
"""
from mealie.schema.recipe.recipe_ingredient import ParsedIngredient

from ..llm.parser import LLMParser


class OpenAIParser(LLMParser):
    """
    Backwards compatibility wrapper for OpenAI parser.
    Delegates to LLMParser which supports multiple LLM providers.
    """
    pass
