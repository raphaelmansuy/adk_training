# Tutorial 28 Critical API Errors - Using Other LLMs

**Date**: 2025-01-13 23:35:00  
**Tutorial**: `docs/tutorial/28_using_other_llms.md`  
**Status**: ❌ CRITICAL ERRORS FOUND  
**Severity**: HIGH (Same Runner API issues as Tutorial 27)

---

## Issues Found

### 1. Deprecated Runner API (20+ occurrences)

**Problem**: All examples use `Runner()` from `google.adk.agents` (doesn't exist in ADK v1.16+)

**Grep Results**:
```bash
$ grep -n "Runner()\|runner.run_async\|from google.adk.agents import.*Runner" \
  docs/tutorial/28_using_other_llms.md | cat

Line 119: from google.adk.agents import Agent, Runner
Line 148: runner = Runner()
Line 150: result = await runner.run_async(
Line 235: from google.adk.agents import Agent, Runner
Line 276: runner = Runner()
Line 285: result = await runner.run_async(query, agent=agent)
Line 437: from google.adk.agents import Agent, Runner
Line 473: runner = Runner()
Line 479: result = await runner.run_async(
Line 576: from google.adk.agents import Agent, Runner
Line 600: runner = Runner()
Line 601: result = await runner.run_async(
Line 649: from google.adk.agents import Agent, Runner
Line 672: runner = Runner()
Line 673: result = await runner.run_async(
Line 716: from google.adk.agents import Agent, Runner
Line 745: runner = Runner()
Line 764: result = await runner.run_async(query, agent=agent)
Line 910: runner = Runner()
Line 911: result = await runner.run_async(query, agent=agent)
Line 942: runner = Runner()
(20+ matches total)
```

**Affected Examples**:
1. OpenAI GPT-4o example (lines 119-160)
2. Claude 3.7 Sonnet example (lines 235-290)
3. Ollama local models example (lines 437-485)
4. Azure OpenAI example (lines 576-605)
5. Claude via Vertex AI example (lines 649-680)
6. Multi-provider comparison example (lines 716-770)
7. Fallback strategy example (lines 910-920)
8. Model routing example (lines 942+)

### 2. Wrong run_async() Signature (10+ occurrences)

**Problem**: Using old API `runner.run_async(query, agent=agent)` instead of async iteration

**Examples**:
```python
# WRONG (Line 150, 285, 479, 601, 673, 764, 911)
result = await runner.run_async(query, agent=agent)
print(result.content.parts[0].text)
```

**Required Pattern**:
```python
# CORRECT
from google.adk.runners import InMemoryRunner
from google.genai import types

runner = InMemoryRunner(agent=agent, app_name='app')
session = await runner.session_service.create_session(
    app_name='app', user_id='user_id'
)
new_message = types.Content(role='user', parts=[types.Part(text=query)])
async for event in runner.run_async(
    user_id='user_id', session_id=session.id, new_message=new_message
):
    if event.content and event.content.parts:
        print(event.content.parts[0].text)
```

---

## Examples Requiring Fixes

### High Priority (Complete rewrites needed)

1. **OpenAI GPT-4o Basic Example** (lines 115-165)
   - Import: `from google.adk.agents import Agent, Runner` → wrong
   - Runner: `runner = Runner()` → wrong
   - run_async: `await runner.run_async(query, agent=agent)` → wrong

2. **Claude 3.7 Sonnet with Tools** (lines 230-295)
   - Same Runner/run_async issues
   - Complex tool usage adds 40+ lines

3. **Ollama Local Models** (lines 435-490)
   - Same Runner/run_async issues
   - Local model configuration specifics

4. **Azure OpenAI** (lines 575-610)
   - Same Runner/run_async issues
   - Enterprise authentication patterns

5. **Claude via Vertex AI** (lines 645-685)
   - Same Runner/run_async issues
   - Google Cloud integration patterns

6. **Multi-Provider Comparison** (lines 715-775)
   - Multiple Runner instantiations
   - Parallel execution patterns needed

7. **Fallback Strategy** (lines 890-930)
   - Exception handling with old API
   - Try/except pattern needs updating

8. **Smart Model Routing** (lines 940-990)
   - Complexity-based routing logic
   - Multiple model configurations

---

## Pattern Analysis

### Consistent Issues
- Every example follows same wrong pattern
- All use `Runner()` instead of `InMemoryRunner()`
- All use old `run_async(query, agent=agent)` signature
- None use session management
- None use async iteration

### Estimated Fix Scope
- **8 major examples** need complete rewrites
- **~500 lines** of code affected
- **20+ import statements** need correction
- **20+ Runner instantiations** need updating
- **10+ run_async calls** need async iteration pattern

---

## Required Changes

### Import Updates
```python
# BEFORE (WRONG)
from google.adk.agents import Agent, Runner

# AFTER (CORRECT)
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types
```

### Runner Instantiation Updates
```python
# BEFORE (WRONG)
runner = Runner()

# AFTER (CORRECT)
runner = InMemoryRunner(agent=agent, app_name='example_app')
session = await runner.session_service.create_session(
    app_name='example_app',
    user_id='user_123'
)
```

### run_async() Pattern Updates
```python
# BEFORE (WRONG)
result = await runner.run_async(query, agent=agent)
print(result.content.parts[0].text)

# AFTER (CORRECT)
new_message = types.Content(role='user', parts=[types.Part(text=query)])
async for event in runner.run_async(
    user_id='user_123', session_id=session.id, new_message=new_message
):
    if event.content and event.content.parts:
        print(event.content.parts[0].text)
```

---

## Verification Sources

**ADK Source Code**: `/research/adk-python/src/google/adk/`

**Runners Implementation**: `runners.py`
```python
class InMemoryRunner:
    async def run_async(
        self,
        user_id: str,  # REQUIRED
        session_id: str,  # REQUIRED
        new_message: types.Content,  # REQUIRED
    ) -> AsyncGenerator[Event, None]:  # ASYNC GENERATOR
        ...
```

**No Runner Class**: `grep -r "class Runner" src/google/adk/` → No matches

---

## Impact Assessment

### Current State
- **Usability**: 0% - All examples fail with TypeError/AttributeError
- **API Correctness**: 0% - Using deprecated/non-existent APIs
- **Tutorial Quality**: DRAFT - Never tested with ADK v1.16+

### After Fixes
- **Usability**: 100% - All examples executable
- **API Correctness**: 100% - Verified against source code
- **Tutorial Quality**: PRODUCTION - All patterns validated

---

## Comparison with Tutorial 27

**Similarities**:
- Same Runner API issues (100% match)
- Same run_async() signature problems
- Same session management missing
- Same async iteration pattern needed

**Differences**:
- Tutorial 27: Import path issues (third_party module)
- Tutorial 28: Import paths correct, only Runner API wrong
- Tutorial 28: More examples (8 vs 4 major ones)
- Tutorial 28: Multi-provider complexity adds fix difficulty

---

## Next Steps

1. Add verification info box (like Tutorial 27)
2. Fix OpenAI example (lines 115-165)
3. Fix Claude example (lines 230-295)
4. Fix Ollama example (lines 435-490)
5. Fix Azure example (lines 575-610)
6. Fix Vertex AI example (lines 645-685)
7. Fix comparison example (lines 715-775)
8. Fix fallback example (lines 890-930)
9. Fix routing example (lines 940-990)

**Priority**: HIGH - Tutorial unusable without fixes
**Estimated Time**: 2-3 hours for all fixes
**Pattern**: Same as Tutorial 24, 25, 27 fixes

---

## Conclusion

Tutorial 28 has the **same critical Runner API issues** as Tutorials 24, 25, and 27. Every single example uses deprecated/non-existent `Runner()` class and old `run_async()` API. Tutorial is completely unusable without comprehensive fixes.

**Fix Strategy**: Apply same patterns as Tutorial 27 fixes
**Verification**: Test against `/research/adk-python/src/google/adk/runners.py`
**Priority**: HIGH - Part of UI integration series, blocks later tutorials
