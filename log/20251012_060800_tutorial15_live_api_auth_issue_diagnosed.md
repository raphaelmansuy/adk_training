# Tutorial 15 Live API Authentication Issue - API Key Not Supported

## Summary
The Tutorial 15 Live API demo fails because the Live API requires OAuth2/Vertex AI authentication, not Google AI Studio API keys. The error "API keys are not supported by this API" confirms that Live API only works with Vertex AI credentials.

## Root Cause Analysis
- **Live API Authentication**: Requires OAuth2 access tokens from Vertex AI
- **API Key Limitation**: Google AI Studio API keys are not accepted by Live API
- **Environment Issue**: Tutorial was configured for API key usage but Live API needs Vertex AI

## Error Details
```
Connection closed: received 1008 (policy violation) API keys are not supported by this API. 
Expected OAuth2 access token or other authentication credentials that assert a principal.
```

## Current Environment
- `GOOGLE_API_KEY`: Set ✓
- `GOOGLE_GENAI_USE_VERTEXAI`: Not set (needs to be 1)
- `GOOGLE_CLOUD_PROJECT`: Not set (required for Vertex AI)

## Required Changes
1. **Authentication**: Switch from API key to Vertex AI OAuth2
2. **Environment Variables**: Set `GOOGLE_GENAI_USE_VERTEXAI=1` and `GOOGLE_CLOUD_PROJECT`
3. **Credentials**: Use Vertex AI service account or OAuth2 flow

## Alternative Solutions
1. **Vertex AI Setup**: Configure proper Vertex AI project and credentials
2. **Fallback Demo**: Create text-only demo without Live API for API key users
3. **Documentation Update**: Clarify that Live API requires Vertex AI

## Impact
- **Current State**: Demo hangs for 3+ minutes then fails with auth error
- **User Experience**: Confusing timeout with unclear error message
- **Tutorial Completeness**: Live API features unavailable without Vertex AI setup

## Recommended Fix
Update the demo to detect authentication method and provide appropriate feedback:

```python
# Check for proper Live API authentication
if not os.getenv('GOOGLE_GENAI_USE_VERTEXAI') or not os.getenv('GOOGLE_CLOUD_PROJECT'):
    print("⚠️  Live API requires Vertex AI authentication:")
    print("   Set GOOGLE_GENAI_USE_VERTEXAI=1")
    print("   Set GOOGLE_CLOUD_PROJECT=your-project-id")
    print("   Configure Vertex AI credentials")
    print()
    print("💡 For text-only demo without Live API, see basic_demo")
    return
```

## Files Affected
- `voice_assistant/demo.py` - Main demo script
- `voice_assistant/agent.py` - VoiceAssistant class
- All Live API examples in tutorial

## Status
✅ **DIAGNOSED** - Root cause identified as authentication mismatch. Live API requires Vertex AI OAuth2, not API keys.</content>
<parameter name="filePath">/Users/raphaelmansuy/Github/03-working/adk_training/log/20251012_060800_tutorial15_live_api_auth_issue_diagnosed.md