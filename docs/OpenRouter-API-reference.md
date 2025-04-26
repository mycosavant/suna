# OpenRouter Integration Guide

This document provides guidance on using OpenRouter as a model provider in Ptah. OpenRouter acts as a gateway to multiple LLM providers, allowing you to access various models with a single API key.

## What is OpenRouter?

[OpenRouter](https://openrouter.ai/) is a unified API for accessing various AI models from different providers, including:

- OpenAI Models (GPT-4o, GPT-4 Turbo, etc.)
- Anthropic Models (Claude 3.5 Sonnet, Claude 3 Opus, etc.)
- Meta Models (Llama 3 family)
- Mistral Models (Mixtral, Mistral Large, etc.)
- Cohere Models
- And many more

OpenRouter offers several advantages:
- Single API key for multiple model providers
- Pay-as-you-go pricing
- Fallback capabilities
- Simplified integration

## Configuration

### Environment Variables

Add your OpenRouter API key to your `.env` file:

```
# OpenRouter Configuration
OPENROUTER_API_KEY=your_api_key_here
OR_SITE_URL=https://your-app-domain.com  # Optional
OR_APP_NAME=YourAppName  # Optional, defaults to "suna.so"
MODEL_TO_USE=openrouter/openai/gpt-4o  # To use OpenRouter as default
```

### OpenRouter Model Names

When using OpenRouter models, prefix the model name with `openrouter/`:

```
openrouter/{provider}/{model}
```

For example:
- `openrouter/openai/gpt-4o`
- `openrouter/anthropic/claude-3-5-sonnet`
- `openrouter/meta-llama/llama-3-70b-instruct`
- `openrouter/mistralai/mistral-large-latest`

## Usage Examples

### Setting as Default Model

To use an OpenRouter model as your default:

```
MODEL_TO_USE=openrouter/openai/gpt-4o
```

### Specifying a Model for an Agent Run

When initializing an agent, you can specify an OpenRouter model:

```python
response = await run_agent(
    thread_id=thread_id,
    project_id=project_id,
    stream=True,
    model_name="openrouter/anthropic/claude-3-opus-20240229"
)
```

## Popular OpenRouter Models

Here are some popular models available through OpenRouter:

### OpenAI
- `openrouter/openai/gpt-4o`
- `openrouter/openai/gpt-4o-mini`
- `openrouter/openai/gpt-4-turbo`

### Anthropic
- `openrouter/anthropic/claude-3-5-sonnet`
- `openrouter/anthropic/claude-3-opus-20240229`
- `openrouter/anthropic/claude-3-sonnet-20240229`
- `openrouter/anthropic/claude-3-haiku-20240307`

### Meta
- `openrouter/meta-llama/llama-3-70b-instruct`
- `openrouter/meta-llama/llama-3-8b-instruct`

### Mistral
- `openrouter/mistralai/mistral-large-latest`
- `openrouter/mistralai/mixtral-8x7b-instruct`

### Google
- `openrouter/google/gemma-7b-it`

## Model Selection Considerations

When choosing a model, consider:

1. **Capability needs**: More complex tasks may require more powerful models
2. **Cost**: Larger models typically cost more per token
3. **Speed**: Smaller models generally respond faster
4. **Token context window**: Varies by model (4K to 128K+)
5. **Tool usage support**: Varies by model

## Testing OpenRouter Connection

We've included a dedicated test script to verify your OpenRouter integration is working properly:

```bash
cd backend
python utils/scripts/test_openrouter.py
```

This script will:
1. Check if your OpenRouter API key is properly configured
2. Test connections to multiple common models
3. Display the response from each model

To test a specific model:

```bash
python utils/scripts/test_openrouter.py openrouter/openai/gpt-4o
```

You can also run the built-in test function in the LLM service module:

```bash
python -c "import asyncio; from services.llm import test_openrouter; asyncio.run(test_openrouter())"
```

## Troubleshooting

Common issues:

1. **Invalid API Key**: Ensure your OpenRouter API key is correctly set in your `.env` file
2. **Incorrect Model Name**: Verify the model name follows the format `openrouter/{provider}/{model}`
3. **Rate Limits**: OpenRouter applies usage limits based on your account type
4. **Missing Headers**: The `OR_SITE_URL` and `OR_APP_NAME` help identify your application to OpenRouter

## Additional Resources

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [OpenRouter API Reference](https://openrouter.ai/docs/api-reference)
- [OpenRouter Dashboard](https://openrouter.ai/dashboard)
