"""OpenAI block executor - AI model interactions"""

from typing import Any, Optional
import os
from openai import AsyncOpenAI

from app.core.logging import get_logger
from app.core.config import settings
from app.executor.state import WorkflowState

logger = get_logger(__name__)


async def execute_openai_block(
    block: dict[str, Any], input_data: dict[str, Any], state: WorkflowState
) -> dict[str, Any]:
    """
    Execute an OpenAI block for chat completions, embeddings, or other AI tasks

    Supports:
    - Chat completions (GPT-4, GPT-3.5, etc.)
    - Embeddings generation
    - Image generation (DALL-E)
    - Text-to-speech
    - Speech-to-text (Whisper)
    """

    logger.info("openai_block_executing", block_id=block["id"], operation=input_data.get("operation", "chat"))

    # Initialize OpenAI client
    api_key = input_data.get("api_key") or settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or provide in block config.")

    client = AsyncOpenAI(api_key=api_key)

    # Determine operation type
    operation = input_data.get("operation", "chat").lower()

    try:
        if operation == "chat" or operation == "completion":
            result = await _execute_chat_completion(client, input_data)
        elif operation == "embeddings" or operation == "embedding":
            result = await _execute_embeddings(client, input_data)
        elif operation == "image" or operation == "dalle":
            result = await _execute_image_generation(client, input_data)
        elif operation == "tts" or operation == "text-to-speech":
            result = await _execute_text_to_speech(client, input_data)
        elif operation == "transcription" or operation == "whisper":
            result = await _execute_transcription(client, input_data)
        else:
            raise ValueError(f"Unknown operation type: {operation}")

        logger.info("openai_block_completed", block_id=block["id"], operation=operation)
        return {"success": True, **result}

    except Exception as e:
        logger.error("openai_block_failed", block_id=block["id"], error=str(e))
        raise


async def _execute_chat_completion(client: AsyncOpenAI, input_data: dict[str, Any]) -> dict[str, Any]:
    """Execute OpenAI chat completion"""

    model = input_data.get("model", "gpt-4")
    messages = input_data.get("messages", [])

    # If messages is a string, convert to chat format
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]
    elif not isinstance(messages, list):
        messages = [{"role": "user", "content": str(messages)}]

    # Optional parameters
    temperature = input_data.get("temperature", 0.7)
    max_tokens = input_data.get("max_tokens")
    tools = input_data.get("tools")
    response_format = input_data.get("response_format")
    top_p = input_data.get("top_p")
    frequency_penalty = input_data.get("frequency_penalty")
    presence_penalty = input_data.get("presence_penalty")
    stream = input_data.get("stream", False)

    # Build request kwargs
    kwargs = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    if max_tokens:
        kwargs["max_tokens"] = max_tokens
    if tools:
        kwargs["tools"] = tools
    if response_format:
        kwargs["response_format"] = response_format
    if top_p is not None:
        kwargs["top_p"] = top_p
    if frequency_penalty is not None:
        kwargs["frequency_penalty"] = frequency_penalty
    if presence_penalty is not None:
        kwargs["presence_penalty"] = presence_penalty
    if stream:
        kwargs["stream"] = stream

    # Make API call
    response = await client.chat.completions.create(**kwargs)

    # Extract response
    message = response.choices[0].message
    result = {
        "content": message.content,
        "role": message.role,
        "model": response.model,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
    }

    # Include tool calls if present
    if hasattr(message, "tool_calls") and message.tool_calls:
        result["tool_calls"] = [
            {
                "id": tc.id,
                "type": tc.type,
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments,
                },
            }
            for tc in message.tool_calls
        ]

    # Include function call if present (legacy)
    if hasattr(message, "function_call") and message.function_call:
        result["function_call"] = {
            "name": message.function_call.name,
            "arguments": message.function_call.arguments,
        }

    return result


async def _execute_embeddings(client: AsyncOpenAI, input_data: dict[str, Any]) -> dict[str, Any]:
    """Execute OpenAI embeddings generation"""

    model = input_data.get("model", "text-embedding-3-small")
    text_input = input_data.get("input") or input_data.get("text")

    if not text_input:
        raise ValueError("Text input is required for embeddings")

    # Convert to list if string
    if isinstance(text_input, str):
        text_input = [text_input]

    response = await client.embeddings.create(
        model=model,
        input=text_input,
    )

    return {
        "embeddings": [item.embedding for item in response.data],
        "model": response.model,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "total_tokens": response.usage.total_tokens,
        },
    }


async def _execute_image_generation(client: AsyncOpenAI, input_data: dict[str, Any]) -> dict[str, Any]:
    """Execute OpenAI image generation (DALL-E)"""

    prompt = input_data.get("prompt")
    if not prompt:
        raise ValueError("Prompt is required for image generation")

    model = input_data.get("model", "dall-e-3")
    size = input_data.get("size", "1024x1024")
    quality = input_data.get("quality", "standard")
    n = input_data.get("n", 1)

    response = await client.images.generate(
        model=model,
        prompt=prompt,
        size=size,
        quality=quality,
        n=n,
    )

    return {
        "images": [
            {
                "url": image.url,
                "revised_prompt": getattr(image, "revised_prompt", None),
            }
            for image in response.data
        ],
    }


async def _execute_text_to_speech(client: AsyncOpenAI, input_data: dict[str, Any]) -> dict[str, Any]:
    """Execute OpenAI text-to-speech"""

    text = input_data.get("input") or input_data.get("text")
    if not text:
        raise ValueError("Text input is required for text-to-speech")

    model = input_data.get("model", "tts-1")
    voice = input_data.get("voice", "alloy")

    response = await client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
    )

    # Return audio content as bytes
    audio_content = await response.aread()

    return {
        "audio": audio_content,
        "format": "mp3",
        "model": model,
        "voice": voice,
    }


async def _execute_transcription(client: AsyncOpenAI, input_data: dict[str, Any]) -> dict[str, Any]:
    """Execute OpenAI audio transcription (Whisper)"""

    audio_file = input_data.get("file") or input_data.get("audio")
    if not audio_file:
        raise ValueError("Audio file is required for transcription")

    model = input_data.get("model", "whisper-1")
    language = input_data.get("language")
    prompt = input_data.get("prompt")
    response_format = input_data.get("response_format", "json")
    temperature = input_data.get("temperature", 0)

    kwargs = {
        "model": model,
        "file": audio_file,
        "response_format": response_format,
        "temperature": temperature,
    }

    if language:
        kwargs["language"] = language
    if prompt:
        kwargs["prompt"] = prompt

    response = await client.audio.transcriptions.create(**kwargs)

    return {
        "text": response.text if hasattr(response, "text") else response,
        "model": model,
    }
