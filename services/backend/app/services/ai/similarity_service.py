"""
Block Similarity Service

Checks for existing blocks before generation to:
1. Avoid duplicates
2. Use existing blocks as templates
3. Learn from working implementations
4. Maintain consistency
"""

import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class SimilarBlock:
    """Represents a similar existing block"""
    block_type: str
    name: str
    description: str
    category: str
    similarity_score: float  # 0.0 to 1.0
    code: Optional[str] = None
    manifest: Optional[Dict[str, Any]] = None
    reason: str = ""  # Why it's considered similar


class BlockSimilarityService:
    """
    Service to find similar existing blocks

    Uses multiple strategies:
    1. Exact name match
    2. Description similarity (keyword matching)
    3. Category matching
    4. Functionality matching
    """

    def __init__(self, blocks_repository=None):
        """
        Initialize similarity service

        Args:
            blocks_repository: Repository for querying blocks (optional)
        """
        self.blocks_repository = blocks_repository
        self.logger = logging.getLogger(__name__)

    async def find_similar_blocks(
        self,
        task: str,
        category: str,
        block_type: Optional[str] = None,
        include_code: bool = True,
        threshold: float = 0.6
    ) -> List[SimilarBlock]:
        """
        Find blocks similar to the requested task

        Args:
            task: Description of the block to generate
            category: Category of the block
            block_type: Optional specific block_type to check
            include_code: Whether to include code in results
            threshold: Minimum similarity score (0.0-1.0)

        Returns:
            List of similar blocks sorted by similarity score
        """
        similar_blocks = []

        # Strategy 1: Check for exact block_type match
        if block_type:
            exact_match = await self._check_exact_match(block_type, include_code)
            if exact_match:
                similar_blocks.append(exact_match)
                return similar_blocks  # Early return for exact match

        # Strategy 2: Find blocks in same category
        category_blocks = await self._find_category_blocks(category, include_code)

        # Strategy 3: Find blocks with similar descriptions
        for block in category_blocks:
            score = self._calculate_similarity(task, block)
            if score >= threshold:
                similar_blocks.append(SimilarBlock(
                    block_type=block.get("block_type", ""),
                    name=block.get("name", ""),
                    description=block.get("description", ""),
                    category=block.get("category", ""),
                    similarity_score=score,
                    code=block.get("code") if include_code else None,
                    manifest=block.get("manifest"),
                    reason=self._explain_similarity(task, block, score)
                ))

        # Sort by similarity score (highest first)
        similar_blocks.sort(key=lambda x: x.similarity_score, reverse=True)

        self.logger.info(
            f"Found {len(similar_blocks)} similar blocks for task '{task[:50]}...'"
        )

        return similar_blocks

    async def _check_exact_match(
        self,
        block_type: str,
        include_code: bool
    ) -> Optional[SimilarBlock]:
        """Check if block_type already exists"""
        if not self.blocks_repository:
            return None

        try:
            existing = await self.blocks_repository.get_by_type(block_type)
            if existing:
                self.logger.warning(f"Exact match found for block_type: {block_type}")
                return SimilarBlock(
                    block_type=existing.get("block_type", ""),
                    name=existing.get("name", ""),
                    description=existing.get("description", ""),
                    category=existing.get("category", ""),
                    similarity_score=1.0,  # Perfect match
                    code=existing.get("code") if include_code else None,
                    manifest=existing.get("manifest"),
                    reason="Exact block_type match"
                )
        except Exception as e:
            self.logger.error(f"Error checking exact match: {e}")

        return None

    async def _find_category_blocks(
        self,
        category: str,
        include_code: bool
    ) -> List[Dict[str, Any]]:
        """Find all blocks in the same category"""
        if not self.blocks_repository:
            return []

        try:
            blocks = await self.blocks_repository.list_by_category(category)
            return blocks
        except Exception as e:
            self.logger.error(f"Error finding category blocks: {e}")
            return []

    def _calculate_similarity(
        self,
        task: str,
        block: Dict[str, Any]
    ) -> float:
        """
        Calculate similarity score between task and existing block

        Uses keyword-based similarity:
        1. Extract keywords from task
        2. Check presence in block name/description
        3. Weight by importance
        """
        score = 0.0
        max_score = 0.0

        task_lower = task.lower()
        block_name = block.get("name", "").lower()
        block_desc = block.get("description", "").lower()
        block_type = block.get("block_type", "").lower()

        # Extract keywords from task
        keywords = self._extract_keywords(task_lower)

        for keyword, weight in keywords.items():
            max_score += weight

            # Check in block_type (highest weight)
            if keyword in block_type:
                score += weight * 1.0

            # Check in name (high weight)
            elif keyword in block_name:
                score += weight * 0.8

            # Check in description (medium weight)
            elif keyword in block_desc:
                score += weight * 0.5

        # Normalize score
        if max_score > 0:
            score = score / max_score

        return min(score, 1.0)

    def _extract_keywords(self, text: str) -> Dict[str, float]:
        """
        Extract keywords with weights from text

        Higher weights for more specific/important terms
        """
        # Common workflow terms with weights
        important_terms = {
            # Operations
            "filter": 1.0,
            "sort": 1.0,
            "aggregate": 1.0,
            "merge": 1.0,
            "split": 1.0,
            "transform": 0.9,
            "parse": 0.9,
            "format": 0.9,
            "convert": 0.9,
            "validate": 0.9,
            # Data types
            "array": 0.8,
            "object": 0.8,
            "string": 0.8,
            "number": 0.8,
            "date": 0.8,
            "time": 0.8,
            "json": 0.8,
            "csv": 0.8,
            "xml": 0.8,
            # Control flow
            "if": 1.0,
            "condition": 0.9,
            "switch": 1.0,
            "loop": 1.0,
            "wait": 0.9,
            # Common functions
            "sum": 0.8,
            "count": 0.8,
            "average": 0.8,
            "min": 0.7,
            "max": 0.7,
        }

        keywords = {}

        # Find important terms in text
        for term, weight in important_terms.items():
            if term in text:
                keywords[term] = weight

        # Extract all significant words (longer than 3 chars)
        words = text.split()
        for word in words:
            cleaned = word.strip(",.!?;:")
            if len(cleaned) > 3 and cleaned not in keywords:
                keywords[cleaned] = 0.5  # Default weight for other words

        return keywords

    def _explain_similarity(
        self,
        task: str,
        block: Dict[str, Any],
        score: float
    ) -> str:
        """Generate human-readable explanation of why blocks are similar"""
        task_lower = task.lower()
        block_name = block.get("name", "")
        block_type = block.get("block_type", "")

        keywords = self._extract_keywords(task_lower)
        matching_keywords = [
            kw for kw in keywords.keys()
            if kw in block_name.lower() or kw in block_type.lower()
        ]

        if score >= 0.9:
            return f"Very similar: shares keywords {', '.join(matching_keywords[:3])}"
        elif score >= 0.7:
            return f"Similar functionality: {', '.join(matching_keywords[:2])}"
        elif score >= 0.5:
            return f"Related: same category with some overlap"
        else:
            return "Weak similarity"

    def create_template_from_similar(
        self,
        similar_blocks: List[SimilarBlock],
        task: str
    ) -> str:
        """
        Create a generation prompt using similar blocks as templates

        Returns:
            Enhanced prompt with template examples
        """
        if not similar_blocks:
            return task

        template_prompt = f"{task}\n\n"
        template_prompt += "Reference these existing similar blocks as templates:\n\n"

        for i, block in enumerate(similar_blocks[:3], 1):  # Top 3 most similar
            template_prompt += f"{i}. {block.name} ({block.block_type})\n"
            template_prompt += f"   Description: {block.description}\n"
            template_prompt += f"   Similarity: {block.similarity_score:.2f}\n"

            if block.code:
                # Include a snippet of the code structure
                code_lines = block.code.split("\n")[:10]  # First 10 lines
                template_prompt += f"   Code structure:\n"
                for line in code_lines:
                    template_prompt += f"   {line}\n"

            template_prompt += "\n"

        template_prompt += "\nCreate a similar block with these improvements:\n"
        template_prompt += "- Follow the same code structure and patterns\n"
        template_prompt += "- Use similar error handling approaches\n"
        template_prompt += "- Maintain consistency with existing blocks\n"
        template_prompt += "- Adapt the logic for the new requirements\n"

        return template_prompt


# Helper function for use in enhanced generator
async def check_and_use_similar_blocks(
    task: str,
    category: str,
    block_type: Optional[str],
    similarity_service: BlockSimilarityService
) -> Tuple[bool, str, List[SimilarBlock]]:
    """
    Check for similar blocks and enhance prompt if found

    Returns:
        (should_proceed, enhanced_prompt, similar_blocks)
        - should_proceed: False if exact match found
        - enhanced_prompt: Task with template examples
        - similar_blocks: List of similar blocks for reference
    """
    similar_blocks = await similarity_service.find_similar_blocks(
        task=task,
        category=category,
        block_type=block_type,
        include_code=True,
        threshold=0.6
    )

    # Check for exact match
    if similar_blocks and similar_blocks[0].similarity_score >= 0.99:
        return (
            False,  # Don't proceed
            f"Exact or near-exact match found: {similar_blocks[0].name}",
            similar_blocks
        )

    # If similar blocks found, use as templates
    if similar_blocks:
        enhanced_prompt = similarity_service.create_template_from_similar(
            similar_blocks,
            task
        )
        return (True, enhanced_prompt, similar_blocks)

    # No similar blocks, proceed with original task
    return (True, task, [])
