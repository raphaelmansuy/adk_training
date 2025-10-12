# Tutorial 25 - Critical API Errors Found

**Date**: 2025-01-13 22:00:00  
**Tutorial**: 25_best_practices.md  
**Status**: CRITICAL - Multiple API usage errors throughout tutorial  
**Impact**: HIGH - Tutorial examples would fail with API errors

## Issues Summary

Found **2 CRITICAL categories** of API misuse affecting **22+ code examples**:

1. ❌ **RunConfig with plugins/trace_to_cloud** (Line 915)
2. ❌ **Old runner.run_async() API signature** (20+ occurrences)

---

## Issue 1: RunConfig with plugins and trace_to_cloud

### Location
- **File**: `docs/tutorial/25_best_practices.md`
- **Line**: 915
- **Section**: "Common Pitfalls & Solutions" → "Pitfall 4: No Monitoring"

### Current Code (WRONG)
```python
# ✅ Comprehensive monitoring
run_config = RunConfig(
    trace_to_cloud=True,
    plugins=[metrics_plugin, alerting_plugin]
)
```

### Problems
1. **RunConfig has NO `plugins` parameter**
   - Verified in: `/research/adk-python/src/google/adk/agents/run_config.py`
   - RunConfig fields: `speech_config`, `streaming_mode`, `max_llm_calls`, audio configs
   - Attempting to use `plugins=` will cause `ValidationError` (pydantic extra='forbid')

2. **RunConfig has NO `trace_to_cloud` parameter**
   - Same source verification
   - `trace_to_cloud` is a CLI deployment flag (`--trace_to_cloud`)
   - NOT a runtime configuration parameter

### Correct Patterns

**For Plugins:**
```python
# ✅ Correct: Register plugins with Runner
runner = InMemoryRunner(
    agent=agent,
    app_name='monitoring_app',
    plugins=[metrics_plugin, alerting_plugin]
)
```

**For Tracing:**
```python
# ✅ Correct: Deployment-time CLI flag
# adk deploy cloud_run --trace_to_cloud

# OR programmatic with AdkApp for Agent Engine
from google.adk.apps.agent_engine_utils import AdkApp
app = AdkApp(agent=agent, enable_tracing=True)
```

### Source Verification
- **RunConfig Source**: `research/adk-python/src/google/adk/agents/run_config.py`
- **Runner Source**: `research/adk-python/src/google/adk/runners.py` (lines 100-150)
- **App Source**: `research/adk-python/src/google/adk/apps/app.py`
- **Official Sample**: `research/adk-python/contributing/samples/plugin_basic/main.py`

---

## Issue 2: Old runner.run_async() API Signature

### Location
**20+ occurrences** throughout the tutorial at lines:
- 268, 284, 377, 488, 585, 696, 721, 740, 763, 799, 882 (and more)

### Current Pattern (WRONG)
```python
# ❌ OLD API - no longer works
runner = Runner()
result = await runner.run_async(query, agent=agent)
response = result.content.parts[0].text
```

### Problem
The `run_async()` method signature changed in ADK v1.16+:

**Actual Signature** (from `runners.py` line 336):
```python
async def run_async(
    self,
    *,
    user_id: str,              # ❌ REQUIRED
    session_id: str,           # ❌ REQUIRED
    invocation_id: Optional[str] = None,
    new_message: Optional[types.Content] = None,  # ❌ Content object, not string
    state_delta: Optional[dict[str, Any]] = None,
    run_config: Optional[RunConfig] = None,
) -> AsyncGenerator[Event, None]:  # ❌ Returns async generator, not single result
```

Key differences:
1. **Requires `user_id` and `session_id`** - no longer accepts positional query argument
2. **`new_message` is `types.Content`** - not a plain string
3. **Returns `AsyncGenerator[Event]`** - not a single result object
4. **No `agent=` parameter** - agent is set in Runner constructor

### Correct Pattern

```python
# ✅ CORRECT: Modern ADK v1.16+ API
from google.genai import types

# 1. Create runner with agent
runner = InMemoryRunner(agent=agent, app_name='test_app')

# 2. Create or get session
session = await runner.session_service.create_session(
    app_name='test_app',
    user_id='user_123'
)

# 3. Create Content object
new_message = types.Content(
    role='user',
    parts=[types.Part(text=query)]
)

# 4. Run and iterate over events
async for event in runner.run_async(
    user_id='user_123',
    session_id=session.id,
    new_message=new_message
):
    if event.content and event.content.parts:
        response = event.content.parts[0].text
        print(response)
```

### Affected Examples
All these examples use the old API and need updating:

1. **Line 268** - Parallel processing example
2. **Line 284** - Sequential processing example  
3. **Line 377** - Authentication example
4. **Line 488** - Error handling example
5. **Line 585** - Graceful degradation example
6. **Line 696** - Batch classification example
7. **Line 721** - Unit test example
8. **Line 740** - Tool invocation test
9. **Line 763** - Multi-agent workflow test
10. **Line 799** - Evaluation framework example
11. **Line 882** - Input validation example

---

## Impact Assessment

### Severity: CRITICAL

1. **All Examples Would Fail**
   - Every `runner.run_async(query, agent=agent)` call will raise TypeError
   - Error: "missing required argument: 'user_id'"
   - Tutorial completely unusable as-is

2. **RunConfig Example Misleading**
   - Suggests using parameters that don't exist
   - Would cause ValidationError immediately
   - Misdirects users on how to configure monitoring

3. **Tutorial Scope**
   - Tutorial 25 is "Best Practices" - supposed to show CORRECT patterns
   - Instead shows OUTDATED/WRONG patterns throughout
   - High impact on user trust and learning

### User Impact

**Before Fix:**
- Copy any code example → immediate API errors
- Follow monitoring advice → ValidationError
- Learn wrong patterns from "best practices" tutorial
- Frustrated users, damaged reputation

**After Fix:**
- All examples use verified ADK v1.16+ APIs
- Correct plugin registration patterns
- Correct tracing configuration guidance
- Users learn actual best practices

---

## Fix Strategy

### Fix 1: Update RunConfig Monitoring Example (Line ~915)

**Replace:**
```python
# ❌ Comprehensive monitoring
run_config = RunConfig(
    trace_to_cloud=True,
    plugins=[metrics_plugin, alerting_plugin]
)
```

**With:**
```python
# ✅ Comprehensive monitoring - correct approach
from google.adk.runners import InMemoryRunner
from google.adk.plugins import BasePlugin

# Register plugins with Runner (NOT RunConfig)
runner = InMemoryRunner(
    agent=agent,
    app_name='monitored_app',
    plugins=[metrics_plugin, alerting_plugin]
)

# Tracing configured at deployment (CLI flag)
# adk deploy cloud_run --trace_to_cloud
```

### Fix 2: Update ALL runner.run_async() Calls

Need to update **20+ examples** with the pattern:

**Template:**
```python
# ✅ Correct modern API
from google.genai import types

runner = InMemoryRunner(agent=agent, app_name='app')
session = await runner.session_service.create_session(
    app_name='app',
    user_id='user_id'
)

new_message = types.Content(
    role='user',
    parts=[types.Part(text=query)]
)

async for event in runner.run_async(
    user_id='user_id',
    session_id=session.id,
    new_message=new_message
):
    if event.content and event.content.parts:
        response = event.content.parts[0].text
```

### Fix 3: Add Verification Info Box

Add at top of tutorial:
```markdown
:::info API Verification

This tutorial has been verified against **ADK Python SDK v1.16.0+**.

**Key API Changes** from older versions:
- ✅ `runner.run_async()` requires `user_id`, `session_id`, returns `AsyncGenerator[Event]`
- ✅ Plugins registered with `Runner(plugins=[...])` or `App(plugins=[...])`
- ✅ `trace_to_cloud` is CLI deployment flag, not RunConfig parameter
- ❌ OLD: `runner.run_async(query, agent=agent)` - no longer works

Source verification: `research/adk-python/src/google/adk/runners.py` (2025-01-13)
:::
```

---

## Source Code Evidence

### RunConfig Actual Fields
```python
# From: research/adk-python/src/google/adk/agents/run_config.py
class RunConfig(BaseModel):
    model_config = ConfigDict(extra='forbid')  # ❌ NO EXTRA FIELDS ALLOWED
    
    # Actual fields:
    speech_config: Optional[types.SpeechConfig] = None
    streaming_mode: StreamingMode = StreamingMode.NONE
    max_llm_calls: int = 500
    save_live_audio: bool = False
    save_input_blobs_as_artifacts: bool = False
    support_cfc: bool = False
    response_modalities: Optional[list[str]] = None
    input_audio_transcription: Optional[types.AudioTranscriptionConfig] = None
    output_audio_transcription: Optional[types.AudioTranscriptionConfig] = None
    # ... NO plugins, NO trace_to_cloud
```

### Runner Constructor Signature
```python
# From: research/adk-python/src/google/adk/runners.py (line ~100)
def __init__(
    self,
    *,
    app: Optional[App] = None,
    app_name: Optional[str] = None,
    agent: Optional[BaseAgent] = None,
    plugins: Optional[List[BasePlugin]] = None,  # ✅ PLUGINS HERE
    artifact_service: Optional[BaseArtifactService] = None,
    session_service: BaseSessionService,
    memory_service: Optional[BaseMemoryService] = None,
    credential_service: Optional[BaseCredentialService] = None,
):
```

### run_async Method Signature
```python
# From: research/adk-python/src/google/adk/runners.py (line ~336)
async def run_async(
    self,
    *,
    user_id: str,  # ✅ REQUIRED
    session_id: str,  # ✅ REQUIRED
    invocation_id: Optional[str] = None,
    new_message: Optional[types.Content] = None,  # ✅ Content object
    state_delta: Optional[dict[str, Any]] = None,
    run_config: Optional[RunConfig] = None,
) -> AsyncGenerator[Event, None]:  # ✅ Returns event stream
```

---

## Verification Date
- **Date**: 2025-01-13
- **ADK Version**: v1.16.0+
- **Source**: `/research/adk-python/src/google/adk/`

## Next Steps
1. Create comprehensive fix for Tutorial 25
2. Update all 22+ affected code examples
3. Add verification info box
4. Update Summary section with correct APIs
5. Test at least one example pattern to confirm

---

## Related Issues
- Tutorial 24 had same RunConfig(plugins, trace_to_cloud) issue - already fixed
- Tutorial 20 had AgentConfig.from_yaml_file() issue - already fixed
- Pattern: DRAFT tutorials not updated for ADK v1.16+ breaking changes
