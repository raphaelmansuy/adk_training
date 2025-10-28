# ADK TypedDict Compatibility Issue - Fixed

**Date**: October 27, 2025 14:39:21
**Project**: commerce_agent_e2e
**Issue**: ADK automatic function calling cannot parse TypedDict return types
**Status**: ✅ RESOLVED

## Problem

When using `ToolResult` TypedDict as a return type annotation in tool functions:

```python
from ..types import ToolResult

def save_preferences(...) -> ToolResult:
    return {"status": "success", ...}
```

ADK Web Server throws this error:

```
ValueError: Failed to parse the parameter return_value: commerce_agent.types.ToolResult 
of function save_preferences for automatic function calling. Automatic function calling 
works best with simpler function signature schema, consider manually parsing your 
function declaration for function save_preferences.
```

## Root Cause

ADK's automatic function calling parser in `_function_parameter_parse_util.py` cannot introspect TypedDict types to generate function declarations for the LLM. It only supports:
- Basic types: `str`, `int`, `float`, `bool`
- Simple generics: `List[str]`, `Dict[str, Any]`
- NOT supported: TypedDict, dataclass, Pydantic models (in return types)

## Solution

**Keep TypedDict definitions for documentation and type checking, but use `Dict[str, Any]` in function signatures:**

```python
from typing import Dict, Any
from ..types import ToolResult  # Import for reference

def save_preferences(...) -> Dict[str, Any]:  # ✅ ADK-compatible
    """Save user preferences.
    
    Returns:
        Dictionary matching ToolResult structure with status, report, and data
    """
    result: ToolResult = {  # Type hint for IDE/static analysis
        "status": "success",
        "report": "Preferences saved",
        "data": {...}
    }
    return result  # Returns dict, ADK can parse signature
```

## Changes Made

### 1. Updated `commerce_agent/tools/preferences.py`

**Before**:
```python
from ..types import ToolResult

def save_preferences(...) -> ToolResult:
    ...

def get_preferences(...) -> Dict[str, Any]:
    ...
```

**After**:
```python
from typing import Dict, Any
from ..types import ToolResult  # For reference only

def save_preferences(...) -> Dict[str, Any]:  # ADK-compatible
    ...

def get_preferences(...) -> Dict[str, Any]:
    ...
```

### 2. Updated `commerce_agent/types.py`

Added prominent warning in module docstring:

```python
"""
⚠️ IMPORTANT: ADK Compatibility Note
These TypedDict types cannot be used directly in function signatures for tools
that use ADK's automatic function calling. Use `Dict[str, Any]` in signatures
instead, but ensure the returned dictionary matches these structures.
"""
```

Added warning to `ToolResult` docstring:

```python
class ToolResult(TypedDict):
    """Standard return type for all tool functions.
    
    ⚠️ Do not use as return type annotation in tool function signatures.
    ADK's automatic function calling cannot parse TypedDict return types.
    Use `Dict[str, Any]` instead but ensure returned dict matches this structure.
    """
```

### 3. Updated Test Documentation

Changed test class docstring from:
```python
class TestPreferencesWithTypes:
    """Test that preference tools work with new type hints."""
```

To:
```python
class TestPreferencesWithTypes:
    """Test that preference tools return ToolResult-compatible dicts."""
```

## Verification

✅ All 14 tests passing
✅ ADK Web Server starts without errors
✅ Tools can be called from web interface
✅ TypedDict still available for documentation and IDE support

## Best Practice

**For ADK Tool Functions:**

1. **Function Signature**: Use `Dict[str, Any]` for return type
2. **Internal Type Hints**: Use TypedDict for local variables
3. **Documentation**: Document that return dict matches TypedDict structure
4. **Validation**: Tests verify structure matches TypedDict

**Example Pattern:**

```python
def my_tool(param: str, tool_context: ToolContext) -> Dict[str, Any]:
    """My tool function.
    
    Returns:
        Dictionary matching ToolResult structure:
        - status: "success" or "error"
        - report: Human-readable message
        - data: Result data
    """
    # Use TypedDict for type checking during development
    result: ToolResult = {
        "status": "success",
        "report": f"Processed {param}",
        "data": {"value": param}
    }
    return result  # Returns plain dict, ADK-compatible
```

## Lesson Learned

TypedDict is excellent for:
- ✅ Documentation
- ✅ IDE autocomplete
- ✅ Static type checking
- ✅ Code clarity

But NOT for:
- ❌ ADK tool function return type annotations
- ❌ Any runtime introspection scenarios

Always use `Dict[str, Any]` for tool signatures when using ADK's automatic function calling, and document the expected structure in docstrings and TypedDict definitions.

## Related Files

- `commerce_agent/tools/preferences.py` - Fixed signatures
- `commerce_agent/types.py` - Added warnings
- `tests/test_callback_and_types.py` - Updated test docs
- ADK source: `/research/adk-python/src/google/adk/tools/_function_parameter_parse_util.py` (parser that fails on TypedDict)

---

**Time to Diagnose**: 5 minutes (error was clear)
**Time to Fix**: 10 minutes (simple revert + documentation)
**Impact**: Critical (blocks web interface usage)
