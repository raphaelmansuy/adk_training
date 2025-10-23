# Custom Session Services - TIL Implementation

This is the working implementation for the TIL: **"Registering Custom Session Services in Google ADK 1.17+"**

## Overview

This project demonstrates how to register and use custom session storage backends (Redis, MongoDB, PostgreSQL, DynamoDB) with Google ADK's service registry pattern.

## ⚠️ CRITICAL: Entry Point Pattern

**Service registration MUST happen BEFORE ADK initializes!**

### Why This Matters
- If services register during agent module import → Too late ❌
- ADK has already decided on the session backend by then
- Custom services won't be used

### Correct Pattern (What We Do Here)
1. Create `__main__.py` entry point
2. Register services FIRST
3. Then call `cli_tools_click.main()`
4. Now ADK sees your registered services ✅

### Usage
```bash
# Correct - uses entry point pattern
python -m custom_session_agent web --session_service_uri=redis://localhost:6379
make dev  # Also uses entry point (calls the above)

# Wrong - bypasses entry point, won't use custom services
adk web
```

## Quick Start

### 1. Setup Environment

```bash
# Install dependencies
make setup

# Copy environment variables
cp .env.example .env
```

### 2. Start Services

```bash
# Start Redis and MongoDB containers
make docker-up

# Verify services are running
docker ps
```

### 3. Run the Agent

```bash
# Start ADK web interface with Redis sessions
make dev

# Open browser: http://localhost:8000
```

### 4. Test Session Persistence

1. Send a message to the agent
2. Refresh the browser page (F5)
3. Your session data persists in Redis! ✅

## Project Structure

```
.
├── Makefile                          # Commands for setup, dev, testing
├── docker-compose.yml                # Redis and MongoDB containers
├── requirements.txt                  # Python dependencies
├── .env.example                      # Environment variables template
├── custom_session_agent/
│   ├── __init__.py                   # Package initialization
│   └── agent.py                      # Main agent + service registration
└── tests/
    ├── __init__.py
    ├── test_imports.py               # Import and configuration tests
    ├── test_tools.py                 # Tool function tests
    └── test_agent.py                 # Agent configuration tests
```

## Architecture

### Service Registry Pattern

ADK uses a **global service registry** that maps URI schemes to factory functions:

```
┌─────────────────────────────────────────────┐
│        Service Registry                     │
├─────────────────────────────────────────────┤
│                                             │
│  "redis"   → redis_service_factory()        │
│  "mongodb" → mongodb_service_factory()      │
│  "memory"  → memory_service_factory()       │
│  "custom"  → your_custom_factory()          │
│                                             │
└─────────────────────────────────────────────┘
        ↓
    When you run:
    adk web --session_service_uri=redis://localhost
        ↓
    Registry looks up "redis" scheme
        ↓
    Calls factory with the URI
        ↓
    Returns configured service instance
```

### Factory Function Pattern

```python
def redis_service_factory(uri: str, **kwargs):
    """Factory creates service instances from URI."""
    kwargs_copy = kwargs.copy()
    kwargs_copy.pop("agents_dir", None)  # ADK passes this, but we don't need it
    
    return redis_session_service.RedisSessionService(
        uri=uri,
        **kwargs_copy
    )

# Register with service registry
registry = get_service_registry()
registry.register_session_service("redis", redis_service_factory)
```

## Available Session Backends

### Redis

**Perfect for:** Production agents, high-frequency sessions, caching

```bash
# Start Redis
make docker-up

# Use with ADK
python custom_session_agent/agent.py web custom_session_agent/ \
  --session_service_uri=redis://localhost:6379/0

# Verify in Redis CLI
docker-compose exec redis redis-cli
> KEYS *
> GET <session_key>
```

**Characteristics:**
- ⚡ Very fast (in-memory)
- 💾 Persistent (RDB snapshots)
- 📊 Distributed (can share across servers)
- 🔄 Well-supported by community

### MongoDB

**Perfect for:** Document-heavy sessions, complex data, MongoDB shops

```bash
# Start MongoDB (included in docker-compose.yml)
make docker-up

# Use with ADK
python custom_session_agent/agent.py web custom_session_agent/ \
  --session_service_uri=mongodb://localhost:27017/adk_sessions

# Verify in MongoDB shell
docker-compose exec mongodb mongosh
> use adk_sessions
> db.sessions.find()
```

**Characteristics:**
- 📄 Flexible document storage
- 🔍 Complex queries
- 📏 No size limits on documents
- 🔐 Built-in authentication

### Memory (Default)

**Perfect for:** Development, testing, stateless deployments

```python
# No setup needed!
# Memory sessions are the default

adk web agents/
```

**Characteristics:**
- ⚡ Fastest option
- 🎯 Simple (no external dependencies)
- ❌ Lost on server restart
- ❌ Only works on single server

### Custom Backend (DIY)

To implement your own backend:

1. Inherit from `BaseSessionStorage`:

```python
from google.adk.sessions import BaseSessionStorage

class PostgresSessionService(BaseSessionStorage):
    """Custom PostgreSQL session storage."""
    
    async def get_session(self, session_id: str):
        # Implement get logic
        pass
    
    async def set_session(self, session_id: str, data: dict):
        # Implement set logic
        pass
    
    async def delete_session(self, session_id: str):
        # Implement delete logic
        pass
```

2. Create a factory:

```python
def postgres_factory(uri: str, **kwargs):
    kwargs_copy = kwargs.copy()
    kwargs_copy.pop("agents_dir", None)
    return PostgresSessionService(uri=uri, **kwargs_copy)
```

3. Register it:

```python
registry = get_service_registry()
registry.register_session_service("postgres", postgres_factory)
```

## Tools

The agent includes 4 demonstration tools:

### 1. `describe_session_info`

Shows information about the current session.

```python
describe_session_info(session_id="my_session")
```

**Returns:**
```json
{
  "status": "success",
  "report": "Session my_session is active",
  "data": {
    "session_id": "my_session",
    "backend": "Session storage is configured via service registry",
    "persistence": "Supported (depends on backend)"
  }
}
```

### 2. `test_session_persistence`

Tests storing and retrieving data in the session.

```python
test_session_persistence(key="user_name", value="Alice")
```

**Returns:**
```json
{
  "status": "success",
  "report": "Stored user_name=Alice in session",
  "data": {
    "key": "user_name",
    "value": "Alice",
    "redis_command": "redis-cli GET session:user_name"
  }
}
```

### 3. `show_service_registry_info`

Displays service registry pattern and how it works.

```python
show_service_registry_info()
```

**Returns:** Information about the factory pattern and registration process.

### 4. `get_session_backend_guide`

Provides comparison of different session backends.

```python
get_session_backend_guide()
```

**Returns:** Detailed comparison of Redis, MongoDB, Memory, and Custom backends.

## Testing

### Run All Tests

```bash
make test
```

### Run Specific Test File

```bash
pytest tests/test_imports.py -v
pytest tests/test_tools.py -v
pytest tests/test_agent.py -v
```

### Run Tests in Watch Mode

```bash
make test-watch
```

### Test Coverage

```bash
make test
# Coverage report shows which code paths are tested
```

## Docker Services

### Start Services

```bash
make docker-up
```

This starts:
- **Redis**: `redis://localhost:6379` (data at `/data`)
- **MongoDB**: `mongodb://localhost:27017` (data at `/data/db`)

### Stop Services

```bash
make docker-down
```

### View Logs

```bash
make docker-logs

# Or specific service
docker-compose logs redis
docker-compose logs mongodb
```

### Full Cleanup (including volumes)

```bash
make clean-all
```

## Environment Variables

See `.env.example`:

```bash
# Google ADK
GOOGLE_API_KEY=your_key_here

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# MongoDB Configuration
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DATABASE=adk_sessions

# Session Service Selection
SESSION_SERVICE_TYPE=redis
SESSION_SERVICE_URI=redis://localhost:6379/0
```

## Key Learning Points

### 1. Service Registry Pattern

The service registry is a **factory registry** that maps URI schemes to creation functions:

- 📍 **Single Responsibility**: Registry only knows about schemes
- 🏭 **Factory Pattern**: Factories create service instances
- 🔗 **Loose Coupling**: New backends don't require code changes
- 🔄 **Extensible**: Add new backends anytime

### 2. Factory Functions

Every factory function:

1. Receives a **URI string**
2. Receives **kwargs** (always pop `agents_dir`)
3. Returns a **session service instance**

```python
def my_factory(uri: str, **kwargs):
    kwargs_copy = kwargs.copy()
    kwargs_copy.pop("agents_dir", None)  # ← IMPORTANT!
    
    # Parse URI if needed
    # Configure service
    # Return instance
    return MySessionService(**kwargs_copy)
```

### 3. BaseSessionStorage Interface

All session services must implement these methods:

```python
class MySessionService(BaseSessionStorage):
    async def get_session(self, session_id: str) -> dict:
        """Retrieve session data."""
        
    async def set_session(self, session_id: str, data: dict) -> None:
        """Store session data."""
        
    async def delete_session(self, session_id: str) -> None:
        """Delete session data."""
```

### 4. Production Considerations

- **Persistence**: Use Redis or MongoDB (not memory)
- **Scalability**: Redis/MongoDB work across multiple servers
- **Monitoring**: Monitor your storage backend (CPU, memory, connections)
- **Backup**: Implement backup strategy for persistence layer
- **Security**: Secure credentials in environment variables

## Commands Reference

```bash
# Setup & Installation
make setup              # Install dependencies and package
make clean             # Remove cache files

# Docker Services
make docker-up         # Start Redis and MongoDB
make docker-down       # Stop services
make docker-logs       # View service logs

# Development
make dev               # Start ADK web with Redis sessions
make demo              # Show demo and usage examples

# Testing
make test              # Run all tests with coverage
make test-watch        # Run tests in watch mode
make test-verbose      # Run tests with verbose output

# Cleanup
make clean             # Remove Python cache
make clean-all         # Stop Docker and remove volumes
```

## Common Issues

### Redis Connection Refused

```
Error: ConnectionError: Unable to connect to redis://localhost:6379
```

**Solution:**

```bash
# Start Docker services
make docker-up

# Or check if Redis is running
docker ps | grep redis
```

### MongoDB Authentication Failed

```
Error: ServerSelectionTimeoutError: Error connecting to MongoDB
```

**Solution:**

```bash
# Check MongoDB is running
docker-compose logs mongodb

# Verify credentials in .env match docker-compose.yml
MONGODB_USERNAME=admin
MONGODB_PASSWORD=password
```

### Tests Fail with Import Errors

```
ImportError: No module named google.adk
```

**Solution:**

```bash
# Install dependencies
pip install -r requirements.txt

# Ensure google-genai is installed
pip install google-genai>=1.15.0
```

## Integration with Your Project

To use custom session services in your own agent:

1. **Copy the pattern**:

```python
from google.adk.cli.service_registry import get_service_registry
from google.adk_community.sessions import redis_session_service

def redis_factory(uri: str, **kwargs):
    kwargs_copy = kwargs.copy()
    kwargs_copy.pop("agents_dir", None)
    return redis_session_service.RedisSessionService(**kwargs_copy)

registry = get_service_registry()
registry.register_session_service("redis", redis_factory)
```

2. **Use in your main file**:

```python
if __name__ == "__main__":
    cli_tools_click.main()
```

3. **Run with Redis**:

```bash
python your_agent.py web agents/ \
  --session_service_uri=redis://localhost:6379
```

## See Also

- **TIL Documentation**: `/docs/docs/til/til_custom_session_services_20251023.md`
- **Google ADK**: https://github.com/google/adk-python
- **Redis Documentation**: https://redis.io/documentation
- **MongoDB Documentation**: https://docs.mongodb.com
- **Service Registry Pattern**: https://refactoring.guru/design-patterns/factory-method

## Questions & Feedback

- 💬 Comment on the TIL
- 🐛 Report issues: https://github.com/raphaelmansuy/adk_training/issues
- 💡 Suggest improvements: https://github.com/raphaelmansuy/adk_training/discussions

---

**TIL**: Custom Session Services in Google ADK 1.17+  
**Difficulty**: Intermediate  
**Time**: ~8 minutes (reading) + ~30 minutes (hands-on)  
**Updated**: October 23, 2025
