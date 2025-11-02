# Migration Guide: Multi-LLM Provider Support

This guide helps you migrate from the OpenAI-only implementation to the new multi-LLM provider system.

## For Existing OpenAI Users

### No Action Required! 🎉

If you're already using OpenAI, **everything will continue to work exactly as before**. No configuration changes are needed.

Your existing environment variables will work:
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `OPENAI_BASE_URL`
- `OPENAI_ENABLE_IMAGE_SERVICES`
- And all other `OPENAI_*` variables

## What's New

You can now choose between three LLM providers:
1. **OpenAI** (GPT-4, GPT-3.5, etc.)
2. **Claude** (Anthropic)
3. **Gemini** (Google)

## Why Switch Providers?

You might want to use a different provider for:
- **Cost**: Different providers have different pricing models
- **Performance**: Some providers may work better for your specific use case
- **Availability**: Regional availability or API access
- **Features**: Different models have different capabilities

## Switching to Claude

1. Get a Claude API key from https://console.anthropic.com/
2. Add these environment variables:
   ```bash
   CLAUDE_API_KEY=your-claude-api-key
   LLM_PROVIDER=claude  # Optional but recommended
   ```
3. Remove or keep your OpenAI configuration (keeping it allows easy switching back)
4. Restart Mealie

## Switching to Gemini

1. Get a Gemini API key from https://makersuite.google.com/app/apikey
2. Add these environment variables:
   ```bash
   GEMINI_API_KEY=your-gemini-api-key
   LLM_PROVIDER=gemini  # Optional but recommended
   ```
3. Remove or keep your OpenAI configuration (keeping it allows easy switching back)
4. Restart Mealie

## Using Multiple Providers

You can configure multiple providers and switch between them:

```bash
# Configure all three
OPENAI_API_KEY=your-openai-key
CLAUDE_API_KEY=your-claude-key
GEMINI_API_KEY=your-gemini-key

# Choose which one to use
LLM_PROVIDER=claude  # or 'openai' or 'gemini'
```

This allows you to:
- Test different providers easily
- Switch providers if one is unavailable
- Compare results across providers

## Configuration Equivalents

### OpenAI → Claude
```bash
# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
OPENAI_ENABLE_IMAGE_SERVICES=true

# Claude equivalent
CLAUDE_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-3-5-sonnet-20241022
CLAUDE_ENABLE_IMAGE_SERVICES=true
```

### OpenAI → Gemini
```bash
# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
OPENAI_ENABLE_IMAGE_SERVICES=true

# Gemini equivalent
GEMINI_API_KEY=AI...
GEMINI_MODEL=gemini-1.5-flash
GEMINI_ENABLE_IMAGE_SERVICES=true
```

## Testing Your Migration

After switching providers, test these features:
1. **Recipe Scraping**: Import a recipe from a URL
2. **Ingredient Parsing**: Add or edit ingredients
3. **Image to Recipe**: Upload a recipe image

Use the admin debug endpoint to verify your configuration.

## Rollback

If you need to switch back to OpenAI:
1. Set `LLM_PROVIDER=openai` (or remove it)
2. Ensure `OPENAI_API_KEY` is still configured
3. Restart Mealie

## Breaking Changes

**None!** This is a fully backwards-compatible update.

## Code Changes (For Developers)

If you've extended Mealie with custom code:

### Old Way (OpenAI-specific)
```python
from mealie.services.openai import OpenAIService

service = OpenAIService()
response = await service.get_response(prompt, message)
```

### New Way (Provider-agnostic)
```python
from mealie.services.llm_providers import get_llm_service

service = get_llm_service()  # Automatically uses configured provider
response = await service.get_response(prompt, message)
```

The old OpenAI-specific imports still work for backwards compatibility!

## FAQ

### Q: Do I need to change my existing configuration?
**A**: No, existing OpenAI configurations continue to work.

### Q: Can I use multiple providers at the same time?
**A**: You can configure multiple providers, but only one is active at a time (selected by `LLM_PROVIDER` or auto-detected).

### Q: Will my recipes be affected?
**A**: No, recipes are stored data. Only new AI operations will use the new provider.

### Q: Are the results the same across providers?
**A**: Results may vary slightly as each provider has different models and capabilities. Test to see which works best for you.

### Q: What happens if I set `LLM_PROVIDER` to a provider that's not configured?
**A**: Mealie will return an error indicating the provider is not enabled. Make sure to set the API key for your chosen provider.

### Q: Can I mix providers (e.g., OpenAI for scraping, Claude for parsing)?
**A**: Not currently. One provider is used for all LLM operations.

## Support

If you encounter issues after migrating:
1. Check that your API key is valid
2. Verify the provider is enabled in the admin section
3. Use the debug endpoint to test connectivity
4. Check the logs for error messages
5. Open an issue on GitHub with details about your configuration (without exposing API keys!)
