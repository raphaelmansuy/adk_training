# AG-UI Framework Research

**Research Date**: 2025-01-08  
**Source**: `research/ag-ui/` (AG-UI Protocol repository)  
**Purpose**: Document AG-UI protocol and ADK integration capabilities

---

## Overview

**AG-UI** (Agent-User Interaction Protocol) is an **open, lightweight, event-based protocol** that standardizes how AI agents connect to user-facing applications.

- **Project**: Official protocol by CopilotKit
- **Status**: ✅ PRODUCTION READY
- **ADK Support**: ✅ OFFICIALLY SUPPORTED (Partnership with Google)
- **Repository**: https://github.com/ag-ui-protocol/ag-ui
- **Documentation**: https://ag-ui.com/
- **Dojo (Examples)**: https://dojo.ag-ui.com/

---

## What is AG-UI?

AG-UI is **complementary to other agentic protocols**:
- **MCP (Model Context Protocol)**: Gives agents tools
- **A2A (Agent-to-Agent)**: Allows agents to communicate with other agents
- **AG-UI**: Brings agents into user-facing applications

### Key Features

1. **Event-Based Protocol**: ~16 standard event types
2. **Transport Agnostic**: Works with SSE, WebSockets, webhooks
3. **Loose Format Matching**: Broad agent/app interoperability
4. **Reference HTTP Implementation**: Default connector included
5. **Multiple Framework Support**: LangGraph, CrewAI, **Google ADK**, Mastra, etc.

---

## Google ADK Integration

### Official Support Status

| Framework | Status | Documentation | Demos |
|-----------|--------|---------------|-------|
| Google ADK | ✅ Supported | [Docs](https://docs.copilotkit.ai/adk) | [Dojo Demos](https://dojo.ag-ui.com/adk-middleware) |

**Partnership**: Google ADK has **official partnership** with AG-UI/CopilotKit

### ADK Middleware Architecture

The `adk-middleware` package bridges Google ADK agents to AG-UI Protocol:

```
Google ADK Agent → ADK Middleware → AG-UI Protocol → Frontend (React/Next.js)
```

**Location**: `research/ag-ui/typescript-sdk/integrations/adk-middleware/`

---

## Installation & Setup

### 1. Install ADK Middleware

```bash
# Clone AG-UI repository
git clone https://github.com/ag-ui-protocol/ag-ui.git

# Navigate to ADK middleware
cd typescript-sdk/integrations/adk-middleware

# Install middleware
pip install .
# or
uv pip install .

# Install example requirements
cd examples
uv pip install -r requirements.txt
```

### 2. Run ADK Backend Server

```bash
export GOOGLE_API_KEY='your-api-key-here'
cd examples
uv run dev
```

**Server starts on**: http://localhost:8000

**Available Endpoints**:
- `/chat` - Agentic Chat
- `/adk-tool-based-generative-ui` - Generative UI with tools
- `/adk-human-in-loop-agent` - Human-in-the-loop patterns
- `/adk-shared-state-agent` - Bidirectional state sync
- `/docs` - OpenAPI documentation

### 3. Run AG-UI Dojo (Frontend)

```bash
cd typescript-sdk
pnpm install && pnpm run dev
```

**Dojo starts on**: http://localhost:3000

**View ADK Examples**: http://localhost:3000/adk-middleware

---

## Integration Patterns

### Pattern 1: Direct Agent Usage

```python
from ag_ui_adk import ADKAgent
from google.adk.agents import Agent

# 1. Create ADK agent
my_agent = Agent(
    name="assistant",
    model="gemini-2.0-flash",
    instruction="You are a helpful assistant."
)

# 2. Wrap with AG-UI middleware
agent = ADKAgent(
    adk_agent=my_agent,
    app_name="my_app", 
    user_id="user123"
)

# 3. Use with AG-UI RunAgentInput
async for event in agent.run(input_data):
    print(f"Event: {event.type}")
```

### Pattern 2: FastAPI Server

```python
from fastapi import FastAPI
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from google.adk.agents import Agent

# 1. Create ADK agent
my_agent = Agent(
    name="assistant",
    model="gemini-2.0-flash",
    instruction="You are a helpful assistant."
)

# 2. Wrap with middleware
agent = ADKAgent(
    adk_agent=my_agent,
    app_name="my_app", 
    user_id="user123"
)

# 3. Create FastAPI app
app = FastAPI()
add_adk_fastapi_endpoint(app, agent, path="/chat")

# Run: uvicorn main:app --host 0.0.0.0 --port 8000
```

### Pattern 3: Multi-Agent Setup

```python
from fastapi import FastAPI
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint

app = FastAPI()

# Create multiple agents
general_agent_wrapper = ADKAgent(
    adk_agent=general_agent,
    app_name="demo_app",
    user_id="demo"
)

technical_agent_wrapper = ADKAgent(
    adk_agent=technical_agent,
    app_name="demo_app",
    user_id="demo"
)

# Different endpoints for each
add_adk_fastapi_endpoint(app, general_agent_wrapper, path="/agents/general")
add_adk_fastapi_endpoint(app, technical_agent_wrapper, path="/agents/technical")
```

---

## AG-UI Event Types (Core Features)

### 1. Agentic Chat
**Feature**: Real-time streaming chat with agents

**Events**:
- `RunStartedEvent` - Agent execution begins
- `TextMessageStartEvent` - Start of assistant message
- `TextMessageContentEvent` - Streaming text chunks
- `TextMessageEndEvent` - Message complete
- `RunFinishedEvent` - Agent execution complete

**Example**:
```json
{
  "type": "TEXT_MESSAGE_CONTENT",
  "message_id": "msg_123",
  "delta": "Hello, how can I help you today?"
}
```

### 2. Tool-Based Generative UI
**Feature**: Frontend tools integrated with agent backend

**Events**:
- `ToolCallStartEvent` - Tool execution begins
- `ToolCallArgsEvent` - Tool arguments streaming
- `ToolCallEndEvent` - Tool execution complete

**Use Case**: Agent calls frontend components (charts, forms, maps)

### 3. Human-in-the-Loop
**Feature**: Agent pauses for human approval/input

**Events**:
- `HumanInputRequestEvent` - Agent requests human input
- `HumanInputResponseEvent` - Human provides input

**Use Case**: Approval workflows, sensitive operations

### 4. Shared State
**Feature**: Bidirectional state synchronization between agent and UI

**Events**:
- `StateUpdateEvent` - State changes from agent
- `StateSnapshotEvent` - Full state sync

**Use Case**: Real-time dashboards, collaborative editing

### 5. Predictive State Updates
**Feature**: Agent predicts and pre-updates UI state

**Use Case**: Optimistic UI updates, faster perceived performance

---

## Frontend Integration (React/Next.js)

### React Example (AG-UI SDK)

```typescript
import { useCopilotChat } from "@copilotkit/react-core";

function ChatComponent() {
  const { messages, sendMessage, isLoading } = useCopilotChat({
    agentEndpoint: "http://localhost:8000/chat",
  });

  return (
    <div>
      {messages.map((msg) => (
        <div key={msg.id}>{msg.content}</div>
      ))}
      <input 
        onSubmit={(e) => sendMessage(e.target.value)} 
        disabled={isLoading}
      />
    </div>
  );
}
```

### Next.js 15 Example

```typescript
// app/api/chat/route.ts (Server Component)
import { NextRequest } from "next/server";
import { streamAGUIResponse } from "@ag-ui/next";

export async function POST(req: NextRequest) {
  const input = await req.json();
  
  return streamAGUIResponse({
    agentEndpoint: "http://localhost:8000/chat",
    input,
  });
}
```

```typescript
// app/chat/page.tsx (Client Component)
"use client";
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";

export default function ChatPage() {
  return (
    <CopilotKit runtimeUrl="/api/chat">
      <CopilotChat />
    </CopilotKit>
  );
}
```

---

## Key Capabilities for UI Integration

### ✅ **Supported Features**

| Feature | Support Level | Details |
|---------|--------------|---------|
| Real-time Streaming | ✅ Full | SSE/WebSocket via AG-UI protocol |
| Bidirectional State | ✅ Full | Shared state between agent and UI |
| Tool Integration | ✅ Full | Frontend tools callable by agent |
| Multi-Agent | ✅ Full | Multiple agents per application |
| Human-in-Loop | ✅ Full | Approval workflows, confirmations |
| Generative UI | ✅ Full | Agent-generated UI components |
| Voice/Audio | ✅ Full | Via WebSocket transport |
| File Uploads | ✅ Full | Via artifact system |
| Authentication | ✅ Full | OAuth2, API keys supported |
| Observability | ✅ Full | OpenTelemetry tracing |

### 📦 **Framework Support**

| Framework | SDK | Transport | Example |
|-----------|-----|-----------|---------|
| React | TypeScript | HTTP/SSE | `@copilotkit/react-core` |
| Next.js | TypeScript | HTTP/SSE | `@copilotkit/react-core` + Next.js |
| Vue.js | TypeScript | HTTP/SSE | Community integration |
| Svelte | TypeScript | HTTP/SSE | Community integration |
| Streamlit | Python | HTTP | Custom client needed |
| Slack | Python | Webhooks | Bolt SDK + middleware |

---

## Example Applications (from AG-UI Dojo)

### 1. Chat with Streaming

**Backend** (`examples/server/api/agentic_chat_app.py`):
```python
from google.adk.agents import Agent
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from fastapi import APIRouter

router = APIRouter()

agent = Agent(
    name="chat_assistant",
    model="gemini-2.0-flash",
    instruction="You are a helpful chat assistant."
)

adk_agent = ADKAgent(
    adk_agent=agent,
    app_name="chat_app",
    user_id="demo"
)

add_adk_fastapi_endpoint(router, adk_agent, path="/")
```

**Frontend** (React):
```typescript
import { useCopilotChat } from "@copilotkit/react-core";

export function ChatDemo() {
  const { messages, sendMessage } = useCopilotChat({
    agentEndpoint: "http://localhost:8000/chat",
  });
  
  return <CopilotChat />;
}
```

### 2. Tool-Based Generative UI

**Backend**:
```python
from google.adk.agents import Agent, tool

@tool
def create_chart(data: list[dict], chart_type: str) -> dict:
    """Generate a chart for the user."""
    return {
        "component": "Chart",
        "props": {"data": data, "type": chart_type}
    }

agent = Agent(
    name="data_viz",
    model="gemini-2.0-flash",
    tools=[create_chart]
)
```

**Frontend** (React renders returned component):
```typescript
<CopilotChat 
  onToolCall={(tool) => {
    if (tool.name === "create_chart") {
      return <ChartComponent {...tool.props} />;
    }
  }}
/>
```

### 3. Human-in-the-Loop

**Backend**:
```python
from google.adk.agents import Agent, long_running_tool

@long_running_tool
async def request_approval(action: str) -> bool:
    """Ask human for approval."""
    # Emits HumanInputRequestEvent
    # Agent pauses until response
    return True  # Human approved
```

---

## Deployment Considerations

### Development
- **Backend**: Run FastAPI with `uvicorn` on localhost:8000
- **Frontend**: Run Next.js dev server on localhost:3000
- **CORS**: Enable for local development

### Production
- **Backend Options**:
  - Google Cloud Run (recommended)
  - Vertex AI Agent Engine
  - GKE (Kubernetes)
  - AWS/Azure containers
- **Frontend Options**:
  - Vercel (Next.js)
  - Netlify (React)
  - Google Cloud Storage + CDN
- **Authentication**: OAuth2, Google IAM
- **Scaling**: Horizontal scaling with session state in Cloud SQL/Firestore

---

## Comparison: Native ADK API vs AG-UI

| Aspect | Native ADK API | AG-UI Protocol |
|--------|---------------|----------------|
| **Protocol** | Custom ADK events | Standardized AG-UI events |
| **Transport** | HTTP/SSE/WebSocket | Any (HTTP/SSE/WebSocket/webhooks) |
| **Frontend SDK** | None (custom client) | `@copilotkit/react-core` |
| **UI Components** | DIY | `<CopilotChat>`, `<CopilotKit>` |
| **Multi-Framework** | ADK-specific | 15+ frameworks supported |
| **Tool Ecosystem** | ADK tools only | ADK + MCP + AG-UI tools |
| **Learning Curve** | ADK-specific | Portable knowledge |
| **Production Examples** | Limited | Extensive (Dojo) |
| **Community** | Google ADK community | AG-UI + CopilotKit community |

**Recommendation**: Use **AG-UI** for most UI integrations due to:
- Pre-built React components
- Extensive examples
- Multi-framework portability
- Active community support

---

## Testing & Development

### Run Tests

```bash
cd typescript-sdk/integrations/adk-middleware
pytest
# 271 comprehensive tests

# With coverage
pytest --cov=src/adk_middleware
```

### Development Setup

```bash
# Editable install
pip install -e .

# With dev dependencies
pip install -e ".[dev]"
```

### Manual Testing with Dojo

1. Start ADK backend: `uv run dev` (examples directory)
2. Start Dojo frontend: `pnpm run dev` (typescript-sdk directory)
3. Open: http://localhost:3000/adk-middleware
4. Test all 5 feature demos

---

## Key Findings for UI Integration Tutorials

### ✅ **High Confidence for Tutorials**

1. **AG-UI + React**: Extensive examples, official docs, production-ready
2. **AG-UI + Next.js 15**: Official support, Server Components compatible
3. **AG-UI + ADK**: Official partnership, well-documented
4. **Multiple Agent Patterns**: Clear examples for multi-agent UIs

### ⚠️ **Considerations**

1. **Additional Dependency**: Requires AG-UI middleware package
2. **Event Translation**: ADK events → AG-UI events (slight overhead)
3. **Framework Lock-in**: Tied to CopilotKit ecosystem
4. **TypeScript Bias**: Frontend SDKs are TypeScript-first

### 🎯 **Tutorial Viability**

| Integration | Confidence | Reason |
|-------------|-----------|--------|
| AG-UI + React | **HIGH** | Official examples, docs, 271 tests |
| AG-UI + Next.js 15 | **HIGH** | Official support, Server Components |
| AG-UI + Streamlit | **MEDIUM** | No official SDK, custom client needed |
| AG-UI + Slack | **MEDIUM** | Webhooks supported, needs custom adapter |

---

## Next Steps

1. ✅ **Completed**: AG-UI framework research and ADK integration
2. ⏳ **Next**: Research official Google ADK documentation
3. ⏳ **Next**: Web research for Pub/Sub, Next.js, React Vite, Streamlit, Slack examples
4. ⏳ **Next**: Assess all findings and plan tutorial series

---

## Resources

- **AG-UI Repository**: https://github.com/ag-ui-protocol/ag-ui
- **ADK Middleware**: `research/ag-ui/typescript-sdk/integrations/adk-middleware/`
- **Documentation**: https://docs.copilotkit.ai/adk
- **Dojo Examples**: https://dojo.ag-ui.com/adk-middleware
- **Discord Community**: https://discord.gg/Jd3FzfdJa8
- **Working Group**: Bi-weekly AG-UI meetings (https://lu.ma/CopilotKit)
