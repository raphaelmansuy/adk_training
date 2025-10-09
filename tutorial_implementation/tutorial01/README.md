# Tutorial 01: Hello World Agent

Your first ADK agent - a friendly conversational assistant powered by Gemini 2.0 Flash.

## 🚀 Quick Start

```bash
# Install dependencies
make setup

# Start the agent
make dev

# Open http://localhost:8000 and select 'hello_agent'
```

## 💬 What It Does

- Greets users warmly
- Introduces itself and capabilities
- Shares fun facts
- Conversational chat assistant

## 📁 Project Structure

```
tutorial01/
├── hello_agent/           # Agent implementation
│   ├── __init__.py        # Package marker
│   ├── agent.py           # Agent definition
│   └── .env.example       # API key template
├── tests/                 # Test suite
├── requirements.txt       # Dependencies
└── Makefile              # Build commands
```

## 🔧 Setup

1. **Get API Key**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. **Install**: `make setup`
3. **Configure**: Copy `.env.example` to `.env` and add your API key
4. **Run**: `make dev`

## 🧪 Testing

```bash
make test    # Run all tests
make demo    # See demo prompts
```

## 🎯 Try These Prompts

- "Hello! Who are you?"
- "What can you do?"
- "Tell me a fun fact"

## 📚 Next Steps

- **Tutorial 02**: Function tools for calculations
- **Tutorial 03**: External API integration
- **Tutorial 04**: Sequential workflows

Built with ❤️ using Google ADK.
