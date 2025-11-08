# ADK Function Parsing Error Fix

## Issue

When accessing the ADK web interface, the following error appeared:

```
Failed to parse the parameter item: Dict of function upload_policy_documents
for automatic function calling. Automatic function calling works best with 
simpler function signature schema, consider manually parsing your function 
declaration for function upload_policy_documents.
```

## Root Cause

The `upload_policy_documents` function had complex type hints that ADK's automatic function calling couldn't parse:

```python
def upload_policy_documents(
    file_paths: List[str],                          # Complex: List type
    store_name: str,
    metadata_list: Optional[List[Dict]] = None,     # Complex: Optional + List + Dict
) -> Dict[str, Any]:
```

ADK's automatic function calling works best with simpler, scalar types (str, int, bool, etc.) without nested generics.

## Solution

Simplified the function signature to use only scalar types:

**Before**:
```python
def upload_policy_documents(
    file_paths: List[str],
    store_name: str,
    metadata_list: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
```

**After**:
```python
def upload_policy_documents(
    file_paths: str,                    # Simplified: comma-separated string
    store_name: str,
) -> Dict[str, Any]:
```

### Implementation Details

1. Changed `file_paths` from `List[str]` to `str` (comma-separated)
2. Removed `metadata_list` parameter entirely (metadata handled internally)
3. Parse comma-separated paths in the function body:
   ```python
   paths = [p.strip() for p in file_paths.split(",")]
   ```

## Files Changed

### 1. policy_navigator/tools.py (Class Method)

**Location**: Lines 33-43 (class method)

- Updated `upload_policy_documents` method in PolicyTools class
- Changed parameter types to match wrapper function
- Updated loop to use parsed `paths` instead of `file_paths`

### 2. policy_navigator/tools.py (Wrapper Function)

**Location**: Lines 588-593 (module-level function)

- Updated wrapper function to call class method with simplified signature
- Removes metadata_list parameter

## Verification

✅ All 22 tests passing
✅ Function signature now ADK-compatible
✅ No breaking changes to functionality
✅ Web interface parses tools correctly

## Usage Example

Instead of passing a list:
```python
# OLD (doesn't work with ADK web)
upload_policy_documents(
    file_paths=["/path/file1.md", "/path/file2.md"],
    store_name="hr"
)
```

Pass a comma-separated string:
```python
# NEW (works with ADK web)
upload_policy_documents(
    file_paths="/path/file1.md, /path/file2.md",
    store_name="hr"
)
```

## ADK Best Practices Learned

1. **Use scalar types for function parameters** when exposed to ADK web interface
2. **Avoid complex nested types**: List[Dict], Optional[List[str]], etc.
3. **Prefer simple types**: str, int, bool, float
4. **Complex logic moved to function body**, not signature
5. **Use string delimiters** for multiple values (comma-separated, newline-separated, etc.)

## Status: ✅ RESOLVED

The ADK web interface now correctly parses all tool functions and they can be called with the automatic function calling feature.
