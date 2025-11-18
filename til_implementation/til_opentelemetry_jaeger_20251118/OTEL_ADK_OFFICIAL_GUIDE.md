# Official Google ADK OpenTelemetry Configuration Guide

Based on official source code from `research/adk-python/src/google/adk/telemetry/`

## Overview

Google ADK provides built-in OpenTelemetry integration for comprehensive observability of AI agents. This guide explains the official configuration patterns and how to properly set up traces, logs, and metrics.

## Official ADK Telemetry Architecture

### Key Components

ADK's telemetry system consists of three main signal types:

1. **Traces**: Distributed request tracing (primary signal for agents)
2. **Logs**: Structured logging correlated with traces
3. **Metrics**: Performance measurements (optional)

### Official Semantic Conventions

ADK follows OpenTelemetry Semantic Conventions v1.37+ for GenAI systems:

```python
# From research/adk-python/src/google/adk/telemetry/tracing.py
GEN_AI_AGENT_NAME = 'gen_ai.agent.name'
GEN_AI_AGENT_DESCRIPTION = 'gen_ai.agent.description'
GEN_AI_CONVERSATION_ID = 'gen_ai.conversation.id'
GEN_AI_OPERATION_NAME = 'gen_ai.operation.name'
GEN_AI_TOOL_NAME = 'gen_ai.tool.name'
GEN_AI_TOOL_DESCRIPTION = 'gen_ai.tool.description'
GEN_AI_TOOL_TYPE = 'gen_ai.tool.type'
GEN_AI_TOOL_CALL_ID = 'gen_ai.tool.call.id'
```

### Automatic Instrumentation

ADK automatically instruments:

- ✅ **Agent Invocations**: `invoke_agent` spans with agent metadata
- ✅ **Tool Calls**: `execute_tool` spans with arguments and responses
- ✅ **LLM Requests**: Model, tokens used, finish reasons
- ✅ **Data Exchange**: Input/output data (configurable)

## Official Setup Pattern

### 1. Basic Telemetry Setup (Traces Only)

From `research/adk-python/src/google/adk/telemetry/setup.py`:

```python
from google.adk.telemetry import setup

# Setup with standard OTLP exporter (uses env variables)
setup.maybe_set_otel_providers(
    otel_hooks_to_setup=[
        # Will auto-detect OTEL_EXPORTER_OTLP_ENDPOINT env var
    ]
)
```

### 2. Local Development with Jaeger

**For this tutorial (recommended):**

```python
# otel_config.py - Initialize before any ADK imports
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry import trace

# Create resource
resource = Resource(attributes={
    "service.name": "my-adk-agent",
    "service.version": "1.0.0",
})

# Create provider with OTLP exporter
provider = TracerProvider(resource=resource)
exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
processor = BatchSpanProcessor(exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# In your main agent module
# math_agent/agent.py
from otel_config import initialize_otel
initialize_otel()  # Must be FIRST!

from google.adk.agents import Agent
# ... rest of agent code
```

### 3. With Logging (Recommended for Production)

From `research/adk-python/src/google/adk/telemetry/setup.py`:

```python
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry import _logs, _events
from opentelemetry.sdk._events import EventLoggerProvider

# Create logger provider
logger_provider = LoggerProvider(resource=resource)

# Add OTLP exporter for logs
log_exporter = OTLPLogExporter(
    endpoint="http://localhost:4318/v1/logs"
)
processor = BatchLogRecordProcessor(log_exporter)
logger_provider.add_log_record_processor(processor)
_logs.set_logger_provider(logger_provider)

# Enable events for gen_ai semantic conventions
event_logger_provider = EventLoggerProvider(logger_provider)
_events.set_event_logger_provider(event_logger_provider)
```

### 4. Google Cloud Integration (Production)

For Cloud Trace, Cloud Logging, Cloud Monitoring:

```python
from google.adk.telemetry.google_cloud import (
    get_gcp_exporters,
    get_gcp_resource
)
from google.adk.telemetry.setup import maybe_set_otel_providers

# Get GCP exporters (uses Application Default Credentials)
gcp_hooks = get_gcp_exporters(
    enable_cloud_tracing=True,
    enable_cloud_metrics=True,
    enable_cloud_logging=True,
)

# Get resource with GCP attributes
resource = get_gcp_resource(project_id="my-project")

# Setup all providers
maybe_set_otel_providers(
    otel_hooks_to_setup=[gcp_hooks],
    otel_resource=resource,
)
```

## Control Span Content

### Privacy: Disable Sensitive Data in Spans

```python
import os

# Disable request/response content in spans
# Useful when handling PII or sensitive information
os.environ["ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS"] = "false"

# Now spans will have empty {} for:
# - gcp.vertex.agent.llm_request
# - gcp.vertex.agent.llm_response
# - gcp.vertex.agent.tool_call_args
# - gcp.vertex.agent.tool_response
```

Default: `true` (backward compatible)

## Environment Variables for OTLP

ADK respects standard OpenTelemetry environment variables:

```bash
# Standard OTLP configuration
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf

# Separate endpoints (override OTEL_EXPORTER_OTLP_ENDPOINT)
export OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://localhost:4318/v1/traces
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://localhost:4318/v1/metrics
export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://localhost:4318/v1/logs

# Resource attributes (service name, version, etc.)
export OTEL_RESOURCE_ATTRIBUTES=service.name=my-agent,service.version=1.0.0
export OTEL_SERVICE_NAME=my-agent
```

## What Gets Traced: Official Span Hierarchy

### invoke_agent (Root Span)

```
invoke_agent (ADK Agent Invocation)
├── attributes:
│   ├── gen_ai.agent.name = "math_assistant"
│   ├── gen_ai.agent.description = "Math helper..."
│   ├── gen_ai.conversation.id = "<session-id>"
│   ├── gen_ai.operation.name = "invoke_agent"
│   └── gcp.vertex.agent.invocation_id = "<invocation-id>"
│
├── call_llm (LLM Request)
│   ├── gen_ai.system = "gcp.vertex.agent"
│   ├── gen_ai.request.model = "gemini-2.5-flash"
│   ├── gen_ai.request.top_p = 0.9
│   ├── gen_ai.request.max_tokens = 8192
│   ├── gen_ai.usage.input_tokens = 150
│   ├── gen_ai.usage.output_tokens = 45
│   ├── gcp.vertex.agent.llm_request = "{...}"
│   └── gcp.vertex.agent.llm_response = "{...}"
│
├── execute_tool (Tool Call)
│   ├── gen_ai.tool.name = "add_numbers"
│   ├── gen_ai.tool.description = "Add two numbers..."
│   ├── gen_ai.tool.type = "FunctionTool"
│   ├── gen_ai.tool.call.id = "<tool-call-id>"
│   ├── gcp.vertex.agent.tool_call_args = "{...}"
│   └── gcp.vertex.agent.tool_response = "{...}"
│
└── send_data
    ├── gcp.vertex.agent.data = "{...}"
    └── gcp.vertex.agent.event_id = "<event-id>"
```

## What's NOT Traced (by design)

From official source code comments:

- ❌ `gen_ai.agent.id`: Unclear semantics (global vs scope-local)
- ❌ `gen_ai.data_source.id`: Not available in ADK models
- ❌ `server.*` attributes: Pending framework confirmation

## Viewing Traces in Jaeger

### Finding Your Traces

1. **Service dropdown**: Select "google-adk-math-agent" (or your service name)
2. **Look for**: Spans named `invoke_agent` (root) with `execute_tool` children
3. **Attributes panel**: Shows all gen_ai semantic convention data

### Common Trace Inspection Tasks

| Task | How |
|------|-----|
| See tool calls | Expand `execute_tool` spans under `invoke_agent` |
| View LLM request | Look at `call_llm` span attributes |
| Check token usage | `gen_ai.usage.input_tokens` and `gen_ai.usage.output_tokens` |
| See tool arguments | Expand `gcp.vertex.agent.tool_call_args` |
| Get conversation ID | Search by `gen_ai.conversation.id` attribute |

## Integration with Python Logging

For better visibility, add Python logging handler:

```python
import logging

# Get logger after OTel setup
logger = logging.getLogger("my_agent")

# Logs will automatically include trace context in structured logging
logger.info("Agent started", extra={"user_id": "123"})

# In Jaeger, logs can be correlated with trace_id/span_id
```

## Testing Your Configuration

```python
# Verify traces are being sent
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("test_span") as span:
    span.set_attribute("test", "value")
    print("Check Jaeger UI for test_span")

# Verify logger provider
from opentelemetry import _logs
logger_provider = _logs.get_logger_provider()
print(f"Logger provider: {logger_provider}")
```

## Performance Considerations

### BatchSpanProcessor (Recommended)

```python
# Used in this tutorial
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Advantages:
# ✅ Batches spans for efficiency
# ✅ Reduces network overhead
# ✅ Async export (non-blocking)
# ✅ Can handle burst traffic
processor = BatchSpanProcessor(exporter)
```

### Configuration Options

```python
# Custom batch settings
processor = BatchSpanProcessor(
    exporter,
    max_queue_size=2048,  # Max spans buffered
    batch_size=512,       # Export when batch reaches this size
    schedule_delay_millis=5000,  # Export every 5 seconds
)
```

## Troubleshooting

### Spans Not Appearing in Jaeger

1. **Check Jaeger is running**: `docker ps | grep jaeger`
2. **Verify endpoint**: OTLP endpoint should be reachable
3. **Check service name**: Make sure filter matches your `service.name`
4. **Enable debug logging**:
   ```python
   os.environ["OTEL_LOG_LEVEL"] = "DEBUG"
   ```

### "Overriding of current TracerProvider is not allowed"

This warning appears when:
- OTel provider already set before calling `trace.set_tracer_provider()`
- Multiple initialization calls in same process

**Solution**: Only initialize once, at application startup

### PII Data in Spans

**Disable with**:
```python
os.environ["ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS"] = "false"
```

## Official References

Source files referenced:
- `research/adk-python/src/google/adk/telemetry/setup.py` - Core setup functions
- `research/adk-python/src/google/adk/telemetry/tracing.py` - Semantic conventions
- `research/adk-python/src/google/adk/telemetry/google_cloud.py` - GCP integration

Official OpenTelemetry Docs:
- [OpenTelemetry Semantic Conventions for GenAI](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
- [OTLP Exporter Documentation](https://opentelemetry.io/docs/languages/python/exporting-data/)

## Next Steps

1. **Run your agent** and check Jaeger UI: `http://localhost:16686`
2. **Export to Cloud Trace** for production using `get_gcp_exporters()`
3. **Add custom spans** for domain-specific operations
4. **Monitor metrics** with Cloud Monitoring or Prometheus

## Example: Complete Setup

See `math_agent/otel_config.py` in this tutorial for a complete, production-ready example with:
- ✅ Traces to Jaeger
- ✅ Logs with OTel integration
- ✅ Events for gen_ai semantic conventions
- ✅ Python logging handler
- ✅ Privacy controls
