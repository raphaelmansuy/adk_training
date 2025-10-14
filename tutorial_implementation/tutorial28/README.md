# Tutorial 28: Using Other LLMs with LiteLLM

Multi-LLM agent supporting OpenAI, Claude, Ollama, and more via LiteLLM integration.

## 🚀 Quick Start

```bash
# Install dependencies
make setup

# Set API keys
export GOOGLE_API_KEY=your_google_key
export OPENAI_API_KEY=sk-your_openai_key
export ANTHROPIC_API_KEY=sk-ant-your_anthropic_key

# Start the agent
make dev

# Open http://localhost:8000 and select 'multi_llm_agent'
```

## 💡 What It Does

This tutorial demonstrates how to use multiple LLM providers in ADK agents via LiteLLM:

- **OpenAI GPT Models**: GPT-4o and GPT-4o-mini for various tasks
- **Anthropic Claude**: Claude 3.7 Sonnet for detailed analysis
- **Ollama Local Models**: Llama 3.3 for privacy-first operation
- **Azure OpenAI**: Enterprise deployment option
- **Multi-Provider Strategy**: Compare and optimize across providers

## 📁 Project Structure

```
tutorial28/
├── multi_llm_agent/       # Agent implementation
│   ├── __init__.py        # Package initialization
│   ├── agent.py           # Multi-LLM agent definitions
│   └── .env.example       # API key templates
├── tests/                 # Comprehensive test suite
│   ├── test_agent.py      # Agent configuration tests
│   ├── test_imports.py    # Import validation
│   └── test_structure.py  # Project structure tests
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Package configuration
├── Makefile              # Build commands
└── README.md             # This file
```

## 🔧 Setup

### Prerequisites

- Python 3.9+
- Google API key from [AI Studio](https://aistudio.google.com/app/apikey)
- OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- Anthropic API key from [Anthropic Console](https://console.anthropic.com/)
- Optional: [Ollama](https://ollama.com) for local models

### Installation

```bash
# 1. Install dependencies
make setup

# 2. Copy environment template
cp multi_llm_agent/.env.example multi_llm_agent/.env

# 3. Edit .env and add your API keys
# 4. For Ollama: Install Ollama and pull models
ollama pull llama3.3
```

## 🎯 Available Agents

### 1. Root Agent (Default)
- **Model**: OpenAI GPT-4o-mini
- **Best For**: Cost-effective general tasks
- **Usage**: Main agent accessible via `adk web`

### 2. GPT-4o Agent
- **Model**: OpenAI GPT-4o (full version)
- **Best For**: Complex reasoning and coding
- **Cost**: Higher but more capable

### 3. Claude Agent
- **Model**: Anthropic Claude 3.7 Sonnet
- **Best For**: Long-form content, detailed analysis
- **Features**: 200K context window

### 4. Ollama Agent
- **Model**: Llama 3.3 (local)
- **Best For**: Privacy, offline operation, no API costs
- **Requires**: Ollama running locally

## 🧪 Testing

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_agent.py -v

# Run with coverage
pytest tests/ --cov=multi_llm_agent --cov-report=html
```

## 💬 Example Prompts

Try these prompts with the agent:

**Mathematical Operations**:
- "What is the square of 25?"
- "Calculate the square of 144"

**Weather Queries**:
- "What's the weather like in San Francisco?"
- "Get weather for New York"

**Sentiment Analysis**:
- "Analyze the sentiment: 'This product is absolutely amazing!'"
- "What's the sentiment of: 'Disappointed with the service'"

**General Conversation**:
- "Explain how LiteLLM enables multi-model support"
- "Compare OpenAI GPT-4o vs Claude 3.7 Sonnet"
- "What are the benefits of using local models with Ollama?"

## 🔑 API Key Configuration

### Google (Gemini)
```bash
export GOOGLE_API_KEY=your_google_api_key
```

### OpenAI
```bash
export OPENAI_API_KEY=sk-your_openai_key
```

### Anthropic (Claude)
```bash
export ANTHROPIC_API_KEY=sk-ant-your_anthropic_key
```

### Ollama (Local)
```bash
export OLLAMA_API_BASE=http://localhost:11434
```

## 📊 Cost Comparison

| Provider | Model | Input Cost | Output Cost | Best For |
|----------|-------|------------|-------------|----------|
| Google | gemini-2.5-flash | $0.075/1M | $0.30/1M | Cheapest cloud |
| OpenAI | gpt-4o-mini | $0.15/1M | $0.60/1M | Balanced |
| OpenAI | gpt-4o | $2.50/1M | $10/1M | Complex tasks |
| Anthropic | claude-3-7-sonnet | $3/1M | $15/1M | Long content |
| Ollama | llama3.3 (local) | $0 | $0 | Privacy/offline |

## ⚠️ Important Notes

### Use `ollama_chat` for Ollama
```python
# ✅ CORRECT
model = LiteLlm(model='ollama_chat/llama3.3')

# ❌ WRONG
model = LiteLlm(model='ollama/llama3.3')
```

### Don't Use LiteLLM for Gemini
For Gemini models, use native `GoogleGenAI` instead:
```python
# ✅ CORRECT for Gemini
agent = Agent(model='gemini-2.5-flash')

# ❌ DON'T DO THIS
agent = Agent(model=LiteLlm(model='gemini/gemini-2.5-flash'))
```

## 🛠️ Switching Models

To use a different model, modify the agent configuration:

```python
from google.adk.models import LiteLlm
from multi_llm_agent.agent import root_agent

# Switch to GPT-4o
root_agent.model = LiteLlm(model='openai/gpt-4o')

# Switch to Claude
root_agent.model = LiteLlm(model='anthropic/claude-3-7-sonnet-20250219')

# Switch to local Ollama
root_agent.model = LiteLlm(model='ollama_chat/llama3.3')
```

## 🔗 Related Tutorials

- **Tutorial 01**: Hello World Agent (basics)
- **Tutorial 02**: Function Tools
- **Tutorial 22**: Model Selection & Configuration
- **Tutorial 27**: Third-Party Tools Integration

## 📚 Resources

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Anthropic Claude Docs](https://docs.anthropic.com/)
- [Ollama Models](https://ollama.com/library)
- [ADK Official Docs](https://google.github.io/adk-docs/)

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -e .
```

### "Authentication error"
Check that API keys are set correctly:
```bash
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY
```

### Ollama connection error
Ensure Ollama is running:
```bash
ollama serve
```

### Rate limits
Implement exponential backoff or use fallback models:
```python
try:
    # Try primary model
    result = await runner.run_async(...)
except RateLimitError:
    # Fall back to alternative model
    agent.model = fallback_model
```

## 📝 License

This tutorial is part of the ADK Training repository.

---

**Built with ❤️ using Google ADK and LiteLLM**
