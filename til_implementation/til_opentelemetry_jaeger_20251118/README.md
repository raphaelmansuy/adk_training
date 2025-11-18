# OpenTelemetry + ADK + Jaeger

Distributed tracing for AI agents using Google ADK, OpenTelemetry, and Jaeger visualization.

## What is Jaeger?

Jaeger is an open-source distributed tracing system that visualizes agent execution flow:

```
Your Agent        Jaeger Backend       Jaeger UI
┌─────────┐      ┌──────────────┐    ┌──────────────┐
│ ADK     │ OTLP │ Span         │    │ Interactive  │
│ Agent   ├─────>│ Collector    │    │ Trace View   │
│ Running │      │ (Docker)     │    │ Flamegraph   │
└─────────┘      └──────────────┘    │ Latency      │
                                     │ Dependencies │
                                     └──────────────┘
                                      http://localhost:16686
```

**Why Jaeger matters**: Debug agent behavior, find bottlenecks, and verify LLM calls in one place.

## Quick Start (3 Steps)

### 1. Setup

```bash
make setup
cp .env.example .env  # Add your GOOGLE_GENAI_API_KEY
```

### 2. Start Jaeger

```bash
make jaeger-up  # Opens UI at http://localhost:16686
```

### 3. Run Agent

```bash
make demo          # Demo script with sample queries
# OR
make web           # Interactive web UI at http://localhost:8000
```

View traces: Select `google-adk-math-agent` service in Jaeger and click "Find Traces".

## How It Works

```
┌──────────────────────────────────────────────────────┐
│ You Ask Agent a Question                             │
└────────────┬─────────────────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────────────────┐
│ Agent Runs (ADK + Gemini)                            │
│  • Plans response                                    │
│  • Calls math tools (add, multiply, etc.)            │
│  • Gets results                                      │
│  • Formats final answer                              │
└────────────┬─────────────────────────────────────────┘
             │
             ▼ (OpenTelemetry)
┌──────────────────────────────────────────────────────┐
│ Export Traces (OTLP HTTP)                            │
│  • Span: invoke_agent (2.5s)                         │
│  • Span: call_llm (1.2s)                             │
│  • Span: execute_tool (0.1s)                         │
└────────────┬─────────────────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────────────────┐
│ Jaeger Receives Traces (localhost:4318)              │
│  • Stores in backend                                 │
│  • Indexes by service & time                         │
└────────────┬─────────────────────────────────────────┘
             │
             ▼
┌──────────────────────────────────────────────────────┐
│ View in Jaeger UI (localhost:16686)                  │
│  • Flame graph visualization                         │
│  • Find bottlenecks                                  │
│  • Debug failures                                    │
└──────────────────────────────────────────────────────┘
```

## Project Structure

```
til_opentelemetry_jaeger_20251118/
├── math_agent/
│   ├── __init__.py          # Package marker
│   ├── agent.py             # Main ADK agent (root_agent export)
│   ├── otel_config.py       # OpenTelemetry initialization
│   └── tools.py             # Math tool implementations
├── tests/
│   ├── __init__.py
│   └── test_agent.py        # Comprehensive test suite (30+ tests)
├── Makefile                 # Standard commands
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project metadata
├── .env.example            # Environment template
└── README.md               # This file
```

## Key Concepts

### OpenTelemetry with ADK: Two Approaches

This tutorial demonstrates **both approaches** that work with ADK v1.17.0+:

```
APPROACH 1: adk web (Recommended)      APPROACH 2: Demo Script
─────────────────────────────────────  ─────────────────────
1. Set environment variables           1. Call initialize_otel()
2. adk web loads agent.py              2. Manually create provider
3. ADK reads env vars                  3. Add OTLP exporter
4. ADK creates TracerProvider          4. Set as global provider
5. Your code inherits it ✓             5. Run agent ✓
   (No conflicts!)                        (Full control!)
```

#### ✅ Approach 1: Environment Variables (Recommended for `adk web`)

Let ADK's built-in OpenTelemetry support handle everything:

```bash
# Set environment variables
export OTEL_SERVICE_NAME=google-adk-math-agent
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true

# Run adk web - ADK automatically configures OTel
adk web .
```

**Why this works with `adk web`**:

- ADK initializes its own TracerProvider before loading agents
- We can't override it once set (OpenTelemetry limitation)
- Solution: Set environment variables and let ADK use them
- The `Makefile` does this automatically: `make web`

**In your agent code**:

```python
from math_agent.otel_config import initialize_otel_env

# Just configure env vars - ADK does the rest
initialize_otel_env(
    service_name="google-adk-math-agent",
    jaeger_endpoint="http://localhost:4318/v1/traces",
)
```

#### ✅ Approach 2: Manual Setup (For Standalone Demo)

Manually initialize TracerProvider in your code:

```python
from math_agent.otel_config import initialize_otel

# Full manual control - works for demo scripts
tracer_provider, logger_provider = initialize_otel(
    service_name="google-adk-math-agent",
    jaeger_endpoint="http://localhost:4318/v1/traces"
)
```

**Why this works for demo**:

- You control initialization order completely
- TracerProvider is set BEFORE ADK imports happen
- No conflict with ADK's provider

**When to use**:

- Standalone scripts (`python -m math_agent.agent`)
- Detailed control over span processors
- Need custom sampling or exporters

### Important: The TracerProvider Conflict

⚠️ **Key Learning**: OpenTelemetry only allows ONE global TracerProvider per process.

When using `adk web`:

1. ADK FastAPI server starts first
2. ADK automatically initializes a TracerProvider
3. If your agent code tries to set another one → warning → ignored
4. Your custom Jaeger exporter never gets attached!

**Solution**: Use environment variables (Approach 1). ADK reads them and
configures everything correctly.

### Code Organization

The `otel_config.py` module provides both approaches:

```python
# Recommended for adk web - just sets env vars
from math_agent.otel_config import initialize_otel_env
initialize_otel_env()

# OR detailed control - for standalone scripts
from math_agent.otel_config import initialize_otel
tracer_provider, logger_provider = initialize_otel()

# Call after agent runs to flush spans to Jaeger
from math_agent.otel_config import force_flush
force_flush()
```



### Math Agent

The `agent.py` module defines the root agent with 4 tools:

- `add_numbers(a, b)` - Addition
- `subtract_numbers(a, b)` - Subtraction
- `multiply_numbers(a, b)` - Multiplication
- `divide_numbers(a, b)` - Division (with zero-check)

The agent uses Gemini-2.5-Flash and receives automatic OTel
instrumentation for:

- Agent planning steps
- Tool selections and calls
- LLM requests to Gemini
- Tool execution timing
- Final response generation

### Trace Structure in Jaeger

When you run the agent, Jaeger captures a complete trace hierarchy:

```
Invocation (root span)
├─ invoke_agent
│  ├─ call_llm (user query)
│  │  └─ 🕐 ~1.5s (Gemini API)
│  ├─ execute_tool (add_numbers)
│  │  └─ result: 579
│  └─ call_llm (final answer)
│     └─ 🕐 ~2s
└─ status: SUCCESS ✓
```

**What you see in Jaeger UI**:
- Flame graph (span duration visualization)
- Exact timing for each operation
- Tool input/output data
- LLM prompts and responses
- Error stack traces (if any)

## Testing

```bash
make test                                          # Run all tests with coverage
pytest tests/test_agent.py::TestToolFunctions -v  # Specific test class
```

**Coverage**: 42 unit tests covering tool functions, OTel setup, edge cases, and documentation.

## Configuration

### Environment Variables

Create `.env` from `.env.example`:

```bash
# Required
GOOGLE_GENAI_API_KEY=your-api-key-here

# Optional (defaults provided)
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318/v1/traces
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_SERVICE_NAME=google-adk-math-agent
OTEL_SERVICE_VERSION=0.1.0
```

### Jaeger Endpoints

**Local Docker (all-in-one)**:
- OTLP HTTP: `http://localhost:4318/v1/traces`
- OTLP gRPC: `localhost:4317`
- Query UI: http://localhost:16686

**Remote Jaeger**:
```python
initialize_otel(jaeger_endpoint="http://jaeger.company.com:4318/v1/traces")
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No traces in Jaeger | Check: `docker ps \| grep jaeger` and verify OTEL_EXPORTER_OTLP_ENDPOINT is `http://localhost:4318` |
| API key error | Set GOOGLE_GENAI_API_KEY in `.env` file |
| Import errors | Run `make setup` to install all dependencies |
| Span batching slow | Reduce `schedule_delay_millis` in BatchSpanProcessor or use sampling for high-volume traces |

## Commands

```bash
make setup          # Install dependencies
make jaeger-up      # Start Jaeger container (http://localhost:16686)
make jaeger-down    # Stop Jaeger
make demo           # Run demo script
make web            # Start ADK web UI (http://localhost:8000)
make test           # Run all tests
make clean          # Remove cache files
make help           # Show all commands
```

## Resources

- [ADK Documentation](https://github.com/google/adk-python)
- [OpenTelemetry Instrumentation](https://opentelemetry.io/docs/instrumentation/python/)
- [Jaeger UI Guide](https://www.jaegertracing.io/docs/)
