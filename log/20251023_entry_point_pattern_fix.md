# Fix Summary: Entry Point Pattern for Session Service Registration

## Problem
Sessions were NOT persisting to Redis despite having a working RedisSessionService implementation.

**Root Cause:**
- Services were being registered during agent module import (in `agent.py`)
- This happens INSIDE ADK's application initialization
- Too late! ADK had already decided to use the default DatabaseSessionService
- Custom Redis service factory was never used by ADK

## Solution
Implemented the official ADK pattern from GitHub discussion #3175:

**Correct Pattern:**
1. Create entry point script (`__main__.py`)
2. Register services in entry point (BEFORE ADK CLI starts)
3. Call `cli_tools_click.main()` to start ADK
4. ADK sees registered services in the registry and uses them

## Changes Made

### 1. Created `custom_session_agent/__main__.py`
- Entry point that runs when invoking: `python -m custom_session_agent`
- Registers Redis and Memory services BEFORE calling ADK CLI
- Ensures services are available when ADK initializes session system

### 2. Updated Makefile dev target
- Old: `adk web` (doesn't use entry point)
- New: `python -m custom_session_agent web --session_service_uri=redis://localhost:6379`
- Ensures entry point pattern is used

### 3. Removed duplicate registration from agent.py
- Removed lines 397-399 that were registering services at import time
- Services are now registered by the entry point only
- Cleaner separation of concerns

## Technical Details

### Service Registration Timing (Critical!)
```
❌ WRONG (agent.py):
  adk web
    ↓ ADK loads app
    ↓ ADK imports agent module
    ↓ Services register (TOO LATE)
    ↗ ADK already chose session service

✅ RIGHT (entry point):
  __main__.py runs first
    ↓ Services register
    ↓ Then call cli_tools_click.main()
    ↓ ADK sees registered services
    ↗ ADK uses registered Redis service
```

### How It Works
1. User runs: `python -m custom_session_agent web --session_service_uri=redis://`
2. Python loads `__main__.py` module
3. `__main__.py` imports CustomSessionServiceDemo
4. Calls `CustomSessionServiceDemo.register_redis_service()`
5. Calls `CustomSessionServiceDemo.register_memory_service()`
6. Services are now in the service registry
7. Then `cli_tools_click.main()` is called
8. ADK CLI starts and sees registered services
9. When user specifies `--session_service_uri=redis://`, ADK uses the registered factory
10. Sessions now persist to Redis!

## Verification Results

### Entry Point Pattern Test (test_entry_point_pattern.py)
✅ All 5 tests passed:
1. Entry point imports successfully
2. Service registration methods exist
3. RedisSessionService connects to Redis
4. Sessions stored in Redis with correct TTL
5. Service registry pattern verified

### Unit Tests
✅ 26 passed, 1 skipped
- All agent configuration tests pass
- All import tests pass
- All tool function tests pass

### Redis Verification
✅ Session key found in Redis:
```
redis-cli KEYS "*"
→ session:test_app:test_user:test_session_123
```

Session data in Redis:
```json
{
  "app_name": "test_app",
  "user_id": "test_user",
  "session_id": "test_session_123",
  "state": {"test_key": "test_value"},
  "created_at": "2025-10-23T08:26:52.633313",
  "updated_at": "2025-10-23T08:26:52.633318",
  "events": []
}
```

## Key Learning Points

1. **Service registration timing matters**
   - Must happen BEFORE ADK initializes its session system
   - Entry point pattern is the correct approach

2. **Factory function pattern**
   - Maps URI schemes to service factories
   - `register_session_service(scheme, factory_function)`
   - Factory receives URI and returns service instance

3. **Correct usage**
   - `python -m custom_session_agent web --session_service_uri=redis://localhost:6379`
   - NOT: `adk web` (bypasses entry point)

## Files Changed
- ✅ `/custom_session_agent/__main__.py` - Created entry point
- ✅ `/custom_session_agent/agent.py` - Removed duplicate registration
- ✅ `/Makefile` - Updated dev target to use entry point
- ✅ `/test_entry_point_pattern.py` - Created comprehensive test

## Testing Procedure
1. `make setup` - Install dependencies
2. `make docker-up` - Start Redis
3. `python test_entry_point_pattern.py` - Verify entry point pattern
4. `redis-cli KEYS "*"` - Verify session keys in Redis
5. `make test` - Verify all unit tests pass

## Next Steps
1. Update TIL documentation to emphasize entry point pattern
2. Update demo instructions to show correct usage
3. Add troubleshooting guide for common issues

## References
- GitHub discussion: https://github.com/google/adk-python/discussions/3175
- TIL: til_custom_session_services_20251023.md
- README: ./README.md
