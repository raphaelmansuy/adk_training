# FastAPI Best Practices for ADK Agents

A concise guide to exposing Google ADK agents via FastAPI with production-grade patterns.

## Why FastAPI?

- **Async Native**: Built for Python async/await with ADK's streaming responses
- **Automatic Docs**: OpenAPI/Swagger docs generated automatically
- **Type Safety**: Full type hints with Pydantic validation
- **Performance**: One of the fastest Python web frameworks
- **Developer Experience**: Minimal boilerplate, maximum clarity

## 7 Core Patterns

The following diagram shows how the 7 patterns work together in a production FastAPI server:

```
    CLIENT REQUEST
          |
          v
    +-----------+
    | CORS      |  Pattern 1: Security
    +-----------+
          |
          v
    +-----------+
    | AUTH      |  Pattern 2: Authentication
    +-----------+
          |
          v
    +-----------+
    | VALIDATE  |  Pattern 5: Error Handling
    +-----------+
          |
          v
    +-----------+
    | TIMEOUT   |  Pattern 4: Reliability
    | + INVOKE  |
    +-----------+
          |
          v
    +-----------+
    | LOGGING   |  Pattern 6: Observability
    +-----------+
          |
          v
    +-----------+
    | METRICS   |  Pattern 7: Monitoring
    +-----------+
          |
          v
    CLIENT RESPONSE + TRACING
```

All patterns are configured via **Pattern 1: Settings** (pydantic BaseSettings)

### 1. Configuration Management

Use `pydantic.BaseSettings` to manage environment-based configuration:

Configuration hierarchy (top to bottom priority):

```
PRIORITY LEVELS:

1. ENVIRONMENT VARIABLES
   (e.g., PORT=8080, API_KEY=xyz)
            |
            v
2. .env FILE
   (e.g., .env.production)
            |
            v
3. CLASS DEFAULTS
   (e.g., port: int = 8000)
            |
            v
4. TYPE DEFAULTS
   (string, int, bool, etc.)
```

All three levels are checked in order, first match wins.

Use `pydantic.BaseSettings` to manage environment-based configuration:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My Agent API"
    environment: str = os.getenv("ENVIRONMENT", "development")
    api_key: Optional[str] = os.getenv("API_KEY", None)
    enable_auth: bool = os.getenv("ENABLE_AUTH", "false").lower() == "true"
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "30"))

    class Config:
        env_file = ".env"

settings = Settings()
```

**Benefits:**

- Externalizes configuration (12-factor app)
- Type-checked settings
- Environment variable support with defaults
- Easy testing with override

### 2. Authentication & Security

Implement Bearer token validation for production:

```python
from fastapi import HTTPException
from typing import Optional

async def verify_api_key(authorization: Optional[str] = None) -> None:
    """Verify API key if authentication is enabled."""
    if not settings.enable_auth:
        return

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization")

    token = authorization.replace("Bearer ", "")
    if token != settings.api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")
```

**Usage in endpoints:**

```python
@app.post("/invoke")
async def invoke_agent(
    request: QueryRequest,
    authorization: Optional[str] = None
):
    await verify_api_key(authorization)
    # ... rest of logic
```

### 3. Health Checks with Status Tracking

Implement comprehensive health checks that track system state:

Health status logic based on error rates:

```
CALCULATE ERROR RATE
        |
        v
    error_rate = errors / total_requests
        |
        v
    IS ERROR RATE > 10%?
    |                 |
   YES                NO
    |                 |
    v                 v
UNHEALTHY         IS ERROR RATE > 5%?
(HTTP 503)        |                 |
                 YES                NO
                  |                 |
                  v                 v
              DEGRADED          HEALTHY
              (HTTP 200)        (HTTP 200)
                  |                 |
                  v                 v
            Return Status + Metrics
```

Implement comprehensive health checks that track system state:

```python
from enum import Enum
from datetime import datetime

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

service_start_time = datetime.now()
request_count = 0
error_count = 0

@app.get("/health")
async def health_check():
    """Health check with real status logic."""
    uptime = (datetime.now() - service_start_time).total_seconds()
    error_rate = error_count / max(request_count, 1)

    # Determine status based on error rate
    if error_rate > 0.1:
        status = HealthStatus.UNHEALTHY
        http_status = 503
    elif error_rate > 0.05:
        status = HealthStatus.DEGRADED
        http_status = 200
    else:
        status = HealthStatus.HEALTHY
        http_status = 200

    response = {
        "status": status.value,
        "uptime_seconds": uptime,
        "error_rate": error_rate,
        "request_count": request_count
    }

    return JSONResponse(response, status_code=http_status)
```

### 4. Request Lifecycle with Timeouts

Wrap agent invocations with timeouts to prevent hanging:

Request flow with timeout protection:

```
START REQUEST
     |
     v
ACQUIRE SESSION
     |
     v
START TIMEOUT <------- timeout = 30 seconds
     |
     v
INVOKE AGENT
     |
     +------> STREAMING EVENTS
     |             |
     |             v
     |        COLLECT TEXT
     |             |
     |             v
     |        ACCUMULATE
     |
     v
TIMEOUT REACHED?
     |
     +------ YES ---> ABORT + HTTP 504
     |
     +------ NO ----> CONTINUE
                      |
                      v
                  COMPLETE
                      |
                      v
                  RETURN RESPONSE
```

Wrap agent invocations with timeouts to prevent hanging:

```python
import asyncio
from google.adk.runners import Runner

@app.post("/invoke")
async def invoke_agent(request: QueryRequest):
    try:
        async with asyncio.timeout(settings.request_timeout):
            response_text = ""
            async for event in runner.run_async(
                user_id="api_user",
                session_id=session.id,
                new_message=new_message
            ):
                if event.content and event.content.parts:
                    text = event.content.parts[0].text
                    if text:
                        response_text += text
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail=f"Request exceeded {settings.request_timeout}s timeout"
        )
```

**Key Points:**

- `asyncio.timeout()` prevents requests from hanging forever
- Check if text is not None before concatenating
- Return proper HTTP 504 status for timeouts
- Track timeout_count metric

### 5. Error Handling & Validation

Use typed exceptions and Pydantic models for validation:

Error handling decision tree:

```
EXCEPTION CAUGHT
        |
        v
    IS HTTPException?
    |                |
   YES               NO
    |                |
    v                v
RE-RAISE         IS ValueError?
(Already          |                |
formatted)       YES               NO
    |                |               |
    |                v               v
    |            VALIDATION      UNEXPECTED
    |            ERROR 400      ERROR 500
    |              |               |
    v              v               v
CLIENT ---- Generic Message ---- No Details
RESPONSE          + Status Code      Logged Internally
```

Use typed exceptions and Pydantic models for validation:

```python
from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    """Request model with built-in validation."""
    query: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Query prompt"
    )
    temperature: float = Field(
        0.5,
        ge=0.0,
        le=2.0,
        description="Randomness: 0=deterministic, 2=creative"
    )

@app.post("/invoke", response_model=QueryResponse)
async def invoke_agent(request: QueryRequest):
    try:
        # Logic here
        pass
    except HTTPException as e:
        # Already formatted, re-raise
        raise
    except ValueError as e:
        # Validation errors
        raise HTTPException(status_code=400, detail="Invalid parameters")
    except Exception as e:
        # Unexpected errors - don't expose details
        logger.error(f"Unexpected error", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred")
```

### 6. Logging & Observability

Implement structured logging with request tracing:

Request flow with logging at each step:

```
REQUEST ARRIVES
        |
        v
request_id = uuid.uuid4()
        |
        v
log.info("invoke_agent.start")
        |
        v
INVOKE AGENT
        |
        +---> log.info("event.received")
        |     log.info("text.processed")
        |
        v
SUCCESS?
    |       |
   YES      NO
    |       |
    v       v
log.info  log.error(
  "success"  exc_info=True
  )         )
    |       |
    v       v
All logs contain request_id = uuid
Can trace single request through entire system
```

Implement structured logging with request tracing:

```python
import logging

def setup_logging() -> logging.Logger:
    """Configure structured logging."""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = setup_logging()

# In endpoints, use request IDs for tracing
request_id = str(uuid.uuid4())
logger.info(f"invoke_agent.start - request_id={request_id} query_len={len(request.query)}")

try:
    # ... agent invocation
    logger.info(f"invoke_agent.success - request_id={request_id} tokens={token_count}")
except Exception as e:
    logger.error(f"invoke_agent.error - request_id={request_id} error={str(e)}", exc_info=True)
```

### 7. Metrics & Monitoring

Track key metrics for observability:

Metrics collection and exposure flow:

```
EACH REQUEST        EACH REQUEST
  SUCCESS            WITH ERROR
      |                  |
      v                  v
successful_requests    error_count += 1
      += 1
      |                  |
      v                  v
    request_count += 1
           |
           v
    ALL REQUESTS
           |
           +----> GET /health
           |           |
           |           v
           |    Calculate error_rate
           |    = error_count / request_count
           |           |
           |           v
           |    Return JSON:
           |    {
           |      status: HEALTHY | DEGRADED | UNHEALTHY
           |      request_count: N
           |      error_count: N
           |      error_rate: 0.05
           |      metrics: {...}
           |    }
           |           |
           v           v
    MONITORING DASHBOARD
    (Cloud Logging, Prometheus, etc.)
```

Track key metrics for observability:

```python
# Global metrics
request_count = 0
successful_requests = 0
error_count = 0
timeout_count = 0

@app.post("/invoke")
async def invoke_agent(request: QueryRequest):
    global request_count, successful_requests, error_count, timeout_count

    request_count += 1

    try:
        # ... invoke agent
        successful_requests += 1
        return QueryResponse(...)
    except asyncio.TimeoutError:
        timeout_count += 1
        raise
    except Exception as e:
        error_count += 1
        raise
```

**Expose metrics in health check:**

```python
response = {
    "status": status.value,
    "metrics": {
        "request_count": request_count,
        "successful_requests": successful_requests,
        "error_count": error_count,
        "timeout_count": timeout_count,
        "error_rate": error_count / max(request_count, 1)
    }
}
```

## Pattern Reference Table

Request flow diagram through all patterns:

```
CLIENT REQUEST (HTTP POST /invoke)
        |
        v
+------------------+
|  CORS Middleware |  Pattern 1: Settings define allowed origins
+------------------+
        |
        v
+------------------+
| Extract Auth     |  Pattern 2: Authentication
| Header           |
+------------------+
        |
        v
+------------------+
| Validate Query   |  Pattern 5: Error Handling & Validation
| (Pydantic)       |
+------------------+
        |
        v
+------------------+
| Start Timeout    |  Pattern 4: Request Lifecycle with Timeouts
| (30 seconds)     |
+------------------+
        |
        v
+------------------+
| Invoke Agent     |  Configured via Pattern 1: Settings
| Via ADK Runner   |
+------------------+
        |
        v
+------------------+
| Log Events       |  Pattern 6: Logging with request_id
| (request_id)     |
+------------------+
        |
        v
+------------------+
| Track Metrics    |  Pattern 7: Metrics & Monitoring
| (counters)       |
+------------------+
        |
        v
RESPONSE (JSON + Metrics)
```

| Pattern        | Benefit                       | Example                           |
| -------------- | ----------------------------- | --------------------------------- |
| **Settings**   | Configuration externalization | `.env` files, no hardcoded values |
| **Auth**       | Production security           | Bearer token validation           |
| **Health**     | Monitoring ready              | Real status based on metrics      |
| **Timeouts**   | Reliability                   | Prevents hanging requests         |
| **Validation** | Data integrity                | Pydantic models with constraints  |
| **Logging**    | Debugging & tracing           | Request IDs, structured logs      |
| **Metrics**    | Observability                 | Track error rates, latency        |

## Production Checklist

Before deploying to Cloud Run or production:

- [ ] **Configuration**: All sensitive data in environment variables, not code
- [ ] **Authentication**: API key or OAuth2 enabled in production environment
- [ ] **Health Checks**: `/health` endpoint configured in orchestrator
- [ ] **Timeouts**: Request timeout set appropriately for your use case
- [ ] **Logging**: Logs captured by orchestrator (Cloud Logging, etc.)
- [ ] **Error Handling**: No stack traces exposed in error responses
- [ ] **CORS**: Configured for specific origins, not wildcard
- [ ] **Tests**: All tests passing with good coverage
- [ ] **Metrics**: Monitoring dashboard set up for key metrics
- [ ] **Graceful Shutdown**: Lifespan events handle cleanup

## Common Pitfalls

### ❌ Don't

```python
# Don't use synchronous client
response = runner.run(...)  # This blocks!

# Don't expose internal errors
raise HTTPException(status_code=500, detail=str(e))

# Don't hardcode API keys
API_KEY = "sk-1234567890"

# Don't skip timeout handling
async for event in runner.run_async(...):  # Could hang forever

# Don't ignore text extraction errors
text = event.content.parts[0].text  # Could be None!
```

### ✅ Do

```python
# Do use async client
async for event in runner.run_async(...):

# Do use generic error messages
raise HTTPException(status_code=500, detail="An error occurred")

# Do use environment variables
api_key = os.getenv("API_KEY")

# Do wrap with timeout
async with asyncio.timeout(30):
    async for event in runner.run_async(...):

# Do check for None
if text and text is not None:
    response_text += text
```

## Performance Tips

1. **Connection Pooling**: Reuse Runner instance across requests
2. **Streaming**: Use `async for event in runner.run_async()` for streaming responses
3. **Caching**: Cache agent configuration between requests
4. **Workers**: Use multiple uvicorn workers: `uvicorn app:app --workers 4`
5. **Async All The Way**: Make every I/O operation async

## Deployment Examples

### Local Development

```bash
uvicorn production_agent.server:app --reload
```

### Production (Cloud Run)

```bash
# Create .env with production values
export PORT=8080
uvicorn production_agent.server:app --host 0.0.0.0 --port 8080
```

### With Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY production_agent/ production_agent/
CMD ["uvicorn", "production_agent.server:app", "--host", "0.0.0.0", "--port", "8080"]
```

## Links & Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Google ADK](https://github.com/google/adk-python)
- [Pydantic Validation](https://docs.pydantic.dev/latest/)
- [Cloud Run Best Practices](https://cloud.google.com/run/docs/quickstarts/build-and-deploy)
- [Python asyncio](https://docs.python.org/3/library/asyncio.html)

## Full Example

See `production_agent/server.py` in this repository for a complete implementation of all these patterns working together.
