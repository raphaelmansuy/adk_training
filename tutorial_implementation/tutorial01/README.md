# Tutorial 01: Hello World Agent Implementation

A complete, working implementation of the Hello World Agent from Tutorial 01. This is your first ADK agent - a simple conversational assistant powered by Gemini.

## Quick Start

```bash
# Clone and setup
make setup

# Run the agent in development mode
make dev

# Run tests
make test

# Clean up
make clean
```

## What This Agent Does

- **Conversational AI**: Friendly chat assistant powered by Gemini 2.0 Flash
- **No Tools**: Pure conversation (tools added in Tutorial 02)
- **Dev UI Ready**: Full integration with ADK's development interface

## Project Structure

```
tutorial01/
├── README.md              # This file
├── Makefile               # Build and test commands
├── hello_agent/           # Agent implementation
│   ├── __init__.py        # Python package marker
│   ├── agent.py           # Agent definition
│   └── .env.example       # Environment template
├── tests/                 # Comprehensive test suite
│   ├── __init__.py
│   ├── test_agent.py      # Agent functionality tests
│   ├── test_imports.py    # Import validation tests
│   └── test_structure.py  # Project structure tests
└── requirements.txt       # Python dependencies
```

## Prerequisites

- Python 3.9+
- Google API key (get free at [Google AI Studio](https://aistudio.google.com/app/apikey))

## Setup Instructions

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API key**:

   ```bash
   cp hello_agent/.env.example hello_agent/.env
   # Edit hello_agent/.env and add your GOOGLE_API_KEY
   ```

3. **Run the agent**:

   ```bash
   make dev
   ```

   Then open <http://localhost:8000> in your browser

## Testing

Run the comprehensive test suite:

```bash
make test
```

Tests cover:

- Agent imports correctly
- Project structure is valid
- Agent configuration is proper
- Authentication setup works
- Basic functionality (when API key available)

## Development Commands

| Command | Description |
|---------|-------------|
| `make setup` | Install dependencies and setup environment |
| `make dev` | Start ADK development server |
| `make test` | Run all tests |
| `make test-unit` | Run unit tests only |
| `make test-integration` | Run integration tests |
| `make clean` | Remove generated files |
| `make help` | Show all available commands |

## Key Features Demonstrated

- **Modern Agent Class**: Uses current ADK `Agent` class (not deprecated `LlmAgent`)
- **Canonical Structure**: Proper `__init__.py`, `agent.py`, `.env` layout
- **Authentication**: Secure API key management via environment variables
- **Dev UI Integration**: Full compatibility with `adk web` interface
- **Best Practices**: Production-ready patterns from day one

## Expected Behavior

```
You: Hello!
Agent: Hello! It's wonderful to meet you! How can I assist you today?

You: What can you do?
Agent: I'm here to chat and help with general questions! I can provide
       information, have conversations, or just be a friendly companion.
       What would you like to talk about?
```

## Troubleshooting

### Agent not found in dropdown

- Run `adk web` from the tutorial01/ directory (parent of hello_agent/)

### Authentication error

- Verify GOOGLE_API_KEY in hello_agent/.env
- Ensure GOOGLE_GENAI_USE_VERTEXAI=FALSE

### Module not found

- Check `__init__.py` contains `from . import agent`

## Next Steps

- **Tutorial 02**: Add function tools for calculations and data processing
- **Tutorial 03**: Integrate external APIs via OpenAPI
- **Tutorial 04**: Build sequential workflows

## Files Overview

- **`hello_agent/agent.py`**: Core agent definition with Gemini 2.0 Flash
- **`hello_agent/__init__.py`**: Package initialization
- **`hello_agent/.env.example`**: Template for API key configuration
- **`tests/test_agent.py`**: Validates agent creation and configuration
- **`tests/test_imports.py`**: Ensures all imports work correctly
- **`tests/test_structure.py`**: Verifies project structure compliance

Built with ❤️ using Google ADK. Ready for production!

