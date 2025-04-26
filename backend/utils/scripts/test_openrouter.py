#!/usr/bin/env python3
"""
OpenRouter Integration Test Script

This script tests the OpenRouter integration by making simple API calls to various
OpenRouter-provided models. Use this script to verify your OpenRouter API key is working
and to test different models.

Usage:
    python test_openrouter.py [model_name]

    model_name (optional): Name of the OpenRouter model to test. 
    If not specified, tests multiple models.

Examples:
    python test_openrouter.py
    python test_openrouter.py openrouter/openai/gpt-4o
    python test_openrouter.py openrouter/anthropic/claude-3-5-sonnet
"""

import os
import sys
import asyncio
from dotenv import load_dotenv
import json

# Add backend directory to path (assuming script is run from the utils/scripts directory)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from services.llm import make_llm_api_call, setup_api_keys


async def test_model(model_name):
    """Test a specific model with a sample query."""
    print(f"\n\033[1mTesting model: {model_name}\033[0m")
    
    test_messages = [
        {"role": "user", "content": "Please respond to this test message with a short haiku about technology."}
    ]
    
    try:
        response = await make_llm_api_call(
            model_name=model_name,
            messages=test_messages,
            temperature=0.7,
            max_tokens=100
        )
        
        if response and hasattr(response, "choices") and response.choices:
            content = response.choices[0].message.content.strip()
            model_used = getattr(response, "model", model_name)
            
            print(f"\033[32m✓ Success!\033[0m")
            print(f"\033[94mModel used:\033[0m {model_used}")
            print(f"\033[94mResponse:\033[0m\n{content}\n")
            return True
        else:
            print(f"\033[31m✗ Failed: Unexpected response format\033[0m")
            return False
            
    except Exception as e:
        print(f"\033[31m✗ Error testing {model_name}: {str(e)}\033[0m")
        return False


async def main():
    """Main test function."""
    load_dotenv()  # Load environment variables from .env
    
    # Ensure API keys are set up
    setup_api_keys()
    
    # Check if OpenRouter API key is set
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_key:
        print("\033[31mERROR: OPENROUTER_API_KEY is not set in your .env file\033[0m")
        print("Please add your OpenRouter API key to your .env file:")
        print("OPENROUTER_API_KEY=your_api_key_here")
        return
    
    # Get model name from command line argument or use multiple test models
    if len(sys.argv) > 1:
        chosen_model = sys.argv[1]
        await test_model(chosen_model)
    else:
        # Test multiple common models
        test_models = [
            "openrouter/openai/gpt-4o-mini",
            "openrouter/anthropic/claude-3-haiku-20240307",
            "openrouter/meta-llama/llama-3-8b-instruct"
        ]
        
        success_count = 0
        for model in test_models:
            if await test_model(model):
                success_count += 1
        
        print(f"\n\033[1mTest summary: {success_count}/{len(test_models)} models tested successfully\033[0m")
        
        print("\nTo test a specific model, run:")
        print("python test_openrouter.py openrouter/provider/model-name")


if __name__ == "__main__":
    asyncio.run(main())
