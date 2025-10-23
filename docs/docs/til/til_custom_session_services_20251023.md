---
id: til_custom_session_services_20251023
title: "TIL: Registering Custom Session Services in Google ADK 1.17"
description: "Extend ADK with custom session storage (Redis, MongoDB, etc)"
sidebar_label: "TIL: Custom Session Services (Oct 23)"
sidebar_position: 4
tags:
  [
    "til",
    "quick-learn",
    "session-services",
    "service-registry",
    "adk-1.17",
    "extensibility",
    "storage-backends",
  ]
keywords:
  [
    "adk",
    "session service",
    "service registry",
    "redis",
    "mongodb",
    "custom storage",
    "backend integration",
  ]
status: "completed"
difficulty: "intermediate"
estimated_time: "8 minutes"
publication_date: "2025-10-23"
adk_version_minimum: "1.17"
implementation_link: "https://github.com/raphaelmansuy/adk_training/tree/main/til_implementation/til_custom_session_services_20251023"
---

import Comments from '@site/src/components/Comments';

## TIL: Custom Session Services - Extend ADK with Your Own Storage Backend

### Why Custom Session Services Matter

**The Problem**: By default, ADK stores sessions in memory. For
production, you need:

- Persistent storage (survive server restarts)
- Distributed storage (multi-server deployments)
- Custom backends (your specific infrastructure)

**In one sentence**: Custom Session Services let you register any
storage backend (Redis, MongoDB, PostgreSQL) with ADK's service
registry so `adk web` and agents can use them seamlessly.

### Why Should You Care?

**Problems it solves:**

- 💾 **Persistent Sessions** - Survive server restarts
- 📊 **Distributed Systems** - Share across multiple servers
- 🏢 **Enterprise Integration** - Use your existing storage
- 🔧 **Custom Backends** - Redis, MongoDB, PostgreSQL, DynamoDB
- 🎛️ **CLI Support** - Works with `adk web` via URI schemes
- ⚡ **Zero Code Changes** - Register once, use everywhere

**Perfect for:**

- Production deployments with persistent requirements
- Teams using specific databases (MongoDB shops, Redis caches)
- Multi-server agent deployments
- Custom storage with special features (encryption, sharding)
- Cloud infrastructure (Google Cloud Storage, AWS DynamoDB)

### Quick Example

```python
from google.adk.cli import cli_tools_click
from google.adk.cli.service_registry import get_service_registry
from google.adk.sessions import BaseSessionService, Session

class RedisSessionService(BaseSessionService):
    """Store sessions in Redis with 24-hour auto-expiration."""
    
    def __init__(self, uri: str = "redis://localhost:6379", **kwargs):
        self.redis_uri = uri
        self.redis_client = redis.from_url(uri, decode_responses=True)
    
    async def create_session(self, *, app_name: str, user_id: str, **kwargs):
        """Create and store session in Redis."""
        session_id = str(uuid.uuid4())
        session = Session(id=session_id, app_name=app_name, user_id=user_id)
        # Store to Redis with 24h TTL
        self.redis_client.set(f"session:{app_name}:{user_id}:{session_id}",
                            json.dumps(session.dict()), ex=86400)
        return session
    
    async def get_session(self, *, app_name: str, user_id: str,
                        session_id: str, **kwargs):
        """Retrieve session from Redis."""
        data = self.redis_client.get(f"session:{app_name}:{user_id}:{session_id}")
        return Session(**json.loads(data)) if data else None
    
    async def append_event(self, session: Session, event):
        """Critical: Save events to Redis when session updates."""
        event = await super().append_event(session=session, event=event)
        # Save updated session with all events to Redis
        key = f"session:{session.app_name}:{session.user_id}:{session.id}"
        self.redis_client.set(key, json.dumps(session.dict()), ex=86400)
        return event

# Register with service registry
def redis_factory(uri: str, **kwargs):
    kwargs_copy = kwargs.copy()
    kwargs_copy.pop("agents_dir", None)
    return RedisSessionService(uri=uri, **kwargs_copy)

registry = get_service_registry()
registry.register_session_service("redis", redis_factory)

if __name__ == '__main__':
    cli_tools_click.main()
```

**Then run:**

```bash
# Redis sessions from CLI
python app.py web agents/ --session_service_uri=redis://localhost:6379

# Sessions automatically persist to Redis!
```

### How It Works (3 Key Concepts)

#### 1. Service Registry Pattern

ADK has a **global service registry** that maps URI schemes to
factories. Here's the flow:

```text
Scheme Registration:

┌─────────────────────────────────────────────────────────┐
│  Service Registry (get_service_registry())              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  "redis"  → redis_factory()                             │
│            Creates RedisSessionService instances        │
│            Loads sessions from Redis                    │
│                                                         │
└─────────────────────────────────────────────────────────┘

When you run: adk web --session_service_uri=redis://localhost:6379

↓
Parse URI scheme: "redis"
↓
Look up factory: registry.get_session_service_factory("redis")
↓
Call factory: redis_factory(uri="redis://localhost:6379")
↓
Return: RedisSessionService instance ready to use
```

#### 2. Factory Function Pattern

Your factory receives the **URI string** and returns a **session
service instance**:

```python
def redis_factory(uri: str, **kwargs):
    """
    Factory receives the full URI from CLI.

    Args:
        uri: Full URI string (e.g., "redis://localhost:6379")
        **kwargs: Additional options from ADK

    Returns:
        RedisSessionService instance ready to use
    """
    kwargs_copy = kwargs.copy()
    kwargs_copy.pop("agents_dir", None)  # Remove non-service kwarg
    return RedisSessionService(uri=uri, **kwargs_copy)
```

#### 3. Inherit from BaseSessionService

Your custom service must inherit from `BaseSessionService`:

```python
from google.adk.sessions import BaseSessionService, Session, Event
import redis
import json
import uuid

class RedisSessionService(BaseSessionService):
    """Store ADK sessions in Redis."""

    def __init__(self, uri: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(uri, decode_responses=True)

    async def create_session(self, *, app_name: str, user_id: str,
                           **kwargs):
        """Create and store session in Redis."""
        session_id = str(uuid.uuid4())
        session = Session(id=session_id, app_name=app_name,
                        user_id=user_id)
        # Store to Redis with 24-hour expiration
        self.redis_client.set(f"session:{session_id}",
                            json.dumps(session.dict()),
                            ex=86400)
        return session

    async def get_session(self, *, app_name: str, user_id: str,
                        session_id: str, **kwargs):
        """Retrieve session from Redis."""
        data = self.redis_client.get(f"session:{session_id}")
        if not data:
            return None
        return Session(**json.loads(data))

    async def list_sessions(self, *, app_name: str, user_id: str,
                          **kwargs):
        """List all sessions for a user."""
        pattern = f"session:*"
        sessions = []
        for key in self.redis_client.keys(pattern):
            data = self.redis_client.get(key)
            if data:
                session_dict = json.loads(data)
                if (session_dict.get("app_name") == app_name and
                    session_dict.get("user_id") == user_id):
                    sessions.append(Session(**session_dict))
        return {"sessions": sessions, "total_count": len(sessions)}

    async def delete_session(self, *, app_name: str, user_id: str,
                           session_id: str, **kwargs):
        """Delete session from Redis."""
        self.redis_client.delete(f"session:{session_id}")

    async def append_event(self, session: Session, event):
        """Critical: Save events and full session to Redis."""
        # Call parent to add event to session.events
        event = await super().append_event(session=session, event=event)
        # IMPORTANT: Save entire session to Redis after event added
        self.redis_client.set(f"session:{session.id}",
                            json.dumps(session.dict()),
                            ex=86400)
        return event
```

### Use Case: Redis Session Service

**Scenario**: You're running agents in production and want fast,
persistent sessions with automatic expiration.

```python
# main.py
from google.adk.cli import cli_tools_click
from google.adk.cli.service_registry import get_service_registry
import redis
import json
import uuid
from google.adk.sessions import BaseSessionService, Session

class RedisSessionService(BaseSessionService):
    """Store ADK sessions in Redis."""

    def __init__(self, uri: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(uri, decode_responses=True)

    async def create_session(self, *, app_name: str, user_id: str,
                           **kwargs):
        session_id = str(uuid.uuid4())
        session = Session(id=session_id, app_name=app_name,
                        user_id=user_id)
        self.redis_client.set(f"session:{session_id}",
                            json.dumps(session.dict()), ex=86400)
        return session

    async def append_event(self, session: Session, event):
        event = await super().append_event(session=session, event=event)
        self.redis_client.set(f"session:{session.id}",
                            json.dumps(session.dict()), ex=86400)
        return event

    async def get_session(self, *, app_name: str, user_id: str,
                        session_id: str, **kwargs):
        data = self.redis_client.get(f"session:{session_id}")
        if not data:
            return None
        return Session(**json.loads(data))

    async def list_sessions(self, *, app_name: str, user_id: str,
                          **kwargs):
        sessions = []
        for key in self.redis_client.keys("session:*"):
            data = self.redis_client.get(key)
            if data:
                s = Session(**json.loads(data))
                if s.app_name == app_name and s.user_id == user_id:
                    sessions.append(s)
        return {"sessions": sessions, "total_count": len(sessions)}

    async def delete_session(self, *, app_name: str, user_id: str,
                           session_id: str, **kwargs):
        self.redis_client.delete(f"session:{session_id}")

# Register the service
def redis_factory(uri: str, **kwargs):
    kwargs_copy = kwargs.copy()
    kwargs_copy.pop("agents_dir", None)
    return RedisSessionService(uri=uri, **kwargs_copy)

registry = get_service_registry()
registry.register_session_service("redis", redis_factory)

if __name__ == '__main__':
    cli_tools_click.main()
```

**Run with:**

```bash
# Default Redis (localhost:6379)
python main.py web agents/

# Custom Redis location
python main.py web agents/ \
  --session_service_uri=redis://redis.prod.example.com:6379

# Result: All sessions persist to Redis with auto-expiration ✅
```

**What happens:**

1. Sessions are created on first interaction
2. Each event (user message, agent response) triggers `append_event()`
3. Full session state is saved to Redis (24-hour TTL)
4. Sessions survive page refreshes, server restarts
5. After 24 hours, sessions auto-expire from Redis

```bash
# Use Redis for fast agents
adk web agents/ --session_service_uri=redis://localhost:6379

# Use PostgreSQL for critical agents
adk web agents/   --session_service_uri=postgres://user:pass@localhost/adk_db
```

## Configuration Reference

```python
registry.register_session_service(
    scheme: str,                    # URI scheme ("redis", "mongodb", etc.)
    factory: Callable[..., Any]     # Factory function
)
```

| Parameter | Type | Purpose |
|-----------|------|---------|
| `scheme` | str | URI scheme identifier (e.g., "redis") |
| `factory` | Callable | Function that takes `(uri: str, **kwargs)` |
| `uri` | str | Full URI (e.g., "redis://localhost:6379") |
| `**kwargs` | dict | Additional options (remove `agents_dir`) |

### Pro Tips

💡 **Tip 1 - Always handle agents_dir**: The CLI passes `agents_dir` to your
factory, but your session service doesn't need it. Always pop it from kwargs:

```python
def my_factory(uri: str, **kwargs):
    kwargs_copy = kwargs.copy()
    kwargs_copy.pop("agents_dir", None)  # ← Do this!
    return MySessionService(**kwargs_copy)
```

💡 **Tip 2 - URI parsing**: Create a helper to parse custom URI schemes:

```python
from urllib.parse import urlparse

def custom_factory(uri: str, **kwargs):
    parsed = urlparse(uri)
    # parsed.scheme = "myservice"
    # parsed.netloc = "localhost:9999"
    # parsed.path = "/path"

    kwargs_copy = kwargs.copy()
    kwargs_copy.pop("agents_dir", None)
    return CustomService(
        host=parsed.hostname,
        port=parsed.port,
        **kwargs_copy
    )
```

💡 **Tip 3 - Test in adk web**: After registering, launch `adk web` and check
the UI. Sessions should persist across browser page reloads:

```bash
# Start your script with registration
python my_setup.py web agents/

# In browser: http://localhost:8000
# Send messages to agent → refresh page → sessions persist ✅
```

💡 **Tip 4 - Async-first**: Always make `write()`, `read()`, `delete()` async.
ADK expects async I/O:

```python
class MySessionService(BaseSessionStorage):
    async def write(self, session_id: str, data: dict) -> None:
        # Async operations: await db.save(), etc.
        pass
```

### When NOT to Use It

⚠️ **Avoid when**:

- Simple development (use default in-memory sessions)
- No persistence needed (throwaway chatbots)
- Single-server, single-process deployment

⚠️ **Consider alternatives**:

- **Default Sessions**: Fine for local dev and demos
- **Database Session Service**: If you need simple SQL backend
- **Cache + Database Hybrid**: Redis for speed, PostgreSQL for backup

### Complete Working Implementation

This TIL includes a production-ready Redis session service that you
can use directly:

**Start the example:**

```bash
cd til_implementation/til_custom_session_services_20251023/

make setup       # Install dependencies + Docker
make docker-up   # Start Redis container
make dev         # Launch web UI with custom sessions
```

**Key files in the implementation:**

- `custom_session_agent/agent.py` - RedisSessionService with all 5
  methods
- `custom_session_agent/__main__.py` - Entry point that registers
  service
- `tests/` - Full test suite for factory and service methods
- `view_sessions.py` - Utility to inspect Redis session data
- `Makefile` - Simplified commands (setup, docker-up, dev, test)

**Run the tests:**

```bash
cd til_implementation/til_custom_session_services_20251023/
pytest tests/ -v

# Expected output:
# test_agent.py::test_agent_config_valid PASSED
# test_imports.py::test_required_env_vars PASSED
# test_tools.py::test_show_service_registry_info PASSED
# ...
# 26 passed ✅
```

### How Persistence Works in Practice

**Session Lifecycle with Redis:**

```text
1. User sends message to agent
   ↓
2. ADK creates/loads session
   ↓
3. Session service loads session data
   RedisSessionService.get_session() loads from Redis
   ↓
4. Agent processes message with session context
   ↓
5. Response generated + event created
   ↓
6. Session saved to Redis
   RedisSessionService.append_event() saves full session
   (This is the CRITICAL method!)
   ↓
7. User refreshes browser
   ↓
8. New request for same session_id
   ↓
9. Session service loads session
   RedisSessionService.get_session() → retrieves from Redis
   Data persists! ✅
   ↓
10. Agent has full context (conversation history, state) ✅
```

**Verification Steps:**

1. Start your agent with Redis sessions:

   ```bash
   make setup
   make docker-up
   make dev
   ```

2. Open browser to `localhost:8000`

3. Send message to agent ("What's your name?")

4. Check Redis directly:

   ```bash
   # View all sessions stored in Redis
   cd til_implementation/til_custom_session_services_20251023/
   python view_sessions.py
   ```

5. You should see session with conversation history ✅

6. Refresh browser - agent remembers conversation ✅

### Next Steps After Learning

1. 📖 **Copy the pattern**: Use `custom_session_agent/agent.py`
   as a template for your own service
2. 🚀 **Adapt to your backend**: Replace Redis client with your
   storage system
3. 💬 **Register service**: Use the factory pattern in your CLI
4. 🔄 **Deploy**: Use in production with `adk web
   --session_service_uri=your_uri`

## Key Takeaway

**Custom Session Services unlock production-grade ADK deployments.**

Register a custom backend once, use it everywhere. Whether you prefer Redis for
speed, MongoDB for documents, PostgreSQL for SQL, or your own custom storage,
ADK's service registry makes integration seamless.

The pattern is powerful: one factory function and one registration call, and
your entire ADK ecosystem (CLI, web UI, agents) uses your backend
automatically. ✨

---

## See Also

### Related TILs

- **[TIL: Context Compaction](/docs/til/til_context_compaction_20250119)** - Optimize
  memory usage in long conversations (works well with persistent sessions!)
- **[TIL: Pause and Resume Invocations](/docs/til/til_pause_resume_20251020)** -
  Checkpoint agent execution state
- **[Back to TIL Index](/docs/til/til_index)** - Browse all quick-learn guides

### Related ADK Tutorials

- **[Tutorial 01: Hello World Agent](/docs/hello_world_agent)** - Start here if
  new to ADK; custom sessions apply to all agents
- **[Tutorial 08: State & Memory](/docs/state_memory)** - Understand session
  state management and persistence patterns
- **[Tutorial 15: Building Multi-Server Systems](/docs/distributed_agents)** -
  Use custom persistent sessions for distributed deployments

### ADK Official Documentation

- **BaseSessionService API** - Complete API reference and abstract
  methods (see google.adk.sessions module)
- **Service Registry** - Service registry implementation in
  google.adk.cli.service_registry
- **ADK Community Sessions** - Working Redis implementation in
  adk-python-community

### Related Resources & Patterns

- **Production Agent Patterns** - Session persistence is critical for
  production agents
- **Custom Session Services Implementation** - Working code example
  with full test suite (see til_implementation directory)

## Questions?

- 💬 Comment below if you have questions
- 🐛 Found an issue? Check the implementation tests
- 🚀 Ready to go deeper? See Tutorial 08

<Comments />
```
```
