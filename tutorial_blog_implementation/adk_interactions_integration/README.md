# ADK with Interactions API Integration

This example demonstrates how to integrate Google's Interactions API with the Agent Development Kit (ADK) for enhanced agentic workflows.

## Features

- ADK agents powered by Interactions API backend
- Server-side state management
- Background execution support
- Tool orchestration with ADK patterns
- Deep Research delegation

## Prerequisites

```bash
# Install dependencies
make setup

# Set your API key
export GOOGLE_API_KEY="your-api-key-here"
```

## Quick Start

```bash
# Run tests
make test

# Start ADK web interface
make dev

# Run demo
make demo
```

## Key Integration Patterns

### Pattern 1: ADK Agent with Interactions Backend

Enable Interactions API for your ADK agent:

```python
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini

root_agent = Agent(
    model=Gemini(
        model="gemini-2.5-flash",
        use_interactions_api=True  # Enable Interactions API!
    ),
    name="interactions_agent",
    description="An agent powered by the Interactions API",
    instruction="You are a helpful assistant.",
    tools=[my_tool],
)
```

### Pattern 2: Delegating to Deep Research

Create an agent that can delegate complex research:

```python
def research_topic(topic: str) -> dict:
    """Delegate research to Deep Research Agent."""
    from google import genai
    
    client = genai.Client()
    interaction = client.interactions.create(
        input=f"Research: {topic}",
        agent="deep-research-pro-preview-12-2025",
        background=True
    )
    
    # Poll for completion
    while interaction.status != "completed":
        interaction = client.interactions.get(interaction.id)
        time.sleep(10)
    
    return {
        "status": "success",
        "report": interaction.outputs[-1].text
    }

# ADK agent with research capability
agent = Agent(
    model="gemini-2.5-flash",
    tools=[research_topic],
    instruction="Use research_topic for complex research questions."
)
```

### Benefits

1. **Automatic State Management**: ADK handles `previous_interaction_id`
2. **Background Tasks**: Long-running agents don't timeout
3. **Native Thought Handling**: Access to model reasoning
4. **Unified Tools**: Same tools across models and agents

## Project Structure

```
adk_interactions_integration/
├── Makefile                    # Build and run commands
├── README.md                   # This file
├── pyproject.toml             # Project configuration
├── requirements.txt           # Dependencies
├── adk_interactions_agent/    # Main agent module
│   ├── __init__.py
│   ├── agent.py               # ADK agent implementation
│   ├── tools.py               # Tool definitions
│   └── .env.example           # Environment template
└── tests/                     # Test suite
    └── test_agent.py          # Agent tests
```

## Learn More

- [ADK Documentation](https://google.github.io/adk-docs/)
- [Interactions API Docs](https://ai.google.dev/gemini-api/docs/interactions)
- [Blog Post: Mastering Interactions API](/blog/interactions-api-deep-research)
