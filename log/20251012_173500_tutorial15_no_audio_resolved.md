# Tutorial 15: Live API Audio Demo - No Sound Issue Resolved

**Date**: October 12, 2025  
**Status**: ✅ Root Cause Identified

## Problem

User ran `make basic_demo_audio` and got no sound:
- ✅ Environment check passed
- ✅ Audio dependencies available
- ❌ No audio played
- ❌ Demo hung without error message

## Root Cause

**The model `gemini-2.0-flash-live-preview-04-09` only works with Vertex AI, not API keys.**

The connection error was:
```
Connection closed: received 1008 (policy violation) 
models/gemini-2.0-flash-live-preview-04-09 is not found for API version v1alpha, 
or is not supported for bidiGenerateConten
```

###  Why the Environment Check Passed

The Makefile sets `GOOGLE_GENAI_USE_VERTEXAI=1` in its targets:

```makefile
export GOOGLE_GENAI_USE_VERTEXAI ?= 1
export GOOGLE_CLOUD_PROJECT ?= saas-app-001
```

**BUT** the user's shell environment had `GOOGLE_API_KEY` set, which the ADK prioritizes over Vertex AI settings.

### The Issue

1. Environment has: `GOOGLE_API_KEY=AIzaSy...` (set in shell)
2. Environment missing: `GOOGLE_GENAI_USE_VERTEXAI` (only in Makefile)
3. ADK sees API key → Uses AI Studio API (not Vertex)
4. Model `gemini-2.0-flash-live-preview-04-09` → Only available on Vertex
5. Connection fails with "model not found"

## Solution

The user needs to **export environment variables in their shell**, not just rely on Makefile:

```bash
# Required for Live API with this model
export GOOGLE_GENAI_USE_VERTEXAI=1
export GOOGLE_CLOUD_PROJECT=saas-app-001
export GOOGLE_CLOUD_LOCATION=us-central1
export VOICE_ASSISTANT_LIVE_MODEL=gemini-2.0-flash-live-preview-04-09

# Authenticate with Vertex AI
gcloud auth application-default login

# Then run the demo
make basic_demo_audio
```

### Alternative: Unset API Keys

```bash
# Temporarily unset API keys to force Vertex AI usage
unset GOOGLE_API_KEY
unset GEMINI_API_KEY

# Makefile will use Vertex AI
make basic_demo_audio
```

## Model Compatibility

| Model | API Key Support | Vertex AI Support | Live API |
|-------|----------------|-------------------|----------|
| `gemini-2.0-flash-live-preview-04-09` | ❌ NO | ✅ YES | ✅ YES |
| `gemini-2.0-flash-live-001` | ✅ YES | ✅ YES | ✅ YES |
| `gemini-2.5-flash` | ✅ YES | ✅ YES | ❌ NO |

The model we're using (`gemini-2.0-flash-live-preview-04-09`) is Vertex-only.

## Recommended Fixes

### 1. Update Documentation

Add clear warning in README.md and AUDIO_SETUP.md:

```markdown
⚠️ **IMPORTANT**: Live API demos require proper environment setup

The `gemini-2.0-flash-live-preview-04-09` model requires Vertex AI.
Export these variables in your shell before running demos:

export GOOGLE_GENAI_USE_VERTEXAI=1
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_LOCATION=us-central1
```

### 2. Improve Error Messages

Update basic_demo.py to detect this specific error and provide helpful guidance.

### 3. Environment Check Enhancement

The `live_env_check` target should verify that Vertex AI will actually be used (not just that the model exists).

## Verification Steps

1. **Check current authentication**:
   ```bash
   env | grep -E "GOOGLE_|GEMINI_"
   ```

2. **Set up Vertex AI properly**:
   ```bash
   export GOOGLE_GENAI_USE_VERTEXAI=1
   export GOOGLE_CLOUD_PROJECT=saas-app-001
   gcloud auth application-default login
   ```

3. **Run demo**:
   ```bash
   make basic_demo_audio
   ```

## Expected Behavior After Fix

```
🎯 Running Basic Live API Demo (AUDIO MODE)...
🎤 User: Hello, how are you today?
🔊 Agent speaking...
   (Receiving response...)
..............  [Audio plays through speakers]
💾 Audio saved to: response.wav (XXXXX bytes)
```

## Status

- ✅ Root cause identified: API key vs Vertex AI conflict
- ✅ Solution documented
- ⏳ User needs to export environment variables
- ⏳ Documentation improvements needed
- ⏳ Better error messaging needed

The demo will work once proper Vertex AI environment variables are exported in the user's shell.
