---
id: using_other_llms
title: "Tutorial 28: Using Other LLMs - Multi-Model Support"
description: "Configure agents to work with different LLM providers including OpenAI, Anthropic, and local models for diverse AI capabilities."
sidebar_label: "28. Other LLMs"
sidebar_position: 28
tags: ["advanced", "llms", "multi-model", "providers", "configuration"]
keywords:
  [
    "other llms",
    "openai",
    "anthropic",
    "multi-model",
    "llm providers",
    "model configuration",
  ]
status: "draft"
difficulty: "advanced"
estimated_time: "1.5 hours"
prerequisites:
  [
    "Tutorial 01: Hello World Agent",
    "Tutorial 22: Model Selection",
    "Multiple LLM API access",
  ]
learning_objectives:
  - "Configure agents with different LLM providers"
  - "Compare capabilities across model providers"
  - "Implement model fallback strategies"
  - "Optimize for different LLM strengths"
implementation_link: "https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial28"
---

# Tutorial 28: Using Other LLMs with LiteLLM

**Goal**: Use OpenAI, Claude, Ollama, and other LLMs in your ADK agents via LiteLLM

**Prerequisites**:

- Tutorial 01 (Hello World Agent)
- Tutorial 22 (Model Selection & Configuration)
- Basic understanding of API keys and environment variables

**What You'll Learn**:

- Using OpenAI models (GPT-4o, GPT-4o-mini) with ADK
- Using Anthropic Claude models (3.7 Sonnet, Opus, Haiku) with ADK
- Running local models with Ollama (Llama3.3, Mistral, Phi4)
- Azure OpenAI integration
- Claude via Vertex AI
- Multi-provider comparison and cost optimization
- When NOT to use LiteLLM
- Best practices for cross-provider development

**Source**: `google/adk/models/lite_llm.py`, `contributing/samples/hello_world_litellm/`, `contributing/samples/hello_world_ollama/`

---

## Why Use LiteLLM?

**LiteLLM** enables ADK agents to use **100+ LLM providers** with a unified interface.

**When to Use LiteLLM**:

- ✅ Need OpenAI models (GPT-4o, GPT-4o-mini)
- ✅ Want Anthropic Claude (3.7 Sonnet, Opus, Haiku)
- ✅ Running local models with Ollama (privacy, cost, offline)
- ✅ Azure OpenAI (enterprise contracts)
- ✅ Multi-provider strategy (fallback, cost optimization)
- ✅ Comparing model performance across providers

**When NOT to Use LiteLLM**:

- ❌ **Using Gemini models** → Use native `GoogleGenAI` (better performance, features)
- ❌ Simple prototype with just Gemini
- ❌ When you need Gemini-specific features (thinking_config, grounding)

---

## 1. OpenAI Integration

**OpenAI's GPT models** are widely used for their strong reasoning and instruction-following.

### Setup

**1. Install dependencies**:

```bash
pip install google-adk[litellm]
# Or manually:
pip install litellm openai
```

**2. Get API key** from https://platform.openai.com/api-keys

**3. Set environment variable**:

```bash
export OPENAI_API_KEY='sk-...'
```

### Example: GPT-4o Agent

```python
"""
ADK agent using OpenAI GPT-4o via LiteLLM.
Source: contributing/samples/hello_world_litellm/agent.py
"""
import asyncio
import os
from google.adk.agents import Agent, Runner
from google.adk.models import LiteLlm
from google.adk.tools import FunctionTool

# Environment setup
os.environ['OPENAI_API_KEY'] = 'sk-...'  # Your OpenAI API key


def calculate_square(number: int) -> int:
    """Calculate the square of a number."""
    return number ** 2


async def main():
    """Agent using OpenAI GPT-4o."""

    # Create LiteLLM model - format: "openai/model-name"
    gpt4o_model = LiteLlm(model='openai/gpt-4o')

    # Create agent with OpenAI model
    agent = Agent(
        model=gpt4o_model,  # Use LiteLlm instance, not string
        name='gpt4o_agent',
        description='Agent powered by OpenAI GPT-4o',
        instruction='You are a helpful assistant.',
        tools=[FunctionTool(calculate_square)]
    )

    # Run queries
    runner = Runner()

    result = await runner.run_async(
        "What is the square of 12?",
        agent=agent
    )

    print(result.content.parts[0].text)


if __name__ == '__main__':
    asyncio.run(main())
```

**Output**:

```
The square of 12 is 144.
```

### GPT-4o-mini (Cost-Optimized)

**GPT-4o-mini** is **60x cheaper** than GPT-4o for simple tasks.

```python
from google.adk.models import LiteLlm

# GPT-4o: $2.50/1M input tokens, $10/1M output tokens
gpt4o = LiteLlm(model='openai/gpt-4o')

# GPT-4o-mini: $0.15/1M input tokens, $0.60/1M output tokens
gpt4o_mini = LiteLlm(model='openai/gpt-4o-mini')

# Use mini for routine tasks
routine_agent = Agent(
    model=gpt4o_mini,
    instruction='You handle simple queries quickly.'
)

# Use full GPT-4o for complex reasoning
complex_agent = Agent(
    model=gpt4o,
    instruction='You solve complex multi-step problems.'
)
```

### Available OpenAI Models

| Model                | Input Cost      | Output Cost     | Best For                  |
| -------------------- | --------------- | --------------- | ------------------------- |
| `openai/gpt-4o`      | $2.50/1M tokens | $10/1M tokens   | Complex reasoning, coding |
| `openai/gpt-4o-mini` | $0.15/1M tokens | $0.60/1M tokens | Simple tasks, high volume |
| `openai/o1`          | $15/1M tokens   | $60/1M tokens   | Advanced reasoning chains |
| `openai/o1-mini`     | $3/1M tokens    | $12/1M tokens   | STEM reasoning            |

**Model string format**: `openai/[model-name]`

---

## 2. Anthropic Claude Integration

**Anthropic's Claude** excels at long-form content, analysis, and following complex instructions.

### Setup

**1. Install dependencies**:

```bash
pip install google-adk[litellm] anthropic
```

**2. Get API key** from https://console.anthropic.com/

**3. Set environment variable**:

```bash
export ANTHROPIC_API_KEY='sk-ant-...'
```

### Example: Claude 3.7 Sonnet Agent

```python
"""
ADK agent using Anthropic Claude 3.7 Sonnet via LiteLLM.
"""
import asyncio
import os
from google.adk.agents import Agent, Runner
from google.adk.models import LiteLlm
from google.adk.tools import FunctionTool

# Environment setup
os.environ['ANTHROPIC_API_KEY'] = 'sk-ant-...'  # Your Anthropic API key


def analyze_sentiment(text: str) -> dict:
    """Analyze sentiment of text (mock implementation)."""
    # In production, use actual sentiment analysis
    return {
        'sentiment': 'positive',
        'confidence': 0.85,
        'key_phrases': ['exciting', 'innovative', 'breakthrough']
    }


async def main():
    """Agent using Claude 3.7 Sonnet."""

    # Create LiteLLM model - format: "anthropic/model-name"
    claude_model = LiteLlm(model='anthropic/claude-3-7-sonnet-20250219')

    # Create agent with Claude model
    agent = Agent(
        model=claude_model,
        name='claude_agent',
        description='Agent powered by Claude 3.7 Sonnet',
        instruction="""
You are a thoughtful analyst who provides detailed, nuanced responses.
You excel at:
- Complex reasoning
- Long-form content
- Ethical considerations
- Following detailed instructions
        """.strip(),
        tools=[FunctionTool(analyze_sentiment)]
    )

    # Run query
    runner = Runner()

    query = """
Analyze the sentiment of this product review and explain your reasoning:
"This new AI assistant is absolutely brilliant! It understands context
incredibly well and provides helpful, accurate responses. The interface
is intuitive and the speed is impressive. Highly recommended!"
    """.strip()

    result = await runner.run_async(query, agent=agent)

    print(result.content.parts[0].text)


if __name__ == '__main__':
    asyncio.run(main())
```

**Output**:

```
I'll analyze this product review's sentiment:

**Overall Sentiment**: Strongly Positive

**Analysis**:
The review exhibits overwhelmingly positive sentiment through several indicators:

1. **Superlative Language**: "absolutely brilliant", "incredibly well",
   "Highly recommended" - these are emphatic positive descriptors

2. **Specific Praise**: The reviewer highlights multiple strengths:
   - Contextual understanding
   - Helpful and accurate responses
   - Intuitive interface
   - Impressive speed

3. **Exclamation Points**: Two instances (!!) signal enthusiasm

4. **Recommendation**: Explicit endorsement ("Highly recommended") shows
   strong satisfaction

5. **No Criticisms**: Complete absence of negative comments or caveats

**Confidence**: 95% - The language is unambiguous and consistently positive
throughout.

**Key Emotional Tone**: Enthusiastic appreciation and satisfaction
```

### Available Claude Models

| Model                                  | Input Cost      | Output Cost   | Context | Best For                |
| -------------------------------------- | --------------- | ------------- | ------- | ----------------------- |
| `anthropic/claude-3-7-sonnet-20250219` | $3/1M tokens    | $15/1M tokens | 200K    | Balanced (most popular) |
| `anthropic/claude-3-5-opus-20240229`   | $15/1M tokens   | $75/1M tokens | 200K    | Complex reasoning       |
| `anthropic/claude-3-5-haiku-20241022`  | $0.80/1M tokens | $4/1M tokens  | 200K    | Fast, simple tasks      |

**Model string format**: `anthropic/[model-name-with-date]`

**Note**: Claude 3.7 Sonnet is the **default recommended model** (as of Q1 2025).

---

## 3. Ollama Local Models

**Ollama** lets you run LLMs **locally** for privacy, cost savings, and offline operation.

### Why Use Ollama?

**Benefits**:

- ✅ **Privacy**: Data never leaves your machine
- ✅ **Cost**: No API costs after initial download
- ✅ **Offline**: Works without internet
- ✅ **Compliance**: Keep sensitive data on-premises
- ✅ **Experimentation**: Try many models freely

**Trade-offs**:

- ❌ Requires GPU for good performance
- ❌ Quality lower than GPT-4o/Claude/Gemini for complex tasks
- ❌ Slower inference on CPU
- ❌ Limited context window (typically 4K-32K vs. 200K for cloud models)

### Setup

**1. Install Ollama**:

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download from https://ollama.com/download
```

**2. Start Ollama server**:

```bash
ollama serve
# Runs on http://localhost:11434 by default
```

**3. Pull a model**:

```bash
# Llama 3.3 (70B parameters, high quality)
ollama pull llama3.3

# Mistral (7B parameters, fast)
ollama pull mistral

# Phi-4 (14B parameters, Microsoft, good coding)
ollama pull phi4

# CodeLlama (7B, specialized for code)
ollama pull codellama
```

**4. Install Python dependencies**:

```bash
pip install google-adk[litellm]
```

### ⚠️ CRITICAL: Use `ollama_chat`, NOT `ollama`

**WRONG** ❌:

```python
# This WON'T work correctly!
model = LiteLlm(model='ollama/llama3.3')  # ❌ WRONG
```

**CORRECT** ✅:

```python
# Always use ollama_chat prefix!
model = LiteLlm(model='ollama_chat/llama3.3')  # ✅ CORRECT
```

**Why?** LiteLLM has two Ollama interfaces:

- `ollama/` - Uses completion API (legacy, limited)
- `ollama_chat/` - Uses chat API (recommended, full features)

ADK agents require the **chat API** for proper function calling and multi-turn conversations.

### Example: Llama 3.3 Local Agent

```python
"""
ADK agent using local Llama 3.3 via Ollama.
Source: contributing/samples/hello_world_ollama/agent.py
"""
import asyncio
import os
from google.adk.agents import Agent, Runner
from google.adk.models import LiteLlm
from google.adk.tools import FunctionTool

# Environment setup for Ollama
os.environ['OLLAMA_API_BASE'] = 'http://localhost:11434'


def get_weather(city: str) -> dict:
    """Get current weather for a city (mock)."""
    # In production, call real weather API
    return {
        'city': city,
        'temperature': 72,
        'condition': 'Sunny',
        'humidity': 45
    }


async def main():
    """Agent using local Llama 3.3 model."""

    # Create LiteLLM model - format: "ollama_chat/model-name"
    # ⚠️ IMPORTANT: Use ollama_chat, NOT ollama!
    llama_model = LiteLlm(model='ollama_chat/llama3.3')

    # Create agent with local model
    agent = Agent(
        model=llama_model,
        name='local_agent',
        description='Agent running locally with Llama 3.3',
        instruction='You are a helpful local assistant. You run entirely on-device.',
        tools=[FunctionTool(get_weather)]
    )

    # Run queries
    runner = Runner()

    print("\n" + "="*60)
    print("LOCAL OLLAMA AGENT (Privacy-First)")
    print("="*60 + "\n")

    result = await runner.run_async(
        "What's the weather like in San Francisco?",
        agent=agent
    )

    print(result.content.parts[0].text)
    print("\n" + "="*60 + "\n")


if __name__ == '__main__':
    asyncio.run(main())
```

**Output**:

```
============================================================
LOCAL OLLAMA AGENT (Privacy-First)
============================================================

The weather in San Francisco is currently sunny with a temperature
of 72°F and 45% humidity. It's a beautiful day!

[All processing done locally - no data sent to cloud]

============================================================
```

### Popular Ollama Models

| Model                   | Size   | Best For                        | GPU RAM |
| ----------------------- | ------ | ------------------------------- | ------- |
| `ollama_chat/llama3.3`  | 70B    | General tasks, strong reasoning | 40GB+   |
| `ollama_chat/llama3.2`  | 3B     | Fast, low resource              | 4GB     |
| `ollama_chat/mistral`   | 7B     | Balanced speed/quality          | 8GB     |
| `ollama_chat/phi4`      | 14B    | Coding, STEM                    | 16GB    |
| `ollama_chat/codellama` | 7B-34B | Code generation                 | 8-32GB  |
| `ollama_chat/gemma2`    | 9B     | Google, instruction following   | 12GB    |
| `ollama_chat/qwen2.5`   | 7B-72B | Multilingual                    | 8-40GB  |

**Model string format**: `ollama_chat/[model-name]` ⚠️ NOT `ollama/`!

### Configuration Options

```python
from google.adk.models import LiteLlm

# Basic usage
model = LiteLlm(model='ollama_chat/llama3.3')

# With custom Ollama server
os.environ['OLLAMA_API_BASE'] = 'http://192.168.1.100:11434'
model = LiteLlm(model='ollama_chat/llama3.3')

# With additional parameters (passed to Ollama)
model = LiteLlm(
    model='ollama_chat/llama3.3',
    temperature=0.7,
    top_p=0.9,
    max_tokens=2048
)
```

---

## 4. Azure OpenAI Integration

**Azure OpenAI** is for enterprises with **Azure contracts** or **compliance requirements**.

### Setup

**1. Create Azure OpenAI resource** in Azure Portal

**2. Deploy a model** (e.g., gpt-4o)

**3. Get credentials**:

- API key from Azure Portal
- Endpoint URL (e.g., `https://your-resource.openai.azure.com/`)
- Deployment name (e.g., `gpt-4o-deployment`)

**4. Set environment variables**:

```bash
export AZURE_API_KEY='your-azure-key'
export AZURE_API_BASE='https://your-resource.openai.azure.com/'
export AZURE_API_VERSION='2024-02-15-preview'
```

### Example: Azure OpenAI Agent

```python
"""
ADK agent using Azure OpenAI.
"""
import asyncio
import os
from google.adk.agents import Agent, Runner
from google.adk.models import LiteLlm

# Azure OpenAI configuration
os.environ['AZURE_API_KEY'] = 'your-azure-key'
os.environ['AZURE_API_BASE'] = 'https://your-resource.openai.azure.com/'
os.environ['AZURE_API_VERSION'] = '2024-02-15-preview'


async def main():
    """Agent using Azure OpenAI."""

    # Create LiteLLM model - format: "azure/deployment-name"
    azure_model = LiteLlm(model='azure/gpt-4o-deployment')

    # Create agent
    agent = Agent(
        model=azure_model,
        name='azure_agent',
        description='Agent using Azure OpenAI',
        instruction='You are an enterprise assistant running on Azure.'
    )

    # Run query
    runner = Runner()
    result = await runner.run_async(
        "Explain the benefits of Azure OpenAI for enterprises",
        agent=agent
    )

    print(result.content.parts[0].text)


if __name__ == '__main__':
    asyncio.run(main())
```

**Why Azure OpenAI?**

- ✅ Enterprise SLAs (99.9% uptime)
- ✅ Data residency (EU, US, Asia)
- ✅ Private networks (VNet integration)
- ✅ Compliance (SOC 2, HIPAA, GDPR)
- ✅ Unified billing with Azure services

---

## 5. Claude via Vertex AI

**Claude on Vertex AI** combines Anthropic's models with Google Cloud infrastructure.

### Setup

**1. Enable Vertex AI API** in Google Cloud Console

**2. Set up authentication**:

```bash
export GOOGLE_CLOUD_PROJECT='your-project'
export GOOGLE_CLOUD_LOCATION='us-central1'  # or your preferred region
export GOOGLE_APPLICATION_CREDENTIALS='/path/to/service-account-key.json'
```

**3. Ensure Vertex AI Claude access** (may require approval)

### Example: Claude via Vertex AI

```python
"""
ADK agent using Claude 3.7 Sonnet via Vertex AI.
"""
import asyncio
import os
from google.adk.agents import Agent, Runner
from google.adk.models import LiteLlm

# Vertex AI configuration
os.environ['GOOGLE_CLOUD_PROJECT'] = 'your-project'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'


async def main():
    """Agent using Claude via Vertex AI."""

    # Create LiteLLM model - format: "vertex_ai/model-name"
    claude_vertex = LiteLlm(model='vertex_ai/claude-3-7-sonnet@20250219')

    # Create agent
    agent = Agent(
        model=claude_vertex,
        name='claude_vertex_agent',
        description='Agent using Claude on Vertex AI',
        instruction='You leverage Claude via Google Cloud infrastructure.'
    )

    # Run query
    runner = Runner()
    result = await runner.run_async(
        "Compare Claude direct vs. Claude on Vertex AI",
        agent=agent
    )

    print(result.content.parts[0].text)


if __name__ == '__main__':
    asyncio.run(main())
```

**Claude Direct vs. Vertex AI**:

| Factor             | Direct (Anthropic) | Via Vertex AI           |
| ------------------ | ------------------ | ----------------------- |
| **Pricing**        | Per-token pricing  | Same or slightly higher |
| **Data residency** | US-based           | Choose GCP region       |
| **SLA**            | Standard           | Google Cloud SLA        |
| **Integration**    | Anthropic API      | Unified with GCP        |
| **Billing**        | Separate           | Unified GCP billing     |
| **Setup**          | Simpler            | More complex            |

**Use Vertex AI Claude when**:

- ✅ Already using Google Cloud extensively
- ✅ Need data residency in specific GCP regions
- ✅ Want unified GCP billing
- ✅ Require Google Cloud SLAs

---

## 6. Multi-Provider Comparison

**Use Case**: Compare response quality across multiple providers for the same query.

```python
"""
Multi-provider agent comparison.
Test same query across Gemini, GPT-4o, Claude, and Llama 3.3.
"""
import asyncio
import os
from google.adk.agents import Agent, Runner
from google.adk.models import GoogleGenAI, LiteLlm

# Environment setup
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = '1'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'your-project'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'
os.environ['OPENAI_API_KEY'] = 'sk-...'
os.environ['ANTHROPIC_API_KEY'] = 'sk-ant-...'
os.environ['OLLAMA_API_BASE'] = 'http://localhost:11434'


async def compare_models():
    """Compare response quality across 4 providers."""

    # Define models
    models = {
        'Gemini 2.5 Flash': GoogleGenAI(model='gemini-2.5-flash'),
        'GPT-4o': LiteLlm(model='openai/gpt-4o'),
        'Claude 3.7 Sonnet': LiteLlm(model='anthropic/claude-3-7-sonnet-20250219'),
        'Llama 3.3 (Local)': LiteLlm(model='ollama_chat/llama3.3')
    }

    # Test query
    query = """
Explain quantum entanglement to a 12-year-old.
Use an analogy they can relate to.
    """.strip()

    runner = Runner()

    print("\n" + "="*70)
    print("MULTI-PROVIDER MODEL COMPARISON")
    print("="*70 + "\n")
    print(f"Query: {query}\n")
    print("="*70 + "\n")

    # Test each model
    for model_name, model in models.items():
        print(f"### {model_name}")
        print("-" * 70)

        agent = Agent(
            model=model,
            instruction='You explain complex topics clearly and simply.'
        )

        try:
            result = await runner.run_async(query, agent=agent)
            response = result.content.parts[0].text

            print(response)
            print(f"\n[Length: {len(response)} chars]")

        except Exception as e:
            print(f"Error: {e}")

        print("\n" + "="*70 + "\n")


if __name__ == '__main__':
    asyncio.run(compare_models())
```

**Example Output**:

```
======================================================================
MULTI-PROVIDER MODEL COMPARISON
======================================================================

Query: Explain quantum entanglement to a 12-year-old.
Use an analogy they can relate to.

======================================================================

### Gemini 2.5 Flash
----------------------------------------------------------------------
Imagine you have two magic coins. When you flip one and it lands on
heads, the other coin INSTANTLY lands on tails - no matter how far
apart they are. Even if one coin is on Earth and the other is on Mars!

That's quantum entanglement. Two particles become "entangled" so that
measuring one INSTANTLY affects the other, even across huge distances.

[Length: 387 chars]

======================================================================

### GPT-4o
----------------------------------------------------------------------
Think of quantum entanglement like having two magical dice that are
connected. When you roll one die and it shows a 6, the other die
automatically shows a 1 - instantly, even if it's on the other side
of the world! Scientists don't fully understand HOW this happens, but
they know it does. It's one of the strangest things in physics!

[Length: 415 chars]

======================================================================

### Claude 3.7 Sonnet
----------------------------------------------------------------------
Imagine you and your best friend each have a magic marble. No matter
how far apart you go - even if you go to different countries - when
you squeeze your marble and it turns red, your friend's marble turns
blue at the EXACT same instant.

That's quantum entanglement! Two particles become linked so that what
happens to one immediately affects the other, no matter the distance.
Einstein called it "spooky action at a distance" because even he
found it weird!

[Length: 512 chars]

======================================================================

### Llama 3.3 (Local)
----------------------------------------------------------------------
Think of quantum entanglement like having two special coins that are
twins. If you flip one coin and it lands on heads, the other coin will
always land on tails - instantly! They're connected in a mysterious way
that scientists are still trying to fully understand.

[Length: 287 chars]

======================================================================
```

**Observations**:

- **Gemini 2.5 Flash**: Fast, concise, accurate
- **GPT-4o**: Clear analogy, acknowledges mystery
- **Claude 3.7 Sonnet**: Most detailed, includes Einstein quote
- **Llama 3.3**: Shortest, simpler but less engaging

---

## 7. Cost Optimization Strategies

### Cost Comparison (per 1M tokens)

| Provider      | Model             | Input Cost | Output Cost | Total (1M in + 1M out) |
| ------------- | ----------------- | ---------- | ----------- | ---------------------- |
| **Google**    | gemini-2.5-flash  | $0.075     | $0.30       | **$0.375** ⭐ Cheapest |
| **Google**    | gemini-2.5-pro    | $1.25      | $5.00       | $6.25                  |
| **OpenAI**    | gpt-4o-mini       | $0.15      | $0.60       | $0.75                  |
| **OpenAI**    | gpt-4o            | $2.50      | $10.00      | $12.50                 |
| **Anthropic** | claude-3-5-haiku  | $0.80      | $4.00       | $4.80                  |
| **Anthropic** | claude-3-7-sonnet | $3.00      | $15.00      | $18.00                 |
| **Ollama**    | llama3.3 (local)  | $0         | $0          | **$0** 🎉 Free         |

### Strategy 1: Tiered Model Selection

```python
def get_model_for_task(complexity: str):
    """Select model based on task complexity."""

    if complexity == 'simple':
        # Use cheapest model for simple tasks
        return LiteLlm(model='openai/gpt-4o-mini')  # Or gemini-2.5-flash

    elif complexity == 'medium':
        # Balanced cost/quality
        return GoogleGenAI(model='gemini-2.5-flash')

    elif complexity == 'complex':
        # Best reasoning, worth the cost
        return LiteLlm(model='anthropic/claude-3-7-sonnet-20250219')

    elif complexity == 'local_ok':
        # Privacy/cost priority
        return LiteLlm(model='ollama_chat/llama3.3')

# Example usage
simple_agent = Agent(model=get_model_for_task('simple'))
complex_agent = Agent(model=get_model_for_task('complex'))
```

### Strategy 2: Fallback Chain

```python
async def run_with_fallback(query: str):
    """Try models in order of cost (cheapest first)."""

    models = [
        ('gemini-2.5-flash', GoogleGenAI(model='gemini-2.5-flash')),
        ('gpt-4o-mini', LiteLlm(model='openai/gpt-4o-mini')),
        ('gpt-4o', LiteLlm(model='openai/gpt-4o'))
    ]

    for model_name, model in models:
        try:
            agent = Agent(model=model)
            runner = Runner()
            result = await runner.run_async(query, agent=agent)

            print(f"✅ Success with {model_name}")
            return result

        except Exception as e:
            print(f"❌ {model_name} failed: {e}")
            continue

    raise Exception("All models failed")
```

### Strategy 3: Local for High Volume

```python
"""
Use local Ollama for high-volume, simple tasks.
Use cloud models only when needed.
"""

async def process_batch(queries: list[str]):
    """Process many queries cost-effectively."""

    # Local model for bulk processing
    local_model = LiteLlm(model='ollama_chat/llama3.3')
    local_agent = Agent(model=local_model)

    # Cloud model for complex queries
    cloud_model = GoogleGenAI(model='gemini-2.5-flash')
    cloud_agent = Agent(model=cloud_model)

    runner = Runner()
    results = []

    for query in queries:
        # Route by complexity
        if is_simple(query):
            # Free local processing
            result = await runner.run_async(query, agent=local_agent)
        else:
            # Use cloud for complex
            result = await runner.run_async(query, agent=cloud_agent)

        results.append(result)

    return results


def is_simple(query: str) -> bool:
    """Determine if query is simple enough for local model."""
    simple_keywords = ['what is', 'define', 'explain', 'summarize']
    return any(kw in query.lower() for kw in simple_keywords)
```

---

## 8. Best Practices

### ✅ DO

**1. Use Native Gemini When Possible**:

```python
# ✅ BEST - Native Gemini
agent = Agent(model='gemini-2.5-flash')

# ❌ DON'T - Gemini via LiteLLM (slower, missing features)
agent = Agent(model=LiteLlm(model='gemini/gemini-2.5-flash'))
```

**2. Set Environment Variables Securely**:

```python
import os

# ✅ GOOD - From environment
api_key = os.environ.get('OPENAI_API_KEY')

# ❌ BAD - Hardcoded
api_key = 'sk-...'  # Never commit this!
```

**3. Handle Provider-Specific Errors**:

```python
try:
    result = await runner.run_async(query, agent=agent)
except Exception as e:
    if 'rate_limit' in str(e).lower():
        print("Hit rate limit, waiting...")
        await asyncio.sleep(60)
    elif 'quota' in str(e).lower():
        print("Quota exceeded, switching provider...")
        agent.model = fallback_model
    else:
        raise
```

**4. Use Ollama Correctly**:

```python
# ✅ CORRECT - ollama_chat prefix
model = LiteLlm(model='ollama_chat/llama3.3')

# ❌ WRONG - ollama prefix (limited functionality)
model = LiteLlm(model='ollama/llama3.3')
```

**5. Monitor Costs**:

```python
import time

class CostTracker:
    def __init__(self):
        self.total_tokens = 0
        self.model_costs = {
            'openai/gpt-4o': 2.50 / 1_000_000,  # per input token
            'anthropic/claude-3-7-sonnet-20250219': 3.00 / 1_000_000
        }

    def track(self, model: str, tokens: int):
        cost = tokens * self.model_costs.get(model, 0)
        self.total_tokens += tokens
        print(f"Cost: ${cost:.4f} | Total: {self.total_tokens:,} tokens")

tracker = CostTracker()
```

### ❌ DON'T

**1. Don't Use LiteLLM for Gemini**:

```python
# ❌ BAD - Loses Gemini-specific features
model = LiteLlm(model='gemini/gemini-2.5-flash')

# ✅ GOOD - Use native
model = 'gemini-2.5-flash'  # Or GoogleGenAI('gemini-2.5-flash')
```

**2. Don't Forget `ollama_chat` Prefix**:

```python
# ❌ WRONG
LiteLlm(model='ollama/llama3.3')

# ✅ RIGHT
LiteLlm(model='ollama_chat/llama3.3')
```

**3. Don't Ignore Provider Limits**:

- OpenAI: 200K tokens/min (tier dependent)
- Anthropic: 200K tokens/min (varies)
- Ollama: Limited by your GPU

**4. Don't Mix Credentials**:

```bash
# ❌ BAD - Conflicts
export OPENAI_API_KEY='key1'
export OPENAI_API_KEY='key2'  # Overwrites!

# ✅ GOOD - Use different env names if needed
export OPENAI_API_KEY='key1'
export AZURE_OPENAI_API_KEY='key2'
```

---

## Summary

You've learned how to use OpenAI, Claude, Ollama, and other LLMs in ADK agents via LiteLLM:

**Key Takeaways**:

- ✅ **LiteLLM** enables 100+ LLM providers in ADK
- ✅ **OpenAI**: `LiteLlm(model='openai/gpt-4o')` - requires `OPENAI_API_KEY`
- ✅ **Claude**: `LiteLlm(model='anthropic/claude-3-7-sonnet-20250219')` - requires `ANTHROPIC_API_KEY`
- ✅ **Ollama**: `LiteLlm(model='ollama_chat/llama3.3')` - ⚠️ Use `ollama_chat`, NOT `ollama`!
- ✅ **Azure OpenAI**: `LiteLlm(model='azure/deployment-name')` - enterprise option
- ✅ **DON'T** use LiteLLM for Gemini - use native `GoogleGenAI` instead
- ✅ **Local models** (Ollama) great for privacy, cost, offline use
- ✅ **Cost optimization**: gemini-2.5-flash ($0.375/1M), gpt-4o-mini ($0.75/1M), local (free)

**Model String Formats**:

| Provider  | Format                | Example                                 |
| --------- | --------------------- | --------------------------------------- |
| OpenAI    | `openai/[model]`      | `openai/gpt-4o`                         |
| Anthropic | `anthropic/[model]`   | `anthropic/claude-3-7-sonnet-20250219`  |
| Ollama    | `ollama_chat/[model]` | `ollama_chat/llama3.3` ⚠️ NOT `ollama/` |
| Azure     | `azure/[deployment]`  | `azure/gpt-4o-deployment`               |
| Vertex AI | `vertex_ai/[model]`   | `vertex_ai/claude-3-7-sonnet@20250219`  |

**When to Use What**:

| Use Case                  | Recommended Model                 |
| ------------------------- | --------------------------------- |
| Simple tasks, high volume | gemini-2.5-flash or gpt-4o-mini   |
| Complex reasoning         | claude-3-7-sonnet or gpt-4o       |
| Privacy/compliance        | ollama_chat/llama3.3 (local)      |
| Enterprise Azure          | azure/gpt-4o-deployment           |
| Cost optimization         | gemini-2.5-flash (cheapest cloud) |
| Offline/air-gapped        | ollama_chat models                |
| Coding tasks              | ollama_chat/phi4 or gpt-4o        |
| Long-form content         | claude-3-7-sonnet                 |

**Environment Variables Required**:

```bash
# OpenAI
export OPENAI_API_KEY='sk-...'

# Anthropic
export ANTHROPIC_API_KEY='sk-ant-...'

# Ollama
export OLLAMA_API_BASE='http://localhost:11434'

# Azure OpenAI
export AZURE_API_KEY='...'
export AZURE_API_BASE='https://your-resource.openai.azure.com/'
export AZURE_API_VERSION='2024-02-15-preview'

# Google (for native Gemini, not LiteLLM)
export GOOGLE_CLOUD_PROJECT='your-project'
export GOOGLE_CLOUD_LOCATION='us-central1'
```

**Production Checklist**:

- [ ] Environment variables configured securely (not hardcoded)
- [ ] API keys stored in secret manager (production)
- [ ] Cost tracking implemented
- [ ] Rate limit handling in place
- [ ] Fallback models configured
- [ ] Ollama models use `ollama_chat` prefix (not `ollama`)
- [ ] NOT using LiteLLM for Gemini (use native instead)
- [ ] Error handling for provider-specific issues
- [ ] Model selection based on task complexity
- [ ] Monitoring and alerting set up

**Next Steps**:

- **Tutorial 22**: Review native Gemini 2.5 models and features
- **Tutorial 26**: Deploy agents to Google AgentSpace
- **Tutorial 27**: Integrate LangChain and CrewAI tools
- **Tutorial 18**: Master Events & Observability

**Resources**:

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Anthropic Claude Documentation](https://docs.anthropic.com/)
- [Ollama Models](https://ollama.com/library)
- [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
- [ADK LiteLLM Sample](https://github.com/google/adk-docs/tree/main/contributing/samples/hello_world_litellm)

---

**Congratulations!** You can now use OpenAI, Claude, Ollama, and other LLMs in your ADK agents, and you understand when to use native Gemini vs. LiteLLM providers.
