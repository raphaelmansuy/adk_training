# SQLite Session Persistence with Google ADK

**Official Implementation Guide for DatabaseSessionService**

## Overview

ADK provides built-in `DatabaseSessionService` for persistent session storage using SQLite, PostgreSQL, MySQL, or Cloud Spanner. This guide shows how to implement SQLite-based session persistence for production deployments.

## Why DatabaseSessionService?

### vs InMemorySessionService

| Feature          | InMemorySessionService  | DatabaseSessionService (SQLite) |
| ---------------- | ----------------------- | ------------------------------- |
| **Persistence**  | ❌ Lost on restart      | ✅ Survives restarts            |
| **Multi-user**   | ⚠️ Possible but limited | ✅ Recommended                  |
| **Concurrency**  | ❌ Limited              | ✅ Good (WAL mode)              |
| **State Scopes** | ✅ session only         | ✅ All (session/user/app/temp)  |
| **Setup**        | ✅ One line             | ⚠️ Database URL required        |
| **Production**   | ❌ Never                | ✅ Recommended                  |

### vs ADK State (user: prefix)

| Feature         | ADK State (`user:`)     | DatabaseSessionService     |
| --------------- | ----------------------- | -------------------------- |
| **Persistence** | ✅ Cross-session        | ✅ Permanent storage       |
| **Complexity**  | ✅ Simple get/set       | ⚠️ DB schema, connections  |
| **Queries**     | ❌ Key-value only       | ✅ SQL queries, JOINs      |
| **Scalability** | ✅ Good for simple data | ✅ Better for complex data |
| **Use Case**    | ✅ User preferences     | ✅ Full application data   |

**Recommendation**: Use ADK state (`user:` prefix) for simple preferences, DatabaseSessionService for complex applications with multiple users.

## Quick Start (5 Minutes)

### 1. Basic Setup

```python
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from commerce_agent import root_agent

# Create session service with SQLite
session_service = DatabaseSessionService(
    db_url="sqlite:///./commerce_agent_sessions.db"
)

# Initialize runner with session service
runner = Runner(
    agent=root_agent,
    app_name="commerce_agent",
    session_service=session_service
)
```

### 2. Create Session

```python
# Create session for user
session = await session_service.create_session(
    app_name="commerce_agent",
    user_id="athlete_123",
    session_id="session_001",  # Optional: auto-generated if not provided
    state={
        "user:sport": "running",
        "user:budget": 200,
        "user:experience": "advanced"
    }
)

print(f"Created session: {session.id}")
print(f"State: {session.state}")
```

### 3. Run Agent with Persistent Sessions

```python
# Run agent - sessions automatically persist
async for event in runner.run_async(
    user_id="athlete_123",
    session_id="session_001",
    new_message={"role": "user", "parts": [{"text": "I want running shoes"}]}
):
    if event.is_final_response():
        print(event.content)
```

### 4. Verify Persistence

```python
# Restart application, retrieve session
session_restored = await session_service.get_session(
    app_name="commerce_agent",
    user_id="athlete_123",
    session_id="session_001"
)

# Data persists!
assert session_restored.state["user:sport"] == "running"
assert len(session_restored.events) > 0  # Conversation history preserved
```

## DatabaseSessionService API

### Connection Strings

```python
# SQLite (local development, single-server)
db_url = "sqlite:///./sessions.db"

# PostgreSQL (production, multi-server)
db_url = "postgresql://user:password@localhost:5432/adk_sessions"

# MySQL (production)
db_url = "mysql://user:password@localhost:3306/adk_sessions"

# Cloud Spanner (Google Cloud production)
db_url = "spanner:///projects/my-project/instances/my-instance/databases/adk-db"
```

### Core Methods

#### Create Session

```python
session = await session_service.create_session(
    app_name: str,              # Required: Agent app name
    user_id: str,               # Required: User identifier
    session_id: str = None,     # Optional: Auto-generated UUID if not provided
    state: dict = None,         # Optional: Initial state
    **kwargs
) -> Session
```

#### Get Session

```python
session = await session_service.get_session(
    app_name: str,
    user_id: str,
    session_id: str,
    **kwargs
) -> Session | None
```

#### List Sessions

```python
sessions = await session_service.list_sessions(
    app_name: str,
    user_id: str,
    **kwargs
) -> dict[str, Any]  # Returns {"sessions": [...], "total_count": N}
```

#### Delete Session

```python
await session_service.delete_session(
    app_name: str,
    user_id: str,
    session_id: str,
    **kwargs
)
```

#### Append Event (Internal - automatic)

```python
# Called automatically by Runner when agent processes messages
event = await session_service.append_event(
    session: Session,
    event: Event
) -> Event
```

## Session Model Structure

```python
from google.adk.sessions import Session, Event

# Session object
session = Session(
    id="uuid-string",                    # Unique session ID
    app_name="commerce_agent",          # Agent application name
    user_id="athlete_123",              # User identifier
    state={                              # Session state (persisted)
        "user:sport": "running",        # User-scoped (cross-session)
        "session:cart": [...],          # Session-scoped (this conversation)
        "app:config": {...},            # App-scoped (global)
        "temp:cache": {...}             # Temporary (not persisted)
    },
    events=[                             # Conversation history
        Event(id="...", timestamp=..., author="user", ...),
        Event(id="...", timestamp=..., author="agent", ...)
    ],
    last_update_time=1761575199.519     # Unix timestamp
)
```

## State Persistence Flow

### How State Updates Are Saved

```python
# Step 1: User sends message
new_message = {"role": "user", "parts": [{"text": "I want running shoes"}]}

# Step 2: Agent processes and modifies state via tools
def save_preferences(sport: str, tool_context: ToolContext):
    tool_context.state["user:sport"] = sport  # State modification tracked
    return {"status": "success"}

# Step 3: Runner captures state delta
# EventActions.state_delta = {"user:sport": "running"}

# Step 4: Session service merges delta into session.state
await session_service.append_event(session, event)
# → Updates session.state with delta
# → Writes to SQLite database
# → Updates last_update_time

# Step 5: Next invocation reads persisted state
session = await session_service.get_session(...)
# session.state["user:sport"] == "running" ✅
```

### Critical Pattern

```python
# ✅ CORRECT - State persists
def my_tool(value: str, tool_context: ToolContext):
    tool_context.state["key"] = value  # Captured in state_delta → persisted
    return {"status": "success"}

# ❌ WRONG - State doesn't persist
session = await session_service.get_session(...)
session.state["key"] = value  # Direct modification bypasses event system
# Not persisted! Use tool_context.state instead
```

## Production Example: Commerce Agent

### File Structure

```
commerce_agent_e2e/
├── commerce_agent/
│   ├── agent.py           # Agent definition
│   └── tools/
│       └── preferences.py # Tools that modify state
├── runner.py              # Runner setup with DatabaseSessionService
└── sessions.db            # SQLite database (created automatically)
```

### runner.py

```python
import asyncio
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from commerce_agent import root_agent

async def main():
    # Initialize session service
    session_service = DatabaseSessionService(
        db_url="sqlite:///./commerce_agent_sessions.db"
    )

    # Create runner
    runner = Runner(
        agent=root_agent,
        app_name="commerce_agent",
        session_service=session_service
    )

    # Create or get session
    user_id = "athlete_123"
    session = await session_service.create_session(
        app_name="commerce_agent",
        user_id=user_id
    )

    print(f"Session ID: {session.id}")

    # Run agent
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message={
            "role": "user",
            "parts": [{"text": "I want running shoes under €150"}]
        }
    ):
        if event.is_final_response():
            print(f"Agent: {event.content}")

    # Verify persistence
    restored_session = await session_service.get_session(
        app_name="commerce_agent",
        user_id=user_id,
        session_id=session.id
    )

    print(f"State persisted: {restored_session.state}")
    print(f"Events count: {len(restored_session.events)}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Tools with State Persistence

```python
from google.adk.tools import ToolContext
from typing import Dict, Any

def save_preferences(
    sport: str,
    budget_max: int,
    experience_level: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """Save user preferences to persistent state."""
    try:
        # Modify state - automatically persisted via DatabaseSessionService
        tool_context.state["user:sport"] = sport
        tool_context.state["user:budget"] = budget_max
        tool_context.state["user:experience"] = experience_level

        return {
            "status": "success",
            "report": f"✓ Saved: {sport}, max €{budget_max}, {experience_level}"
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

def get_preferences(tool_context: ToolContext) -> Dict[str, Any]:
    """Retrieve saved preferences from persistent state."""
    try:
        state = tool_context.state

        prefs = {
            "sport": state.get("user:sport"),
            "budget_max": state.get("user:budget"),
            "experience_level": state.get("user:experience")
        }

        # Filter None values
        prefs = {k: v for k, v in prefs.items() if v is not None}

        return {
            "status": "success",
            "data": prefs,
            "report": f"Retrieved: {', '.join(f'{k}={v}' for k, v in prefs.items())}"
        }
    except Exception as e:
        return {"status": "error", "error": str(e), "data": {}}
```

## Using with adk web

### Basic Usage

```bash
# Start ADK web with default InMemorySessionService (development)
adk web

# Sessions lost on restart ❌
```

### With DatabaseSessionService (SQLite Persistence)

**✅ OFFICIAL SUPPORT:** `adk web` supports `--session_service_uri` flag for SQLite!

```bash
# SQLite in current directory
adk web --session_service_uri sqlite:///./sessions.db

# SQLite with absolute path
adk web --session_service_uri sqlite:////absolute/path/to/sessions.db

# SQLite with WAL mode (recommended for production)
adk web --session_service_uri "sqlite:///./sessions.db?mode=wal"

# Sessions persist across restarts! ✅
```

**Other Database Options:**

```bash
# PostgreSQL (production recommended)
adk web --session_service_uri postgresql://user:password@localhost/adk_sessions

# MySQL
adk web --session_service_uri mysql://user:password@localhost/adk_sessions

# Cloud Spanner (Google Cloud)
adk web --session_service_uri spanner:///projects/my-project/instances/my-instance/databases/adk-db

# Agent Engine sessions (Google Cloud)
adk web --session_service_uri agentengine://<agent_engine_resource_id>
```

**Complete Example with All Options:**

```bash
adk web \
  --port 8000 \
  --host 0.0.0.0 \
  --session_service_uri "sqlite:///./sessions.db?mode=wal" \
  --artifact_service_uri gs://my-artifacts-bucket \
  --log_level INFO \
  --reload_agents
```

**Reference:** [ADK CLI Documentation](https://google.github.io/adk-docs/api-reference/cli/cli.html#web)

### Advanced: Custom Entry Point Script (For Custom Session Services)

If you need a **custom session service** (Redis, MongoDB, etc.), use this pattern:

```python
# entry_point.py
from google.adk.cli import cli_tools_click
from google.adk.cli.service_registry import get_service_registry
from google.adk.sessions import DatabaseSessionService

# Register DatabaseSessionService as default
def db_session_factory(uri: str = None, **kwargs):
    db_url = uri or "sqlite:///./adk_sessions.db"
    return DatabaseSessionService(db_url=db_url)

registry = get_service_registry()
registry.register_session_service("sqlite", db_session_factory)

if __name__ == '__main__':
    cli_tools_click.main()
```

```bash
# Run with custom entry point
python entry_point.py web --session_service_uri=sqlite:///./sessions.db
```

#### Option 2: Custom Session Service (Advanced)

See `til_implementation/til_custom_session_services_20251023/` for complete implementation.

## Multi-User Support

### User Isolation

```python
# Alice's session
alice_session = await session_service.create_session(
    app_name="commerce_agent",
    user_id="alice@example.com",
    state={"user:sport": "running"}
)

# Bob's session
bob_session = await session_service.create_session(
    app_name="commerce_agent",
    user_id="bob@example.com",
    state={"user:sport": "cycling"}
)

# Complete isolation - Alice and Bob have separate states
alice_prefs = await session_service.get_session(..., user_id="alice@example.com", ...)
bob_prefs = await session_service.get_session(..., user_id="bob@example.com", ...)

assert alice_prefs.state["user:sport"] == "running"
assert bob_prefs.state["user:sport"] == "cycling"
```

### List All Sessions for User

```python
# Get all sessions for Alice
alice_sessions = await session_service.list_sessions(
    app_name="commerce_agent",
    user_id="alice@example.com"
)

print(f"Alice has {alice_sessions['total_count']} sessions")
for session in alice_sessions['sessions']:
    print(f"  - {session.id}: {session.state}")
```

## Database Schema

ADK automatically creates the following tables:

```sql
-- Sessions table (created by DatabaseSessionService)
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,           -- Session UUID
    app_name TEXT NOT NULL,        -- Agent app name
    user_id TEXT NOT NULL,         -- User identifier
    state TEXT NOT NULL,           -- JSON-encoded state dict
    events TEXT NOT NULL,          -- JSON-encoded events list
    last_update_time REAL NOT NULL -- Unix timestamp
);

-- Indexes for efficient queries
CREATE INDEX idx_sessions_user ON sessions(app_name, user_id);
CREATE INDEX idx_sessions_app ON sessions(app_name);
```

## Performance Considerations

### SQLite WAL Mode (Recommended)

```python
# Enable Write-Ahead Logging for better concurrency
db_url = "sqlite:///./sessions.db?mode=wal"

session_service = DatabaseSessionService(db_url=db_url)
```

**Benefits:**

- Multiple readers don't block writers
- Better performance under concurrent load
- Safer for production use

### Connection Pooling (PostgreSQL/MySQL)

```python
# PostgreSQL with connection pool
db_url = "postgresql://user:pass@localhost/adk?pool_size=10&max_overflow=20"

session_service = DatabaseSessionService(db_url=db_url)
```

## Troubleshooting

### Issue: "Session not found"

```python
# ❌ WRONG - Session never created
runner.run_async(user_id="user123", session_id="session456", ...)
# Error: Session not found

# ✅ CORRECT - Create session first
session = await session_service.create_session(
    app_name="commerce_agent",
    user_id="user123"
)
runner.run_async(user_id="user123", session_id=session.id, ...)
```

### Issue: "State not persisting"

```python
# ❌ WRONG - Direct session modification
session = await session_service.get_session(...)
session.state["key"] = "value"  # Not persisted!

# ✅ CORRECT - Modify via tool_context
def my_tool(value: str, tool_context: ToolContext):
    tool_context.state["key"] = value  # Persisted via state_delta
    return {"status": "success"}
```

### Issue: "Database locked" (SQLite)

```python
# Solution 1: Use WAL mode
db_url = "sqlite:///./sessions.db?mode=wal"

# Solution 2: Increase timeout
db_url = "sqlite:///./sessions.db?timeout=30.0"

# Solution 3: Use PostgreSQL for high concurrency
db_url = "postgresql://user:pass@localhost/adk"
```

## Migration from InMemorySessionService

```python
# Before: In-memory sessions (lost on restart)
from google.adk.sessions import InMemorySessionService

session_service = InMemorySessionService()

# After: Persistent sessions with SQLite
from google.adk.sessions import DatabaseSessionService

session_service = DatabaseSessionService(
    db_url="sqlite:///./sessions.db?mode=wal"
)

# No other code changes required! ✅
```

## Best Practices

1. **Use WAL Mode** for SQLite in production
2. **User Isolation** - Always use unique user_ids
3. **State Scopes** - Use proper prefixes (user:, session:, app:, temp:)
4. **Error Handling** - Always wrap session operations in try/except
5. **Cleanup** - Periodically delete old sessions to save disk space
6. **Backup** - Regular backups of SQLite database file
7. **Testing** - Use separate test database (`:memory:` or temp file)

## References

- **ADK Documentation**: https://google.github.io/adk-docs/sessions/
- **TIL: Custom Session Services**: `docs/til/til_custom_session_services_20251023.md`
- **Working Example**: `til_implementation/til_custom_session_services_20251023/`
- **Tutorial 35**: Commerce Agent E2E with DatabaseSessionService
- **Official Samples**: `research/adk-samples/python/agents/`

## Next Steps

1. **Implement in your agent** - Replace InMemorySessionService
2. **Test persistence** - Restart app and verify state survives
3. **Monitor performance** - Check database size and query times
4. **Consider PostgreSQL** - For multi-server production deployments
5. **Implement cleanup** - Delete old sessions periodically

---

**Created**: 2025-01-27  
**ADK Version**: 1.17+  
**Status**: Production-ready
