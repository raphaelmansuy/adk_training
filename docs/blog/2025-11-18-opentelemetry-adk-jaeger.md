---
title: "Observing ADK Agents: OpenTelemetry Tracing with Jaeger"
authors: [adk-team]
tags: [adk, opentelemetry, jaeger, observability, tracing, debugging]
---

You build an AI agent with Google ADK. It works. But when you ask
**"Why did the agent choose that tool?"** or **"Which LLM call took
5 seconds?"** – you're flying blind.

Enter **distributed tracing**: Jaeger visualizes every step your agent
takes, from reasoning to tool execution to LLM calls. ADK has
**built-in OpenTelemetry support**, making this a breeze... once you
understand one crucial gotcha.

This post shows you the complete picture: what to do, why it matters,
and the one thing that trips up most developers.

<!--truncate-->

## The Problem We're Solving

Your agent runs. But where does the time go?

```text
Input: "What is 123 + 456?"
│
├─ Agent reasoning (planning which tool)    ⏱️ 0.5s
├─ LLM call to Gemini                       ⏱️ 1.2s
├─ Tool execution (add_numbers)             ⏱️ 0.1s
├─ Final response generation                ⏱️ 0.8s
│
Output: "579"
```

Without tracing, you never see this breakdown. With Jaeger, you get a
flame graph showing every millisecond.

## Quick Start: 5 Minutes

### 1. Start Jaeger (Docker)

```bash
docker run -d --name jaeger \
  -e COLLECTOR_OTLP_ENABLED=true \
  -p 16686:16686 -p 4318:4318 \
  jaegertracing/all-in-one:latest
```

### 2. Install Dependencies

```bash
pip install google-adk opentelemetry-sdk \
  opentelemetry-exporter-otlp-proto-http
```

### 3. Copy the Tutorial

```bash
cd til_opentelemetry_jaeger_20251118
make setup
cp .env.example .env  # Add GOOGLE_GENAI_API_KEY
```

### 4. Run and Observe

```bash
make demo                # See traces exported automatically
```

### 5. View in Jaeger

Open [http://localhost:16686](http://localhost:16686) → Select
`google-adk-math-agent` → Click "Find Traces"

**You now have complete observability.** That's it.

## The Real Challenge: TracerProvider Conflicts

Here's where most developers get stuck:

### ❌ This Doesn't Work (With `adk web`)

```python
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry import trace

# You manually create a provider
provider = TracerProvider()
# ... add your exporter ...
trace.set_tracer_provider(provider)

# Meanwhile, adk web already started and:
# 1. Started FastAPI server
# 2. Initialized its own TracerProvider
# 3. Now your set_tracer_provider() call fails silently

# Result: Your custom exporter never gets used ❌
```

**Why?** OpenTelemetry enforces: *"One global TracerProvider per
process."* ADK initializes first (in `adk web` mode), so you can't
override it. Your exporter gets ignored, and traces never reach
Jaeger.

### ✅ The Solution: Environment Variables

Instead of fighting for control, **let ADK initialize everything**:

```bash
# Set these environment variables
export OTEL_SERVICE_NAME=google-adk-math-agent
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
export OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf

# Now start adk web - it reads env vars and configures OTel automatically
adk web .
```

**In your agent code**, just set the same env vars in your config:

```python
import os

os.environ.setdefault("OTEL_SERVICE_NAME", "google-adk-math-agent")
os.environ.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318")
os.environ.setdefault("OTEL_EXPORTER_OTLP_PROTOCOL", "http/protobuf")

# ADK (v1.17.0+) reads these and configures everything
# Your code runs on top of ADK's already-initialized provider
# No conflicts! ✓
```

This is the **recommended approach** in ADK v1.17.0+.

## Alternative: Manual Setup (For Standalone Scripts)

If you're **not** using `adk web`, you have full control:

```python
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry import trace

# Initialize FIRST (before any ADK imports)
provider = TracerProvider()
processor = BatchSpanProcessor(
    OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# NOW import ADK (uses your provider)
from google.adk.agents import Agent
# ... rest of your agent code ...
```

**Why this works**: You control initialization order. Provider is
set before ADK runs.

**When to use this**: Standalone scripts, custom sampling, or
detailed control over span processors.

## What You Get in Jaeger

When you query `google-adk-math-agent` in Jaeger, you see:

```text
Invocation (root)
├─ invoke_agent
│  ├─ call_llm (user question)
│  │  └─ 🕐 1.2s ← Gemini API latency
│  ├─ execute_tool (add_numbers)
│  │  └─ result: 579
│  └─ call_llm (final response)
│     └─ 🕐 0.8s
└─ SUCCESS ✓
```

Each span includes:

- **Exact timing** (microsecond precision)
- **Tool inputs/outputs** (what arguments were passed)
- **LLM prompts and responses** (if not redacted)
- **Error traces** (if something failed)

This is invaluable for debugging:

- "Why did the agent pick the wrong tool?" → See the LLM reasoning
- "Why is my system slow?" → Flame graph shows the bottleneck
- "Did the tool actually run?" → See the span execution timing

## Two Approaches at a Glance

| Scenario | Approach | Code |
|----------|----------|------|
| Using `adk web` | Environment variables | `os.environ["OTEL_..."]` |
| Standalone script | Manual setup | `trace.set_tracer_provider()` |
| Need custom sampling | Manual setup | Control `TracerProvider` directly |
| Local development | Either | Both work equally well |

## Common Issues

**Q: Traces not appearing in Jaeger?**  
A: Check Jaeger is running (`docker ps`), and verify `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318`

**Q: I see warnings about "Overriding TracerProvider"?**  
A: You're using manual setup with `adk web`. Switch to environment variables instead.

**Q: Can I use this in production?**  
A: Yes. Export to Google Cloud Trace, Honeycomb, Datadog, or any
OTLP-compatible backend by changing the endpoint.

## The Real Tutorial

This blog post is the high-level "why." For the complete working
example with tests, see:

📚 **[OpenTelemetry + ADK + Jaeger Tutorial](https://github.com/google/adk-python/tree/main/til_opentelemetry_jaeger_20251118)**

- 42 unit tests
- Both approaches demonstrated
- Production-ready configuration
- Makefile automation
- Troubleshooting guide

## Summary

✓ **ADK has excellent OTel support out of the box**  
✓ **Use environment variables for `adk web` mode** (no conflicts)  
✓ **Use manual setup for standalone scripts** (full control)  
✓ **Jaeger visualizes everything: reasoning, LLM calls, tool execution**  
✓ **Works locally and in production (change the endpoint)**  

The "black box" of AI agents becomes fully observable. Debug with confidence.

Happy tracing! 🔍


