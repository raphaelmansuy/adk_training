# Interactions API Basic Example

This example demonstrates the fundamental capabilities of Google's Interactions API for building stateful conversations with Gemini models.

## Features

- Basic text interactions with Gemini models
- Server-side state management with `previous_interaction_id`
- Streaming responses for real-time output
- Function calling with tools
- Built-in tools (Google Search, Code Execution)

## Prerequisites

```bash
# Install dependencies
make setup

# Set your API key
export GOOGLE_API_KEY="your-api-key-here"
```

## Quick Start

```bash
# Run tests to validate setup
make test

# Run interactive demo
make demo

# See all available commands
make help
```

## Examples

### Basic Interaction

```python
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-2.5-flash",
    input="Tell me a short joke about programming."
)

print(interaction.outputs[-1].text)
```

### Stateful Conversation

```python
# First turn
interaction1 = client.interactions.create(
    model="gemini-2.5-flash",
    input="My favorite color is blue."
)

# Second turn - context preserved!
interaction2 = client.interactions.create(
    model="gemini-2.5-flash",
    input="What is my favorite color?",
    previous_interaction_id=interaction1.id
)
# Output: "Your favorite color is blue."
```

### Streaming

```python
stream = client.interactions.create(
    model="gemini-2.5-flash",
    input="Explain quantum entanglement simply.",
    stream=True
)

for chunk in stream:
    if chunk.event_type == "content.delta":
        print(chunk.delta.text, end="", flush=True)
```

### Function Calling

```python
weather_tool = {
    "type": "function",
    "name": "get_weather",
    "description": "Gets weather for a location",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {"type": "string"}
        },
        "required": ["location"]
    }
}

interaction = client.interactions.create(
    model="gemini-2.5-flash",
    input="What's the weather in Paris?",
    tools=[weather_tool]
)
```

## Project Structure

```
interactions_api_basic/
├── Makefile                    # Build and run commands
├── README.md                   # This file
├── pyproject.toml             # Project configuration
├── requirements.txt           # Dependencies
├── interactions_basic_agent/  # Main agent module
│   ├── __init__.py
│   ├── agent.py               # Agent implementation
│   ├── tools.py               # Tool definitions
│   └── .env.example           # Environment template
└── tests/                     # Test suite
    ├── test_agent.py          # Agent tests
    ├── test_imports.py        # Import tests
    └── test_interactions.py   # Interactions API tests
```

## Running Tests

```bash
# Run all tests
make test

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_interactions.py -v
```

## Learn More

- [Interactions API Documentation](https://ai.google.dev/gemini-api/docs/interactions)
- [Blog Post: Mastering Interactions API](/blog/interactions-api-deep-research)
- [Google AI Studio](https://aistudio.google.com/apikey)
