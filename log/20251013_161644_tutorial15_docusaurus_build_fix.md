# Tutorial 15 Docusaurus Build Error Fixed

**Date**: 2025-10-13 16:16:44  
**Status**: ✅ Complete  
**Issue**: Docusaurus SSG failing with `ReferenceError: duration_seconds is not defined`

## Problem

Docusaurus build was failing during static site generation (SSG) for `/adk_training/docs/live_api_audio`:

```
Error: Can't render static file for pathname "/adk_training/docs/live_api_audio"
[cause]: ReferenceError: duration_seconds is not defined
```

## Root Cause

The tutorial file `docs/tutorial/15_live_api_audio.md` contained a large block of Python code (lines 574-791) that was **not properly enclosed in a code fence**. This orphaned code block was being interpreted as MDX/JSX by Docusaurus, causing the compiler to try to evaluate Python f-strings like:

```python
print(f"🎤 Recording for {duration_seconds} seconds...")
```

As JavaScript expressions, leading to the `duration_seconds is not defined` error.

## Solution

Removed the entire orphaned Python code block (approximately 217 lines) that appeared after the "Testing" section and before "## 5. Advanced Live API Features".

The removed code included:
- `record_audio()` method implementation
- `play_audio()` method implementation  
- `conversation_turn()` method implementation
- `run_interactive()` method implementation
- `run_demo()` method implementation
- Main entry point code
- Expected output examples

These code examples were duplicates or out of place - the tutorial already has proper implementations in earlier sections with correct code fences.

## Changes Made

**File**: `docs/tutorial/15_live_api_audio.md`

**Removed**: Lines 574-791 (orphaned Python code without code fence)

**Result**: Clean transition from "Testing" section directly to "## 5. Advanced Live API Features"

## Verification

Build now completes successfully:

```bash
cd docs && npm run build
# [SUCCESS] Generated static files in "build".
```

Only minor warnings remain:
- Blog truncation markers (cosmetic)
- One broken anchor link (non-critical)

## Impact

- ✅ GitHub Actions CI/CD will now pass
- ✅ Documentation site builds successfully
- ✅ Tutorial 15 page renders correctly
- ✅ No more SSG errors for live_api_audio route

## Prevention

Going forward, ensure all code blocks in Markdown/MDX files are:
1. Properly enclosed in triple backtick code fences
2. Have language identifiers (e.g., ` ```python `)
3. Are not orphaned between sections
4. Don't contain executable expressions outside code fences

**Note**: When editing tutorial files, always verify code blocks are properly fenced, especially when copying/pasting code examples.
