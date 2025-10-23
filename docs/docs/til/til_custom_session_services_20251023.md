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

**The Problem**: By default, ADK stores sessions in memory. For production agents, you need:

- Persistent storage (survive server restarts)
- Distributed storage (multi-server deployments)
- Custom backends (your specific infrastructure)

**In one sentence**: Custom Session Services let you register any storage backend (Redis, MongoDB, PostgreSQL, DynamoDB) with ADK's service registry so `adk web` and your agents can use them seamlessly.

### Why Should You Care?

**Problems it solves:**

- 💾 **Persistent Sessions** - Sessions survive server restarts
- 📊 **Distributed Systems** - Share sessions across multiple servers
- 🏢 **Enterprise Integration** - Use your existing storage infrastructure
- 🔧 **Custom Backends** - MongoDB, Redis, PostgreSQL, DynamoDB, or anything
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
from google.adk_community.sessions import redis_session_service

# Step 1: Create a factory function
def redis_service_factory(uri: str, **kwargs):
    """Factory for creating a RedisSessionService."""
    kwargs_copy = kwargs.copy()
    kwargs_copy.pop("agents_dir", None)
    return redis_session_service.RedisSessionService(**kwargs_copy)

# Step 2: Register with service registry
registry = get_service_registry()
registry.register_session_service("redis", redis_service_factory)

# Step 3: Use via CLI
if __name__ == '__main__':
    cli_tools_click.main()
```

**Then run:**

```bash
# Redis sessions from CLI
adk web agents/ --session_service_uri=redis://localhost:6379/0

# Or MongoDB (if you implement it)
adk web agents/ --session_service_uri=mongodb://localhost:27017/adk_sessions
```

### How It Works (3 Key Concepts)

#### 1. Service Registry Pattern

ADK has a **global service registry** that maps URI schemes to factories:

```
URI Scheme Registration:

┌─────────────────────────────────────────────────────────┐
│  Service Registry (get_service_registry())              │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  "redis"     → redis_service_factory()                  │
│               Creates RedisSessionService instances     │
│                                                          │
│  "mongodb"   → mongodb_service_factory()                │
│               Creates MongoDBSessionService instances   │
│                                                          │
│  "postgres"  → postgres_service_factory()               │
│               Creates PostgresSessionService instances  │
│                                                          │
│  [custom]    → your_factory()                           │
│               Creates YourCustomService instances       │
│                                                          │
└─────────────────────────────────────────────────────────┘

When you run: adk web --session_service_uri=redis://localhost:6379

↓
Parse URI scheme: "redis"
↓
Look up factory: registry.get_session_service_factory("redis")
↓
Call factory: redis_service_factory(uri="redis://localhost:6379")
↓
Return: RedisSessionService instance ready to use
```

#### 2. Factory Function Pattern

Your factory receives the **URI string** and returns a **session service instance**:

```python
def custom_session_factory(uri: str, **kwargs):
    """
    Factory receives the full URI from CLI.

    Args:
        uri: Full URI string (e.g., "redis://localhost:6379/0")
        **kwargs: Additional options from ADK

    Returns:
        Instance of your custom session service
    """
    # Parse URI if needed
    parsed = parse_uri(uri)  # extract host, port, db, etc.

    # Create and return service instance
    return CustomSessionService(
        host=parsed.host,
        port=parsed.port,
        **kwargs
    )
```

**Why kwargs handling matters:**

```python
# Always remove agents_dir from kwargs
# It's passed by ADK but your service doesn't need it
def redis_factory(uri: str, **kwargs):
    kwargs_copy = kwargs.copy()
    kwargs_copy.pop("agents_dir", None)  # ← Important!
    return RedisSessionService(**kwargs_copy)
```

#### 3. Inheritance from BaseSessionStorage

Your custom service must inherit from `BaseSessionStorage`:

```python
from google.adk.sessions import BaseSessionStorage

class CustomSessionService(BaseSessionStorage):
    """Your custom session storage backend."""

    async def write(self, session_id: str, data: dict) -> None:
        """Write session data to storage."""
        # Your implementation: save to Redis, MongoDB, etc.
        pass

    async def read(self, session_id: str) -> dict:
        """Read session data from storage."""
        # Your implementation: retrieve from your backend
        pass

    async def delete(self, session_id: str) -> None:
        """Delete session data."""
        # Your implementation: remove from your backend
        pass
```

### Use Case 1: Redis Session Service

**Scenario**: You're running agents in production and want fast, persistent sessions.

```python
# redis_setup.py
from google.adk.cli import cli_tools_click
from google.adk.cli.service_registry import get_service_registry
from google.adk_community.sessions import redis_session_service

def redis_factory(uri: str, **kwargs):
    kwargs_copy = kwargs.copy()
    kwargs_copy.pop("agents_dir", None)
    return redis_session_service.RedisSessionService(**kwargs_copy)

registry = get_service_registry()
registry.register_session_service("redis", redis_factory)

if __name__ == '__main__':
    cli_tools_click.main()
```

**Run with:**

```bash
# Default Redis (localhost:6379, db=0)
python redis_setup.py web agents/

# Custom Redis location
python redis_setup.py web agents/ \
  --session_service_uri=redis://redis.prod.example.com:6379/1

# Result: All sessions persist to Redis ✅
```

### Use Case 2: Custom MongoDB Service

**Scenario**: Your team uses MongoDB, and you want session documents stored there.

```python
from google.adk.sessions import BaseSessionStorage
from pymongo import MongoClient
import json

class MongoDBSessionService(BaseSessionStorage):
    """Store ADK sessions in MongoDB."""

    def __init__(self, connection_string: str, **kwargs):
        self.client = MongoClient(connection_string)
        self.db = self.client['adk_sessions']
        self.collection = self.db['sessions']

    async def write(self, session_id: str, data: dict) -> None:
        """Write session to MongoDB."""
        self.collection.update_one(
            {"_id": session_id},
            {"$set": {"data": data}},
            upsert=True
        )

    async def read(self, session_id: str) -> dict:
        """Read session from MongoDB."""
        doc = self.collection.find_one({"_id": session_id})
        return doc["data"] if doc else {}

    async def delete(self, session_id: str) -> None:
        """Delete session from MongoDB."""
        self.collection.delete_one({"_id": session_id})

# Register it
def mongodb_factory(uri: str, **kwargs):
    kwargs_copy = kwargs.copy()
    kwargs_copy.pop("agents_dir", None)
    return MongoDBSessionService(
        connection_string=uri.replace("mongodb://", "mongodb://"),
        **kwargs_copy
    )

registry = get_service_registry()
registry.register_session_service("mongodb", mongodb_factory)
```

**Run with:**

```bash
adk web agents/ --session_service_uri=mongodb://localhost:27017/mydb
```

### Use Case 3: Multi-Backend Setup

**Scenario**: Different agents use different backends (Redis for cache,
PostgreSQL for critical data).

```python
from google.adk.cli import cli_tools_click
from google.adk.cli.service_registry import get_service_registry
from google.adk_community.sessions import redis_session_service
from my_custom import postgres_session_service

registry = get_service_registry()

# Register Redis
def redis_factory(uri: str, **kwargs):
    kwargs_copy = kwargs.copy()
    kwargs_copy.pop("agents_dir", None)
    return redis_session_service.RedisSessionService(**kwargs_copy)

registry.register_session_service("redis", redis_factory)

# Register PostgreSQL
def postgres_factory(uri: str, **kwargs):
    kwargs_copy = kwargs.copy()
    kwargs_copy.pop("agents_dir", None)
    return postgres_session_service.PostgresSessionService(**kwargs_copy)

registry.register_session_service("postgres", postgres_factory)

if __name__ == '__main__':
    cli_tools_click.main()
```

**Choose at runtime:**

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
| `scheme` | str | URI scheme identifier (e.g., "redis", "mongodb") |
| `factory` | Callable | Function that takes `(uri: str, **kwargs)` and returns service |
| `uri` | str | Full URI passed to factory (e.g., "redis://localhost:6379") |
| `**kwargs` | dict | Additional options (remove `agents_dir` before using) |

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

The full implementation includes:

- Full Redis session service example (or MongoDB alternative)
- Registration in ADK CLI
- Comprehensive tests for factory pattern
- Test suite for session operations
- Multiple backends demonstrated
- Environment configuration

```bash
cd til_implementation/til_custom_session_services_20251023/

make setup       # Install dependencies
make test        # Run all tests (validates registration)
make dev         # Launch web UI with custom sessions
```

**Test the implementation:**

```bash
# Run from implementation directory
pytest tests/ -v

# Expected output:
# test_registration.py::test_factory_registration PASSED
# test_registration.py::test_uri_parsing PASSED
# test_redis_service.py::test_session_write PASSED
# test_redis_service.py::test_session_read PASSED
# test_redis_service.py::test_session_delete PASSED
```

### How Persistence Works in Practice

**Session Lifecycle with Custom Backend:**

```
1. User sends message to agent
   ↓
2. ADK creates/loads session
   ↓
3. Session service loads old data
   myService.read(session_id) → fetches from Redis/MongoDB
   ↓
4. Agent processes message with session context
   ↓
5. Response generated
   ↓
6. Session updated and saved
   myService.write(session_id, updated_data) → Redis/MongoDB
   ↓
7. User refreshes browser
   ↓
8. New request for same session_id
   ↓
9. Session service loads saved data
   myService.read(session_id) → data persists! ✅
   ↓
10. Agent has full context from previous interaction ✅
```

**Verification Steps:**

1. Start your agent with custom sessions:
   ```bash
   python my_setup.py web agents/ --session_service_uri=redis://localhost:6379
   ```

2. Open browser to localhost:8000

3. Send message to agent ("What's your name?")

4. Check backend (Redis/MongoDB directly):
   ```bash
   # Redis
   redis-cli GET session:xyz123

   # MongoDB
   db.sessions.find({"_id": "xyz123"})
   ```

5. You should see session data persisted ✅

6. Refresh browser - agent remembers conversation ✅

### Next Steps After Learning

1. 📖 **Check adk-python-community**: See working Redis implementation
2. 🚀 **Implement your backend**: Adapt example to your storage system
3. 💬 **Register and test**: Use the pattern in your main CLI
4. 🔄 **Deploy**: Use in production `adk web` and agents

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

- **[TIL: Context Compaction](til_context_compaction_20250119)** - Optimize
  memory usage in long conversations (works well with persistent sessions!)
- **[TIL: Pause and Resume Invocations](til_pause_resume_20251020)** -
  Checkpoint agent execution state
- **[Back to TIL Index](til_index)** - Browse all quick-learn guides

### Related ADK Tutorials

- **[Tutorial 01: Hello World Agent](/docs/hello_world_agent)** - Start here if
  new to ADK; custom sessions apply to all agents
- **[Tutorial 08: State & Memory](/docs/state_memory)** - Understand session
  state management and persistence patterns
- **[Tutorial 15: Building Multi-Server Systems](/docs/distributed_agents)** -
  Use custom persistent sessions for distributed deployments

### ADK Official Documentation

- **[BaseSessionStorage API](https://github.com/google/adk-python/tree/main/google/adk/sessions)** -
  Complete API reference and abstract methods
- **[Service Registry](https://github.com/google/adk-python/blob/main/google/adk/cli/service_registry.py)** -
  Service registry implementation
- **[ADK Community Sessions](https://github.com/google/adk-python-community/tree/main/src/google/adk_community/sessions)** -
  Working Redis implementation

### Related Resources & Patterns

- **[Production Agent Patterns](/blog/production-agent-checklist)** - Session
  persistence is critical for production agents
- **[Custom Session Services Implementation](https://github.com/raphaelmansuy/adk_training/tree/main/til_implementation/til_custom_session_services_20251023)** -
  Working code example with full test suite

## Questions?

- 💬 Comment below if you have questions
- 🐛 Found an issue? Check the implementation tests
- 🚀 Ready to go deeper? See Tutorial 08

<Comments />
```
