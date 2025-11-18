# OpenTelemetry + ADK + Jaeger Tutorial

**Complete example of distributed tracing with Google's Agent Development Kit (ADK), OpenTelemetry instrumentation, and Jaeger visualization.**

This tutorial demonstrates how to:

1. Build a simple AI agent using ADK
2. Configure OpenTelemetry to export traces to Jaeger
3. Visualize agent execution flow, LLM calls, and tool execution in Jaeger UI
4. Debug and observe multi-step agent reasoning

## Quick Start

### Prerequisites

- Python 3.10+
- Docker (for running Jaeger)
- Google API key (for Gemini models)

### Setup

```bash
# Clone and navigate to tutorial
cd til_opentelemetry_jaeger_20251118

# Install dependencies
make setup

# Copy environment template
cp .env.example .env
# Edit .env and add your GOOGLE_GENAI_API_KEY
```

### Run Jaeger (Local Docker)

```bash
docker run -d --name jaeger \
  -e COLLECTOR_OTLP_ENABLED=true \
  -p 16686:16686 \
  -p 4317:4317 \
  -p 4318:4318 \
  jaegertracing/all-in-one:latest
```

Open Jaeger UI: http://localhost:16686

### Run the Agent

```bash
# Run demo with sample queries
make demo

# Or run with Python directly
python -m math_agent.agent
```

### View Traces in Jaeger

1. Go to http://localhost:16686
2. Select service: `google-adk-math-agent`
3. Click "Find Traces"
4. Click any trace to see hierarchical span details

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

### OpenTelemetry Initialization

The `otel_config.py` module handles OTel setup:

```python
from math_agent.otel_config import initialize_otel

# Must be called BEFORE importing ADK
initialize_otel(
    service_name="google-adk-math-agent",
    service_version="0.1.0",
    jaeger_endpoint="http://localhost:4318/v1/traces"
)
```

**Important**: OTel initialization must happen before any ADK imports, or early spans will be missed.

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

When you run the agent, you'll see traces like:

```
Agent.run (root span)
├── planner (reasoning step)
├── tool_call: add_numbers (tool execution)
│   └── function execution (actual computation)
├── generate_content (Gemini API call)
│   └── prompt/response (if not redacted)
└── response generation
```

Each span includes:
- Execution duration
- Attributes (tool name, input/output)
- Status (success/error)
- Logs and events

## Testing

Run the comprehensive test suite:

```bash
# Run all tests with coverage
make test

# Run specific test class
pytest tests/test_agent.py::TestToolFunctions -v

# Run specific test
pytest tests/test_agent.py::TestToolFunctions::test_add_numbers_positive -v
```

**Test Coverage**:
- ✅ 30+ unit tests for math operations
- ✅ Edge cases (division by zero, large numbers, type mixing)
- ✅ OTel initialization and configuration
- ✅ Span processor setup
- ✅ Tracer creation and usage
- ✅ Tool documentation validation

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

## Production Considerations

This tutorial demonstrates the basics. For production:

### Add These Features

1. **Retry Logic**
   ```python
   from tenacity import retry, stop_after_attempt, wait_exponential
   
   @retry(stop=stop_after_attempt(3), wait=wait_exponential())
   async def run_agent_with_retries(query):
       ...
   ```

2. **Rate Limiting**
   ```python
   from ratelimit import limits, RateLimitException
   
   @limits(calls=60, period=60)
   async def run_agent_limited(query):
       ...
   ```

3. **Circuit Breaker**
   ```python
   from pybreaker import CircuitBreaker
   
   breaker = CircuitBreaker(
       fail_max=5,
       reset_timeout=60
   )
   
   @breaker
   async def run_agent_safe(query):
       ...
   ```

4. **Structured Logging**
   ```python
   import logging
   import uuid
   
   logger = logging.getLogger(__name__)
   correlation_id = uuid.uuid4()
   
   logger.info(
       "agent_started",
       extra={
           "correlation_id": correlation_id,
           "query": query,
           "timestamp": datetime.utcnow().isoformat(),
       }
   )
   ```

5. **Cost Tracking**
   ```python
   class CostTracker:
       def __init__(self):
           self.total_cost = 0.0
       
       def record(self, tokens: int, cost_per_1m: float):
           cost = (tokens / 1_000_000) * cost_per_1m
           self.total_cost += cost
           return cost
   ```

6. **Authentication/Authorization**
   ```python
   async def run_agent_secure(user_id: str, query: str):
       if not user.has_permission(f"agent:math"):
           raise PermissionError(f"User {user_id} cannot access math agent")
       ...
   ```

## Troubleshooting

### Traces not appearing in Jaeger

**Check**:
1. Jaeger is running: `docker ps | grep jaeger`
2. OTLP endpoint is correct (default: `http://localhost:4318/v1/traces`)
3. OTel initialization happens before ADK imports
4. No errors in agent console output

**Debug**:
```bash
# Check Jaeger connectivity
curl http://localhost:16686/api/services

# Verify OTel configuration
python -c "
from math_agent.otel_config import initialize_otel
import os
provider = initialize_otel()
print('OTEL_EXPORTER_OTLP_ENDPOINT:', os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT'))
print('Provider:', provider)
"
```

### Agent not generating spans

**Check**:
1. Agent is using correct LLM (gemini-2.5-flash)
2. Google API key is set and valid
3. OpenTelemetry SDK is installed: `pip show opentelemetry-sdk`
4. Exporter is installed: `pip show opentelemetry-exporter-otlp-proto-http`

### Memory/Performance Issues

**Optimization**:
1. Adjust batch size in `BatchSpanProcessor`:
   ```python
   BatchSpanProcessor(
       exporter,
       max_queue_size=2048,  # Default: 2048
       max_export_batch_size=512,  # Default: 512
       schedule_delay_millis=5000,  # Default: 5000
   )
   ```

2. Use sampling to reduce trace volume:
   ```python
   from opentelemetry.sdk.trace.sampler import TraceIdRatioBased
   
   provider = TracerProvider(
       sampler=TraceIdRatioBased(0.1),  # Sample 10% of traces
       resource=resource
   )
   ```

## Common Commands

```bash
# Setup
make setup                    # Install dependencies

# Launch ADK Web UI (interactive chat)
make web                      # Access at http://localhost:8000

# Jaeger Management
make jaeger-up                # Start Jaeger (Docker required)
                              # UI at http://localhost:16686
make jaeger-down              # Stop and remove Jaeger
make jaeger-status            # Check if Jaeger is running

# Development
make demo                     # Run demo with sample queries

# Testing
make test                     # Run all tests with coverage

# Cleanup
make clean                    # Remove cache and artifacts

# Help
make help                     # Show all commands with descriptions
```

## Learning Resources

- [ADK Documentation](https://github.com/google/adk-python)
- [OpenTelemetry Python Docs](https://opentelemetry.io/docs/instrumentation/python/)
- [Jaeger UI Guide](https://www.jaegertracing.io/docs/latest/frontend-ui/)
- [OTLP Specification](https://opentelemetry.io/docs/specs/otel/protocol/)

## Blog Post

This tutorial is documented in the blog post:
[Using OpenTelemetry with Google ADK AI Agents and Visualizing Traces in Jaeger](../../../docs/blog/2025-11-18-opentelemetry-adk-jaeger.md)

## License

MIT License - See LICENSE file

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review ADK documentation: https://github.com/google/adk-python
3. Check OpenTelemetry docs: https://opentelemetry.io
4. Review Jaeger docs: https://www.jaegertracing.io
