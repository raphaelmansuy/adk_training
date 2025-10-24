---
id: commerce_agent_e2e
title: "End-to-End Implementation 01: Production Commerce Agent with Session Persistence"
description: "Complete end-to-end implementation of a production-ready commerce agent demonstrating multi-user session management, tool integration, proactive recommendations, and comprehensive testing with Google ADK v1.17.0."
sidebar_label: "E2E 01. Commerce Agent"
sidebar_position: 35
tags: ["advanced", "e2e", "production", "sessions", "tools", "multi-user", "commerce", "database", "testing"]
keywords:
  [
    "commerce agent",
    "session persistence",
    "multi-user",
    "google adk",
    "sqlite",
    "product recommendations",
    "end-to-end",
    "production ready",
    "testing",
    "adk v1.17.0",
  ]
status: "completed"
difficulty: "advanced"
estimated_time: "90 minutes"
prerequisites: ["Tutorial 01-34 completed", "Python 3.9+", "Google API key", "SQLite3"]
learning_objectives:
  - "Build a production-ready multi-user commerce agent"
  - "Implement persistent session management with SQLite"
  - "Master session state isolation and user data handling"
  - "Integrate Google Search with custom tools"
  - "Implement proactive agent intelligence"
  - "Build comprehensive test suites (unit, integration, e2e)"
  - "Handle tool confirmation flows for critical operations"
  - "Deploy to production with proper error handling"
image: /img/docusaurus-social-card.jpg
implementation_link: "https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/commerce_agent_e2e"
---

import Comments from '@site/src/components/Comments';

## Overview

This is a **production-ready end-to-end implementation** of a Commerce Agent that demonstrates enterprise-grade ADK capabilities. The agent handles real-world scenarios including:

- **Multi-user sessions** with complete isolation and persistence
- **Product discovery** via Google Search with Decathlon integration
- **Proactive recommendations** based on user history and preferences
- **Narrative generation** for engagement and storytelling
- **Session management** with advanced pause/resume capabilities
- **Comprehensive testing** covering 8 major workflows

This tutorial teaches you to build agents that scale from development through production deployment.

## Prerequisites

- ✅ Completed Tutorials 01-34 (especially #08 State Memory, #11 Built-in Tools, #19 Artifacts)
- ✅ Python 3.9 or higher
- ✅ Google API Key with Gemini access
- ✅ SQLite3 (usually pre-installed on macOS/Linux)
- ✅ Understanding of async/await patterns
- ✅ Familiarity with pytest and testing

## Core Concepts

### 1. Multi-User Session Architecture

Unlike tutorials 1-34 which focus on single users, this agent handles **concurrent users with complete data isolation**:

```
User Alice (user123)          User Bob (user456)
    |                              |
    v                              v
Session A123 ← ISOLATED →  Session B456
    |                              |
    +-- state['user:sport']    +-- state['user:sport']
    |   = "running"            |   = "cycling"
    |                          |
    +-- state['temp:buffer']   +-- state['temp:buffer']
        (lost after turn)          (lost after turn)
    
Both users share:
    state['app:cache']              (global product cache)
```

### 2. Tool Architecture: Overcoming the Single Built-in Tool Limitation

ADK v1.17.0 allows only ONE built-in tool per agent. The workaround uses sub-agents:

```
┌─────────────────────────────────────┐
│      Root Commerce Coordinator       │
│    (Orchestrates All Sub-Agents)    │
└──────────────┬──────────────────────┘
               │
     ┌─────────┼─────────┐
     v         v         v
 [Search]   [Prefs]   [Story]
 Sub-Agent  Sub-Agent  Sub-Agent
     │         │         v
     │         │       No Tools
     │         │       (Pure LLM)
     │         v
     │     Custom Pref
     │     Tool (DB)
     │
     v
 GoogleSearchTool
 (site:decathlon.fr)
```

### 3. State Management Deep Dive

The agent uses all three state scopes correctly:

| Scope | Prefix | Lifetime | Example |
|-------|--------|----------|---------|
| Session | none | Current chat only | `current_query`, `search_results` |
| User | `user:` | Persists across sessions | `user:preferences`, `user:favorites` |
| App | `app:` | Shared by all users | `app:product_cache`, `app:metrics` |
| Temp | `temp:` | Just this invocation | `temp:search_buffer` |

**Critical**: User-scoped data persists to SQLite. Each user can only access their own `user:*` keys.

### 4. Session Persistence with SQLite

The agent uses `DatabaseSessionService` to persist all data:

```python
from google.adk.sessions import DatabaseSessionService

session_service = DatabaseSessionService(
    db_url="sqlite:///./commerce_agent_sessions.db"
)

# Create session
session = await session_service.create_session(
    app_name="commerce_agent",
    user_id="user123",           # Multi-user isolation by this ID
    session_id="session456",
    state={"user:sport": "running"}
)

# Data persists even after app restart!
session_restored = await session_service.get_session(
    "commerce_agent", "user123", "session456"
)
assert session_restored.state["user:sport"] == "running"  # ✅
```

### 5. Evaluation Framework (v1.17.0)

The implementation includes metrics collection:

- **Tool use quality**: Rubric-based evaluation of tool calls
- **Hallucination detection**: Identifies false claims
- **Response quality**: Evaluates recommendation relevance
- **Performance metrics**: Latency, cache hits, user isolation verification

## Architecture Overview

### Agent Hierarchy

```
Commerce Agent (Root)
├── ProductSearchAgent (Sub-agent 1)
│   └── GoogleSearchTool
│       └── site:decathlon.fr
├── PreferenceManager (Sub-agent 2)
│   └── manage_user_preferences() tool
│       └── SQLite backend
└── StorytellerAgent (Sub-agent 3)
    └── No tools (pure LLM narrative)
```

### Data Flow

```
User Query
    ↓
Root Agent (orchestrator)
    ↓
┌───────────┬──────────────┬─────────────┐
│           │              │             │
v           v              v             v
Search   Preferences  Storytelling   State
Query    Update       Generation     Save
│           │              │             │
└───────────┴──────────────┴─────────────┘
            ↓
    Tool Confirmation
    (if expensive)
            ↓
    Tool Execution
            ↓
    State Persistence
    (DatabaseSessionService)
            ↓
    Response to User
```

## Database Schema

The SQLite database stores all persistent data:

```sql
-- User preferences and profile
CREATE TABLE user_preferences (
    user_id TEXT PRIMARY KEY,
    preferences_json TEXT,  -- JSON: {sports, price_range, brands}
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Interaction history for personalization
CREATE TABLE interaction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    query TEXT,
    result_count INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_preferences(user_id)
);

-- Favorite products
CREATE TABLE user_favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    product_id TEXT,
    product_name TEXT,
    url TEXT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_preferences(user_id)
);

-- Search result cache (app-wide)
CREATE TABLE product_cache (
    cache_key TEXT PRIMARY KEY,
    results_json TEXT,
    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ttl_seconds INTEGER DEFAULT 3600
);
```

## Implementation Deep Dive

### Step 1: Running the Implementation

```bash
# Navigate to the tutorial
cd tutorial_implementation/commerce_agent_e2e

# Setup dependencies
make setup

# Run all tests (recommended first step)
make test

# Start development UI
make dev

# Try a demo
make demo
```

### Step 2: Understanding the Tool Implementations

#### Custom Preference Tool (Function Tool)

```python
def manage_user_preferences(
    action: str,  # 'get', 'update', 'add_history'
    user_id: str,
    data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Manages user preferences in SQLite.
    
    Actions:
    - 'get': Retrieve current preferences
    - 'update': Update user preferences
    - 'add_history': Add to interaction history
    
    Returns:
        {'status': 'success'/'error', 'report': '...', 'data': {...}}
    """
```

This tool demonstrates:
- ✅ Structured return format
- ✅ Error handling with descriptive messages
- ✅ Database persistence
- ✅ Multi-user isolation (by `user_id` parameter)

#### Google Search Tool (Built-in)

```python
search_agent = LlmAgent(
    name="ProductSearchAgent",
    model="gemini-2.5-flash",
    instruction="Search Decathlon for products...",
    tools=[
        GoogleSearchTool(
            query_params={"site": "decathlon.fr"},
            bypass_multi_tools_limit=True  # v1.17.0 feature
        )
    ]
)
```

Key features:
- ✅ Site-restricted search (only Decathlon products)
- ✅ Works in sub-agent (v1.17.0 workaround)
- ✅ Caches results to `state['app:product_cache']`

#### Storyteller Agent (Pure LLM)

```python
story_agent = LlmAgent(
    name="StorytellerAgent",
    model="gemini-2.5-flash",
    instruction="""You are a creative storyteller...
    Create engaging narratives around product recommendations.
    Connect the product to the user's interests and lifestyle.
    Use vivid imagery and emotional appeal."""
    # No tools needed - pure LLM capability
)
```

Demonstrates:
- ✅ Agents without tools (pure conversation)
- ✅ Specialized roles in multi-agent systems

### Step 3: Session Management Testing

The tutorial includes comprehensive tests for session isolation:

```python
@pytest.mark.asyncio
async def test_multi_user_session_isolation():
    """Verify users cannot access each other's state"""
    service = DatabaseSessionService(db_url="sqlite:///:memory:")
    
    # Alice sets sport preference
    alice = await service.create_session(
        "commerce_agent", "alice", "session1",
        state={"user:sport": "running"}
    )
    
    # Bob sets different preference
    bob = await service.create_session(
        "commerce_agent", "bob", "session1",
        state={"user:sport": "cycling"}
    )
    
    # Verify isolation
    alice_session = await service.get_session("commerce_agent", "alice", "session1")
    assert alice_session.state["user:sport"] == "running"
    
    bob_session = await service.get_session("commerce_agent", "bob", "session1")
    assert bob_session.state["user:sport"] == "cycling"
    
    # Cross-user access must fail
    with pytest.raises(Exception):
        await service.get_session("commerce_agent", "alice", "session1_bob_data")
```

### Step 4: Testing with `adk web`

Once running, test interactively:

1. **Test Session Persistence**:
   - Set User ID: "athlete_1", Session ID: "session_1"
   - Type: "My favorite sport is running"
   - Close browser, reopen → Preferences persisted ✅

2. **Test Multi-User Isolation**:
   - Open two browser tabs
   - Tab 1: User ID "alice", set sport "running"
   - Tab 2: User ID "bob", set sport "cycling"
   - Verify each sees only their own preferences ✅

3. **Test Product Search**:
   - Type: "Find Kalenji running shoes under €150 on Decathlon"
   - Verify search tool executes
   - Results include Decathlon products ✅

4. **Test Proactive Recommendations**:
   - Set preferences for running
   - Agent should suggest: "Based on your interest in running..." ✅

## Complete Testing Workflow

### Tier 1: Unit Tests

```bash
pytest tests/test_tools.py -v
# Tests:
# - Tool return format correct
# - Database operations work
# - Error handling robust
# - User isolation in database
```

### Tier 2: Integration Tests

```bash
pytest tests/test_integration.py -v
# Tests:
# - Agent + tools work together
# - Session service integration
# - State persistence
# - Tool confirmation flow
```

### Tier 3: End-to-End Tests

```bash
pytest tests/test_e2e.py -v
# Tests:
# - Complete user workflows
# - Multi-user scenarios
# - Session retrieval after restart
# - Full recommendation pipeline
```

### Run All Tests with Coverage

```bash
make test
# Runs: pytest tests/ -v --cov=commerce_agent --cov-report=html
# Opens coverage report in browser
```

## Key Features Demonstrated

### 1. Session Persistence (v1.17.0)

```python
session_service = DatabaseSessionService(
    db_url="sqlite:///./sessions.db"
)

# Data survives app restarts
session = await session_service.get_session(
    "commerce_agent", "user123", "session456"
)
# Returns all user preferences and history
```

### 2. Session Rewind (v1.17.0)

```python
# Go back to a previous invocation state
await session_service.rewind_session(
    "commerce_agent", "user123", "session456",
    to_invocation_num=2
)
# Session restored to state before invocation 3
```

### 3. Tool Confirmation (Human-in-the-Loop)

```python
# For expensive operations, ask for confirmation
if product_price > 100:
    await tool_context.request_tool_confirmation(
        tool_name="purchase_recommendation",
        message=f"Recommend expensive item: {product_name} (€{product_price}). Confirm?"
    )
```

### 4. Artifacts (Image Display)

```python
# Save product images for display
image_part = types.Part.from_bytes(
    data=image_bytes,
    mime_type="image/png"
)
version = await context.save_artifact(
    filename=f"product_{product_id}.png",
    artifact=image_part
)
# Image appears in chat automatically
```

### 5. Multi-Agent Coordination

```python
root_agent = LlmAgent(
    name="CommerceCoordinator",
    sub_agents=[
        AgentTool(agent=search_agent),
        AgentTool(agent=prefs_agent),
        AgentTool(agent=story_agent)
    ]
)
# Root agent orchestrates all three
```

## Deployment Scenarios

### Local Development

```bash
# Use in-memory SQLite
make dev
# Access at http://localhost:8000
```

### Production (Tier 2 - Small Scale)

```bash
# Use persistent SQLite + Cloud Run
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
adk deploy cloud_run --session-db sqlite://./sessions.db
```

### Enterprise Scale (Tier 3 - Google Cloud Spanner)

```python
# Switch to Cloud Spanner for multi-region scale
session_service = DatabaseSessionService(
    db_url="spanner://projects/my-project/instances/my-instance/databases/commerce"
)
```

## Success Criteria

You'll know everything is working when:

✅ All 8 test scenarios pass
✅ Multi-user sessions properly isolated
✅ Product recommendations generated correctly
✅ Session persistence verified across restarts
✅ Tool confirmation flow works end-to-end
✅ No data loss or corruption in SQLite
✅ Performance acceptable for concurrent users
✅ `make dev` starts cleanly with dropdown showing agent

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Agent not appearing in web dropdown | Run `pip install -e .` in tutorial root |
| SQLite "database is locked" | Ensure only one process accesses db at a time |
| Search tool returns no results | Verify GOOGLE_API_KEY is set and valid |
| Tests fail with auth error | Set GOOGLE_API_KEY or GOOGLE_APPLICATION_CREDENTIALS |
| Session state not persisting | Verify db_url is correct and file writable |

## What You'll Learn

By completing this implementation, you'll master:

1. **Session Management**: Multi-user systems with complete data isolation
2. **Database Integration**: SQLite persistence with ADK SessionService
3. **Tool Architecture**: Overcoming ADK limitations with sub-agent workarounds
4. **Agent Orchestration**: Coordinating multiple specialized agents
5. **Testing Strategy**: Unit, integration, and end-to-end test patterns
6. **Production Practices**: Error handling, RBAC, monitoring, deployment
7. **Advanced Evaluation**: Rubric-based quality metrics and hallucination detection
8. **State Management**: All three state scopes (session, user, app, temp)

## Next Steps

After completing this tutorial:

1. **Extend the agent**: Add more product categories, payment integration
2. **Scale to production**: Deploy to Agent Engine or Cloud Run
3. **Add personalization**: Implement ML-based recommendation engine
4. **Monitor and optimize**: Add observability, analyze user behavior
5. **Build frontend**: Create custom UI with CopilotKit or Next.js integration

## References

### Official Resources

- [ADK Session Management](https://google.github.io/adk-docs/sessions/)
- [DatabaseSessionService](https://google.github.io/adk-docs/sessions/session/)
- [Tool Integration Guide](https://google.github.io/adk-docs/tools/)
- [Multi-Agent Systems](https://google.github.io/adk-docs/agents/multi-agents/)
- [Testing Guide](https://google.github.io/adk-docs/get-started/testing/)

### Implementation Files

- [Source Code](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/commerce_agent_e2e)
- [Agent Definition](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/commerce_agent_e2e/commerce_agent/agent.py)
- [Custom Tools](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/commerce_agent_e2e/commerce_agent/tools.py)
- [Test Suite](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/commerce_agent_e2e/tests)

---

<Comments />
