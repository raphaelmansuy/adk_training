---
id: ui_integration_intro
---

# Tutorial 29: Introduction to UI Integration & AG-UI Protocol

**Estimated Reading Time**: 35-45 minutes  
**Difficulty Level**: Intermediate  
**Prerequisites**: Tutorials 1-3 (ADK Basics), Tutorial 14 (Streaming & SSE)

---

## Table of Contents

1. [Overview](#overview)
2. [The ADK UI Integration Landscape](#the-adk-ui-integration-landscape)
3. [Understanding the AG-UI Protocol](#understanding-the-ag-ui-protocol)
4. [Integration Approaches](#integration-approaches)
5. [Quick Start: Your First AG-UI Integration](#quick-start-your-first-ag-ui-integration)
6. [Decision Framework](#decision-framework)
7. [Architecture Patterns](#architecture-patterns)
8. [Best Practices](#best-practices)
9. [Next Steps](#next-steps)

---

## Overview

### What You'll Learn

In this tutorial, you'll master the fundamentals of integrating Google ADK agents with user interfaces. You'll understand:

- **The UI integration landscape** - Different approaches and when to use each
- **AG-UI Protocol** - The official protocol for agent-UI communication  
- **Integration patterns** - React/Next.js, Streamlit, Slack, and event-driven architectures
- **Decision framework** - How to choose the right approach for your use case
- **Architecture patterns** - Production-ready deployment strategies

### Why UI Integration Matters

While ADK agents are powerful on their own, connecting them to user interfaces unlocks their full potential:

```
┌─────────────────────────────────────────────────────────────┐
│                  WHY UI INTEGRATION?                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  CLI Agent              →  Limited to technical users       │
│  API Agent              →  Requires custom client code      │
│  UI-Integrated Agent    →  ✅ Accessible to all users       │
│                            ✅ Rich interactions             │
│                            ✅ Production-ready              │
│                            ✅ Scalable                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Real-World Use Cases**:

- **Customer Support Chatbots** - Web-based chat interfaces for customer service
- **Data Analysis Dashboards** - Interactive ML/AI tools for business intelligence
- **Team Collaboration Bots** - Slack/Teams bots for enterprise workflows
- **Document Processing Systems** - Event-driven UI for document pipelines

---

## The ADK UI Integration Landscape

### Overview of Integration Options

Google ADK supports multiple UI integration paths, each optimized for different use cases:

```
┌────────────────────────────────────────────────────────────────┐
│                ADK UI INTEGRATION OPTIONS                       │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. AG-UI Protocol (CopilotKit)                                │
│     ├─ Best for: React/Next.js web applications                │
│     ├─ Features: Pre-built components, TypeScript SDK          │
│     └─ Tutorials: 29, 30, 31, 35                               │
│                                                                 │
│  2. Native ADK API (HTTP/SSE/WebSocket)                        │
│     ├─ Best for: Custom implementations, any framework         │
│     ├─ Features: Full control, no dependencies                 │
│     └─ Tutorials: 14, 29, 32                                   │
│                                                                 │
│  3. Direct Python Integration                                  │
│     ├─ Best for: Data apps, Streamlit, internal tools          │
│     ├─ Features: In-process, no HTTP overhead                  │
│     └─ Tutorial: 32                                            │
│                                                                 │
│  4. Messaging Platform Integration                             │
│     ├─ Best for: Team collaboration, Slack/Teams bots          │
│     ├─ Features: Native platform UX, rich formatting           │
│     └─ Tutorial: 33                                            │
│                                                                 │
│  5. Event-Driven Architecture                                  │
│     ├─ Best for: High-scale, asynchronous processing           │
│     ├─ Features: Pub/Sub, scalable, decoupled                  │
│     └─ Tutorial: 34                                            │
│                                                                 │
└────────────────────────────────────────────────────────────────┘
```

### Comparison Matrix

| Approach | Best For | Complexity | Scalability | Time to Production |
|----------|----------|------------|-------------|-------------------|
| **AG-UI Protocol** | Modern web apps | Low | High | ⚡ Fast (hours) |
| **Native API** | Custom frameworks | Medium | High | 🔨 Moderate (days) |
| **Direct Python** | Data apps | Low | Medium | ⚡ Fast (hours) |
| **Slack/Teams** | Team tools | Low | High | ⚡ Fast (hours) |
| **Pub/Sub** | Event-driven | High | Very High | 🔨 Complex (weeks) |

---

## Understanding the AG-UI Protocol

### What is AG-UI?

**AG-UI (Agent-Generative UI)** is an open protocol for agent-user interaction, developed through an **official partnership between Google ADK and CopilotKit**. It provides a standardized way for AI agents to communicate with web UIs.

```
┌──────────────────────────────────────────────────────────────┐
│                    AG-UI PROTOCOL STACK                       │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Frontend (React/Next.js)                                    │
│  ├─ @copilotkit/react-core    (TypeScript SDK)              │
│  ├─ <CopilotChat>             (Pre-built UI)                │
│  └─ useCopilotAction()        (Custom actions)              │
│                                                               │
│  ↕ (WebSocket/SSE)                                           │
│                                                               │
│  Backend (Python)                                            │
│  ├─ ag_ui_adk                 (Protocol adapter)            │
│  ├─ ADKAgent wrapper          (Agent integration)           │
│  └─ FastAPI/Flask             (HTTP server)                 │
│                                                               │
│  ↕                                                            │
│                                                               │
│  Google ADK Agent                                            │
│  └─ Your agent logic                                         │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### Key Features

**1. Event-Based Communication**

AG-UI uses events for agent-UI communication:

```typescript
// Frontend sends action request
{
  "type": "action",
  "name": "analyze_data",
  "arguments": { "dataset": "sales_2024.csv" }
}

// Agent sends progress updates
{
  "type": "textMessage",
  "content": "Analyzing sales data..."
}

// Agent sends result
{
  "type": "actionResult",
  "actionName": "analyze_data",
  "result": { "revenue": 1500000, "growth": 0.15 }
}
```

**2. Pre-Built React Components**

```tsx
import { CopilotChat } from "@copilotkit/react-ui";

// Drop-in chat UI with zero configuration
<CopilotChat />
```

**3. Generative UI**

Agents can render custom React components:

```python
# Agent returns structured data
return {
    "component": "DataVisualization",
    "props": {
        "chartType": "bar",
        "data": sales_data
    }
}
```

**4. Production-Ready Middleware**

```python
from ag_ui_adk import ADKAgent
from google.adk.agents import Agent

# Create ADK agent and wrap it
adk_agent = Agent(
    name="customer_support",
    model="gemini-2.0-flash-exp"
)
agent = ADKAgent(adk_agent=adk_agent, app_name="customer_support")
```

### Why AG-UI Protocol?

**✅ Advantages**:

- **Official Support** - Partnership with Google ADK team
- **Pre-Built Components** - `<CopilotChat>`, `<CopilotTextarea>`
- **TypeScript SDK** - Type-safe React integration
- **Extensive Examples** - Production-ready code
- **Active Community** - Discord, GitHub discussions
- **Comprehensive Testing** - 271 tests passing

**⚠️ Considerations**:

- Additional dependency (CopilotKit packages)
- TypeScript-first ecosystem (though JS works)
- Event translation overhead (minimal, ~5ms)

---

## Integration Approaches

### Approach 1: AG-UI Protocol (Recommended for Web Apps)

**When to Use**:
- Building React/Next.js web applications
- Need pre-built UI components
- Want TypeScript type safety
- Prefer official, well-documented patterns

**Architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  User Browser                                               │
│  ├─ React App                                               │
│  ├─ CopilotKit Provider                                     │
│  └─ <CopilotChat> component                                 │
│                                                              │
│         ↕ (WebSocket/SSE)                                    │
│                                                              │
│  Backend Server (FastAPI)                                   │
│  ├─ ag_ui_adk                  (AG-UI Protocol adapter)     │
│  ├─ ADKAgent wrapper           (Session management)         │
│  └─ Your ADK agent             (google.adk.agents.LlmAgent) │
│                                                              │
│         ↕                                                    │
│                                                              │
│  Gemini API                                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Quick Example**:

```typescript
// Frontend (Next.js)
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";

export default function Home() {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit">
      <CopilotChat
        instructions="You are a helpful customer support agent."
      />
    </CopilotKit>
  );
}
```

```python
# Backend (Python)
from fastapi import FastAPI
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from google.adk.agents import Agent

app = FastAPI()

adk_agent = Agent(name="support", model="gemini-2.0-flash-exp")
agent = ADKAgent(
    adk_agent=adk_agent,
    app_name="support_app",
    user_id="user",
    use_in_memory_services=True
)

add_adk_fastapi_endpoint(app, agent, path="/api/copilotkit")
```

**Covered in**: Tutorial 30 (Next.js), Tutorial 31 (Vite), Tutorial 35 (Advanced)

---

### Approach 2: Native ADK API

**When to Use**:
- Building custom UI frameworks (Vue, Svelte, Angular)
- Need full control over transport layer
- Want to minimize dependencies
- Building mobile apps (React Native, Flutter)

**Architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  Your UI (Any Framework)                                    │
│  ├─ Custom HTTP client                                      │
│  ├─ WebSocket/SSE handler                                   │
│  └─ Custom UI components                                    │
│                                                              │
│         ↕ (HTTP/SSE/WebSocket)                              │
│                                                              │
│  ADK Web Server                                             │
│  ├─ /run (HTTP)                                             │
│  ├─ /run_sse (Server-Sent Events)                           │
│  └─ /run_live (WebSocket)                                   │
│                                                              │
│         ↕                                                    │
│                                                              │
│  Your ADK Agent                                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Quick Example**:

```typescript
// Frontend (Any framework)
const response = await fetch('http://localhost:8000/run', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    session_id: 'user-123',
    user_content: [{ text: 'What is ADK?' }]
  })
});

const result = await response.json();
console.log(result.agent_content);
```

```python
# Backend (Python)
from google.adk.agents import Agent

# Create ADK agent
agent = Agent(
    model='gemini-2.0-flash-exp',
    name='my_agent',
    instruction='You are a helpful assistant that provides clear and concise answers.'
)

# For web server deployment, use: adk web agent.py
# Or integrate with FastAPI/Flask for custom HTTP endpoints
```

**Covered in**: Tutorial 14 (Streaming & SSE), Tutorial 29 (this tutorial)

---

### Approach 3: Direct Python Integration

**When to Use**:
- Building data apps with Streamlit
- Internal tools and dashboards
- ML/AI workflows
- Python-only stack

**Architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  Streamlit App (Python)                                     │
│  ├─ st.chat_message()                                       │
│  ├─ st.chat_input()                                         │
│  └─ Direct ADK integration (in-process)                     │
│                                                              │
│         ↕ (No HTTP - direct Python calls)                   │
│                                                              │
│  Your ADK Agent                                             │
│  └─ In-process execution                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Quick Example**:

```python
import streamlit as st
from google.adk.agents import Agent, Runner
from google.genai import types

# Initialize agent
agent = Agent(
    model='gemini-2.0-flash-exp',
    name='data_analyst',
    instruction='You are an expert data analyst who helps users understand their data.'
)

# Initialize runner
runner = Runner(app_name='streamlit_app', agent=agent)

# Streamlit UI
if prompt := st.chat_input("Ask me about your data"):
    st.chat_message("user").write(prompt)
    
    # Proper ADK execution pattern
    import asyncio
    events = asyncio.run(runner.run_async(
        user_id='user1',
        session_id='session1',
        new_message=types.Content(parts=[types.Part(text=prompt)], role='user')
    ))
    response_text = ''.join([e.content.parts[0].text for e in events if hasattr(e, 'content')])
    
    st.chat_message("assistant").write(response_text)
```

**Covered in**: Tutorial 32 (Streamlit)

---

### Approach 4: Messaging Platform Integration

**When to Use**:
- Building team collaboration tools
- Slack/Microsoft Teams bots
- Enterprise internal tools
- Need native platform UX

**Architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  Slack/Teams Platform                                       │
│  └─ Native messaging UI                                     │
│                                                              │
│         ↕ (Webhook/Event Subscription)                      │
│                                                              │
│  Your Bot Server                                            │
│  ├─ Slack Bolt SDK                                          │
│  ├─ Event handlers (@app.message)                           │
│  └─ ADK agent integration                                   │
│                                                              │
│         ↕                                                    │
│                                                              │
│  Your ADK Agent                                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Quick Example**:

```python
from slack_bolt import App
from google.adk.agents import Agent, Runner
from google.genai import types
import asyncio

app = App(token="xoxb-...")

# Initialize agent once at startup
agent = Agent(
    model='gemini-2.0-flash-exp',
    name='support_agent',
    instruction='You are a helpful Slack support bot that assists team members with their questions.'
)

# Initialize runner
runner = Runner(app_name='slack_bot', agent=agent)

@app.message("")
def handle_message(message, say):
    # Proper ADK execution pattern
    events = asyncio.run(runner.run_async(
        user_id=message['user'],
        session_id=message['channel'],
        new_message=types.Content(parts=[types.Part(text=message['text'])], role='user')
    ))
    response_text = ''.join([e.content.parts[0].text for e in events if hasattr(e, 'content')])
    
    # Reply in Slack thread
    say(response_text, thread_ts=message['ts'])

app.start(port=3000)
```

**Covered in**: Tutorial 33 (Slack)

---

### Approach 5: Event-Driven Architecture

**When to Use**:
- High-scale systems (millions of events)
- Asynchronous processing
- Multiple subscribers (fan-out)
- Decoupled architectures

**Architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  Web UI                                                     │
│  └─ WebSocket connection for real-time updates             │
│                                                              │
│         ↕                                                    │
│                                                              │
│  API Server                                                 │
│  ├─ Publishes events to Pub/Sub                            │
│  └─ WebSocket manager                                       │
│                                                              │
│         ↕                                                    │
│                                                              │
│  Google Cloud Pub/Sub                                       │
│  └─ Event distribution                                      │
│                                                              │
│         ↕                                                    │
│                                                              │
│  Agent Subscriber(s)                                        │
│  ├─ Pull messages from Pub/Sub                             │
│  ├─ Process with ADK agent                                  │
│  └─ Publish results back                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Quick Example**:

```python
from google.cloud import pubsub_v1
from google import genai

# Publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('my-project', 'agent-requests')

# Publish event
publisher.publish(topic_path, data=b'Process document X')

# Initialize agent once at startup (outside callback)
from google.adk.agents import Agent, Runner
from google.genai import types
import asyncio

agent = Agent(
    model='gemini-2.0-flash-exp',
    name='doc_processor',
    instruction='You process documents and extract key information.'
)

# Initialize runner
runner = Runner(app_name='pubsub_processor', agent=agent)

# Subscriber
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path('my-project', 'agent-sub')

def callback(message):
    # Proper ADK execution pattern
    events = asyncio.run(runner.run_async(
        user_id='system',
        session_id=message.message_id,
        new_message=types.Content(parts=[types.Part(text=message.data.decode())], role='user')
    ))
    
    # Publish result or acknowledge
    message.ack()

subscriber.subscribe(subscription_path, callback=callback)
```

**Covered in**: Tutorial 34 (Pub/Sub)

---

## Quick Start: Your First AG-UI Integration

Let's build a simple ADK agent with AG-UI in **under 10 minutes**!

### Prerequisites

```bash
# Python 3.9+
python --version

# Node.js 18+
node --version

# Google AI API Key
export GOOGLE_GENAI_API_KEY="your-api-key"
```

### Step 1: Create Backend (Python)

```bash
# Create project
mkdir adk-quickstart && cd adk-quickstart
mkdir backend && cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install google-genai fastapi uvicorn ag_ui_adk
```

Create `backend/agent.py`:

```python
"""Simple ADK agent with AG-UI integration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint

# Initialize FastAPI
app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create ADK agent with google.adk
from google.adk.agents import Agent

adk_agent = Agent(
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Run backend**:

```bash
python agent.py
```

### Step 2: Create Frontend (React + Vite)

```bash
# In new terminal, from project root
cd ..
npm create vite@latest frontend -- --template react-ts
cd frontend

# Install CopilotKit
npm install @copilotkit/react-core @copilotkit/react-ui
npm install
```

Update `frontend/src/App.tsx`:

```typescript
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

function App() {
  return (
    <div style={{ height: "100vh" }}>
      <CopilotKit runtimeUrl="http://localhost:8000/api/copilotkit">
        <div style={{ padding: "2rem" }}>
          <h1>ADK + AG-UI Quickstart</h1>
          <p>Ask me anything!</p>
        </div>
        <CopilotChat
          instructions="You are a helpful assistant powered by Google ADK."
          labels={{
            title: "ADK Assistant",
            initial: "Hi! I'm an AI assistant powered by Google ADK. How can I help you today?",
          }}
        />
      </CopilotKit>
    </div>
  );
}

export default App;
```

**Run frontend**:

```bash
npm run dev
```

### Step 3: Test It!

1. Open http://localhost:5173 in your browser
2. You'll see a chat interface
3. Type: "What is Google ADK?"
4. The agent responds using Gemini!

**🎉 Congratulations! You just built your first ADK UI integration in under 10 minutes!**

---

## Decision Framework

### Choosing the Right Approach

Use this decision tree to select the best integration approach:

```
START
  │
  ├─ Building a web app? ─── YES ──┐
  │                                 │
  │                                 ├─ Using React/Next.js? ─── YES ─→ AG-UI Protocol ✅
  │                                 │                                   (Tutorials 30, 31, 35)
  │                                 │
  │                                 └─ Using Vue/Svelte/Angular? ─→ Native API ⚙️
  │                                                                 (Tutorial 14, 29)
  │
  ├─ Building a data app? ─── YES ─→ Streamlit Direct Integration 📊
  │                                   (Tutorial 32)
  │
  ├─ Building a team bot? ─── YES ─→ Slack/Teams Integration 💬
  │                                   (Tutorial 33)
  │
  └─ Need high scale? ─── YES ─────→ Event-Driven (Pub/Sub) 🚀
                                      (Tutorial 34)
```

### Detailed Comparison

#### AG-UI Protocol vs Native API

| Factor | AG-UI Protocol | Native API |
|--------|---------------|------------|
| **Setup Time** | ⚡ 10 minutes | 🔨 1-2 hours |
| **UI Components** | ✅ Pre-built (`<CopilotChat>`) | ❌ Build yourself |
| **TypeScript Support** | ✅ Full type safety | ⚠️ Manual types |
| **Framework** | React/Next.js only | Any framework |
| **Dependencies** | CopilotKit + ag_ui_adk | None (just ADK) |
| **Documentation** | ✅ Extensive | ✅ Good |
| **Production Ready** | ✅ Yes (271 tests) | ✅ Yes |
| **Customization** | 🔶 Medium (theme, props) | ✅ Full control |

**Recommendation**: Use **AG-UI Protocol** for React/Next.js apps. Use **Native API** for other frameworks or when you need full control.

---

#### Web vs Python vs Messaging

| Use Case | Best Approach | Why? |
|----------|--------------|------|
| **Customer-facing SaaS** | AG-UI (Next.js) | Production-ready, scalable, great UX |
| **Internal data tools** | Streamlit | Fast dev, Python-only, built-in UI |
| **Team collaboration** | Slack/Teams | Native UX, no custom UI needed |
| **Document processing** | Pub/Sub | Async, scalable, decoupled |
| **Mobile app** | Native API | Framework-agnostic |

---

## Architecture Patterns

### Pattern 1: Monolith (Quick Start)

**Best for**: Prototypes, MVPs, small teams

```
┌────────────────────────────────┐
│   Single Server (Cloud Run)    │
│   ├─ FastAPI                   │
│   ├─ AG-UI endpoint            │
│   ├─ ADK agent                 │
│   └─ Static frontend files     │
└────────────────────────────────┘
```

**Pros**: Simple deployment, low cost  
**Cons**: Limited scalability

---

### Pattern 2: Separated Frontend/Backend (Recommended)

**Best for**: Production apps, scaling teams

```
┌──────────────────┐        ┌──────────────────┐
│  Frontend        │        │  Backend         │
│  (Vercel/Netlify)│ ◄────► │  (Cloud Run)     │
│  - Next.js       │  CORS  │  - FastAPI       │
│  - CopilotKit    │        │  - ADK Agent     │
└──────────────────┘        └──────────────────┘
```

**Pros**: Independent scaling, CDN for frontend  
**Cons**: CORS configuration needed

---

### Pattern 3: Microservices (Enterprise)

**Best for**: Large teams, high scale

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Frontend    │    │  API Gateway │    │  Agent Fleet │
│  (Vercel)    │◄──►│  (Cloud Run) │◄──►│  (GKE)       │
└──────────────┘    └──────────────┘    └──────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  Pub/Sub     │
                    │  Queue       │
                    └──────────────┘
```

**Pros**: Unlimited scale, fault isolation  
**Cons**: Complex infrastructure

---

## Best Practices

### 1. Session Management

**Always persist agent state for conversation continuity**:

```python
from google.adk.agents import Agent, Runner
from google.genai import types
import asyncio

# ❌ Bad: New agent every request (loses context)
@app.post("/chat")
def chat(message: str):
    agent = Agent(
        model='gemini-2.0-flash-exp',
        name='support_agent',
        instruction='You are a helpful support agent'
    )
    runner = Runner(app_name='support', agent=agent)
    events = asyncio.run(runner.run_async(
        user_id='user1',
        session_id='session1',
        new_message=types.Content(parts=[types.Part(text=message)], role='user')
    ))
    return ''.join([e.content.parts[0].text for e in events if hasattr(e, 'content')])

# ✅ Good: Initialize agent and runner once, reuse for conversations
agent = Agent(
    model='gemini-2.0-flash-exp',
    name='support_agent',
    instruction='You are a helpful support agent with conversation memory'
)
runner = Runner(app_name='support', agent=agent)

@app.post("/chat")
def chat(user_id: str, session_id: str, message: str):
    # Runner manages conversation history with session_id
    events = asyncio.run(runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=types.Content(parts=[types.Part(text=message)], role='user')
    ))
    return ''.join([e.content.parts[0].text for e in events if hasattr(e, 'content')])
```

---

### 2. Error Handling

**Gracefully handle agent failures**:

```python
from fastapi import HTTPException

@app.post("/chat")
async def chat(message: str):
    try:
        response = await agent.send_message(message)
        return {"response": response.text}
    except Exception as e:
        # Log error for debugging
        logger.error(f"Agent error: {e}")
        
        # Return friendly error to user
        raise HTTPException(
            status_code=500,
            detail="I'm having trouble processing that request. Please try again."
        )
```

---

### 3. Rate Limiting

**Protect your API from abuse**:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/chat")
@limiter.limit("10/minute")  # 10 requests per minute
async def chat(request: Request, message: str):
    # ... agent logic
    pass
```

---

### 4. Streaming for Better UX

**Stream responses for long-running agents**:

```typescript
// Frontend: Stream responses
const { messages, sendMessage, isLoading } = useCopilotChat({
  stream: true,  // Enable streaming
});

// User sees partial responses as agent thinks
```

```python
# Backend: Enable streaming
agent = ADKAgent(
    name="streaming_agent",
    model="gemini-2.0-flash-exp",
    stream=True  # Return partial responses
)
```

---

### 5. Monitoring & Observability

**Track agent performance**:

```python
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter

# Set up tracing
tracer = trace.get_tracer(__name__)

@app.post("/chat")
async def chat(message: str):
    with tracer.start_as_current_span("agent_chat"):
        span = trace.get_current_span()
        span.set_attribute("message_length", len(message))
        
        response = await agent.send_message(message)
        
        span.set_attribute("response_length", len(response.text))
        return response
```

---

## Next Steps

### Where to Go From Here

Now that you understand the UI integration landscape, choose your path:

#### **For Web Developers**

→ **Tutorial 30**: Next.js 15 + ADK Integration (AG-UI)  
Build a production-ready customer support chatbot with Next.js 15 and deploy to Vercel.

→ **Tutorial 31**: React Vite + ADK Integration (AG-UI)  
Create a lightweight data analysis dashboard with React Vite.

→ **Tutorial 35**: AG-UI Deep Dive - Building Custom Components  
Master advanced AG-UI features: generative UI, human-in-the-loop, custom components.

#### **For Python/Data Engineers**

→ **Tutorial 32**: Streamlit + ADK Integration  
Build interactive data apps with direct Python integration.

#### **For DevOps/Enterprise Teams**

→ **Tutorial 33**: Slack Bot Integration with ADK  
Create team collaboration bots for Slack.

→ **Tutorial 34**: Google Cloud Pub/Sub + Event-Driven Agents  
Design scalable, event-driven agent architectures.

---

### Additional Resources

**Official Documentation**:
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [AG-UI Protocol Docs](https://docs.copilotkit.ai)
- [CopilotKit GitHub](https://github.com/CopilotKit/CopilotKit)

**Sample Code**:
- [ADK Samples Repository](https://github.com/google/adk-samples)
- [gemini-fullstack Example](https://github.com/google/adk-samples/tree/main/gemini-fullstack)

**Community**:
- [CopilotKit Discord](https://discord.gg/copilotkit)
- [Google AI Community](https://discuss.ai.google.dev)

---

## Summary

### Key Takeaways

✅ **Multiple Integration Options**: AG-UI Protocol, Native API, Direct Python, Messaging, Pub/Sub  
✅ **AG-UI Protocol**: Official, production-ready solution for React/Next.js  
✅ **Decision Framework**: Choose based on framework, scale, and use case  
✅ **Quick Start**: Get running in under 10 minutes  
✅ **Best Practices**: Session management, error handling, streaming, monitoring  

### What's Next

You now have a comprehensive understanding of ADK UI integration. The next tutorials will dive deep into each integration approach with production-ready examples.

**Ready to build? Start with Tutorial 30 for web apps or Tutorial 32 for data apps!**

---

**🎉 Tutorial 29 Complete!**

**Next**: [Tutorial 30: Next.js 15 + ADK Integration](./30_nextjs_adk_integration.md)

---

**Questions or feedback?** Open an issue on the [ADK Training Repository](https://github.com/google/adk-training).
