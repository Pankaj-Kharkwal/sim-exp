#!/usr/bin/env python3
"""
System Validation Script - Checks if all components are properly set up
Does not require running services, just validates file structure and imports
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple

class SystemValidator:
    def __init__(self, root_dir: Path):
        self.root = root_dir
        self.results = []

    def check_file_exists(self, path: str, description: str) -> bool:
        """Check if a file exists"""
        full_path = self.root / path
        exists = full_path.exists()
        self.results.append({
            "test": f"File: {description}",
            "status": "✅ PASS" if exists else "❌ FAIL",
            "path": path,
            "exists": exists
        })
        return exists

    def check_directory_exists(self, path: str, description: str) -> bool:
        """Check if a directory exists"""
        full_path = self.root / path
        exists = full_path.is_dir()
        self.results.append({
            "test": f"Directory: {description}",
            "status": "✅ PASS" if exists else "❌ FAIL",
            "path": path,
            "exists": exists
        })
        return exists

    def check_files_in_directory(self, directory: str, pattern: str, min_count: int, description: str) -> bool:
        """Check if directory contains minimum number of matching files"""
        full_path = self.root / directory
        if not full_path.exists():
            self.results.append({
                "test": description,
                "status": "❌ FAIL",
                "error": f"Directory {directory} not found"
            })
            return False

        matching_files = list(full_path.glob(pattern))
        count = len(matching_files)
        passed = count >= min_count

        self.results.append({
            "test": description,
            "status": "✅ PASS" if passed else "❌ FAIL",
            "count": count,
            "expected": f">= {min_count}"
        })
        return passed

    def validate_backend(self):
        """Validate backend structure"""
        print("\n" + "="*60)
        print("BACKEND VALIDATION")
        print("="*60)

        # Core directories
        self.check_directory_exists("services/backend", "Backend root directory")
        self.check_directory_exists("services/backend/app", "App directory")
        self.check_directory_exists("services/backend/app/api", "API directory")
        self.check_directory_exists("services/backend/app/executor", "Executor directory")
        self.check_directory_exists("services/backend/app/services", "Services directory")

        # Core files
        self.check_file_exists("services/backend/app/main.py", "Main FastAPI app")
        self.check_file_exists("services/backend/app/__init__.py", "App init file")
        self.check_file_exists("services/backend/requirements.txt", "Python dependencies")

        # API routers
        self.check_file_exists("services/backend/app/api/v1/__init__.py", "API v1 router")
        self.check_file_exists("services/backend/app/api/v1/auth.py", "Auth router")
        self.check_file_exists("services/backend/app/api/v1/workflows.py", "Workflows router")
        self.check_file_exists("services/backend/app/api/v1/blocks.py", "Blocks router")
        self.check_file_exists("services/backend/app/api/v1/chat.py", "Chat router")
        self.check_file_exists("services/backend/app/api/v1/copilot.py", "Copilot router")
        self.check_file_exists("services/backend/app/api/v1/credentials.py", "Credentials router")

        # Block executors
        self.check_file_exists("services/backend/app/executor/engine.py", "Workflow engine")
        self.check_file_exists("services/backend/app/executor/blocks/openai.py", "OpenAI executor")
        self.check_file_exists("services/backend/app/executor/blocks/anthropic.py", "Anthropic executor")
        self.check_file_exists("services/backend/app/executor/blocks/slack.py", "Slack executor")
        self.check_file_exists("services/backend/app/executor/blocks/gmail.py", "Gmail executor")
        self.check_file_exists("services/backend/app/executor/blocks/github.py", "GitHub executor")
        self.check_file_exists("services/backend/app/executor/blocks/notion.py", "Notion executor")
        self.check_file_exists("services/backend/app/executor/blocks/google_sheets.py", "Google Sheets executor")

        # Block metadata
        self.check_files_in_directory(
            "services/backend/app/executor/blocks/metadata",
            "*_meta.py",
            50,
            "Block metadata files (minimum 50)"
        )

        # Services
        self.check_file_exists("services/backend/app/services/chat_service.py", "Chat service")
        self.check_file_exists("services/backend/app/services/copilot_service.py", "Copilot service")
        self.check_file_exists("services/backend/app/services/credential_service.py", "Credential service")

        # Workers
        self.check_directory_exists("services/backend/app/workers", "Workers directory")
        self.check_file_exists("services/backend/app/workers/celery_app.py", "Celery app")
        self.check_file_exists("services/backend/app/workers/tasks.py", "Celery tasks")

    def validate_frontend(self):
        """Validate frontend structure"""
        print("\n" + "="*60)
        print("FRONTEND VALIDATION")
        print("="*60)

        # Core directories
        self.check_directory_exists("services/frontend", "Frontend root directory")
        self.check_directory_exists("services/frontend/src", "Source directory")
        self.check_directory_exists("services/frontend/src/pages", "Pages directory")
        self.check_directory_exists("services/frontend/src/components", "Components directory")
        self.check_directory_exists("services/frontend/src/stores", "Stores directory")

        # Core files
        self.check_file_exists("services/frontend/package.json", "Package.json")
        self.check_file_exists("services/frontend/vite.config.ts", "Vite config")
        self.check_file_exists("services/frontend/tsconfig.json", "TypeScript config")
        self.check_file_exists("services/frontend/src/main.tsx", "Main entry point")

        # Pages
        self.check_file_exists("services/frontend/src/pages/WorkflowsListPage.tsx", "Workflows list page")
        self.check_file_exists("services/frontend/src/pages/WorkflowEditorPage.tsx", "Workflow editor page")
        self.check_file_exists("services/frontend/src/pages/ChatPage.tsx", "Chat page")
        self.check_file_exists("services/frontend/src/pages/DashboardPage.tsx", "Dashboard page")

        # Stores
        self.check_file_exists("services/frontend/src/stores/workflowStore.ts", "Workflow store")
        self.check_file_exists("services/frontend/src/stores/panel/chat/store.ts", "Chat store")

        # API client
        self.check_file_exists("services/frontend/src/lib/api.ts", "API client")

    def validate_documentation(self):
        """Validate documentation"""
        print("\n" + "="*60)
        print("DOCUMENTATION VALIDATION")
        print("="*60)

        self.check_file_exists("services/docs/MIGRATION_STATUS.md", "Migration status doc")
        self.check_file_exists("services/docs/MISSING_FEATURES_ANALYSIS.md", "Missing features analysis")
        self.check_file_exists("services/docs/FEATURE_COMPLETION_SUMMARY.md", "Feature completion summary")
        self.check_file_exists("services/TESTING_GUIDE.md", "Testing guide")

    def check_python_syntax(self, file_path: str) -> bool:
        """Check if a Python file has valid syntax"""
        try:
            with open(self.root / file_path, 'r') as f:
                code = f.read()
                compile(code, file_path, 'exec')
            return True
        except SyntaxError as e:
            print(f"   ❌ Syntax error in {file_path}: {e}")
            return False
        except Exception as e:
            print(f"   ⚠️  Warning checking {file_path}: {e}")
            return True  # Don't fail for other errors

    def validate_python_syntax(self):
        """Validate Python syntax for critical files"""
        print("\n" + "="*60)
        print("PYTHON SYNTAX VALIDATION")
        print("="*60)

        critical_files = [
            "services/backend/app/main.py",
            "services/backend/app/executor/engine.py",
            "services/backend/app/executor/blocks/openai.py",
            "services/backend/app/executor/blocks/anthropic.py",
            "services/backend/app/executor/blocks/slack.py",
            "services/backend/app/services/credential_service.py",
            "services/backend/app/api/v1/credentials.py",
        ]

        all_valid = True
        for file_path in critical_files:
            if (self.root / file_path).exists():
                is_valid = self.check_python_syntax(file_path)
                status = "✅ PASS" if is_valid else "❌ FAIL"
                print(f"{status} - {file_path}")
                if not is_valid:
                    all_valid = False
            else:
                print(f"⚠️  SKIP - {file_path} (file not found)")

        self.results.append({
            "test": "Python syntax validation",
            "status": "✅ PASS" if all_valid else "❌ FAIL"
        })

    def print_summary(self):
        """Print validation summary"""
        print("\n" + "="*60)
        print("VALIDATION SUMMARY")
        print("="*60)

        total = len(self.results)
        passed = sum(1 for r in self.results if "✅" in r["status"])
        failed = total - passed

        print(f"\nTotal Checks: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {(passed/total*100) if total > 0 else 0:.1f}%")

        if failed > 0:
            print("\n" + "="*60)
            print("FAILED CHECKS")
            print("="*60)
            for result in self.results:
                if "❌" in result["status"]:
                    print(f"\n❌ {result['test']}")
                    if 'path' in result:
                        print(f"   Path: {result['path']}")
                    if 'error' in result:
                        print(f"   Error: {result['error']}")
                    if 'count' in result and 'expected' in result:
                        print(f"   Found: {result['count']}, Expected: {result['expected']}")

    def run_all_validations(self):
        """Run all validation checks"""
        print("\n╔═══════════════════════════════════════════════════════════╗")
        print("║         PANKH.AI SYSTEM VALIDATION SUITE                 ║")
        print("║                                                           ║")
        print("║  Validates file structure and code integrity             ║")
        print("║  Does not require running services                       ║")
        print("╚═══════════════════════════════════════════════════════════╝")

        self.validate_backend()
        self.validate_frontend()
        self.validate_documentation()
        self.validate_python_syntax()
        self.print_summary()

        # Return exit code
        failed = sum(1 for r in self.results if "❌" in r["status"])
        return 0 if failed == 0 else 1


def main():
    # Find project root
    script_dir = Path(__file__).parent
    root_dir = script_dir

    validator = SystemValidator(root_dir)
    exit_code = validator.run_all_validations()

    print("\n" + "="*60)
    if exit_code == 0:
        print("✅ ALL VALIDATIONS PASSED!")
        print("\nNext steps:")
        print("  1. Start backend: cd services/backend && uvicorn app.main:app --reload")
        print("  2. Start frontend: cd services/frontend && npm run dev")
        print("  3. Run API tests: python services/backend/test_api.py")
        print("  4. Open browser: http://localhost:5173")
    else:
        print("❌ SOME VALIDATIONS FAILED")
        print("\nPlease fix the failed checks before proceeding.")
    print("="*60 + "\n")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
