# Ptah Backend

## Running the backend

Within the backend directory, run the following command to stop and start the backend:
```bash
docker compose down && docker compose up --build
```

## Running Individual Services

You can run individual services from the docker-compose file. This is particularly useful during development:

### Running only Redis
```bash
docker compose up redis
```

### Running only the API
```bash
docker compose up api
```

## Development Setup

For local development, you might only need to run Redis while working on the API locally. This is useful when:

- You're making changes to the API code and want to test them directly
- You want to avoid rebuilding the API container on every change
- You're running the API service directly on your machine

To run just Redis for development:```bash
docker compose up redis
```

Then you can run your API service locally with your preferred method (e.g., poetry run python3.11 api.py).

### Environment Configuration
When running services individually, make sure to:
1. Check your `.env` file and adjust any necessary environment variables
2. Ensure Redis connection settings match your local setup (default: `localhost:6379`)
3. Update any service-specific environment variables if needed

## LLM Configuration

### Supported LLM Providers

Ptah supports multiple LLM providers, giving you flexibility in choosing the right model for your needs:

1. **Anthropic** - Models like Claude 3 Opus, Claude 3 Sonnet, Claude 3.5 Sonnet
2. **OpenAI** - GPT-4, GPT-4 Turbo, GPT-4o models
3. **AWS Bedrock** - Access to Claude models via AWS
4. **Groq** - For high-performance inference
5. **OpenRouter** - A unified API for accessing various AI models

### Using OpenRouter

[OpenRouter](https://openrouter.ai/) provides access to models from multiple providers (OpenAI, Anthropic, Meta, Mistral, etc.) through a single API key. This is especially useful for self-hosted deployments where you want flexibility in model selection.

To use OpenRouter:

1. Create an account at [OpenRouter](https://openrouter.ai/) and generate an API key
2. Add the following to your `.env` file:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   MODEL_TO_USE=openrouter/openai/gpt-4o  # Example model path
   ```
3. Prefix the model name with `openrouter/provider/model-name`, for example:
   - `openrouter/openai/gpt-4o`
   - `openrouter/anthropic/claude-3-5-sonnet`
   - `openrouter/meta-llama/llama-3-70b-instruct`

For detailed documentation on OpenRouter integration, see [OpenRouter API Reference](../docs/OpenRouter-API-reference.md).

## Redis Configuration

### Redis Host Configuration
When running the API locally with Redis in Docker, you need to set the correct Redis host in your `.env` file:
- For Docker-to-Docker communication (when running both services in Docker): use `REDIS_HOST=redis`
- For local-to-Docker communication (when running API locally): use `REDIS_HOST=localhost`

Example `.env` configuration for local development:
```env
REDIS_HOST=localhost (instead of 'redis')
REDIS_PORT=6379
REDIS_PASSWORD=
```
