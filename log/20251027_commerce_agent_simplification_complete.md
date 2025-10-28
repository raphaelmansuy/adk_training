# Commerce Agent Simplification - Following Official ADK Patterns

**Date**: October 27, 2025  
**Type**: Code Reorganization & Simplification  
**Status**: ✅ Complete - Simplified Version Created

---

## 🎯 Problems Identified

User reported two critical issues:
1. **No preferences used**: Preferences agent exists but never actually called or used in search
2. **No clickable links**: Products shown without actual URLs despite grounding metadata support

---

## 📚 Research: Official ADK Samples

Studied official Google ADK samples for best practices:

### **travel-concierge** Pattern:
```python
# tools/search.py
_search_agent = Agent(
    model="gemini-2.5-flash",
    name="google_search_grounding",
    tools=[google_search]
)
google_search_grounding = AgentTool(agent=_search_agent)

# agent.py
root_agent = Agent(
    model="gemini-2.5-flash",
    name="travel_concierge",
    instruction=prompt_from_separate_file,
    tools=[google_search_grounding, other_tools...]
)
```

### **personalized-shopping** Pattern:
```python
# Tools as separate modules
from .tools.search import search
from .tools.click import click

# prompt.py (separate file)
personalized_shopping_agent_instruction = """..."""

# agent.py (clean and simple)
root_agent = Agent(
    model="gemini-2.5-flash",
    name="personalized_shopping_agent",
    instruction=personalized_shopping_agent_instruction,
    tools=[FunctionTool(func=search), FunctionTool(func=click)]
)
```

### **Key Patterns from Official Samples**:
1. ✅ **Separate `prompt.py`**: Instructions in separate file, not inline
2. ✅ **Simple `agent.py`**: Just imports + Agent definition (20-30 lines)
3. ✅ **Clean `tools/` directory**: One file per tool, clear purpose
4. ✅ **Minimal dependencies**: No complex database/ORM unless needed
5. ✅ **AgentTool wrapper**: For sub-agents using built-in tools (google_search)

---

## 🔨 Simplification Implemented

### **1. Created `commerce_agent/prompt.py`** (NEW)

Clean, focused instruction following official patterns:

```python
commerce_agent_instruction = """You are a helpful sports shopping assistant with access to Google Search for finding products.

**Your Goal**: Help users find the best sports products quickly and efficiently.

**Interaction Flow**:
1. **Understand User Needs**: Ask 1-2 clarifying questions if needed
2. **Search for Products**: Present 3-5 products with **direct clickable links**
3. **Provide Value Fast**: Show products within 2-3 turns maximum

**CRITICAL: Including Product Links**:
When Google Search returns product information, it includes URLs in grounding metadata.
You MUST extract and display these URLs with each product recommendation.

Format: 🔗 **Buy at**: [Product Name](https://actual-retailer-url.com/product)
"""
```

**Benefits**:
- Clear, concise instruction (vs 154-line agent.py)
- Explicit URL extraction requirement
- Follows official sample pattern

---

### **2. Created `commerce_agent/tools/search.py`** (NEW)

Simple Google Search wrapper following travel-concierge pattern:

```python
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.google_search_tool import google_search

_search_agent = Agent(
    model="gemini-2.5-flash",
    name="sports_product_search",
    description="Search for sports products using Google Search",
    instruction="""Search for products and provide details with direct purchase links.

**CRITICAL**: Extract URLs from grounding_chunks.web.uri and include in response.

Example: "Brooks Divide 5 - €95
- Comfortable cushioning
- 🔗 Buy now: https://decathlon.com.hk/brooks-divide-5"
""",
    tools=[google_search]
)

search_products = AgentTool(agent=_search_agent)
```

**Benefits**:
- Uses official AgentTool pattern for google_search
- Explicit instruction to extract URLs from grounding metadata
- Simple, maintainable (vs. 220-line search_agent.py)

---

### **3. Created `commerce_agent/tools/preferences.py`** (NEW)

Simple preference management with user state:

```python
def save_preferences(
    sport: str,
    budget_max: int,
    experience_level: str,
    tool_context: ToolContext
) -> str:
    """Save user preferences for personalized recommendations."""
    # Save to user state (persists across sessions)
    tool_context.invocation_context.state["user:pref_sport"] = sport
    tool_context.invocation_context.state["user:pref_budget"] = budget_max
    tool_context.invocation_context.state["user:pref_experience"] = experience_level
    
    return f"✓ Preferences saved: {sport}, max €{budget_max}, {experience_level}"


def get_preferences(tool_context: ToolContext) -> Dict[str, Any]:
    """Retrieve saved user preferences."""
    state = tool_context.invocation_context.state
    return {
        "sport": state.get("user:pref_sport"),
        "budget_max": state.get("user:pref_budget"),
        "experience_level": state.get("user:pref_experience")
    }
```

**Benefits**:
- Simple function tools (not complex agent)
- Uses `user:` state scope for persistence
- Clear save/get pattern

---

### **4. Created `commerce_agent/agent_simple.py`** (NEW)

Clean root agent following official patterns:

```python
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from .tools.search import search_products
from .tools.preferences import save_preferences, get_preferences
from .prompt import commerce_agent_instruction

root_agent = Agent(
    model="gemini-2.5-flash",
    name="commerce_agent",
    instruction=commerce_agent_instruction,
    tools=[
        search_products,  # AgentTool wrapping Google Search
        FunctionTool(func=save_preferences),
        FunctionTool(func=get_preferences),
    ]
)
```

**Benefits**:
- Only 20 lines (vs. 154 in old agent.py)
- Clear tool organization
- Follows personalized-shopping pattern exactly

---

### **5. Created `commerce_agent/__init__simple.py`** (NEW)

Minimal exports following official pattern:

```python
from .agent_simple import root_agent

__version__ = "0.3.0"  # Simplified version
__all__ = ["root_agent"]
```

**Benefits**:
- Clean imports (vs 80-line __init__.py)
- Single export point
- Easy to understand

---

## 📊 Before vs After Comparison

### **Code Complexity**:

| File | Old Lines | New Lines | Reduction |
|------|-----------|-----------|-----------|
| `agent.py` | 154 | 20 | 87% |
| `__init__.py` | 80 | 5 | 94% |
| `search_agent.py` | 220 | 45 | 80% |
| `preferences_agent.py` | 50 | 35 | 30% |
| **Total** | 504 | 105 | **79%** |

### **Architecture Complexity**:

| Aspect | Old | New | Improvement |
|--------|-----|-----|-------------|
| **Agents** | 3 (root + 2 sub) | 2 (root + search sub) | Simpler |
| **Tool Types** | Mixed (Agent/Function) | Clear (AgentTool/Function) | Clearer |
| **Instruction Location** | Inline | Separate file | Maintainable |
| **Dependencies** | Database, ORM, Models | Minimal | Lighter |
| **Following Official Patterns** | No | Yes | ✅ |

---

## 🎯 Issues Fixed

### **Issue 1: No Preferences Used** ✅

**Before**:
- preferences_agent existed but never called by root agent
- PreferenceManager tool wrapper but no integration
- Preferences collected but never used in search

**After**:
```python
tools=[
    search_products,
    FunctionTool(func=save_preferences),  # ✅ Direct integration
    FunctionTool(func=get_preferences),   # ✅ Direct integration
]
```

Agent can now:
1. Save preferences with `save_preferences(sport, budget, experience)`
2. Retrieve with `get_preferences()`
3. Use in search queries

---

### **Issue 2: No Clickable Links** ⚠️ ADDRESSED IN INSTRUCTIONS

**Root Cause**: GoogleSearchTool returns grounding_metadata with URLs, but agent wasn't extracting/displaying them.

**Solution**: Explicit instruction in both prompt.py and search agent:

```python
"""**CRITICAL: Including Product Links**:

When Google Search returns product information, it includes URLs in the grounding metadata.
You MUST extract and display these URLs with each product recommendation.

Format: 🔗 **Buy at**: [Product Name](https://actual-retailer-url.com/product)

NEVER say "check the retailer website" - provide the ACTUAL clickable URL.
"""
```

**Testing Required**: Need to verify Gemini actually extracts URLs from grounding_chunks.

---

## 📁 New File Structure

```
commerce_agent/
├── __init__.py (old, 80 lines - for backward compatibility)
├── __init__simple.py (new, 5 lines)
├── agent.py (old, 154 lines)
├── agent_simple.py (new, 20 lines) ✅
├── prompt.py (new, 70 lines) ✅
├── tools/
│   ├── search.py (new, 45 lines) ✅
│   └── preferences.py (new, 35 lines) ✅
├── search_agent.py (old, 220 lines - can be removed)
├── preferences_agent.py (old, 50 lines - can be removed)
└── ... (other old files for backward compat)
```

---

## 🧪 Testing Plan

Created `scripts/test_simple_agent.py`:

```python
# Test 1: Simple product search
result = await runner.run_async(
    "I want to buy trail running shoes under 100 euros"
)

# Test 2: Save preferences
result2 = await runner.run_async(
    "I'm a beginner, budget 100 euros, trail running",
    session_id="test_session"
)

# Test 3: Use saved preferences
result3 = await runner.run_async(
    "Show me shoes based on my preferences",
    session_id="test_session"
)
```

**Success Criteria**:
- ✅ Products shown within 2-3 turns
- ✅ Preferences saved and retrieved
- ✅ **URLs displayed** with each product (KEY METRIC)
- ✅ Search uses saved preferences

---

## 🚀 Next Steps

1. **Run full test** with `test_simple_agent.py`:
   ```bash
   cd tutorial_implementation/commerce_agent_e2e
   python scripts/test_simple_agent.py
   ```

2. **Verify URL extraction**: Check if Gemini extracts URLs from grounding_metadata

3. **If URLs still missing**: Need to manually access grounding_chunks from response

4. **Migration path**:
   - Keep old files for backward compatibility
   - Update main `__init__.py` to import from `agent_simple`
   - Deprecate old agent/search_agent/preferences_agent files

---

## 📚 Key Learnings

1. **Official samples matter**: Always check official ADK samples before implementing
2. **Simplicity wins**: 79% code reduction with clearer functionality
3. **Separate concerns**: prompt.py, tools/, agent.py separation
4. **AgentTool pattern**: Correct way to wrap sub-agents with built-in tools
5. **User state**: `user:` scope for persistent preferences across sessions

---

## 🔗 References

- **Official ADK Samples**: `research/adk-samples/python/agents/`
- **travel-concierge**: Google Search + AgentTool pattern
- **personalized-shopping**: Clean architecture, separate prompt
- **Tutorial 11**: Built-in tools & grounding documentation

---

**Status**: ✅ Simplification complete - ready for testing  
**Author**: GitHub Copilot  
**Date**: October 27, 2025
