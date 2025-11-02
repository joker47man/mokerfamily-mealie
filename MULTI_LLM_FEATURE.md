# Multi-LLM Provider Support

## Overview

This feature enables Mealie to work with multiple Large Language Model (LLM) providers, giving users the flexibility to choose between OpenAI, Claude (Anthropic), and Gemini (Google) based on their preferences, costs, and availability.

## 🎯 Key Benefits

- **Choice**: Select the AI provider that works best for you
- **Cost Optimization**: Different providers have different pricing models
- **Flexibility**: Switch providers without code changes
- **Reliability**: Use alternative providers if one is unavailable
- **No Breaking Changes**: 100% backwards compatible with existing OpenAI configurations

## 🚀 Quick Start

### For New Users

Choose your preferred provider and set the required environment variables:

**OpenAI**
```bash
OPENAI_API_KEY=sk-...
```

**Claude**
```bash
CLAUDE_API_KEY=sk-ant-...
```

**Gemini**
```bash
GEMINI_API_KEY=AI...
```

### For Existing OpenAI Users

No action required! Your existing configuration will continue to work exactly as before.

## 📋 Supported Providers

| Provider | Default Model | Image Support | Cost |
|----------|---------------|---------------|------|
| OpenAI | gpt-4o | ✅ Yes | $$$ |
| Claude | claude-3-5-sonnet-20241022 | ✅ Yes | $$ |
| Gemini | gemini-1.5-flash | ✅ Yes | $ |

## 🔧 Configuration

### Explicit Provider Selection

Set `LLM_PROVIDER` to explicitly choose a provider:

```bash
LLM_PROVIDER=claude  # Options: openai, claude, gemini
```

### Auto-Detection

If `LLM_PROVIDER` is not set, Mealie will automatically use the first enabled provider in this order:
1. OpenAI (for backwards compatibility)
2. Claude
3. Gemini

### Provider-Specific Settings

Each provider has its own configuration options:

```bash
# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
OPENAI_BASE_URL=
OPENAI_ENABLE_IMAGE_SERVICES=true
OPENAI_WORKERS=2
OPENAI_SEND_DATABASE_DATA=true
OPENAI_REQUEST_TIMEOUT=300

# Claude
CLAUDE_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-3-5-sonnet-20241022
CLAUDE_BASE_URL=
CLAUDE_ENABLE_IMAGE_SERVICES=true
CLAUDE_WORKERS=2
CLAUDE_SEND_DATABASE_DATA=true
CLAUDE_REQUEST_TIMEOUT=300

# Gemini
GEMINI_API_KEY=AI...
GEMINI_MODEL=gemini-1.5-flash
GEMINI_ENABLE_IMAGE_SERVICES=true
GEMINI_WORKERS=2
GEMINI_SEND_DATABASE_DATA=true
GEMINI_REQUEST_TIMEOUT=300
```

## 🎨 Features

All providers support these Mealie features:

1. **Recipe Scraping**: Extract recipes from URLs
2. **Ingredient Parsing**: Parse ingredient strings into structured data
3. **Image to Recipe**: Extract recipes from images (photos of recipe cards, cookbooks)
4. **Debug Endpoint**: Test your LLM provider configuration

## 📚 Documentation

- [LLM Providers Configuration Guide](docs/LLM_PROVIDERS.md)
- [Migration Guide for OpenAI Users](docs/MIGRATION_TO_MULTI_LLM.md)

## 🏗️ Architecture

### High-Level Structure

```
mealie/services/llm_providers/
├── base.py                    # Abstract base class
├── factory.py                 # Provider factory & utilities
├── providers/
│   ├── openai_provider.py    # OpenAI implementation
│   ├── claude_provider.py    # Claude implementation
│   └── gemini_provider.py    # Gemini implementation
└── prompts/                   # Shared prompts for all providers
```

### Factory Functions

- `get_llm_service()`: Get the configured LLM service
- `is_llm_provider_enabled()`: Check if any provider is enabled
- `is_llm_image_services_enabled()`: Check if image services are available
- `get_active_provider_name()`: Get the name of the active provider

## 🔍 Testing Your Configuration

Use the admin debug endpoint to test your provider:

1. Log in as an admin
2. Navigate to Admin → Debug
3. Use the "Debug OpenAI" endpoint (works for all providers)
4. Optionally upload an image to test image services

The response will indicate:
- Which provider is being used
- Whether the connection is working
- A test response from the AI

## ⚠️ Error Handling

The system provides clear error messages to help you fix configuration issues:

- `"No LLM provider is enabled"` → Set at least one API key
- `"LLM provider 'X' is configured but not enabled"` → Check your API key
- `"Unknown LLM provider: X"` → Use 'openai', 'claude', or 'gemini'
- `"LLM image services are not available"` → Enable image services for your provider

## 💡 Tips

### Cost Optimization
- Use `gemini-1.5-flash` for the most cost-effective option
- Reduce `WORKERS` to minimize parallel API calls
- Set `SEND_DATABASE_DATA=false` to reduce token usage (may reduce accuracy)

### Performance
- Increase `WORKERS` for faster processing (higher cost)
- Use `gpt-4o` or `claude-3-5-sonnet` for best accuracy
- Adjust `REQUEST_TIMEOUT` based on your needs

### Switching Providers
1. Set the new provider's API key
2. Set `LLM_PROVIDER` to the new provider (optional)
3. Restart Mealie
4. Test with the debug endpoint

## 🔄 Backwards Compatibility

This feature is 100% backwards compatible:
- All existing OpenAI configurations work without changes
- The `mealie.services.openai` module still exists as a compatibility wrapper
- No database migrations required
- No breaking changes to the API

## 🤝 Contributing

To add support for a new LLM provider:

1. Create a new provider class in `mealie/services/llm_providers/providers/`
2. Implement the `BaseLLMService` interface
3. Add provider configuration to `mealie/core/settings/settings.py`
4. Update the factory in `mealie/services/llm_providers/factory.py`
5. Add documentation for the new provider

## 📊 Comparison

### When to use each provider:

**OpenAI (GPT-4o)**
- Best overall accuracy
- Excellent vision capabilities
- Most expensive
- Great for complex recipes

**Claude (3.5 Sonnet)**
- Strong reasoning
- Good balance of cost and performance
- Excellent for parsing instructions
- Good vision support

**Gemini (1.5 Flash)**
- Most cost-effective
- Fast responses
- Good for simple recipes
- Basic vision support

## 🐛 Troubleshooting

### Provider not working?
1. Check API key is valid
2. Verify provider is enabled in settings
3. Use debug endpoint to test connection
4. Check logs for detailed error messages

### Image services not working?
1. Ensure `*_ENABLE_IMAGE_SERVICES=true`
2. Verify API key has vision access
3. Check image format is supported
4. Try with a different provider

### Rate limiting?
1. Reduce `WORKERS` setting
2. Add delays between requests
3. Upgrade your API plan
4. Switch to a different provider

## 📝 License

This feature is part of Mealie and is subject to the same AGPL-3.0 license.

## 🙏 Acknowledgments

- OpenAI for GPT models
- Anthropic for Claude models
- Google for Gemini models
- The Mealie community for feedback and testing
