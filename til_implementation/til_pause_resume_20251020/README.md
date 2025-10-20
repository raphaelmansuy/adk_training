# TIL: Pause and Resume Invocations with Google ADK 1.16.0

Demonstration of ADK 1.16.0's new **Pause and Resume Invocation** feature for building
resilient, long-running agent workflows with automatic state checkpointing and resumption support.

## Quick Start

```bash
# 1. Install dependencies
make setup

# 2. Add your API key
# Edit pause_resume_agent/.env and add GOOGLE_API_KEY

# 3. Try the agent
make dev
# Opens http://localhost:8000 - select 'pause_resume_agent'

# 4. Run tests
make test
```

## What's Included

- **`pause_resume_agent/`** - Main agent implementation
  - `agent.py` - Agent with tools for data processing, checkpoint validation, and resumption hints
  - `.env.example` - Environment configuration template
- **`app.py`** - ADK App configuration with ResumabilityConfig enabled
- **`tests/`** - Comprehensive test suite (unit tests)
- **`Makefile`** - Standard development commands
- **`requirements.txt`** - Dependencies

## File Structure

```text
til_pause_resume_20251020/
├── pause_resume_agent/
│   ├── __init__.py        # Package initialization
│   ├── agent.py           # Agent definition with root_agent export
│   └── .env.example       # Environment template
├── tests/
│   ├── __init__.py
│   └── test_agent.py      # Comprehensive tests
├── app.py                 # App config with ResumabilityConfig
├── pyproject.toml         # Project metadata
├── Makefile              # Development commands
├── requirements.txt      # Dependencies
└── README.md             # This file
```

## How Pause/Resume Invocations Work

Pause/Resume Invocations enable:

1. **Agent State Checkpointing** - Agents automatically save their state at key points
2. **Invocation Pausing** - Long-running operations can be paused gracefully
3. **State Restoration** - Previous state is restored when resuming
4. **Fault Tolerance** - If execution is interrupted, state is preserved
5. **Human-in-the-Loop** - Agents can pause to request human input, then resume

### State Checkpoint Architecture

```
Invocation Flow:
================

Initial Request
    ↓
[Agent Processing]
    ↓
Checkpoint Reached
(end_of_agent=True)
    ↓
State Serialized
    ↓
Event Emitted with
agent_state field
    ↓
[PAUSE] - Can Save Here
    ↓
[LATER] Resume Request
    ↓
State Restored from
Previous Checkpoint
    ↓
Execution Continues
    ↓
[Agent Processing]
    ↓
Completion
```

### Example Configuration

```python
from google.adk.apps import App, ResumabilityConfig

# Enable pause/resume support
config = ResumabilityConfig(is_resumable=True)

app = App(
    root_agent=agent,
    resumability_config=config
)
```

## The Agent

This implementation includes an agent with three tools demonstrating long-running workflows:

### 1. `process_data_chunk(data: str)`

Simulates processing data chunks (represents long operations):

```python
result = process_data_chunk("Sample data...")
# Returns: {
#     "status": "success",
#     "lines_processed": 5,
#     "word_count": 42,
#     "data_summary": "..."
# }
```

### 2. `validate_checkpoint(checkpoint_data: str)`

Validates checkpoint integrity before resuming:

```python
result = validate_checkpoint(checkpoint_state)
# Returns: {
#     "status": "success",
#     "is_valid": True,
#     "checkpoint_size": 256
# }
```

### 3. `get_resumption_hint(context: str)`

Analyzes context and suggests best resumption point:

```python
result = get_resumption_hint("processing data")
# Returns: {
#     "status": "success",
#     "hint": "Consider resuming from the data processing stage",
#     "context_length": 18
# }
```

## Testing

Run all tests:

```bash
make test
```

Or run specific test class:

```bash
pytest tests/test_agent.py::TestAgentConfiguration -v
```

**Test Coverage:**

- ✅ Agent configuration (name, model, description, instruction)
- ✅ Tools availability and functionality
- ✅ Import validation
- ✅ App configuration
- ✅ ResumabilityConfig setup

## Using in Development

### Watch Events Tab

When running `make dev`, check the Events tab to see pause/resume in action:

1. Send a message that triggers data processing
2. Watch for checkpoint events with `end_of_agent=True`
3. Check for `agent_state` field in events
4. See state preservation markers

### Try These Prompts

```
1. "Process this data: Hello world, this is a test"
   (triggers data processing checkpoint)

2. "Can you validate this checkpoint?"
   (triggers validation tool)

3. "What checkpoint should I use for processing?"
   (gets resumption hints)

4. Continue with follow-ups to observe state handling
```

## Key Features

### Agent State Checkpointing

```python
# Agent emits checkpoint event
Event(
    invocation_id='inv_1',
    author='pause_resume_agent',
    actions=EventActions(
        end_of_agent=True,
        agent_state={'processing': True}  # State saved
    ),
    content="Processing complete"
)
```

### Resuming Invocations

```python
# Resume from saved state
await runner.run_async(
    session=session,
    new_message=next_user_input,
    invocation_id=previous_invocation_id,  # Restores state
)
```

## Use Cases

### 1. Long-Running Workflows

Process large datasets or complex tasks over extended periods:

```
Initial Request → Process Phase 1 → [CHECKPOINT]
[Pause - Save state]
[Later] Resume → Process Phase 2 → [CHECKPOINT]
[Pause - Save state]
[Later] Resume → Finalize → Complete
```

### 2. Human-in-the-Loop

Agent pauses to request feedback, then resumes:

```
Agent Processing → [CHECKPOINT]
↓
Await Human Input
↓
Human Provides Feedback
↓
Resume with Feedback → Complete
```

### 3. Fault Tolerance

System failure doesn't lose progress:

```
Agent Processing
↓
[CHECKPOINT] - State saved
↓
[SYSTEM FAILURE]
↓
[RECOVERY] - State restored
↓
Resume from checkpoint → Complete
```

### 4. Multi-Stage Operations

Sequential agent workflows with natural pause points:

```
✅ Data Validation [CHECKPOINT 1]
↓
✅ Processing [CHECKPOINT 2]
↓
✅ Analysis [CHECKPOINT 3]
↓
✅ Results Generation [CHECKPOINT 4]
↓
Done
```

## Adjusting Configuration

The default configuration works for most use cases:

```python
# Current default
resumability_config = ResumabilityConfig(is_resumable=True)
```

### Enable Pause/Resume

```python
resumability_config = ResumabilityConfig(is_resumable=True)
```

### Disable Pause/Resume (for backward compatibility)

```python
resumability_config = ResumabilityConfig(is_resumable=False)
# Or omit the config entirely
```

## Troubleshooting

### Agent doesn't load in web UI

```bash
# Reinstall as editable package
pip install -e .
adk web
```

### Tests fail with import errors

```bash
# Reinstall requirements
make setup
```

### Environment file missing

```bash
# Copy the example file
cp pause_resume_agent/.env.example pause_resume_agent/.env
# Add your GOOGLE_API_KEY
```

### Can't see checkpoint events

1. Ensure `ResumabilityConfig(is_resumable=True)` is set in `app.py`
2. Run agent with longer operations to trigger checkpoints
3. Check Events tab during agent execution
4. Look for events with `end_of_agent=True` in event details

## Related Learning

- **[TIL Article](../../til_implementation/20251020_125000_pause_resume_invocation.md)** - Full explanation and best practices
- **[Tutorial 17](../../docs/tutorial/17_agent_to_agent_communication.md)** - Multi-agent workflows
- **[ADK Docs](https://github.com/google/adk-python)** - Official documentation

## Extending This Example

Try these modifications:

1. **Multi-step Workflow** - Chain multiple tools with checkpoints between each
2. **Custom State** - Track additional state in checkpoint data
3. **Error Recovery** - Implement error handling that preserves state
4. **Progress Tracking** - Store progress metrics in checkpoint state
5. **State Analysis** - Log and analyze state transitions

## Implementation Details

### Agent State Structure

```python
from google.adk.agents.base_agent import BaseAgentState

# States are automatically captured at checkpoints
agent_state = {
    'processing_stage': 'data_validation',
    'items_processed': 42,
    'checkpoint_timestamp': '2025-01-20T10:30:00Z'
}
```

### Event Emission with State

```python
# Agent framework automatically handles this
event = Event(
    invocation_id='inv_1',
    author='pause_resume_agent',
    actions=EventActions(
        end_of_agent=True,
        agent_state=agent_state  # Persisted
    ),
    content=response
)
```

### Session Storage

Pause/Resume requires sessions to persist events:

```python
# State is automatically saved in session
session.events.append(checkpoint_event)
# State is automatically restored on resume
invocation_context = await runner._setup_context_for_resumed_invocation(...)
```

## Key Parameters

| Parameter | Type | Default | Purpose |
|-----------|------|---------|---------|
| `is_resumable` | bool | - | Enable pause/resume support |

## Best Practices

1. **Always Configure ResumabilityConfig** - Explicitly set to true for resumable apps
2. **Understand Your Checkpoints** - Know where your agent pauses naturally
3. **Test Resumption** - Test both normal and resumed execution paths
4. **Handle State Errors** - Implement error handling for corrupted state
5. **Clean Up Sessions** - Archive old sessions periodically

## Performance Considerations

- **State Serialization**: JSON-serializable state only
- **Storage**: Session events stored in configured session service
- **Resumption Latency**: State restoration is fast (< 100ms typically)
- **Checkpoint Frequency**: Automatic, based on agent completion points

## Limitations

1. App must explicitly enable resumability via `ResumabilityConfig(is_resumable=True)`
2. State must be JSON-serializable
3. Resumption requires session to have original invocation events
4. Sub-agent resumption has documented limitations (see ADK docs)

## Next Steps

1. ✅ Run `make setup` to prepare environment
2. ✅ Add your API key to `.env`
3. ✅ Run `make test` to validate setup
4. ✅ Run `make dev` to try the agent
5. ✅ Observe checkpoint events in web UI
6. ✅ Modify agent and experiment with checkpoints
7. ✅ Integrate pause/resume into your own projects

## Notes

- Pause/Resume Invocations require ADK 1.16.0+
- Checkpointing is automatic and transparent to agent logic
- State is preserved across restarts and failures
- Perfect for production agents with long-running operations
- Works seamlessly with human-in-the-loop workflows

---

**Questions?** See the full [Pause/Resume Invocations TIL Article](../../til_implementation/20251020_125000_pause_resume_invocation.md)!
