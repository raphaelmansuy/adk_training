# Tutorial 17: Agent-to-Agent Communication - Official ADK Implementation

This tutorial demonstrates **real Agent-to-Agent (A2A) communication** using Google ADK's official RemoteA2aAgent class. The orchestrator coordinates multiple remote specialized agents running as separate ADK A2A servers for distributed AI systems.

## Overview

**What you'll learn:**
- Setting up real A2A servers using official `to_a2a()` function
- Using `RemoteA2aAgent` to communicate with remote agents
- Auto-generated agent discovery via `.well-known/agent-card.json`
- Running multiple agents as independent uvicorn services
- Orchestrating distributed agent workflows with official ADK patterns

**Key Concepts:**
- **RemoteA2aAgent**: Official ADK class for consuming remote A2A agents
- **to_a2a() function**: Official ADK utility for exposing agents via A2A
- **Auto-generated Agent Cards**: JSON metadata automatically created by ADK
- **uvicorn A2A Servers**: Specialized agents deployed using uvicorn + to_a2a()
- **Sub-Agent Pattern**: Official ADK pattern for agent delegation

## Architecture

```
┌─────────────────┐  RemoteA2aAgent     ┌─────────────────┐
│  A2A            │◄───────────────────►│  Research Agent │
│  Orchestrator   │  (localhost:8001)   │  (ADK Server)   │
│  (ADK Agent)    │                     └─────────────────┘
│                 │
│ ┌─────────────┐ │  RemoteA2aAgent     ┌─────────────────┐
│ │RemoteA2a    │◄────────────────────►│  Analysis Agent │
│ │Agent Classes│ │  (localhost:8002)   │  (ADK Server)   │
│ └─────────────┘ │                     └─────────────────┘
└─────────────────┘
         │
         │  RemoteA2aAgent     ┌─────────────────┐
         └────────────────────►│  Content Agent  │
              (localhost:8003) │  (ADK Server)   │
                               └─────────────────┘
```

## Quick Start

### 1. Setup Environment

```bash
# Install all dependencies (orchestrator + remote agents)
make setup

# Copy environment template
cp a2a_orchestrator/.env.example a2a_orchestrator/.env

# Edit .env and add your Google API key
# GOOGLE_API_KEY=your_actual_api_key_here
```

### 2. Start Remote A2A Agents

In one terminal, start all remote A2A agents using the official ADK command:

```bash
./start_a2a_servers.sh
```

This will start:

- Research Agent on <http://localhost:8001>
- Analysis Agent on <http://localhost:8002>
- Content Agent on <http://localhost:8003>

### 3. Start Orchestrator

In another terminal, start the ADK development server:

```bash
make dev
```

Open <http://localhost:8000> in your browser and select `a2a_orchestrator` 
from the agent dropdown.

### 4. Try Example Queries

```text
Research latest quantum computing developments and create a technical summary
```

```text
Analyze market trends for electric vehicles and generate an executive report
```

## Project Structure

```text
tutorial17/
├── a2a_orchestrator/          # Main ADK agent package
│   ├── __init__.py           # Package initialization
│   ├── agent.py              # Official ADK RemoteA2aAgent implementation
│   └── .env.example          # Environment template
├── research_agent/           # Remote Research Agent (ADK A2A Server)
│   ├── __init__.py
│   ├── agent.py              # Research agent using ADK patterns
│   └── agent-card.json       # Agent discovery card
├── analysis_agent/           # Remote Analysis Agent (ADK A2A Server)
│   ├── __init__.py
│   ├── agent.py              # Analysis agent using ADK patterns
│   └── agent-card.json       # Agent discovery card
├── content_agent/            # Remote Content Agent (ADK A2A Server)
│   ├── __init__.py
│   ├── agent.py              # Content agent using ADK patterns
│   └── agent-card.json       # Agent discovery card
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_agent.py         # Agent configuration tests
│   ├── test_imports.py       # Import validation tests
│   └── test_structure.py     # Project structure tests
├── start_a2a_servers.sh      # Start all A2A servers script
├── stop_a2a_servers.sh       # Stop all A2A servers script
├── pyproject.toml            # Main package configuration
├── requirements.txt          # Dependencies
├── Makefile                 # Development commands
└── README.md                # This file
```

## Agent Implementation

### Official ADK RemoteA2aAgent Setup

The orchestrator uses Google ADK's official `RemoteA2aAgent` class to connect to 
remote specialized agents:

```python
from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent

# Official ADK sub-agent pattern
root_agent = Agent(
    name="a2a_orchestrator",
    model="gemini-2.0-flash-exp",
    description="Orchestrates A2A communication with remote agents",
    instruction="""You coordinate with specialized remote agents...""",
    sub_agents=[
        RemoteA2aAgent(
            name="research_agent",
            base_url="http://localhost:8001"
        ),
        RemoteA2aAgent(
            name="analysis_agent", 
            base_url="http://localhost:8002"
        ),
        RemoteA2aAgent(
            name="content_agent",
            base_url="http://localhost:8003"
        ),
    ]
)
```

### Official ADK A2A Communication Flow

1. **Agent Discovery**: Orchestrator uses RemoteA2aAgent with base URLs
2. **Sub-Agent Pattern**: RemoteA2aAgent automatically handles communication
3. **Message Delegation**: Orchestrator delegates tasks to appropriate sub-agents
4. **Response Processing**: ADK handles all protocol details automatically
5. **Connection Management**: ADK manages HTTP clients and connections

### Starting Remote A2A Servers

Each remote agent runs using the official ADK `to_a2a()` function with uvicorn:

```bash
# Start all servers
./start_a2a_servers.sh

# Individual server startup (what the script does):
uvicorn research_agent.agent:a2a_app --host localhost --port 8001
uvicorn analysis_agent.agent:a2a_app --host localhost --port 8002
uvicorn content_agent.agent:a2a_app --host localhost --port 8003
```

The remote agents automatically expose:

- Auto-generated agent cards at `http://localhost:{port}/.well-known/agent-card.json`
- A2A endpoints for task execution
- Health checks and service discovery

## Official ADK A2A Protocol Details

### Agent Discovery

Remote agents expose **auto-generated agent cards** at
`/.well-known/agent-card.json` using the official `to_a2a()` function:

```json
{
  "name": "research_specialist",
  "description": "Conducts web research and fact-checking",
  "capabilities": {},
  "skills": [
    {
      "name": "research_topic",
      "description": "Research a specific topic and provide detailed findings"
    }
  ],
  "url": "http://localhost:8001"
}
```

### to_a2a() Function Benefits

- **Auto-Generated Cards**: Agent cards created automatically from agent code
- **Protocol Handling**: All A2A protocol details handled by ADK
- **Easy Deployment**: Simple uvicorn + to_a2a() pattern
- **Type Safety**: Full TypeScript/Python type definitions

## Testing

Run the comprehensive test suite:

```bash
make test
```

Tests cover:

- Agent configuration and initialization
- Tool functionality
- Import validation
- Project structure compliance

## Demo Mode

See example usage and capabilities:

```bash
make demo
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google AI Studio API key | Yes |

## Troubleshooting

### Common Issues

#### Agent card not found

- Remote agent not deployed or not exposing
  `/.well-known/agent-card.json`
- Check network connectivity and agent URL

#### Authentication failed

- Missing or invalid authentication tokens
- Verify token format and permissions

#### Connection timeout

- Network issues or remote agent unavailable
- Check agent status and retry logic

### Development Tips

- Use `./start_a2a_servers.sh` to start all agents with proper health checks
- Check agent cards at `http://localhost:800x/.well-known/agent-card.json`
- Monitor logs for coordination debugging

## Production Deployment

Use the official ADK deployment commands with the to_a2a() pattern:

```bash
# Deploy orchestrator
adk deploy cloud_run a2a_orchestrator/

# Deploy remote agents using uvicorn + to_a2a()
# (Custom deployment for production A2A servers)
```

## Next Steps

- **Tutorial 18**: Events & Observability
- **Tutorial 19**: Artifacts & File Management
- **Tutorial 20**: YAML Configuration

## Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [RemoteA2aAgent API](https://google.github.io/adk-docs/api/remote-a2a-agent/)
- [A2A Protocol Guide](https://google.github.io/adk-docs/a2a/)

---

**🎉 Tutorial 17 Complete!** You now understand how to build distributed
multi-agent systems with official ADK A2A communication.
