# Tutorial 27 - Critical API Errors Found

**Date**: 2025-01-13 23:00:00  
**Tutorial**: 27_third_party_tools.md  
**Status**: CRITICAL - Multiple API usage errors  
**Impact**: HIGH - All examples would fail with import and API errors

## Issues Summary

Found **3 CRITICAL categories** of errors:

1. ❌ **Wrong import paths** - `from google.adk.tools.third_party import ...` (doesn't exist)
2. ❌ **Old Runner API** - `Runner()` instead of `InMemoryRunner()`  
3. ❌ **Old run_async() signature** - 8 occurrences using old API

---

## Issue 1: Incorrect Import Paths

### Location
**Throughout tutorial** - Lines 107, 119, 296, 300, 348, etc.

### Current Code (WRONG)
```python
from google.adk.tools.third_party import LangchainTool
from google.adk.tools.third_party import CrewaiTool
```

### Problem
**The `third_party` submodule DOES NOT EXIST** in `google.adk.tools`

**Source Verification**:
```bash
$ ls /research/adk-python/src/google/adk/tools/
# Output shows:
langchain_tool.py  # ✅ EXISTS
crewai_tool.py     # ✅ EXISTS
# NO third_party/ directory
```

**Test**:
```bash
$ python -c "from google.adk.tools.third_party import LangchainTool"
# ModuleNotFoundError: No module named 'google.adk.tools.third_party'
```

### Correct Import Paths

```python
# ✅ CORRECT
from google.adk.tools.langchain_tool import LangchainTool
from google.adk.tools.crewai_tool import CrewaiTool
```

### Impact
- ❌ **Every example fails immediately** with `ModuleNotFoundError`
- ❌ Users cannot import tools at all
- ❌ Tutorial completely unusable from line 1

### Affected Lines
All import statements:
- Line 107: `from google.adk.tools.third_party import LangchainTool`
- Line 119: `from google.adk.tools.third_party import LangchainTool`
- Line 211: `from google.adk.tools.third_party import LangchainTool`
- Line 230: `from google.adk.tools.third_party import LangchainTool`
- Line 296: `from google.adk.tools.third_party import CrewaiTool`
- Line 300: `from google.adk.tools.third_party import CrewaiTool`
- Line 348: `from google.adk.tools.third_party import CrewaiTool`
- Line 398: `from google.adk.tools.third_party import CrewaiTool`
- And more...

---

## Issue 2: Old Runner API

### Location
**8 occurrences** at lines: 129, 168, 342, 380, 580, 615, 703, 810

### Current Pattern (WRONG)
```python
from google.adk.agents import Agent, Runner  # ❌ WRONG MODULE

async def main():
    agent = Agent(...)
    runner = Runner()  # ❌ OLD API
    result = await runner.run_async(query, agent=agent)  # ❌ OLD SIGNATURE
```

### Problem
1. **`Runner` should be `InMemoryRunner`** and imported from `google.adk.runners`
2. **`Runner()` constructor different** from `InMemoryRunner(agent, app_name)`
3. **`run_async()` signature changed** - requires `user_id`, `session_id`, returns `AsyncGenerator[Event]`

### Correct Pattern

```python
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types

async def main():
    agent = Agent(...)
    
    # ✅ CORRECT: InMemoryRunner with agent
    runner = InMemoryRunner(agent=agent, app_name='third_party_demo')
    
    # ✅ CORRECT: Create session
    session = await runner.session_service.create_session(
        app_name='third_party_demo',
        user_id='demo_user'
    )
    
    # ✅ CORRECT: Content object and event iteration
    new_message = types.Content(
        role='user',
        parts=[types.Part(text=query)]
    )
    
    async for event in runner.run_async(
        user_id='demo_user',
        session_id=session.id,
        new_message=new_message
    ):
        if event.content and event.content.parts:
            print(event.content.parts[0].text)
```

### Source Verification

**File**: `/research/adk-python/src/google/adk/runners.py`

```python
# Line 1135: InMemoryRunner constructor
def __init__(
    self,
    agent: Optional[BaseAgent] = None,
    *,
    app_name: Optional[str] = 'InMemoryRunner',
    plugins: Optional[list[BasePlugin]] = None,
    app: Optional[App] = None,
):
```

```python
# Line 336: run_async signature
async def run_async(
    self,
    *,
    user_id: str,  # ❌ REQUIRED
    session_id: str,  # ❌ REQUIRED
    invocation_id: Optional[str] = None,
    new_message: Optional[types.Content] = None,
    state_delta: Optional[dict[str, Any]] = None,
    run_config: Optional[RunConfig] = None,
) -> AsyncGenerator[Event, None]:  # ❌ Returns async generator
```

---

## Issue 3: Old run_async() Calls

### Location
**8 occurrences** throughout tutorial

### Examples

**Example 1: Tavily Search (Lines ~169-171)**
```python
# ❌ WRONG
runner = Runner()
result = await runner.run_async(
    "What are the latest developments in quantum computing? (2025)",
    agent=agent
)
print(result.content.parts[0].text)
```

**Example 2: Serper Search (Lines ~381-383)**
```python
# ❌ WRONG
runner = Runner()
result = await runner.run_async(
    "What is the current price of Bitcoin?",
    agent=agent
)
```

**Example 3: Multi-tool Agent (Lines ~616-617)**
```python
# ❌ WRONG
runner = Runner()
final_result = await runner.run_async(
    "Research quantum computing and write a summary",
    agent=coordinator
)
```

**Example 4: Integration Example (Line 829)**
```python
# ❌ WRONG
result = await runner.run_async(query, agent=research_agent)
```

### All Affected Lines
- Line 169-171: Tavily search example
- Line 381-383: Serper search example  
- Line 616-617: Multi-tool coordinator
- Line 829: Integration example
- Plus 4 more instances

---

## Tool Wrapper Verification

**GOOD NEWS**: The tool wrapper APIs shown in the tutorial are CORRECT!

### LangchainTool ✅

**Source**: `/research/adk-python/src/google/adk/tools/langchain_tool.py`

```python
class LangchainTool(FunctionTool):
    def __init__(
        self,
        tool: Union[LangchainBaseTool, object],
        name: Optional[str] = None,  # ✅ Optional
        description: Optional[str] = None,  # ✅ Optional
    ):
```

**Tutorial Usage** - CORRECT:
```python
tavily_tool = TavilySearchResults(...)
tavily_adk = LangchainTool(tool=tavily_tool)  # ✅ CORRECT
```

### CrewaiTool ✅

**Source**: `/research/adk-python/src/google/adk/tools/crewai_tool.py`

```python
class CrewaiTool(FunctionTool):
    def __init__(self, tool: CrewaiBaseTool, *, name: str, description: str):
        # name and description are REQUIRED
```

**Tutorial Usage** - CORRECT:
```python
serper_tool = SerperDevTool()
serper_adk = CrewaiTool(
    tool=serper_tool,
    name='serper_search',  # ✅ REQUIRED, correctly provided
    description='Search Google for current information'  # ✅ REQUIRED
)
```

**Tutorial even has correct warning**:
> ⚠️ CRITICAL: CrewAI tools **REQUIRE** `name` and `description` parameters!

---

## Fix Strategy

### Fix 1: Update All Import Statements

**Find and replace** throughout tutorial:

```python
# BEFORE
from google.adk.tools.third_party import LangchainTool
from google.adk.tools.third_party import CrewaiTool

# AFTER  
from google.adk.tools.langchain_tool import LangchainTool
from google.adk.tools.crewai_tool import CrewaiTool
```

**Count**: ~10+ import statements to fix

### Fix 2: Update All Runner Imports

```python
# BEFORE
from google.adk.agents import Agent, Runner

# AFTER
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types  # Add for Content objects
```

### Fix 3: Update All Runner Instantiation and Usage

**Template for each example:**

```python
# BEFORE (WRONG)
runner = Runner()
result = await runner.run_async(query, agent=agent)
print(result.content.parts[0].text)

# AFTER (CORRECT)
runner = InMemoryRunner(agent=agent, app_name='example_app')
session = await runner.session_service.create_session(
    app_name='example_app',
    user_id='user_123'
)

new_message = types.Content(
    role='user',
    parts=[types.Part(text=query)]
)

async for event in runner.run_async(
    user_id='user_123',
    session_id=session.id,
    new_message=new_message
):
    if event.content and event.content.parts:
        print(event.content.parts[0].text)
```

### Fix 4: Add Verification Info Box

Add at top of tutorial (after the danger box):

```markdown
:::info API Verification

This tutorial has been verified against **ADK Python SDK v1.16.0+**.

**Critical API Changes:**

- ✅ Import: `from google.adk.tools.langchain_tool import LangchainTool`
- ✅ Import: `from google.adk.tools.crewai_tool import CrewaiTool`
- ✅ Runner: Use `InMemoryRunner` from `google.adk.runners`
- ✅ run_async: Requires `user_id`, `session_id`, returns `AsyncGenerator[Event]`
- ❌ OLD: `from google.adk.tools.third_party` - module doesn't exist
- ❌ OLD: `Runner()` from `google.adk.agents` - use InMemoryRunner

Source verification: `research/adk-python/src/google/adk/tools/` (2025-01-13)

:::
```

---

## Impact Assessment

### Severity: CRITICAL

1. **Import Errors (Most Critical)**
   - **Every single example fails** with `ModuleNotFoundError`
   - Happens at import time, before any code runs
   - 100% tutorial failure rate

2. **Runner API Errors**
   - Even if imports were fixed, would still fail
   - `TypeError: missing required argument: 'user_id'`
   - 8 examples affected

3. **Educational Impact**
   - Tutorial teaches **completely wrong** import paths
   - Users learn APIs that don't exist
   - Frustration and confusion guaranteed

### User Impact

**Before Fix:**
```bash
$ python example.py
Traceback (most recent call last):
  File "example.py", line 3, in <module>
    from google.adk.tools.third_party import LangchainTool
ModuleNotFoundError: No module named 'google.adk.tools.third_party'
```

**After Fix:**
```bash
$ python example.py
Based on recent web search results:
**Latest Quantum Computing Developments (2025)**:
...
```

---

## Examples Requiring Fixes

### Example 1: Tavily Search (Lines ~125-175)
- ❌ Import path wrong
- ❌ Runner API wrong
- ✅ Tool wrapper correct

### Example 2: Wikipedia Tool (Lines ~206-224)
- ❌ Import path wrong  
- ✅ Tool wrapper correct

### Example 3: Python REPL (Lines ~226-243)
- ❌ Import path wrong
- ✅ Tool wrapper correct

### Example 4: Serper Search (Lines ~337-387)
- ❌ Import path wrong
- ❌ Runner API wrong
- ✅ Tool wrapper correct

### Example 5: Website Scraping (Lines ~393-410)
- ❌ Import path wrong
- ✅ Tool wrapper correct

### Example 6: Multi-Tool Coordinator (Lines ~575-620)
- ❌ Import path wrong
- ❌ Runner API wrong
- ✅ Tool wrappers correct

### Example 7: Production Integration (Lines ~700-835)
- ❌ Import path wrong
- ❌ Runner API wrong
- ✅ Tool patterns correct

---

## Testing After Fixes

### Test 1: Verify Imports
```bash
python -c "
from google.adk.tools.langchain_tool import LangchainTool
from google.adk.tools.crewai_tool import CrewaiTool
print('✅ Imports successful')
"
```

### Test 2: Verify Runner Pattern
```python
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types
import asyncio

async def test():
    agent = Agent(model='gemini-2.0-flash')
    runner = InMemoryRunner(agent=agent, app_name='test')
    session = await runner.session_service.create_session(
        app_name='test', user_id='test'
    )
    msg = types.Content(role='user', parts=[types.Part(text='Hello')])
    async for event in runner.run_async(
        user_id='test', session_id=session.id, new_message=msg
    ):
        if event.content:
            print('✅ Runner pattern works')
            break

asyncio.run(test())
```

### Test 3: Verify Tool Wrapper (if langchain installed)
```python
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
wiki_tool = LangchainTool(tool=wikipedia)
print(f'✅ Tool wrapper works: {wiki_tool.name}')
```

---

## Related Issues

- **Tutorial 25**: Same `Runner()` → `InMemoryRunner()` issue - FIXED
- **Tutorial 24**: Same `run_async()` signature issue - FIXED  
- **Tutorial 20**: Import path issue with different API - FIXED
- **Pattern**: All DRAFT tutorials not updated for ADK v1.16+ breaking changes

---

## Completion Checklist

- [ ] Fix all import statements (`third_party` → direct module imports)
- [ ] Update all `Runner` → `InMemoryRunner` with imports
- [ ] Fix all 8 `run_async()` call sites
- [ ] Add verification info box
- [ ] Test at least one example end-to-end
- [ ] Verify tool wrapper examples still correct
- [ ] Update any summary/key takeaways sections

---

## Source Code Evidence

### Import Paths
```bash
# Verified directory structure:
/research/adk-python/src/google/adk/tools/
├── langchain_tool.py  ✅
├── crewai_tool.py     ✅
└── (no third_party/)  ❌
```

### LangchainTool Class
```python
# From: langchain_tool.py, line 56
class LangchainTool(FunctionTool):
    def __init__(
        self,
        tool: Union[LangchainBaseTool, object],
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
```

### CrewaiTool Class
```python
# From: crewai_tool.py, line 47
class CrewaiTool(FunctionTool):
    def __init__(self, tool: CrewaiBaseTool, *, name: str, description: str):
        # name and description REQUIRED
```

### InMemoryRunner
```python
# From: runners.py, line 1135
class InMemoryRunner(Runner):
    def __init__(
        self,
        agent: Optional[BaseAgent] = None,
        *,
        app_name: Optional[str] = 'InMemoryRunner',
        plugins: Optional[list[BasePlugin]] = None,
        app: Optional[App] = None,
    ):
```

---

## Priority: CRITICAL - Fix Before Any Other Tutorial

This tutorial has the **most severe** issues found so far:
- Import paths completely wrong (module doesn't exist)
- 100% failure rate on import
- Core functionality completely broken

Must be fixed before Tutorial 27 can be used at all.
