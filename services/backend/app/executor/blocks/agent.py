"""Agent block executor - LLM inference with multi-provider support"""

from typing import Any, Optional
import httpx

from app.core.config import settings
from app.core.logging import get_logger
from app.executor.state import WorkflowState

logger = get_logger(__name__)


class AgentError(Exception):
    """Custom exception for agent errors"""
    pass


async def execute_agent_block(
    block: dict[str, Any], input_data: dict[str, Any], state: WorkflowState
) -> dict[str, Any]:
    """Execute an AI agent block with LLM

    Supports multiple providers:
    - OpenAI (GPT-3.5, GPT-4, GPT-4-turbo, etc.)
    - Azure OpenAI (all OpenAI models via Azure)
    - Anthropic (Claude 3 models)
    - Groq (Llama, Mixtral, etc.)
    - Google (Gemini)

    Auto-detects provider based on model name or explicit provider setting.
    """

    model = input_data.get("model", "gpt-4")
    provider = input_data.get("provider", _detect_provider(model))

    logger.info(
        "agent_block_executing",
        block_id=block["id"],
        model=model,
        provider=provider,
    )

    # Route to appropriate provider
    if provider == "azure-openai":
        result = await _execute_azure_openai(input_data, block)
    elif provider == "anthropic":
        result = await _execute_anthropic(input_data, block)
    elif provider == "groq":
        result = await _execute_groq(input_data, block)
    elif provider == "google":
        result = await _execute_google(input_data, block)
    elif provider == "openai":
        result = await _execute_openai(input_data, block)
    else:
        raise AgentError(f"Unsupported provider: {provider}")

    logger.info(
        "agent_block_completed",
        block_id=block["id"],
        provider=provider,
        tokens=result.get("tokens", {}).get("total", 0),
    )

    return result


def _detect_provider(model: str) -> str:
    """Auto-detect provider based on model name"""
    model_lower = model.lower()

    if "claude" in model_lower:
        return "anthropic"
    elif "gemini" in model_lower:
        return "google"
    elif "llama" in model_lower or "mixtral" in model_lower:
        return "groq"
    else:
        # Default to OpenAI
        return "openai"


async def _execute_openai(input_data: dict[str, Any], block: dict[str, Any]) -> dict[str, Any]:
    """Execute OpenAI request"""

    system_prompt = input_data.get("system_prompt", "")
    user_prompt = input_data.get("user_prompt", "")
    model = input_data.get("model", "gpt-4")
    temperature = input_data.get("temperature", 0.7)
    max_tokens = input_data.get("max_tokens")
    api_key = input_data.get("api_key") or (
        settings.OPENAI_API_KEY if hasattr(settings, 'OPENAI_API_KEY') else None
    )

    if not api_key:
        raise AgentError("OpenAI API key is required")

    # Prepare messages
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    # Prepare request payload
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    if max_tokens:
        payload["max_tokens"] = max_tokens

    # Call OpenAI API
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=120.0,
            )

            response.raise_for_status()
            data = response.json()

        # Extract response
        content = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})

        return {
            "content": content,
            "tokens": {
                "prompt": usage.get("prompt_tokens", 0),
                "completion": usage.get("completion_tokens", 0),
                "total": usage.get("total_tokens", 0),
            },
            "model": model,
            "provider": "openai",
            "finish_reason": data["choices"][0].get("finish_reason"),
        }

    except httpx.HTTPStatusError as e:
        logger.error(
            "openai_request_failed",
            block_id=block["id"],
            status_code=e.response.status_code,
            error=e.response.text,
        )
        raise AgentError(f"OpenAI request failed: {e.response.text}") from e


async def _execute_azure_openai(input_data: dict[str, Any], block: dict[str, Any]) -> dict[str, Any]:
    """Execute Azure OpenAI request"""

    system_prompt = input_data.get("system_prompt", "")
    user_prompt = input_data.get("user_prompt", "")
    model = input_data.get("model", "gpt-4")
    temperature = input_data.get("temperature", 0.7)
    max_tokens = input_data.get("max_tokens")

    # Azure-specific configuration
    api_key = input_data.get("api_key") or (
        settings.AZURE_OPENAI_API_KEY if hasattr(settings, 'AZURE_OPENAI_API_KEY') else None
    )
    endpoint = input_data.get("azure_endpoint") or (
        settings.AZURE_OPENAI_ENDPOINT if hasattr(settings, 'AZURE_OPENAI_ENDPOINT') else None
    )
    deployment = input_data.get("azure_deployment") or model
    api_version = input_data.get("azure_api_version", "2024-02-15-preview")

    if not api_key:
        raise AgentError("Azure OpenAI API key is required")

    if not endpoint:
        raise AgentError("Azure OpenAI endpoint is required")

    # Prepare messages
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    # Prepare request payload
    payload = {
        "messages": messages,
        "temperature": temperature,
    }

    if max_tokens:
        payload["max_tokens"] = max_tokens

    # Build Azure OpenAI URL
    url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={api_version}"

    # Call Azure OpenAI API
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers={
                    "api-key": api_key,
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=120.0,
            )

            response.raise_for_status()
            data = response.json()

        # Extract response
        content = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})

        return {
            "content": content,
            "tokens": {
                "prompt": usage.get("prompt_tokens", 0),
                "completion": usage.get("completion_tokens", 0),
                "total": usage.get("total_tokens", 0),
            },
            "model": deployment,
            "provider": "azure-openai",
            "finish_reason": data["choices"][0].get("finish_reason"),
        }

    except httpx.HTTPStatusError as e:
        logger.error(
            "azure_openai_request_failed",
            block_id=block["id"],
            status_code=e.response.status_code,
            error=e.response.text,
        )
        raise AgentError(f"Azure OpenAI request failed: {e.response.text}") from e


async def _execute_anthropic(input_data: dict[str, Any], block: dict[str, Any]) -> dict[str, Any]:
    """Execute Anthropic Claude request"""

    system_prompt = input_data.get("system_prompt", "")
    user_prompt = input_data.get("user_prompt", "")
    model = input_data.get("model", "claude-3-5-sonnet-20241022")
    temperature = input_data.get("temperature", 0.7)
    max_tokens = input_data.get("max_tokens", 4096)
    api_key = input_data.get("api_key") or (
        settings.ANTHROPIC_API_KEY if hasattr(settings, 'ANTHROPIC_API_KEY') else None
    )

    if not api_key:
        raise AgentError("Anthropic API key is required")

    # Prepare request payload
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [{"role": "user", "content": user_prompt}],
    }

    if system_prompt:
        payload["system"] = system_prompt

    # Call Anthropic API
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=120.0,
            )

            response.raise_for_status()
            data = response.json()

        # Extract response
        content = data["content"][0]["text"]
        usage = data.get("usage", {})

        return {
            "content": content,
            "tokens": {
                "prompt": usage.get("input_tokens", 0),
                "completion": usage.get("output_tokens", 0),
                "total": usage.get("input_tokens", 0) + usage.get("output_tokens", 0),
            },
            "model": model,
            "provider": "anthropic",
            "finish_reason": data.get("stop_reason"),
        }

    except httpx.HTTPStatusError as e:
        logger.error(
            "anthropic_request_failed",
            block_id=block["id"],
            status_code=e.response.status_code,
            error=e.response.text,
        )
        raise AgentError(f"Anthropic request failed: {e.response.text}") from e


async def _execute_groq(input_data: dict[str, Any], block: dict[str, Any]) -> dict[str, Any]:
    """Execute Groq request (fast inference)"""

    system_prompt = input_data.get("system_prompt", "")
    user_prompt = input_data.get("user_prompt", "")
    model = input_data.get("model", "llama-3.1-70b-versatile")
    temperature = input_data.get("temperature", 0.7)
    max_tokens = input_data.get("max_tokens")
    api_key = input_data.get("api_key") or (
        settings.GROQ_API_KEY if hasattr(settings, 'GROQ_API_KEY') else None
    )

    if not api_key:
        raise AgentError("Groq API key is required")

    # Prepare messages
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    # Prepare request payload
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    if max_tokens:
        payload["max_tokens"] = max_tokens

    # Call Groq API (OpenAI-compatible)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=60.0,
            )

            response.raise_for_status()
            data = response.json()

        # Extract response
        content = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})

        return {
            "content": content,
            "tokens": {
                "prompt": usage.get("prompt_tokens", 0),
                "completion": usage.get("completion_tokens", 0),
                "total": usage.get("total_tokens", 0),
            },
            "model": model,
            "provider": "groq",
            "finish_reason": data["choices"][0].get("finish_reason"),
        }

    except httpx.HTTPStatusError as e:
        logger.error(
            "groq_request_failed",
            block_id=block["id"],
            status_code=e.response.status_code,
            error=e.response.text,
        )
        raise AgentError(f"Groq request failed: {e.response.text}") from e


async def _execute_google(input_data: dict[str, Any], block: dict[str, Any]) -> dict[str, Any]:
    """Execute Google Gemini request"""

    user_prompt = input_data.get("user_prompt", "")
    model = input_data.get("model", "gemini-pro")
    temperature = input_data.get("temperature", 0.7)
    api_key = input_data.get("api_key") or (
        settings.GOOGLE_API_KEY if hasattr(settings, 'GOOGLE_API_KEY') else None
    )

    if not api_key:
        raise AgentError("Google API key is required")

    # Prepare request payload
    payload = {
        "contents": [{"parts": [{"text": user_prompt}]}],
        "generationConfig": {
            "temperature": temperature,
        },
    }

    # Call Google Gemini API
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}",
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=120.0,
            )

            response.raise_for_status()
            data = response.json()

        # Extract response
        content = data["candidates"][0]["content"]["parts"][0]["text"]

        return {
            "content": content,
            "tokens": {
                "prompt": 0,  # Google doesn't provide token counts in response
                "completion": 0,
                "total": 0,
            },
            "model": model,
            "provider": "google",
            "finish_reason": data["candidates"][0].get("finishReason"),
        }

    except httpx.HTTPStatusError as e:
        logger.error(
            "google_request_failed",
            block_id=block["id"],
            status_code=e.response.status_code,
            error=e.response.text,
        )
        raise AgentError(f"Google Gemini request failed: {e.response.text}") from e
