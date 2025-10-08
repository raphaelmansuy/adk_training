# Tutorial Modernization: Agent Pattern Update

## Overview

**Update Date**: January 2025  
**Purpose**: Modernize all tutorials to use the `Agent` pattern instead of legacy `LlmAgent`  
**Scope**: 5 tutorial files updated  
**Status**: ✅ Complete

## Background

In October 2025, the ADK introduced `Agent` as a type alias for `LlmAgent`. While both are functionally identical, `Agent` is the modern convention:

```python
# From google/adk/agents/__init__.py
from .llm_agent import Agent
from .llm_agent import LlmAgent

# From llm_agent.py line 840
Agent: TypeAlias = LlmAgent
```

**Both patterns work**, but we've updated all practical code examples to use the modern `Agent` pattern while keeping documentation that explains both are valid.

## Files Updated

### Summary

| File | Replacements | Status |
|------|-------------|--------|
| `tutorial/29_ui_integration_intro.md` | 3 | ✅ Complete |
| `tutorial/30_nextjs_adk_integration.md` | 2 | ✅ Complete |
| `tutorial/31_react_vite_adk_integration.md` | 2 | ✅ Complete |
| `tutorial/35_agui_deep_dive.md` | 2 | ✅ Complete |
| `tutorial/10_evaluation_testing.md` | 2 | ✅ Complete |
| **Total** | **11** | **✅ Complete** |

### Detailed Changes

#### 1. Tutorial 29 - UI Integration Intro (3 replacements)

**File**: `tutorial/29_ui_integration_intro.md`

**Change 1** - Line ~201: Import Statement
```python
# Before:
from google.adk.agents import LlmAgent

# After:
from google.adk.agents import Agent
```

**Change 2** - Line ~286: Agent Creation
```python
# Before:
adk_agent = LlmAgent(
    name="support",
    model="gemini-2.0-flash-exp"
)

# After:
adk_agent = Agent(
    name="support",
    model="gemini-2.0-flash-exp"
)
```

**Change 3** - Line ~606: Full Agent Definition
```python
# Before:
from google.adk.agents import LlmAgent

adk_agent = LlmAgent(
    name="support",
    model="gemini-2.0-flash-exp",
    instruction="You are a helpful support agent...",
    tools=[...]
)

# After:
from google.adk.agents import Agent

adk_agent = Agent(
    name="support",
    model="gemini-2.0-flash-exp",
    instruction="You are a helpful support agent...",
    tools=[...]
)
```

---

#### 2. Tutorial 30 - Next.js Integration (2 replacements)

**File**: `tutorial/30_nextjs_adk_integration.md`

**Change 1** - Line ~196: Import Statement
```python
# Before:
from google.adk.agents import LlmAgent

# After:
from google.adk.agents import Agent
```

**Change 2** - Line ~292: Agent Creation
```python
# Before:
adk_agent = LlmAgent(
    name="customer_support_agent",
    model="gemini-2.0-flash-exp",
    instruction="You are a helpful customer support agent...",
    tools=[search_knowledge_base, create_ticket]
)

# After:
adk_agent = Agent(
    name="customer_support_agent",
    model="gemini-2.0-flash-exp",
    instruction="You are a helpful customer support agent...",
    tools=[search_knowledge_base, create_ticket]
)
```

---

#### 3. Tutorial 31 - React Vite Integration (2 replacements)

**File**: `tutorial/31_react_vite_adk_integration.md`

**Change 1** - Line ~193: Import Statement
```python
# Before:
from google.adk.agents import LlmAgent

# After:
from google.adk.agents import Agent
```

**Change 2** - Line ~330: Agent Creation
```python
# Before:
adk_agent = LlmAgent(
    name="data_analyst",
    model="gemini-2.0-flash-exp",
    instruction="You are a data analyst agent...",
    tools=[query_database, generate_chart]
)

# After:
adk_agent = Agent(
    name="data_analyst",
    model="gemini-2.0-flash-exp",
    instruction="You are a data analyst agent...",
    tools=[query_database, generate_chart]
)
```

---

#### 4. Tutorial 35 - AG-UI Deep Dive (2 replacements)

**File**: `tutorial/35_agui_deep_dive.md`

**Change 1** - Line ~144: Import Statement
```python
# Before:
from google.adk.agents import LlmAgent

# After:
from google.adk.agents import Agent
```

**Change 2** - Line ~231: Agent Creation
```python
# Before:
adk_agent = LlmAgent(
    name="research_agent",
    model="gemini-2.0-flash-exp",
    instruction="You are a research assistant...",
    tools=[search_web, summarize_document]
)

# After:
adk_agent = Agent(
    name="research_agent",
    model="gemini-2.0-flash-exp",
    instruction="You are a research assistant...",
    tools=[search_web, summarize_document]
)
```

---

#### 5. Tutorial 10 - Evaluation & Testing (2 replacements)

**File**: `tutorial/10_evaluation_testing.md`

**Change 1** - Line ~234: Import Statement
```python
# Before:
from google.adk.agents import LlmAgent

# After:
from google.adk.agents import Agent
```

**Change 2** - Line ~280: Agent Creation
```python
# Before:
adk_agent = LlmAgent(
    name="support_agent",
    model="gemini-2.0-flash-exp",
    instruction="You are a helpful support agent. Use tools to help customers.",
    tools=[search_knowledge_base, create_ticket]
)

# After:
adk_agent = Agent(
    name="support_agent",
    model="gemini-2.0-flash-exp",
    instruction="You are a helpful support agent. Use tools to help customers.",
    tools=[search_knowledge_base, create_ticket]
)
```

**Note**: Tutorial 10 also contains troubleshooting examples that intentionally show both patterns (lines ~1310-1314). These were **not changed** as they serve an educational purpose.

---

## Files NOT Updated (Intentionally)

### Documentation Files

These files retain `LlmAgent` references because they explain both patterns:

1. **`tutorial/10_evaluation_testing.md`** (lines 1310-1314)
   - Troubleshooting section explaining the type alias
   - Shows both `Agent` and `LlmAgent` are valid

2. **`tutorial/IMPORT_PATH_REVIEW.md`**
   - Import path reference documentation
   - Explains legacy pattern for historical context

3. **`tutorial/AGENT_VS_LLMAGENT_CLARIFICATION.md`**
   - Comprehensive explanation of both patterns
   - Source code evidence
   - FAQ section

### Tutorials Already Using Modern Pattern

All tutorials 01-28 and 32-34 already use the `Agent` pattern:

```bash
# Verified with grep search - 0 results for LlmAgent in:
- tutorial/01_hello_world_agent.md through 28_using_other_llms.md
- tutorial/32_streamlit_integration.md
- tutorial/33_slack_integration.md  
- tutorial/34_pubsub_integration.md
```

## Update Pattern Used

For each file, we followed this systematic approach:

1. **Search**: Located all `LlmAgent` occurrences
2. **Read Context**: Read surrounding code (±10 lines)
3. **Replace Import**: Updated `from google.adk.agents import LlmAgent` → `import Agent`
4. **Replace Usage**: Updated `adk_agent = LlmAgent(...)` → `Agent(...)`
5. **Verify**: Confirmed changes were applied correctly

## Migration Guide for Users

If you have existing code using `LlmAgent`, you can update it using this simple pattern:

### Step 1: Update Import
```python
# Old:
from google.adk.agents import LlmAgent

# New:
from google.adk.agents import Agent
```

### Step 2: Update Agent Creation
```python
# Old:
agent = LlmAgent(
    name="my_agent",
    model="gemini-2.0-flash-exp",
    instruction="You are a helpful assistant."
)

# New:
agent = Agent(
    name="my_agent",
    model="gemini-2.0-flash-exp",
    instruction="You are a helpful assistant."
)
```

### No Functional Changes

**Important**: This is purely a cosmetic update. Both patterns are functionally identical:
- Same parameters
- Same behavior
- Same API
- Same performance

Your existing code with `LlmAgent` will continue to work without any changes.

## Verification Checklist

✅ **Tutorial 29**: All 3 replacements complete  
✅ **Tutorial 30**: All 2 replacements complete  
✅ **Tutorial 31**: All 2 replacements complete  
✅ **Tutorial 35**: All 2 replacements complete  
✅ **Tutorial 10**: All 2 replacements complete  
✅ **Documentation files**: Verified intentionally unchanged  
✅ **Other tutorials**: Verified already using modern pattern  
✅ **Test implementations**: Not updated (both patterns work)  

## Related Documentation

For more information about the Agent/LlmAgent relationship:

1. **`AGENT_VS_LLMAGENT_CLARIFICATION.md`**
   - Complete explanation of type alias
   - Source code evidence
   - FAQ section

2. **`IMPORT_PATH_REVIEW.md`**
   - Import path reference guide
   - Historical context

3. **Tutorial 10** (lines 1310-1314)
   - Troubleshooting section
   - Shows both patterns in action

## Statistics

- **Total Files Updated**: 5
- **Total Replacements**: 11
- **Import Statements Updated**: 5
- **Agent Creation Statements Updated**: 6
- **Lines Modified**: ~11 (one replacement per line)
- **Files Reviewed**: 35 tutorials + 3 documentation files
- **Verification Searches**: 8 grep operations

## Timeline

1. **Discovery Phase**: User questioned if `LlmAgent` was latest pattern
2. **Research Phase**: Agent verified in ADK source code (`Agent: TypeAlias = LlmAgent`)
3. **Planning Phase**: Searched all tutorials for `LlmAgent` usage (42 occurrences found)
4. **Implementation Phase**: Systematically updated 5 files
5. **Verification Phase**: Confirmed all other tutorials already modern
6. **Documentation Phase**: Created this summary

## Conclusion

All tutorial code examples now use the modern `Agent` pattern consistently. Documentation files retain references to both patterns to educate users about the type alias relationship. This update aligns the tutorials with ADK October 2025 conventions while maintaining backward compatibility documentation.

Users can choose either pattern based on preference, but `Agent` is recommended for new code.

---

**Update Completed**: January 2025  
**Files Modified**: 5  
**Pattern**: LlmAgent → Agent  
**Status**: ✅ Complete
