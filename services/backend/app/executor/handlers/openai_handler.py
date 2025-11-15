"""
OpenAI Block Handler
Handles OpenAI API calls
"""
from typing import Any, Dict, List
from openai import AsyncOpenAI
from app.executor.types import (
    BlockType,
    SerializedBlock,
    ExecutionContext,
)
from app.core.config import settings


class OpenAIBlockHandler:
    """Handler for OpenAI blocks"""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    def can_handle(self, block: SerializedBlock) -> bool:
        """Check if this is an OpenAI block"""
        return block.metadata.get("id") == BlockType.OPENAI

    async def execute(
        self,
        ctx: ExecutionContext,
        block: SerializedBlock,
        inputs: Dict[str, Any],
    ) -> Any:
        """
        Execute an OpenAI API call

        Args:
            ctx: Execution context
            block: Block configuration
            inputs: Input values for the block

        Returns:
            OpenAI API response
        """
        model = inputs.get("model", "gpt-4")
        messages = inputs.get("messages", [])
        temperature = inputs.get("temperature", 0.7)
        max_tokens = inputs.get("max_tokens")
        tools = inputs.get("tools")
        response_format = inputs.get("response_format")

        # Ensure messages is a list
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        elif not isinstance(messages, list):
            messages = []

        # Make API call
        try:
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

            response = await self.client.chat.completions.create(**kwargs)

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
            if message.tool_calls:
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

            return result

        except Exception as e:
            raise Exception(f"OpenAI API call failed: {str(e)}")
