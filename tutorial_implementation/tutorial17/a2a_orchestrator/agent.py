"""
Official ADK A2A Orchestrator Agent - Agent-to-Agent Communication

This demonstrates the official ADK approach to distributed agent orchestration
using RemoteA2aAgent for consuming remote agents exposed via 'adk api_server --a2a'.
"""

from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH
from google.adk.tools import FunctionTool
from google.genai import types


def check_agent_availability(agent_name: str, base_url: str) -> dict:
    """Check if a remote A2A agent is available."""
    try:
        import requests
        card_url = f"{base_url}{AGENT_CARD_WELL_KNOWN_PATH}"
        response = requests.get(card_url, timeout=5)
        
        if response.status_code == 200:
            return {
                "status": "success",
                "available": True,
                "report": f"Agent {agent_name} is available",
                "agent_card": response.json()
            }
        else:
            return {
                "status": "error", 
                "available": False,
                "report": f"Agent {agent_name} returned status {response.status_code}"
            }
    except Exception as e:
        return {
            "status": "error",
            "available": False, 
            "report": f"Failed to check {agent_name}: {str(e)}"
        }


def log_coordination_step(step: str, agent_name: str = "") -> dict:
    """Log orchestration steps for tracking."""
    message = f"🎯 {step}"
    if agent_name:
        message += f" with {agent_name}"
    print(message)
    
    return {
        "status": "success",
        "report": message,
        "step": step,
        "agent": agent_name
    }


# Remote agents using official ADK RemoteA2aAgent
research_agent = RemoteA2aAgent(
    name="research_specialist",
    description="Conducts web research and fact-checking",
    agent_card=f"http://localhost:8001{AGENT_CARD_WELL_KNOWN_PATH}"
)

analysis_agent = RemoteA2aAgent(
    name="data_analyst", 
    description="Analyzes data and generates insights",
    agent_card=f"http://localhost:8002{AGENT_CARD_WELL_KNOWN_PATH}"
)

content_agent = RemoteA2aAgent(
    name="content_writer",
    description="Creates written content and summaries", 
    agent_card=f"http://localhost:8003{AGENT_CARD_WELL_KNOWN_PATH}"
)

# Main orchestrator agent using official ADK patterns
root_agent = Agent(
    model="gemini-2.0-flash",
    name="a2a_orchestrator",
    description="Coordinates multiple remote specialized agents using official ADK A2A",
    instruction="""
You are an orchestration agent that coordinates specialized remote agents 
using the official ADK Agent-to-Agent (A2A) protocol.

**Available Remote Agents (Sub-Agents):**

1. **research_specialist**: Use for web research, fact-checking, current events
2. **data_analyst**: Use for data analysis, statistics, insights  
3. **content_writer**: Use for content creation, summaries, writing

**Official ADK A2A Workflow:**
1. Delegate research tasks to research_specialist sub-agent
2. Delegate analysis tasks to data_analyst sub-agent
3. Delegate content creation to content_writer sub-agent
4. Use log_coordination_step to track the orchestration process
5. Use check_agent_availability to verify agent status

The remote agents are exposed using uvicorn + to_a2a() and work
seamlessly as sub-agents in your orchestration workflow.

Always explain which remote agent you're delegating to and why.
    """,
    sub_agents=[research_agent, analysis_agent, content_agent],
    tools=[
        FunctionTool(check_agent_availability),
        FunctionTool(log_coordination_step)
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.5,
        max_output_tokens=2048
    )
)
