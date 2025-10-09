# Tutorial 11: Built-in Tools & Grounding - Grounding Agent

**Tutorial Link**: [Tutorial 11: Built-in Tools & Grounding](../tutorial/11_built_in_tools_grounding.md)

This implementation demonstrates web grounding capabilities using Google Search and other built-in ADK tools for accessing current information.

## 🚀 Quick Start

```bash
# Install dependencies
make setup

# Start the agent
make dev
```

Then open `http://localhost:8000` and select `research_assistant` from the dropdown.

## 📋 What This Agent Does

This grounding agent provides three different agent configurations:

### 1. Basic Grounding Agent

- Uses `google_search` tool directly
- Simple web search capabilities
- Best for basic current information queries

### 2. Advanced Grounding Agent

- Combines search with custom analysis tools
- Demonstrates tool composition patterns
- Multi-step research workflows

### 3. Research Assistant (Default)

- Production-ready research agent
- Multi-step research workflow
- Search → Analyze → Save pattern
- Comprehensive research capabilities

## 🔍 Try These Queries

```bash
"What are the latest developments in AI for 2025?"
"Research quantum computing breakthroughs"
"Find current information about renewable energy trends"
"Analyze recent developments in space exploration"
```

## 🛠️ Available Tools

### Built-in ADK Tools

- **`google_search`**: Web grounding for current information (Gemini 2.0+ only)

### Custom Tools

- **`analyze_search_results`**: Processes and analyzes search content
- **`save_research_findings`**: Saves research as artifacts

## 🔧 Setup & Installation

### Prerequisites

- Python 3.9+
- Google Cloud Project (for VertexAI) OR Gemini API key

### Authentication Options

#### Option 1: Gemini API (Free)

```bash
export GOOGLE_API_KEY=your_api_key_here
# Get key at: https://aistudio.google.com/app/apikey
```

#### Option 2: VertexAI (Production)

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
export GOOGLE_CLOUD_PROJECT=your_project_id
export GOOGLE_CLOUD_LOCATION=us-central1
```

### Installation

```bash
# Clone and navigate to tutorial
cd tutorial_implementation/tutorial11

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Copy environment template
cp grounding_agent/.env.example grounding_agent/.env
# Edit .env with your API keys
```

## 🧪 Testing

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# View coverage report in htmlcov/
```

## 📁 Project Structure

```
tutorial11/
├── grounding_agent/           # Agent implementation
│   ├── __init__.py           # Package marker
│   ├── agent.py              # Agent definitions & tools
│   └── .env.example          # Environment template
├── tests/                    # Test suite
│   ├── __init__.py
│   └── test_agent.py         # Comprehensive tests
├── requirements.txt          # Python dependencies
├── pyproject.toml           # Package configuration
├── setup.py                 # Installation script
├── Makefile                 # Development commands
└── README.md                # This file
```

## 🎯 Key Features Demonstrated

### Web Grounding
- Real-time web search integration
- Current information access
- Source citation and verification

### Tool Composition
- Mixing built-in and custom tools
- Multi-step research workflows

### Production Patterns
- Error handling and validation
- Structured tool responses
- Research documentation and saving

## 🔍 Understanding the Code

### Agent Hierarchy

```python
# Basic: Direct google_search usage
basic_grounding_agent = Agent(
    tools=[google_search]  # Direct built-in tool
)

# Advanced: Tool mixing with custom tools
advanced_grounding_agent = Agent(
    tools=[google_search, custom_tool1, custom_tool2]
)

# Research: Production-ready with full workflow
research_assistant = Agent(
    tools=[google_search, analyze_tool, save_tool],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.3  # Factual research
    )
)
```

### Tool Implementation

```python
def analyze_search_results(query: str, content: str) -> Dict[str, Any]:
    """Analyze search results and extract insights."""
    # Process content, count words, extract key points
    return {
        'status': 'success',
        'analysis': {...},
        'report': 'Analysis complete'
    }

def save_research_findings(topic: str, findings: str) -> Dict[str, Any]:
    """Save research as artifact."""
    # Create document and save
    return {
        'status': 'success',
        'filename': 'research_topic.md'
    }
```

## 🚨 Important Notes

### Model Requirements
- **Gemini 2.0+ required** for `google_search` tool
- Older models (1.5, 1.0) will raise errors
- Use `gemini-2.0-flash` for best performance/cost balance

### Tool Limitations
- Built-in tools cannot be mixed directly with custom tools
- Use separate agents for different tool combinations

### Security
- Never commit `.env` files with real API keys
- Use `.env.example` as template
- Rotate keys regularly in production

## 🐛 Troubleshooting

### "google_search requires Gemini 2.0+"
```bash
# Fix: Use correct model
agent = Agent(model='gemini-2.0-flash', tools=[google_search])
```

### Authentication Errors
```bash
# Check your .env file or environment variables
# Ensure GOOGLE_API_KEY or GOOGLE_APPLICATION_CREDENTIALS is set
```

## 📚 Learn More

- **Tutorial**: [Tutorial 11: Built-in Tools & Grounding](../tutorial/11_built_in_tools_grounding.md)
- **ADK Docs**: [Built-in Tools](https://google.github.io/adk-docs/tools/built-in-tools/)
- **Grounding**: [Web Grounding Enterprise](https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/web-grounding-enterprise)

## 🤝 Contributing

This is part of the ADK Training repository. See the main [README](../../README.md) for contribution guidelines.

---

**🎉 Happy Grounding!** Your agent can now access current web information and perform comprehensive research.
