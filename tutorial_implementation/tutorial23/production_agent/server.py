"""
Custom FastAPI server implementation for production deployment.

This demonstrates how to create a production-ready API server with:
- Health check endpoints
- Agent invocation
- Request tracking
- Error handling
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.adk.agents import Runner
from google.genai import types
from datetime import datetime
import os

from .agent import root_agent

# Environment setup
os.environ.setdefault('GOOGLE_GENAI_USE_VERTEXAI', '0')

app = FastAPI(
    title="ADK Production Deployment API",
    version="1.0",
    description="Production-ready API server for ADK agents"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create runner
runner = Runner()

# Track service metrics
service_start_time = datetime.now()
request_count = 0
error_count = 0


class QueryRequest(BaseModel):
    """Request model for agent invocation."""
    query: str
    temperature: float = 0.5
    max_tokens: int = 2048


class QueryResponse(BaseModel):
    """Response model for agent invocation."""
    response: str
    model: str
    tokens: int


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "ADK Production Deployment API",
        "version": "1.0",
        "endpoints": {
            "health": "/health",
            "invoke": "/invoke (POST)",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health")
async def health_check():
    """
    Comprehensive health check endpoint.
    
    Returns service status, uptime, and metrics.
    """
    uptime = (datetime.now() - service_start_time).total_seconds()
    
    health_status = {
        "status": "healthy",
        "service": "adk-production-deployment-api",
        "uptime_seconds": uptime,
        "request_count": request_count,
        "error_count": error_count,
        "error_rate": error_count / request_count if request_count > 0 else 0,
        "agent": {
            "name": root_agent.name,
            "model": root_agent.model
        }
    }
    
    return health_status


@app.post("/invoke", response_model=QueryResponse)
async def invoke_agent(request: QueryRequest):
    """
    Invoke the production deployment agent.
    
    Args:
        request: Query and configuration parameters
        
    Returns:
        Agent response with metadata
    """
    global request_count, error_count
    
    request_count += 1
    
    try:
        # Update agent config if needed
        root_agent.generate_content_config = types.GenerateContentConfig(
            temperature=request.temperature,
            max_output_tokens=request.max_tokens
        )
        
        # Run agent
        result = await runner.run_async(request.query, agent=root_agent)
        
        # Extract response
        response_text = result.content.parts[0].text
        
        # Estimate tokens (simple word count)
        token_count = len(response_text.split())
        
        return QueryResponse(
            response=response_text,
            model=root_agent.model,
            tokens=token_count
        )
        
    except Exception as e:
        error_count += 1
        raise HTTPException(status_code=500, detail=str(e))


@app.middleware("http")
async def track_requests(request, call_next):
    """Middleware to track requests and errors."""
    global request_count, error_count
    
    response = await call_next(request)
    
    if response.status_code >= 400:
        error_count += 1
    
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "8080")),
        log_level="info"
    )
