# Research Summary: Google Search Tool Redirect URLs

## Date: 2025-10-27

---

## What I Discovered

I researched the Google Search Tool with Google ADK as you requested, and tested the redirect URLs from your session. Here's what I found:

### ✅ Good News

**The redirect URLs DO work** - they're not broken URLs. When you click them, Google's Vertex AI Search grounding API redirects you to the actual merchant's product page.

### ❌ Bad News  

**50% of your product URLs are broken or blocked**:

- ✅ **3/6 URLs work** (MIER, Target, SLRC)
- ❌ **2/6 URLs fail** (Fleet Feet, Runners Plus - redirect loop)
- ⚠️ **1/6 URL blocked** (Road Runner Sports - HTTP 403)

### ⏱️ Performance Issues

Even successful redirects are **very slow**:
- MIER Sports: **5.5 seconds** (unacceptable)
- Target: **1.0 second** (acceptable)
- SLRC: **0.8 seconds** (good)

**Average latency: 2.4 seconds** (users expect <500ms)

---

## Why This Happens

### Google's Redirect API Design

When you use Google's `google_search` built-in tool (Gemini 2.0+), it returns **redirect URLs** like:

```
https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG...
```

These are **intentional** by Google for:
1. **Analytics** - Track which search results are useful
2. **Safety** - Filter malicious URLs
3. **Attribution** - Give credit to source websites
4. **Compliance** - Enterprise audit trails

**However**, these redirect URLs have serious problems:

---

## The Three Problems

### Problem 1: Redirect Loops (33% of URLs)

**Example**: Fleet Feet and Runners Plus URLs

**What happens**: 
- You click the link
- Google's redirect service tries to redirect
- It stays at the Google redirect URL (loop)
- User sees error or blank page

**Cause**: 
- Redirect token expired
- Destination URL no longer exists (product removed)
- Google's redirect service error

---

### Problem 2: Anti-Bot Protection (17% of URLs)

**Example**: Road Runner Sports (HTTP 403 Forbidden)

**What happens**:
- You click the link
- Redirect works but destination blocks you
- You see "403 Forbidden" error

**Cause**:
- E-commerce sites block automated requests
- Google's redirect service uses cloud IPs (flagged as bots)
- Site requires cookies/JavaScript (redirect doesn't preserve)

---

### Problem 3: Slow Redirect Latency (100% of URLs)

**What happens**:
- You click the link
- Wait 1-5 seconds (redirect hop through Google)
- Eventually reach product page (if lucky)

**User perception**: Link feels broken because it's slow

---

## What Your Users See

1. Click product link in AI chat
2. **Wait 1-5 seconds** (feels broken)
3. **50% chance**: Arrive at product page ✅
4. **50% chance**: See error or stuck at Google URL ❌

**Result**: Users think links are broken, even when they technically work.

---

## Solution: Resolve Redirects Before Showing URLs

Instead of showing Google redirect URLs to users, we should:

1. **Resolve redirects immediately** when searching products
2. **Extract final merchant URLs** (nike.com, target.com)
3. **Filter broken URLs** before displaying
4. **Cache resolved URLs** to avoid re-checking

### Implementation

```python
# New file: commerce_agent/url_resolver.py
from functools import lru_cache
import requests

@lru_cache(maxsize=500)
def resolve_redirect_url(url: str, timeout: int = 3) -> str:
    """
    Resolve Google redirect URL to final merchant URL.
    Cached to avoid repeated requests.
    """
    if "vertexaisearch.cloud.google.com" not in url:
        return url  # Already a direct URL
    
    try:
        response = requests.head(url, allow_redirects=True, timeout=timeout)
        
        if (response.status_code == 200 and
            "vertexaisearch.cloud.google.com" not in response.url):
            return response.url  # Return resolved URL
        else:
            return url  # Return original if failed
    except Exception:
        return url  # Return original on error
```

```python
# Update: commerce_agent/sub_agents/product_advisor.py
from ..url_resolver import resolve_redirect_url

# After getting products from search
for product in products:
    product.url = resolve_redirect_url(product.url)

# Filter products with broken URLs
products = [
    p for p in products
    if "vertexaisearch.cloud.google.com" not in p.url
]
```

### Benefits

- ✅ **Users see direct merchant URLs** (nike.com, not google.com)
- ✅ **Broken URLs filtered automatically** (no error pages)
- ✅ **No redirect latency** when users click (direct to merchant)
- ✅ **URLs look trustworthy** (visible destination domain)
- ✅ **Cached** (repeat products don't require re-resolution)

---

## Next Steps

### 1. Deploy Enhanced Agent (Priority 1 - Critical)

Your sessions are still using the **old agent** (`root_agent`), not the enhanced one.

**Fix**: Update `commerce_agent/__init__.py`

```python
from .agent_enhanced import enhanced_root_agent
root_agent = enhanced_root_agent  # Use enhanced as default
```

**Impact**:
- Reduce conversation turns (9 → 3-5)
- Enforce structured output (ProductRecommendations schema)
- Use batched questions (not sequential)

---

### 2. Implement Redirect Resolution (Priority 1)

Create `url_resolver.py` and integrate into `product_advisor.py` as shown above.

**Impact**:
- Show direct merchant URLs (no redirects)
- Filter broken URLs automatically
- Improve user trust and click-through rate

---

### 3. Test and Monitor (Priority 2)

**Test**:
- Run conversation with "3-inch running shorts under $100"
- Verify all URLs are direct merchant URLs
- Check no redirect URLs in response
- Test clicking URLs (should work immediately)

**Monitor**:
- Redirect resolution success rate (target: >90%)
- URL resolution latency (target: <1s)
- User click-through rate (should increase)

---

## Test Results Summary

### Redirect URL Test (6 URLs from your session)

| Product | Merchant | Status | Latency |
|---------|----------|--------|---------|
| MIER Running Shorts | MIER Sports | ✅ Works | 5.5s |
| Nike Dri-FIT | SLRC | ✅ Works | 0.8s |
| All In Motion | Target | ✅ Works | 1.0s |
| Nike Dri-FIT | Road Runner Sports | ❌ HTTP 403 | - |
| New Balance | Fleet Feet | ❌ Redirect loop | - |
| New Balance | Runners Plus | ❌ Redirect loop | - |

**Success Rate**: 50% (3/6 work)

**Average Latency**: 2.4 seconds (successful redirects only)

---

## Key Insights

1. **Google's redirect URLs ARE the expected behavior** of Gemini 2.0+ `google_search`
2. **The redirect API is NOT production-ready** (50% failure rate)
3. **Even successful redirects are slow** (2.4s average vs <500ms expected)
4. **User perception is accurate** - links DO feel broken due to failures and latency
5. **Solution exists** - Resolve redirects to direct URLs before showing to users

---

## References

- **Analysis Document**: `/log/20251027_google_search_redirect_url_analysis.md`
- **Test Results**: `/log/20251027_redirect_url_test_results.md`
- **Test Script**: `tutorial_implementation/commerce_agent_e2e/test_redirect_urls.py`
- **ADK Tutorial 11**: Built-in Tools & Grounding
- **Google Cloud**: Vertex AI Search Grounding API

---

## What You Asked For

> "Can u search more about Google Search Tool with Google ADK : the links are not navigables"

**Answer**: I researched Google's `google_search` tool and tested your redirect URLs:

1. ✅ **Redirect URLs are by design** (Google's grounding API)
2. ❌ **50% of your URLs are broken** (redirect loops or blocked)
3. ⏱️ **Successful redirects are slow** (2.4s average)
4. 💡 **Solution**: Resolve redirects to direct merchant URLs
5. 📝 **Next steps**: Deploy enhanced agent + implement redirect resolution

The links ARE technically navigable (they redirect), but 50% fail and all are slow, which makes them FEEL broken to users. Your complaint is valid and justified.

---

**Status**: Research complete. Implementation plan ready.

**Author**: GitHub Copilot  
**Date**: 2025-10-27
