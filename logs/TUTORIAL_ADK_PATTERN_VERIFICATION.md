# Tutorial ADK Pattern Verification Report

**Date**: October 8, 2025  
**Verification Scope**: Tutorials 29-35  
**Status**: ⚠️ ISSUES FOUND - 5 of 7 tutorials need corrections

---

## Executive Summary

**Verified Tutorials**: 7 total  
**Correct Implementations**: 2 (Tutorials 31, 35)  
**Incorrect Implementations**: 5 (Tutorials 29, 30, 32, 33, 34)

### Critical Issue

Multiple tutorials use the **deprecated/incorrect** `client.agentic.create_agent()` API instead of the **correct** `google.adk.agents.Agent` class.

**Incorrect Pattern** ❌:
```python
from google import genai
client = genai.Client(http_options={'api_version': 'v1alpha'})
agent = client.agentic.create_agent(
    model='gemini-2.0-flash-exp',
    name='my_agent'
)
```

**Correct Pattern** ✅:
```python
from google.adk.agents import Agent

agent = Agent(
    model="gemini-2.0-flash-exp",
    name="my_agent",
    instruction="You are a helpful assistant."
)
```

---

## Detailed Findings

### ✅ Tutorial 31: React Vite + ADK Integration - CORRECT

**Status**: No issues found  
**Pattern Used**: `google.adk.agents.Agent`  
**Lines Verified**: 193, 330, 359

**Example Code**:
```python
from google.adk.agents import Agent

adk_agent = Agent(
    name="data_analyst",
    model="gemini-2.0-flash-exp",
    instruction="""...""",
    tools=[load_csv_data, analyze_data, create_chart]
)

agent = ADKAgent(
    adk_agent=adk_agent,
    app_name="data_analyst",
    user_id="demo_user"
)
```

**Verdict**: ✅ Fully compliant with ADK best practices

---

### ✅ Tutorial 35: AG-UI Deep Dive - CORRECT

**Status**: No issues found  
**Pattern Used**: `google.adk.agents.Agent`  
**Lines Verified**: 144, 231, 278

**Example Code**:
```python
from google.adk.agents import Agent

adk_agent = Agent(
    name="research_agent",
    model="gemini-2.0-flash-exp",
    instruction="""...""",
    tools=[search_web, analyze_document]
)

agent = ADKAgent(
    adk_agent=adk_agent,
    app_name="research_assistant"
)
```

**Verdict**: ✅ Fully compliant with ADK best practices

---

### ⚠️ Tutorial 29: UI Integration Intro - ISSUES FOUND

**Status**: Mixed - some correct, some incorrect  
**Correct Examples**: Lines 201, 204, 286, 290, 606, 608  
**Incorrect Examples**: Lines 361, 407, 469, 540

#### Issue 1: Line 361-365 (Native API Example)

**Current (INCORRECT)**:
```python
# Backend (Python)
from google import genai

client = genai.Client(http_options={'api_version': 'v1alpha'})

# ADK automatically creates web server
agent = client.agentic.create_agent(
    model='gemini-2.0-flash-exp',
    name='my_agent'
)

# Run server: python your_agent.py --server
```

**Should Be (CORRECT)**:
```python
# Backend (Python)
from google.adk.agents import Agent

# Create ADK agent
agent = Agent(
    model='gemini-2.0-flash-exp',
    name='my_agent',
    instruction='You are a helpful assistant.'
)

# To run as web server, use adk web command:
# adk web agent.py
```

#### Issue 2: Line 407-420 (Streamlit Example)

**Current (INCORRECT)**:
```python
import streamlit as st
from google import genai

# Initialize agent
client = genai.Client(http_options={'api_version': 'v1alpha'})
agent = client.agentic.create_agent(
    model='gemini-2.0-flash-exp',
    name='data_analyst'
)

# Streamlit UI
if prompt := st.chat_input("Ask me about your data"):
    st.chat_message("user").write(prompt)
    
    # Direct agent call (no HTTP)
    session = client.agentic.create_session(agent=agent.name)
    response = session.send_message(prompt)
    
    st.chat_message("assistant").write(response.text)
```

**Should Be (CORRECT)**:
```python
import streamlit as st
from google.adk.agents import Agent

# Initialize agent (in-process)
agent = Agent(
    model='gemini-2.0-flash-exp',
    name='data_analyst',
    instruction='You are a data analysis expert.'
)

# Streamlit UI
if prompt := st.chat_input("Ask me about your data"):
    st.chat_message("user").write(prompt)
    
    # Direct agent call (no HTTP, no sessions)
    response = agent(prompt)
    
    st.chat_message("assistant").write(response.text)
```

#### Issue 3: Line 469-475 (Slack Example)

**Current (INCORRECT)**:
```python
@app.message("")
def handle_message(message, say):
    # Get ADK agent response
    agent = client.agentic.get_agent("support_agent")
    session = client.agentic.create_session(agent=agent.name)
    response = session.send_message(message['text'])
    
    # Reply in Slack thread
    say(response.text, thread_ts=message['ts'])
```

**Should Be (CORRECT)**:
```python
# Initialize agent once at startup
agent = Agent(
    model='gemini-2.0-flash-exp',
    name='support_agent',
    instruction='You are a helpful Slack support bot.'
)

@app.message("")
def handle_message(message, say):
    # Direct agent call
    response = agent(message['text'])
    
    # Reply in Slack thread
    say(response.text, thread_ts=message['ts'])
```

#### Issue 4: Line 540-545 (Pub/Sub Example)

**Current (INCORRECT)**:
```python
def callback(message):
    # Process with ADK agent
    client = genai.Client(http_options={'api_version': 'v1alpha'})
    agent = client.agentic.get_agent("doc_processor")
    session = client.agentic.create_session(agent=agent.name)
    response = session.send_message(message.data.decode())
    message.ack()
```

**Should Be (CORRECT)**:
```python
# Initialize agent once at startup
agent = Agent(
    model='gemini-2.0-flash-exp',
    name='doc_processor',
    instruction='You process documents and extract information.'
)

def callback(message):
    # Process with ADK agent
    response = agent(message.data.decode())
    
    # Publish result or ack
    message.ack()
```

**Verdict**: ⚠️ Needs updates to 4 code examples

---

### ⚠️ Tutorial 30: Next.js + ADK Integration - ISSUES FOUND

**Status**: Mixed - main implementation correct, examples incorrect  
**Correct Examples**: Lines 196, 292, 317  
**Incorrect Examples**: Lines 616, 772, 1290

#### Issue 1: Line 616-623 (Testing Section)

**Context**: Testing with agent API  
**Location**: "Testing Your Integration" section

**Current (INCORRECT)**:
```python
# Test agent directly
agent = client.agentic.create_agent(
    model='gemini-2.0-flash-exp',
    name='test_agent'
)
```

**Should Be (CORRECT)**:
```python
# Test agent directly
agent = Agent(
    model='gemini-2.0-flash-exp',
    name='test_agent',
    instruction='You are a test assistant.'
)
```

#### Issue 2: Line 772-779 (Streaming Example)

**Current (INCORRECT)**:
```python
agent = client.agentic.create_agent(
    model='gemini-2.0-flash-exp',
    name='streaming_agent',
    stream=True
)
```

**Should Be (CORRECT)**:
```python
agent = Agent(
    model='gemini-2.0-flash-exp',
    name='streaming_agent',
    instruction='You are a helpful assistant.',
    # Streaming is handled by AG-UI middleware, not agent config
)
```

#### Issue 3: Line 1290-1297 (Production Deployment)

**Current (INCORRECT)**:
```python
agent = client.agentic.create_agent(
    model='gemini-2.0-flash-exp',
    name='production_agent'
)
```

**Should Be (CORRECT)**:
```python
agent = Agent(
    model='gemini-2.0-flash-exp',
    name='production_agent',
    instruction='You are a production-ready assistant.'
)
```

**Verdict**: ⚠️ Needs updates to 3 code examples

---

### ⚠️ Tutorial 32: Streamlit + ADK Integration - ISSUES FOUND

**Status**: Documentation conflicts with test implementation  
**Incorrect Examples**: Lines 654, 1594

#### Critical Issue: Documentation vs Implementation Mismatch

The **test implementation** (tutorial32_test/) correctly uses `google.adk.agents.Agent`, but the **tutorial documentation** shows incorrect `client.agentic.create_agent()` pattern.

#### Issue 1: Line 654-660 (Main Example)

**Current (INCORRECT)**:
```python
def get_agent():
    """Initialize and return ADK agent."""
    client = genai.Client(http_options={'api_version': 'v1alpha'})
    
    agent = client.agentic.create_agent(
        model='gemini-2.0-flash-exp',
        name='data_analyst',
        instruction=AGENT_INSTRUCTION
    )
    
    return agent
```

**Should Be (CORRECT)** - Match test implementation:
```python
from google.adk.agents import Agent

def get_agent():
    """Initialize and return ADK agent."""
    agent = Agent(
        model='gemini-2.0-flash-exp',
        name='data_analyst',
        instruction=AGENT_INSTRUCTION
    )
    
    return agent
```

#### Issue 2: Line 1594-1601 (Production Section)

**Current (INCORRECT)**:
```python
agent = client.agentic.create_agent(
    model='gemini-2.0-flash-exp',
    name='production_analyst'
)
```

**Should Be (CORRECT)**:
```python
agent = Agent(
    model='gemini-2.0-flash-exp',
    name='production_analyst',
    instruction='You are a production data analyst.'
)
```

**Verdict**: ⚠️ CRITICAL - Documentation must match working test implementation

---

### ⚠️ Tutorial 33: Slack + ADK Integration - ISSUES FOUND

**Status**: All examples incorrect  
**Incorrect Examples**: Lines 201, 689, 1671

#### Issue 1: Line 201-208 (Quick Start)

**Current (INCORRECT)**:
```python
agent = client.agentic.create_agent(
    model='gemini-2.0-flash-exp',
    name='slack_agent',
    instruction=AGENT_INSTRUCTION
)
```

**Should Be (CORRECT)**:
```python
from google.adk.agents import Agent

agent = Agent(
    model='gemini-2.0-flash-exp',
    name='slack_agent',
    instruction=AGENT_INSTRUCTION
)
```

#### Issue 2: Line 689-696 (Full Implementation)

**Current (INCORRECT)**:
```python
agent = client.agentic.create_agent(
    model='gemini-2.0-flash-exp',
    name='slack_support_bot'
)
```

**Should Be (CORRECT)**:
```python
agent = Agent(
    model='gemini-2.0-flash-exp',
    name='slack_support_bot',
    instruction='You are a helpful Slack support bot.'
)
```

#### Issue 3: Line 1671-1678 (Advanced Features)

**Current (INCORRECT)**:
```python
agent = client.agentic.create_agent(
    model='gemini-2.0-flash-exp',
    name='advanced_slack_bot'
)
```

**Should Be (CORRECT)**:
```python
agent = Agent(
    model='gemini-2.0-flash-exp',
    name='advanced_slack_bot',
    instruction='You are an advanced Slack bot with rich features.'
)
```

**Verdict**: ⚠️ Needs updates to all 3 code examples

---

### ⚠️ Tutorial 34: Pub/Sub + ADK Integration - ISSUES FOUND

**Status**: All examples incorrect  
**Incorrect Examples**: Lines 289, 616, 742

#### Issue 1: Line 289-296 (Publisher Example)

**Current (INCORRECT)**:
```python
agent = client.agentic.create_agent(
    model='gemini-2.0-flash-exp',
    name='pubsub_processor'
)
```

**Should Be (CORRECT)**:
```python
from google.adk.agents import Agent

agent = Agent(
    model='gemini-2.0-flash-exp',
    name='pubsub_processor',
    instruction='You process Pub/Sub messages and extract insights.'
)
```

#### Issue 2: Line 616-623 (Subscriber Example)

**Current (INCORRECT)**:
```python
agent = client.agentic.create_agent(
    model='gemini-2.0-flash-exp',
    name='document_processor'
)
```

**Should Be (CORRECT)**:
```python
agent = Agent(
    model='gemini-2.0-flash-exp',
    name='document_processor',
    instruction='You analyze documents from Pub/Sub queue.'
)
```

#### Issue 3: Line 742-749 (Production Example)

**Current (INCORRECT)**:
```python
agent = client.agentic.create_agent(
    model='gemini-2.0-flash-exp',
    name='production_processor'
)
```

**Should Be (CORRECT)**:
```python
agent = Agent(
    model='gemini-2.0-flash-exp',
    name='production_processor',
    instruction='You are a production event processor.'
)
```

**Verdict**: ⚠️ Needs updates to all 3 code examples

---

## Impact Analysis

### Severity: HIGH

**Why This Matters**:
1. **API Doesn't Exist**: `client.agentic.create_agent()` is not a real ADK API
2. **Confuses Learners**: Students following tutorials will get errors
3. **Conflicts with Tests**: Tutorial 32 docs don't match working test code
4. **Inconsistent**: Only 2 of 7 tutorials show correct pattern

### Affected Lines Summary

| Tutorial | Total Issues | Affected Lines | Status |
|----------|--------------|----------------|--------|
| Tutorial 29 | 4 | 361, 407, 469, 540 | ⚠️ Fix Required |
| Tutorial 30 | 3 | 616, 772, 1290 | ⚠️ Fix Required |
| Tutorial 31 | 0 | - | ✅ Correct |
| Tutorial 32 | 2 | 654, 1594 | ⚠️ Fix Required |
| Tutorial 33 | 3 | 201, 689, 1671 | ⚠️ Fix Required |
| Tutorial 34 | 3 | 289, 616, 742 | ⚠️ Fix Required |
| Tutorial 35 | 0 | - | ✅ Correct |
| **Total** | **15** | **15 code blocks** | **5 tutorials** |

---

## Correction Plan

### Phase 1: Update Tutorial 32 (Highest Priority)

**Why First**: Documentation conflicts with working test implementation

**Tasks**:
1. Update lines 654-660 to use `google.adk.agents.Agent`
2. Update line 1594-1601 to use correct pattern
3. Remove all `client.agentic` references
4. Add note about direct in-process execution

**Estimated Time**: 15 minutes

---

### Phase 2: Update Tutorial 29 (Foundation Tutorial)

**Why Second**: This is the introduction tutorial - sets expectations

**Tasks**:
1. Update line 361-365 (Native API example)
2. Update line 407-420 (Streamlit example)
3. Update line 469-475 (Slack example)
4. Update line 540-545 (Pub/Sub example)
5. Add clarification about different integration patterns

**Estimated Time**: 30 minutes

---

### Phase 3: Update Tutorials 30, 33, 34 (Feature Tutorials)

**Tasks**:
- Tutorial 30: Update 3 code blocks (lines 616, 772, 1290)
- Tutorial 33: Update 3 code blocks (lines 201, 689, 1671)
- Tutorial 34: Update 3 code blocks (lines 289, 616, 742)

**Estimated Time**: 45 minutes total (15 min each)

---

### Phase 4: Verification

**Tasks**:
1. Re-run grep search for `client.agentic` across all tutorials
2. Verify all code uses `google.adk.agents.Agent`
3. Update this verification report with results
4. Mark as complete

**Estimated Time**: 15 minutes

---

## Recommended Pattern Template

For all tutorials, use this consistent pattern:

```python
"""
Standard ADK Agent Pattern for All Tutorials
"""

# CORRECT IMPORT
from google.adk.agents import Agent

# CORRECT AGENT CREATION
agent = Agent(
    model="gemini-2.0-flash-exp",
    name="agent_name",
    instruction="Clear instruction about agent's role and behavior.",
    tools=[tool1, tool2]  # Optional: list of functions
)

# CORRECT EXECUTION
# For direct calls (Streamlit, CLI):
response = agent(user_query)

# For AG-UI integration:
from ag_ui_adk import ADKAgent
ag_ui_agent = ADKAgent(
    adk_agent=agent,
    app_name="app_name",
    user_id="user_id"
)
```

---

## Next Actions

### Immediate (Today)
1. ✅ Complete this verification report
2. ⏳ Update Tutorial 32 (highest priority)
3. ⏳ Update Tutorial 29 (foundation)

### Short-term (This Week)
4. ⏳ Update Tutorials 30, 33, 34
5. ⏳ Re-verify all tutorials
6. ⏳ Update CHECKLIST.md

### Documentation
7. ⏳ Add note to overview.md about correct pattern
8. ⏳ Create ADK_PATTERNS.md reference guide
9. ⏳ Update README with pattern guidelines

---

## Verification Checklist

Use this checklist when reviewing future tutorials:

- [ ] Imports `from google.adk.agents import Agent`
- [ ] Creates agent with `Agent(model=..., name=..., instruction=...)`
- [ ] No usage of `client.agentic.create_agent()`
- [ ] No usage of `client.agentic.create_session()`
- [ ] Direct execution uses `agent(query)` pattern
- [ ] AG-UI integration uses `ADKAgent(adk_agent=...)`
- [ ] Tool integration passes functions directly to `tools=[...]`
- [ ] Examples are self-contained and runnable
- [ ] Code matches any test implementations

---

## References

### Correct Pattern Sources

1. **Tutorial 32 Test Implementation**:
   - File: `test_tutorials/tutorial32_test/backend/agent.py`
   - Lines: 14 (import), 364-370 (agent creation)
   - Status: ✅ Correct implementation with 53 passing tests

2. **Tutorial 31 Documentation**:
   - File: `tutorial/31_react_vite_adk_integration.md`
   - Lines: 193, 330, 359
   - Status: ✅ Correct pattern throughout

3. **Tutorial 35 Documentation**:
   - File: `tutorial/35_agui_deep_dive.md`
   - Lines: 144, 231, 278
   - Status: ✅ Correct pattern throughout

### Official Documentation

- **ADK Agents Guide**: https://google.github.io/adk-docs/agents/
- **Agent API Reference**: https://google.github.io/adk-docs/api/agents/
- **Best Practices**: overview.md (Mental Models section)

---

## Conclusion

**Current State**: 5 of 7 tutorials contain incorrect ADK patterns that will confuse learners and cause runtime errors.

**Required Action**: Update 15 code blocks across 5 tutorials to use correct `google.adk.agents.Agent` pattern.

**Timeline**: ~2 hours total for all corrections + verification.

**Priority Order**: Tutorial 32 → Tutorial 29 → Tutorials 30, 33, 34 → Final verification

**Success Criteria**: 
- Zero usage of `client.agentic.create_agent()` in any tutorial
- All code examples use `google.adk.agents.Agent`
- Documentation matches test implementations
- grep search shows no incorrect patterns

---

**Report Status**: ✅ COMPLETE  
**Next Step**: Begin corrections starting with Tutorial 32  
**Created By**: GitHub Copilot Agent  
**Date**: October 8, 2025
