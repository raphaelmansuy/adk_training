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

**Total: 47 tests**

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
Get a free key at: https://aistudio.google.com/app/apikey

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
```

### Testing
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

**Agent:** "For real-time voice chat applications, I recommend **gemini-2.0-flash-live**. This model is specifically designed for:

- ✅ Real-time bidirectional streaming
- ✅ Low latency audio processing
- ✅ Multimodal voice + text interactions

This is the only model in the Gemini family that supports live, bidirectional streaming, making it ideal for voice assistants and real-time conversational applications."

### Benchmark Output

```
======================================================================
BENCHMARKING: gemini-2.5-flash
======================================================================

✅ Query: What is the capital of France?...
   Latency: 0.85s, Tokens: ~8
✅ Query: Explain quantum computing in simple terms...
   Latency: 1.23s, Tokens: ~95
...

📊 RESULTS:
   Avg Latency: 1.03s
   Avg Tokens: 41
   Success Rate: 100.0%
   Cost Estimate: $0.000003 per query
   Quality Score: 0.493

======================================================================
COMPARISON SUMMARY
======================================================================

Model                            Latency   Tokens       Cost    Quality
----------------------------------------------------------------------
gemini-2.5-flash                    1.03s       41 $0.000003      0.493
gemini-2.0-flash                    0.98s       39 $0.000004      0.505
gemini-1.5-flash                    0.86s       37 $0.000003      0.537

======================================================================

🎯 RECOMMENDATIONS:

⚡ Fastest: gemini-1.5-flash (0.86s)
💰 Cheapest: gemini-2.5-flash ($0.000003)
🏆 Best Quality: gemini-1.5-flash (0.537)
```

## Links

- **Tutorial Documentation**: [docs/tutorial/22_model_selection.md](../../docs/tutorial/22_model_selection.md)
- **ADK Documentation**: https://github.com/google/adk-python
- **Gemini API Documentation**: https://ai.google.dev/gemini-api/docs/models
- **Vertex AI Gemini**: https://cloud.google.com/vertex-ai/docs/generative-ai/models

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

**🎉 Tutorial 22 Complete!** You now have a working model selection framework. Ready to optimize your AI applications!
