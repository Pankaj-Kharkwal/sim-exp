"""
AI Services for Automated Block Generation

This package provides intelligent block generation using Azure OpenAI/Anthropic:
- AIService: Base AI service for code generation
- EnhancedAIBlockGenerator: Full AI-powered block generation pipeline
- BlockSimilarityService: Find similar blocks to avoid duplicates
- SelfHealingService: Auto-fix failing block tests with LangGraph
- TestExecutionService: Safe sandbox for testing generated blocks
"""

from .ai_service import AIService, RequirementAnalysis, BlockCode
from .enhanced_generator import (
    EnhancedAIBlockGenerator,
    BlockGenerationRequest,
    BlockGenerationResult,
    BlockCategory,
    CredentialType,
)
from .similarity_service import BlockSimilarityService, SimilarBlock
from .self_healing import SelfHealingService, get_self_healing_service
from .test_execution import TestExecutionService, TestResult, TestStatus, get_test_execution_service

__all__ = [
    "AIService",
    "RequirementAnalysis",
    "BlockCode",
    "EnhancedAIBlockGenerator",
    "BlockGenerationRequest",
    "BlockGenerationResult",
    "BlockCategory",
    "CredentialType",
    "BlockSimilarityService",
    "SimilarBlock",
    "SelfHealingService",
    "get_self_healing_service",
    "TestExecutionService",
    "TestResult",
    "TestStatus",
    "get_test_execution_service",
]
