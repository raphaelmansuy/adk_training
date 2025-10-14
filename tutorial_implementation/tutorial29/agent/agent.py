"""Tutorial 29: Introduction to UI Integration - Quick Start Example.

This is a minimal ADK agent demonstrating AG-UI Protocol integration.
Based on the Quick Start section from Tutorial 29.
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# AG-UI ADK integration imports
try:
    from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
except ImportError:
    raise ImportError(
        "ag_ui_adk not found. Install with: pip install ag-ui-adk"
    )

# Google ADK imports
from google.adk.agents import Agent

# Load environment variables
load_dotenv()


# ============================================================================
# Agent Configuration
# ============================================================================

# Create simple ADK agent
adk_agent = Agent(
    name="quickstart_agent",
    model="gemini-2.0-flash-exp",
    instruction="""You are a helpful AI assistant powered by Google ADK.

Your role:
- Answer questions clearly and concisely
- Be friendly and professional
- Provide accurate information
- If you don't know something, say so
- Help users understand ADK and AI concepts

Guidelines:
- Keep responses under 3 paragraphs unless more detail is requested
- Use markdown formatting for better readability
- Be conversational but professional
- Offer to help with follow-up questions"""
)

# Wrap ADK agent with AG-UI middleware
agent = ADKAgent(
    adk_agent=adk_agent,
    app_name="quickstart_demo",
    user_id="demo_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True,
)

# Export for testing
root_agent = adk_agent


# ============================================================================
# FastAPI Application
# ============================================================================

# Create FastAPI app
app = FastAPI(
    title="Tutorial 29 - UI Integration Quickstart",
    description="Minimal ADK agent demonstrating AG-UI Protocol",
    version="1.0.0",
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",  # Next.js default (alternative)
        "http://localhost:8000",  # Local testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add ADK endpoint for CopilotKit
add_adk_fastapi_endpoint(app, agent, path="/api/copilotkit")


# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agent": "quickstart_agent",
        "version": "1.0.0",
        "tutorial": "29"
    }


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "Tutorial 29 - UI Integration Quickstart API",
        "tutorial": "Introduction to UI Integration & AG-UI Protocol",
        "endpoints": {
            "health": "/health",
            "copilotkit": "/api/copilotkit",
            "docs": "/docs",
        },
    }


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    # Get configuration from environment
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")

    print("=" * 60)
    print("🚀 Tutorial 29 - UI Integration Quickstart")
    print("=" * 60)
    print(f"🌐 Server: http://{host}:{port}")
    print(f"📚 Docs: http://{host}:{port}/docs")
    print(f"💬 CopilotKit: http://{host}:{port}/api/copilotkit")
    print("=" * 60)
    print()
    print("This is a minimal example demonstrating:")
    print("  • ADK agent with AG-UI Protocol")
    print("  • FastAPI backend with CopilotKit endpoint")
    print("  • Ready for React/Vite frontend integration")
    print("=" * 60)

    # Run with uvicorn
    uvicorn.run(
        "agent:app",
        host=host,
        port=port,
        reload=True,
        log_level="info",
    )
