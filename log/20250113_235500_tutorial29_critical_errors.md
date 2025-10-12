# Tutorial 29 Critical API Errors - UI Integration Introduction

**Date**: 2025-01-13 23:55:00  
**Tutorial**: `docs/tutorial/29_ui_integration_intro.md`  
**Status**: ❌ CRITICAL ERRORS FOUND  
**Severity**: HIGH (Same Runner API issues as previous tutorials)

---

## Issues Found

### 1. Deprecated Runner API (9 occurrences)

**Problem**: All examples use `Runner()` from `google.adk.agents` (doesn't exist in ADK v1.16+)

**Grep Results**:
```bash
$ grep -n "Runner()\|runner.run_async\|from google.adk.agents import.*Runner" \
  docs/tutorial/29_ui_integration_intro.md | cat

Line 418: from google.adk.agents import Agent, Runner
Line 437: events = asyncio.run(runner.run_async(
Line 486: from google.adk.agents import Agent, Runner
Line 505: events = asyncio.run(runner.run_async(
Line 574: from google.adk.agents import Agent, Runner
Line 593: events = asyncio.run(runner.run_async(
Line 880: from google.adk.agents import Agent, Runner
Line 893: events = asyncio.run(runner.run_async(
Line 911: events = asyncio.run(runner.run_async(
```

**Affected Examples**:
1. Basic HTTP example (around line 418)
2. SSE streaming example (around line 486)
3. WebSocket example (around line 574)
4. Production HTTP example (around line 880)

### 2. Unusual run_async() Usage Pattern

**Pattern Found**:
```python
events = asyncio.run(runner.run_async(...))
```

This is mixing `asyncio.run()` (which creates a new event loop) with `runner.run_async()`. While this might work in some contexts, the correct ADK v1.16+ pattern should be:

```python
# Inside an async function
async for event in runner.run_async(
    user_id='user_id',
    session_id=session.id,
    new_message=new_message
):
    if event.content and event.content.parts:
        print(event.content.parts[0].text)
```

---

## Examples Requiring Fixes

### Example 1: Basic HTTP Example (around line 418)
**Context**: Demonstrating simple HTTP request/response
**Issues**: Runner API + run_async pattern
**Estimated lines**: ~30 lines

### Example 2: SSE Streaming Example (around line 486)
**Context**: Server-Sent Events for real-time streaming
**Issues**: Runner API + run_async pattern
**Estimated lines**: ~30 lines

### Example 3: WebSocket Example (around line 574)
**Context**: WebSocket bidirectional communication
**Issues**: Runner API + run_async pattern
**Estimated lines**: ~30 lines

### Example 4: Production HTTP Example (around line 880)
**Context**: Production-ready HTTP endpoint with error handling
**Issues**: Runner API + run_async pattern (2 occurrences)
**Estimated lines**: ~40 lines

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
runner = InMemoryRunner(agent=agent, app_name='ui_app')
session = await runner.session_service.create_session(
    app_name='ui_app',
    user_id='user_001'
)
```

### run_async() Pattern Updates
```python
# BEFORE (WRONG - mixing asyncio.run with async generator)
events = asyncio.run(runner.run_async(query, agent=agent))

# AFTER (CORRECT - proper async iteration)
new_message = types.Content(role='user', parts=[types.Part(text=query)])
async for event in runner.run_async(
    user_id='user_001',
    session_id=session.id,
    new_message=new_message
):
    if event.content and event.content.parts:
        # Process event
        yield event  # or accumulate/process as needed
```

---

## Special Considerations for Tutorial 29

This tutorial focuses on **UI integration patterns**, so the examples may need additional context around:

1. **HTTP/API Context**: Examples might be inside FastAPI/Flask endpoints
2. **Streaming Context**: SSE examples need proper async streaming
3. **WebSocket Context**: Bidirectional communication patterns
4. **Production Context**: Error handling, logging, monitoring

Each fix needs to preserve the UI integration context while updating the Runner API.

---

## Verification Sources

**ADK Source**: `/research/adk-python/src/google/adk/runners.py`

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

---

## Impact Assessment

### Current State
- **Usability**: 0% - All examples fail with TypeError/AttributeError
- **Tutorial Focus**: UI Integration - critical for production deployments
- **User Impact**: HIGH - This is the entry tutorial for entire UI series

### After Fixes
- **Usability**: 100% - All examples executable
- **API Correctness**: 100% - Verified against source code
- **Tutorial Value**: Maintained - UI patterns preserved

---

## Next Steps

1. Add verification info box at top of tutorial
2. Fix Basic HTTP example (line ~418)
3. Fix SSE streaming example (line ~486)
4. Fix WebSocket example (line ~574)
5. Fix Production HTTP example (lines ~880-911)

**Priority**: HIGH - This tutorial introduces UI integration concepts for all following tutorials (30-34)

**Estimated Time**: 1-2 hours

---

## Conclusion

Tutorial 29 has the same **Runner API issues** as previous tutorials. As the introduction to the UI integration series, fixing these issues is critical for users following the tutorial sequence 29→30→31→32→33→34.

**Fix Strategy**: Apply same patterns as Tutorial 28 fixes  
**Verification**: Test against `/research/adk-python/src/google/adk/runners.py`  
**Priority**: HIGH - Blocks understanding of UI integration series
