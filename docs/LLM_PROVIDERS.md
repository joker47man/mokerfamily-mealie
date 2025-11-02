# LLM Provider Configuration

Mealie now supports multiple Large Language Model (LLM) providers for AI-powered features like recipe scraping, ingredient parsing, and recipe extraction from images.

## Supported Providers

### 1. OpenAI
- **Models**: GPT-4o, GPT-4, GPT-3.5-turbo, and other OpenAI models
- **Features**: Text generation, vision (image understanding)
- **Default Model**: `gpt-4o`

### 2. Claude (Anthropic)
- **Models**: Claude 3 Opus, Claude 3.5 Sonnet, Claude 3 Haiku
- **Features**: Text generation, vision (image understanding)
- **Default Model**: `claude-3-5-sonnet-20241022`

### 3. Gemini (Google)
- **Models**: Gemini 1.5 Pro, Gemini 1.5 Flash
- **Features**: Text generation, vision (image understanding)
- **Default Model**: `gemini-1.5-flash`

## Configuration

### Environment Variables

#### General LLM Configuration
```bash
# Optional: Explicitly set the LLM provider to use
LLM_PROVIDER=openai  # Options: 'openai', 'claude', 'gemini'
```

If `LLM_PROVIDER` is not set, Mealie will automatically use the first enabled provider (OpenAI has priority for backwards compatibility).

#### OpenAI Configuration
```bash
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4o                    # Optional, default: gpt-4o
OPENAI_BASE_URL=                       # Optional, for custom endpoints
OPENAI_ENABLE_IMAGE_SERVICES=true     # Optional, default: true
OPENAI_WORKERS=2                       # Optional, default: 2
OPENAI_SEND_DATABASE_DATA=true        # Optional, default: true
OPENAI_REQUEST_TIMEOUT=300            # Optional, default: 300 seconds
```

#### Claude Configuration
```bash
CLAUDE_API_KEY=your-api-key-here
CLAUDE_MODEL=claude-3-5-sonnet-20241022  # Optional
CLAUDE_BASE_URL=                         # Optional, for custom endpoints
CLAUDE_ENABLE_IMAGE_SERVICES=true       # Optional, default: true
CLAUDE_WORKERS=2                         # Optional, default: 2
CLAUDE_SEND_DATABASE_DATA=true          # Optional, default: true
CLAUDE_REQUEST_TIMEOUT=300              # Optional, default: 300 seconds
```

#### Gemini Configuration
```bash
GEMINI_API_KEY=your-api-key-here
GEMINI_MODEL=gemini-1.5-flash           # Optional
GEMINI_ENABLE_IMAGE_SERVICES=true      # Optional, default: true
GEMINI_WORKERS=2                        # Optional, default: 2
GEMINI_SEND_DATABASE_DATA=true         # Optional, default: true
GEMINI_REQUEST_TIMEOUT=300             # Optional, default: 300 seconds
```

## Getting API Keys

### OpenAI
1. Visit https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Set the `OPENAI_API_KEY` environment variable

### Claude (Anthropic)
1. Visit https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Set the `CLAUDE_API_KEY` environment variable

### Gemini (Google)
1. Visit https://makersuite.google.com/app/apikey
2. Sign up or log in with your Google account
3. Create a new API key
4. Set the `GEMINI_API_KEY` environment variable

## Features by Provider

### Recipe Scraping
All providers can extract recipes from web pages.

**Example**: When you provide a URL, Mealie sends the page content to the LLM to extract recipe information.

### Ingredient Parsing
All providers can parse ingredient strings into structured data (quantity, unit, food, notes).

**Example**: "2 cups of flour" → `{quantity: 2, unit: "cups", food: "flour"}`

### Recipe from Images
All providers support extracting recipes from images (photos of recipe cards, cookbooks, etc.).

**Example**: Upload an image of a recipe, and the LLM will extract the title, ingredients, instructions, etc.

## Provider Selection Strategy

If `LLM_PROVIDER` is not explicitly set, Mealie will use the first available provider in this order:
1. OpenAI (if `OPENAI_API_KEY` is set)
2. Claude (if `CLAUDE_API_KEY` is set)
3. Gemini (if `GEMINI_API_KEY` is set)

## Cost Considerations

- **Workers**: Increasing the number of workers can speed up processing but will increase API costs
- **Database Data**: Sending database data (like existing units) can improve accuracy but increases token usage
- **Image Services**: Image processing typically costs more than text-only requests

## Backwards Compatibility

All existing OpenAI configuration and functionality is preserved. Projects using OpenAI will continue to work without any changes.

## Testing Your Configuration

You can test your LLM provider configuration using the admin debug endpoint:
1. Log in as an admin
2. Navigate to the admin section
3. Use the "Debug OpenAI" endpoint (works for all providers)
4. Optionally upload an image to test image services

The endpoint will return which provider is being used and a test response.

## Troubleshooting

### "No LLM provider is enabled"
- Make sure at least one of `OPENAI_API_KEY`, `CLAUDE_API_KEY`, or `GEMINI_API_KEY` is set
- Verify the API key is valid

### "LLM image services are not available"
- Check that `*_ENABLE_IMAGE_SERVICES` is set to `true` for your provider
- Verify your API key has access to vision models

### Provider not being used
- Set `LLM_PROVIDER` explicitly to force a specific provider
- Check that the provider is enabled (has a valid API key)

### Rate Limiting
- Most providers have rate limits on their APIs
- Reduce the number of `WORKERS` if you're hitting rate limits
- Consider upgrading your API plan if needed

## Model Recommendations

### For Cost Efficiency
- **Gemini**: `gemini-1.5-flash` - Fast and cost-effective
- **OpenAI**: `gpt-3.5-turbo` - Good balance of cost and performance
- **Claude**: `claude-3-haiku-20240307` - Fast and affordable

### For Best Results
- **OpenAI**: `gpt-4o` - Excellent vision and text understanding
- **Claude**: `claude-3-5-sonnet-20241022` - Great reasoning and accuracy
- **Gemini**: `gemini-1.5-pro` - Strong multimodal capabilities

### For Vision Tasks
- All providers support vision, but quality may vary
- Test with your specific use case to determine the best provider
