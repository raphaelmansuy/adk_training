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

This is a **production-ready end-to-end implementation** of a Commerce Agent that demonstrates essential ADK v1.17.0 capabilities in a clean, maintainable architecture. The agent handles real-world e-commerce scenarios including:

- **Grounding metadata extraction** from Google Search results for source attribution
- **Multi-user session management** with ADK state isolation (`user:` prefix)
- **Product discovery** via Google Search with site-specific filtering (Decathlon)
- **Personalized recommendations** based on saved user preferences
- **Type-safe tool interfaces** using TypedDict patterns
- **Comprehensive testing** covering unit, integration, and e2e scenarios
- **Optional SQLite persistence** for sessions that survive app restarts

This tutorial teaches you to build clean, testable agents that follow ADK best practices and scale from development through production deployment.

**Key Implementation Highlights:**
- ✅ **Simple Architecture**: One root agent with 3 tools (not complex multi-agent)
- ✅ **Grounding Callback**: Extract and monitor Google Search source attribution
- ✅ **Two Persistence Modes**: ADK state (default) or SQLite (optional)
- ✅ **Vertex AI Ready**: Optimized for Vertex AI with fallback to Gemini API
- ✅ **TypedDict Safety**: Type-safe tool returns with IDE autocomplete

## Prerequisites

- ✅ Completed Tutorials 01-34 (especially #08 State Memory, #11 Built-in Tools, #19 Artifacts)
- ✅ Python 3.9 or higher
- ✅ Google API Key with Gemini access
- ✅ SQLite3 (usually pre-installed on macOS/Linux)
- ✅ Understanding of async/await patterns
- ✅ Familiarity with pytest and testing

## Core Concepts

### 1. Simple Agent Architecture

This implementation uses a **clean, single-agent design** with three tools:

```text
┌─────────────────────────────────────┐
│      Commerce Agent (Root)          │
│   Personal Shopping Concierge       │
└──────────────┬──────────────────────┘
               │
     ┌─────────┼─────────┐
     v         v         v
[Search]   [Save]    [Get]
 Tool      Prefs     Prefs
  │
  v
AgentTool wrapping
Google Search Agent
(site:decathlon.com.hk)
```

**Why this approach?**

- ✅ Simpler to understand and maintain
- ✅ Follows ADK best practices from official samples
- ✅ Easier to test and debug
- ✅ Production-ready without overengineering

### 2. Multi-User State Isolation

The agent uses ADK's built-in state management with the `user:` prefix
for cross-session persistence:

```text
User Alice (alice)              User Bob (bob)
    |                              |
    v                              v
Session s1 ← ISOLATED →      Session s2
    |                              |
    +-- state['user:pref_sport']   +-- state['user:pref_sport']
    |   = "running"                |   = "cycling"
    |                              |
    +-- state['user:pref_budget']  +-- state['user:pref_budget']
        = 150                          = 200

Each user has completely isolated preferences
```

**Key Point**: The `user:` prefix in ADK state automatically provides
multi-user isolation. No complex database setup required for basic use cases.

### 3. State Management Deep Dive

The agent uses ADK state scopes correctly for different data lifetimes:

| Scope | Prefix | Lifetime | Example |
|-------|--------|----------|---------|
| Session | none | Current chat | `current_query` |
| User | `user:` | Across sessions | `user:pref_sport` |
| App | `app:` | Shared globally | `app:product_cache` |
| Temp | `temp:` | Current invocation | `temp:grounding_sources` |

**How it works:**

```python
# In save_preferences tool
def save_preferences(sport: str, budget_max: int, ..., tool_context: ToolContext):
    # Saves to user-scoped state (persists across sessions)
    tool_context.state["user:pref_sport"] = sport
    tool_context.state["user:pref_budget"] = budget_max
    # ✅ This data survives when user starts a new chat session

# In get_preferences tool
def get_preferences(tool_context: ToolContext):
    # Retrieves user-scoped state
    sport = tool_context.state.get("user:pref_sport")
    budget = tool_context.state.get("user:pref_budget")
    # ✅ Returns saved preferences from previous sessions
```

**Critical**: User-scoped data with `user:` prefix provides multi-user isolation.
User "alice" cannot access user "bob"'s preferences.

### 4. Optional SQLite Persistence

While ADK state (`user:` prefix) handles most use cases, the implementation
also supports SQLite for full session persistence:

**Two modes available:**

1. **ADK State (Default)**: `make dev`
   - Simple, works out-of-box
   - Preferences persist across invocations
   - Sessions lost on app restart

2. **SQLite (Advanced)**: `make dev-sqlite`
   - Full conversation history preserved  
   - Sessions survive app restarts
   - SQL query capabilities

```python
# SQLite mode (optional)
from google.adk.sessions import DatabaseSessionService

session_service = DatabaseSessionService(
    db_url="sqlite:///./commerce_sessions.db?mode=wal"
)

# Or use CLI:
# adk web --session_service_uri "sqlite:///./sessions.db?mode=wal"
```

**When to use SQLite:**
- ✅ Need conversation history across restarts
- ✅ Want SQL query capabilities
- ✅ Production deployment requirements

**When ADK state is enough:**
- ✅ Simple user preferences (sport, budget, experience)
- ✅ Development and testing
- ✅ Single-server deployments

### 5. Grounding Metadata Extraction (NEW in v1.17.0)

A key feature of this implementation is the **grounding callback** that extracts
source attribution from Google Search results:

```python
from commerce_agent import create_grounding_callback
from google.adk.runners import Runner

runner = Runner(
    agent=root_agent,
    after_model_callbacks=[create_grounding_callback(verbose=True)]
)
```

**What it extracts:**

- ✅ Source URLs and titles from grounding chunks
- ✅ Domain names (e.g., "decathlon.com.hk", "alltricks.com")
- ✅ Segment-level attribution (which sources support which claims)
- ✅ Confidence scores based on multi-source agreement

**Console output example:**

```text
====================================================================
✓ GROUNDING METADATA EXTRACTED
====================================================================
Total Sources: 5

Sources:
  1. [decathlon.com.hk] Brooks Divide 5 - Trail Running Shoes
  2. [alltricks.com] Brooks Divide 5 - €95 Free Shipping
  3. [runningwarehouse.com] Brooks Divide 5 Review

Grounding Supports: 8 segments
  1. [high] "Brooks Divide 5 costs €95" (3 sources)
  2. [medium] "ideal for beginner trail runners" (2 sources)
  ... and 6 more
====================================================================
```

**Why this matters:**

- ✅ **Transparency**: Users see which retailers/sources support each claim
- ✅ **Trust**: Multiple sources = higher confidence in recommendations
- ✅ **Debugging**: Console logs help verify search quality during development
- ✅ **Anti-hallucination**: Validate that URLs are from real search results

## Architecture Overview

### Agent Structure

The commerce agent uses a **simple, maintainable architecture**:

```text
Commerce Agent (Root)
├── Tool 1: search_products (AgentTool wrapping Google Search)
├── Tool 2: save_preferences (FunctionTool)
└── Tool 3: get_preferences (FunctionTool)
```

**No complex sub-agents**. This design:

- ✅ Follows ADK best practices from official samples
- ✅ Easier to test (fewer moving parts)
- ✅ Clearer debugging (single agent flow)
- ✅ Production-ready without overengineering

### Data Flow

```text
User Query ("Find running shoes under €100")
    ↓
Root Agent receives message
    ↓
┌───────────────────────────────────────┐
│ 1. Call get_preferences()             │
│    → Check if user has saved prefs    │
└───────────────┬───────────────────────┘
                ↓
┌───────────────────────────────────────┐
│ 2. If prefs missing:                  │
│    Ask clarifying questions           │
│    Then call save_preferences()       │
└───────────────┬───────────────────────┘
                ↓
┌───────────────────────────────────────┐
│ 3. Call search_products()             │
│    → Executes Google Search           │
│    → site:decathlon.com.hk filter     │
│    → Returns 3-5 products             │
└───────────────┬───────────────────────┘
                ↓
┌───────────────────────────────────────┐
│ 4. Grounding Callback (after_model)   │
│    → Extracts source attribution      │
│    → Logs to console                  │
│    → Stores in state['temp:*']        │
└───────────────┬───────────────────────┘
                ↓
┌───────────────────────────────────────┐
│ 5. Generate Response                  │
│    → Personalized recommendations     │
│    → Why each product fits user needs │
│    → Purchase links with retailers    │
└───────────────────────────────────────┘
                ↓
    Response to User
```

## Database Schema

The implementation includes a **simple SQLite database** used by the preference
tools for storing historical data and favorites. This is **optional** and
separate from ADK's session management.

**Database file**: `commerce_agent_sessions.db` (created automatically)

```sql
-- User preferences (managed by save_preferences/get_preferences tools)
CREATE TABLE user_preferences (
    user_id TEXT PRIMARY KEY,
    preferences_json TEXT,  -- JSON: {sports, price_range, brands}
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Interaction history for analytics (optional)
CREATE TABLE interaction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    query TEXT,
    result_count INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Favorite products (optional)
CREATE TABLE user_favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    product_id TEXT,
    product_name TEXT,
    url TEXT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Important clarifications:**

1. **ADK State vs Database**: The agent primarily uses ADK's `user:` state for
   preferences. The database is for additional features (history, favorites).

2. **Not for ADK Sessions**: This database does NOT store ADK session data.
   For that, use `DatabaseSessionService` with `make dev-sqlite`.

3. **Initialization**: Database is created automatically on first `make setup`
   via `init_database()` call.

## Implementation Deep Dive

### Step 1: Setup and Running

```bash
# Navigate to the tutorial
cd tutorial_implementation/commerce_agent_e2e

# Option 1: Install dependencies only
make setup

# Option 2: Setup with Vertex AI authentication (recommended)
make setup-vertex-ai  # Interactive script to configure service account
make setup

# Run all tests
make test

# Start development UI (ADK state persistence)
make dev

# OR start with SQLite persistence (survives restarts)
make dev-sqlite
```

### Step 2: Understanding the Tool Implementations

#### Tool 1: Product Search (AgentTool wrapping Google Search)

```python
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.google_search_tool import google_search

# Search agent with Google Search grounding
_search_agent = Agent(
    model="gemini-2.5-flash",
    name="sports_product_search",
    description="Search for sports products using Google Search with grounding",
    instruction="""Search for sports products and provide detailed information.

When searching:
1. Use comprehensive queries like "best trail running shoes under 100 euros 2025"
2. Extract key product information: name, brand, price, features
3. **CRITICAL**: Display URLs from search results with clear retailer attribution
4. Present 3-5 products with clickable links

Response format:
- Product name and brand
- Price in EUR
- Key features (2-3 bullet points)
- **Purchase Link**: Show with visible retailer domain
- Brief explanation of why it fits user needs
""",
    tools=[google_search],
)

# Export as AgentTool for use in main agent
search_products = AgentTool(agent=_search_agent)
```

**Key points:**

- ✅ Uses AgentTool pattern to wrap Google Search agent
- ✅ Site-restricted search via query params (e.g., "site:decathlon.com.hk")
- ✅ Grounding metadata automatically extracted by Google Search
- ✅ Works best with Vertex AI (Gemini API has site: operator limitations)

#### Tool 2: Save Preferences (FunctionTool)

```python
from typing import Dict, Any
from google.adk.tools import ToolContext

def save_preferences(
    sport: str,
    budget_max: int,
    experience_level: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """Save user preferences for personalized recommendations."""
    try:
        # Save to user state (persists across sessions)
        tool_context.state["user:pref_sport"] = sport
        tool_context.state["user:pref_budget"] = budget_max
        tool_context.state["user:pref_experience"] = experience_level
        
        return {
            "status": "success",
            "report": f"✓ Preferences saved: {sport}, max €{budget_max}, {experience_level} level",
            "data": {
                "sport": sport,
                "budget_max": budget_max,
                "experience_level": experience_level
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "report": f"Failed to save preferences: {str(e)}",
            "error": str(e)
        }
```

**Key points:**

- ✅ Uses `tool_context.state["user:*"]` for cross-session persistence
- ✅ Returns structured dict matching ToolResult TypedDict (but not in signature)
- ✅ Proper error handling with descriptive messages
- ✅ Simple and testable

#### Tool 3: Get Preferences (FunctionTool)

```python
def get_preferences(tool_context: ToolContext) -> Dict[str, Any]:
    """Retrieve saved user preferences."""
    try:
        state = tool_context.state
        
        prefs = {
            "sport": state.get("user:pref_sport"),
            "budget_max": state.get("user:pref_budget"),
            "experience_level": state.get("user:pref_experience")
        }
        
        # Filter out None values
        prefs = {k: v for k, v in prefs.items() if v is not None}
        
        if not prefs:
            return {
                "status": "success",
                "report": "No preferences saved yet",
                "data": {}
            }
        
        return {
            "status": "success",
            "report": f"Retrieved preferences: {', '.join(f'{k}={v}' for k, v in prefs.items())}",
            "data": prefs
        }
    except Exception as e:
        return {
            "status": "error",
            "report": f"Failed to retrieve preferences: {str(e)}",
            "error": str(e),
            "data": {}
        }
```

**Key points:**

- ✅ Reads from `user:*` state keys
- ✅ Handles missing preferences gracefully
- ✅ Returns consistent format

### Step 3: The Grounding Callback

```python
from commerce_agent.callbacks import create_grounding_callback

def create_grounding_callback(verbose: bool = True):
    """Create a grounding metadata extraction callback.
    
    Returns:
        Async callback function for use with Runner
    """
    
    async def extract_grounding_metadata(callback_context, llm_response):
        """Extract grounding metadata from LLM response."""
        if not hasattr(llm_response, 'candidates'):
            return None
        
        candidate = llm_response.candidates[0]
        if not hasattr(candidate, 'grounding_metadata'):
            return None
        
        metadata = candidate.grounding_metadata
        
        # Extract sources from grounding_chunks
        sources = []
        if hasattr(metadata, 'grounding_chunks'):
            for chunk in metadata.grounding_chunks:
                if hasattr(chunk, 'web') and chunk.web:
                    sources.append({
                        "title": chunk.web.title,
                        "uri": chunk.web.uri,
                        "domain": extract_domain(chunk.web.uri)
                    })
        
        # Store in temp state for current invocation
        callback_context.state["temp:_grounding_sources"] = sources
        
        if verbose:
            print(f"\n{'='*60}")
            print("✓ GROUNDING METADATA EXTRACTED")
            print(f"Total Sources: {len(sources)}")
            for i, source in enumerate(sources, 1):
                print(f"  {i}. [{source['domain']}] {source['title']}")
            print(f"{'='*60}\n")
        
        return None  # ADK callbacks return None
    
    return extract_grounding_metadata
```

**Usage with Runner:**

```python
from google.adk.runners import Runner
from commerce_agent import root_agent, create_grounding_callback

runner = Runner(
    agent=root_agent,
    after_model_callbacks=[create_grounding_callback(verbose=True)]
)
```

**Key points:**

- ✅ Function-based callback (not class-based)
- ✅ Goes in Runner's `after_model_callbacks`, not Agent
- ✅ Extracts source URLs, titles, domains from grounding_chunks
- ✅ Console logging for development visibility
- ✅ Stores in `temp:` state (current invocation only)

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

1. **Test Preference Workflow**:
   - Open http://localhost:8000
   - Select "commerce_agent" from dropdown
   - Type: "I want running shoes"
   - Agent should call `get_preferences` → ask for budget & experience
   - Type: "Under 150 euros, I'm a beginner"
   - Agent should call `save_preferences` → confirm saved ✅

2. **Test Product Search**:
   - Type: "Find trail running shoes"
   - Agent calls `search_products` 
   - Verify results include Decathlon products ✅
   - Check terminal for grounding metadata extraction logs

3. **Test Preference Persistence**:
   - Refresh browser (new session, same user)
   - Type: "What are my preferences?"
   - Agent should retrieve saved preferences from previous session ✅

4. **Test Personalized Recommendations**:
   - Type: "Recommend something for me"
   - Agent should reference saved sport/budget/experience ✅
   - Recommendations should be tailored to beginner level

**Note on Multi-User Testing**: The `adk web` UI doesn't have User ID input.
To test multi-user isolation, use the API endpoints directly (see
`docs/TESTING_WITH_USER_IDENTITIES.md` or run `make test-guide`).

## Complete Testing Workflow

### Test Organization

The test suite follows a clear structure:

```text
tests/
├── conftest.py                    # Test fixtures and configuration
├── test_tools.py                  # Unit tests for individual tools
├── test_integration.py            # Integration tests (agent + tools)
├── test_e2e.py                    # End-to-end user scenarios
├── test_agent_instructions.py     # Agent prompt/instruction tests
└── test_callback_and_types.py     # Callback and TypedDict tests
```

### Tier 1: Unit Tests

```bash
pytest tests/test_tools.py -v
```

**Tests:**

- ✅ `save_preferences` stores data in ADK state correctly
- ✅ `get_preferences` retrieves data from state
- ✅ Tool return format matches ToolResult TypedDict structure
- ✅ Error handling with proper status/report fields
- ✅ Missing preferences handled gracefully

### Tier 2: Integration Tests

```bash
pytest tests/test_integration.py -v
```

**Tests:**

- ✅ Agent configuration is valid (model, name, description)
- ✅ Agent has all 3 tools attached correctly
- ✅ Tool imports work (search_products, save_preferences, get_preferences)
- ✅ Package structure is correct
- ✅ Grounding callback imports successfully

### Tier 3: End-to-End Tests

```bash
pytest tests/test_e2e.py -v
```

**Tests:**

- ✅ Complete new user workflow (set prefs → search → get recommendations)
- ✅ Returning customer scenario (preferences persist across sessions)
- ✅ Multi-user isolation (Alice's prefs don't affect Bob's)
- ✅ Database operations (if using optional SQLite features)
- ✅ Error recovery scenarios

### Tier 4: Agent Instruction Tests

```bash
pytest tests/test_agent_instructions.py -v
```

**Tests:**

- ✅ Agent instruction contains preference workflow steps
- ✅ Instruction mentions all 3 tools
- ✅ Concierge persona is present
- ✅ Product presentation format specified

### Tier 5: Callback and Type Tests

```bash
pytest tests/test_callback_and_types.py -v
```

**Tests:**

- ✅ Grounding callback creates function correctly
- ✅ TypedDict structures are importable
- ✅ ToolResult matches expected format
- ✅ Callback can be attached to Runner

### Run All Tests with Coverage

```bash
make test
# Runs: pytest tests/ -v --cov=commerce_agent --cov-report=html
# Generates: htmlcov/index.html (opens automatically in browser)
```

**Expected Results:**

- ✅ 14+ tests passing
- ✅ 85%+ code coverage
- ✅ No import errors
- ✅ All test tiers green

## Key Features Demonstrated

### 1. Grounding Metadata Extraction (NEW)

The grounding callback extracts source attribution from Google Search:

```python
from commerce_agent import create_grounding_callback
from google.adk.runners import Runner

runner = Runner(
    agent=root_agent,
    after_model_callbacks=[create_grounding_callback(verbose=True)]
)
```

**What it provides:**

- ✅ Source URLs and titles from grounding_chunks
- ✅ Domain extraction (e.g., "decathlon.com.hk")
- ✅ Segment-level attribution (which sources support which claims)
- ✅ Console logging for debugging
- ✅ Anti-hallucination validation

### 2. ADK State Management (Primary Method)

Uses `user:` prefix for cross-session persistence:

```python
def save_preferences(..., tool_context: ToolContext):
    tool_context.state["user:pref_sport"] = sport
    tool_context.state["user:pref_budget"] = budget
    # ✅ Persists across invocations, isolated by user
```

**Benefits:**

- ✅ Zero configuration required
- ✅ Automatic multi-user isolation
- ✅ Works with any ADK deployment (web, CLI, API)
- ✅ Perfect for simple key-value preferences

### 3. Optional SQLite Persistence (Advanced)

Available via `make dev-sqlite` for full session history:

```python
from google.adk.sessions import DatabaseSessionService

session_service = DatabaseSessionService(
    db_url="sqlite:///./commerce_sessions.db?mode=wal"
)

# Or via CLI:
# adk web --session_service_uri "sqlite:///./sessions.db?mode=wal"
```

**When to use:**

- ✅ Need conversation history across restarts
- ✅ Want SQL query capabilities
- ✅ Production requirements for audit trails

### 4. TypedDict for Type Safety

All tools return structured dicts with TypedDict hints:

```python
from commerce_agent.types import ToolResult

def my_tool(...) -> Dict[str, Any]:  # Use Dict in signature (ADK requirement)
    result: ToolResult = {           # Can use TypedDict for hints
        "status": "success",
        "report": "Operation completed",
        "data": {"key": "value"}
    }
    return result  # ✅ IDE autocomplete + type checking
```

**Benefits:**

- ✅ Full IDE autocomplete
- ✅ Type checking with mypy
- ✅ Clear API contracts
- ✅ ADK compatibility maintained

### 5. Simple Agent Coordination

Clean single-agent design with specialized tools:

```python
root_agent = Agent(
    model="gemini-2.5-flash",
    name="commerce_agent",
    tools=[
        search_products,              # AgentTool (wraps Google Search)
        FunctionTool(func=save_preferences),
        FunctionTool(func=get_preferences),
    ]
)
```

**Why this approach:**

- ✅ Simpler than multi-agent orchestration
- ✅ Easier to test and debug
- ✅ Follows official ADK samples
- ✅ Production-ready without overengineering

## Authentication & Setup

### ⚠️ Critical: Vertex AI vs Gemini API

The agent works with both authentication methods, but with key differences:

| Feature | Vertex AI | Gemini API |
|---------|-----------|------------|
| **Google Search** | ✅ Full support | ⚠️ Limited |
| **site: operator** | ✅ Works | ❌ Doesn't work |
| **Search quality** | ✅ Excellent | ⚠️ Mixed results |
| **Grounding** | ✅ Full metadata | ⚠️ Partial |
| **Production** | ✅ Recommended | ❌ Dev only |

**Problem with Gemini API**: The `site:decathlon.com.hk` search operator
doesn't work, causing the agent to return results from Amazon, eBay, Adidas,
and other non-Decathlon retailers. This breaks the core product discovery flow.

### Setup Option 1: Vertex AI (Recommended)

```bash
# Navigate to tutorial
cd tutorial_implementation/commerce_agent_e2e

# Run interactive setup script
make setup-vertex-ai

# Follow prompts to:
# 1. Verify service account at ./credentials/commerce-agent-key.json
# 2. Unset any conflicting API keys
# 3. Set GOOGLE_CLOUD_PROJECT and GOOGLE_APPLICATION_CREDENTIALS
# 4. Test authentication

# Then install dependencies
make setup
```

The `setup-vertex-ai` script handles:

- ✅ Service account verification
- ✅ Environment variable configuration
- ✅ Credential testing
- ✅ Conflict resolution (removes GOOGLE_API_KEY if set)

### Setup Option 2: Gemini API (Limited)

```bash
# Get API key from https://aistudio.google.com/app/apikey
export GOOGLE_API_KEY=your_key_here

# Install dependencies
cd tutorial_implementation/commerce_agent_e2e
make setup
```

**Known Limitation**: Search will return non-Decathlon results.

### Verifying Authentication

```bash
# Check which credentials are active
echo $GOOGLE_API_KEY
echo $GOOGLE_APPLICATION_CREDENTIALS

# If both are set, Vertex AI takes precedence
# Manually unset API key if needed:
unset GOOGLE_API_KEY

# Restart agent
make dev
```

## Deployment Scenarios

### Local Development

```bash
# Option 1: ADK state (simple, preferences persist across invocations)
make dev

# Option 2: SQLite (full history, survives restarts)
make dev-sqlite

# Access at http://localhost:8000
```

### Production (Cloud Run)

```bash
# Using Vertex AI
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Option 1: ADK state (simple)
adk deploy cloud_run --name commerce-agent

# Option 2: SQLite persistence
adk deploy cloud_run \
  --name commerce-agent \
  --session_service_uri "sqlite:///./sessions.db?mode=wal"
```

### Enterprise Scale (Agent Engine + Cloud Spanner)

```bash
# Deploy to Agent Engine with Cloud Spanner persistence
adk deploy agent_engine \
  --name commerce-agent \
  --session_service_uri "spanner://projects/MY_PROJECT/instances/MY_INSTANCE/databases/commerce"
```

**Benefits of Cloud Spanner:**

- ✅ Multi-region deployment
- ✅ Automatic scaling
- ✅ High availability (99.999% SLA)
- ✅ ACID transactions
- ✅ SQL query capabilities

## Success Criteria

You'll know everything is working when:

✅ All 14+ tests pass (`make test`)  
✅ Agent starts without errors (`make dev`)  
✅ Agent appears in dropdown at [http://localhost:8000](http://localhost:8000)  
✅ Agent calls `get_preferences` at conversation start  
✅ Agent calls `save_preferences` when user provides info  
✅ Agent searches products using Google Search  
✅ Preferences persist across browser refresh  
✅ Grounding metadata appears in server logs (terminal)  
✅ Product recommendations include Decathlon links  
✅ No "site: operator" issues (if using Vertex AI)

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Agent not in dropdown | Run `pip install -e .` in tutorial root |
| Search returns non-Decathlon | Using Gemini API - switch to Vertex AI |
| "site: operator doesn't work" | Run `make setup-vertex-ai` |
| Tests fail with auth error | Set credentials (see Authentication section) |
| Grounding metadata not visible | Check terminal logs (not in UI) |
| Preferences not persisting | Verify `user:` prefix in state keys |
| Both API key and SA set | Unset GOOGLE_API_KEY (Vertex AI takes precedence) |
| Database locked error | Only happens if using SQLite mode, restart dev |

### Detailed Troubleshooting

#### Issue: Search Returns Wrong Retailers

**Symptom**: Agent recommends products from Amazon, eBay, Adidas instead of
Decathlon.

**Cause**: Using Gemini API instead of Vertex AI. The `site:decathlon.com.hk`
operator doesn't work with Gemini API.

**Solution**:

```bash
# 1. Check which auth is active
echo $GOOGLE_API_KEY
echo $GOOGLE_APPLICATION_CREDENTIALS

# 2. If GOOGLE_API_KEY is set, unset it
unset GOOGLE_API_KEY

# 3. Run Vertex AI setup
make setup-vertex-ai

# 4. Restart agent
make dev
```

#### Issue: Grounding Metadata Not Showing

**Expected Behavior**: Grounding metadata appears in **terminal logs**, not in
the web UI.

**Where to look**:

```bash
# Terminal output after search_products call:
====================================================================
✓ GROUNDING METADATA EXTRACTED
====================================================================
Total Sources: 5
  1. [decathlon.com.hk] Brooks Divide 5...
  2. [alltricks.com] Brooks Divide 5...
====================================================================
```

**Note**: To display grounding in UI, you'd need custom frontend integration
(CopilotKit or React components).

#### Issue: Preferences Not Persisting

**Check**:

1. Verify tools use `user:` prefix:

```python
tool_context.state["user:pref_sport"] = sport  # ✅ Correct
tool_context.state["pref_sport"] = sport       # ❌ Wrong (session only)
```

2. Check agent instruction mentions preference workflow
3. Verify user isn't changing User ID between sessions

## What You'll Learn

By completing this implementation, you'll master:

1. **Simple Agent Design**: Clean single-agent with specialized tools
2. **ADK State Management**: User-scoped state for multi-user isolation
3. **Grounding Metadata**: Extracting and monitoring Google Search sources
4. **TypedDict Safety**: Type-safe tool returns with IDE support
5. **Function Tools**: Simple, testable tool implementations
6. **Testing Patterns**: Unit, integration, and e2e test organization
7. **Authentication**: Vertex AI vs Gemini API trade-offs
8. **Production Deployment**: Cloud Run, Agent Engine, and Spanner options

**Key Takeaways**:

- ✅ Start simple (single agent) before going complex (multi-agent)
- ✅ Use ADK state for preferences (unless you need SQL queries)
- ✅ Vertex AI is required for site-restricted search
- ✅ Grounding callback provides transparency and anti-hallucination
- ✅ TypedDict helps but can't be used in tool signatures (ADK limitation)

## Next Steps

After completing this tutorial:

1. **Customize the prompt**: Edit `commerce_agent/prompt.py` for different
   personalities
2. **Add more tools**: Create tools for cart management, order tracking, reviews
3. **Integrate frontend**: Use CopilotKit to build custom UI with grounding
   display
4. **Switch to SQLite**: Try `make dev-sqlite` for persistent conversation
   history
5. **Deploy to production**: Use `adk deploy cloud_run` with Vertex AI
6. **Add analytics**: Track user behavior, popular products, search patterns
7. **Implement ML recommendations**: Use Vertex AI predictions for personalization

## References

### Official Resources

- [ADK Documentation](https://google.github.io/adk-docs/)
- [State Management Guide](https://google.github.io/adk-docs/state/)
- [Google Search Tool](https://google.github.io/adk-docs/tools/google-search/)
- [Session Service](https://google.github.io/adk-docs/sessions/)
- [Testing Guide](https://google.github.io/adk-docs/get-started/testing/)
- [Deployment Options](https://google.github.io/adk-docs/deployment/)

### Implementation Files

- [Source Code](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/commerce_agent_e2e)
- [Agent Definition](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/commerce_agent_e2e/commerce_agent/agent.py)
- [Tools](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/commerce_agent_e2e/commerce_agent/tools/)
- [Callback](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/commerce_agent_e2e/commerce_agent/callbacks.py)
- [Test Suite](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/commerce_agent_e2e/tests)
- [README](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/commerce_agent_e2e/README.md)

### Additional Documentation

- `docs/GROUNDING_CALLBACK_GUIDE.md` - Complete grounding metadata usage
- `docs/SQLITE_SESSION_PERSISTENCE_GUIDE.md` - SQLite persistence deep dive
- `docs/TESTING_WITH_USER_IDENTITIES.md` - Multi-user testing via API
- `TESTING_GUIDE.md` - Testing instructions and debugging

---

<Comments />
