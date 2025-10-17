# Tutorial 23: Production Deployment Strategies

**Goal**: Deploy production-grade agents with auto-scaling, monitoring, and reliability patterns across local servers, Cloud Run, Vertex AI, and Kubernetes.

**Prerequisites**:
- Tutorial 01 (Hello World Agent)
- Google Cloud Platform account
- Basic Docker knowledge (helpful)

**What You'll Learn**:
- 🚀 Deploy agents with one command (`adk deploy`)
- 🏗️ Build production FastAPI servers with health checks
- 📊 Monitor and observe agent systems
- 🔐 Manage secrets and configuration
- 📈 Auto-scale across platforms
- 🛡️ Implement reliability patterns

**Time to Complete**: 45 minutes

---

## What You'll Build

This tutorial includes a **complete, production-ready implementation**:

```
tutorial23/
├── production_agent/
│   ├── agent.py              # Agent with 3 tools
│   └── server.py             # FastAPI server (488 lines!)
├── tests/                    # 40 comprehensive tests
├── Makefile                  # Make setup, dev, test, demo
├── FASTAPI_BEST_PRACTICES.md # 7 core patterns guide
└── README.md                 # Full documentation
```

**Key Features**:
- ✅ Production-ready FastAPI server with auth, logging, timeouts
- ✅ Configuration management (pydantic BaseSettings)
- ✅ Health checks with metrics tracking
- ✅ Error handling and validation
- ✅ Structured logging with request tracing
- ✅ 40 passing tests (93% coverage)
- ✅ Makefile with helpful commands

📖 **Full Implementation**: [View on GitHub →](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial23)

---

## Quick Start (5 minutes)

```bash
cd tutorial_implementation/tutorial23

# Setup
make setup

# Run development server
export GOOGLE_API_KEY=your_key
make dev

# Run tests
make test

# See demos
make demo-info
```

**Open** `http://localhost:8000` and select `production_deployment_agent` from dropdown.

---

## Deployment Strategies

ADK supports multiple deployment paths. Choose based on your needs:

### Comparison Matrix

| Strategy | Setup Time | Scaling | Cost | Best For |
|----------|-----------|---------|------|----------|
| **Local** | < 1 min | Manual | Free | Development |
| **Cloud Run** | 5 mins | Auto | Pay-per-use | Most apps |
| **Agent Engine** | 10 mins | Auto | Pay-per-use | Enterprise |
| **GKE** | 20 mins | Manual | Hourly | Complex |

---

## 1. Local Development

**Perfect for**: Quick testing and iteration

```bash
# Start FastAPI server
adk api_server

# Custom port
adk api_server --port 8090
```

Test it:
```bash
curl http://localhost:8080/health
curl -X POST http://localhost:8080/invoke \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello!"}'
```

**Features**:
- 🔄 Hot reload during development
- 📖 Auto-generated API docs at `/docs`
- ⚡ Instant feedback loop

See [tutorial implementation](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial23) for custom server code.

---

## 2. Cloud Run (Recommended for Most Apps)

**Perfect for**: Serverless auto-scaling with minimal ops

```bash
# Deploy in one command
adk deploy cloud_run \
  --project your-project-id \
  --region us-central1 \
  --service-name my-agent
```

That's it! ADK handles:
- ✅ Building container image
- ✅ Pushing to Container Registry
- ✅ Deploying to Cloud Run
- ✅ Setting up auto-scaling

**Manual Alternative**:
```bash
# 1. Build
gcloud builds submit --tag gcr.io/YOUR_PROJECT/agent

# 2. Deploy
gcloud run deploy agent \
  --image gcr.io/YOUR_PROJECT/agent \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --max-instances 100
```

**Cost**: ~$0.40 per million requests + compute

---

## 3. Vertex AI Agent Engine

**Perfect for**: Managed agent infrastructure with built-in versioning

```bash
# Deploy to managed service
adk deploy agent_engine \
  --project your-project-id \
  --region us-central1 \
  --agent-name my-agent
```

**Benefits**:
- 📦 Managed infrastructure
- 🎯 Version control
- 🔄 A/B testing
- 📊 Built-in monitoring
- 🔐 Enterprise security

---

## 4. Google Kubernetes Engine (GKE)

**Perfect for**: Complex deployments needing full control

```bash
# Create cluster
gcloud container clusters create agent-cluster \
  --region us-central1 \
  --machine-type n1-standard-2 \
  --num-nodes 3

# Get credentials
gcloud container clusters get-credentials agent-cluster \
  --region us-central1

# Deploy
kubectl apply -f deployment.yaml
```

**When to use GKE**:
- Need advanced networking
- Running multiple services
- Existing Kubernetes expertise
- Custom orchestration requirements

See tutorial implementation for full Kubernetes manifests.

---

## Deployment Flow Diagram

```
YOUR AGENT CODE
       |
       v
+-------------------+
| adk deploy XXXX   |
+-------------------+
       |
       +-------+-------+-------+-------+
       |       |       |       |       |
       v       v       v       v       v
     LOCAL  CLOUD-RUN  AGENT-ENG  GKE  CUSTOM
       |       |         |        |      |
       v       v         v        v      v
  localhost  serverless  managed  k8s  your-infra
```

---

## Production Setup

### Environment Configuration

Create `.env` file (never commit!):

```bash
# Google Cloud
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=1

# Application
MODEL=gemini-2.0-flash
TEMPERATURE=0.5
MAX_TOKENS=2048

# Security
API_KEY=your-secret-key
ALLOWED_ORIGINS=https://yourdomain.com

# Monitoring
LOG_LEVEL=INFO
ENABLE_TRACING=true
```

### Health Checks

All deployments should expose `/health` endpoint:

```json
GET /health

{
  "status": "healthy",
  "uptime_seconds": 3600,
  "request_count": 1250,
  "error_count": 3,
  "error_rate": 0.0024,
  "metrics": {
    "successful_requests": 1247,
    "timeout_count": 0
  }
}
```

**Configure in orchestrator**:
- **Cloud Run**: Automatically detected
- **GKE**: Set as liveness probe
- **Agent Engine**: Built-in

### Secrets Management

**Never** commit API keys to code. Use Google Secret Manager:

```python
from google.cloud import secretmanager

def get_secret(secret_id: str) -> str:
    client = secretmanager.SecretManagerServiceClient()
    project = os.environ['GOOGLE_CLOUD_PROJECT']
    name = f"projects/{project}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode('UTF-8')

# Usage
api_key = get_secret('api-key')
```

---

## Monitoring & Observability

### Key Metrics to Track

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Error Rate | < 0.5% | > 5% |
| P99 Latency | < 2 sec | > 5 sec |
| Availability | > 99.9% | < 99% |
| Request Count | Track | N/A |

### Structured Logging

All production servers should log JSON to stdout:

```json
{
  "timestamp": "2025-01-17T10:30:45Z",
  "severity": "INFO",
  "message": "invoke_agent.success",
  "request_id": "550e8400-e29b",
  "tokens": 245,
  "latency_ms": 1230
}
```

Cloud Logging automatically parses and indexes these fields.

---

## Best Practices

### 🔐 Security

- [ ] Use API keys from Secret Manager, never hardcode
- [ ] Enable authentication in production
- [ ] Configure CORS for specific origins, never use wildcard
- [ ] Use HTTPS everywhere
- [ ] Implement rate limiting
- [ ] Set up Cloud Audit Logs

### 📊 Observability

- [ ] Export logs to Cloud Logging
- [ ] Set up error tracking with Error Reporting
- [ ] Monitor metrics with Cloud Monitoring
- [ ] Use request IDs for tracing
- [ ] Log important business events

### ⚡ Reliability

- [ ] Set request timeouts (30s recommended)
- [ ] Implement health checks
- [ ] Configure auto-scaling appropriately
- [ ] Use load balancing
- [ ] Plan for disaster recovery

### 📈 Performance

- [ ] Use connection pooling
- [ ] Stream responses when possible
- [ ] Cache agent configuration
- [ ] Monitor memory usage
- [ ] Use multiple workers

---

## FastAPI Best Practices

This implementation demonstrates **7 core production patterns**:

1. **Configuration Management** - Environment-based settings
2. **Authentication & Security** - Bearer token validation
3. **Health Checks** - Real metrics-based status
4. **Request Lifecycle** - Timeout protection
5. **Error Handling** - Typed exceptions
6. **Logging & Observability** - Request tracing
7. **Metrics & Monitoring** - Observable systems

📖 **Full Guide**: [FastAPI Best Practices for ADK Agents →](../../tutorial_implementation/tutorial23/FASTAPI_BEST_PRACTICES.md)

This guide includes:
- ✅ Code examples for each pattern
- ✅ ASCII diagrams showing flows
- ✅ Production checklist
- ✅ Common pitfalls (❌ Don't / ✅ Do)
- ✅ Deployment examples

---

## Common Patterns

### Pattern: Gradual Rollout

```
Deploy to Cloud Run
       |
       v
Traffic: 5% (canary)
       |
       v
Monitor for 1 hour
       |
       +------ Error Rate High? -----> ROLLBACK
       |
       +------ Healthy? -------> 25% traffic
                                  |
                                  v
                               Monitor
                                  |
                                  +---> 100% traffic
```

### Pattern: Zero-Downtime Deployment

**Blue-Green Deployment**:
```
CURRENT (Blue)          NEW (Green)
   |                        |
   +----> BOTH ACTIVE <-----+
   |           |            |
   +--- LB routes traffic ---+
   |                        |
   +-- Health checks OK? ---|
           |                |
         YES                NO
           |                |
           v                v
        Blue OFF       Rollback (Blue ON)
        Green ON           Green OFF
```

---

## Troubleshooting

### Agent Not Found in Dropdown

**Problem**: `adk web agent_name` fails

**Solution**: Install as package first
```bash
pip install -e .
adk web  # Then select from dropdown
```

### `GOOGLE_API_KEY Not Set`

```bash
export GOOGLE_API_KEY=your_key
# Or in Cloud Run: Set env var in Cloud Console
```

### High Latency

Check:
1. Request timeout setting
2. Agent complexity (use streaming)
3. Resource limits (increase CPU)
4. Model selection (try `gemini-2.0-flash`)

### Memory Issues

- Reduce max_tokens
- Enable request streaming
- Use connection pooling
- Monitor with Cloud Profiler

---

## Quick Reference

### CLI Commands

```bash
# Local
adk api_server --port 8080

# Deploy
adk deploy cloud_run --project PROJECT --region REGION
adk deploy agent_engine --project PROJECT --region REGION
adk deploy gke

# List deployments
adk list deployments
```

### Environment Variables

```
GOOGLE_CLOUD_PROJECT       # GCP project ID
GOOGLE_CLOUD_LOCATION      # Region (us-central1)
GOOGLE_GENAI_USE_VERTEXAI  # Use Vertex AI (1 or 0)
MODEL                      # Model name
API_KEY                    # Secret key for auth
REQUEST_TIMEOUT            # Timeout in seconds
```

### Endpoints

```
GET  /                  # API info
GET  /health            # Health check + metrics
POST /invoke            # Agent invocation
GET  /docs              # OpenAPI docs
```

---

## Summary

**You now know**:
- ✅ Deploy locally for development
- ✅ Deploy to Cloud Run for most production apps
- ✅ Use Agent Engine for managed infrastructure
- ✅ Use GKE for complex deployments
- ✅ Configure and secure production systems
- ✅ Monitor and observe agent systems
- ✅ Implement reliability patterns

**Deployment Checklist**:
- [ ] Environment variables configured
- [ ] Secrets in Secret Manager
- [ ] Health checks working
- [ ] Monitoring/logging setup
- [ ] Auto-scaling configured
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Error handling tested
- [ ] Disaster recovery planned

**Next Steps**:

- **Tutorial 24**: [Advanced Observability](./24_advanced_observability.md) - Deep observability patterns
- **Tutorial 25**: [Best Practices & Patterns](./25_best_practices.md) - Production patterns
- 🚀 Deploy your own agent to production!

---

## Resources

- 📚 [Tutorial Implementation →](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial23)
- 📖 [FastAPI Best Practices Guide →](../../tutorial_implementation/tutorial23/FASTAPI_BEST_PRACTICES.md)
- 🌐 [Cloud Run Docs](https://cloud.google.com/run/docs)
- 🤖 [Agent Engine Docs](https://cloud.google.com/vertex-ai/docs/agent-engine)
- ⚙️ [GKE Docs](https://cloud.google.com/kubernetes-engine/docs)
- 🔐 [Secret Manager](https://cloud.google.com/secret-manager/docs)

---

**🎉 Tutorial 23 Complete!** You're now ready to deploy agents to production. Proceed to Tutorial 24 for advanced observability.
