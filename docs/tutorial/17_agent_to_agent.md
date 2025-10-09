---
id: agent_to_agent
---

# Tutorial 17: Agent-to-Agent (A2A) Communication

**Goal**: Enable agents to communicate and collaborate with other remote agents using the Agent-to-Agent (A2A) protocol, creating distributed multi-agent systems.

**Prerequisites**:
- Tutorial 01 (Hello World Agent)
- Tutorial 06 (Multi-Agent Systems)
- Understanding of HTTP APIs and authentication
- Basic knowledge of REST principles

**What You'll Learn**:
- Understanding Agent-to-Agent (A2A) protocol
- Using `RemoteA2aAgent` to call remote agents
- Agent discovery with agent cards (`.well-known/agent.json`)
- Authentication between agents
- Building distributed agent orchestration
- Error handling in A2A communication
- Best practices for production A2A systems

**Time to Complete**: 50-65 minutes

---

## Why A2A Matters

**Problem**: Agents are often isolated - they can't leverage capabilities of other specialized agents deployed elsewhere.

**Solution**: **Agent-to-Agent (A2A)** protocol enables agents to discover and communicate with remote agents over HTTP, creating distributed AI systems.

**Benefits**:
- 🌐 **Distributed Intelligence**: Leverage agents across organizations
- 🔍 **Discovery**: Find agents by capability via agent cards
- 🔐 **Secure**: Built-in authentication and authorization
- 🎯 **Specialization**: Each agent focuses on its expertise
- 🔄 **Reusability**: Use same agent from multiple orchestrators
- ⚡ **Scalability**: Scale agents independently

**Use Cases**:
- Enterprise: Customer service agent calls internal knowledge agent
- Multi-org: Legal agent consults external compliance agent
- Microservices: Specialized agents as independent services
- Multi-cloud: Agents distributed across cloud providers

---

## 1. A2A Protocol Basics

### What is Agent-to-Agent Protocol?

**A2A** defines a standard way for agents to:

1. **Discover** other agents via agent cards
2. **Authenticate** with other agents
3. **Invoke** remote agent capabilities
4. **Receive** responses from remote agents

**Architecture**:
```
Local Agent (Orchestrator)
    ↓
RemoteA2aAgent (ADK Wrapper)
    ↓
HTTP Request with Auth
    ↓
Remote Agent Endpoint
    ↓
Remote Agent Execution
    ↓
Response back to Local Agent
```

**Source**: `google/adk/agents/remote_a2a_agent.py`

### Agent Card (Discovery)

Remote agents expose an **agent card** at `.well-known/agent.json`:

```json
{
  "name": "youtube_helper",
  "description": "YouTube video search and information retrieval",
  "url": "https://youtube-agent.example.com",
  "version": "1.0.0",
  "capabilities": ["search", "get_video_info", "get_comments"],
  "authentication": {
    "type": "bearer",
    "required": true
  }
}
```

**Well-Known Path**:
```python
from google.adk.agents import AGENT_CARD_WELL_KNOWN_PATH

# Standard location for agent cards
print(AGENT_CARD_WELL_KNOWN_PATH)
# Output: .well-known/agent.json

# Full URL example:
# https://youtube-agent.example.com/.well-known/agent.json
```

---

## 2. Using RemoteA2aAgent

### Basic Setup

```python
from google.adk.agents import Agent, RemoteA2aAgent, Runner
from google.adk.tools import AgentTool

# Connect to remote agent
remote_youtube_agent = RemoteA2aAgent(
    name='youtube_helper',
    base_url='https://youtube-agent.example.com',
    # Authentication handled automatically via agent card
)

# Create local orchestrator agent
orchestrator = Agent(
    model='gemini-2.0-flash',
    name='content_researcher',
    instruction="""
You coordinate research tasks. You have access to:
- youtube_helper: Search YouTube and get video information

Use youtube_helper when users ask about videos or YouTube content.
    """,
    tools=[AgentTool(remote_youtube_agent)]
)

runner = Runner()
result = runner.run(
    "Find the most popular videos about quantum computing",
    agent=orchestrator
)

print(result.content.parts[0].text)
```

### How It Works

**Step-by-Step Flow**:

1. **Discovery**: Orchestrator finds remote agent via agent card at `.well-known/agent.json`
2. **Authentication**: Orchestrator authenticates with remote agent
3. **Invocation**: Orchestrator sends request to remote agent
4. **Execution**: Remote agent processes request
5. **Response**: Remote agent returns results
6. **Integration**: Orchestrator incorporates results into response

**Internal Implementation** (simplified from `remote_a2a_agent.py`):

```python
class RemoteA2aAgent:
    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url
        
        # Fetch agent card for discovery
        self.agent_card = self._fetch_agent_card()
    
    def _fetch_agent_card(self):
        """Fetch agent card from .well-known path."""
        url = f"{self.base_url}/.well-known/agent.json"
        response = requests.get(url)
        return response.json()
    
    async def _run_async_impl(self, query: str, tool_context):
        """Invoke remote agent."""
        
        # Authenticate
        auth_token = await self._authenticate()
        
        # Call remote agent
        response = requests.post(
            f"{self.base_url}/execute",
            json={'query': query},
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        return response.json()['result']
```

---

## 3. Real-World Example: Multi-Service Agent Orchestration

Let's build a system where a main agent orchestrates multiple specialized remote agents.

### Complete Implementation

```python
"""
Multi-Service Agent Orchestration with A2A
Main agent coordinates research, analysis, and content creation agents.
"""

import asyncio
import os
from google.adk.agents import Agent, RemoteA2aAgent, Runner, Session
from google.adk.tools import AgentTool, FunctionTool
from google.genai import types

# Environment setup
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = '1'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'your-project-id'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'


class MultiServiceOrchestrator:
    """Orchestrates multiple remote specialized agents."""
    
    def __init__(self):
        """Initialize orchestrator with remote agents."""
        
        # Remote research agent (hypothetical external service)
        self.research_agent = RemoteA2aAgent(
            name='research_specialist',
            base_url='https://research-agent.example.com',
            description='Conducts web research and fact-checking'
        )
        
        # Remote analysis agent (hypothetical external service)
        self.analysis_agent = RemoteA2aAgent(
            name='data_analyst',
            base_url='https://analysis-agent.example.com',
            description='Analyzes data and generates insights'
        )
        
        # Remote content agent (hypothetical external service)
        self.content_agent = RemoteA2aAgent(
            name='content_writer',
            base_url='https://content-agent.example.com',
            description='Creates written content and summaries'
        )
        
        # Local coordination tool
        def log_action(action: str, agent_name: str) -> str:
            """Log coordination actions."""
            print(f"📝 [{agent_name}] {action}")
            return f"Logged: {action}"
        
        # Main orchestrator agent
        self.orchestrator = Agent(
            model='gemini-2.0-flash',
            name='orchestrator',
            description='Coordinates multiple specialized agents',
            instruction="""
You are an orchestration agent that coordinates specialized agents:

1. **research_specialist**: Use for web research, fact-checking, current events
   - Accesses web data
   - Verifies facts
   - Finds sources

2. **data_analyst**: Use for data analysis, statistics, insights
   - Analyzes numerical data
   - Generates reports
   - Identifies patterns

3. **content_writer**: Use for content creation, summaries, writing
   - Creates articles
   - Writes summaries
   - Formats content

**Workflow for complex tasks:**
1. Use research_specialist to gather information
2. Use data_analyst to analyze findings
3. Use content_writer to create final output
4. Log each step with log_action

Always explain which agent you're using and why.
            """.strip(),
            tools=[
                AgentTool(self.research_agent),
                AgentTool(self.analysis_agent),
                AgentTool(self.content_agent),
                FunctionTool(log_action)
            ],
            generate_content_config=types.GenerateContentConfig(
                temperature=0.5,
                max_output_tokens=2048
            )
        )
        
        self.runner = Runner()
        self.session = Session()
    
    async def execute_task(self, task: str):
        """
        Execute complex task with agent orchestration.
        
        Args:
            task: Task description
        """
        
        print(f"\n{'='*70}")
        print(f"TASK: {task}")
        print(f"{'='*70}\n")
        
        result = await self.runner.run_async(
            task,
            agent=self.orchestrator,
            session=self.session
        )
        
        print(f"\n📊 FINAL RESULT:\n")
        print(result.content.parts[0].text)
        print(f"\n{'='*70}\n")
        
        return result


async def main():
    """Main entry point."""
    
    orchestrator = MultiServiceOrchestrator()
    
    # Example 1: Market research
    await orchestrator.execute_task("""
Create a comprehensive market analysis report on electric vehicles:
1. Research current market trends
2. Analyze sales data by region
3. Write executive summary with key insights
    """)
    
    await asyncio.sleep(2)
    
    # Example 2: Competitive analysis
    await orchestrator.execute_task("""
Compare top 3 AI companies (OpenAI, Anthropic, Google DeepMind):
1. Research each company's recent developments
2. Analyze their product offerings and market position
3. Create comparison summary
    """)
    
    await asyncio.sleep(2)
    
    # Example 3: Technical deep-dive
    await orchestrator.execute_task("""
Produce technical analysis of quantum computing progress in 2025:
1. Research latest breakthroughs
2. Analyze research paper metrics and citations
3. Write technical summary for engineers
    """)


if __name__ == '__main__':
    asyncio.run(main())
```

### Expected Output

```
======================================================================
TASK: Create a comprehensive market analysis report on electric vehicles:
1. Research current market trends
2. Analyze sales data by region
3. Write executive summary with key insights
======================================================================

📝 [orchestrator] Starting multi-agent workflow for EV market analysis

🤖 Using research_specialist to gather market data...

📝 [research_specialist] Gathering current EV market trends
📝 [research_specialist] Found data: Global EV sales up 35% YoY
📝 [research_specialist] Key players: Tesla, BYD, Volkswagen
📝 [research_specialist] Regional breakdown collected

🤖 Using data_analyst to analyze sales data...

📝 [data_analyst] Analyzing regional sales data
📝 [data_analyst] Processing: North America, Europe, Asia-Pacific
📝 [data_analyst] Insights: Asia-Pacific dominates with 60% market share

🤖 Using content_writer to create executive summary...

📝 [content_writer] Generating executive summary
📝 [content_writer] Incorporating research findings and analysis
📝 [content_writer] Formatting for C-level audience

📊 FINAL RESULT:

# Electric Vehicle Market Analysis - Executive Summary

## Key Findings

The global electric vehicle market experienced remarkable growth in 2025, with 
sales increasing 35% year-over-year. This analysis examines current trends, 
regional performance, and strategic implications.

## Market Overview

**Global Sales:** 12.5 million units (up from 9.3 million in 2024)
**Market Leaders:** Tesla (18%), BYD (15%), Volkswagen (9%)
**Growth Rate:** 35% YoY

## Regional Analysis

### Asia-Pacific (60% market share)
- China leads with 7.5M units
- Strong government incentives
- Domestic manufacturers dominating

### Europe (25% market share)
- 3.1M units sold
- EU emissions regulations driving adoption
- Premium segment growing fastest

### North America (15% market share)
- 1.9M units sold
- Infrastructure expansion accelerating
- Pickup truck segment emerging

## Strategic Implications

1. **Supply Chain:** Battery production capacity critical
2. **Infrastructure:** Charging network expansion essential
3. **Competition:** Chinese manufacturers expanding globally
4. **Technology:** Solid-state batteries next frontier

## Recommendations

- Invest in battery production capabilities
- Accelerate charging infrastructure deployment
- Focus on mid-range price segments
- Develop partnerships with Chinese suppliers

**Prepared by:** Multi-Agent Research System
**Date:** October 2025

======================================================================
```

---

## 4. Authentication in A2A

### Authentication Configuration

A2A supports multiple authentication methods:

```python
from google.adk.agents import RemoteA2aAgent

# Bearer token authentication
remote_agent = RemoteA2aAgent(
    name='secure_agent',
    base_url='https://secure-agent.example.com',
    
    # Authentication configured via agent card
    # Card specifies: {"authentication": {"type": "bearer", "required": true}}
    
    # Token can be provided via:
    # 1. Environment variable: REMOTE_AGENT_TOKEN
    # 2. Credential storage
    # 3. OAuth flow
)
```

### Agent Card Authentication

Remote agent's `.well-known/agent.json`:

```json
{
  "name": "secure_research_agent",
  "description": "Secure research agent with authentication",
  "url": "https://research.example.com",
  "authentication": {
    "type": "bearer",
    "required": true,
    "token_url": "https://research.example.com/auth/token",
    "scopes": ["read", "search"]
  },
  "capabilities": ["search", "fact_check", "cite_sources"]
}
```

### Providing Credentials

```python
import os

# Option 1: Environment variable
os.environ['RESEARCH_AGENT_TOKEN'] = 'your-secret-token'

remote = RemoteA2aAgent(
    name='research_agent',
    base_url='https://research.example.com'
)

# Option 2: Via credential storage (in tools)
from google.adk.tools.tool_context import ToolContext

async def setup_auth(tool_context: ToolContext):
    """Store credentials for remote agent."""
    await tool_context.save_credential(
        'research_agent_token',
        'your-secret-token'
    )
```

---

## 5. Advanced A2A Patterns

### Pattern 1: Fallback Chain

Try multiple remote agents in sequence:

```python
from google.adk.agents import Agent, RemoteA2aAgent, Runner
from google.adk.tools import AgentTool

# Primary research agent
primary_research = RemoteA2aAgent(
    name='primary_research',
    base_url='https://primary-research.example.com'
)

# Backup research agent
backup_research = RemoteA2aAgent(
    name='backup_research',
    base_url='https://backup-research.example.com'
)

# Orchestrator with fallback logic
orchestrator = Agent(
    model='gemini-2.0-flash',
    name='resilient_orchestrator',
    instruction="""
When researching:
1. Try primary_research first
2. If it fails, use backup_research
3. Report which agent was used
    """,
    tools=[
        AgentTool(primary_research),
        AgentTool(backup_research)
    ]
)
```

### Pattern 2: Parallel Remote Execution

Call multiple remote agents concurrently:

```python
# Create multiple remote agents
agent_a = RemoteA2aAgent(name='agent_a', base_url='...')
agent_b = RemoteA2aAgent(name='agent_b', base_url='...')
agent_c = RemoteA2aAgent(name='agent_c', base_url='...')

# Orchestrator with parallel execution
orchestrator = Agent(
    model='gemini-2.0-flash',
    name='parallel_orchestrator',
    instruction="""
For comprehensive analysis:
1. Call all agents simultaneously
2. Synthesize their responses
3. Create unified summary
    """,
    tools=[
        AgentTool(agent_a),
        AgentTool(agent_b),
        AgentTool(agent_c)
    ]
)

runner = Runner()

# Agent will call remotes in parallel
result = await runner.run_async(
    "Get analysis from all agents and compare",
    agent=orchestrator
)
```

### Pattern 3: Agent Registry

Dynamically discover and connect to agents:

```python
import requests
from typing import List, Dict

class AgentRegistry:
    """Discover and manage remote agents."""
    
    def __init__(self, registry_url: str):
        self.registry_url = registry_url
    
    def discover_agents(self, capability: str) -> List[Dict]:
        """Find agents by capability."""
        response = requests.get(
            f"{self.registry_url}/agents",
            params={'capability': capability}
        )
        return response.json()['agents']
    
    def create_remote_agent(self, agent_info: Dict) -> RemoteA2aAgent:
        """Create RemoteA2aAgent from registry info."""
        return RemoteA2aAgent(
            name=agent_info['name'],
            base_url=agent_info['url'],
            description=agent_info['description']
        )


# Usage
registry = AgentRegistry('https://agent-registry.example.com')

# Find agents that can search
search_agents = registry.discover_agents('search')

# Create remote agents dynamically
remote_agents = [
    registry.create_remote_agent(agent_info)
    for agent_info in search_agents
]

# Use in orchestrator
orchestrator = Agent(
    model='gemini-2.0-flash',
    tools=[AgentTool(agent) for agent in remote_agents]
)
```

---

## 6. Deploying A2A-Compatible Agents

### Creating Agent Card Endpoint

```python
"""
FastAPI endpoint exposing agent card.
"""

from fastapi import FastAPI
from google.adk.agents import Agent, AGENT_CARD_WELL_KNOWN_PATH

app = FastAPI()

# Your agent
my_agent = Agent(
    model='gemini-2.0-flash',
    name='youtube_helper',
    description='YouTube video search and information'
)


@app.get(AGENT_CARD_WELL_KNOWN_PATH)
async def get_agent_card():
    """Expose agent card for discovery."""
    return {
        "name": "youtube_helper",
        "description": "YouTube video search and information retrieval",
        "url": "https://youtube-agent.example.com",
        "version": "1.0.0",
        "capabilities": ["search_videos", "get_video_info", "get_comments"],
        "authentication": {
            "type": "bearer",
            "required": True
        }
    }


@app.post("/execute")
async def execute_agent(request: dict, authorization: str = None):
    """Execute agent with A2A protocol."""
    
    # Validate authentication
    if not authorization or not authorization.startswith('Bearer '):
        return {"error": "Unauthorized"}, 401
    
    # Extract query
    query = request.get('query')
    
    # Execute agent
    from google.adk.agents import Runner
    runner = Runner()
    result = await runner.run_async(query, agent=my_agent)
    
    return {
        "result": result.content.parts[0].text,
        "agent": "youtube_helper"
    }
```

### Sample Agent Card

Save as `public/.well-known/agent.json`:

```json
{
  "name": "youtube_helper",
  "description": "YouTube video search and information retrieval",
  "url": "https://youtube-agent.example.com",
  "version": "1.0.0",
  "author": "Your Organization",
  "capabilities": [
    "search_videos",
    "get_video_info",
    "get_video_comments",
    "get_channel_info"
  ],
  "authentication": {
    "type": "bearer",
    "required": true,
    "token_url": "https://youtube-agent.example.com/auth/token"
  },
  "rate_limits": {
    "requests_per_minute": 60,
    "requests_per_hour": 1000
  },
  "terms_of_service": "https://youtube-agent.example.com/terms",
  "privacy_policy": "https://youtube-agent.example.com/privacy"
}
```

---

## 7. Best Practices

### ✅ DO: Validate Remote Agent Availability

```python
# ✅ Good - Test connectivity first
import requests

def check_agent_availability(base_url: str) -> bool:
    """Check if remote agent is available."""
    try:
        response = requests.get(
            f"{base_url}/.well-known/agent.json",
            timeout=5
        )
        return response.status_code == 200
    except:
        return False


if check_agent_availability('https://remote-agent.example.com'):
    remote = RemoteA2aAgent(
        name='remote_agent',
        base_url='https://remote-agent.example.com'
    )
else:
    print("Remote agent unavailable")
```

### ✅ DO: Handle Authentication Errors

```python
# ✅ Good - Authentication error handling
try:
    result = runner.run("Query remote agent", agent=orchestrator)
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    # Retry with token refresh
except Exception as e:
    print(f"A2A error: {e}")
```

### ✅ DO: Set Timeouts

```python
# ✅ Good - Timeout configuration
remote = RemoteA2aAgent(
    name='slow_agent',
    base_url='https://slow-agent.example.com',
    timeout=30.0  # 30 second timeout
)

# ❌ Bad - No timeout (may hang indefinitely)
remote = RemoteA2aAgent(
    name='agent',
    base_url='https://agent.example.com'
)
```

### ✅ DO: Implement Retry Logic

```python
# ✅ Good - Retry on failure
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def call_remote_agent(query: str):
    """Call remote agent with retry."""
    result = await runner.run_async(query, agent=orchestrator)
    return result
```

### ✅ DO: Monitor A2A Calls

```python
# ✅ Good - Log A2A interactions
import logging

logging.basicConfig(level=logging.INFO)

# ADK automatically logs A2A calls
remote = RemoteA2aAgent(
    name='monitored_agent',
    base_url='https://agent.example.com'
)

# Logs will show:
# - Agent discovery
# - Authentication attempts
# - Request/response details
# - Errors and retries
```

---

## 8. Troubleshooting

### Error: "Agent card not found"

**Problem**: Remote agent doesn't expose agent card

**Solution**:
```bash
# Test agent card manually
curl https://remote-agent.example.com/.well-known/agent.json

# Should return agent card JSON
# If 404, remote agent not configured correctly
```

### Error: "Authentication failed"

**Problem**: Missing or invalid credentials

**Solutions**:

1. **Check environment variable**:
```python
import os
print(os.environ.get('REMOTE_AGENT_TOKEN'))
```

2. **Verify token with agent**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://remote-agent.example.com/execute
```

3. **Check agent card auth requirements**:
```bash
curl https://remote-agent.example.com/.well-known/agent.json | \
     jq '.authentication'
```

### Issue: "Slow A2A responses"

**Problem**: Network latency or remote agent performance

**Solutions**:

1. **Set appropriate timeout**:
```python
remote = RemoteA2aAgent(
    name='agent',
    base_url='...',
    timeout=60.0  # Increase if needed
)
```

2. **Use caching**:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def call_remote_cached(query: str):
    """Cache remote agent responses."""
    return runner.run(query, agent=orchestrator)
```

---

## Summary

You've mastered Agent-to-Agent communication:

**Key Takeaways**:
- ✅ `RemoteA2aAgent` enables distributed agent systems
- ✅ Agent cards at `.well-known/agent.json` enable discovery
- ✅ Built-in authentication support (bearer tokens)
- ✅ Create distributed orchestration patterns
- ✅ Deploy A2A-compatible agents with agent cards
- ✅ Handle authentication, timeouts, and errors
- ✅ Monitor A2A interactions for reliability
- ✅ Use agent registries for dynamic discovery

**Production Checklist**:
- [ ] Agent cards properly configured
- [ ] Authentication implemented and tested
- [ ] Timeouts set for all remote calls
- [ ] Retry logic for network failures
- [ ] Error handling for auth/connectivity issues
- [ ] Monitoring/logging of A2A calls
- [ ] Rate limiting considered
- [ ] Security reviewed (TLS, auth, secrets)

**Next Steps**:
- **Tutorial 18**: Learn Events & Observability
- **Tutorial 19**: Implement Artifacts & File Management
- **Tutorial 20**: Master YAML Configuration

**Resources**:
- [A2A Protocol Specification](https://google.github.io/adk-docs/a2a/)
- [Sample: a2a_auth](research/adk-python/contributing/samples/a2a_auth/)
- [Agent Card Schema](https://google.github.io/adk-docs/a2a/agent-card/)

---

**🎉 Tutorial 17 Complete!** You now know how to build distributed multi-agent systems with A2A. Continue to Tutorial 18 to learn about events and observability.
