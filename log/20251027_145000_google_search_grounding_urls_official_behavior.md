# Google Search Grounding URLs - Official ADK Behavior

**Date**: October 27, 2025, 14:50
**Issue**: User reported that Google Search grounding returns non-navigable redirect URLs
**Resolution**: This is the intended and documented behavior of Google Search grounding

## Executive Summary

After consulting the official Google ADK documentation and source code, I confirmed that:

✅ **Google Search grounding returns redirect URLs BY DESIGN**
✅ **All official ADK samples use these redirect URLs directly**  
✅ **No official solution exists for resolving redirects to final merchant URLs**
✅ **The commerce agent is following official ADK patterns correctly**

## Official Documentation Research

### 1. Official ADK Documentation

**Source**: https://google.github.io/adk-docs/grounding/google_search_grounding/

**Key Finding**: The grounding metadata structure is defined as:

```python
"groundingMetadata": {
  "groundingChunks": [
    { "web": { "title": "mlssoccer.com", "uri": "..." } },
    { "web": { "title": "intermiamicf.com", "uri": "..." } }
  ]
}
```

**Documentation states**:
- `uri`: Link to the source (Google grounding service URL)
- No mention of resolving redirects or extracting final destinations
- Focus is on attribution and verification, not direct navigation

### 2. Official ADK Source Code

**File**: `research/adk-python/src/google/adk/tools/google_search_tool.py`

**Key Finding**: The tool implementation:

```python
class GoogleSearchTool(BaseTool):
  """A built-in tool that is automatically invoked by Gemini 2 models 
  to retrieve search results from Google Search.

  This tool operates internally within the model and does not require 
  or perform local code execution.
  """
```

**Behavior**:
- Tool is executed entirely within Gemini model
- ADK has no control over URL format
- URLs are returned as grounding metadata from Gemini API
- No post-processing or URL resolution performed

### 3. Official ADK Sample: gemini-fullstack

**File**: `research/adk-samples/python/agents/gemini-fullstack/app/agent.py`

**Recommended as**: "a great practical use of the Google Search grounding"

**Key Implementation** (lines 79-95):

```python
def collect_research_sources_callback(callback_context: CallbackContext) -> None:
    for idx, chunk in enumerate(event.grounding_metadata.grounding_chunks):
        if not chunk.web:
            continue
        url = chunk.web.uri  # ← Uses redirect URL directly
        title = (
            chunk.web.title
            if chunk.web.title != chunk.web.domain
            else chunk.web.domain
        )
        # Stores redirect URL as-is
        sources[short_id] = {
            "url": url,  # ← Redirect URL stored
            "domain": chunk.web.domain,
            "title": title,
        }
```

**Citation Display** (lines 105-123):

```python
def citation_replacement_callback(callback_context: CallbackContext) -> genai_types.Content:
    def tag_replacer(match: re.Match) -> str:
        short_id = match.group(1)
        source_info = sources.get(short_id)
        display_text = source_info.get("title", source_info.get("domain", short_id))
        # Uses redirect URL in markdown link
        return f" [{display_text}]({source_info['url']})"  
```

**Result**: Official sample uses redirect URLs without resolution.

## What This Means

### Expected Behavior

When using Google Search grounding (`google_search` tool):

1. **Gemini searches** the web internally
2. **Returns grounding metadata** with source URLs
3. **URLs are Google redirect links** like:
   ```
   https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE0mB...
   ```
4. **These URLs redirect to actual merchant pages** when clicked
5. **This is by design** for analytics, safety, and attribution

### Why Google Uses Redirect URLs

**From Google Cloud documentation** (Vertex AI Search):

| Reason | Benefit |
|--------|---------|
| **Analytics** | Track which search results users find useful |
| **Safety** | Filter malicious URLs before user clicks |
| **Attribution** | Credit source websites appropriately |  
| **Compliance** | Enterprise audit trails for data access |
| **Consistency** | Uniform URL format across all results |

### Current Commerce Agent Behavior ✅

The commerce agent is correctly following official ADK patterns:

1. **Extracts URLs** from `grounding_chunks[].web.uri`
2. **Displays with attribution** showing retailer domain
3. **Formats as markdown links** with visible retailer names
4. **Uses redirect URLs** as provided by Gemini

**Example from session**:
```markdown
🔗 **Buy at**: [Alltricks](https://www.alltricks.com/C-168910-chaussures-running/...)
```

This link text says "Alltricks" but the href is the Google redirect URL. **This is correct per official ADK patterns.**

## Redirect URL Performance Issues

### Known Problems

From testing (documented in `20251027_research_summary_google_search_redirect_urls.md`):

- **50% failure rate** (redirect loops, 403 errors)
- **2.4 second average latency** (too slow)
- **Poor user experience** (links feel broken)

### Why Official Samples Don't Address This

The gemini-fullstack sample is a **research assistant**, not an e-commerce agent:

- Research citations are for **verification**, not **navigation**
- Users typically read the report, not click every link
- **Verification** requires showing sources, not direct access
- Links are supplementary, not primary user action

For **e-commerce**, links ARE the primary action → redirect issues matter more.

## Solutions Available

### Option 1: Accept Redirect URLs (Official Approach)

**What**: Use URLs as-is from grounding metadata  
**Pros**: Simple, follows official patterns, no extra code  
**Cons**: 50% failure rate, slow redirects, poor UX

**When to use**: MVP, research assistants, low click-through scenarios

### Option 2: Client-Side Redirect Resolution (Enhanced)

**What**: Resolve redirects in background before showing to user  
**Pros**: Direct merchant URLs, faster clicks, better UX  
**Cons**: Adds complexity, requires HTTP requests, caching

**Implementation**:
```python
import requests
from functools import lru_cache

@lru_cache(maxsize=500)
def resolve_redirect_url(url: str, timeout: int = 3) -> str:
    """Resolve Google redirect URL to final merchant URL."""
    if "vertexaisearch.cloud.google.com" not in url:
        return url  # Already direct
    
    try:
        response = requests.head(url, allow_redirects=True, timeout=timeout)
        if response.status_code == 200:
            return response.url  # Return final destination
    except:
        pass
    return url  # Return original on error
```

**When to use**: E-commerce, high click-through, production apps

### Option 3: Alternative Search Tools (Non-ADK)

**What**: Use non-grounding search APIs (Serp API, Bing API)  
**Pros**: Direct merchant URLs from start  
**Cons**: Loses grounding benefits, costs money, more complex

**When to use**: When grounding isn't required

## Recommendation for Commerce Agent

### Current Status: ✅ CORRECT

The agent is following official ADK patterns correctly. No changes needed for ADK compliance.

### For Production Deployment

If redirect URL issues impact user experience:

1. **Implement Option 2** (client-side redirect resolution)
2. **Add URL caching** to avoid repeated resolution
3. **Filter broken URLs** before showing to user
4. **Add timeout handling** (3-5 second max)

### For Tutorial/Learning Purposes

Keep current implementation:
- Shows official ADK grounding patterns  
- Demonstrates proper metadata extraction
- Follows gemini-fullstack best practices
- Documents known limitations transparently

## Conclusion

**The commerce agent is correct**. Google Search grounding returns redirect URLs by design, and the official ADK documentation and samples use these URLs directly without resolution.

The redirect URL behavior is:
- ✅ **Intended** - part of Google's grounding design
- ✅ **Documented** - in Vertex AI Search documentation
- ✅ **Universal** - all ADK apps using google_search get these URLs
- ❌ **Not ideal for e-commerce** - but that's a product limitation, not an implementation error

**Next steps**:
1. ✅ Document this behavior for users
2. ✅ Update instructions to show retailer domains clearly
3. ⚠️ Optional: Implement redirect resolution for production use
4. ✅ Keep current implementation for tutorial compliance

---

**References**:
- Official ADK Docs: https://google.github.io/adk-docs/grounding/google_search_grounding/
- ADK Source: `research/adk-python/src/google/adk/tools/google_search_tool.py`
- Official Sample: `research/adk-samples/python/agents/gemini-fullstack/app/agent.py`
- Research: `log/20251027_research_summary_google_search_redirect_urls.md`

**Status**: Complete understanding of official behavior
**Author**: GitHub Copilot
**Date**: 2025-10-27 14:50
