# 20251014_085443_blog_links_fixed_complete

## Summary
Fixed all broken tutorial links in the blog article `docs/blog/2025-10-14-tutorial-progress-update.md`. 

## Problem
The blog article contained incorrect URLs with `/docs/tutorial/XX_name` pattern, but the actual Docusaurus site uses `/docs/name` URLs based on the sidebar configuration.

## Solution
Updated all 23 tutorial links to remove the `/tutorial/` path segment and the `XX_` prefix from the URLs. The links now correctly point to:
- `https://raphaelmansuy.github.io/adk_training/docs/hello_world_agent` (instead of `/docs/tutorial/01_hello_world_agent`)
- And similarly for all other tutorials

## Files Modified
- `docs/blog/2025-10-14-tutorial-progress-update.md` - Fixed 23 broken tutorial links

## Verification
- Confirmed URL structure matches Docusaurus sidebar configuration in `docs/sidebars.ts`
- All tutorial IDs in sidebar use clean names without numeric prefixes
- No remaining `/docs/tutorial/` links found in the blog article