# Tutorial 22: Model Selection & Optimization - Working Implementation

This is the complete working implementation of **Tutorial 22: Model Selection & Optimization** from the ADK Training repository.

## Overview

This implementation demonstrates a comprehensive framework for selecting, benchmarking, and comparing AI models, including:

- **Model Selection Tools**: Recommend the right model for specific use cases
- **Model Information Retrieval**: Get detailed capabilities and pricing for each model
- **Benchmarking Framework**: Compare models on performance, cost, and quality
- **Interactive Agent**: Conversational interface for model recommendations

## Quick Start

```bash
# Install dependencies
make setup

# Run the agent in development mode
make dev

# Run automated model comparison
make demo
```

## Project Structure

```text
tutorial22/
├── model_selector/          # Agent implementation
│   ├── __init__.py         # Package exports
│   ├── agent.py            # Model selection framework
│   └── .env.example        # Environment template
├── model_specs.py           # Standalone model specifications
├── tests/                  # Comprehensive test suite
│   ├── __init__.py         # Test package
│   ├── test_agent.py       # Agent and tool tests
│   ├── test_imports.py     # Import validation
│   └── test_structure.py   # Project structure tests
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Project configuration
├── Makefile               # Development commands
└── README.md              # This file
```

## Agent Features

### Root Agent: `model_selector_agent`

A conversational AI assistant that helps users:

1. **Choose the Right Model**: Recommends models based on use case requirements
2. **Compare Models**: Explains tradeoffs between different models
3. **Understand Capabilities**: Details features, pricing, and limitations
4. **Optimize Costs**: Suggests cost-effective alternatives

### Available Tools

#### 1. `recommend_model_for_use_case(use_case: str)`

Recommends the best model for a given use case.

**Example use cases:**

- "real-time voice assistant" → `gemini-2.0-flash-live`
- "complex strategic planning" → `gemini-2.5-pro`
- "high-volume content moderation" → `gemini-2.5-flash-lite`
- "general customer service" → `gemini-2.5-flash` (recommended default)

#### 2. `get_model_info(model_name: str)`

Returns detailed information about a specific model including:

- Context window size
- Key features
- Best use cases
- Pricing tier
- Speed characteristics

### ModelSelector Framework

The `ModelSelector` class provides programmatic model comparison:

```python
from model_selector.agent import ModelSelector

selector = ModelSelector()

# Benchmark models on test queries
await selector.compare_models(
    models=['gemini-2.5-flash', 'gemini-2.0-flash'],
    test_queries=[...],
    instruction="..."
)
```

## Quality Score Calculation

The **Quality Score** measures model **performance** using this formula:

```python
quality_score = success_rate * (1.0 / (1.0 + avg_latency))
```

**What it measures:**

- **`success_rate`**: Percentage of successful queries (reliability)
- **`avg_latency`**: Average response time in seconds (speed)
- **Higher scores** = Better performance (faster + more reliable)

**Important Note:** This score measures **performance** (speed + reliability),
not **response quality** (accuracy, helpfulness, or correctness). The current
implementation focuses on operational metrics that can be measured
programmatically.

**Score interpretation:**

- **0.8-1.0**: Excellent performance (very fast, highly reliable)
- **0.5-0.8**: Good performance (balanced speed and reliability)
- **0.2-0.5**: Fair performance (acceptable for some use cases)
- **<0.2**: Poor performance (slow or unreliable)

**Example calculations:**

- **gemini-2.5-flash-lite** (0.73s avg) → `1.0 / (1.0 + 0.73)` = **0.579**
- **gemini-2.0-flash** (1.24s avg) → `1.0 / (1.0 + 1.24)` = **0.447**
- **gemini-2.5-flash** (3.31s avg) → `1.0 / (1.0 + 3.31)` = **0.232**

**Future Enhancement:** Response quality evaluation could be added using
metrics like BLEU, ROUGE, or human evaluation, but this would require ground
truth answers and more complex evaluation logic.

## Testing

### Unit Tests

Run comprehensive test suite:

```bash
make test
```

**Test Coverage:**

- ✅ Agent configuration (8 tests)
- ✅ Tool functionality (12 tests)
- ✅ ModelSelector class (2 tests)
- ✅ ModelBenchmark dataclass (1 test)
- ✅ Import validation (10 tests)
- ✅ Project structure (14 tests)

Total: 47 tests

### Coverage Report

Generate coverage report:

```bash
make test-cov
```

Opens `htmlcov/index.html` with detailed coverage analysis.

## Demo Prompts

Try these example prompts in the ADK web interface:

```bash
make demo
```

### Interactive Mode (Web UI)

1. **Model Recommendation**: "What model should I use for real-time voice chat?"
2. **Model Comparison**: "Compare gemini-2.5-flash and gemini-2.5-pro"
3. **Model Information**: "Tell me about gemini-2.5-flash-lite"
4. **Use Case Advice**: "Which model is best for complex reasoning tasks?"

### Standalone Benchmark Mode

The demo also runs an automated comparison:

```bash
python -m model_selector.agent
```

This benchmarks multiple models on standard test queries and provides:

- Average latency per query
- Token usage statistics
- Cost estimates
- Quality scores
- Recommendations by category (fastest, cheapest, best quality)

## Configuration

### Environment Variables

Choose one authentication method:

**Method 1 - API Key (Gemini API):**

```bash
export GOOGLE_API_KEY=your_api_key_here
```

Get a free key at: <https://aistudio.google.com/app/apikey>

**Method 2 - Service Account (Vertex AI):**

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
export GOOGLE_CLOUD_PROJECT=your_project_id
```

### Model Configuration

The agent uses `gemini-2.5-flash` (recommended default) but can work with:

- **gemini-2.5-flash**: Best price-performance (RECOMMENDED)
- **gemini-2.5-flash-lite**: Ultra-fast for simple tasks
- **gemini-2.5-pro**: Highest quality for complex reasoning
- **gemini-2.0-flash-live**: Real-time bidirectional streaming
- **gemini-1.5-pro**: 2M token context for large documents

## Development Commands

### Setup

```bash
make setup              # Install dependencies and configure environment
```

### Development

```bash
make dev                # Start ADK web interface (localhost:8000)
make demo               # Show demo prompts and run benchmark
make benchmark          # Run automated model performance tests
make compare-models     # Compare specific models side-by-side
make model-info         # Show detailed model specifications
make full-demo          # Complete experience (all demos)
```

### Testing Commands

```bash
make test               # Run all tests with pytest
make test-cov           # Run tests with coverage report
```

### Cleanup

```bash
make clean              # Remove cache files and artifacts
```

## Key Learnings

### Model Selection Best Practices

1. **Always Specify Model Explicitly**

   ```python
   agent = Agent(
       model='gemini-2.5-flash',  # RECOMMENDED
       name='my_agent'
   )
   ```

2. **Match Model to Use Case**

   - Real-time streaming → `gemini-2.0-flash-live`
   - Complex reasoning → `gemini-2.5-pro`
   - High-volume simple → `gemini-2.5-flash-lite`
   - General purpose → `gemini-2.5-flash`

3. **Consider Tradeoffs**

   - Cost vs Quality
   - Speed vs Capability
   - Context window vs Price

4. **Benchmark Before Production**
   - Test with realistic queries
   - Measure latency, cost, and quality
   - Compare multiple models

### Cost Optimization

- Use cheaper models (flash-lite) for simple tasks
- Use expensive models (pro) only when needed
- Implement dynamic model selection based on query complexity
- Monitor and optimize token usage

## Expected Output Examples

### Interactive Agent Response

**User:** "What model should I use for real-time voice chat?"

**Agent:** "For real-time voice chat applications, I recommend
**gemini-2.0-flash-live**. This model is specifically designed for:

- ✅ Real-time bidirectional streaming
- ✅ Low latency audio processing
- ✅ Multimodal voice + text interactions

This is the only model in the Gemini family that supports live,
bidirectional streaming, making it ideal for voice assistants and
real-time conversational applications."

### Benchmark Output

```
======================================================================
BENCHMARKING: gemini-2.5-flash
======================================================================

Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.
✅ Query: What is the capital of France?...
   Latency: 0.56s, Tokens: ~1
✅ Query: Explain quantum computing in simple terms...
   Latency: 6.69s, Tokens: ~126
✅ Query: Write a haiku about artificial intelligence...
   Latency: 2.67s, Tokens: ~14

📊 RESULTS:
   Avg Latency: 3.31s
   Avg Tokens: 47
   Success Rate: 100.0%
   Cost Estimate: $0.000004 per query
   Quality Score: 0.232

======================================================================
BENCHMARKING: gemini-2.0-flash
======================================================================

Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.
✅ Query: What is the capital of France?...
   Latency: 0.56s, Tokens: ~6
✅ Query: Explain quantum computing in simple terms...
   Latency: 2.31s, Tokens: ~149
✅ Query: Write a haiku about artificial intelligence...
   Latency: 0.84s, Tokens: ~10

📊 RESULTS:
   Avg Latency: 1.24s
   Avg Tokens: 55
   Success Rate: 100.0%
   Cost Estimate: $0.000006 per query
   Quality Score: 0.447

======================================================================
BENCHMARKING: gemini-2.5-flash-lite
======================================================================

Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.
✅ Query: What is the capital of France?...
   Latency: 0.61s, Tokens: ~6
✅ Query: Explain quantum computing in simple terms...
   Latency: 1.24s, Tokens: ~172
✅ Query: Write a haiku about artificial intelligence...
   Latency: 0.33s, Tokens: ~15

📊 RESULTS:
   Avg Latency: 0.73s
   Avg Tokens: 64
   Success Rate: 100.0%
   Cost Estimate: $0.000003 per query
   Quality Score: 0.579

======================================================================
COMPARISON SUMMARY
======================================================================

Model                             Latency   Tokens       Cost    Quality
----------------------------------------------------------------------
gemini-2.5-flash                    3.31s       47 $ 0.000004      0.232
gemini-2.0-flash                    1.24s       55 $ 0.000006      0.447
gemini-2.5-flash-lite               0.73s       64 $ 0.000003      0.579

======================================================================

🎯 RECOMMENDATIONS:

⚡ Fastest: gemini-2.5-flash-lite (0.73s)
💰 Cheapest: gemini-2.5-flash-lite ($0.000003)
🏆 Best Quality: gemini-2.5-flash-lite (0.579)
```

## Links

- **Tutorial Documentation**: [docs/tutorial/22_model_selection.md](../../docs/tutorial/22_model_selection.md)
- **ADK Documentation**: <https://github.com/google/adk-python>
- **Gemini API Documentation**: <https://ai.google.dev/gemini-api/docs/models>
- **Vertex AI Gemini**: <https://cloud.google.com/vertex-ai/docs/generative-ai/models>

## Contributing

This implementation follows ADK best practices:

- ✅ Root agent exported as `root_agent`
- ✅ Tools return structured dicts with `status` and `report`
- ✅ Comprehensive test coverage
- ✅ Standard project structure
- ✅ Environment configuration via `.env.example`

## License

Part of the ADK Training repository. See main repository LICENSE for details.

---

**🎉 Tutorial 22 Complete!** You now have a working model selection
framework. Ready to optimize your AI applications!
