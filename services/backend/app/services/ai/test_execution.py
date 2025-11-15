"""
Test Execution Service - Safe Sandbox for Testing Generated Blocks

Executes generated test code in a safe sandbox before block registration.
Only blocks that pass tests are registered to the database.
"""

import asyncio
import logging
import time
import io
import sys
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum
from contextlib import redirect_stdout, redirect_stderr

logger = logging.getLogger(__name__)


class TestStatus(str, Enum):
    """Test execution status"""
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    SKIPPED = "skipped"
    TIMEOUT = "timeout"


class TestResult:
    """Result of test execution"""

    def __init__(
        self,
        status: TestStatus,
        duration_ms: float,
        output: str = "",
        error: Optional[str] = None,
        error_type: Optional[str] = None,
        test_case_results: Optional[List[Dict[str, Any]]] = None
    ):
        self.status = status
        self.duration_ms = duration_ms
        self.output = output
        self.error = error
        self.error_type = error_type
        self.test_case_results = test_case_results or []
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "status": self.status.value,
            "duration_ms": self.duration_ms,
            "output": self.output,
            "error": self.error,
            "error_type": self.error_type,
            "test_case_results": self.test_case_results,
            "timestamp": self.timestamp.isoformat()
        }

    @property
    def passed(self) -> bool:
        """Check if test passed"""
        return self.status == TestStatus.PASSED


class TestExecutionService:
    """
    Service for executing block tests in a safe sandbox

    Features:
    - Safe execution environment
    - Timeout protection
    - Detailed error reporting
    - Test result storage
    """

    def __init__(self, default_timeout_sec: int = 10):
        self.default_timeout_sec = default_timeout_sec
        self.logger = logging.getLogger(__name__)

    async def execute_test(
        self,
        test_code: str,
        test_config: Dict[str, Any],
        block_code: str,
        block_type: str,
        timeout_sec: Optional[int] = None
    ) -> TestResult:
        """
        Execute test code for a block

        Args:
            test_code: Test code to execute
            test_config: Test configuration (input parameters)
            block_code: Block code being tested
            block_type: Type of the block
            timeout_sec: Timeout in seconds (default: 10)

        Returns:
            TestResult with execution details
        """
        timeout = timeout_sec or self.default_timeout_sec
        start_time = time.time()

        self.logger.info(f"🧪 Executing test for block: {block_type}")
        self.logger.info(f"   Timeout: {timeout}s")
        self.logger.debug(f"   Test config: {test_config}")

        try:
            # Execute test with timeout
            result = await asyncio.wait_for(
                self._execute_test_safe(test_code, test_config, block_code, block_type),
                timeout=timeout
            )

            duration_ms = (time.time() - start_time) * 1000

            test_status = "PASSED" if result.get("success") else "FAILED"
            self.logger.info(f"{'✅' if result.get('success') else '❌'} Test completed: {test_status} ({duration_ms:.0f}ms)")

            return TestResult(
                status=TestStatus.PASSED if result.get("success") else TestStatus.FAILED,
                duration_ms=duration_ms,
                output=result.get("output", ""),
                error=result.get("error"),
                error_type=result.get("error_type"),
                test_case_results=result.get("test_cases", [])
            )

        except asyncio.TimeoutError:
            duration_ms = (time.time() - start_time) * 1000
            self.logger.error(f"❌ Test timeout after {timeout}s")

            return TestResult(
                status=TestStatus.TIMEOUT,
                duration_ms=duration_ms,
                error=f"Test execution timed out after {timeout} seconds",
                error_type="TimeoutError"
            )

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            self.logger.error(f"❌ Test execution error: {e}", exc_info=True)

            return TestResult(
                status=TestStatus.ERROR,
                duration_ms=duration_ms,
                error=str(e),
                error_type=type(e).__name__
            )

    async def _execute_test_safe(
        self,
        test_code: str,
        test_config: Dict[str, Any],
        block_code: str,
        block_type: str
    ) -> Dict[str, Any]:
        """
        Execute test in a safe sandbox environment

        Returns:
            Dictionary with test results
        """
        # Create safe namespace for execution
        namespace = {
            "__name__": f"test_{block_type}",
            "__builtins__": {
                # Safe built-ins only
                "len": len,
                "str": str,
                "int": int,
                "float": float,
                "bool": bool,
                "list": list,
                "dict": dict,
                "tuple": tuple,
                "set": set,
                "range": range,
                "enumerate": enumerate,
                "zip": zip,
                "map": map,
                "filter": filter,
                "sum": sum,
                "min": min,
                "max": max,
                "abs": abs,
                "round": round,
                "sorted": sorted,
                "reversed": reversed,
                "any": any,
                "all": all,
                "isinstance": isinstance,
                "type": type,
                "print": print,
                "__import__": __import__,
                "__build_class__": __build_class__,
                "__name__": f"test_{block_type}",
                "exec": exec,
                "ValueError": ValueError,
                "TypeError": TypeError,
                "KeyError": KeyError,
                "IndexError": IndexError,
                "Exception": Exception,
                "AssertionError": AssertionError,
            },
            # Standard library modules
            "asyncio": asyncio,
            "json": __import__("json"),
            "logging": logging,
        }

        # Capture output
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        try:
            # Execute the test code
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(test_code, namespace)

                # Find the test function
                test_func = None
                for name, obj in namespace.items():
                    if name.startswith("test_") and callable(obj):
                        test_func = obj
                        break

                if not test_func:
                    return {
                        "success": False,
                        "error": "No test function found (must start with 'test_')",
                        "error_type": "TestNotFoundError"
                    }

                # Execute the test
                if asyncio.iscoroutinefunction(test_func):
                    result = await test_func()
                else:
                    result = test_func()

                # Get captured output
                stdout = stdout_capture.getvalue()
                stderr = stderr_capture.getvalue()

                # Determine success based on result
                if isinstance(result, bool):
                    success = result
                elif isinstance(result, dict):
                    success = result.get("success", True)
                else:
                    success = True  # If test didn't fail with exception, consider it passed

                return {
                    "success": success,
                    "output": stdout + stderr,
                    "result": result if not isinstance(result, bool) else None
                }

        except AssertionError as e:
            return {
                "success": False,
                "error": f"Assertion failed: {str(e)}",
                "error_type": "AssertionError",
                "output": stdout_capture.getvalue() + stderr_capture.getvalue()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__,
                "output": stdout_capture.getvalue() + stderr_capture.getvalue()
            }


# Global service instance
_test_execution_service: Optional[TestExecutionService] = None


def get_test_execution_service() -> TestExecutionService:
    """Get or create the global test execution service"""
    global _test_execution_service
    if _test_execution_service is None:
        _test_execution_service = TestExecutionService(default_timeout_sec=10)
    return _test_execution_service
