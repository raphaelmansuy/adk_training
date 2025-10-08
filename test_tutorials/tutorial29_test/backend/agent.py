"""Tutorial 29 - Quickstart Agent Test Implementation."""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from google.adk.agents import LlmAgent

# Initialize FastAPI
app = FastAPI(title="Tutorial 29 Quickstart Agent")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create ADK agent
adk_agent = LlmAgent(
    name="quickstart_agent",
    model="gemini-2.0-flash-exp",
    instruction="You are a helpful AI assistant. Answer questions clearly and concisely."
)

# Wrap with ADKAgent middleware
agent = ADKAgent(
    adk_agent=adk_agent,
    app_name="quickstart_demo",
    user_id="demo_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True
)

# Add ADK endpoint
add_adk_fastapi_endpoint(app, agent, path="/api/copilotkit")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agent": "quickstart_agent",
        "tutorial": "29"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
