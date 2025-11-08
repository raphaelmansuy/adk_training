# Makefile Enhancement - Clean Stores Command

**Date**: 2025-01-08  
**Status**: ✅ COMPLETE

## What Was Added

A new `make clean-stores` command to delete all File Search stores and start from a fresh state.

## Files Created/Modified

### 1. **Makefile** - Added new command documentation and target
- Added `clean-stores` to help text
- Added `clean-stores` target that calls the cleanup script

### 2. **scripts/cleanup_stores.py** - New cleanup script
- Lists all File Search stores
- Deletes each store with force=True to remove stored documents
- Provides detailed progress reporting
- Gracefully handles errors

### 3. **policy_navigator/stores.py** - Enhanced delete_store method
- Added `force` parameter to `delete_store()` method
- Uses `DeleteFileSearchStoreConfig` to pass force flag to API
- Added `from google.genai import types` import

## Usage

```bash
# Delete all File Search stores and start fresh
make clean-stores

# Then recreate stores and upload files
make demo-upload

# Test searches
make demo-search
```

## How It Works

1. `make clean-stores` calls the cleanup script
2. Script lists all File Search stores in the account
3. For each store, it calls `delete_store(name, force=True)`
4. Force flag removes documents stored in the store before deletion
5. Script reports success/failure for each store

## Test Results

- ✅ All 22 tests pass
- ✅ Successfully deleted 10+ stores with documents
- ✅ `demo-upload` works after cleanup
- ✅ `demo-search` works after cleanup

## Key Technical Details

### Force Delete Implementation
```python
def delete_store(self, store_name: str, force: bool = False) -> bool:
    config = None
    if force:
        config = types.DeleteFileSearchStoreConfig(force=True)
    self.client.file_search_stores.delete(name=store_name, config=config)
```

The REST API requires `force` as a query parameter, which the Python SDK wraps in a `DeleteFileSearchStoreConfig` object.

## Benefits

- ✅ **Fresh Start**: Can reset entire File Search environment
- ✅ **Development**: Useful during testing and development cycles
- ✅ **Cleanup**: Remove old test stores cluttering the account
- ✅ **Documentation**: Clear help text for users

## Next Steps (Optional)

1. Add automatic cleanup to CI/CD pipeline
2. Add --dry-run option to see what will be deleted
3. Add --filter option to delete only specific stores
4. Add interactive confirmation before deletion

---

**Summary**: Tutorial 37 now has a `make clean-stores` command for resetting the File Search environment to a fresh state. Useful for development and testing workflows.
