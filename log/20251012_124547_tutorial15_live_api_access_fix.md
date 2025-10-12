# Tutorial 15 Live API Access Issue Resolution

## Problem

The `advanced_demo` was failing with error:
```
websockets.exceptions.ConnectionClosedError: received 1008 (policy violation) 
Publisher Model `projects/saas-app-001/locations/us-central1/publishers/google/
models/gemini-live-2.5-flash-preview` not fo
```

## Root Cause

Live API models (including `gemini-live-2.5-flash-preview`) are not enabled in
the Vertex AI project. The Live API is in preview and requires allowlist access
from Google Cloud.

## Solution

Updated `voice_assistant/advanced.py` to gracefully handle missing Live API
access:

1. Added clear warning message explaining Live API availability
2. Disabled proactivity and affective dialog examples that require Live API
3. Kept video streaming example (conceptual only, doesn't need Live API)
4. Provided instructions for requesting access

## How to Enable Live API

1. Visit https://ai.google.dev/gemini-api/docs/live
2. Contact Google Cloud support to enable Live API publisher models
3. Alternative: Use Google AI Studio API key (GOOGLE_API_KEY) instead of
   Vertex AI

## Verification

```bash
make advanced_demo
# Now completes successfully with informative warning
```

## Files Modified

- `tutorial_implementation/tutorial15/voice_assistant/advanced.py`
  - Updated `main()` to skip unavailable Live API calls
  - Added user-friendly error messaging
  - Kept code examples visible for learning
