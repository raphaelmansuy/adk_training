# Tutorial 23: Production Deployment

Production deployment agent demonstrating deployment strategies and best practices for ADK agents.

## Overview

This implementation showcases production-ready patterns including:

- **Local API Server**: FastAPI development server
- **Cloud Run Deployment**: Serverless auto-scaling
- **Agent Engine Deployment**: Managed agent infrastructure
- **GKE Deployment**: Custom Kubernetes control
- **Best Practices**: Security, monitoring, scalability

## Quick Start

### 1. Setup

```bash
# Install dependencies
make setup

# Configure environment
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### 2. Run Development Server

```bash
# Set API key
export GOOGLE_API_KEY=your_api_key

# Start ADK web interface
make dev
```

Open http://localhost:8000 and select `production_deployment_agent` from the dropdown.

### 3. Run Tests

```bash
make test
```

## Features

### Agent Tools

The agent provides three specialized tools:

1. **check_deployment_status**: Verify deployment health and status
2. **get_deployment_options**: Get available deployment strategies
3. **get_best_practices**: Learn production best practices

### Custom FastAPI Server

The implementation includes a production-ready FastAPI server:

```bash
# Start custom server
python -m uvicorn production_agent.server:app --reload

# Visit API docs
open http://localhost:8000/docs
```

Features:

- Health check endpoint at `/health`
- Agent invocation at `/invoke`
- Request metrics tracking
- Error handling and logging
- OpenAPI documentation

📖 **Guide**: [FastAPI Best Practices](./FASTAPI_BEST_PRACTICES.md) - learn 7 core patterns.

## Deployment Options

### 1. Local API Server

```bash
adk api_server
```

Features:

- Hot reload for development
- Automatic API docs
- CORS enabled

### 2. Cloud Run

```bash
adk deploy cloud_run \
  --project your-project-id \
  --region us-central1
```

Features:

- Serverless auto-scaling
- Pay-per-use pricing
- Managed infrastructure

### 3. Agent Engine

```bash
adk deploy agent_engine \
  --project your-project-id \
  --region us-central1
```

Features:

- Managed agent infrastructure
- Built-in monitoring
- Version control

### 4. GKE (Kubernetes)

```bash
adk deploy gke
```

Features:

- Full Kubernetes control
- Custom scaling policies
- Advanced networking

## Example Prompts

Try these prompts with the agent:

```
"What deployment options are available?"
"How do I deploy to Cloud Run?"
"What are the best practices for production?"
"Show me security best practices"
"How do I configure auto-scaling?"
"What's the difference between Cloud Run and Agent Engine?"
```

## Best Practices

### Security

- Use Google Secret Manager for secrets
- Never commit API keys
- Configure CORS with specific origins
- Implement rate limiting

### Monitoring

- Add health check endpoints
- Use structured logging (JSON)
- Enable Cloud Trace
- Track error rates and latency

### Scalability

- Configure auto-scaling
- Set resource limits
- Use connection pooling
- Optimize memory usage

### Reliability

- Implement graceful shutdown
- Add liveness/readiness probes
- Use circuit breakers
- Configure retries with backoff

## Project Structure

```
tutorial23/
├── production_agent/
│   ├── __init__.py          # Package initialization
│   ├── agent.py             # Agent definition with tools
│   └── server.py            # Custom FastAPI server
├── tests/
│   ├── test_structure.py    # Project structure tests
│   ├── test_imports.py      # Import validation
│   ├── test_agent.py        # Agent configuration tests
│   └── test_server.py       # Server endpoint tests
├── pyproject.toml           # Project configuration
├── requirements.txt         # Dependencies
├── Makefile                 # Common commands
├── .env.example            # Environment template
└── README.md               # This file
```

## Testing

Run the comprehensive test suite:

```bash
# All tests
make test

# Specific test file
pytest tests/test_agent.py -v

# With coverage report
pytest tests/ -v --cov=production_agent --cov-report=html
```

Test coverage includes:

- ✅ Project structure validation
- ✅ Import verification
- ✅ Agent configuration
- ✅ Tool functionality
- ✅ Server endpoints
- ✅ Request/response models
- ✅ Health checks
- ✅ Metrics tracking

## Environment Variables

See `.env.example` for all available configuration options:

```bash
# Required
GOOGLE_API_KEY=your-api-key

# Optional (for Vertex AI)
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=1

# Server configuration
PORT=8080
HOST=0.0.0.0
```

## Resources

- [Tutorial 23 Documentation](../../docs/tutorial/23_production_deployment.md)
- [ADK Deployment Guide](https://google.github.io/adk-docs/deploy/)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/docs/agent-engine)

## Troubleshooting

### "Agent not found in dropdown"

Make sure you've installed the package:

```bash
pip install -e .
```

### "GOOGLE_API_KEY not set"

Export your API key:

```bash
export GOOGLE_API_KEY=your_key
```

### "Module not found"

Install dependencies:

```bash
make setup
```

## Next Steps

- **Tutorial 24**: Advanced Observability
- **Tutorial 25**: Best Practices & Patterns
- Try deploying to Cloud Run with your own agent
- Explore Agent Engine managed deployment
