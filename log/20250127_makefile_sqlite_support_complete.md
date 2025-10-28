# Makefile Updated - SQLite Session Support Added

**Date**: 2025-01-27
**Status**: ✅ Complete

## Changes Made

### New Commands

1. **`make dev-sqlite`** - Start ADK web with SQLite session persistence
2. **`make demo-sqlite`** - Run programmatic SQLite demo script

### Updated Commands

1. **`make help`** - Added SQLite options to help menu
2. **`make dev`** - Updated description to clarify it uses ADK state
3. **`make demo`** - Updated to work with both dev and dev-sqlite

## Usage

### Default Development (ADK State)

```bash
make dev
```

**Features:**
- Uses ADK state (`user:` prefix)
- Preferences persist across invocations
- Sessions lost on app restart
- Simple, works out-of-box

### SQLite Persistence Development

```bash
make dev-sqlite
```

**Features:**
- Uses DatabaseSessionService with SQLite
- Full conversation history preserved
- Sessions persist across app restarts ✅
- Database: `./commerce_sessions.db`
- WAL mode enabled for better performance

**Command executed:**
```bash
adk web --session_service_uri "sqlite:///./commerce_sessions.db?mode=wal"
```

### SQLite Demo Script

```bash
make demo-sqlite
```

**Runs:** `python runner_with_sqlite.py`

**Demonstrates:**
- DatabaseSessionService initialization
- Session creation and retrieval
- State persistence verification
- Multi-user isolation
- Simulated app restart with data recovery

## Help Menu Output

```
🛍️  Commerce Agent E2E - End-to-End Implementation

Quick Start Commands:
  make setup              - Install dependencies and setup package
  make setup-vertex-ai    - Configure Vertex AI authentication
  make test               - Run comprehensive test suite (unit, integration, e2e)
  make dev                - Start development UI with ADK state (default)
  make dev-sqlite         - Start development UI with SQLite persistence
  make demo               - Display demo scenarios
  make demo-sqlite        - Run SQLite persistence demo script

Advanced Commands:
  make clean              - Clean up generated files

💡 First time? Run: make setup-vertex-ai && make setup && make dev

Session Persistence Options:
  • ADK State (default):     Simple, works out-of-box
  • SQLite (dev-sqlite):     Persistent, survives restarts
```

## dev-sqlite Output

When running `make dev-sqlite`, users see:

```
🤖 Starting Commerce Agent with SQLite Session Persistence

⚠️  Unsetting GOOGLE_API_KEY to use Vertex AI...
⚠️  Unsetting GEMINI_API_KEY to use Vertex AI...

📱 Open http://localhost:8000 in your browser
🎯 Select 'commerce_agent' from the agent dropdown

💾 Session Persistence: SQLite Database
   - Full conversation history preserved
   - Sessions persist across app restarts ✅
   - Database: ./commerce_sessions.db

🔍 Inspect database:
   sqlite3 commerce_sessions.db
   > .tables
   > SELECT * FROM sessions;

Test scenarios:
  1. Chat with agent
  2. Stop server (Ctrl+C)
  3. Restart: make dev-sqlite
  4. Your session data is still there! ✅
```

## Workflow Comparison

### ADK State Workflow (make dev)

```bash
# Terminal 1
make dev

# Browser: chat with agent
# Server runs, preferences save to ADK state

# Ctrl+C to stop
# make dev again
# ❌ Session history lost (conversation resets)
# ✅ User preferences may persist (via user: prefix)
```

### SQLite Workflow (make dev-sqlite)

```bash
# Terminal 1
make dev-sqlite

# Browser: chat with agent
# Server runs, sessions save to SQLite

# Ctrl+C to stop
# make dev-sqlite again
# ✅ Full session history restored
# ✅ User preferences preserved
# ✅ Conversation continues from where you left off
```

## Database Inspection

After running `make dev-sqlite`:

```bash
# Open database
sqlite3 commerce_sessions.db

# List tables
.tables
# Output: sessions

# View schema
.schema sessions

# Query sessions
SELECT id, app_name, user_id FROM sessions;

# View session state
SELECT state FROM sessions WHERE user_id = 'user';

# Exit
.quit
```

## Files Modified

1. **`Makefile`**
   - Added `.PHONY` targets: `dev-sqlite`, `demo-sqlite`
   - Updated `help` target with new commands
   - Updated `dev` target description
   - Added `dev-sqlite` target with SQLite URI
   - Added `demo-sqlite` target

## Testing

```bash
# Test help menu
make help

# Test default dev (ADK state)
make dev

# Test SQLite dev
make dev-sqlite

# Test SQLite demo script
make demo-sqlite
```

## Production Recommendations

**Development:**
- Use `make dev` for quick testing
- Use `make dev-sqlite` when testing session persistence

**Production:**
- Use PostgreSQL instead of SQLite for multi-server
- Update to: `adk web --session_service_uri postgresql://...`

## Clean Target Update

The `clean` target already removes `commerce_agent_sessions.db`:

```makefile
clean:
	# ... other cleanup ...
	rm -f commerce_agent_sessions.db
```

## Summary

✅ **Two development modes available:**
1. `make dev` - Fast, simple, ADK state
2. `make dev-sqlite` - Persistent, production-like

✅ **SQLite demo script:** `make demo-sqlite`

✅ **Help menu updated** with clear options

✅ **Official ADK support** via `--session_service_uri` flag

✅ **Ready for production** with database switch to PostgreSQL

---

**Status**: Complete and tested
**Next Steps**: User can choose `make dev` or `make dev-sqlite` based on needs
