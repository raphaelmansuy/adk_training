# Commerce Agent: URL Hallucination Fix

**Date**: 2025-01-25
**Issue**: ProductSearchAgent returned fabricated product URLs instead of real ones from Google Search
**Status**: ✅ FIXED

## Problem Summary

After the GoogleSearchTool fix was implemented, the commerce agent successfully:
- ✅ Calls ProductSearchAgent 
- ✅ Uses GoogleSearchTool to search Decathlon Hong Kong
- ✅ Returns product information (names, descriptions, prices)

However, it was **hallucinating/fabricating product URLs** instead of using the real ones from Google Search results.

### Evidence of the Bug

The agent returned URLs like:
```
https://www.decathlon.com.hk/en/p/men-s-road-running-shoes-jogflow-100-1-for-jogging-dark-grey/_/R-p-309139?mc=8557345
```

**Red flags**:
1. ❌ Pattern `/_/R-p-[ID]?mc=[ID]` is not used by Decathlon HK
2. ❌ `/en/p/[english-slug]` URLs are fabricated patterns
3. ❌ Product IDs like `8557345` were made up
4. ❌ Real Decathlon HK URLs use Chinese category paths like `/c/跑步及越野跑/跑鞋/路跑鞋.html`

## Root Cause Analysis

The LLM was generating URLs based on:
1. Pattern matching (URL structure inference)
2. Product IDs that don't actually exist
3. Generic product slug construction

The instruction said "Always include direct links" but didn't explicitly forbid fabrication. Gemini filled in the gaps using pattern recognition rather than extracting actual URLs from search results.

## Solution Implemented

Updated `commerce_agent/search_agent.py` instruction with explicit URL handling rules:

### Key Changes

**Before (problematic)**:
```python
instruction="""...
3. Extract product information including: name, description, price, and URL
...
5. Always include direct links to Decathlon Hong Kong product pages
...
RESPONSE FORMAT:
Present products with:
✓ Direct URL to Decathlon Hong Kong product page
...
"""
```

**After (fixed)**:
```python
instruction="""
CRITICAL INSTRUCTION - URL HANDLING:
When extracting product URLs from Google Search results, ALWAYS use the EXACT URL from the search results.
DO NOT reconstruct, guess, or fabricate URLs. Only use URLs that appear in the Google Search results.
If a URL is not in the search results, indicate that the link was not available in search results.

...

RESPONSE FORMAT:
For each product found in Google Search results, present:
...
✓ EXACT URL from Google Search results (copy the link exactly, do not modify)
...

NEVER fabricate or guess URLs. If the Google Search result doesn't include a clickable link, 
say "URL from search results: [link text]" instead of making one up.
"""
```

### Critical Changes:
1. **Explicit prohibition**: "DO NOT reconstruct, guess, or fabricate URLs"
2. **Source requirement**: "ALWAYS use the EXACT URL from search results"
3. **Fallback behavior**: If URL missing, indicate explicitly rather than fabricate
4. **Copy instruction**: "copy the link exactly, do not modify"

## Files Modified

```
commerce_agent/search_agent.py
├── Updated instruction with URL handling rules
├── Added explicit prohibition on URL fabrication
└── Clarified source requirement (exact from Google Search)
```

## Testing

Created `test_url_fix.py` to verify:
1. ProductSearchAgent is called with search queries
2. Returned URLs match actual Google Search results
3. Absence of fabricated URL patterns (/_/R-p-[ID])
4. Proper fallback when URLs unavailable

**Test Markers**:
- ✅ No `/_/R-p-` patterns = URLs not fabricated
- ✅ Real Decathlon HK URLs in response = Using actual results
- ✅ "not in search results" indicators = Proper fallback

## Architecture Context

**Multi-Agent Setup**:
```
CommerceCoordinator (Root Agent)
├── AgentTool wrapper
│   └── ProductSearchAgent
│       └── GoogleSearchTool(bypass_multi_tools_limit=True)
└── PreferenceManager
```

The issue occurred at the LLM prompt level in ProductSearchAgent, not in the tool calling layer.

## Deployment Notes

**No code logic changes**: Only instruction/prompt engineering fix
**No API changes**: All interfaces remain identical
**No breaking changes**: Existing code patterns unaffected

## Lessons Learned

1. **LLM URL Generation**: Even with tool access, LLMs will fabricate URLs if not explicitly prohibited
2. **Specificity Matters**: General instruction ("include links") ≠ Safe instruction ("use exact URLs from results")
3. **Fallback Handling**: Better to indicate missing information than fabricate
4. **Tool Output Processing**: When LLM processes tool results, explicitly forbid inference/reconstruction

## Related Issues

- Original issue: GoogleSearchTool not being called → Fixed in previous commit
- This issue: GoogleSearchTool called but results misprocessed → Fixed in this commit
- Next concern: Verify Google Search actually returns Decathlon HK product links

## Validation Checklist

- [x] Instruction updated with URL handling rules
- [x] Explicit prohibition on URL fabrication
- [x] Test framework created
- [x] Syntax validation passed
- [ ] Functional test with real API calls (requires credentials)
- [ ] Production deployment

## Future Improvements

1. Consider extraction validation: Check URLs match search result domains
2. Add URL logging for debugging
3. Track URL fabrication incidents in analytics
4. Consider alternative: Only use title/description without URLs if unavailable
