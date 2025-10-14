# Tutorial 24: Advanced Observability & Monitoring

Enterprise-grade observability system demonstrating ADK's plugin architecture for comprehensive monitoring, metrics collection, alerting, and performance profiling.

## Features

- **SaveFilesAsArtifactsPlugin**: Automatic artifact storage for debugging
- **MetricsCollectorPlugin**: Comprehensive request/response metrics
- **AlertingPlugin**: Real-time error detection and alerting
- **PerformanceProfilerPlugin**: Detailed performance analysis
- **Production Monitoring System**: Complete monitoring solution

## Quick Start

### 1. Setup

```bash
# Install dependencies
make setup

# Set up authentication (choose one method)

# Method 1: API Key (Gemini API)
export GOOGLE_API_KEY=your_api_key_here

# Method 2: Service Account (VertexAI)
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_LOCATION=us-central1
```

### 2. Run the Agent

```bash
# Start ADK web interface
make dev

# Open http://localhost:8000
# Select 'observability_agent' from dropdown
```

### 3. Try Demo Prompts

```bash
# See demo instructions
make demo
```

## What You'll Learn

### Plugin System

The ADK plugin system allows modular observability without modifying agent code:

```python
runner = InMemoryRunner(
    agent=agent,
    app_name='my_app',
    plugins=[
        SaveFilesAsArtifactsPlugin(),
        MetricsCollectorPlugin(),
        AlertingPlugin(),
        PerformanceProfilerPlugin()
    ]
)
```

### Custom Plugins

Create custom plugins by extending `BasePlugin`:

```python
from google.adk.plugins import BasePlugin

class MetricsCollectorPlugin(BasePlugin):
    async def on_request_start(self, request_id: str, agent: Agent, query: str):
        # Track request start
        pass
    
    async def on_request_complete(self, request_id: str, result):
        # Collect metrics
        pass
```

### Cloud Trace Integration

Enable Cloud Trace for distributed tracing:

```bash
# Deploy with tracing
adk deploy cloud_run --trace_to_cloud

# Local testing with tracing
adk web --trace_to_cloud
```

## Project Structure

```
tutorial24/
├── observability_agent/       # Agent implementation
│   ├── __init__.py
│   └── agent.py              # Main agent with plugins
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_agent.py
│   ├── test_imports.py
│   ├── test_plugins.py
│   └── test_structure.py
├── pyproject.toml           # Package configuration
├── requirements.txt         # Dependencies
├── Makefile                # Commands
├── .env.example           # Environment template
└── README.md             # This file
```

## Running Tests

```bash
# Run all tests with coverage
make test

# Run specific test file
pytest tests/test_plugins.py -v

# Run with detailed output
pytest tests/ -vv --tb=long
```

## Key Concepts

### Observability Pillars

1. **Traces**: Request flow through system
2. **Metrics**: Quantitative measurements
3. **Logs**: Detailed event records
4. **Events**: State changes and actions

### Plugin Lifecycle

1. `on_request_start()` - Request begins
2. `on_tool_call_start()` - Tool execution begins
3. `on_tool_call_complete()` - Tool execution completes
4. `on_request_complete()` - Request succeeds
5. `on_request_error()` - Request fails

### Metrics Collected

- **Request Metrics**: Total, success rate, latency
- **Performance**: Token counts, tool call duration
- **Errors**: Error rates, consecutive failures
- **Alerts**: Threshold violations, anomalies

## Production Deployment

### Cloud Trace Setup

```bash
# Deploy to Cloud Run with tracing
adk deploy cloud_run \
  --project your-project-id \
  --region us-central1 \
  --trace_to_cloud

# Deploy to Agent Engine
adk deploy agent_engine \
  --project your-project-id \
  --region us-central1 \
  --trace_to_cloud
```

### Monitoring Dashboard

View traces in Cloud Console:
```
https://console.cloud.google.com/traces?project=your-project-id
```

## Troubleshooting

### Common Issues

**Plugin not working?**
- Ensure plugins are registered in Runner/App constructor
- Check plugin lifecycle methods are implemented correctly

**No metrics collected?**
- Verify plugin is in plugins list
- Check async/await syntax in lifecycle methods

**Cloud Trace not showing?**
- Use `--trace_to_cloud` CLI flag
- Ensure Google Cloud project is configured
- Check IAM permissions for Cloud Trace

## Resources

- [Tutorial 24 Documentation](../../docs/tutorial/24_advanced_observability.md)
- [ADK Plugin System](https://github.com/google/adk-python)
- [Cloud Trace Documentation](https://cloud.google.com/trace/docs)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/)

## Next Steps

After mastering observability:
- **Tutorial 25**: Best Practices & Patterns (Final Tutorial!)

---

**🎉 Congratulations!** You now understand advanced observability patterns for production agent systems.
