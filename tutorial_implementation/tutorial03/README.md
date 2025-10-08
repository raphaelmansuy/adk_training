# Tutorial 03: Chuck Norris OpenAPI Tools Agent

A fun agent that demonstrates OpenAPIToolset usage with the Chuck Norris API. This agent can retrieve jokes, search for specific topics, and list available categories using automatically generated API tools.

## 🚀 Quick Start

```bash
# Install dependencies
make setup

# Start the agent
make dev

# Open http://localhost:8000 and select 'chuck_norris_agent'
```

## 💬 What It Does

- **Random Jokes**: Get random Chuck Norris facts
- **Category Filtering**: Get jokes from specific categories (dev, movie, food, etc.)
- **Search Functionality**: Find jokes containing specific keywords
- **Category Listing**: See all available joke categories

## 📁 Project Structure

```text
tutorial03/
├── chuck_norris_agent/        # Agent implementation
│   ├── __init__.py           # Package marker
│   ├── agent.py              # Agent with OpenAPI spec & tools
│   └── .env.example          # Environment template
├── tests/                    # Comprehensive test suite
├── requirements.txt          # Dependencies
└── Makefile                 # Build commands
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

- "Tell me a random Chuck Norris joke"
- "Find jokes about programming"
- "What categories are available?"
- "Give me a random dev joke"
- "Search for jokes with the word 'code'"

## 🔧 How It Works

This agent uses **OpenAPIToolset** to automatically generate tools from the Chuck Norris API OpenAPI specification. No manual tool functions needed!

**Auto-generated tools:**

- `get_random_joke(category=None)` - Get random joke, optionally by category
- `search_jokes(query)` - Search for jokes containing keywords
- `get_categories()` - List all available categories

## 📚 Next Steps

- **Tutorial 04**: Sequential workflows
- **Tutorial 05**: Parallel processing
- **Tutorial 06**: Multi-agent systems

Built with ❤️ using Google ADK and the [Chuck Norris API](https://api.chucknorris.io/).
