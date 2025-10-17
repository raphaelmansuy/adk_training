# Build Process Fix - Tutorial 23 Production Deployment

## Issue
Docusaurus build was failing with error:
```
Can't reference blog post authors by a key (such as 'team') because no authors map file could be loaded.
```

The blog post `2025-01-17-deploy-ai-agents.md` was using a reference to a global author key `team`, but:
1. No authors map file was configured in `docusaurus.config.ts`
2. Docusaurus wasn't able to load the authors configuration

## Root Cause
The `blog` plugin configuration in `docusaurus.config.ts` did not specify an `authorsMapPath`, causing Docusaurus to fail when processing blog posts that reference author keys.

## Solution
Changed the blog post author from a key reference to an inline author object:

**Before:**
```yaml
authors: [team]
```

**After:**
```yaml
authors:
  - name: ADK Training Team
    title: Google ADK Training
    url: https://github.com/raphaelmansuy/adk_training
    image_url: https://github.com/raphaelmansuy.png
```

## Changes Made
1. Updated `/docs/blog/2025-01-17-deploy-ai-agents.md` - Converted `authors` from global key reference to inline author object
2. Created `/docs/blog/authors.yml` - Global authors file (for future use if needed)
3. Updated `docusaurus.config.ts` - Added `authorsMapPath: 'blog/authors.yml'` configuration

## Result
✅ Build now succeeds
✅ Blog post renders correctly with author information
✅ Global authors file is configured for future blog posts

## Notes
- Inline authors provide the most reliable approach for blog post authorship
- The global authors file can be used for subsequent blog posts using the pattern: `authors: [team]` after initial implementation verification
- All Docusaurus build steps complete successfully without errors
