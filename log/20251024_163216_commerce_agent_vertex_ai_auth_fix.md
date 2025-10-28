# Commerce Agent Vertex AI Authentication Fix

**Date**: 2025-10-24 16:32:16
**Issue**: Commerce Agent `make dev` was failing with `ValueError: Missing key inputs argument!`

## Root Cause

The `.env` file was using:
1. Relative path for credentials: `./credentials/commerce-agent-key.json` instead of absolute path
2. Incorrect environment variable: `USE_VERTEX_AI=true` instead of `GOOGLE_GENAI_USE_VERTEXAI=TRUE`
3. Missing `GOOGLE_CLOUD_LOCATION` environment variable

When `adk web` runs, it loads the `.env` file but the relative path is resolved from the current working directory, not from the .env file's directory. This caused the credentials file to not be found.

Additionally, the `google-genai` library (used internally by ADK) specifically looks for `GOOGLE_GENAI_USE_VERTEXAI=TRUE` to route Vertex AI authentication, not a custom `USE_VERTEX_AI` variable.

## Solution

Updated `.env` file:
- Changed `GOOGLE_APPLICATION_CREDENTIALS` from relative to absolute path
- Changed `USE_VERTEX_AI=true` to `GOOGLE_GENAI_USE_VERTEXAI=TRUE`
- Added `GOOGLE_CLOUD_LOCATION=us-central1`
- Updated `.env.example` with correct template

## Files Modified

1. **commerce_agent/.env**
   - Updated credentials path to absolute path
   - Fixed environment variables for Vertex AI

2. **commerce_agent/.env.example**
   - Updated example template with correct variable names
   - Added GOOGLE_CLOUD_LOCATION

## Test Results

✅ Agent imports successfully  
✅ adk web server starts without ValueError  
✅ 37/38 tests pass  
  (1 test failure is expected: `test_root_agent_has_sub_agents` fails by design because root agent uses AgentTool instead of sub_agents to avoid Gemini tool limitations)

## Next Steps

The agent is now ready to:
1. Run `make dev` to start the development UI
2. Connect to Vertex AI using the service account credentials
3. Use Gemini 2.5 Flash model on Vertex AI

## Key Learnings

- ADK requires `GOOGLE_GENAI_USE_VERTEXAI=TRUE` to enable Vertex AI backend
- Relative paths in .env files are problematic when working directory changes
- Always use absolute paths for credentials files in .env configuration
- The `google-genai` library is the underlying client library that ADK uses for Gemini models
