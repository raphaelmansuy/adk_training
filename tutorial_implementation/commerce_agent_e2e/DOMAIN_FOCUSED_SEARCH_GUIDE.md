# Domain-Focused Search Implementation Guide

## Overview

This guide explains how the Commerce Agent implements **Option 1: Prompt
Engineering Approach** for limiting Google Search results to Decathlon.fr
exclusively.

## The Challenge

When using the `google_search` tool with ADK, there's no built-in parameter to
limit results to specific domains. The `exclude_domains` parameter in the
google-genai SDK:

- ✅ Works on **Vertex AI backend**
- ❌ Does NOT work on **Gemini API backend**
- ❌ Only excludes domains (doesn't whitelist them)

## The Solution: Prompt Engineering

Rather than relying on backend-specific parameters, we use **prompt engineering**
to guide the search agent to construct site-restricted Google Search queries
using the `site:` operator.

### How It Works

```text
User Query
    ↓
Root Agent analyzes intent
    ↓
Search Agent receives instruction to use "site:decathlon.fr"
    ↓
Search Agent constructs: "site:decathlon.fr [user's product request]"
    ↓
Google Search (automatically limited to Decathlon.fr)
    ↓
Results presented to user (guaranteed Decathlon-only)
```

## Implementation Details

### 1. Search Agent Instruction Strategy

The `search_agent` instruction includes:

**PRIMARY METHOD - Site-Restricted Search:**

```text
"site:decathlon.fr running shoes"
"site:decathlon.fr women's yoga mat"
"site:decathlon.fr mountain bike helmet"
```

**CONTEXT-AWARE SEARCHING:**

```text
"site:decathlon.fr Kalenji running" (with brand)
"site:decathlon.fr €50 €100 trail shoes" (with price)
"site:decathlon.fr beginner cycling" (with activity level)
```

**DECATHLON-SPECIFIC TERMINOLOGY:**

The agent knows Decathlon's own brands:

- Kalenji - running shoes
- Quechua - hiking/outdoor gear
- Newfeel - urban sports
- Kiprun - trail running
- Rockrider - mountain biking
- Triban - road cycling

### 2. Root Agent Coordination

The `root_agent` reinforces the domain-focused strategy:

- Reminds search agent to use site-restricted queries
- Ensures user preferences inform targeted searches
- Validates that all recommendations are from Decathlon

### 3. Backend Compatibility

This approach works with:

- ✅ **Gemini API** (via Google AI Studio)
- ✅ **Vertex AI** (Google Cloud)
- ✅ **Both** simultaneously (no backend changes needed)

## Example Usage

### User: "I need running shoes"

**Search Agent Process:**

1. Receives user query: "I need running shoes"
2. Constructs search: `"site:decathlon.fr running shoes"`
3. Passes to Google Search tool
4. Receives Decathlon.fr results only
5. Formats and returns to user

### User: "Show me yoga mats around €40"

**Search Agent Process:**

1. Receives user query with price range
2. Constructs search: `"site:decathlon.fr yoga mat €40"`
3. Passes to Google Search tool
4. Receives Decathlon results in price range
5. Formats and returns to user

### User: "I'm a beginner cyclist, what do you recommend?"

**Search Agent Process:**

1. Preferences Agent notes: "beginner cyclist"
2. Search Agent constructs: `"site:decathlon.fr beginner cycling bike"`
3. Passes to Google Search tool
4. May also search for related gear: `"site:decathlon.fr cycling helmet"`
5. Storyteller creates engagement narrative
6. All results guaranteed from Decathlon.fr

## Fallback Handling

If an exact product isn't found on Decathlon:

```text
User: "Do you have Arc'teryx jackets?"
Search Agent: Searches "site:decathlon.fr Arc'teryx jacket"
Result: No Arc'teryx on Decathlon
Response: "We don't carry Arc'teryx, but here are similar high-quality 
outdoor jackets from Decathlon's Quechua brand..."
```

## Key Advantages

| Aspect | Benefit |
|--------|---------|
| **Backend Agnostic** | Works with Gemini API and Vertex AI equally |
| **No Config Changes** | No need to change authentication or deployment |
| **Natural Language** | Feels conversational, not robotic |
| **Extensible** | Easy to add more sites/filters if needed |
| **Transparent** | Clear why results are limited to Decathlon |
| **Reliable** | Uses Google's native `site:` operator |

## Troubleshooting

### Issue: Results include non-Decathlon sites

**Cause:** Search agent didn't include `site:decathlon.fr` in query

**Fix:** Check search agent instruction is clear about site: requirement

**Monitor:** Add logging to inspect actual search queries being constructed

### Issue: No results found

**Cause:** Exact product not on Decathlon, search query too specific

**Fix:** Search agent falls back to suggest similar Decathlon alternatives

**Example:** If user searches for specific non-Decathlon brand, agent suggests
closest Decathlon equivalent

### Issue: Results are slow

**Cause:** Multiple search queries for related products

**Fix:** Cache preference profile, batch related searches

## Testing the Implementation

### Test Cases

1. **Basic Product Search**
   - User: "Find me a running mat"
   - Expected: Results from decathlon.fr only

2. **Branded Product Search**
   - User: "Show me Kalenji shoes"
   - Expected: Decathlon Kalenji brand results

3. **Price-Constrained Search**
   - User: "Yoga mats under €50"
   - Expected: Decathlon yoga mats under €50

4. **Activity-Based Search**
   - User: "I want to start hiking"
   - Expected: Decathlon hiking gear recommendations

5. **Fallback Test**
   - User: "Do you have Nike products?"
   - Expected: "We don't carry Nike, here's what Decathlon offers..."

## Code Reference

### File: `commerce_agent/agent.py`

**Search Agent** (lines ~50-100):

- Contains detailed site-restricted search instructions
- Lists Decathlon brand names
- Defines fallback strategy

**Root Agent** (lines ~140-180):

- Orchestrates search agent
- Reinforces domain-focus requirement
- Coordinates with preference manager for context

## Future Enhancements

### Option: Migration to Vertex AI `exclude_domains`

If you later want to use Vertex AI's `exclude_domains` parameter:

```python
# Instead of prompt engineering, could use:
from google.genai.types import GoogleSearch, Tool

tool = Tool(
    google_search=GoogleSearch(
        exclude_domains=["amazon.com", "ebay.com", "sportdirect.com"]
    )
)
```

**Trade-offs:**

- ✅ More explicit control
- ❌ Only works on Vertex AI backend
- ❌ Excludes competitors rather than whitelisting Decathlon
- ❌ Requires backend migration

### Option: Custom Search Tool Wrapper

Could create a custom tool that:

1. Intercepts search queries
2. Always adds `site:decathlon.fr`
3. Post-processes results
4. Returns filtered results

```python
def decathlon_search(query: str) -> Dict[str, Any]:
    """Wrapper around google_search that forces Decathlon focus"""
    scoped_query = f"site:decathlon.fr {query}"
    results = google_search(scoped_query)
    return filter_to_decathlon_only(results)
```

**Trade-offs:**

- ✅ Maximum control
- ✅ Works on any backend
- ❌ Requires custom tool implementation
- ❌ More maintenance overhead

## Related Documentation

- [Google Search Grounding Guide](../../../docs/grounding/google_search_grounding/)
- [ADK Tools Documentation](https://google.github.io/adk-docs/tools/)
- [Agent Instruction Best Practices](../../../docs/skills/how_to_write_good_documentation.md)

## Summary

The Commerce Agent uses **prompt engineering** to achieve domain-focused searching:

1. **Search Agent** is instructed to use `site:decathlon.fr` queries
2. **Root Agent** ensures all searches follow this pattern
3. **Users** get guaranteed Decathlon-only results
4. **No backend changes** required - works with any platform
5. **Natural conversation** - feels like intelligent agent behavior

This approach is reliable, maintainable, and extensible for other e-commerce scenarios.
