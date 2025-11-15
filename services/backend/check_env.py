#!/usr/bin/env python3
"""
Environment Configuration Checker
Validates all required environment variables for Pankh.AI backend
"""

import os
import sys
from typing import Dict, List, Tuple


class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def check_env_var(name: str, required: bool = True) -> Tuple[bool, str]:
    """Check if environment variable is set"""
    value = os.getenv(name)
    if value:
        # Mask sensitive values
        if any(x in name for x in ['KEY', 'SECRET', 'PASSWORD', 'TOKEN']):
            masked = value[:8] + '*' * (len(value) - 12) + value[-4:] if len(value) > 12 else '*' * len(value)
            return True, masked
        return True, value
    return False, "Not set"


def print_section(title: str):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 80}{Colors.END}")


def print_check(name: str, status: bool, value: str, required: bool = True):
    """Print check result"""
    status_icon = f"{Colors.GREEN}✅" if status else (f"{Colors.RED}❌" if required else f"{Colors.YELLOW}⚠️ ")
    req_label = "REQUIRED" if required else "Optional"
    status_color = Colors.GREEN if status else (Colors.RED if required else Colors.YELLOW)

    print(f"{status_icon} {Colors.END}{name:<35} {status_color}{value}{Colors.END} ({req_label})")


def main():
    """Main check function"""
    print(f"\n{Colors.BOLD}Pankh.AI Backend - Environment Configuration Checker{Colors.END}")
    print(f"{Colors.BOLD}Checking environment variables...{Colors.END}")

    all_ok = True
    warnings = []

    # Azure OpenAI Configuration (REQUIRED for AI block generation)
    print_section("🤖 Azure OpenAI Configuration")

    checks = [
        ("AZURE_OPENAI_ENDPOINT", True),
        ("AZURE_OPENAI_API_KEY", True),
        ("AZURE_OPENAI_API_VERSION", True),
        ("AZURE_OPENAI_DEPLOYMENT_CHAT", True),
        ("AZURE_OPENAI_DEPLOYMENT_CODE", True),
        ("AZURE_OPENAI_DEPLOYMENT_EMBEDDINGS", False),
    ]

    for var, required in checks:
        status, value = check_env_var(var, required)
        print_check(var, status, value, required)
        if not status and required:
            all_ok = False
        elif not status:
            warnings.append(f"{var} is not set (optional)")

    # Alternative AI Providers
    print_section("🔄 Alternative AI Providers (Optional)")

    openai_status, openai_value = check_env_var("OPENAI_API_KEY", False)
    print_check("OPENAI_API_KEY", openai_status, openai_value, False)

    anthropic_status, anthropic_value = check_env_var("ANTHROPIC_API_KEY", False)
    print_check("ANTHROPIC_API_KEY", anthropic_status, anthropic_value, False)

    # Database Configuration
    print_section("💾 Database Configuration")

    db_checks = [
        ("DATABASE_URL", True),
        ("POSTGRES_USER", False),
        ("POSTGRES_PASSWORD", False),
        ("POSTGRES_DB", False),
        ("POSTGRES_HOST", False),
        ("POSTGRES_PORT", False),
    ]

    for var, required in db_checks:
        status, value = check_env_var(var, required)
        print_check(var, status, value, required)
        if not status and required:
            all_ok = False

    # MongoDB Configuration
    print_section("🍃 MongoDB Configuration")

    mongo_checks = [
        ("MONGO_URI", False),
        ("MONGO_DB", False),
    ]

    for var, required in mongo_checks:
        status, value = check_env_var(var, required)
        print_check(var, status, value, required)

    # Redis Configuration
    print_section("🔴 Redis Configuration")

    redis_checks = [
        ("REDIS_URL", False),
        ("REDIS_HOST", False),
        ("REDIS_PORT", False),
    ]

    for var, required in redis_checks:
        status, value = check_env_var(var, required)
        print_check(var, status, value, required)

    # Security Configuration
    print_section("🔐 Security Configuration")

    security_checks = [
        ("SECRET_KEY", True),
        ("ALGORITHM", False),
        ("ACCESS_TOKEN_EXPIRE_MINUTES", False),
        ("API_KEY", False),
    ]

    for var, required in security_checks:
        status, value = check_env_var(var, required)
        print_check(var, status, value, required)
        if not status and required:
            all_ok = False

    # Application Settings
    print_section("⚙️  Application Settings")

    app_checks = [
        ("APP_NAME", False),
        ("DEBUG", False),
        ("LOG_LEVEL", False),
        ("ENVIRONMENT", False),
        ("CORS_ORIGINS", False),
    ]

    for var, required in app_checks:
        status, value = check_env_var(var, required)
        print_check(var, status, value, required)

    # AI Block Generation Settings
    print_section("🧠 AI Block Generation Settings")

    ai_checks = [
        ("ENABLE_AI_BLOCK_GENERATION", False),
        ("MAX_HEALING_ATTEMPTS", False),
        ("BLOCK_TEST_TIMEOUT_SEC", False),
    ]

    for var, required in ai_checks:
        status, value = check_env_var(var, required)
        print_check(var, status, value, required)

    # External Services
    print_section("🌐 External Services (Optional)")

    ext_checks = [
        ("AZURE_KEY_VAULT_URL", False),
        ("SEARXNG_URL", False),
        ("QDRANT_URL", False),
        ("WORKER_SERVICE_URL", False),
        ("GLUON_SERVICE_URL", False),
    ]

    for var, required in ext_checks:
        status, value = check_env_var(var, required)
        print_check(var, status, value, required)

    # Summary
    print_section("📊 Summary")

    if all_ok:
        print(f"{Colors.GREEN}✅ All required environment variables are set!{Colors.END}")
        print(f"\n{Colors.BOLD}Next steps:{Colors.END}")
        print(f"1. Start the backend: {Colors.BLUE}poetry run uvicorn app.main:app --reload{Colors.END}")
        print(f"2. Test AI block generation: {Colors.BLUE}curl -X POST http://localhost:8000/api/v1/blocks/generate{Colors.END}")
        print(f"3. Read the docs: {Colors.BLUE}AI_BLOCK_GENERATION_QUICKSTART.md{Colors.END}")
    else:
        print(f"{Colors.RED}❌ Some required environment variables are missing!{Colors.END}")
        print(f"\n{Colors.BOLD}Required actions:{Colors.END}")
        print(f"1. Copy .env.example to .env: {Colors.BLUE}cp .env.example .env{Colors.END}")
        print(f"2. Update the required variables in .env")
        print(f"3. Run this check again: {Colors.BLUE}python check_env.py{Colors.END}")
        print(f"\n{Colors.BOLD}See ENV_SETUP.md for detailed instructions.{Colors.END}")

    if warnings:
        print(f"\n{Colors.YELLOW}⚠️  Warnings:{Colors.END}")
        for warning in warnings[:5]:  # Show first 5 warnings
            print(f"   - {warning}")
        if len(warnings) > 5:
            print(f"   ... and {len(warnings) - 5} more")

    print(f"\n{Colors.BOLD}{'=' * 80}{Colors.END}\n")

    return 0 if all_ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Check cancelled by user{Colors.END}")
        sys.exit(1)
