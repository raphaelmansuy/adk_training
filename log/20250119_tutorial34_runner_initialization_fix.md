# Tutorial 34: Runner API Initialization Fix

**Date**: January 19, 2025
**Status**: Complete ✅

## Problem Statement

The subscriber encountered an error when initializing the Runner class:
```
Either app or both app_name and agent must be provided.
```

This occurred after fixing the import paths but getting the Runner initialization parameters wrong.

## Root Cause

The Runner class requires specific initialization parameters:
- **Option 1**: Provide `app` (an App instance)
- **Option 2**: Provide both `app_name` (string) and `agent` (Agent instance)

The code was only providing `agent`, missing the required `app_name` parameter.

## Solution

Updated the Runner initialization to include the `app_name` parameter:

**Before (incorrect)**:
```python
runner = Runner(
    agent=root_agent,
    session_service=session_service
)
```

**After (correct)**:
```python
session_service = InMemorySessionService()
runner = Runner(
    app_name="pubsub_processor",
    agent=root_agent,
    session_service=session_service
)
```

## Files Modified

1. **subscriber.py**: Updated Runner initialization with `app_name` parameter
2. **README.md**: Updated both code examples (section on local testing and full subscriber example) with correct Runner initialization

## Changes Details

### subscriber.py
- Added `app_name="pubsub_processor"` parameter to Runner
- Kept `agent=root_agent` and `session_service=session_service` parameters
- Maintained session service initialization with `InMemorySessionService()`

### README.md
- Updated local testing example to show `app_name` parameter
- Updated full subscriber.py code example in section 5
- Added comment explaining Runner parameter requirements

## Testing Results

- ✅ All 80 unit tests pass
- ✅ Valid Python syntax
- ✅ Correct Runner API usage
- ✅ All parameters properly configured
- ✅ Ready for Pub/Sub message processing

## Architecture Notes

The `app_name` parameter helps ADK identify the application context. Using "pubsub_processor" makes sense because:
1. It identifies the application purpose
2. It's used for logging and monitoring
3. It helps with session and state management

## Next Steps

The subscriber is now properly configured to:
1. Receive Pub/Sub messages
2. Create a new Runner instance with proper parameters
3. Route documents through the coordinator agent
4. Process with specialized analyzers
5. Return structured JSON results

No further changes needed for the Runner initialization pattern.
