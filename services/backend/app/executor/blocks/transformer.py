"""Transformer block executor - Data manipulation and transformation"""

import json
import re
from typing import Any, Optional
from datetime import datetime
import hashlib

from app.core.logging import get_logger
from app.executor.state import WorkflowState

logger = get_logger(__name__)


class TransformerError(Exception):
    """Custom exception for transformer errors"""
    pass


async def execute_transformer_block(
    block: dict[str, Any], input_data: dict[str, Any], state: WorkflowState
) -> dict[str, Any]:
    """Execute a data transformer block

    Supports:
    - JSON operations (parse, stringify, extract, merge)
    - Text operations (uppercase, lowercase, trim, replace)
    - Array operations (map, filter, join, slice)
    - Object operations (pick, omit, merge, keys, values)
    - Type conversions (to_string, to_number, to_boolean, to_array)
    - Hashing (md5, sha256)
    - Date/time formatting
    """

    logger.info(
        "transformer_block_executing",
        block_id=block["id"],
        operation=input_data.get("operation"),
    )

    operation = input_data.get("operation", "identity")
    data = input_data.get("data")

    try:
        # Route to appropriate transformer function
        if operation == "json_parse":
            result = _json_parse(data)
        elif operation == "json_stringify":
            result = _json_stringify(data, input_data.get("pretty", False))
        elif operation == "json_extract":
            result = _json_extract(data, input_data.get("path"))
        elif operation == "json_merge":
            result = _json_merge(data, input_data.get("merge_with", {}))

        elif operation == "text_uppercase":
            result = _text_uppercase(data)
        elif operation == "text_lowercase":
            result = _text_lowercase(data)
        elif operation == "text_trim":
            result = _text_trim(data)
        elif operation == "text_replace":
            result = _text_replace(data, input_data.get("find"), input_data.get("replace"))
        elif operation == "text_split":
            result = _text_split(data, input_data.get("separator", ","))
        elif operation == "text_concat":
            result = _text_concat(data, input_data.get("values", []))

        elif operation == "array_map":
            result = _array_map(data, input_data.get("field"))
        elif operation == "array_filter":
            result = _array_filter(data, input_data.get("condition"))
        elif operation == "array_join":
            result = _array_join(data, input_data.get("separator", ","))
        elif operation == "array_slice":
            result = _array_slice(data, input_data.get("start", 0), input_data.get("end"))
        elif operation == "array_unique":
            result = _array_unique(data)
        elif operation == "array_flatten":
            result = _array_flatten(data)

        elif operation == "object_pick":
            result = _object_pick(data, input_data.get("keys", []))
        elif operation == "object_omit":
            result = _object_omit(data, input_data.get("keys", []))
        elif operation == "object_keys":
            result = _object_keys(data)
        elif operation == "object_values":
            result = _object_values(data)
        elif operation == "object_merge":
            result = _object_merge(data, input_data.get("merge_with", {}))

        elif operation == "to_string":
            result = _to_string(data)
        elif operation == "to_number":
            result = _to_number(data)
        elif operation == "to_boolean":
            result = _to_boolean(data)
        elif operation == "to_array":
            result = _to_array(data)

        elif operation == "hash_md5":
            result = _hash_md5(data)
        elif operation == "hash_sha256":
            result = _hash_sha256(data)

        elif operation == "date_format":
            result = _date_format(data, input_data.get("format", "%Y-%m-%d %H:%M:%S"))
        elif operation == "date_parse":
            result = _date_parse(data, input_data.get("format"))

        elif operation == "identity":
            result = data
        else:
            raise TransformerError(f"Unknown transformer operation: {operation}")

        logger.info("transformer_block_completed", block_id=block["id"], operation=operation)

        return {
            "result": result,
            "operation": operation,
            "input_type": type(data).__name__,
            "output_type": type(result).__name__,
        }

    except Exception as e:
        logger.error(
            "transformer_block_failed",
            block_id=block["id"],
            operation=operation,
            error=str(e),
            exc_info=True,
        )
        raise TransformerError(f"Transformer operation '{operation}' failed: {str(e)}") from e


# JSON Operations
def _json_parse(data: str) -> Any:
    """Parse JSON string to object"""
    if isinstance(data, str):
        return json.loads(data)
    return data


def _json_stringify(data: Any, pretty: bool = False) -> str:
    """Convert object to JSON string"""
    if pretty:
        return json.dumps(data, indent=2, ensure_ascii=False)
    return json.dumps(data, ensure_ascii=False)


def _json_extract(data: Any, path: Optional[str]) -> Any:
    """Extract value from JSON using dot notation path"""
    if not path:
        return data

    keys = path.split('.')
    result = data

    for key in keys:
        if isinstance(result, dict):
            result = result.get(key)
        elif isinstance(result, list) and key.isdigit():
            idx = int(key)
            result = result[idx] if 0 <= idx < len(result) else None
        else:
            return None

    return result


def _json_merge(data: dict, merge_with: dict) -> dict:
    """Merge two objects"""
    if not isinstance(data, dict):
        raise TransformerError("json_merge requires dict input")
    result = data.copy()
    result.update(merge_with)
    return result


# Text Operations
def _text_uppercase(data: str) -> str:
    """Convert text to uppercase"""
    return str(data).upper()


def _text_lowercase(data: str) -> str:
    """Convert text to lowercase"""
    return str(data).lower()


def _text_trim(data: str) -> str:
    """Trim whitespace from text"""
    return str(data).strip()


def _text_replace(data: str, find: Optional[str], replace: Optional[str]) -> str:
    """Replace text"""
    if not find:
        return str(data)
    return str(data).replace(find, replace or "")


def _text_split(data: str, separator: str) -> list[str]:
    """Split text into array"""
    return str(data).split(separator)


def _text_concat(data: Any, values: list[Any]) -> str:
    """Concatenate values"""
    all_values = [str(data)] + [str(v) for v in values]
    return "".join(all_values)


# Array Operations
def _array_map(data: list, field: Optional[str]) -> list:
    """Map array to extract field from each item"""
    if not isinstance(data, list):
        raise TransformerError("array_map requires list input")

    if not field:
        return data

    return [item.get(field) if isinstance(item, dict) else None for item in data]


def _array_filter(data: list, condition: Optional[dict]) -> list:
    """Filter array based on condition"""
    if not isinstance(data, list):
        raise TransformerError("array_filter requires list input")

    if not condition:
        return data

    # Simple filtering: {"field": "status", "value": "active"}
    field = condition.get("field")
    value = condition.get("value")

    if not field:
        return data

    return [
        item for item in data
        if isinstance(item, dict) and item.get(field) == value
    ]


def _array_join(data: list, separator: str) -> str:
    """Join array into string"""
    if not isinstance(data, list):
        raise TransformerError("array_join requires list input")
    return separator.join(str(item) for item in data)


def _array_slice(data: list, start: int, end: Optional[int]) -> list:
    """Slice array"""
    if not isinstance(data, list):
        raise TransformerError("array_slice requires list input")
    return data[start:end]


def _array_unique(data: list) -> list:
    """Get unique values from array"""
    if not isinstance(data, list):
        raise TransformerError("array_unique requires list input")

    # Preserve order while removing duplicates
    seen = set()
    result = []
    for item in data:
        # Convert unhashable types to strings for comparison
        key = json.dumps(item, sort_keys=True) if isinstance(item, (dict, list)) else item
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def _array_flatten(data: list) -> list:
    """Flatten nested arrays"""
    if not isinstance(data, list):
        raise TransformerError("array_flatten requires list input")

    result = []
    for item in data:
        if isinstance(item, list):
            result.extend(_array_flatten(item))
        else:
            result.append(item)
    return result


# Object Operations
def _object_pick(data: dict, keys: list[str]) -> dict:
    """Pick specific keys from object"""
    if not isinstance(data, dict):
        raise TransformerError("object_pick requires dict input")
    return {k: v for k, v in data.items() if k in keys}


def _object_omit(data: dict, keys: list[str]) -> dict:
    """Omit specific keys from object"""
    if not isinstance(data, dict):
        raise TransformerError("object_omit requires dict input")
    return {k: v for k, v in data.items() if k not in keys}


def _object_keys(data: dict) -> list[str]:
    """Get object keys"""
    if not isinstance(data, dict):
        raise TransformerError("object_keys requires dict input")
    return list(data.keys())


def _object_values(data: dict) -> list:
    """Get object values"""
    if not isinstance(data, dict):
        raise TransformerError("object_values requires dict input")
    return list(data.values())


def _object_merge(data: dict, merge_with: dict) -> dict:
    """Merge objects"""
    if not isinstance(data, dict):
        raise TransformerError("object_merge requires dict input")
    result = data.copy()
    result.update(merge_with)
    return result


# Type Conversions
def _to_string(data: Any) -> str:
    """Convert to string"""
    if isinstance(data, (dict, list)):
        return json.dumps(data)
    return str(data)


def _to_number(data: Any) -> float:
    """Convert to number"""
    if isinstance(data, (int, float)):
        return float(data)
    if isinstance(data, str):
        return float(data)
    raise TransformerError(f"Cannot convert {type(data).__name__} to number")


def _to_boolean(data: Any) -> bool:
    """Convert to boolean"""
    if isinstance(data, bool):
        return data
    if isinstance(data, str):
        return data.lower() in ['true', '1', 'yes', 'y']
    if isinstance(data, (int, float)):
        return bool(data)
    return bool(data)


def _to_array(data: Any) -> list:
    """Convert to array"""
    if isinstance(data, list):
        return data
    if isinstance(data, str):
        return [data]
    if isinstance(data, dict):
        return list(data.values())
    return [data]


# Hashing
def _hash_md5(data: Any) -> str:
    """Generate MD5 hash"""
    text = str(data)
    return hashlib.md5(text.encode()).hexdigest()


def _hash_sha256(data: Any) -> str:
    """Generate SHA256 hash"""
    text = str(data)
    return hashlib.sha256(text.encode()).hexdigest()


# Date/Time
def _date_format(data: Any, format_str: str) -> str:
    """Format datetime"""
    if isinstance(data, datetime):
        return data.strftime(format_str)
    if isinstance(data, str):
        # Try to parse ISO format
        dt = datetime.fromisoformat(data.replace('Z', '+00:00'))
        return dt.strftime(format_str)
    raise TransformerError("Invalid datetime input")


def _date_parse(data: str, format_str: Optional[str]) -> str:
    """Parse datetime string"""
    if format_str:
        dt = datetime.strptime(data, format_str)
    else:
        dt = datetime.fromisoformat(data.replace('Z', '+00:00'))
    return dt.isoformat()
