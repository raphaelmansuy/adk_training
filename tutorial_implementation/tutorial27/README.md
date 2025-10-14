# Tutorial 27: Third-Party Tools Integration

**Learn how to integrate third-party framework tools (LangChain, CrewAI) into ADK agents**

## Overview

This tutorial demonstrates how to integrate tools from popular AI frameworks into Google ADK agents. The implementation uses LangChain's Wikipedia tool as a working example that requires no API keys.

### What You'll Learn

- ✅ How to use `LangchainTool` wrapper for LangChain tools
- ✅ Proper import paths (`google.adk.tools.langchain_tool`)
- ✅ Tool wrapping and agent configuration
- ✅ Working with third-party tool ecosystems
- ✅ Best practices for tool integration

### Key Features

- **Wikipedia Integration**: Search Wikipedia through LangChain
- **No API Keys Required**: Works out of the box with public APIs
- **Production-Ready**: Proper error handling and testing
- **Well-Documented**: Comprehensive code comments and examples

## Quick Start

### 1. Setup

```bash
# Install dependencies
make setup

# Set up authentication (choose one method)
export GOOGLE_API_KEY=your_api_key_here  # Get from https://aistudio.google.com/app/apikey
```

### 2. Run the Agent

```bash
# Start ADK web interface
make dev
```

Open http://localhost:8000 and select `third_party_agent` from the dropdown.

### 3. Try It Out

Ask the agent questions like:
- "What is quantum computing?"
- "Tell me about Ada Lovelace"
- "Explain the theory of relativity"
- "What is machine learning?"

## Project Structure

```
tutorial27/
├── third_party_agent/          # Agent implementation
│   ├── __init__.py
│   └── agent.py               # Main agent with Wikipedia tool
├── tests/                     # Test suite
│   └── test_agent.py         # Agent configuration tests
├── Makefile                  # Development commands
├── README.md                 # This file
├── pyproject.toml           # Package configuration
└── requirements.txt         # Dependencies
```

## Implementation Details

### Agent Configuration

The agent uses LangChain's Wikipedia tool wrapped with `LangchainTool`:

```python
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# Create Wikipedia tool
wikipedia = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(
        top_k_results=3,
        doc_content_chars_max=4000
    )
)

# Wrap for ADK
wiki_tool = LangchainTool(tool=wikipedia)

# Use in agent
agent = Agent(
    model='gemini-2.0-flash',
    tools=[wiki_tool]
)
```

### Critical Import Paths

✅ **CORRECT**:
```python
from google.adk.tools.langchain_tool import LangchainTool
from google.adk.tools.crewai_tool import CrewaiTool
```

❌ **WRONG**:
```python
from google.adk.tools.third_party import ...  # Module doesn't exist
```

## Available Commands

| Command | Description |
|---------|-------------|
| `make setup` | Install all dependencies |
| `make dev` | Start the agent in web interface |
| `make test` | Run test suite |
| `make demo` | Show example queries |
| `make clean` | Clean up cache files |

## Testing

Run the comprehensive test suite:

```bash
make test
```

Tests cover:
- Agent configuration
- Tool registration
- Import validation
- LangChain integration
- Wikipedia tool functionality

## Extending the Implementation

### Adding More LangChain Tools

See the tutorial documentation for examples of:
- **Tavily Search**: Web search optimized for AI (requires API key)
- **Serper Search**: Google search API (requires API key)
- **Python REPL**: Execute Python code
- **ArXiv**: Search research papers

Example with Tavily (requires `TAVILY_API_KEY`):

```python
from langchain_community.tools.tavily_search import TavilySearchResults

tavily_tool = TavilySearchResults(max_results=5)
tavily_adk = LangchainTool(tool=tavily_tool)
```

### Adding CrewAI Tools

CrewAI tools require `name` and `description`:

```python
from google.adk.tools.crewai_tool import CrewaiTool
from crewai_tools import SerperDevTool

serper_tool = SerperDevTool()
serper_adk = CrewaiTool(
    tool=serper_tool,
    name='serper_search',
    description='Search Google for current information'
)
```

## Environment Variables

### Required
- `GOOGLE_API_KEY` or `GOOGLE_APPLICATION_CREDENTIALS`

### Optional (for other tools)
- `TAVILY_API_KEY` - For Tavily search tool
- `SERPER_API_KEY` - For Serper/Google search
- `OPENWEATHERMAP_API_KEY` - For weather data
- `WOLFRAM_ALPHA_APPID` - For computational queries

## Troubleshooting

### "ModuleNotFoundError: No module named 'langchain_community'"

```bash
pip install langchain-community
```

### "ModuleNotFoundError: No module named 'wikipedia'"

```bash
pip install wikipedia
```

### "Rate limit exceeded"

Wikipedia API has rate limits. Add delays between requests if needed:

```python
import time
time.sleep(1)  # Between searches
```

### Agent doesn't appear in dropdown

Make sure you've installed the package:

```bash
pip install -e .
```

## Key Concepts

### Tool Wrapping

Third-party tools must be wrapped before use in ADK:

```python
# LangChain tools
langchain_tool = LangchainTool(tool=your_langchain_tool)

# CrewAI tools (require name and description)
crewai_tool = CrewaiTool(
    tool=your_crewai_tool,
    name='tool_name',
    description='What it does'
)
```

### Tool Selection

The LLM automatically selects and uses tools based on user queries. No explicit routing needed.

### Error Handling

Third-party tools may fail. The agent handles errors gracefully and provides helpful feedback.

## Resources

- [Tutorial Documentation](../../docs/tutorial/27_third_party_tools.md)
- [LangChain Tools](https://python.langchain.com/docs/integrations/tools/)
- [CrewAI Tools](https://docs.crewai.com/tools/)
- [ADK Third-Party Tools](https://google.github.io/adk-docs/tools/third-party-tools/)

## Next Steps

- **Tutorial 28**: Use other LLMs with LiteLLM
- **Tutorial 26**: Deploy to Google AgentSpace
- **Tutorial 19**: Artifacts & File Management
- **Tutorial 18**: Events & Observability

## License

Part of the ADK Training repository.
