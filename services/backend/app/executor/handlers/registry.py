"""
Block Handler Registry
Manages all block handlers
"""
from typing import List, Optional
from app.executor.types import SerializedBlock, BlockHandler
from app.executor.handlers.api_handler import ApiBlockHandler
from app.executor.handlers.function_handler import FunctionBlockHandler
from app.executor.handlers.openai_handler import OpenAIBlockHandler


class HandlerRegistry:
    """Registry for all block handlers"""

    def __init__(self):
        self.handlers: List[BlockHandler] = [
            ApiBlockHandler(),
            FunctionBlockHandler(),
            OpenAIBlockHandler(),
            # TODO: Add all 90+ handlers
        ]

    def get_handler(self, block: SerializedBlock) -> Optional[BlockHandler]:
        """
        Get the appropriate handler for a block

        Args:
            block: Block to handle

        Returns:
            Handler instance or None if no handler found
        """
        for handler in self.handlers:
            if handler.can_handle(block):
                return handler
        return None

    def register_handler(self, handler: BlockHandler):
        """Register a new handler"""
        self.handlers.append(handler)


# Global registry instance
registry = HandlerRegistry()
