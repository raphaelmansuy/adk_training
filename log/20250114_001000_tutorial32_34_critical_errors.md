# Critical Errors: Tutorials 32 & 34 - Undefined runner Variable

**Date**: 2025-01-14 00:10:00  
**Severity**: CRITICAL (NameError)  
**Issue**: Undefined `runner` variable in multiple examples  
**Tutorials Affected**: Tutorial 32 (Streamlit), Tutorial 34 (Pub/Sub)

---

## Executive Summary

**Problem**: Both tutorials reference `runner.run_async()` but never define the `runner` variable.  
**Impact**: 100% failure rate - NameError on execution  
**Root Cause**: Copy-paste error mixing ADK agent code with low-level genai client code  
**Fix**: Remove incorrect ADK runner references; use correct genai client API

---

## Tutorial 32: Streamlit ADK Integration

### File
`/docs/tutorial/32_streamlit_adk_integration.md`

### Issues Found

#### Issue 1: Undefined runner at Line 916 (Data Analysis Example)

**Location**: Lines 910-925 (chat response generation)

**Problem**:
```python
events = asyncio.run(runner.run_async(  # ❌ runner is undefined
    user_id='user1',
    session_id='session1',
    new_message=types.Content(
        parts=[types.Part(text=f"{context}\n\nUser question: {prompt}")],
        role='user'
    )
))
```

**Context**: This example uses low-level genai client API (not ADK):
- Agent defined with `Agent(model='...', tools=[...])`  
- But agent is used as genai client configuration, not ADK agent
- No `InMemoryRunner` created anywhere in example
- Code tries to use ADK runner API on genai client

**Diagnosis**:
1. The `get_agent()` function returns a genai `Agent` configuration (NOT ADK)
2. Example should use `client.aio.generate_content()` (genai API)
3. Someone incorrectly added `runner.run_async()` (ADK API)
4. These are two different APIs - cannot be mixed

---

#### Issue 2: Undefined runner at Line 1482 (Multi-Agent Routing Example)

**Location**: Lines 1470-1490 (routing between specialist agents)

**Problem**:
```python
# Similar issue - runner undefined
events = asyncio.run(runner.run_async(
    user_id='user1',
    session_id='session1',
    new_message=...
))
```

**Context**: Multi-agent routing example
- Uses genai client agent configuration
- No ADK InMemoryRunner created
- Same copy-paste error as Issue 1

---

#### Issue 3: Undefined runner at Line 1535 (Production Deployment Example)

**Location**: Lines 1530-1545 (production streaming pattern)

**Problem**:
```python
events = asyncio.run(runner.run_async(
    user_id='user1',
    session_id='session1',
    new_message=...
))
```

**Context**: Production deployment patterns
- Same genai client vs ADK confusion
- No runner initialization
- Third occurrence of same error

---

## Tutorial 34: Pub/Sub ADK Integration

### File
`/docs/tutorial/34_pubsub_adk_integration.md`

### Issues Found

#### Issue 4: Undefined runner at Line 361 (Basic Pub/Sub Example)

**Location**: Lines 355-370 (message processing callback)

**Problem**:
```python
events = asyncio.run(runner.run_async(
    user_id='system',
    session_id=message_id,
    new_message=...
))
```

**Context**: Pub/Sub subscriber callback
- Processing messages from Pub/Sub
- References undefined `runner`
- Same pattern as Tutorial 32

---

#### Issue 5: Undefined runner at Line 651 (Multi-Agent Coordination Example)

**Location**: Lines 640-660 (agent coordination via Pub/Sub)

**Problem**:
```python
events = asyncio.run(runner.run_async(
    user_id='user1',
    session_id=session_id,
    new_message=...
))
```

**Context**: Multi-agent system with Pub/Sub
- Coordinating multiple agents
- No runner initialization
- Second occurrence in Tutorial 34

---

#### Issue 6: Undefined runner at Line 836 (Production Deployment Example)

**Location**: Lines 830-845 (production Pub/Sub pattern)

**Problem**:
```python
events = asyncio.run(runner.run_async(
    user_id='user1',
    session_id=session_id,
    new_message=...
))
```

**Context**: Production deployment pattern
- Cloud Run + Pub/Sub integration
- No runner initialization
- Third occurrence in Tutorial 34

---

## Pattern Analysis

### Root Cause
1. **API Confusion**: Tutorials mix two different APIs:
   - **Genai Client API**: `client.aio.generate_content()` or `client.aio.generate_content_stream()`
   - **ADK Runner API**: `InMemoryRunner().run_async()`

2. **Copy-Paste Error**: Someone copied ADK runner code into genai client examples

3. **Missing Context**: Both tutorials use genai client but have ADK runner calls

### Fix Strategy

**Two Options**:

**Option A: Use Genai Client API (Simpler for these tutorials)**
- Remove all `runner.run_async()` calls
- Use `client.aio.generate_content()` or `client.aio.generate_content_stream()`
- Matches the rest of tutorial code structure

**Option B: Convert to ADK Runner API (More complex, full rewrite)**
- Add `from google.adk.runners import InMemoryRunner`
- Create runner: `runner = InMemoryRunner(agent=agent, app_name='app')`
- Create sessions properly
- Complete rewrite of examples

**Recommendation**: Option A (Use genai client) - simpler, matches tutorial structure

---

## Impact Assessment

### Tutorial 32 (Streamlit)
- **Examples Broken**: 3 out of ~6 major examples
- **Failure Mode**: NameError: name 'runner' is not defined
- **User Impact**: Cannot run data analysis, routing, or production examples
- **Fix Effort**: Medium (~100 lines across 3 examples)

### Tutorial 34 (Pub/Sub)
- **Examples Broken**: 3 out of ~5 major examples
- **Failure Mode**: NameError: name 'runner' is not defined
- **User Impact**: Cannot run any Pub/Sub integration examples
- **Fix Effort**: Medium (~80 lines across 3 examples)

### Combined Impact
- **Total Broken Examples**: 6
- **Error Type**: NameError (100% failure)
- **Lines to Fix**: ~180 lines
- **Tutorials Affected**: 2 of remaining 5

---

## Verification Required

For each fix, verify:

1. ✅ **Import Check**: Correct imports for genai client
2. ✅ **API Usage**: Using `client.aio.generate_content()` not `runner.run_async()`
3. ✅ **Async Pattern**: Proper `asyncio.run()` or native async
4. ✅ **Response Handling**: Correct iteration over genai response
5. ✅ **Error Handling**: Try/except blocks preserved

---

## Next Steps

1. ✅ Fix Tutorial 32 (3 examples)
2. ✅ Fix Tutorial 34 (3 examples)
3. ✅ Verify Tutorials 30, 31, 33 (confirmed clean)
4. ✅ Create completion logs
5. ✅ Update phase 2 progress report

---

## Lessons Learned

1. **API Clarity**: Genai client ≠ ADK runner - completely different APIs
2. **Copy-Paste Risk**: Check full context when copying code patterns
3. **Variable Scope**: Verify all variables are defined before use
4. **Testing**: NameError would be caught immediately by any test run

---

## Statistics

- **Tutorials Affected**: 2 (32, 34)
- **Examples Broken**: 6 total
- **Lines to Fix**: ~180
- **Fix Pattern**: Replace runner.run_async() with client.aio.generate_content()
- **Estimated Time**: 60-90 minutes for both tutorials
