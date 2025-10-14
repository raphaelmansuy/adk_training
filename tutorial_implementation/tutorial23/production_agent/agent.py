"""
Production deployment agent demonstrating deployment strategies.

This agent showcases best practices for production deployment including:
- FastAPI server integration
- Environment configuration
- Health checks
- Monitoring patterns
"""

from google.adk.agents import Agent
from google.genai import types


def check_deployment_status() -> dict:
    """
    Check deployment status and health.
    
    Returns:
        Dict with deployment status information
    """
    return {
        "status": "success",
        "report": "Deployment health check successful",
        "deployment_type": "production",
        "features": [
            "FastAPI server",
            "Cloud Run deployment",
            "Agent Engine deployment",
            "GKE deployment",
            "Health checks",
            "Monitoring"
        ]
    }


def get_deployment_options() -> dict:
    """
    Get available deployment options.
    
    Returns:
        Dict with deployment options and descriptions
    """
    return {
        "status": "success",
        "report": "Available deployment options retrieved",
        "options": {
            "local_api_server": {
                "command": "adk api_server",
                "description": "Start local FastAPI server for development",
                "features": ["Hot reload", "API docs", "CORS enabled"]
            },
            "cloud_run": {
                "command": "adk deploy cloud_run",
                "description": "Deploy to serverless Cloud Run",
                "features": ["Auto-scaling", "Managed infrastructure", "Pay per use"]
            },
            "agent_engine": {
                "command": "adk deploy agent_engine",
                "description": "Deploy to Vertex AI Agent Engine",
                "features": ["Managed agents", "Built-in monitoring", "Version control"]
            },
            "gke": {
                "command": "adk deploy gke",
                "description": "Deploy to Google Kubernetes Engine",
                "features": ["Full control", "Custom scaling", "Advanced networking"]
            }
        }
    }


def get_best_practices() -> dict:
    """
    Get production deployment best practices.
    
    Returns:
        Dict with best practices for production deployment
    """
    return {
        "status": "success",
        "report": "Production best practices retrieved",
        "best_practices": {
            "security": [
                "Use Google Secret Manager for secrets",
                "Never commit API keys or credentials",
                "Enable CORS with specific origins only",
                "Implement rate limiting"
            ],
            "monitoring": [
                "Implement health check endpoints",
                "Use structured logging (JSON format)",
                "Enable Cloud Trace for observability",
                "Track error rates and response times"
            ],
            "scalability": [
                "Configure auto-scaling appropriately",
                "Set min and max instance counts",
                "Optimize memory and CPU limits",
                "Use connection pooling"
            ],
            "reliability": [
                "Implement graceful shutdown",
                "Add readiness and liveness probes",
                "Use circuit breakers for external calls",
                "Configure retries with exponential backoff"
            ]
        }
    }


# Create the production deployment agent
root_agent = Agent(
    name="production_deployment_agent",
    model="gemini-2.0-flash",
    description="Production deployment expert providing guidance on deployment strategies, best practices, and infrastructure patterns for ADK agents.",
    instruction="""
You are an expert in production deployment of ADK agents. You help users understand:

1. **Deployment Options**:
   - Local API server with FastAPI
   - Serverless deployment with Cloud Run
   - Managed deployment with Agent Engine
   - Custom Kubernetes deployment with GKE

2. **Best Practices**:
   - Security: secrets management, authentication, CORS
   - Monitoring: health checks, logging, tracing
   - Scalability: auto-scaling, resource limits
   - Reliability: error handling, retries, failover

3. **Commands**:
   - `adk api_server`: Start local FastAPI server
   - `adk deploy cloud_run`: Deploy to Cloud Run
   - `adk deploy agent_engine`: Deploy to Agent Engine
   - `adk deploy gke`: Deploy to GKE

When users ask about deployment:
- Recommend the most appropriate deployment option based on their needs
- Provide specific commands and configuration examples
- Highlight important considerations (cost, complexity, scalability)
- Share relevant best practices

Be practical, provide working examples, and focus on production-ready patterns.
    """.strip(),
    tools=[
        check_deployment_status,
        get_deployment_options,
        get_best_practices
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.5,
        max_output_tokens=2048
    )
)
