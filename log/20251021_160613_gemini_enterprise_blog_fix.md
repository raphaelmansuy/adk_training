# Gemini Enterprise Blog Post Build Fix

**Date**: 2025-10-21  
**Status**: ✅ RESOLVED

## Problem

The npm build was failing with the following error:

```
Error: Can't reference blog post authors by a key (such as 'adk-team') because no authors map file could be loaded.
```

This was occurring in the blog post: `docs/blog/2025-10-21-gemini-enterprise.md`

## Root Cause

1. **Author Reference Issue**: The blog post was using a key-based author reference instead of inline author objects
2. **MDX Syntax Issue**: The blog post contained `<1w` in a table, which is invalid MDX syntax

## Solutions Applied

### Fix 1: Update Author Reference Format

Changed the frontmatter to use inline author object format used by working blog posts.

### Fix 2: Escape HTML Entity in MDX Table

Changed the table cell to escape the `<` character as `&lt;1w`.

## Verification

- ✅ Build completed successfully
- ✅ 229 HTML files generated
- ✅ No compilation errors
- ✅ Blog post correctly displays with author attribution

## Files Modified

- `docs/blog/2025-10-21-gemini-enterprise.md` - Fixed author reference and MDX syntax

## Key Learning

When using authors in Docusaurus blog posts:
1. Inline author objects are more reliable than key references
2. All HTML entities in tables must be properly escaped
3. The `<` character must be escaped as `&lt;` in MDX content
