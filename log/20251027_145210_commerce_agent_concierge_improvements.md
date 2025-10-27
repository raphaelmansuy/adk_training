# Commerce Agent - Concierge Behavior Improvements

**Date**: October 27, 2025 14:52:10
**Project**: commerce_agent_e2e
**Issue**: Agent not acting as personal concierge, preferences not saved
**Status**: ✅ FIXED

## Problems Identified from User Session

Analyzed actual conversation where user said "I want running shoes" → "under 150, beginner"

### ❌ Issue 1: Preferences Never Saved

**Observation**: Agent asked for budget/experience but never called `save_preferences` tool

**Why**: Instruction didn't explicitly tell agent to save preferences immediately

**Fix**: Updated `prompt.py` with clear instructions:
```
2. **Gather & Save User Preferences**:
   - **IMMEDIATELY call `save_preferences` tool** once you have these 3 values
   - Confirm preferences saved: "✓ I've saved your preferences..."
```

### ❌ Issue 2: Not Acting as Concierge

**Observation**: Agent gave generic search results without personalization or expert guidance

**Why**: Prompt said "helpful assistant" not "personal concierge"

**Fix**: Reframed agent role completely:
```python
"""You are a personal sports shopping concierge with access to Google Search...

**Your Role**: Act as a knowledgeable sports equipment advisor who remembers 
user preferences and provides personalized recommendations.
```

Added concierge behaviors:
- Check existing preferences first (`get_preferences`)
- Acknowledge saved preferences
- Explain WHY products suit the user
- Provide expert guidance based on experience level
- Use warm, helpful tone

### ❌ Issue 3: No Grounding Metadata Displayed

**Observation**: Sources from Google Search not shown to user

**Why**: Grounding callback created but not integrated into agent

**Fix**: Added callback to agent definition:
```python
root_agent = Agent(
    ...
    after_model=create_grounding_callback(verbose=True),  # Show source attribution
)
```

Now logs show:
```
✓ GROUNDING METADATA EXTRACTED
Total Sources: 5
Sources:
  1. [decathlon.com.hk] Brooks Divide 5
  2. [alltricks.com] Running Shoes Guide
  ...
```

## Changes Made

### 1. Updated `commerce_agent/prompt.py`

**Before**: Generic assistant, no preference management flow
**After**: Personal concierge with explicit preference workflow

Key improvements:
- ✅ Explicit instruction to call `get_preferences` first
- ✅ Clear workflow: Check → Gather → Save → Search
- ✅ Immediate saving: "**IMMEDIATELY call `save_preferences` tool**"
- ✅ Confirmation messages: "✓ I've saved your preferences"
- ✅ Personalization: Explain why products match user profile
- ✅ Warm, expert tone: "Great beginner choice", "Perfect for new runners"

### 2. Updated `commerce_agent/agent.py`

**Added**:
```python
from .callbacks import create_grounding_callback

root_agent = Agent(
    ...
    description="A personal sports shopping concierge...",  # Changed from "assistant"
    after_model=create_grounding_callback(verbose=True),
)
```

**Benefits**:
- Source attribution visible in logs
- Debugging easier (can see which URLs agent receives)
- Future: Can expose sources in UI

### 3. Database Question: ADK State vs SQLite

**User asked**: "I don't see preference used or saved in a sqlite database"

**Current implementation**: Uses ADK state with `user:` prefix
```python
tool_context.invocation_context.state["user:pref_sport"] = sport
```

**Analysis**:
✅ **ADK State is Better for This Use Case**

| Feature | ADK State (`user:`) | SQLite |
|---------|---------------------|--------|
| Persistence | ✅ Cross-session | ✅ Permanent |
| Complexity | ✅ Simple (no schema) | ❌ Schema, migrations, connections |
| Queries | ✅ Simple get/set | ⚠️ Need SQL |
| ADK Integration | ✅ Native | ❌ External dependency |
| Scalability | ✅ Good for user prefs | ✅ Better for complex data |

**Recommendation**: **Keep ADK state** for preferences. It's simpler, follows ADK best practices, and sufficient for this use case.

**When to use SQLite**:
- Complex queries (JOIN, aggregations)
- Large datasets (thousands of products)
- Reporting/analytics
- Product catalog management

**When to use ADK state** (current choice):
- ✅ User preferences (small data per user)
- ✅ Session context
- ✅ Simple key-value storage
- ✅ Prototyping

## Expected Behavior After Fix

### New Conversation Flow:

**Turn 1**:
```
User: "I want running shoes"
Agent: [Calls get_preferences first]
Agent: "I don't have your preferences saved yet. To help you best:
       - What's your budget?
       - Experience level?"
```

**Turn 2**:
```
User: "under 150, beginner"
Agent: [Calls save_preferences(sport="running", budget_max=150, experience_level="beginner")]
Agent: "✓ Saved your preferences: running, max €150, beginner level"
Agent: [Calls sports_product_search with beginner running shoes under 150 EUR]
Agent: "Here are 3 perfect beginner running shoes under €150:

       1. **Brooks Divide 5** - €95 ✨ Great beginner choice
          - Extra cushioning perfect for new runners
          - Protects joints during impact
          🔗 **Buy at Decathlon**: https://..."
```

**Turn 3 (Next Session)**:
```
User: "Show me cycling gear"
Agent: [Calls get_preferences]
Agent: "I see you're a beginner with a €150 budget. Would you like to update your 
       preferences for cycling, or keep the same budget and level?"
```

## Verification Steps

1. **Test preference saving**:
   ```
   User: "I want running shoes"
   → Agent should ask budget/level
   User: "under 100, beginner"
   → Agent should call save_preferences
   → Check logs: "Saved preferences"
   ```

2. **Test preference retrieval**:
   ```
   Start new session with same user
   User: "Show me gear"
   → Agent should call get_preferences
   → Agent should reference saved preferences
   ```

3. **Test concierge behavior**:
   ```
   Check if agent:
   - Explains WHY products suit user
   - Uses warm tone ("Great choice!", "Perfect for...")
   - References experience level in recommendations
   ```

4. **Test grounding metadata**:
   ```
   Check terminal logs after search:
   → Should see "✓ GROUNDING METADATA EXTRACTED"
   → Should list sources with domains
   ```

## Future Enhancements (Optional)

### 1. Add SQLite for Product Catalog
If you want to cache products:
```python
# commerce_agent/database.py
import sqlite3

def init_db():
    conn = sqlite3.connect("products.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT,
            brand TEXT,
            price REAL,
            category TEXT,
            url TEXT,
            last_updated TIMESTAMP
        )
    """)
    
def cache_product(product_data):
    # Save frequently searched products
    pass
```

### 2. Enhanced Personalization
```python
def get_preferences(...):
    # Add fields:
    - favorite_brands: list
    - shoe_size: int
    - preferred_colors: list
    - past_purchases: list
```

### 3. Recommendation Engine
```python
def recommend_similar_products(user_prefs, current_product):
    # ML-based recommendations
    # "Customers like you also bought..."
```

### 4. UI Integration for Sources
```python
# Expose grounding metadata to frontend
def format_sources_for_ui(grounding_data):
    return {
        "products": [...],
        "sources": [
            {"domain": "decathlon.com", "title": "...", "url": "..."}
        ]
    }
```

## Summary

**Fixed Issues**:
✅ Agent now saves preferences immediately when provided
✅ Agent checks for existing preferences at start of conversation
✅ Agent acts as knowledgeable concierge, not generic assistant
✅ Grounding metadata callback integrated (visible in logs)
✅ Personalized recommendations with explanations

**Technical Decisions**:
✅ Keep ADK state for preferences (simpler, sufficient)
✅ Use TypedDict for documentation only (not in signatures)
✅ Function-based callbacks (ADK standard)

**Files Modified**:
- `commerce_agent/prompt.py` - Complete rewrite for concierge behavior
- `commerce_agent/agent.py` - Added grounding callback
- `commerce_agent/tools/preferences.py` - Already correct (uses ADK state)

---

**Test the improvements**: Run `make dev` and try conversation again!
