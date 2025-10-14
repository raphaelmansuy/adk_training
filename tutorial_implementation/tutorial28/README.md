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

## 🧪 Testing Different AI Models

### Step-by-Step Testing Guide

#### 1. Test with OpenAI GPT-4o-mini (Default)

```bash
# Set only OpenAI key
export OPENAI_API_KEY=sk-your_openai_key_here

# Run the demo
make demo

# Expected: All demos run successfully with GPT-4o-mini
```

#### 2. Test with Claude 3.7 Sonnet

```bash
# Set only Anthropic key
export ANTHROPIC_API_KEY=sk-ant-your_anthropic_key_here

# Run the demo
make demo

# Expected: All demos run successfully with Claude
```

#### 3. Test with Ollama (Local Model)

```bash
# Install Ollama if not already installed
# Visit: https://ollama.com

# Pull the Granite 4 model
ollama pull granite4:latest

# Start Ollama server (in another terminal)
ollama serve

# Run the demo (no API keys needed for local)
make demo

# Expected: Ollama demos run locally, others may fail without API keys
```

#### 4. Test Multiple Providers Simultaneously

```bash
# Set all API keys
export OPENAI_API_KEY=sk-your_openai_key_here
export ANTHROPIC_API_KEY=sk-ant-your_anthropic_key_here

# Ensure Ollama is running
ollama serve

# Run the demo
make demo

# Expected: All 4 models tested across all demo scenarios
```

### Testing Specific Agents

#### Run Individual Agents via ADK Web Interface

```bash
# Start ADK web interface
make dev

# Open http://localhost:8000
# Select from dropdown:
# - multi_llm_agent (OpenAI GPT-4o-mini)
# - gpt4o_mini_agent (OpenAI GPT-4o-mini alternative)
# - claude_agent (Claude 3.7 Sonnet)
# - ollama_agent (Granite 4 local)
```

#### Test Agents Programmatically

```python
# Test specific agent
from multi_llm_agent.agent import root_agent, claude_agent, ollama_agent

# Test OpenAI agent
print("Testing OpenAI GPT-4o-mini...")
# Use agent.run() or Runner pattern

# Test Claude agent
print("Testing Claude 3.7 Sonnet...")
# Use agent.run() or Runner pattern

# Test Ollama agent
print("Testing Ollama Granite 4...")
# Use agent.run() or Runner pattern
```

### Adding More AI Models

#### 1. Add a New LiteLLM-Supported Model

```python
# In agent.py, add new agent configuration
new_agent = Agent(
    name="new_model_agent",
    model=LiteLlm(model='provider/model-name'),  # e.g., 'together/mistral-7b'
    description="Agent powered by New Model",
    instruction="You are powered by the new AI model.",
    tools=[calculate_square, get_weather, analyze_sentiment]
)
```

#### 2. Supported Model Examples

```python
# More OpenAI models
gpt4_turbo_agent = Agent(
    model=LiteLlm(model='openai/gpt-4-turbo'),
    # ... other config
)

# Google models via LiteLLM (not recommended, use native instead)
# gemini_pro_agent = Agent(
#     model=LiteLlm(model='gemini/gemini-pro'),
#     # ... but better to use native: model='gemini-pro'
# )

# Together AI models
mistral_agent = Agent(
    model=LiteLlm(model='together/mistral-7b-instruct'),
    # ... other config
)

# Hugging Face models
zephyr_agent = Agent(
    model=LiteLlm(model='huggingface/zephyr-7b-beta'),
    # ... other config
)

# More Ollama models
llama_agent = Agent(
    model=LiteLlm(model='ollama_chat/llama3.2'),
    # ... other config
)
```

#### 3. Test New Models

```bash
# Set appropriate API keys for the new provider
export TOGETHER_API_KEY=your_together_key
export HUGGINGFACE_API_KEY=your_hf_key

# Add to demo.py agents list
agents.append((new_agent, "New Model Name"))

# Run demo
make demo
```

### API Key Management

#### Environment Variables for Different Providers

```bash
# OpenAI
export OPENAI_API_KEY=sk-...

# Anthropic
export ANTHROPIC_API_KEY=sk-ant-...

# Together AI
export TOGETHER_API_KEY=...

# Hugging Face
export HUGGINGFACE_API_KEY=hf_...

# Replicate
export REPLICATE_API_TOKEN=...

# Azure OpenAI
export AZURE_API_KEY=...
export AZURE_API_BASE=...
export AZURE_API_VERSION=...
```

#### Testing API Key Validity

```bash
# Quick test script
python -c "
import os
from litellm import completion

# Test OpenAI
try:
    response = completion(
        model='openai/gpt-4o-mini',
        messages=[{'role': 'user', 'content': 'Hello'}],
        api_key=os.getenv('OPENAI_API_KEY')
    )
    print('✅ OpenAI: Working')
except Exception as e:
    print(f'❌ OpenAI: {e}')

# Test Anthropic
try:
    response = completion(
        model='anthropic/claude-3-haiku-20240307',
        messages=[{'role': 'user', 'content': 'Hello'}],
        api_key=os.getenv('ANTHROPIC_API_KEY')
    )
    print('✅ Anthropic: Working')
except Exception as e:
    print(f'❌ Anthropic: {e}')
"
```

### Performance Comparison Testing

#### Run Benchmarks

```bash
# Test response times
python -c "
import time
from multi_llm_agent.examples.demo import run_query
from multi_llm_agent.agent import root_agent, claude_agent, ollama_agent

agents = [
    (root_agent, 'GPT-4o-mini'),
    (claude_agent, 'Claude 3.7'),
    (ollama_agent, 'Ollama Granite')
]

query = 'What is 15 squared?'
for agent, name in agents:
    start = time.time()
    result = await run_query(agent, query, name)
    elapsed = time.time() - start
    print(f'{name}: {elapsed:.2f}s')
"
```

#### Cost Analysis

```bash
# Estimate costs (requires litellm)
python -c "
import litellm

# Get pricing
pricing = litellm.get_model_cost('openai/gpt-4o-mini')
print('GPT-4o-mini pricing:', pricing)

pricing = litellm.get_model_cost('anthropic/claude-3-7-sonnet-20250219')
print('Claude 3.7 pricing:', pricing)
"
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

## Built with ❤️ using Google ADK and LiteLLM
