---
title: "Using OpenTelemetry with Google ADK AI Agents and Visualizing Traces in Jaeger"
authors: [adk_team]
tags: [adk, opentelemetry, observability, jaeger, tracing, agents]
---

Google's **Agent Development Kit (ADK)** is an open-source Python framework for building sophisticated AI agents and multi-agent systems. It is powered by Gemini models by default but is model-agnostic. ADK has **built-in OpenTelemetry (OTel) instrumentation** that automatically creates traces for key agent actions: LLM calls, tool executions, planning steps, agent runs, etc.

This makes it extremely easy to observe the internal reasoning flow of your agents (e.g., why a tool was called, what prompt was sent to the model, latencies).

By default, when running locally, traces are only in-memory (visible in console or ADK's dev UI). To persist and visualize them in tools like **Jaeger**, you just need to configure an OTLP exporter.

This tutorial shows a complete end-to-end example:

1. Install ADK and dependencies
2. Build a simple AI agent with tools
3. Run Jaeger (all-in-one) with Docker
4. Configure OpenTelemetry to export traces to Jaeger via OTLP
5. Run the agent and view beautiful hierarchical traces in Jaeger UI

<!--truncate-->

## Step 1: Install ADK and OpenTelemetry Packages

```bash
pip install google-adk[all]  # or git+https://github.com/google/adk-python.git for latest
pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-http
```

> Note: ADK already depends on `opentelemetry-api`, so you only need the SDK and exporter.

You also need a Google AI API key (for Gemini):

```bash
export GOOGLE_GENAI_API_KEY=your-key-here
# or use google-auth for GCP
```

## Step 2: Create a Simple ADK Agent

Create a file `math_agent.py`:

```python
# Initialize OpenTelemetry FIRST (before any ADK imports)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry import trace

resource = Resource(attributes={
    "service.name": "google-adk-math-agent",
    "service.version": "0.1.0"
})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces"))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Now import ADK
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

# Define tools
def add_numbers(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

# Create agent with tools
root_agent = Agent(
    name="math_assistant",
    model="gemini-2.5-flash",
    description="A helpful math assistant.",
    instruction="You are a helpful math assistant. Use tools when asked to perform calculations.",
    tools=[FunctionTool(func=add_numbers)],
)
```

This agent will:
- Receive the question
- Reason → decide to call the `add_numbers` tool
- Call the tool
- Return the answer

ADK automatically creates OTel spans for all these steps.

## Step 3: Start Jaeger (All-in-One)

The easiest way is the official Jaeger all-in-one Docker image:

```bash
docker run -d --name jaeger \
  -e COLLECTOR_OTLP_ENABLED=true \
  -p 16686:16686 \
  -p 4317:4317 \
  -p 4318:4318 \
  jaegertracing/all-in-one:latest
```

## Step 4: Run the Agent

```bash
python math_agent.py
```

Expected output:

```
Final answer: 579
```

## Step 5: View Traces in Jaeger

1. Open Jaeger UI at http://localhost:16686
2. Select service: `google-adk-math-agent`
3. Click "Find Traces"
4. Click any trace to see hierarchical span details

You will see spans like:

- Agent planning
- Tool selection and execution
- LLM calls to Gemini
- Response generation

## Bonus: Run with ADK Dev UI

Instead of `InMemoryRunner`, use `adk web .` in your agent folder – it starts a nice chat UI and still exports traces to Jaeger exactly the same way.

## Cleanup

```bash
docker rm -f jaeger
```

## Summary

- ADK has **excellent out-of-the-box OpenTelemetry instrumentation** – no manual `@trace` decorators needed.
- To send traces anywhere (Jaeger, Tempo, Zipkin, Google Cloud Trace, Honeycomb, etc.), just configure the global `TracerProvider` with an OTLP exporter before importing ADK.
- Works locally, in containers, Cloud Run, Vertex AI Agent Engine, or on-prem.

This setup turns the "black box" of AI agents into a fully observable, debuggable system – essential for production.

Happy agent building! 🚀
