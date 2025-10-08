# Tutorial 23: Production Deployment Strategies

**Goal**: Master production deployment patterns including local servers, Cloud Run, Agent Engine, and GKE deployments with best practices for scalability, reliability, and monitoring.

**Prerequisites**:

- Tutorial 01 (Hello World Agent)
- Tutorial 18 (Events & Observability)
- Tutorial 22 (Model Selection)
- Basic understanding of Docker and Kubernetes (optional)

**What You'll Learn**:

- Local API server with `adk api_server`
- Cloud Run deployment with `adk deploy cloud_run`
- Vertex AI Agent Engine deployment
- Google Kubernetes Engine (GKE) deployment
- Environment configuration management
- Scaling and load balancing strategies
- Monitoring and health checks
- CI/CD integration patterns

**Time to Complete**: 60-75 minutes

---

## Why Production Deployment Matters

**Problem**: Development agents need robust, scalable deployment infrastructure for production use.

**Solution**: **ADK deployment tools** provide streamlined paths from development to production across multiple platforms.

**Benefits**:

- 🚀 **One-Command Deployment**: Deploy with ADK CLI
- 📈 **Auto-Scaling**: Handle variable load automatically
- 🛡️ **Reliability**: Health checks, retries, failover
- 📊 **Monitoring**: Built-in observability
- 💰 **Cost Optimization**: Pay for actual usage
- 🔐 **Security**: Authentication, authorization, encryption

**Deployment Options**:

- **Local Server**: Development and testing
- **Cloud Run**: Serverless, auto-scaling
- **Agent Engine**: Managed agent infrastructure (Vertex AI)
- **GKE**: Full Kubernetes control
- **Custom**: Your own infrastructure

---

## 1. Local API Server

### Starting Local Server

```bash
# Start local FastAPI server
adk api_server

# Custom port
adk api_server --port 8090

# Custom host
adk api_server --host 0.0.0.0 --port 8080

# With specific agent file
adk api_server --agent agent.py
```

### Server Features

- **FastAPI** backend
- **Automatic API docs** at `/docs`
- **Health check** endpoint at `/health`
- **Agent invocation** endpoint at `/invoke`
- **CORS** enabled for web clients
- **Hot reload** in development mode

### Testing Local Server

```bash
# Health check
curl http://localhost:8080/health

# Invoke agent
curl -X POST http://localhost:8080/invoke \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello, world!"}'
```

### Custom Server Implementation

```python
"""
Custom FastAPI server with ADK agent.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.adk.agents import Agent, Runner
from google.genai import types
import os

# Environment setup
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = '1'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'your-project-id'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'

app = FastAPI(title="ADK Agent API", version="1.0")

# Create agent
agent = Agent(
    model='gemini-2.0-flash',
    name='api_agent',
    instruction="You are a helpful API assistant."
)

runner = Runner()


class QueryRequest(BaseModel):
    """Request model for agent invocation."""
    query: str
    temperature: float = 0.7
    max_tokens: int = 1024


class QueryResponse(BaseModel):
    """Response model for agent invocation."""
    response: str
    model: str
    tokens: int


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "adk-agent-api"}


@app.post("/invoke", response_model=QueryResponse)
async def invoke_agent(request: QueryRequest):
    """
    Invoke agent with query.
    
    Args:
        request: Query and configuration
    
    Returns:
        Agent response
    """
    
    try:
        # Update agent config if needed
        agent.generate_content_config = types.GenerateContentConfig(
            temperature=request.temperature,
            max_output_tokens=request.max_tokens
        )
        
        # Run agent
        result = await runner.run_async(request.query, agent=agent)
        
        # Extract response
        response_text = result.content.parts[0].text
        
        # Estimate tokens
        token_count = len(response_text.split())
        
        return QueryResponse(
            response=response_text,
            model=agent.model,
            tokens=token_count
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "ADK Agent API",
        "endpoints": {
            "health": "/health",
            "invoke": "/invoke (POST)",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

---

## 2. Cloud Run Deployment

### Automated Cloud Run Deployment

```bash
# Deploy to Cloud Run (one command)
adk deploy cloud_run \
  --project your-project-id \
  --region us-central1 \
  --service-name my-agent-service

# Deploy with custom configuration
adk deploy cloud_run \
  --project your-project-id \
  --region us-central1 \
  --service-name my-agent-service \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 100 \
  --min-instances 1
```

### Manual Cloud Run Deployment

**Step 1: Create Dockerfile**

```dockerfile
# Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent code
COPY . .

# Expose port
EXPOSE 8080

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Start server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
```

**Step 2: Create requirements.txt**

```
google-adk>=0.5.0
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
google-cloud-aiplatform>=1.38.0
```

**Step 3: Build and Deploy**

```bash
# Build container
gcloud builds submit --tag gcr.io/your-project-id/agent-service

# Deploy to Cloud Run
gcloud run deploy agent-service \
  --image gcr.io/your-project-id/agent-service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 100 \
  --min-instances 1 \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=your-project-id,GOOGLE_CLOUD_LOCATION=us-central1"
```

### Cloud Run Configuration

```yaml
# service.yaml (Cloud Run configuration)

apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: agent-service
  namespace: 'your-project-id'
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: '1'
        autoscaling.knative.dev/maxScale: '100'
        run.googleapis.com/cpu-throttling: 'false'
    spec:
      containerConcurrency: 80
      timeoutSeconds: 300
      containers:
      - image: gcr.io/your-project-id/agent-service
        ports:
        - containerPort: 8080
        env:
        - name: GOOGLE_CLOUD_PROJECT
          value: 'your-project-id'
        - name: GOOGLE_CLOUD_LOCATION
          value: 'us-central1'
        - name: GOOGLE_GENAI_USE_VERTEXAI
          value: '1'
        resources:
          limits:
            memory: 2Gi
            cpu: '2'
```

---

## 3. Vertex AI Agent Engine Deployment

### Agent Engine Overview

**Agent Engine** is a fully managed service for deploying and scaling agents on Vertex AI.

**Benefits**:

- Managed infrastructure
- Built-in scaling
- Integrated monitoring
- Version management
- A/B testing support

### Deploy to Agent Engine

```bash
# Deploy agent to Agent Engine
adk deploy agent_engine \
  --project your-project-id \
  --region us-central1 \
  --agent-name my-production-agent

# Deploy with specific configuration
adk deploy agent_engine \
  --project your-project-id \
  --region us-central1 \
  --agent-name my-production-agent \
  --model gemini-2.0-flash \
  --max-instances 50
```

### Agent Engine Configuration

```python
"""
Configure agent for Agent Engine deployment.
"""

from google.cloud import aiplatform
from google.adk.agents import Agent
from google.genai import types

# Initialize Vertex AI
aiplatform.init(
    project='your-project-id',
    location='us-central1'
)

# Create agent for deployment
agent = Agent(
    model='gemini-2.0-flash',
    name='production_agent',
    instruction="""
You are a production assistant helping customers with inquiries.
    """.strip(),
    generate_content_config=types.GenerateContentConfig(
        temperature=0.5,
        max_output_tokens=2048
    )
)

# Deploy to Agent Engine
# (ADK handles deployment details)
```

---

## 4. Google Kubernetes Engine (GKE) Deployment

### Kubernetes Deployment

**Step 1: Create Kubernetes manifests**

```yaml
# deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-service
  labels:
    app: agent-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agent-service
  template:
    metadata:
      labels:
        app: agent-service
    spec:
      containers:
      - name: agent-service
        image: gcr.io/your-project-id/agent-service:latest
        ports:
        - containerPort: 8080
        env:
        - name: GOOGLE_CLOUD_PROJECT
          value: "your-project-id"
        - name: GOOGLE_CLOUD_LOCATION
          value: "us-central1"
        - name: GOOGLE_GENAI_USE_VERTEXAI
          value: "1"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: agent-service
spec:
  type: LoadBalancer
  selector:
    app: agent-service
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: agent-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: agent-service
  minReplicas: 3
  maxReplicas: 100
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

**Step 2: Deploy to GKE**

```bash
# Create GKE cluster
gcloud container clusters create agent-cluster \
  --region us-central1 \
  --machine-type n1-standard-2 \
  --num-nodes 3 \
  --enable-autoscaling \
  --min-nodes 3 \
  --max-nodes 10

# Get credentials
gcloud container clusters get-credentials agent-cluster \
  --region us-central1

# Deploy application
kubectl apply -f deployment.yaml

# Check status
kubectl get pods
kubectl get services
kubectl get hpa

# View logs
kubectl logs -l app=agent-service --follow
```

---

## 5. Environment Configuration

### Environment Variables

```bash
# .env file (DO NOT COMMIT)

# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_USE_VERTEXAI=1

# Application Configuration
MODEL=gemini-2.0-flash
TEMPERATURE=0.5
MAX_TOKENS=2048

# Monitoring
ENABLE_TRACING=true
LOG_LEVEL=INFO

# Security
API_KEY=your-secret-api-key
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### Configuration Management

```python
"""
Configuration management with environment variables.
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Application configuration."""
    
    # Google Cloud
    project_id: str
    location: str
    use_vertexai: bool
    
    # Model
    model: str
    temperature: float
    max_tokens: int
    
    # Monitoring
    enable_tracing: bool
    log_level: str
    
    # Security
    api_key: Optional[str]
    allowed_origins: list[str]
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Load configuration from environment variables."""
        
        return cls(
            project_id=os.environ['GOOGLE_CLOUD_PROJECT'],
            location=os.environ.get('GOOGLE_CLOUD_LOCATION', 'us-central1'),
            use_vertexai=os.environ.get('GOOGLE_GENAI_USE_VERTEXAI', '1') == '1',
            
            model=os.environ.get('MODEL', 'gemini-2.0-flash'),
            temperature=float(os.environ.get('TEMPERATURE', '0.5')),
            max_tokens=int(os.environ.get('MAX_TOKENS', '2048')),
            
            enable_tracing=os.environ.get('ENABLE_TRACING', 'false').lower() == 'true',
            log_level=os.environ.get('LOG_LEVEL', 'INFO'),
            
            api_key=os.environ.get('API_KEY'),
            allowed_origins=os.environ.get('ALLOWED_ORIGINS', '').split(',')
        )


# Usage
config = Config.from_env()

agent = Agent(
    model=config.model,
    generate_content_config=types.GenerateContentConfig(
        temperature=config.temperature,
        max_output_tokens=config.max_tokens
    )
)
```

---

## 6. Monitoring and Health Checks

### Health Check Implementation

```python
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

# Track service metrics
service_start_time = datetime.now()
request_count = 0
error_count = 0


@app.get("/health")
async def health_check():
    """Comprehensive health check."""
    
    uptime = (datetime.now() - service_start_time).total_seconds()
    
    # Check critical dependencies
    vertex_ai_healthy = check_vertex_ai_connection()
    
    health_status = {
        "status": "healthy" if vertex_ai_healthy else "degraded",
        "uptime_seconds": uptime,
        "request_count": request_count,
        "error_count": error_count,
        "error_rate": error_count / request_count if request_count > 0 else 0,
        "dependencies": {
            "vertex_ai": "healthy" if vertex_ai_healthy else "unhealthy"
        }
    }
    
    return health_status


def check_vertex_ai_connection() -> bool:
    """Check Vertex AI connectivity."""
    try:
        # Attempt simple API call
        # aiplatform.gapic.ModelServiceClient()
        return True
    except Exception:
        return False


@app.middleware("http")
async def track_requests(request, call_next):
    """Middleware to track requests."""
    global request_count, error_count
    
    request_count += 1
    
    response = await call_next(request)
    
    if response.status_code >= 400:
        error_count += 1
    
    return response
```

---

## 7. Best Practices

### ✅ DO: Use Secrets Manager

```python
from google.cloud import secretmanager

def get_secret(secret_id: str) -> str:
    """Retrieve secret from Secret Manager."""
    
    client = secretmanager.SecretManagerServiceClient()
    
    project_id = os.environ['GOOGLE_CLOUD_PROJECT']
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    
    response = client.access_secret_version(request={"name": name})
    
    return response.payload.data.decode('UTF-8')


# Use secret
api_key = get_secret('api-key')
```

### ✅ DO: Implement Rate Limiting

```python
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time

# Simple rate limiter
rate_limit_store = {}

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    """Rate limiting middleware."""
    
    client_ip = request.client.host
    current_time = time.time()
    
    if client_ip in rate_limit_store:
        last_request, count = rate_limit_store[client_ip]
        
        # Reset if more than 60 seconds
        if current_time - last_request > 60:
            rate_limit_store[client_ip] = (current_time, 1)
        else:
            # Check rate limit (100 requests per minute)
            if count >= 100:
                return JSONResponse(
                    status_code=429,
                    content={"error": "Rate limit exceeded"}
                )
            
            rate_limit_store[client_ip] = (last_request, count + 1)
    else:
        rate_limit_store[client_ip] = (current_time, 1)
    
    response = await call_next(request)
    return response
```

### ✅ DO: Enable Structured Logging

```python
import logging
import json

class JSONFormatter(logging.Formatter):
    """JSON log formatter for Cloud Logging."""
    
    def format(self, record):
        log_obj = {
            "timestamp": self.formatTime(record),
            "severity": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_obj)


# Configure logging
logger = logging.getLogger("agent-service")
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)


# Usage
logger.info("Agent invoked", extra={"query_id": "123", "user_id": "user-456"})
```

---

## Summary

You've mastered production deployment:

**Key Takeaways**:

- ✅ `adk api_server` for local development
- ✅ `adk deploy cloud_run` for serverless deployment
- ✅ `adk deploy agent_engine` for managed agents
- ✅ GKE for full Kubernetes control
- ✅ Environment configuration management
- ✅ Health checks and monitoring
- ✅ Secrets management and rate limiting

**Production Checklist**:

- [ ] Deployment strategy selected
- [ ] Environment variables configured
- [ ] Secrets stored in Secret Manager
- [ ] Health checks implemented
- [ ] Monitoring and logging configured
- [ ] Rate limiting enabled
- [ ] Auto-scaling configured
- [ ] CI/CD pipeline setup
- [ ] Disaster recovery plan documented

**Next Steps**:

- **Tutorial 24**: Master Advanced Observability
- **Tutorial 25**: Explore Best Practices & Patterns

**Resources**:

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Agent Engine Documentation](https://cloud.google.com/vertex-ai/docs/agent-builder)
- [GKE Documentation](https://cloud.google.com/kubernetes-engine/docs)

---

**🎉 Tutorial 23 Complete!** You now know how to deploy agents to production. Continue to Tutorial 24 to learn about advanced observability patterns.
