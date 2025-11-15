"""
Enhanced AI Block Generator with Deep Research Integration

This service extends the base AI service with:
1. Deep research capabilities for complex APIs
2. Credential handling integration
3. Advanced validation
4. Block category-specific generation strategies
5. Self-healing test execution
6. Automatic block registration
"""

import logging
import time
from typing import Dict, Any, List, Optional
from enum import Enum
from pydantic import BaseModel, Field

from .ai_service import AIService, RequirementAnalysis
from .similarity_service import BlockSimilarityService, check_and_use_similar_blocks
from .test_execution import get_test_execution_service
from .self_healing import get_self_healing_service

logger = logging.getLogger(__name__)


class BlockCategory(str, Enum):
    """Block category types"""
    CORE = "core"
    DATA_TRANSFORMATION = "data_transformation"
    PYTHON_PACKAGE = "python_package"
    SIMPLE_API = "simple_api"
    COMPLEX_OAUTH = "complex_oauth"
    DATABASE = "database"
    AI_SERVICE = "ai_service"
    COMMUNICATION = "communication"
    STORAGE = "storage"


class CredentialType(str, Enum):
    """Credential authentication types"""
    NONE = "none"
    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    SERVICE_ACCOUNT = "service_account"
    BASIC_AUTH = "basic_auth"


class BlockGenerationRequest(BaseModel):
    """Request for block generation"""
    task: str = Field(description="Natural language description of the block")
    category: BlockCategory
    name: Optional[str] = None
    block_type: Optional[str] = None

    # Advanced options
    use_similarity_check: bool = True
    enable_self_healing: bool = True
    include_logging: bool = True
    include_retry_logic: bool = False


class BlockGenerationResult(BaseModel):
    """Result of block generation"""
    success: bool
    block_type: str
    name: str
    code: str
    manifest: Dict[str, Any]

    # Validation results
    validation_passed: bool = False
    validation_errors: List[str] = Field(default_factory=list)

    # Test Execution
    test_code: Optional[str] = None
    test_config: Optional[Dict[str, Any]] = None
    test_executed: bool = False
    test_passed: bool = False
    test_results: Optional[Dict[str, Any]] = None
    test_error: Optional[str] = None

    # Metadata
    generation_time_s: float = 0.0
    ai_model_used: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class EnhancedAIBlockGenerator:
    """
    Enhanced AI Block Generator with Deep Research

    Capabilities:
    1. Direct Generation: Simple blocks with clear requirements
    2. Similarity Check: Avoid duplicates, use templates
    3. Validation: Tests generated code before returning
    4. Self-Healing: Auto-fix failing tests
    """

    def __init__(
        self,
        ai_service: AIService,
        similarity_service: Optional[BlockSimilarityService] = None,
        enable_self_healing: bool = True
    ):
        """
        Initialize enhanced generator

        Args:
            ai_service: Base AI service for code generation
            similarity_service: Service to find similar blocks
            enable_self_healing: Enable auto-fix for failing tests
        """
        self.ai_service = ai_service
        self.similarity_service = similarity_service
        self.enable_self_healing = enable_self_healing
        self.logger = logging.getLogger(__name__)

    async def generate_block(
        self,
        request: BlockGenerationRequest
    ) -> BlockGenerationResult:
        """
        Generate block with optional similarity check and self-healing

        Args:
            request: Block generation request

        Returns:
            BlockGenerationResult with code, manifest, and validation
        """
        start_time = time.time()

        try:
            self.logger.info("=" * 80)
            self.logger.info(f"🚀 Starting enhanced block generation")
            self.logger.info(f"📝 Task: {request.task}")
            self.logger.info(f"📂 Category: {request.category.value}")
            self.logger.info("=" * 80)

            # Step 0: Check for similar existing blocks
            similar_blocks = []
            if request.use_similarity_check and self.similarity_service:
                self.logger.info("🔍 Checking for similar existing blocks...")
                should_proceed, enhanced_task_or_message, similar_blocks = await check_and_use_similar_blocks(
                    task=request.task,
                    category=request.category.value,
                    block_type=request.block_type,
                    similarity_service=self.similarity_service
                )

                if not should_proceed:
                    # Exact match found, return error
                    self.logger.warning(f"❌ Exact match found: {enhanced_task_or_message}")
                    return BlockGenerationResult(
                        success=False,
                        block_type=request.block_type or "",
                        name="",
                        code="",
                        manifest={},
                        validation_errors=[enhanced_task_or_message],
                        generation_time_s=time.time() - start_time
                    )

                # Use enhanced task with templates if similar blocks found
                if similar_blocks:
                    self.logger.info(f"✅ Found {len(similar_blocks)} similar blocks, using as templates")
                    request.task = enhanced_task_or_message
                else:
                    self.logger.info("📭 No similar blocks found")

            # Step 1: Prepare enhanced prompt based on category
            self.logger.info(f"📋 Step 1: Enhancing task prompt for category '{request.category.value}'")
            enhanced_task = self._enhance_task_prompt(request)

            # Step 2: Analyze the enhanced task to create RequirementAnalysis
            self.logger.info(f"🔍 Step 2: Analyzing requirements...")
            analysis = await self.ai_service.analyze_requirement(enhanced_task)
            self.logger.info(f"✅ Analysis complete: block_type={analysis.block_type}, category={analysis.category}")

            # Override block_type if specified in request
            if request.block_type:
                self.logger.info(f"🔧 Overriding block_type to: {request.block_type}")
                analysis.block_type = request.block_type

            # Override category to match request
            analysis.category = request.category.value

            # Step 3: Generate block using AI service
            self.logger.info(f"🤖 Step 3: Generating block code...")
            block_code, token_usage = await self.ai_service.generate_block_code(analysis)

            if token_usage:
                self.logger.info(
                    f"✅ Block generated: {block_code.block_type} ({len(block_code.code)} chars) | "
                    f"Tokens: {token_usage.total_tokens} (prompt: {token_usage.prompt_tokens}, completion: {token_usage.completion_tokens})"
                )
            else:
                self.logger.info(f"✅ Block generated: {block_code.block_type} ({len(block_code.code)} chars)")

            # Step 4: Post-process code
            self.logger.info("🔧 Step 4: Post-processing code...")
            code = block_code.code
            manifest = block_code.manifest

            # Add imports based on category
            code = self._add_required_imports(code, request)
            self.logger.info("✅ Required imports added")

            # Step 5: Validate generated code
            self.logger.info("✔️  Step 5: Validating generated code...")
            validation_result = self._validate_code(code, manifest)
            if validation_result["passed"]:
                self.logger.info("✅ Validation passed")
            else:
                self.logger.warning(f"⚠️  Validation issues: {validation_result.get('errors', [])}")

            # Step 6: Generate test code
            self.logger.info("🧪 Step 6: Generating test code...")
            test_code, test_config = await self._generate_test_code(
                code, manifest, block_code.block_type
            )
            self.logger.info(f"✅ Test code generated ({len(test_code) if test_code else 0} chars)")

            # Step 7: Execute test code
            test_executed = False
            test_passed = False
            test_results_dict = None
            test_error = None

            if test_code and test_config is not None:
                self.logger.info("🧪 Step 7: Executing test code...")
                try:
                    test_service = get_test_execution_service()
                    test_result = await test_service.execute_test(
                        test_code=test_code,
                        test_config=test_config,
                        block_code=code,
                        block_type=block_code.block_type,
                        timeout_sec=15
                    )

                    test_executed = True
                    test_passed = test_result.passed
                    test_results_dict = test_result.to_dict()

                    if test_passed:
                        self.logger.info(f"✅ Test PASSED ({test_result.duration_ms:.0f}ms)")
                    else:
                        self.logger.warning(f"❌ Test FAILED: {test_result.error}")
                        test_error = test_result.error

                        # Step 8: Self-Healing Loop
                        if request.enable_self_healing and self.enable_self_healing:
                            self.logger.info("🔄 Step 8: Starting self-healing loop...")
                            try:
                                healing_service = get_self_healing_service(
                                    provider=self.ai_service.provider,
                                    model=self.ai_service.model,
                                    max_attempts=3
                                )
                                healing_result = await healing_service.heal_block(
                                    task=request.task,
                                    category=request.category.value,
                                    block_type=block_code.block_type,
                                    name=request.name or manifest.get("name", "Generated Block"),
                                    manifest=manifest,
                                    initial_code=code,
                                    initial_test_code=test_code,
                                    initial_test_config=test_config
                                )

                                if healing_result["success"]:
                                    self.logger.info(f"✅ Self-healing succeeded after {healing_result['attempt']} attempts!")
                                    # Update with healed code
                                    code = healing_result["final_code"]
                                    manifest = healing_result["final_manifest"]
                                    test_passed = True
                                    test_error = None
                                    test_results_dict = healing_result["test_results"]
                                else:
                                    self.logger.warning(f"❌ Self-healing failed after {healing_result['attempt']} attempts")

                            except Exception as e:
                                self.logger.error(f"❌ Self-healing error: {e}", exc_info=True)

                except Exception as e:
                    self.logger.error(f"❌ Test execution error: {e}", exc_info=True)
                    test_executed = True
                    test_passed = False
                    test_error = str(e)
            else:
                self.logger.info("⏭️  Step 7: Skipped (no test code generated)")

            # Step 9: Build result
            self.logger.info("📦 Step 9: Building result...")
            generation_time = time.time() - start_time

            result = BlockGenerationResult(
                success=True,
                block_type=request.block_type or block_code.block_type,
                name=request.name or manifest.get("name", "Generated Block"),
                code=code,
                manifest=manifest,
                validation_passed=validation_result["passed"],
                validation_errors=validation_result.get("errors", []),
                test_code=test_code,
                test_config=test_config,
                test_executed=test_executed,
                test_passed=test_passed,
                test_results=test_results_dict,
                test_error=test_error,
                generation_time_s=generation_time,
                ai_model_used=self.ai_service.model,
                prompt_tokens=token_usage.prompt_tokens if token_usage else 0,
                completion_tokens=token_usage.completion_tokens if token_usage else 0,
                total_tokens=token_usage.total_tokens if token_usage else 0
            )

            self.logger.info("=" * 80)
            self.logger.info(f"✅ BLOCK GENERATION COMPLETE")
            self.logger.info(f"📝 Name: {result.name}")
            self.logger.info(f"🔖 Type: {result.block_type}")
            self.logger.info(f"✔️  Validation: {'PASSED' if result.validation_passed else 'FAILED'}")
            self.logger.info(f"🧪 Tests: {'PASSED' if result.test_passed else 'FAILED' if result.test_executed else 'SKIPPED'}")
            self.logger.info(f"⏱️  Time: {generation_time:.2f}s")
            self.logger.info("=" * 80)

            return result

        except Exception as e:
            self.logger.error(f"Block generation failed: {e}", exc_info=True)
            return BlockGenerationResult(
                success=False,
                block_type="",
                name="",
                code="",
                manifest={},
                validation_errors=[str(e)],
                generation_time_s=time.time() - start_time
            )

    def _enhance_task_prompt(self, request: BlockGenerationRequest) -> str:
        """Enhance task prompt based on category and requirements"""

        category_guidance = self._get_category_guidance(request.category)

        enhanced = f"""
{request.task}

Category: {request.category.value}

{category_guidance}

Requirements:
"""

        if request.include_logging:
            enhanced += "- Include logging statements for debugging\n"

        if request.include_retry_logic:
            enhanced += "- Implement retry logic with exponential backoff\n"

        return enhanced

    def _get_category_guidance(self, category: BlockCategory) -> str:
        """Get category-specific generation guidance"""

        guidance = {
            BlockCategory.CORE: """
This is a core workflow control block. Focus on:
- Clean flow control logic
- Proper error handling
- Clear input/output contracts
- No external dependencies
            """,
            BlockCategory.DATA_TRANSFORMATION: """
This is a data transformation block. Focus on:
- Efficient data processing
- Support for various data types
- Clear transformation logic
- Proper validation
            """,
            BlockCategory.SIMPLE_API: """
This is an API integration block. Focus on:
- Proper HTTP request handling
- Error response handling
- Rate limiting awareness
- Clear API endpoint documentation
            """,
        }

        return guidance.get(category, "")

    def _add_required_imports(
        self,
        code: str,
        request: BlockGenerationRequest
    ) -> str:
        """Add required imports based on category"""

        # Check if imports already present
        if "import" in code[:200]:  # Check first 200 chars
            return code

        imports = []

        # Category-specific imports
        if request.category in [BlockCategory.SIMPLE_API, BlockCategory.COMPLEX_OAUTH]:
            imports.append("import httpx")

        if request.include_retry_logic:
            imports.append("import asyncio")

        # Add imports to top of code
        if imports:
            import_block = "\n".join(imports) + "\n\n"
            return import_block + code

        return code

    def _validate_code(
        self,
        code: str,
        manifest: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate generated code

        Checks:
        1. Syntax validity
        2. Has execute function
        3. Manifest schema valid
        """
        errors = []

        # Check 1: Syntax validation
        try:
            compile(code, "<string>", "exec")
        except SyntaxError as e:
            errors.append(f"Syntax error: {e}")

        # Check 2: Has execute function
        has_execute = "def execute(" in code or "async def execute(" in code
        if not has_execute:
            errors.append("Missing execute() function")

        # Check 3: Manifest validation
        required_manifest_fields = ["name", "category"]
        for field in required_manifest_fields:
            if field not in manifest:
                errors.append(f"Missing manifest field: {field}")

        # Check for description or summary (at least one required)
        if "description" not in manifest and "summary" not in manifest:
            errors.append("Missing manifest field: description or summary")

        return {
            "passed": len(errors) == 0,
            "errors": errors
        }

    async def _generate_test_code(
        self,
        block_code: str,
        manifest: Dict[str, Any],
        block_type: str
    ) -> tuple[Optional[str], Optional[Dict[str, Any]]]:
        """
        Generate test code for the block

        Returns:
            (test_code, test_config) tuple
        """
        try:
            import json

            # Extract config schema from manifest
            config_schema = manifest.get("config_schema", {})

            # Generate appropriate test config based on schema
            test_config = self._generate_test_config(config_schema, manifest)

            # Generate test code
            block_name = manifest.get('name', block_type)
            test_code = f"""
import asyncio
import json
from typing import Dict, Any


async def test_{block_type.replace('-', '_')}():
    \"\"\"Test for {block_name}\"\"\"

    # Mock runtime
    class MockRuntime:
        def __init__(self):
            self.logger = self._get_logger()

        def _get_logger(self):
            import logging
            return logging.getLogger("{block_type}")

    runtime = MockRuntime()

    # Test configuration
    test_config = {json.dumps(test_config, indent=8)}

    # Execute block
    try:
        # Import block code
        namespace = {{'asyncio': asyncio, 'json': json, 'logging': __import__('logging')}}
        block_code = '''{block_code}'''

        exec(block_code, namespace)

        # Get execute function
        execute_func = namespace.get('execute')

        if not execute_func:
            return {{'success': False, 'error': 'No execute function found'}}

        # Run test
        result = await execute_func(runtime, **test_config)

        # Validate result
        if result is None:
            return {{'success': False, 'error': 'Block returned None'}}

        if not isinstance(result, dict):
            # Some blocks might return simple values - consider that OK
            return {{'success': True, 'result': result}}

        # Check for explicit error field
        if result.get('error') and result.get('error') != None:
            return {{'success': False, 'error': str(result.get('error'))}}

        # If result is a dict and has no error, consider it success
        return {{'success': True, 'result': result}}

    except Exception as e:
        return {{'success': False, 'error': str(e), 'error_type': type(e).__name__}}


if __name__ == "__main__":
    result = asyncio.run(test_{block_type.replace('-', '_')}())
    if isinstance(result, dict):
        exit(0 if result.get('success') else 1)
    exit(0 if result else 1)
"""

            return test_code, test_config

        except Exception as e:
            self.logger.warning(f"Failed to generate test code: {e}")
            return None, None

    def _generate_test_config(
        self,
        config_schema: Dict[str, Any],
        manifest: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate appropriate test configuration based on config schema"""
        test_config = {}

        # Get properties from schema
        properties = config_schema.get("properties", {})

        for param_name, param_spec in properties.items():
            param_type = param_spec.get("type", "string")
            default = param_spec.get("default")

            # Use default if available
            if default is not None:
                test_config[param_name] = default
                continue

            # Generate based on type
            if param_type == "string":
                test_config[param_name] = "test_value"
            elif param_type == "integer":
                test_config[param_name] = 42
            elif param_type == "number":
                test_config[param_name] = 3.14
            elif param_type == "boolean":
                test_config[param_name] = True
            elif param_type == "array":
                test_config[param_name] = ["item1", "item2", "item3"]
            elif param_type == "object":
                test_config[param_name] = {"key": "value"}
            else:
                test_config[param_name] = None

        return test_config
