"""
Self-Healing Block Generation Service - Using LangGraph

Implements an intelligent retry loop that:
1. Tests generated block code
2. If test fails, analyzes the error
3. Sends error context to AI for fixing
4. Regenerates the block code
5. Retests until success or max retries

Uses LangGraph for state machine orchestration.
"""

import logging
import os
from typing import Dict, Any, Optional, List, TypedDict
from datetime import datetime

from langgraph.graph import StateGraph, END
from langchain_openai import AzureChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

logger = logging.getLogger(__name__)


class HealingState(TypedDict):
    """State for the self-healing graph"""
    # Input
    task: str
    category: str
    block_type: str
    name: str
    manifest: Dict[str, Any]

    # Current attempt
    attempt: int
    max_attempts: int
    block_code: str
    test_code: str
    test_config: Dict[str, Any]

    # Test results
    test_executed: bool
    test_passed: bool
    test_error: Optional[str]
    test_results: Optional[Dict[str, Any]]

    # Healing history
    fixes_attempted: List[Dict[str, Any]]
    error_analysis: Optional[str]

    # Final result
    success: bool
    final_code: Optional[str]
    final_manifest: Optional[Dict[str, Any]]


class SelfHealingService:
    """
    Service that uses LangGraph to create a self-healing loop for block generation

    Flow:
    START → generate_code → test_code → [PASS] → END
                              ↓ [FAIL]
                         analyze_error → fix_code → test_code
                              ↓ [MAX RETRIES]
                             END
    """

    def __init__(
        self,
        provider: str = "azure-openai",
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        model: str = "gpt-4",
        max_attempts: int = 3
    ):
        """
        Initialize self-healing service

        Args:
            provider: "azure-openai" or "anthropic"
            endpoint: Azure endpoint (for Azure OpenAI)
            api_key: API key
            model: Model name
            max_attempts: Maximum healing attempts
        """
        self.max_attempts = max_attempts
        self.logger = logging.getLogger(__name__)
        self.provider = provider

        # Initialize LLM based on provider
        if provider == "azure-openai":
            endpoint = endpoint or os.getenv("AZURE_OPENAI_ENDPOINT")
            api_key = api_key or os.getenv("AZURE_OPENAI_API_KEY")
            api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")

            if not endpoint or not api_key:
                raise ValueError("Azure OpenAI credentials not configured")

            self.llm = AzureChatOpenAI(
                azure_endpoint=endpoint,
                api_key=api_key,
                api_version=api_version,
                deployment_name=model,
                temperature=0.7,
                max_tokens=4000
            )
        elif provider == "anthropic":
            api_key = api_key or os.getenv("ANTHROPIC_API_KEY")

            if not api_key:
                raise ValueError("Anthropic API key not configured")

            self.llm = ChatAnthropic(
                api_key=api_key,
                model=model,
                temperature=0.7,
                max_tokens=4000
            )
        else:
            raise ValueError(f"Unknown provider: {provider}")

        # Build the LangGraph
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the self-healing state machine with LangGraph"""

        workflow = StateGraph(HealingState)

        # Define nodes
        workflow.add_node("generate_code", self._generate_code_node)
        workflow.add_node("test_code", self._test_code_node)
        workflow.add_node("analyze_error", self._analyze_error_node)
        workflow.add_node("fix_code", self._fix_code_node)

        # Define edges
        workflow.set_entry_point("generate_code")

        # After generate_code, always test
        workflow.add_edge("generate_code", "test_code")

        # After test_code, check result
        workflow.add_conditional_edges(
            "test_code",
            self._should_retry,
            {
                "success": END,
                "retry": "analyze_error",
                "give_up": END
            }
        )

        # After analyze_error, fix the code
        workflow.add_edge("analyze_error", "fix_code")

        # After fix_code, test again
        workflow.add_edge("fix_code", "test_code")

        return workflow.compile()

    async def heal_block(
        self,
        task: str,
        category: str,
        block_type: str,
        name: str,
        manifest: Dict[str, Any],
        initial_code: str,
        initial_test_code: str,
        initial_test_config: Dict[str, Any]
    ) -> HealingState:
        """
        Run the self-healing loop for a block

        Args:
            task: Original task description
            category: Block category
            block_type: Block type identifier
            name: Block name
            manifest: Block manifest
            initial_code: Initially generated code that failed
            initial_test_code: Test code
            initial_test_config: Test configuration

        Returns:
            Final HealingState with results
        """

        self.logger.info(f"🔄 Starting self-healing loop for block: {block_type}")
        self.logger.info(f"   Max attempts: {self.max_attempts}")

        # Initialize state
        initial_state: HealingState = {
            "task": task,
            "category": category,
            "block_type": block_type,
            "name": name,
            "manifest": manifest,
            "attempt": 0,
            "max_attempts": self.max_attempts,
            "block_code": initial_code,
            "test_code": initial_test_code,
            "test_config": initial_test_config,
            "test_executed": False,
            "test_passed": False,
            "test_error": None,
            "test_results": None,
            "fixes_attempted": [],
            "error_analysis": None,
            "success": False,
            "final_code": None,
            "final_manifest": None
        }

        # Run the graph
        final_state = await self.graph.ainvoke(initial_state)

        self.logger.info(f"{'✅' if final_state['success'] else '❌'} Self-healing completed: {block_type}")
        self.logger.info(f"   Attempts: {final_state['attempt']}/{self.max_attempts}")
        self.logger.info(f"   Success: {final_state['success']}")

        return final_state

    async def _generate_code_node(self, state: HealingState) -> HealingState:
        """Generate initial code (or use provided code on first run)"""

        self.logger.info(f"📝 Generate code node (attempt {state['attempt']})")

        # On first attempt, code is already provided
        # This node is mainly for subsequent regenerations
        state["attempt"] = state["attempt"] + 1

        return state

    async def _test_code_node(self, state: HealingState) -> HealingState:
        """Execute tests on the block code"""

        self.logger.info(f"🧪 Testing code (attempt {state['attempt']})")

        try:
            from .test_execution import get_test_execution_service

            test_service = get_test_execution_service()
            test_result = await test_service.execute_test(
                test_code=state["test_code"],
                test_config=state["test_config"],
                block_code=state["block_code"],
                block_type=state["block_type"],
                timeout_sec=15
            )

            state["test_executed"] = True
            state["test_passed"] = test_result.passed
            state["test_results"] = test_result.to_dict()
            state["test_error"] = test_result.error

            if test_result.passed:
                self.logger.info(f"✅ Test passed on attempt {state['attempt']}")
                state["success"] = True
                state["final_code"] = state["block_code"]
                state["final_manifest"] = state["manifest"]
            else:
                self.logger.warning(f"❌ Test failed on attempt {state['attempt']}: {test_result.error}")

        except Exception as e:
            self.logger.error(f"❌ Test execution failed: {e}", exc_info=True)
            state["test_executed"] = True
            state["test_passed"] = False
            state["test_error"] = str(e)

        return state

    def _should_retry(self, state: HealingState) -> str:
        """Decide whether to retry, succeed, or give up"""

        if state["test_passed"]:
            return "success"

        if state["attempt"] >= state["max_attempts"]:
            self.logger.warning(f"⚠️  Max attempts reached ({state['max_attempts']}), giving up")
            return "give_up"

        return "retry"

    async def _analyze_error_node(self, state: HealingState) -> HealingState:
        """Use AI to analyze the test failure"""

        self.logger.info(f"🔍 Analyzing error (attempt {state['attempt']})")

        # Build context for AI
        error_context = f"""
Block Code that Failed:
```python
{state['block_code']}
```

Test Code:
```python
{state['test_code']}
```

Test Configuration:
{state['test_config']}

Test Error:
{state['test_error']}

Test Results:
{state['test_results']}

Previous Fix Attempts:
{state['fixes_attempted']}
"""

        system_prompt = """You are an expert Python developer analyzing test failures.
Your job is to:
1. Understand why the test failed
2. Identify the root cause in the block code
3. Explain what needs to be fixed

Be specific and concise. Focus on the actual error, not general advice."""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Analyze this test failure and explain what's wrong:\n\n{error_context}")
            ]

            response = await self.llm.ainvoke(messages)
            analysis = response.content

            state["error_analysis"] = analysis
            self.logger.info(f"📊 Error analysis complete: {analysis[:200]}...")

        except Exception as e:
            self.logger.error(f"❌ Error analysis failed: {e}", exc_info=True)
            state["error_analysis"] = f"Analysis failed: {str(e)}"

        return state

    async def _fix_code_node(self, state: HealingState) -> HealingState:
        """Use AI to fix the block code"""

        self.logger.info(f"🔧 Fixing code (attempt {state['attempt']})")

        # Build fix context
        fix_context = f"""
Original Task: {state['task']}

Current Block Code (BROKEN):
```python
{state['block_code']}
```

Block Manifest:
{state['manifest']}

Error Analysis:
{state['error_analysis']}

Test Error:
{state['test_error']}

Previous Fix Attempts:
{[fix['description'] for fix in state['fixes_attempted']]}
"""

        system_prompt = """You are an expert Python developer fixing broken code.

Your job is to:
1. Fix the block code based on the error analysis
2. Ensure the code follows the manifest schema
3. Make sure the code will pass the test

IMPORTANT:
- Return ONLY the fixed Python code, nothing else
- No markdown code blocks, no explanations
- The code must be a valid Python async function called 'execute'
- The function signature must be: async def execute(runtime, **config)
- Use proper error handling
- Return a dictionary with results

DO NOT include any text before or after the code."""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=f"Fix this code:\n\n{fix_context}")
            ]

            response = await self.llm.ainvoke(messages)
            fixed_code = response.content.strip()

            # Clean up any markdown if AI didn't follow instructions
            if fixed_code.startswith("```python"):
                fixed_code = fixed_code.split("```python")[1].split("```")[0].strip()
            elif fixed_code.startswith("```"):
                fixed_code = fixed_code.split("```")[1].split("```")[0].strip()

            # Record the fix attempt
            state["fixes_attempted"].append({
                "attempt": state["attempt"],
                "description": state["error_analysis"][:200],
                "timestamp": datetime.utcnow().isoformat()
            })

            # Update the block code
            state["block_code"] = fixed_code
            self.logger.info(f"✨ Code fixed ({len(fixed_code)} chars)")

        except Exception as e:
            self.logger.error(f"❌ Code fix failed: {e}", exc_info=True)
            # Keep the old code on error

        return state


# Global service instance
_self_healing_service: Optional[SelfHealingService] = None


def get_self_healing_service(
    provider: str = "azure-openai",
    model: str = "gpt-4",
    max_attempts: int = 3
) -> SelfHealingService:
    """Get or create the global self-healing service"""
    global _self_healing_service

    if _self_healing_service is None:
        _self_healing_service = SelfHealingService(
            provider=provider,
            model=model,
            max_attempts=max_attempts
        )

    return _self_healing_service
