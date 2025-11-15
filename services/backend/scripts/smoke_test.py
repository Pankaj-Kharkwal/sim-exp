"""
Smoke Test Script for Pankh.AI Backend

Tests all major API endpoints to ensure they're working correctly.

Usage:
    python scripts/smoke_test.py
"""

import asyncio
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import httpx
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings

console = Console()

BASE_URL = f"http://{settings.HOST}:{settings.PORT}"
API_URL = f"{BASE_URL}{settings.API_V1_STR}"


class APITester:
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        self.results = []
        self.token = None

    async def test(
        self,
        name: str,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        expected_status: int = 200,
        use_auth: bool = False,
    ):
        """Test an API endpoint"""
        url = f"{API_URL}{endpoint}"

        # Add auth header if needed
        if use_auth and self.token:
            if headers is None:
                headers = {}
            headers["Authorization"] = f"Bearer {self.token}"

        try:
            response = await self.client.request(
                method=method,
                url=url,
                data=data,
                json=json,
                headers=headers,
            )

            success = response.status_code == expected_status
            status = "✅ PASS" if success else "❌ FAIL"

            self.results.append({
                "name": name,
                "status": status,
                "code": response.status_code,
                "expected": expected_status,
                "success": success,
            })

            return response

        except Exception as e:
            self.results.append({
                "name": name,
                "status": "❌ ERROR",
                "code": "N/A",
                "expected": expected_status,
                "success": False,
                "error": str(e),
            })
            return None

    async def run_tests(self):
        """Run all smoke tests"""
        console.print("\n[bold blue]🚀 Starting API Smoke Tests[/bold blue]\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Running tests...", total=None)

            # Test 1: Health Check
            await self.test(
                name="Health Check",
                method="GET",
                endpoint="/health" if settings.API_V1_STR else "/health",
                expected_status=200,
            )

            # Test 2: Root endpoint
            await self.test(
                name="Root Endpoint",
                method="GET",
                endpoint="",
                expected_status=200,
            )

            # Test 3: Create Demo User (if not exists)
            signup_response = await self.test(
                name="User Signup",
                method="POST",
                endpoint="/auth/signup",
                json={
                    "email": "test@pankh.ai",
                    "password": "TestPass123!",
                    "name": "Test User",
                },
                expected_status=201,
            )

            # Test 4: Login
            login_response = await self.test(
                name="User Login",
                method="POST",
                endpoint="/auth/login",
                json={
                    "email": "demo@pankh.ai",  # Use demo user from init
                    "password": "demo",
                },
                expected_status=200,
            )

            # Extract token if login successful
            if login_response and login_response.status_code == 200:
                try:
                    data = login_response.json()
                    self.token = data.get("access_token")
                except:
                    pass

            # Test 5: List Workflows
            await self.test(
                name="List Workflows",
                method="GET",
                endpoint="/workflows",
                expected_status=200,
                use_auth=True,
            )

            # Test 6: Create Workflow
            create_workflow_response = await self.test(
                name="Create Workflow",
                method="POST",
                endpoint="/workflows",
                json={
                    "name": "Test Workflow",
                    "description": "Smoke test workflow",
                    "blocks": [],
                    "edges": [],
                },
                expected_status=201,
                use_auth=True,
            )

            workflow_id = None
            if create_workflow_response and create_workflow_response.status_code == 201:
                try:
                    data = create_workflow_response.json()
                    workflow_id = data.get("id")
                except:
                    pass

            # Test 7: Get Workflow (if created)
            if workflow_id:
                await self.test(
                    name="Get Workflow",
                    method="GET",
                    endpoint=f"/workflows/{workflow_id}",
                    expected_status=200,
                    use_auth=True,
                )

            # Test 8: List Blocks
            await self.test(
                name="List Blocks",
                method="GET",
                endpoint="/blocks",
                expected_status=200,
                use_auth=True,
            )

            # Test 9: List Executions
            await self.test(
                name="List Executions",
                method="GET",
                endpoint="/executions",
                expected_status=200,
                use_auth=True,
            )

            # Test 10: List Tasks
            await self.test(
                name="List Tasks",
                method="GET",
                endpoint="/tasks",
                expected_status=200,
                use_auth=True,
            )

            # Test 11: List Knowledge Bases
            await self.test(
                name="List Knowledge Bases",
                method="GET",
                endpoint="/knowledge",
                expected_status=200,
                use_auth=True,
            )

            # Test 12: Create Knowledge Base
            create_kb_response = await self.test(
                name="Create Knowledge Base",
                method="POST",
                endpoint="/knowledge",
                json={
                    "name": "Test KB",
                    "description": "Test knowledge base",
                },
                expected_status=201,
                use_auth=True,
            )

            kb_id = None
            if create_kb_response and create_kb_response.status_code == 201:
                try:
                    data = create_kb_response.json()
                    kb_id = data.get("id")
                except:
                    pass

            # Test 13: List Documents (if KB created)
            if kb_id:
                await self.test(
                    name="List Documents",
                    method="GET",
                    endpoint=f"/knowledge/{kb_id}/documents",
                    expected_status=200,
                    use_auth=True,
                )

            # Test 14: List Organizations
            await self.test(
                name="List Organizations",
                method="GET",
                endpoint="/organizations",
                expected_status=200,
                use_auth=True,
            )

            # Test 15: List Folders
            await self.test(
                name="List Folders",
                method="GET",
                endpoint="/folders",
                expected_status=200,
                use_auth=True,
            )

            progress.update(task, completed=True)

        await self.client.aclose()

    def print_results(self):
        """Print test results in a nice table"""
        console.print("\n[bold]Test Results[/bold]\n")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Test Name", style="cyan", width=30)
        table.add_column("Status", width=12)
        table.add_column("Status Code", justify="center", width=12)
        table.add_column("Expected", justify="center", width=10)

        for result in self.results:
            status_style = "green" if result["success"] else "red"
            table.add_row(
                result["name"],
                f"[{status_style}]{result['status']}[/{status_style}]",
                str(result["code"]),
                str(result["expected"]),
            )

        console.print(table)

        # Summary
        total = len(self.results)
        passed = sum(1 for r in self.results if r["success"])
        failed = total - passed
        success_rate = (passed / total * 100) if total > 0 else 0

        console.print(f"\n[bold]Summary:[/bold]")
        console.print(f"  Total Tests: {total}")
        console.print(f"  [green]Passed: {passed}[/green]")
        console.print(f"  [red]Failed: {failed}[/red]")
        console.print(f"  Success Rate: {success_rate:.1f}%")

        if failed > 0:
            console.print("\n[yellow]⚠️  Some tests failed. Check the logs for details.[/yellow]")
            sys.exit(1)
        else:
            console.print("\n[green]✅ All tests passed successfully![/green]")
            sys.exit(0)


async def main():
    """Main function"""
    console.print(f"[bold]Testing API at: {API_URL}[/bold]")

    # Check if backend is running
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{BASE_URL}/health")
            if response.status_code != 200:
                console.print("[red]❌ Backend is not healthy![/red]")
                sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ Cannot connect to backend: {e}[/red]")
        console.print(f"[yellow]Make sure the backend is running at {BASE_URL}[/yellow]")
        sys.exit(1)

    # Run tests
    tester = APITester()
    await tester.run_tests()
    tester.print_results()


if __name__ == "__main__":
    # Install required packages if not available
    try:
        import rich
    except ImportError:
        console.print("[yellow]Installing required package: rich[/yellow]")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "rich"])
        import rich

    asyncio.run(main())
