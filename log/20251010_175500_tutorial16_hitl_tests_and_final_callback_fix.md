# Tutorial 16: Human-in-the-Loop Tests and Callback Signature Fix - Complete

**Date**: 2025-10-10  
**Status**: ✅ Complete  
**Tests**: 64/64 passing (39 original + 25 new HITL tests)

## Summary

Fixed ADK 1.16.0 callback signature compatibility issue and added comprehensive Human-in-the-Loop (HITL) test coverage. The callback now correctly handles tool objects instead of tool names, and all edge cases are thoroughly tested.

## Critical Discovery

### ADK 1.16.0 Callback Signature

The actual ADK 1.16.0 callback signature is:

```python
def before_tool_callback(
    tool,  # BaseTool object, not string!
    args: Dict[str, Any],
    tool_context  # ToolContext with state access
) -> Optional[Dict[str, Any]]:
```

**Key Points**:
1. **NO `callback_context` parameter** - this was removed in ADK 1.16.0
2. **`tool` is an object**, not a string - must extract `.name` attribute
3. **`tool_context.state`** replaces `callback_context.state` for state access
4. **`tool_context`** provides session, invocation_id, and other context

### Evolution from Tutorial 09

Tutorial 09 (older ADK version) used:
```python
def before_tool_callback(
    callback_context: CallbackContext,  # Removed in 1.16.0
    tool_name: str,  # Changed to tool object
    args: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
```

## Issues Fixed

### Issue 1: Missing callback_context Parameter

**Error**:
```
TypeError: before_tool_callback() missing 1 required positional argument: 'callback_context'
```

**Root Cause**: ADK 1.16.0 doesn't pass `callback_context` - it passes `tool`, `args`, and `tool_context`.

**Fix**: Removed `callback_context` parameter and used `tool_context.state` instead:

```python
# Before (broken)
def before_tool_callback(
    callback_context: CallbackContext,
    tool: str,
    args: Dict[str, Any],
    tool_context: Any = None
) -> Optional[Dict[str, Any]]:
    tool_count = callback_context.state.get('temp:tool_count', 0)
    
# After (working)
def before_tool_callback(
    tool,  # Tool object, not string
    args: Dict[str, Any],
    tool_context  # Has .state attribute
) -> Optional[Dict[str, Any]]:
    tool_count = tool_context.state.get('temp:tool_count', 0)
```

### Issue 2: Tool Parameter is Object, Not String

**Error**: Logs showed:
```
[TOOL REQUEST] <google.adk.tools.mcp_tool.mcp_tool.MCPTool object at 0x113fda6f0> with args: ...
```

**Root Cause**: The `tool` parameter is a `BaseTool` object, not a string.

**Fix**: Extract tool name from object:

```python
def before_tool_callback(
    tool,  # This is a BaseTool object!
    args: Dict[str, Any],
    tool_context
) -> Optional[Dict[str, Any]]:
    # Extract tool name from tool object
    tool_name = tool.name if hasattr(tool, 'name') else str(tool)
    
    logger.info(f"[TOOL REQUEST] {tool_name} with args: {args}")
    # ... rest of callback logic uses tool_name string
```

### Issue 3: None Values in State

**Error**: Test failure with `TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'`

**Root Cause**: `state.get()` can return `None` if value is explicitly set to `None`.

**Fix**: Added `or 0` fallback:

```python
# Before (failed on None)
tool_count = tool_context.state.get('temp:tool_count', 0)

# After (handles None)
tool_count = tool_context.state.get('temp:tool_count', 0) or 0
```

## Changes Made

### File: `mcp_agent/agent.py`

**Callback Signature**:
```python
def before_tool_callback(
    tool,  # BaseTool object (not string, not callback_context)
    args: Dict[str, Any],
    tool_context  # Replaces callback_context for state access
) -> Optional[Dict[str, Any]]:
    # Extract tool name from object
    tool_name = tool.name if hasattr(tool, 'name') else str(tool)
    
    logger.info(f"[TOOL REQUEST] {tool_name} with args: {args}")
    
    # Use tool_context.state instead of callback_context.state
    tool_count = tool_context.state.get('temp:tool_count', 0) or 0
    tool_context.state['temp:tool_count'] = tool_count + 1
    tool_context.state['temp:last_tool'] = tool_name
    
    # Check destructive operations
    DESTRUCTIVE_OPERATIONS = {
        'write_file': 'Writing files modifies content',
        'write_text_file': 'Writing files modifies content',
        'move_file': 'Moving files changes file locations',
        'create_directory': 'Creating directories modifies filesystem structure',
    }
    
    if tool_name in DESTRUCTIVE_OPERATIONS:
        auto_approve = tool_context.state.get('user:auto_approve_file_ops', False)
        if not auto_approve:
            return {
                'status': 'requires_approval',
                'message': f"⚠️ APPROVAL REQUIRED...",
                'tool_name': tool_name,
                'args': args,
                'requires_approval': True
            }
    
    return None  # Allow execution
```

**Removed Import**:
```python
# Removed: from google.adk.agents.callback_context import CallbackContext
# Not used in ADK 1.16.0
```

### File: `tests/test_hitl.py` (NEW)

Created comprehensive test suite with 25 tests covering:

#### 1. Tool Name Extraction (2 tests)
- Test extraction from tool object with `.name` attribute
- Test fallback to string representation for objects without `.name`

#### 2. Destructive Operation Detection (8 tests)
- Parameterized tests for all 4 destructive operations (write, move, create)
- Parameterized tests for 4 safe operations (read, list, search, get_info)
- Verify destructive operations are blocked without approval
- Verify safe operations are allowed automatically

#### 3. Approval Workflow (3 tests)
- Auto-approve flag bypasses approval
- Missing auto-approve flag blocks operations
- Explicitly `False` auto-approve flag blocks operations

#### 4. State Management (3 tests)
- Tool count increments correctly across multiple calls
- Last tool name is tracked in state
- State persists across callback invocations

#### 5. Approval Message Content (4 tests)
- Message includes operation name
- Message includes reason for blocking
- Message includes tool arguments
- Message includes approval instructions

#### 6. Edge Cases (3 tests)
- Empty args dictionary handled gracefully
- `None` values in state handled correctly
- Unknown tool names allowed by default

#### 7. Integration Scenarios (2 tests)
- Workflow: read (allowed) → write (blocked) → enable approval → write (allowed)
- Multiple destructive operations all blocked correctly

## Test Results

### Before (39 tests)
```
============================== 39 passed in 2.59s ==============================
```

### After (64 tests)
```
============================== 64 passed in 2.32s ==============================
```

**New Tests**:
- 25 HITL-specific tests
- All parameterized for comprehensive coverage
- Mock-based unit tests (no external dependencies)
- Fast execution (< 3 seconds total)

## Verified Functionality

### ✅ Callback Invocation
- Correct signature: `(tool, args, tool_context)`
- Tool object properly handled
- Tool name extracted successfully
- State accessed via `tool_context.state`

### ✅ HITL Workflow
- Destructive operations blocked: `write_file`, `write_text_file`, `move_file`, `create_directory`
- Safe operations allowed: `read_file`, `list_directory`, `search_files`, `get_file_info`
- Auto-approve flag works correctly
- Tool usage tracking operational

### ✅ Real ADK Server
From server logs:
```
2025-10-10 17:55:23,896 - INFO - agent.py:64 - [TOOL REQUEST] write_file with args: ...
2025-10-10 17:55:23,896 - WARNING - agent.py:84 - [APPROVAL REQUIRED] write_file: Writing files modifies content
```

Tool name extraction working, HITL blocking triggered correctly!

## Best Practices Applied

### 1. Defensive Coding
```python
tool_name = tool.name if hasattr(tool, 'name') else str(tool)
tool_count = tool_context.state.get('temp:tool_count', 0) or 0  # Handle None
```

### 2. Comprehensive Testing
- Unit tests for individual functions
- Integration tests for workflows
- Edge case handling
- Parameterized tests for reusability

### 3. Clear Documentation
- Docstrings explain callback purpose
- Test descriptions are descriptive
- Comments explain non-obvious logic

## ADK Version Compatibility Matrix

| ADK Version | callback_context | tool Parameter | State Access |
|-------------|------------------|----------------|--------------|
| < 1.16.0    | First parameter  | String name    | callback_context.state |
| ≥ 1.16.0    | Not passed       | Tool object    | tool_context.state |

## Migration Guide

### From Tutorial 09 Signature to ADK 1.16.0

```python
# OLD (Tutorial 09 / ADK < 1.16.0)
def before_tool_callback(
    callback_context: CallbackContext,
    tool_name: str,
    args: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    count = callback_context.state.get('tool_count', 0)
    callback_context.state['tool_count'] = count + 1
    
    if tool_name in DESTRUCTIVE_OPS:
        # Check approval
        pass
    return None

# NEW (ADK 1.16.0+)
def before_tool_callback(
    tool,  # Object, not string!
    args: Dict[str, Any],
    tool_context  # Replaces callback_context
) -> Optional[Dict[str, Any]]:
    tool_name = tool.name if hasattr(tool, 'name') else str(tool)
    count = tool_context.state.get('tool_count', 0) or 0  # Handle None
    tool_context.state['tool_count'] = count + 1
    
    if tool_name in DESTRUCTIVE_OPS:
        # Check approval
        pass
    return None
```

## Files Modified

1. **`mcp_agent/agent.py`**:
   - Updated `before_tool_callback` signature
   - Removed `callback_context` parameter
   - Added tool name extraction logic
   - Changed `callback_context.state` to `tool_context.state`
   - Added None handling for state values
   - Removed `CallbackContext` import

2. **`tests/test_hitl.py`** (NEW):
   - 25 comprehensive HITL tests
   - 7 test classes organized by functionality
   - Parameterized tests for efficiency
   - Mock-based for fast execution

## Lessons Learned

### 1. Always Check Current ADK Version Signatures
Documentation may be outdated. Check actual invocation in ADK source code:
```bash
grep -A 10 "function_response = callback(" \
  ~/.venv/lib/python3.12/site-packages/google/adk/flows/llm_flows/functions.py
```

### 2. Tool Parameter is an Object
ADK passes the full `BaseTool` object to callbacks, not just the name string. Always extract the name:
```python
tool_name = tool.name if hasattr(tool, 'name') else str(tool)
```

### 3. State Access Changed
- Old: `callback_context.state`
- New: `tool_context.state`

Both provide same interface, but callback_context is no longer passed to callbacks.

### 4. Test Against Real Framework
Unit tests may pass, but integration with ADK web server revealed actual signature mismatch. Always test with `adk web` or `adk dev`.

### 5. Handle None in State
State values can be explicitly set to `None`. Always use fallback:
```python
value = state.get('key', default) or default
```

## Next Steps

- ✅ Tutorial 16 fully functional with ADK 1.16.0
- ✅ Human-in-the-Loop approval workflow operational
- ✅ Comprehensive test coverage (64 tests)
- ⏭️ Consider updating Tutorial 09 with same signature for consistency
- ⏭️ Document callback signature evolution in ADK cheat sheet

## Impact

- **Tutorial 16**: ✅ Production-ready with ADK 1.16.0
- **HITL**: ✅ Fully tested approval workflow
- **MCP Integration**: ✅ Filesystem operations secured
- **Test Coverage**: ✅ 64 tests covering all scenarios
- **ADK Compatibility**: ✅ Forward-compatible with ADK 1.16.0+

---

**Status**: ✅ Complete - All callback signature issues resolved, comprehensive HITL tests added  
**Tests**: 64/64 passing  
**ADK Version**: 1.16.0  
**Ready**: For production use with full HITL approval workflow
