# TIL: Context Compaction with Google ADK 1.16

Demonstration of ADK 1.16's new **Context Compaction** feature for automatically
summarizing conversation history to reduce token usage in long agent conversations.

## Quick Start

```bash
# 1. Install dependencies
make setup

# 2. Add your API key
# Edit context_compaction_agent/.env and add GOOGLE_API_KEY

# 3. Try the agent
make dev
# Opens http://localhost:8000 - select 'context_compaction_agent'

# 4. Run tests
make test
```

## What's Included

- **`context_compaction_agent/`** - Main agent implementation
  - `agent.py` - Agent with tools for text summarization and complexity analysis
  - `.env.example` - Environment configuration template
- **`app.py`** - ADK App configuration with EventsCompactionConfig enabled
- **`tests/`** - Comprehensive test suite (unit tests)
- **`Makefile`** - Standard development commands
- **`requirements.txt`** - Dependencies

## File Structure

```text
til_context_compaction_20250119/
├── context_compaction_agent/
│   ├── __init__.py        # Package initialization
│   ├── agent.py           # Agent definition with root_agent export
│   └── .env.example       # Environment template
├── tests/
│   ├── __init__.py
│   └── test_agent.py      # 16 comprehensive tests
├── app.py                 # App config with EventsCompactionConfig
├── pyproject.toml         # Project metadata
├── Makefile              # Development commands
├── requirements.txt      # Dependencies
└── README.md             # This file
```

## How Context Compaction Works

Context Compaction automatically:

1. **Detects long conversations** - After N interactions (configurable)
2. **Summarizes old events** - Uses LLM to create intelligent summaries
3. **Maintains context** - Keeps overlap between summaries for continuity
4. **Reduces tokens** - Old events replaced with compact summaries

### Example Configuration

```python
from google.adk.apps.compaction import EventsCompactionConfig

config = EventsCompactionConfig(
    # Compact every 5 new user interactions
    compaction_invocation_threshold=5,
    # Keep 1 previous interaction for context overlap
    overlap_size=1,
)

app = App(root_agent=agent, events_compaction_config=config)
```

## The Agent

This implementation includes an agent with two tools:

### 1. `summarize_text(text: str)`

Demonstrates text summarization capability used in compaction:

```python
result = summarize_text("Long text...")
# Returns: {"status": "success", "report": "...", "summary": "..."}
```

### 2. `calculate_complexity(question: str)`

Analyzes question complexity to understand conversation depth:

```python
result = calculate_complexity("What is context compaction?")
# Returns: {
#     "status": "success",
#     "complexity_level": "medium",
#     "word_count": 4
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
- ✅ EventsCompactionConfig setup

## Using in Development

### Watch Events Tab

When running `make dev`, open the Events tab to see compaction in action:

1. Have a multi-turn conversation (5+ exchanges)
2. Watch for `EventCompaction` events
3. See how old events are summarized

### Try These Prompts

```
1. "Explain context compaction in simple terms"
   (triggers complexity analysis tool)

2. "Tell me about long conversations in AI agents"
   (tests conversation handling)

3. Continue with follow-ups to trigger compaction
```

## Key Parameters

| `compaction_invocation_threshold` | int | 5 | Trigger compaction |
| `overlap_size` | int | 1 | Context continuity |
| `compactor` | optional | Auto | Custom summarizer |

## Adjusting Parameters

**For aggressive compaction** (lower costs, less context):

```python
EventsCompactionConfig(
    compaction_invocation_threshold=3,  # Compact more often
    overlap_size=0,                     # No overlap
)
```

**For conservative compaction** (higher costs, more context):

```python
EventsCompactionConfig(
    compaction_invocation_threshold=10,  # Compact less often
    overlap_size=3,                      # More overlap
)
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
cp context_compaction_agent/.env.example context_compaction_agent/.env
# Add your GOOGLE_API_KEY to context_compaction_agent/.env
```

## Related Learning

- **[TIL Article](../../docs/til/til_context_compaction_20250119.md)** - Full
  explanation and best practices
- **[Tutorial 08](../../docs/tutorial/08_state_memory.md)** - Broader memory
  management patterns
- **[ADK Docs](https://google.github.io/adk-docs/)** - Official documentation

## Extending This Example

Try these modifications:

1. **Custom summarizer** - Implement custom `LlmEventSummarizer`
2. **Different thresholds** - Test with different compaction_invocation_threshold
3. **Token tracking** - Log token usage before/after compaction
4. **Multi-tool agent** - Add more tools that trigger different compaction behaviors

## Notes

- Context Compaction requires ADK 1.16+
- Compaction happens automatically - transparent to agent logic
- Summaries preserve key information while reducing tokens
- Perfect for production agents with long-running conversations

## Next Steps

1. ✅ Run `make setup` to prepare environment
2. ✅ Add your API key to `.env`
3. ✅ Run `make test` to validate setup
4. ✅ Run `make dev` to try the agent
5. ✅ Modify parameters and observe behavior
6. ✅ Integrate into your own projects

---

**Questions?** See the full [Context Compaction TIL
Article](../../docs/til/til_context_compaction_20250119.md)!
