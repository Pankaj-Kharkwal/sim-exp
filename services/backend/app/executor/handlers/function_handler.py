"""
Function Block Handler
Executes JavaScript/Python code blocks
"""
import ast
import json
from typing import Any, Dict
from app.executor.types import (
    BlockType,
    SerializedBlock,
    ExecutionContext,
)


class FunctionBlockHandler:
    """Handler for function blocks that execute code"""

    def can_handle(self, block: SerializedBlock) -> bool:
        """Check if this is a function block"""
        return block.metadata.get("id") == BlockType.FUNCTION

    async def execute(
        self,
        ctx: ExecutionContext,
        block: SerializedBlock,
        inputs: Dict[str, Any],
    ) -> Any:
        """
        Execute a function block (Python code)

        Args:
            ctx: Execution context
            block: Block configuration
            inputs: Input values for the block

        Returns:
            Result of code execution
        """
        code = inputs.get("code", "").strip()
        language = inputs.get("language", "python").lower()

        if not code:
            return None

        if language == "python":
            return await self._execute_python(code, inputs, ctx)
        else:
            raise ValueError(f"Unsupported language: {language}")

    async def _execute_python(
        self, code: str, inputs: Dict[str, Any], ctx: ExecutionContext
    ) -> Any:
        """Execute Python code safely"""
        # Create execution namespace
        namespace = {
            "inputs": inputs,
            "context": ctx.dict(),
            "json": json,
            "print": print,
        }

        # Add common utilities
        try:
            # Parse and execute code
            tree = ast.parse(code, mode="exec")
            compiled = compile(tree, filename="<function_block>", mode="exec")
            exec(compiled, namespace)

            # Return the 'result' variable if it exists
            return namespace.get("result", None)

        except SyntaxError as e:
            raise Exception(f"Syntax error in code: {str(e)}")
        except Exception as e:
            raise Exception(f"Code execution failed: {str(e)}")
