"""
Automated API Testing Script for Pankh.AI Backend
Tests all major endpoints and features
"""

import asyncio
import httpx
import json
from typing import Dict, Any, Optional

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
TEST_USER = {
    "email": "test@pankhapp.com",
    "password": "TestPassword123!",
    "name": "Test User"
}

class APITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.test_results = []

    async def test(self, name: str, method: str, endpoint: str, **kwargs):
        """Run a single test"""
        print(f"\n{'='*60}")
        print(f"Testing: {name}")
        print(f"{'='*60}")

        url = f"{self.base_url}{endpoint}"
        headers = kwargs.get('headers', {})

        if self.token and 'Authorization' not in headers:
            headers['Authorization'] = f"Bearer {self.token}"
            kwargs['headers'] = headers

        try:
            async with httpx.AsyncClient() as client:
                response = await getattr(client, method.lower())(url, **kwargs)

                success = 200 <= response.status_code < 300

                result = {
                    "name": name,
                    "method": method,
                    "endpoint": endpoint,
                    "status_code": response.status_code,
                    "success": success,
                    "response": response.text[:200] if len(response.text) > 200 else response.text
                }

                self.test_results.append(result)

                if success:
                    print(f"✅ PASSED - Status: {response.status_code}")
                    print(f"Response: {response.text[:200]}...")
                else:
                    print(f"❌ FAILED - Status: {response.status_code}")
                    print(f"Error: {response.text}")

                return response

        except Exception as e:
            print(f"❌ EXCEPTION: {str(e)}")
            self.test_results.append({
                "name": name,
                "success": False,
                "error": str(e)
            })
            return None

    async def run_all_tests(self):
        """Run complete test suite"""
        print("\n" + "="*60)
        print("PANKH.AI BACKEND API TEST SUITE")
        print("="*60)

        # Test 1: Health Check
        await self.test(
            "Health Check",
            "GET",
            "/../health"  # Going up from /api/v1
        )

        # Test 2: List Blocks (public endpoint)
        response = await self.test(
            "List All Blocks",
            "GET",
            "/blocks/"
        )

        if response and response.status_code == 200:
            try:
                blocks = response.json()
                print(f"   Found {len(blocks.get('blocks', []))} blocks")
            except:
                pass

        # Test 3: Get OpenAI Block Metadata
        await self.test(
            "Get OpenAI Block Metadata",
            "GET",
            "/blocks/openai"
        )

        # Test 4: Get Anthropic Block Metadata
        await self.test(
            "Get Anthropic Block Metadata",
            "GET",
            "/blocks/anthropic"
        )

        # Test 5: Get Slack Block Metadata
        await self.test(
            "Get Slack Block Metadata",
            "GET",
            "/blocks/slack"
        )

        # Test 6: Get blocks by category
        await self.test(
            "Get AI Category Blocks",
            "GET",
            "/blocks/category/ai"
        )

        # Note: Auth tests would require a running database
        # The following tests would need authentication
        print("\n" + "="*60)
        print("NOTE: Auth-protected endpoint tests skipped")
        print("Reason: Requires running database and user authentication")
        print("="*60)
        print("\nAuth-protected endpoints that would be tested:")
        print("  - POST /auth/login")
        print("  - GET /workflows/")
        print("  - POST /workflows/")
        print("  - POST /credentials/")
        print("  - POST /chat/")
        print("  - POST /copilot/suggest")
        print("  - POST /workflows/{id}/execute")

        # Print Summary
        self.print_summary()

    def print_summary(self):
        """Print test results summary"""
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)

        total = len(self.test_results)
        passed = sum(1 for r in self.test_results if r.get('success', False))
        failed = total - passed

        print(f"\nTotal Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {(passed/total*100) if total > 0 else 0:.1f}%")

        if failed > 0:
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result.get('success', False):
                    print(f"  ❌ {result['name']}")
                    if 'error' in result:
                        print(f"     Error: {result['error']}")
                    else:
                        print(f"     Status: {result.get('status_code', 'N/A')}")

async def main():
    """Main test execution"""
    tester = APITester(BASE_URL)

    print("\n🚀 Starting Pankh.AI API Tests...")
    print(f"Base URL: {BASE_URL}")
    print(f"{'='*60}\n")

    try:
        await tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")

    print("\n✅ Test suite completed!\n")

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║         PANKH.AI AUTOMATED API TEST SUITE                ║
    ║                                                           ║
    ║  Prerequisites:                                           ║
    ║    - Backend server running on http://localhost:8000     ║
    ║    - Database connection configured                       ║
    ║    - Redis connection configured                          ║
    ║                                                           ║
    ║  To start backend:                                        ║
    ║    cd services/backend                                    ║
    ║    uvicorn app.main:app --reload --port 8000             ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    asyncio.run(main())
