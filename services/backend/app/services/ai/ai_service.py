"""
Base AI Service for Block Code Generation

Adapted from Pankh POC v4 with Azure OpenAI and Anthropic support.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, ValidationError
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

logger = logging.getLogger(__name__)


class RequirementAnalysis(BaseModel):
    """Analysis of user requirement for block generation"""
    intent: str
    block_type: str
    parameters: Dict[str, Any]
    description: str
    category: str


class BlockCode(BaseModel):
    """Generated block code with manifest"""
    block_type: str
    name: str
    description: str
    category: str
    parameters: Dict[str, Any]
    code: str
    manifest: Dict[str, Any]


class TokenUsage(BaseModel):
    """Token usage tracking"""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class AIService:
    """
    AI Service for generating workflow blocks

    Supports:
    - Azure OpenAI (gpt-4, gpt-4-turbo, gpt-3.5-turbo)
    - OpenAI (with API key)
    - Anthropic Claude (claude-3-opus, claude-3-sonnet)
    """

    _RETRY_TEMPERATURES = (0.7, 0.8, 0.9)

    def __init__(
        self,
        provider: str = "azure-openai",
        model: str = "gpt-4",
        api_key: Optional[str] = None,
        endpoint: Optional[str] = None,
    ):
        """
        Initialize AI Service

        Args:
            provider: "azure-openai", "openai", or "anthropic"
            model: Model name
            api_key: API key (falls back to env vars)
            endpoint: Endpoint URL for Azure OpenAI
        """
        self.provider = provider
        self.model = model
        self.client = None
        self._block_code_schema = self._create_block_code_schema()
        self._initialize_client(api_key, endpoint)

    @staticmethod
    def _create_block_code_schema() -> Dict[str, Any]:
        """JSON schema for block code response"""
        return {
            "type": "object",
            "properties": {
                "block_type": {"type": "string"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "category": {"type": "string"},
                "parameters": {"type": "object", "additionalProperties": True},
                "code": {"type": "string"},
                "manifest": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "summary": {"type": "string"},
                        "category": {"type": "string"},
                        "config_schema": {"type": "object"},
                    },
                    "required": ["name", "category"],
                    "additionalProperties": True,
                },
            },
            "required": [
                "block_type",
                "name",
                "description",
                "category",
                "parameters",
                "code",
                "manifest",
            ],
            "additionalProperties": False,
        }

    def _initialize_client(self, api_key: Optional[str], endpoint: Optional[str]):
        """Initialize the appropriate AI client"""
        try:
            if self.provider == "azure-openai":
                key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
                ep = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
                version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

                if not key or not ep:
                    logger.warning("Azure OpenAI credentials missing")
                    return

                from openai import AsyncAzureOpenAI
                self.client = AsyncAzureOpenAI(
                    api_key=key,
                    api_version=version,
                    azure_endpoint=ep
                )
                logger.info(f"✅ Azure OpenAI client initialized: {self.model}")

            elif self.provider == "openai":
                key = api_key or os.getenv("OPENAI_API_KEY")

                if not key:
                    logger.warning("OpenAI API key missing")
                    return

                self.client = AsyncOpenAI(api_key=key)
                logger.info(f"✅ OpenAI client initialized: {self.model}")

            elif self.provider == "anthropic":
                key = api_key or os.getenv("ANTHROPIC_API_KEY")

                if not key:
                    logger.warning("Anthropic API key missing")
                    return

                self.client = AsyncAnthropic(api_key=key)
                logger.info(f"✅ Anthropic client initialized: {self.model}")

            else:
                logger.error(f"Unknown provider: {self.provider}")

        except Exception as e:
            logger.error(f"Failed to initialize AI client: {e}", exc_info=True)
            self.client = None

    async def analyze_requirement(self, requirement: str) -> RequirementAnalysis:
        """Analyze user requirement and extract block parameters"""
        if not self.client:
            return RequirementAnalysis(
                intent="data_processing",
                block_type="custom_block",
                parameters={},
                description=requirement,
                category="utility"
            )

        try:
            system_prompt = """You are an expert in workflow automation. Analyze the user requirement and suggest:
1. The intent (what they want to accomplish)
2. A unique block_type identifier (snake_case)
3. Required parameters with default values
4. A clear description
5. The category: core, data_transformation, python_package, simple_api, complex_oauth, database, ai_service, communication, storage

Respond in JSON format matching the RequirementAnalysis schema."""

            if self.provider == "anthropic":
                response = await self.client.messages.create(
                    model=self.model,
                    max_tokens=2000,
                    system=system_prompt,
                    messages=[{"role": "user", "content": requirement}]
                )
                content = response.content[0].text
            else:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": requirement}
                    ],
                    max_tokens=2000,
                    temperature=0.7
                )
                content = response.choices[0].message.content

            result = json.loads(content)
            return RequirementAnalysis(**result)

        except Exception as e:
            logger.error(f"Error analyzing requirement: {e}", exc_info=True)
            return RequirementAnalysis(
                intent="general_task",
                block_type="custom_block",
                parameters={},
                description=requirement,
                category="utility"
            )

    async def generate_block_code(
        self,
        analysis: RequirementAnalysis
    ) -> tuple[BlockCode, Optional[TokenUsage]]:
        """Generate complete block code from requirement analysis"""
        if not self.client:
            return self._fallback_block_code(analysis), None

        system_prompt = """You are an expert Python developer building production-ready workflow automation blocks.
Write robust, well-tested code that handles configuration validation, logging, and error handling.

IMPORTANT: You MUST include ALL required fields in your response:
- block_type: string (e.g., 'http_get', 'gdrive_list_files')
- name: string (human-readable name)
- description: string (what the block does)
- category: string (e.g., 'utility', 'storage', 'communication')
- parameters: object (configuration parameters with defaults)
- code: string (complete Python code with async def execute(runtime, **config))
- manifest: object (with name, summary/description, category, config_schema)

The code MUST:
1. Be a complete async Python function named 'execute'
2. Accept parameters: execute(runtime, **config)
3. Return a dictionary with results
4. Include proper error handling and logging
5. Use type hints

Return ONLY valid JSON matching the BlockCode schema."""

        user_prompt = f"""Create a workflow block for: {analysis.description}

Requirements:
- block_type: {analysis.block_type}
- category: {analysis.category}
- parameters: {json.dumps(analysis.parameters, indent=2)}

Implement async def execute(runtime, **config) that returns a dictionary of results.
Ensure the manifest config_schema matches the parameters."""

        last_error = None

        for attempt, temperature in enumerate(self._RETRY_TEMPERATURES, start=1):
            try:
                if self.provider == "anthropic":
                    response = await self.client.messages.create(
                        model=self.model,
                        max_tokens=8000,
                        temperature=temperature,
                        system=system_prompt,
                        messages=[{"role": "user", "content": user_prompt}]
                    )
                    content = response.content[0].text
                    usage = TokenUsage(
                        prompt_tokens=response.usage.input_tokens,
                        completion_tokens=response.usage.output_tokens,
                        total_tokens=response.usage.input_tokens + response.usage.output_tokens
                    )
                else:
                    response = await self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        max_tokens=8000,
                        temperature=temperature,
                        response_format={"type": "json_object"}
                    )
                    content = response.choices[0].message.content
                    usage = TokenUsage(
                        prompt_tokens=response.usage.prompt_tokens,
                        completion_tokens=response.usage.completion_tokens,
                        total_tokens=response.usage.total_tokens
                    )

                # Parse and validate
                payload = self._extract_block_payload(content)
                validated = BlockCode(**payload)

                logger.info(f"✅ Block code generated on attempt {attempt}")
                return validated, usage

            except (json.JSONDecodeError, ValidationError, ValueError) as e:
                logger.warning(f"Attempt {attempt} failed validation: {e}")
                last_error = e
                continue
            except Exception as e:
                logger.error(f"Attempt {attempt} failed: {e}", exc_info=True)
                last_error = e
                continue

        logger.error(f"All {len(self._RETRY_TEMPERATURES)} attempts failed")
        return self._fallback_block_code(analysis), None

    @staticmethod
    def _extract_block_payload(content: str) -> Dict[str, Any]:
        """Extract JSON payload from response, handling markdown code blocks"""
        text = content.strip()

        # Remove markdown code blocks
        if text.startswith("```"):
            lines = [line for line in text.splitlines() if not line.strip().startswith("```")]
            text = "\n".join(lines).strip()

        # Extract JSON object
        if not text.startswith("{"):
            start_idx = text.find("{")
            end_idx = text.rfind("}")
            if start_idx == -1 or end_idx == -1:
                raise ValueError("No JSON object found in response")
            text = text[start_idx:end_idx + 1]

        return json.loads(text)

    @staticmethod
    def _fallback_block_code(analysis: RequirementAnalysis) -> BlockCode:
        """Create fallback block when AI generation fails"""
        return BlockCode(
            block_type=analysis.block_type,
            name=analysis.description,
            description=analysis.description,
            category=analysis.category,
            parameters=analysis.parameters,
            code="""async def execute(runtime, **config):
    \"\"\"Fallback block implementation\"\"\"
    import logging
    logger = logging.getLogger(__name__)

    logger.info(f"Executing fallback block with config: {config}")

    return {
        "success": True,
        "message": "Fallback block executed",
        "config": config
    }
""",
            manifest={
                "name": analysis.description,
                "summary": analysis.description,
                "category": analysis.category,
                "config_schema": {
                    "type": "object",
                    "properties": analysis.parameters,
                    "additionalProperties": True
                }
            }
        )


# Factory function
def get_ai_service(
    provider: str = "azure-openai",
    model: str = "gpt-4"
) -> AIService:
    """Get configured AI service instance"""
    return AIService(provider=provider, model=model)
