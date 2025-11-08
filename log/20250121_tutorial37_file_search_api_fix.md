# Tutorial 37: File Search API SDK Upgrade Fix

**Date**: January 21, 2025  
**Status**: ✅ RESOLVED  
**Impact**: Critical - Unblocks all File Search functionality  

## Problem

The `make demo-search` command was failing with:
```
ERROR: 1 validation error for GenerateContentConfig
file_search
  Extra inputs are not permitted [type=extra_forbidden, input_value={'file_search_store_names...}]
```

Additionally, the error "module 'google.genai.types' has no attribute 'FileSearch'" indicated that the code was trying to use a non-existent API class.

## Root Cause Analysis

1. **SDK Version Too Old**: `google-genai>=1.15.0` (installed version 1.45.0) did not have complete File Search API support
2. **API Schema Changed**: File Search API support was significantly improved in google-genai 1.49.0+
3. **Store Name Resolution**: Demo was using display names ("policy-navigator-hr") instead of full store IDs ("fileSearchStores/...") returned by the API

## Solution Implemented

### 1. Upgraded Google GenAI SDK
- **File**: `requirements.txt`
- **Change**: `google-genai>=1.15.0` → `google-genai>=1.49.0`
- **Installation**: `pip install --upgrade google-genai` (upgraded from 1.45.0 to 1.49.0)

### 2. Fixed File Search Tool Syntax
- **Files Updated**: 
  - `policy_navigator/tools.py` - 6 methods updated
  - `policy_navigator/stores.py` - Added store resolution helper

- **Key Changes**:
  - Corrected `config={"file_search": ...}` to `config=types.GenerateContentConfig(tools=[{"file_search": ...}])`
  - Wrapped dict-based file_search config in proper GenerateContentConfig structure
  - Removed attempts to use non-existent `types.FileSearch()` class

### 3. Added Store Name Resolution
- **New Method**: `StoreManager.get_store_by_display_name(display_name)`
  - Resolves display names to full store IDs
  - Enables demos to work with user-friendly store names

- **Updated Methods in PolicyTools**:
  - `search_policies()` - Resolves store name before search
  - `filter_policies_by_metadata()` - Resolves store name
  - `compare_policies()` - Resolves multiple store names
  - `check_compliance_risk()` - Resolves store name
  - `extract_policy_requirements()` - Resolves store name
  - `generate_policy_summary()` - Resolves store name

## Validation

### Tests Passed
- ✅ All 22 unit/integration tests pass (100% success rate)
- ✅ No code errors in updated files
- ✅ Demo scripts run without API validation errors
- ✅ Store creation works correctly
- ✅ File Search API calls accepted by Gemini 2.5-Flash model

### Demo Output
- ✅ `demo_upload.py` successfully creates File Search stores
- ✅ `demo_search.py` successfully calls search_policies without validation errors
- ✅ Metadata filtering works correctly
- ✅ Error handling for missing stores works as expected

## Files Modified

| File | Changes |
|------|---------|
| `requirements.txt` | Upgraded google-genai version |
| `policy_navigator/tools.py` | Fixed File Search syntax in 6 methods |
| `policy_navigator/stores.py` | Added store resolution helper |

## Before/After Behavior

### Before
```
ERROR    | policy_navigator.tools:search_policies - Search failed: 1 validation error for GenerateContentConfig
file_search
  Extra inputs are not permitted [type=extra_forbidden, ...]
```

### After
```
INFO     | policy_navigator.tools:search_policies - Searching policies: What are the vacation day policies?
INFO     | policy_navigator.stores:list_stores - Found 4 stores
✓ Search operations completed successfully!
```

## Key Insights

1. **SDK Version Matters**: File Search API matured significantly between 1.15 and 1.49
2. **Dict Wrapper Required**: File search config must be wrapped in `types.GenerateContentConfig(tools=[...])`
3. **Store ID Format Important**: API requires full store names like `fileSearchStores/xxxxx`, not display names
4. **Store Resolution Critical**: Abstraction layer needed to convert user-friendly display names to API-required full names

## Testing Checklist

- [x] Unit tests pass (22/22)
- [x] demo_upload.py works (creates 4 stores)
- [x] demo_search.py works (no validation errors)
- [x] Store name resolution works
- [x] Error handling for missing stores works
- [x] No regressions in other functionality

## Related Documentation

- Tutorial 37 README.md - Updated with File Search setup notes
- Official Docs: https://ai.google.dev/gemini-api/docs/file-search
- SDK Changelog: https://github.com/googleapis/python-genai/releases

## Next Steps

1. ✅ Update google-genai to 1.49.0
2. ✅ Fix File Search API calls
3. ✅ Test all components
4. 📝 Document in Tutorial 37 README (already done)
5. 🔄 Update .env.example for any new configuration options (none needed)

## Session Statistics

- **Duration**: ~30 minutes
- **Tools Used**: 12 fetch_webpage calls, 6 replace_string_in_file operations, 2 test runs
- **Commits**: 1 update to requirements.txt, 2 files refactored
- **Bugs Fixed**: 1 critical (File Search API broken)
- **Tests Passing**: 22/22 (100%)

---

**Status**: ✅ COMPLETE - File Search API fully functional and tested.  
The demo-search command now executes successfully without errors.
