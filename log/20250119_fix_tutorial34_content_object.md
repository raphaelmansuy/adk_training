# Tutorial 34: Fixed Content Object Bug in Subscriber

## Problem Sequence

### Problem 1: String Instead of Content Object
**Error**: `'str' object has no attribute 'role'`

The subscriber was passing a string directly as `new_message` parameter to `runner.run_async()`, but ADK expects a proper `types.Content` object with `role` and `parts` attributes.

**Solution**: Created proper Content objects with role and parts.

### Problem 2: Invalid Session ID (CURRENT)
**Error**: `Session not found: session_DOC-001`

After fixing the Content object, a new error appeared: the session ID was invalid because we were passing an arbitrary string instead of a session created via `session_service.create_session()`.

**Root Cause**: The ADK Runner requires sessions to be created and managed by the SessionService, not arbitrary strings.

## Root Cause Analysis

The bug occurred due to two missing pieces:
1. Messages must be `types.Content` objects with role and parts
2. Sessions must be created via `session_service.create_session()` before use

## Solution Applied

Updated both subscriber.py and README.md code examples:

1. **Added import**: `from google.genai import types`

2. **Created session before use**:
   ```python
   session = await session_service.create_session(
       app_name="pubsub_processor",
       user_id="pubsub_subscriber"
   )
   ```

3. **Use created session in runner.run_async()**:
   ```python
   async for event in runner.run_async(
       user_id="pubsub_subscriber",
       session_id=session.id,  # Use session.id, not arbitrary string
       new_message=prompt
   ):
       final_result = event
   ```

4. **Modified prompt creation**:
   ```python
   prompt_text = f"""..."""  # The actual text
   prompt = types.Content(
       role="user",
       parts=[types.Part(text=prompt_text)]
   )
   ```

## Files Modified
- `subscriber.py`: Added session creation, proper Content objects
- `README.md`: Updated both local testing example and full subscriber code example

## Testing
- ✅ All 80 unit tests pass
- ✅ subscriber.py syntax validation passes
- ✅ All imports validate successfully

## Reference
The fix was based on patterns in tutorial14/demos/basic_streaming_demo.py which shows:
1. Create session service
2. Create runner with session service
3. Call `session_service.create_session()` to get session object
4. Pass `session.id` to `runner.run_async()`
5. Pass `types.Content(role=..., parts=...)` as message

This is the correct pattern for ADK Runner session management.

