# Next.js 15 & React Vite Integration Research

**Research Date**: 2025-10-08  
**Sources**: 
- CopilotKit/AG-UI documentation
- ADK Samples (gemini-fullstack)
- Official ADK docs

---

## Overview

This document consolidates research on integrating Google ADK agents with modern React frameworks: Next.js 15 and React Vite.

### Key Finding: Two Integration Approaches

1. **AG-UI Protocol (Recommended)** - Via CopilotKit middleware
2. **Native ADK API** - Direct FastAPI integration

---

## Integration Approach 1: AG-UI + CopilotKit (RECOMMENDED)

### Why AG-UI is Recommended

✅ **Production-ready UI components**
✅ **Official partnership** with Google ADK
✅ **TypeScript SDK** with React hooks
✅ **Extensive examples** and documentation
✅ **Multi-framework support**
✅ **Active community** and maintenance

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Frontend (Next.js 15 / React Vite)                      │
│  ┌───────────────────────────────────────────────────┐  │
│  │  @copilotkit/react-core                            │  │
│  │  - useCoAgent()                                    │  │
│  │  - useCopilotChat()                                │  │
│  │  - useCoAgentStateRender()                         │  │
│  └───────────────┬───────────────────────────────────┘  │
└──────────────────┼─────────────────────────────────────┘
                   │ HTTP/SSE
                   ▼
┌─────────────────────────────────────────────────────────┐
│  Backend (Python FastAPI)                                │
│  ┌───────────────────────────────────────────────────┐  │
│  │  AG-UI ADK Middleware                              │  │
│  │  from ag_ui_adk import ADKAgent                    │  │
│  └───────────────┬───────────────────────────────────┘  │
│                  │                                        │
│  ┌───────────────▼───────────────────────────────────┐  │
│  │  Google ADK Agent                                  │  │
│  │  - LlmAgent, SequentialAgent, etc.                 │  │
│  │  - Native ADK tools and capabilities               │  │
│  └─────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

---

## Next.js 15 Integration

### Project Structure

```
my-adk-nextjs-app/
├── app/
│   ├── api/
│   │   └── copilotkit/
│   │       └── route.ts          # API route for agent
│   ├── page.tsx                   # Main app page
│   └── layout.tsx                 # Root layout with CopilotKit
├── agent/                         # Python backend
│   ├── agent.py                   # ADK agent definition
│   ├── requirements.txt
│   └── .env                       # GOOGLE_API_KEY
└── package.json
```

### Step-by-Step Setup

#### 1. Create Next.js 15 App

```bash
npx create-next-app@latest my-adk-app --typescript --app --tailwind
cd my-adk-app
```

#### 2. Install CopilotKit Dependencies

```bash
npm install @copilotkit/react-core @copilotkit/react-ui
```

#### 3. Backend: Python ADK Agent

**agent/agent.py**:
```python
from fastapi import FastAPI
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from google.adk.agents import LlmAgent
from google.adk.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get current weather for a location."""
    return f"Weather in {location}: Sunny, 72°F"

# Define ADK agent
my_agent = LlmAgent(
    name="assistant",
    model="gemini-2.0-flash",
    instruction="You are a helpful assistant.",
    tools=[get_weather]
)

# Wrap with AG-UI middleware
adk_agent = ADKAgent(
    adk_agent=my_agent,
    app_name="my_app",
    user_id="demo",
    use_in_memory_services=True
)

# Create FastAPI app
app = FastAPI()
add_adk_fastapi_endpoint(app, adk_agent, path="/chat")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**agent/requirements.txt**:
```txt
google-adk
ag-ui-adk
fastapi
uvicorn[standard]
```

#### 4. Frontend: Next.js API Route

**app/api/copilotkit/route.ts**:
```typescript
import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const body = await req.json();
  
  // Proxy to backend
  const response = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  // Forward SSE stream
  if (response.headers.get("content-type")?.includes("text/event-stream")) {
    return new NextResponse(response.body, {
      headers: {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
      },
    });
  }

  const data = await response.json();
  return NextResponse.json(data);
}
```

#### 5. Frontend: Root Layout

**app/layout.tsx**:
```typescript
import { CopilotKit } from "@copilotkit/react-core";
import "./globals.css";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <CopilotKit runtimeUrl="/api/copilotkit">
          {children}
        </CopilotKit>
      </body>
    </html>
  );
}
```

#### 6. Frontend: Main Page

**app/page.tsx**:
```typescript
"use client";

import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

export default function Home() {
  return (
    <main className="h-screen">
      <CopilotChat
        labels={{
          title: "My ADK Assistant",
          initial: "Hi! How can I help you today?",
        }}
      />
    </main>
  );
}
```

#### 7. Run the Application

Terminal 1 (Backend):
```bash
cd agent
python agent.py
```

Terminal 2 (Frontend):
```bash
npm run dev
```

Visit: http://localhost:3000

---

## React Vite Integration

### Project Structure

```
my-adk-vite-app/
├── src/
│   ├── App.tsx                    # Main app component
│   ├── main.tsx                   # Entry point with CopilotKit
│   └── index.css
├── agent/                         # Python backend (same as Next.js)
│   ├── agent.py
│   └── requirements.txt
├── package.json
└── vite.config.ts
```

### Step-by-Step Setup

#### 1. Create Vite App

```bash
npm create vite@latest my-adk-vite-app -- --template react-ts
cd my-adk-vite-app
```

#### 2. Install Dependencies

```bash
npm install @copilotkit/react-core @copilotkit/react-ui
```

#### 3. Backend (Same as Next.js)

Use the same `agent/agent.py` from Next.js example above.

#### 4. Configure Vite Proxy

**vite.config.ts**:
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api/copilotkit': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/copilotkit/, '/chat'),
      },
    },
  },
})
```

#### 5. Main Entry Point

**src/main.tsx**:
```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import { CopilotKit } from "@copilotkit/react-core"
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <CopilotKit runtimeUrl="/api/copilotkit">
      <App />
    </CopilotKit>
  </React.StrictMode>,
)
```

#### 6. App Component

**src/App.tsx**:
```typescript
import { CopilotChat } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

function App() {
  return (
    <div style={{ height: "100vh" }}>
      <CopilotChat
        labels={{
          title: "My ADK Assistant",
          initial: "Hi! How can I help you today?",
        }}
      />
    </div>
  );
}

export default App;
```

#### 7. Run the Application

Terminal 1 (Backend):
```bash
cd agent
python agent.py
```

Terminal 2 (Frontend):
```bash
npm run dev
```

Visit: http://localhost:5173

---

## Advanced Features with AG-UI

### 1. Generative UI (Tool-Based)

**Backend** (agent.py):
```python
from google.adk.tools import tool
from typing import List, Dict

@tool
def create_chart(data: List[Dict[str, any]], chart_type: str) -> dict:
    """Generate a chart visualization."""
    return {
        "component": "Chart",
        "props": {
            "data": data,
            "type": chart_type
        }
    }
```

**Frontend** (Next.js/Vite):
```typescript
import { useCoAgent } from "@copilotkit/react-core";
import { BarChart } from "@/components/charts";

function MyComponent() {
  useCoAgent({
    name: "assistant",
    render: ({ name, args, result }) => {
      if (name === "create_chart") {
        return <BarChart {...args} />;
      }
    },
  });
}
```

### 2. Shared State

**Backend**:
```python
from google.adk.agents.callback_context import CallbackContext

def on_before_agent(callback_context: CallbackContext):
    if "user_preferences" not in callback_context.state:
        callback_context.state["user_preferences"] = {
            "theme": "dark",
            "language": "en"
        }

my_agent = LlmAgent(
    name="assistant",
    model="gemini-2.0-flash",
    before_agent_callback=on_before_agent
)
```

**Frontend**:
```typescript
import { useCoAgent } from "@copilotkit/react-core";

type AgentState = {
  user_preferences: {
    theme: string;
    language: string;
  };
};

function PreferencesPanel() {
  const { state } = useCoAgent<AgentState>({
    name: "assistant",
  });

  return (
    <div>
      <p>Theme: {state?.user_preferences?.theme}</p>
      <p>Language: {state?.user_preferences?.language}</p>
    </div>
  );
}
```

### 3. Human-in-the-Loop

**Backend**:
```python
from google.adk.tools import long_running_tool

@long_running_tool
async def request_approval(action: str, details: dict) -> bool:
    """Request human approval for an action."""
    # This will pause agent execution and emit HumanInputRequestEvent
    # Agent waits for HumanInputResponseEvent from frontend
    return True  # Approved

my_agent = LlmAgent(
    name="assistant",
    model="gemini-2.0-flash",
    tools=[request_approval]
)
```

**Frontend**: Automatic handling via CopilotKit UI

---

## Real-World Example: Gemini Fullstack

**Source**: https://github.com/google/adk-samples/tree/main/python/agents/gemini-fullstack

### Architecture

```
Frontend (React + Vite)
├── TypeScript + Tailwind
├── Shadcn UI components
└── CopilotKit integration

Backend (Python + FastAPI)
├── Multi-agent research pipeline
├── Sequential workflow
├── Human-in-the-loop planning
└── Web search integration
```

### Key Features

1. **Two-Phase Workflow**
   - Phase 1: Interactive planning (HITL)
   - Phase 2: Autonomous research execution

2. **Multi-Agent System**
   - Planner agent
   - Researcher agent
   - Critic agent
   - Composer agent

3. **State Management**
   - Research plan in shared state
   - Progress tracking
   - Iterative refinement

4. **Frontend Integration**
   - Real-time progress timeline
   - Agent state rendering
   - Interactive plan editing
   - Final report display

### Installation

```bash
git clone https://github.com/google/adk-samples.git
cd adk-samples/python/agents/gemini-fullstack

# Set environment variables
echo "GOOGLE_API_KEY=your-key" >> app/.env

# Install and run
make install && make dev
```

---

## Integration Approach 2: Native ADK API (Direct)

### When to Use

- ✅ Need full control over transport layer
- ✅ Custom WebSocket implementation
- ✅ Non-React frontend (Vue, Svelte, vanilla JS)
- ✅ Mobile app integration
- ❌ Don't use if AG-UI covers your needs

### Architecture

```
Frontend → HTTP/SSE/WebSocket → FastAPI (ADK CLI) → ADK Agent
```

### Backend Setup

```bash
# Start ADK API server
adk api_server --agent-dir ./agents --web --allow-origins "*"
```

Or programmatically:

```python
from google.adk.cli.fast_api import get_fast_api_app

app = get_fast_api_app(
    agent_dir="./agents",
    web=True,
    allow_origins=["http://localhost:3000"]
)
```

### Frontend: Next.js Example

**app/api/agent/route.ts**:
```typescript
import { NextRequest } from "next/server";

export async function POST(req: NextRequest) {
  const { message, sessionId } = await req.json();
  
  const response = await fetch("http://localhost:8000/run_sse", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      app_name: "my_agent",
      user_id: "user123",
      session_id: sessionId,
      new_message: {
        role: "user",
        parts: [{ text: message }]
      },
      streaming: true
    }),
  });

  return new Response(response.body, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
    },
  });
}
```

**components/ChatInterface.tsx**:
```typescript
"use client";

import { useState } from "react";

export function ChatInterface() {
  const [messages, setMessages] = useState<string[]>([]);
  const [input, setInput] = useState("");
  
  async function sendMessage() {
    const response = await fetch("/api/agent", {
      method: "POST",
      body: JSON.stringify({
        message: input,
        sessionId: "sess123",
      }),
    });

    const reader = response.body!.getReader();
    const decoder = new TextDecoder();
    let assistantMessage = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      
      const chunk = decoder.decode(value);
      const lines = chunk.split("\n");
      
      for (const line of lines) {
        if (line.startsWith("data:")) {
          const event = JSON.parse(line.slice(5));
          if (event.content?.parts?.[0]?.text) {
            assistantMessage += event.content.parts[0].text;
            setMessages(prev => [...prev.slice(0, -1), assistantMessage]);
          }
        }
      }
    }
  }

  return (
    <div>
      {messages.map((msg, i) => (
        <div key={i}>{msg}</div>
      ))}
      <input value={input} onChange={e => setInput(e.target.value)} />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}
```

### Frontend: React Vite Example

**src/hooks/useADKAgent.ts**:
```typescript
import { useState, useCallback } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export function useADKAgent() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = useCallback(async (content: string) => {
    setIsLoading(true);
    setMessages(prev => [...prev, { role: "user", content }]);

    try {
      const response = await fetch("http://localhost:8000/run_sse", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          app_name: "my_agent",
          user_id: "user123",
          session_id: "sess123",
          new_message: {
            role: "user",
            parts: [{ text: content }]
          },
          streaming: true
        }),
      });

      const reader = response.body!.getReader();
      const decoder = new TextDecoder();
      let assistantMessage = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const lines = chunk.split("\n");
        
        for (const line of lines) {
          if (line.startsWith("data:")) {
            const event = JSON.parse(line.slice(5));
            if (event.content?.parts?.[0]?.text) {
              assistantMessage += event.content.parts[0].text;
              setMessages(prev => {
                const updated = [...prev];
                if (updated[updated.length - 1]?.role === "assistant") {
                  updated[updated.length - 1].content = assistantMessage;
                } else {
                  updated.push({ role: "assistant", content: assistantMessage });
                }
                return updated;
              });
            }
          }
        }
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { messages, sendMessage, isLoading };
}
```

---

## Comparison: AG-UI vs Native API

| Aspect | AG-UI (CopilotKit) | Native ADK API |
|--------|-------------------|----------------|
| **Setup Complexity** | Low (npm + pip packages) | Medium (manual client) |
| **UI Components** | Pre-built (`<CopilotChat>`) | DIY |
| **TypeScript Support** | Full SDK with types | Manual types |
| **State Management** | Built-in hooks | Manual implementation |
| **Streaming** | Automatic | Manual SSE parsing |
| **Tool Rendering** | Declarative | Manual |
| **Human-in-Loop** | Built-in UI | Custom modals |
| **Learning Curve** | Low (React patterns) | Medium (ADK API docs) |
| **Flexibility** | Medium | High |
| **Best For** | React apps, rapid development | Custom UIs, non-React |

---

## Production Deployment

### Next.js 15 (Vercel)

**Frontend** (Vercel):
```bash
vercel deploy
```

**Backend** (Google Cloud Run):
```bash
gcloud run deploy adk-agent \
  --source ./agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

Update `runtimeUrl` in Next.js:
```typescript
<CopilotKit runtimeUrl="https://adk-agent-xyz.run.app/chat">
```

### React Vite (Netlify/Vercel)

**Build Configuration**:
```json
{
  "build": {
    "command": "npm run build",
    "publish": "dist"
  },
  "redirects": [
    {
      "from": "/api/copilotkit/*",
      "to": "https://adk-agent-xyz.run.app/chat/:splat",
      "status": 200
    }
  ]
}
```

---

## Key Findings

### ✅ High Confidence for Tutorials

1. **AG-UI + Next.js 15**: Official support, extensive docs, production examples
2. **AG-UI + React Vite**: Same patterns as Next.js, proven in gemini-fullstack
3. **Native API + Next.js**: Documented in ADK official docs, clear patterns
4. **Native API + Vite**: Straightforward HTTP/SSE client implementation

### ⚠️ Considerations

1. **AG-UI Dependency**: Additional npm package, CopilotKit ecosystem
2. **Event Translation**: ADK events → AG-UI events (minimal overhead)
3. **Version Compatibility**: Ensure AG-UI middleware matches ADK version
4. **CORS Configuration**: Required for local development

### 🎯 Recommendations

**For Most Users**: Use **AG-UI + CopilotKit**
- Faster development
- Production-ready UI
- Extensive examples
- Active support

**For Advanced Users**: Use **Native ADK API**
- Full control
- Custom WebSocket
- Non-React frontends
- Mobile apps

---

## Next Steps

1. ✅ **Completed**: Next.js 15 and React Vite research
2. ⏳ **Next**: Research Streamlit integration patterns
3. ⏳ **Next**: Research Slack Bolt integration
4. ⏳ **Next**: Research Google Cloud Pub/Sub patterns
5. ⏳ **Next**: Verify version compatibility with ADK source

---

## Resources

- **AG-UI Docs**: https://docs.copilotkit.ai/adk
- **ADK Samples**: https://github.com/google/adk-samples
- **Gemini Fullstack**: https://github.com/google/adk-samples/tree/main/python/agents/gemini-fullstack
- **CopilotKit GitHub**: https://github.com/copilotkit/copilotkit
- **AG-UI Protocol**: https://github.com/ag-ui-protocol/ag-ui
- **ADK Docs**: https://google.github.io/adk-docs/
