# Tutorial 24 Advanced Observability - CRITICAL API ERRORS FOUND

**Date**: January 13, 2025, 21:20:00  
**Tutorial**: Tutorial 24 - Advanced Observability & Monitoring  
**Status**: CRITICAL ISSUES FOUND ❌ - REQUIRES FIXES  
**Severity**: HIGH - Multiple incorrect API usages

---

## Critical Issues Summary

**2 CRITICAL API ERRORS** found in Tutorial 24:

1. ❌ **RunConfig does NOT have `plugins` parameter**
2. ❌ **RunConfig does NOT have `trace_to_cloud` parameter**

Both are fundamental API errors that would cause immediate failures.

---

## Issue 1: Wrong Plugin Registration API (CRITICAL)

### Tutorial Claims (INCORRECT) ❌

```python
# Tutorial shows this (WRONG):
run_config = RunConfig(
    plugins=[artifact_plugin]  # ❌ RunConfig has NO plugins parameter
)

runner = Runner()
result = await runner.run_async(
    "query",
    agent=agent,
    run_config=run_config  # ❌ Wrong approach
)
```

### Actual API (CORRECT) ✅

**Source**: `/research/adk-python/contributing/samples/plugin_basic/main.py`

```python
# Correct way to use plugins:
runner = InMemoryRunner(
    agent=root_agent,
    app_name='test_app_with_plugin',
    plugins=[CountInvocationPlugin()],  # ✅ Plugins go in Runner constructor
)

async for event in runner.run_async(
    user_id='user',
    session_id=session.id,
    new_message=types.Content(...)
):
    # Process events
```

**Alternative Correct Approach** (using App):

**Source**: `/research/adk-python/src/google/adk/apps/app.py`

```python
from google.adk.apps.app import App

app = App(
    name='my_app',
    root_agent=agent,
    plugins=[artifact_plugin]  # ✅ Plugins registered at App level
)

runner = Runner(app=app)
```

### RunConfig Source Code Verification

**File**: `/research/adk-python/src/google/adk/agents/run_config.py`

**Actual RunConfig fields**:
```python
class RunConfig(BaseModel):
    speech_config: Optional[types.SpeechConfig] = None
    response_modalities: Optional[list[str]] = None
    save_input_blobs_as_artifacts: bool = False  # DEPRECATED
    support_cfc: bool = False
    streaming_mode: StreamingMode = StreamingMode.NONE
    output_audio_transcription: Optional[types.AudioTranscriptionConfig] = ...
    input_audio_transcription: Optional[types.AudioTranscriptionConfig] = ...
    realtime_input_config: Optional[types.RealtimeInputConfig] = None
    enable_affective_dialog: Optional[bool] = None
    proactivity: Optional[types.ProactivityConfig] = None
    session_resumption: Optional[types.SessionResumptionConfig] = None
    save_live_audio: bool = False
    max_llm_calls: int = 500
    
    # ❌ NO plugins parameter
    # ❌ NO trace_to_cloud parameter
```

**Conclusion**: `RunConfig` is for runtime behavior configuration (streaming, audio, etc.), NOT for plugins or tracing.

---

## Issue 2: Wrong trace_to_cloud Location (CRITICAL)

### Tutorial Claims (INCORRECT) ❌

```python
# Tutorial shows this (WRONG):
run_config = RunConfig(
    trace_to_cloud=True  # ❌ RunConfig has NO trace_to_cloud parameter
)

result = await runner.run_async(
    "query",
    agent=agent,
    run_config=run_config
)
```

### Actual API (CORRECT) ✅

**trace_to_cloud** is a **CLI option**, not a RunConfig parameter.

**Source**: `/research/adk-python/src/google/adk/cli/cli_tools_click.py`

```bash
# CLI usage (CORRECT):
adk web --trace_to_cloud

adk api_server --trace_to_cloud

adk deploy cloud_run --trace_to_cloud
```

**Deployment Template Usage**:

**Source**: `/research/adk-python/src/google/adk/cli/cli_deploy.py`

```python
_AGENT_ENGINE_APP_TEMPLATE = """
from vertexai.preview.reasoning_engines import AdkApp

adk_app = AdkApp(
  agent=root_agent,
  enable_tracing={trace_to_cloud_option},  # ✅ At AdkApp level
)
"""
```

**Conclusion**: `trace_to_cloud` is:
- ✅ A CLI flag for deployments
- ✅ An `enable_tracing` parameter in `AdkApp` for Agent Engine
- ❌ NOT a `RunConfig` parameter
- ❌ NOT a `Runner` parameter for local execution

---

## Correct API Patterns

### Pattern 1: Plugins with Runner

```python
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.plugins import SaveFilesAsArtifactsPlugin

agent = Agent(
    model='gemini-2.0-flash',
    name='my_agent',
    instruction="You are helpful"
)

# Create plugin
plugin = SaveFilesAsArtifactsPlugin()

# Register plugin with runner
runner = InMemoryRunner(
    agent=agent,
    app_name='my_app',
    plugins=[plugin]  # ✅ Correct location
)

# Run agent
session = await runner.session_service.create_session(
    user_id='user',
    app_name='my_app'
)

async for event in runner.run_async(
    user_id='user',
    session_id=session.id,
    new_message=types.Content(role='user', parts=[...])
):
    print(event)
```

### Pattern 2: Plugins with App

```python
from google.adk.apps.app import App
from google.adk.agents import Agent, Runner
from google.adk.plugins import SaveFilesAsArtifactsPlugin

agent = Agent(...)
plugin = SaveFilesAsArtifactsPlugin()

# Register plugin at App level
app = App(
    name='my_app',
    root_agent=agent,
    plugins=[plugin]  # ✅ Correct location
)

# Create runner with app
runner = Runner(app=app)

# Run
result = await runner.run_async(
    user_id='user',
    session_id=session_id,
    new_message=content
)
```

### Pattern 3: Cloud Trace (Deployment Only)

```bash
# Deploy with tracing enabled
adk deploy cloud_run \
  --project your-project-id \
  --region us-central1 \
  --service-name my-agent \
  --trace_to_cloud  # ✅ CLI flag

# Or for Agent Engine:
adk deploy agent_engine \
  --project your-project-id \
  --region us-central1 \
  --trace_to_cloud  # ✅ CLI flag
```

**For Agent Engine Python code**:

```python
from vertexai.preview.reasoning_engines import AdkApp

adk_app = AdkApp(
    agent=root_agent,
    enable_tracing=True  # ✅ Correct parameter name
)
```

---

## Additional Findings

### SaveFilesAsArtifactsPlugin API - VERIFIED ✅

**Source**: `/research/adk-python/src/google/adk/plugins/save_files_as_artifacts_plugin.py`

**Correct Usage**:
```python
from google.adk.plugins import SaveFilesAsArtifactsPlugin

plugin = SaveFilesAsArtifactsPlugin(
    name='save_files_as_artifacts_plugin'  # Optional, has default
)

# Plugin automatically saves inline_data blobs as artifacts
# Replaces blobs with text placeholders
# Uses Blob.display_name for filename
```

**Behavior**:
- Intercepts user messages with `inline_data` blobs
- Saves blobs as artifacts via `artifact_service`
- Replaces blob with text placeholder: `[Uploaded Artifact: "filename"]`
- Requires `artifact_service` to be configured

**Conclusion**: ✅ Plugin exists and works as documented (except registration location)

---

## Required Tutorial Fixes

### Fix 1: SaveFilesAsArtifactsPlugin Example

**BEFORE** ❌:
```python
artifact_plugin = SaveFilesAsArtifactsPlugin(
    output_dir='./artifacts',  # ❌ Wrong parameter
    save_all_responses=True    # ❌ Wrong parameter
)

run_config = RunConfig(
    plugins=[artifact_plugin]  # ❌ Wrong location
)

result = await runner.run_async(
    "query",
    agent=agent,
    run_config=run_config  # ❌ Wrong approach
)
```

**AFTER** ✅:
```python
from google.adk.runners import InMemoryRunner
from google.adk.plugins import SaveFilesAsArtifactsPlugin

artifact_plugin = SaveFilesAsArtifactsPlugin()

runner = InMemoryRunner(
    agent=agent,
    app_name='artifact_demo',
    plugins=[artifact_plugin]  # ✅ Correct location
)

session = await runner.session_service.create_session(
    user_id='user',
    app_name='artifact_demo'
)

async for event in runner.run_async(
    user_id='user',
    session_id=session.id,
    new_message=types.Content(
        role='user',
        parts=[types.Part.from_text("Generate a report")]
    )
):
    if event.content and event.content.parts:
        print(event.content.parts[0].text)
```

---

### Fix 2: Cloud Trace Example

**BEFORE** ❌:
```python
run_config = RunConfig(
    trace_to_cloud=True  # ❌ Wrong location
)

result = await runner.run_async(
    "query",
    agent=agent,
    run_config=run_config
)
```

**AFTER** ✅:
```markdown
## Cloud Trace Integration

Cloud Trace is enabled at **deployment time**, not in local development code.

### For Cloud Run:

\`\`\`bash
adk deploy cloud_run \\
  --project your-project-id \\
  --region us-central1 \\
  --service-name traced-agent \\
  --trace_to_cloud  # Enable tracing
\`\`\`

### For Agent Engine:

\`\`\`python
# In Agent Engine deployment
from vertexai.preview.reasoning_engines import AdkApp

adk_app = AdkApp(
    agent=root_agent,
    enable_tracing=True  # Enable tracing for Agent Engine
)
\`\`\`

### Viewing Traces:

1. Deploy agent with `--trace_to_cloud` flag
2. Visit: https://console.cloud.google.com/traces?project=YOUR_PROJECT
3. Filter by agent name or trace ID
4. Analyze latency, spans, and errors
```

---

### Fix 3: All Plugin Examples

**Search and Replace Pattern**:

1. Find all: `RunConfig(plugins=[...])`
2. Replace with: `InMemoryRunner(agent=..., app_name=..., plugins=[...])`

3. Find all: `runner.run_async(..., run_config=run_config)`
4. Replace with proper async iteration pattern

---

## Plugin System Architecture (VERIFIED)

### Plugin Base Class

**Source**: `/research/adk-python/src/google/adk/plugins/base_plugin.py`

```python
class BasePlugin:
    """Base class for ADK plugins."""
    
    async def on_user_message_callback(self, ...) -> Optional[types.Content]
    async def before_run_callback(self, ...) -> None
    async def after_run_callback(self, ...) -> None
    async def on_event_callback(self, ...) -> None
    async def before_agent_callback(self, ...) -> None
    async def after_agent_callback(self, ...) -> None
    async def before_tool_callback(self, ...) -> None
    async def after_tool_callback(self, ...) -> None
    async def on_tool_error_callback(self, ...) -> None
    async def before_model_callback(self, ...) -> None
    async def after_model_callback(self, ...) -> None
    async def on_model_error_callback(self, ...) -> None
```

**Conclusion**: ✅ Plugin architecture is well-documented in source, tutorial just uses wrong registration API

---

## Impact Assessment

**Severity**: HIGH (Critical API errors)

**Impact**:
- Users following tutorial will get `TypeError` or `ValidationError`
- Plugins will not be loaded
- Tracing configuration will be ignored
- Complete failure of all plugin examples

**User Experience**:
```python
# User follows tutorial
run_config = RunConfig(plugins=[plugin])

# Error:
pydantic.error_wrappers.ValidationError: 1 validation error for RunConfig
plugins
  extra fields not permitted (type=value_error.extra)
```

---

## Files to Modify

1. **Tutorial 24**: `/docs/tutorial/24_advanced_observability.md`
   - Fix all `RunConfig(plugins=[...])` → `InMemoryRunner(..., plugins=[...])`
   - Fix all `RunConfig(trace_to_cloud=True)` → Document CLI flags instead
   - Update SaveFilesAsArtifactsPlugin parameters
   - Fix all `runner.run_async()` calls to use proper async iteration
   - Add verification info box with correct API

---

## Summary

| Issue | Tutorial Shows | Actual API | Severity |
|-------|----------------|------------|----------|
| Plugin Registration | `RunConfig(plugins=[])` | `Runner(plugins=[])` or `App(plugins=[])` | CRITICAL |
| trace_to_cloud | `RunConfig(trace_to_cloud=True)` | CLI flag `--trace_to_cloud` or `AdkApp(enable_tracing=True)` | CRITICAL |
| SaveFilesAsArtifactsPlugin params | `output_dir=`, `save_all_responses=` | `name=` (optional, only param) | HIGH |

---

## Next Steps

1. ❌ Tutorial 24 requires CRITICAL fixes
2. ⏸️ Pause verification to fix Tutorial 24
3. 📝 Create fixed version of Tutorial 24
4. ✅ After fix, continue with Tutorial 25

---

**Verification Completed**: January 13, 2025, 21:20:00  
**Verified By**: AI Agent  
**Verification Method**: Direct source code inspection + official samples  
**Status**: CRITICAL FIXES REQUIRED
