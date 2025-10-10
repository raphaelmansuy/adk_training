# Tutorial 16: Callback Signature Fixes - Complete

**Date**: 2025-10-10  
**Status**: ✅ Complete

## Summary

Fixed `before_tool_callback` signature issues in Tutorial 16 MCP agent to work with ADK 1.16.0's callback invocation mechanism.

## Issues Encountered

### Issue 1: Missing `tool` parameter
**Error**: `before_tool_callback() got an unexpected keyword argument 'tool'`

**Cause**: ADK 1.16.0 passes `tool` as the parameter name, not `tool_name` as used in older tutorials.

**Fix**: Changed function signature from:
```python
def before_tool_callback(callback_context, tool_name, args):
```

To:
```python
def before_tool_callback(callback_context, tool, args):
```

### Issue 2: Missing `tool_context` parameter  
**Error**: `before_tool_callback() got an unexpected keyword argument 'tool_context'`

**Cause**: ADK 1.16.0 also passes a `tool_context` parameter that wasn't in the function signature.

**Fix**: Added `tool_context` and `**kwargs` to accept any additional parameters:
```python
def before_tool_callback(
    callback_context: CallbackContext,
    tool: str,
    args: Dict[str, Any],
    tool_context: Any = None,
    **kwargs: Any
) -> Optional[Dict[str, Any]]:
```

## Root Cause Analysis

ADK's callback mechanism evolved between versions:
- **Older versions**: Used `tool_name` parameter
- **ADK 1.16.0**: Uses `tool` and adds `tool_context` parameter
- **Tutorial 09**: Still uses old signature (needs update)

The signature must match what ADK's `functions.py:305` passes in `_execute_single_function_call_async`.

## Changes Made

### File: `mcp_agent/agent.py`

**Before**:
```python
def before_tool_callback(
    callback_context: CallbackContext,
    tool_name: str,
    args: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
```

**After**:
```python
def before_tool_callback(
    callback_context: CallbackContext,
    tool: str,  # Changed from tool_name
    args: Dict[str, Any],
    tool_context: Any = None,  # Added
    **kwargs: Any  # Added for forward compatibility
) -> Optional[Dict[str, Any]]:
```

### Updated all references inside function:
- Changed `tool_name` → `tool` throughout function body
- Logger messages now use `tool` variable
- State keys now use `tool` variable

## Testing

✅ **All 39 tests passing**:
```bash
$ make test
============================== 39 passed in 2.59s ==============================
✅ All tests passed!
```

✅ **ADK web server working**: No more callback errors when using MCP tools

✅ **HITL functional**: Human-in-the-loop approval workflow works correctly

## Best Practices Applied

### 1. Forward Compatibility
Using `**kwargs` ensures the callback won't break if ADK adds more parameters in future versions:

```python
def before_tool_callback(
    callback_context,
    tool,
    args,
    tool_context=None,
    **kwargs  # Accept any future parameters
):
```

### 2. Optional Parameters
Made `tool_context` optional with default `None` since it may not always be provided:

```python
tool_context: Any = None
```

### 3. Type Hints
Maintained proper type hints for better IDE support and documentation:

```python
from typing import Dict, Any, Optional
```

## Lessons Learned

### 1. Check ADK Version
Different ADK versions may have different callback signatures. Always check:
```bash
python -c "import google.adk; print(google.adk.__version__)"
```

### 2. Use Flexible Signatures
When writing callbacks for frameworks, use `**kwargs` for resilience:
```python
def my_callback(..., **kwargs):  # Won't break on new params
```

### 3. Test Against Real Framework
Unit tests may pass, but integration with ADK web server revealed the actual signature mismatch.

### 4. Check Framework Source
When errors occur, trace back to framework source code to see exact invocation.

## Related Issues

### Tutorial 09 Needs Update
Tutorial 09 (`content_moderator`) still uses the old signature:
```python
def before_tool_callback(
    callback_context: CallbackContext,
    tool_name: str,  # Should be 'tool'
    args: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
```

**Recommendation**: Update Tutorial 09 to use the same signature for consistency.

## Verification Steps

1. ✅ Tests pass: `make test`
2. ✅ Agent starts: `make dev`
3. ✅ MCP tools work: Try "List files in sample_files"
4. ✅ HITL triggers: Try "Write a file" (should request approval)
5. ✅ No callback errors in logs

## Impact

- **Tutorial 16**: ✅ Fully working with ADK 1.16.0
- **Human-in-the-Loop**: ✅ Approval workflow functional
- **MCP Integration**: ✅ Filesystem operations working
- **ADK Compatibility**: ✅ Forward-compatible callback signature

## Files Modified

1. **`mcp_agent/agent.py`**:
   - Updated `before_tool_callback` signature
   - Changed all `tool_name` references to `tool`
   - Added `tool_context` and `**kwargs` parameters

## Next Steps

- [ ] Consider updating Tutorial 09 with same signature
- [ ] Document callback signature in ADK cheat sheet
- [ ] Add callback version compatibility note to tutorials

---

**Status**: ✅ Complete - All callback signature issues resolved
**Tests**: 39/39 passing  
**ADK Version**: 1.16.0
**Ready**: For production use
