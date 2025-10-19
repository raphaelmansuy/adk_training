---
id: adk-cheat-sheet
title: ADK Cheat Sheet - Quick Reference Guide
description: Comprehensive cheat sheet for Google Agent Development Kit - commands, patterns, configurations, and best practices at your fingertips.
sidebar_label: ADK Cheat Sheet
keywords:
  [
    "ADK cheat sheet",
    "quick reference",
    "commands",
    "patterns",
    "best practices",
    "troubleshooting",
  ]
---

**🎯 Purpose**: Everything you need to know about Google ADK in one comprehensive reference.

**📚 Source of Truth**: [google/adk-python](https://github.com/google/adk-python) (ADK 1.15)

---

## 🚀 Quick Start

### Installation & Setup

```bash
# Install ADK
pip install google-adk

# Verify installation
adk --version

# Set up environment
export GOOGLE_API_KEY="your-key-here"
export GOOGLE_GENAI_USE_VERTEXAI=false  # or true for Vertex AI
```

### Basic Agent Creation

```python
from google.adk.agents import Agent

# Minimal agent
agent = Agent(
    name="my_agent",
    model="gemini-2.0-flash",
    instruction="You are a helpful assistant.",
)

# Run agent
from google.adk.runners import Runner
runner = Runner()
result = await runner.run_async("Hello!", agent=agent)
print(result.content.parts[0].text)
```

---

## 🛠️ Agent Patterns

### LLM Agent (Basic Conversational)

```python
agent = Agent(
    name="chatbot",
    model="gemini-2.0-flash",
    description="Conversational assistant",
    instruction="Be helpful and friendly.",
)
```

### Tool-Enabled Agent

```python
def calculate_sum(a: int, b: int) -> dict:
    """Add two numbers."""
    return {"status": "success", "result": a + b}

agent = Agent(
    name="calculator",
    model="gemini-2.0-flash",
    instruction="Use tools to help users.",
    tools=[calculate_sum],
)
```

### Sequential Workflow

```python
from google.adk.agents import SequentialAgent

workflow = SequentialAgent(
    name="content_pipeline",
    sub_agents=[researcher, writer, editor],
    description="Research → Write → Edit pipeline",
)
```

### Parallel Processing

```python
from google.adk.agents import ParallelAgent

parallel_agent = ParallelAgent(
    name="research_team",
    sub_agents=[web_searcher, data_analyzer, expert_consultant],
    description="Concurrent research tasks",
)
```

### Loop Agent (Iterative Refinement)

```python
from google.adk.agents import LoopAgent

refinement_agent = LoopAgent(
    sub_agents=[writer, critic],
    max_iterations=3,
    description="Iterative content improvement",
)
```

---

## 🔧 Tool Patterns

### Function Tool

```python
def my_tool(param: str, tool_context) -> dict:
    """
    Tool description for LLM.

    Args:
        param: Parameter description
    """
    try:
        # Your logic here
        result = process_data(param)
        return {
            "status": "success",
            "report": "Human-readable success message",
            "data": result
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "report": "Human-readable error message"
        }
```

### OpenAPI Tool

```python
from google.adk.tools.openapi_toolset import OpenAPIToolset

# From OpenAPI spec URL
toolset = OpenAPIToolset(spec="https://api.example.com/openapi.json")

# With authentication
toolset = OpenAPIToolset(
    spec="https://api.example.com/openapi.json",
    auth_config={"type": "bearer", "token": "your-token"}
)

agent = Agent(..., tools=[toolset])
```

### MCP Tool

```python
from google.adk.tools.mcp_toolset import MCPToolset

# Filesystem access
filesystem_tools = MCPToolset(
    server="filesystem",
    path="/allowed/path"
)

# Database access
db_tools = MCPToolset(
    server="postgresql",
    connection_string="postgresql://..."
)

agent = Agent(..., tools=[filesystem_tools, db_tools])
```

### Built-in Tools

```python
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools.google_maps_grounding_tool import GoogleMapsGroundingTool
from google.adk.tools.code_execution_tool import CodeExecutionTool

agent = Agent(
    ...,
    tools=[
        GoogleSearchTool(),
        GoogleMapsGroundingTool(),
        CodeExecutionTool(),
    ]
)
```

---

## 📊 State Management

### State Scopes

```python
# Session state (current conversation)
tool_context.state['current_topic'] = 'python'

# User state (persistent across sessions)
tool_context.state['user:language'] = 'en'
tool_context.state['user:difficulty'] = 'intermediate'

# App state (global across all users)
tool_context.state['app:version'] = '1.0'

# Temp state (discarded after invocation)
tool_context.state['temp:calculation'] = 42
```

### Output Key (Auto-save Response)

```python
agent = Agent(
    ...,
    output_key="last_response"  # Auto-saves to state
)

# Response available in state
response = tool_context.state['last_response']
```

### Memory Service

```python
from google.adk.memory import VertexAiMemoryBankService

memory_service = VertexAiMemoryBankService(
    project="your-project",
    location="us-central1",
    agent_engine_id="123456789"
)

runner = Runner(agent=agent, memory_service=memory_service)

# Memory automatically saved after interactions
```

---

## 🌐 Environment Variables

### Google Cloud (Vertex AI)

```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
export GOOGLE_GENAI_USE_VERTEXAI=true
```

### API Keys

```bash
export GOOGLE_API_KEY="your-gemini-api-key"
export ANTHROPIC_API_KEY="your-claude-key"  # For other LLMs
export OPENAI_API_KEY="your-gpt-key"       # For other LLMs
```

### Application Settings

```bash
export MODEL="gemini-2.0-flash"
export TEMPERATURE="0.7"
export MAX_TOKENS="2048"
export LOG_LEVEL="INFO"
```

---

## 🚀 CLI Commands

### Development

```bash
# Start web interface
adk web

# Start web interface with specific agent
adk web my_agent

# Run agent from CLI
adk run my_agent

# API server mode
adk api_server
adk api_server --port 8090
```

### Deployment

```bash
# Cloud Run deployment
adk deploy cloud_run \
  --project your-project \
  --region us-central1 \
  --service-name my-agent

# Agent Engine deployment
adk deploy agent_engine \
  --project your-project \
  --region us-central1 \
  --agent-name my-production-agent

# GKE deployment
adk deploy gke \
  --project your-project \
  --cluster my-cluster \
  --service-name my-agent
```

### Testing & Debugging

```bash
# Run tests
pytest tests/

# With coverage
pytest tests/ --cov=src --cov-report=html

# Specific test
pytest tests/test_agent.py::TestAgent::test_basic_functionality

# Debug mode
adk web --debug
```

---

## 🔍 Debugging & Monitoring

### Events Tab (Web UI)

- View agent execution flow
- Track state changes
- Monitor tool calls
- Debug errors

### Logging

```python
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# In agent code
logger = logging.getLogger(__name__)
logger.info("Agent started", extra={"user_id": "123"})
```

### Callbacks for Monitoring

```python
def logging_callback(callback_context):
    print(f"Agent: {callback_context.agent.name}")
    print(f"Event: {callback_context.event_type}")
    if callback_context.error:
        print(f"Error: {callback_context.error}")

agent = Agent(
    ...,
    before_agent_callback=logging_callback,
    after_agent_callback=logging_callback,
    before_tool_callback=logging_callback,
    after_tool_callback=logging_callback,
)
```

### Health Checks

```python
# Add to FastAPI server
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": "2025-01-01T00:00:00Z",
        "version": "1.0.0"
    }
```

---

## 🧪 Testing Patterns

### Unit Tests

```python
import pytest
from google.adk.agents import Agent
from google.adk.runners import Runner

class TestMyAgent:
    @pytest.fixture
    def agent(self):
        return Agent(name="test_agent", model="gemini-2.0-flash")

    @pytest.mark.asyncio
    async def test_basic_response(self, agent):
        runner = Runner()
        result = await runner.run_async("Hello", agent=agent)
        assert "hello" in result.content.parts[0].text.lower()
```

### Tool Testing

```python
def test_calculator_tool():
    # Mock tool context
    class MockContext:
        def __init__(self):
            self.state = {}

    context = MockContext()
    result = calculate_sum(2, 3, context)

    assert result["status"] == "success"
    assert result["result"] == 5
```

### Integration Tests

```python
@pytest.mark.asyncio
async def test_full_workflow():
    # Test complete agent workflows
    runner = Runner()
    result = await runner.run_async(
        "Calculate 2 + 3 and explain the result",
        agent=calculator_agent
    )
    # Assertions on final result
```

---

## 📈 Performance Optimization

### Model Selection

```python
# Fast responses
agent = Agent(model="gemini-2.0-flash")

# High quality
agent = Agent(model="gemini-2.0-flash-thinking")

# Cost effective
agent = Agent(model="gemini-1.5-flash")
```

### Parallel Execution

```python
# Use ParallelAgent for independent tasks
parallel_agent = ParallelAgent(
    sub_agents=[task1, task2, task3]  # Runs simultaneously
)
```

### Caching

```python
# Implement caching in tools
@cachetools.ttl_cache(maxsize=100, ttl=300)  # 5-minute cache
def expensive_api_call(param):
    # Expensive operation
    return result
```

### Rate Limiting

```python
from fastapi import Request, HTTPException
import time

# Simple rate limiter
request_counts = {}

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    client_ip = request.client.host
    current_time = time.time()

    # Reset every minute
    if client_ip not in request_counts:
        request_counts[client_ip] = (current_time, 0)

    last_time, count = request_counts[client_ip]
    if current_time - last_time > 60:
        request_counts[client_ip] = (current_time, 1)
    elif count >= 100:  # 100 requests per minute
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    else:
        request_counts[client_ip] = (last_time, count + 1)

    return await call_next(request)
```

---

## 🚨 Common Issues & Solutions

### Issue: "State not persisting"

**Solution**: Use persistent SessionService

```python
from google.adk.sessions import DatabaseSessionService
runner = Runner(session_service=DatabaseSessionService())
```

### Issue: "Tool not being called"

**Solution**: Check tool docstring and parameter names

```python
def my_tool(query: str) -> dict:  # Correct
    """Search for information."""  # Descriptive docstring
```

### Issue: "Agent gives wrong answers"

**Solution**: Improve instructions and add grounding

```python
agent = Agent(
    instruction="Use tools for factual information. Always verify claims.",
    tools=[GoogleSearchTool()]
)
```

### Issue: "Slow responses"

**Solution**: Use faster models and parallel processing

```python
agent = Agent(model="gemini-2.0-flash")  # Fast model
# Or use ParallelAgent for concurrent tasks
```

### Issue: "Memory errors"

**Solution**: Reduce context length and use streaming

```python
agent = Agent(
    model="gemini-2.0-flash",
    generate_content_config={"max_output_tokens": 1024}
)
```

### Issue: "Authentication failures"

**Solution**: Check environment variables and permissions

```bash
export GOOGLE_API_KEY="your-key"
export GOOGLE_CLOUD_PROJECT="your-project"
gcloud auth application-default login
```

---

## 🔒 Security Best Practices

### Input Validation

```python
def safe_tool(user_input: str, tool_context) -> dict:
    # Validate input
    if not user_input or len(user_input) > 1000:
        return {"status": "error", "report": "Invalid input"}

    # Sanitize input
    clean_input = sanitize(user_input)

    # Process safely
    return {"status": "success", "result": process(clean_input)}
```

### Guardrails

```python
def content_filter(context):
    """Block inappropriate content."""
    if contains_profanity(context.query):
        context.block("Inappropriate content detected")
    return context

agent = Agent(
    ...,
    before_agent_callback=content_filter,
)
```

### Secrets Management

```python
# Use Secret Manager for production
from google.cloud import secretmanager

def get_secret(secret_id: str) -> str:
    client = secretmanager.SecretManagerServiceClient()
    project = os.environ['GOOGLE_CLOUD_PROJECT']
    name = f"projects/{project}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode('UTF-8')

api_key = get_secret('api-key')
```

---

## 📋 Production Checklist

### Pre-Deployment

- [ ] All tests passing (unit, integration, evaluation)
- [ ] Security review completed
- [ ] Performance benchmarks meet SLAs
- [ ] Error handling tested
- [ ] Rate limiting configured
- [ ] Monitoring and alerting setup
- [ ] Secrets stored in Secret Manager
- [ ] Documentation updated

### Production Deployment

- [ ] Staged rollout (dev → staging → prod)
- [ ] Health checks configured
- [ ] Auto-scaling enabled
- [ ] Backup and recovery tested
- [ ] Rollback plan documented
- [ ] On-call rotation scheduled

### Post-Deployment

- [ ] Monitor metrics for anomalies
- [ ] Review error logs
- [ ] Collect user feedback
- [ ] Measure against SLIs/SLOs
- [ ] Document lessons learned
- [ ] Plan optimization iterations

---

## 🎯 Best Practices

### Agent Design

- **Single Responsibility**: One agent, one clear purpose
- **Descriptive Names**: `content_writer` not `agent1`
- **Clear Instructions**: Specific, actionable prompts
- **Error Handling**: Graceful failure with helpful messages

### Tool Development

- **Structured Returns**: Always return `{"status": "success/error", "report": "...", "data": ...}`
- **Docstrings**: Clear descriptions for LLM understanding
- **Validation**: Check inputs and handle edge cases
- **Idempotent**: Safe to call multiple times

### State Management

- **Appropriate Scopes**: `user:` for preferences, `temp:` for calculations
- **Descriptive Keys**: `user:preferred_language` not `lang`
- **Default Values**: `state.get('key', 'default')`
- **Clean Up**: Remove unnecessary state data

### Performance

- **Parallel When Possible**: Use ParallelAgent for independent tasks
- **Caching**: Cache expensive operations
- **Streaming**: Use for long responses
- **Model Selection**: Balance speed vs quality vs cost

### Security

- **Input Validation**: Sanitize all user inputs
- **Rate Limiting**: Prevent abuse
- **Secrets**: Never hardcode credentials
- **Monitoring**: Log suspicious activity

---

## 📚 Quick Links

- **Official Docs**: [google.github.io/adk-docs](https://google.github.io/adk-docs)
- **API Reference**: [google.github.io/adk-docs/api](https://google.github.io/adk-docs/api)
- **GitHub**: [github.com/google/adk-python](https://github.com/google/adk-python)
- **Tutorials**: [Tutorial Index]()
- **Glossary**: [ADK Glossary](glossary.md)

**Last Updated**: October 2025 | **ADK Version**: 1.15
