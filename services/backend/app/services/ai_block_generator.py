"""
AI-Powered Dynamic Block Generation Service

Uses LangGraph + PydanticAI + Azure OpenAI to generate custom workflow blocks on-the-fly
based on user chat conversations with the copilot.

Architecture:
1. User chats with copilot: "I need a block that sends data to my custom API"
2. LangGraph workflow analyzes intent and generates block structure
3. PydanticAI validates and structures the output
4. Block is created dynamically and added to user's workspace
5. Block executor is generated with proper type safety
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import json

from langgraph.graph import StateGraph, END
from openai import AzureOpenAI

from app.core.config import settings
from app.core.logging import get_logger
from app.executor.blocks.registry import get_all_blocks, BLOCK_REGISTRY

logger = get_logger(__name__)


# ============================================================================
# Pydantic Models for Structured Block Generation
# ============================================================================

class BlockInput(BaseModel):
    """Block input field definition"""
    name: str = Field(..., description="Input field name (camelCase)")
    type: str = Field(..., description="Data type: string, number, boolean, json, array")
    description: str = Field(..., description="Human-readable description")
    required: bool = Field(default=False, description="Whether this field is required")
    default: Optional[Any] = Field(default=None, description="Default value if any")


class BlockOutput(BaseModel):
    """Block output field definition"""
    name: str = Field(..., description="Output field name (camelCase)")
    type: str = Field(..., description="Data type: string, number, boolean, json, array")
    description: str = Field(..., description="Human-readable description")


class BlockParameter(BaseModel):
    """Block configuration parameter (for UI)"""
    id: str = Field(..., description="Parameter ID (camelCase)")
    title: str = Field(..., description="Display title")
    type: str = Field(..., description="UI component: short-input, long-input, dropdown, code, etc.")
    layout: str = Field(default="full", description="Layout: full or half")
    placeholder: Optional[str] = Field(default=None, description="Placeholder text")
    required: bool = Field(default=False, description="Whether required")
    options: Optional[List[Dict[str, str]]] = Field(default=None, description="For dropdowns")


class GeneratedBlock(BaseModel):
    """Complete generated block structure"""
    type: str = Field(..., description="Block type identifier (lowercase_snake_case)")
    name: str = Field(..., description="Display name")
    description: str = Field(..., description="Short description")
    long_description: str = Field(..., description="Detailed description with examples")
    category: str = Field(default="custom", description="Block category")

    # UI Configuration
    parameters: List[BlockParameter] = Field(..., description="Block parameters for UI")

    # Data Schema
    inputs: List[BlockInput] = Field(..., description="Input schema")
    outputs: List[BlockOutput] = Field(..., description="Output schema")

    # Execution Logic (Python code)
    executor_code: str = Field(..., description="Python function code for execution")

    # Tools/APIs used
    tools: List[str] = Field(default_factory=list, description="Tool IDs this block uses")


# ============================================================================
# LangGraph State for Block Generation Workflow
# ============================================================================

class BlockGenerationState(BaseModel):
    """State for LangGraph workflow"""
    user_request: str = Field(..., description="User's original chat message")
    conversation_history: List[Dict[str, str]] = Field(default_factory=list)

    # Analysis results
    intent: Optional[str] = None  # API call, data transform, notification, etc.
    requirements: Optional[Dict[str, Any]] = None  # Extracted requirements
    similar_blocks: Optional[List[Dict[str, Any]]] = None  # Existing similar blocks

    # Generation
    generated_block: Optional[GeneratedBlock] = None
    validation_errors: Optional[List[str]] = None

    # Final
    status: str = "pending"  # pending, generating, validating, completed, failed
    error: Optional[str] = None


# ============================================================================
# AI Block Generator Service
# ============================================================================

class AIBlockGenerator:
    """Service for generating blocks using AI"""

    def __init__(self):
        self.client = AzureOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        )
        self.model = settings.AZURE_OPENAI_DEPLOYMENT_CHAT

        # Build LangGraph workflow
        self.workflow = self._build_workflow()

    def _build_workflow(self) -> StateGraph:
        """Build LangGraph workflow for block generation"""

        workflow = StateGraph(BlockGenerationState)

        # Define nodes
        workflow.add_node("analyze_intent", self._analyze_intent)
        workflow.add_node("extract_requirements", self._extract_requirements)
        workflow.add_node("find_similar_blocks", self._find_similar_blocks)
        workflow.add_node("generate_block_structure", self._generate_block_structure)
        workflow.add_node("generate_executor_code", self._generate_executor_code)
        workflow.add_node("validate_block", self._validate_block)

        # Define edges
        workflow.set_entry_point("analyze_intent")
        workflow.add_edge("analyze_intent", "extract_requirements")
        workflow.add_edge("extract_requirements", "find_similar_blocks")
        workflow.add_edge("find_similar_blocks", "generate_block_structure")
        workflow.add_edge("generate_block_structure", "generate_executor_code")
        workflow.add_edge("generate_executor_code", "validate_block")
        workflow.add_edge("validate_block", END)

        return workflow.compile()

    async def generate_block(
        self,
        user_request: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> GeneratedBlock:
        """
        Generate a custom block based on user request

        Args:
            user_request: User's chat message describing what they need
            conversation_history: Previous chat messages for context

        Returns:
            GeneratedBlock with full configuration and executor code
        """
        logger.info("ai_block_generation_started", request=user_request)

        # Initialize state
        state = BlockGenerationState(
            user_request=user_request,
            conversation_history=conversation_history or []
        )

        # Run LangGraph workflow
        result = await self.workflow.ainvoke(state)

        if result["status"] == "failed":
            raise ValueError(f"Block generation failed: {result['error']}")

        generated_block = result["generated_block"]
        logger.info("ai_block_generated", block_type=generated_block.type)

        return generated_block

    async def _analyze_intent(self, state: BlockGenerationState) -> BlockGenerationState:
        """Analyze user intent to determine block type"""

        prompt = f"""Analyze this user request and determine their intent for a workflow block.

User Request: {state.user_request}

Conversation History:
{json.dumps(state.conversation_history, indent=2)}

Determine:
1. What type of block do they need? (API call, data transformation, notification, integration, etc.)
2. What's the primary purpose?
3. What category does it fit? (integrations, data, ai, communication, etc.)

Return JSON:
{{
    "intent_type": "string",
    "purpose": "string",
    "category": "string",
    "confidence": 0.0-1.0
}}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=1.0
        )

        intent_data = json.loads(response.choices[0].message.content)
        state.intent = intent_data["intent_type"]

        logger.info("intent_analyzed", intent=state.intent)
        return state

    async def _extract_requirements(self, state: BlockGenerationState) -> BlockGenerationState:
        """Extract specific requirements from user request"""

        prompt = f"""Extract specific requirements for building this workflow block.

User Request: {state.user_request}
Intent: {state.intent}

Extract:
1. Required inputs (what data does the block need?)
2. Expected outputs (what should it return?)
3. Configuration parameters (what can user configure?)
4. Any specific APIs, services, or tools mentioned
5. Example use case

Return detailed JSON structure with all requirements.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=1.0
        )

        state.requirements = json.loads(response.choices[0].message.content)
        logger.info("requirements_extracted", requirements=state.requirements)
        return state

    async def _find_similar_blocks(self, state: BlockGenerationState) -> BlockGenerationState:
        """Find existing blocks similar to what user wants"""

        all_blocks = get_all_blocks()

        # Use AI to find similar blocks
        blocks_summary = [
            {
                "type": b["type"],
                "name": b["name"],
                "description": b.get("description", ""),
                "tools": b.get("tools", [])
            }
            for b in all_blocks
        ]

        prompt = f"""Given this block request, find the 3 most similar existing blocks that could serve as examples.

Request: {state.user_request}
Requirements: {json.dumps(state.requirements, indent=2)}

Available Blocks:
{json.dumps(blocks_summary, indent=2)}

Return JSON array of top 3 most relevant blocks with reasoning.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=1.0
        )

        result = json.loads(response.choices[0].message.content)
        state.similar_blocks = result.get("similar_blocks", [])
        logger.info("similar_blocks_found", count=len(state.similar_blocks))
        return state

    async def _generate_block_structure(self, state: BlockGenerationState) -> BlockGenerationState:
        """Generate complete block structure (metadata, UI, schema)"""

        examples = "\n\n".join([
            f"Example Block: {b['name']}\n{json.dumps(b, indent=2)}"
            for b in (state.similar_blocks or [])[:2]
        ])

        prompt = f"""Generate a complete workflow block structure.

User Request: {state.user_request}
Requirements: {json.dumps(state.requirements, indent=2)}

Reference Examples:
{examples}

Generate a block following this exact schema:
{{
    "type": "unique_block_type_name",
    "name": "Display Name",
    "description": "Short description",
    "long_description": "Detailed description with examples",
    "category": "custom",
    "parameters": [
        {{
            "id": "fieldName",
            "title": "Field Title",
            "type": "short-input|long-input|dropdown|code|etc",
            "layout": "full|half",
            "placeholder": "Optional placeholder",
            "required": true|false
        }}
    ],
    "inputs": [
        {{
            "name": "inputName",
            "type": "string|number|boolean|json|array",
            "description": "Input description",
            "required": true|false
        }}
    ],
    "outputs": [
        {{
            "name": "outputName",
            "type": "string|number|boolean|json|array",
            "description": "Output description"
        }}
    ],
    "tools": ["tool_id_if_any"]
}}

Be thorough and follow the examples closely!
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=1.0
        )

        block_structure = json.loads(response.choices[0].message.content)

        # We'll add executor_code in next step
        block_structure["executor_code"] = ""

        # Validate with Pydantic
        try:
            state.generated_block = GeneratedBlock(**block_structure)
            logger.info("block_structure_generated", block_type=state.generated_block.type)
        except Exception as e:
            state.validation_errors = [str(e)]
            logger.error("block_structure_invalid", error=str(e))

        return state

    async def _generate_executor_code(self, state: BlockGenerationState) -> BlockGenerationState:
        """Generate Python executor function for the block"""

        if not state.generated_block:
            return state

        block = state.generated_block

        prompt = f"""Generate Python async executor function for this workflow block.

Block Type: {block.type}
Description: {block.description}
Inputs: {json.dumps([i.dict() for i in block.inputs], indent=2)}
Outputs: {json.dumps([o.dict() for o in block.outputs], indent=2)}
Requirements: {json.dumps(state.requirements, indent=2)}

Generate a complete async function following this template:

```python
async def execute_{block.type}_block(
    block: dict[str, Any],
    input_data: dict[str, Any],
    state: WorkflowState
) -> dict[str, Any]:
    \"\"\"Execute {block.name} block\"\"\"

    logger.info("{block.type}_block_executing", block_id=block["id"])

    # Extract inputs
    # TODO: Extract each input field

    # Execute logic
    # TODO: Implement the actual block logic

    # Return outputs
    return {{
        # TODO: Return expected outputs
    }}
```

Generate ONLY the Python function code, fully implemented with error handling.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=1.0
        )

        executor_code = response.choices[0].message.content

        # Clean up markdown code blocks if present
        if "```python" in executor_code:
            executor_code = executor_code.split("```python")[1].split("```")[0].strip()

        block.executor_code = executor_code
        logger.info("executor_code_generated", lines=len(executor_code.split("\n")))

        return state

    async def _validate_block(self, state: BlockGenerationState) -> BlockGenerationState:
        """Final validation of generated block"""

        if not state.generated_block:
            state.status = "failed"
            state.error = "No block generated"
            return state

        block = state.generated_block
        errors = []

        # Validate required fields
        if not block.type or not block.name:
            errors.append("Missing type or name")

        if not block.inputs and not block.outputs:
            errors.append("Block must have inputs or outputs")

        if not block.executor_code or len(block.executor_code) < 100:
            errors.append("Executor code is missing or too short")

        # Validate executor code syntax
        try:
            compile(block.executor_code, "<string>", "exec")
        except SyntaxError as e:
            errors.append(f"Executor code has syntax error: {e}")

        if errors:
            state.status = "failed"
            state.error = "; ".join(errors)
            state.validation_errors = errors
        else:
            state.status = "completed"

        logger.info("block_validation_completed", status=state.status, errors=errors)
        return state


# ============================================================================
# Global instance
# ============================================================================

ai_block_generator = AIBlockGenerator()
