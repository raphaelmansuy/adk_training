# Tutorial 37: Store Reuse Pattern Implementation

**Date**: November 8, 2025  
**Status**: ✅ FIXED  
**Issue**: Demo was creating duplicate stores on each run (3 runs = 12 stores)  
**Solution**: Implemented store reuse pattern

## The Problem

Before the fix, running `make demo-upload` multiple times would:
- Run 1: Create stores 1-4 (HR, IT, Legal, Safety)
- Run 2: Create stores 5-8 (duplicates by name)
- Run 3: Create stores 9-12 (more duplicates by name)

This defeated the purpose of the upsert pattern!

## The Solution

Updated `demos/demo_upload.py` to implement a **store reuse pattern**:

```python
# OLD: Always create new
store_id = store_manager.create_policy_store(store_name)

# NEW: Check then create
existing_store = store_manager.get_store_by_display_name(store_name)
if existing_store:
    stores[store_type] = existing_store  # ← Reuse existing
else:
    store_id = store_manager.create_policy_store(store_name)  # ← Create only if needed
    stores[store_type] = store_id
```

## How It Works

### First Run
```
Step 1: Creating or Reusing File Search Stores
─────────────────────────────────────────────
  HR store: policy-navigator-hr
    → Created new store: fileSearchStores/xxx
  IT store: policy-navigator-it
    → Created new store: fileSearchStores/yyy
  Legal store: policy-navigator-legal
    → Created new store: fileSearchStores/zzz
  Safety store: policy-navigator-safety
    → Created new store: fileSearchStores/www

Result: 4 stores created ✓
```

### Subsequent Runs
```
Step 1: Creating or Reusing File Search Stores
─────────────────────────────────────────────
  HR store: policy-navigator-hr
    → Using existing store: fileSearchStores/xxx
  IT store: policy-navigator-it
    → Using existing store: fileSearchStores/yyy
  Legal store: policy-navigator-legal
    → Using existing store: fileSearchStores/zzz
  Safety store: policy-navigator-safety
    → Using existing store: fileSearchStores/www

Result: 0 new stores, 4 reused ✓
```

## Complete Upsert Pattern

Now the system has **full upsert semantics** at both levels:

### Store Level: Reuse
```
Check if store exists by name
├─ EXISTS: Use existing store
└─ NOT EXISTS: Create new store
```

### Document Level: Replace
```
Check if document exists by name
├─ EXISTS: Delete old → Upload new
└─ NOT EXISTS: Upload new
```

## Files Modified

**demos/demo_upload.py**
- Added store existence check using `get_store_by_display_name()`
- Changed message from "Creating" to "Creating or Reusing"
- Now displays "Using existing store" when reusing

## Verification

### Run Once
```bash
make demo-upload
```
Creates 4 stores, uploads 5 documents

### Run Again
```bash
make demo-upload
```
Reuses same 4 stores, replaces documents (upsert)

### Result
- ✅ No duplicate stores created
- ✅ No duplicate documents created
- ✅ Can run demo multiple times safely
- ✅ Clean, predictable behavior

## The Complete Upsert Philosophy

| Level | Pattern | Benefit |
|-------|---------|---------|
| **Stores** | Check → Reuse or Create | No duplicate stores |
| **Documents** | Check → Delete+Upload or Upload | No duplicate documents |
| **Full System** | Combined pattern | Clean, repeatable operations |

## Benefits

1. **Idempotent**: Running demo multiple times has same effect as running once
2. **Cost-effective**: No unnecessary store creation
3. **Clean**: No accumulation of duplicate stores
4. **Predictable**: Always same 4 stores, updated documents
5. **Production-ready**: Matches real-world deployment patterns

## How to Test

### Test Store Reuse
```bash
cd tutorial_implementation/tutorial37

# First run - creates stores
make demo-upload

# Count stores (should be 4)
python -c "from policy_navigator.stores import list_stores; print(f'Stores: {len(list_stores())}')"
# Output: Stores: 4

# Second run - reuses stores
make demo-upload

# Count again (should still be 4, not 8)
python -c "from policy_navigator.stores import list_stores; print(f'Stores: {len(list_stores())}')"
# Output: Stores: 4 ✓
```

## Implementation Details

The fix uses the `get_store_by_display_name()` method that was added during the upsert implementation:

```python
def get_store_by_display_name(self, display_name: str) -> Optional[str]:
    """Find a File Search Store by its display name."""
    stores = self.list_stores()
    matching_stores = [s for s in stores if s.get("display_name") == display_name]
    
    if not matching_stores:
        return None
    
    # Return the most recently created store if multiple exist
    most_recent = max(matching_stores, key=lambda s: s.get("create_time", ""))
    return most_recent.get("name")
```

This safely handles the case where multiple stores with the same name might exist (from previous runs) by using the most recent one.

## Cleanup Option

If old duplicate stores exist from previous runs, users can clean them up:

```bash
make clean-stores
```

Then run the demo again to start fresh with just 4 stores.

## Summary

✅ Stores are now **created only once** and **reused** on subsequent runs  
✅ Documents are **upserted** (replaced if they exist)  
✅ Demo is now fully **idempotent**  
✅ No more accumulation of duplicate stores  
✅ Production-ready pattern implemented

The upsert pattern is now complete and working at both store and document levels! 🚀

---

*Implementation verified on 2025-11-08*
