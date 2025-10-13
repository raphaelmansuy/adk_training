# Tutorial 30: Next.js ADK Integration

A complete implementation of a customer support chatbot using Next.js 15, CopilotKit, and Google ADK with AG-UI Protocol.

## 🚀 Quick Start

```bash
# 1. Install dependencies
make setup

# 2. Configure API key
cp agent/.env.example agent/.env
# Edit agent/.env and add your GOOGLE_API_KEY

# 3. Start both backend and frontend
make dev

# 4. Open http://localhost:3000 in your browser
```

## 📋 What's Included

This implementation demonstrates:

- ✅ **Python ADK Agent** with custom tools
- ✅ **FastAPI backend** with AG-UI integration
- ✅ **Next.js 15 frontend** with CopilotKit
- ✅ **Real-time chat interface** with streaming
- ✅ **Tool-augmented responses** (knowledge base, order lookup, ticket creation)
- ✅ **Comprehensive test suite** (30+ tests)
- ✅ **Production-ready architecture**

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  USER'S BROWSER                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Next.js 15 App (Port 3000)                          │  │
│  │  ├─ app/page.tsx (Chat UI)                           │  │
│  │  │  └─ <CopilotKit> provider                         │  │
│  │  │     └─ <CopilotChat> component                    │  │
│  │  │                                                     │  │
│  │  └─ @copilotkit/react-core (TypeScript SDK)          │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ AG-UI Protocol (HTTP/SSE)
                        │
┌───────────────────────▼─────────────────────────────────────┐
│  BACKEND SERVER (Port 8000)                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FastAPI + ag_ui_adk                                 │  │
│  │  ├─ /api/copilotkit endpoint                         │  │
│  │  ├─ AG-UI protocol adapter                           │  │
│  │  └─ Session management                               │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                   │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │  Google ADK Agent                                    │  │
│  │  ├─ model: "gemini-2.0-flash-exp"                    │  │
│  │  ├─ tools: [search_knowledge_base,                   │  │
│  │  │          lookup_order_status,                     │  │
│  │  │          create_support_ticket]                   │  │
│  │  └─ instruction: Customer support prompt             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                        │
                        │ Gemini API
                        │
┌───────────────────────▼─────────────────────────────────────┐
│  GEMINI 2.0 FLASH                                            │
│  ├─ Text generation                                          │
│  ├─ Function calling                                         │
│  └─ Streaming responses                                      │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
tutorial30/
├── agent/                      # Python backend
│   ├── __init__.py
│   ├── agent.py               # ADK agent + FastAPI app
│   └── .env.example           # Environment template
├── nextjs_frontend/           # Next.js frontend
│   ├── app/
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Chat page with CopilotKit & advanced features
│   │   ├── advanced/
│   │   │   └── page.tsx       # Advanced features demo page
│   │   └── globals.css        # Tailwind styles
│   ├── components/
│   │   ├── ThemeToggle.tsx    # Dark/light mode toggle
│   │   └── ProductCard.tsx    # Generative UI product card
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   └── tailwind.config.ts
├── tests/                     # Test suite
│   ├── test_agent.py          # Agent configuration tests
│   ├── test_imports.py        # Import validation
│   ├── test_structure.py      # Project structure tests
│   └── test_tools.py          # Tool function tests (including advanced features)
├── Makefile                   # Build commands
├── README.md                  # This file
├── requirements.txt           # Python dependencies
└── pyproject.toml            # Python package config
```

## ⚡ Advanced Features

This implementation includes three powerful advanced features from Tutorial 30:

### 1. 🎨 Generative UI

The agent can render rich, interactive React components directly in the chat:

- **Product Cards**: Display products with images, prices, ratings, and stock status
- **Dynamic Components**: Agent decides when to use visual components vs text
- **Implementation**: `create_product_card()` tool returns structured data, `ProductCard` component renders it

**Try it**: "Show me product PROD-001"

### 2. 🔐 Human-in-the-Loop (HITL)

Sensitive operations require explicit user approval:

- **Refund Approval**: User must confirm before processing refunds
- **Confirmation Dialog**: Clear display of action details before approval
- **Cancellation**: Users can deny requests, agent continues with alternative

**Try it**: "I want a refund for order ORD-12345"

### 3. 👤 Shared State

Agent has real-time access to user context without asking:

- **User Data**: Name, email, account type automatically available
- **Order History**: Agent knows your orders (ORD-12345, ORD-67890)
- **Member Info**: Join date and account status accessible

**Try it**: "What's my account status?"

**Learn More**: Visit `/advanced` in the running app for detailed implementation documentation.

## 🏠 Home Page Structure

The main page (`http://localhost:3000`) includes:

1. **Header Section**
   - Support Assistant branding
   - User account display (logged in as John Doe)
   - Advanced Features navigation link
   - Dark/Light mode toggle

2. **Chat Interface** (Fixed height: 600px)
   - Real-time AI chat with CopilotKit
   - Example prompts in initial message
   - Streaming responses
   - Tool execution feedback

3. **Feature Showcase** (Below chat, scrollable)
   - **Tabbed Interface**: Switch between three features
   - **Generative UI Tab**: Live ProductCard examples
   - **HITL Tab**: Mock refund approval dialog
   - **Shared State Tab**: User account information display
   - Appears directly on home page for immediate discoverability

**User Flow**:
- Land on page → See chat with example prompts
- Scroll down → Discover advanced features with live demos
- Click tabs → Explore each feature interactively
- Visit `/advanced` → Read implementation details

## 🛠️ Available Commands

### Setup

```bash
make setup              # Install all dependencies (backend + frontend)
make setup-backend      # Install only backend dependencies
make setup-frontend     # Install only frontend dependencies
```

### Development

```bash
make dev                # Start both backend and frontend
make dev-backend        # Start only backend (port 8000)
make dev-frontend       # Start only frontend (port 3000)
```

### Testing

```bash
make test               # Run all tests
make demo               # Show demo prompts
```

### Cleanup

```bash
make clean              # Remove generated files
```

## 💬 Try These Prompts

### Knowledge Base Queries

- "What is your refund policy?"
- "How long does shipping take?"
- "Tell me about your warranty"
- "How do I reset my password?"

### Order Status Lookup

- "Check order status for ORD-12345"
- "What's the status of order ORD-67890?"
- "Track my order ORD-11111"

### Support Ticket Creation

- "My product stopped working after 2 months"
- "I need help with a billing issue"
- "Create a ticket for account access problems"

### Advanced Features

#### Generative UI (Feature 1)
- "Show me product PROD-001"
- "What products do you have available?"
- "Tell me about the Widget Pro" (displays product card)
- "Display product PROD-002" (shows Gadget Plus)

#### Human-in-the-Loop (Feature 2)
- "I want a refund for order ORD-12345"
- "Process a refund of $99.99 for my order"
- "Can you refund my purchase?" (requires approval dialog)

#### Shared State (Feature 3)
- "What's my account status?" (agent knows your name)
- "Show me my recent orders" (agent has order history)
- "When did I join?" (agent knows member since date)

## 🔧 Configuration

### Backend Configuration

Edit `agent/.env`:

```bash
# Required
GOOGLE_API_KEY=your_api_key_here

# Optional
PORT=8000
HOST=0.0.0.0
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Frontend Configuration

Edit `nextjs_frontend/.env`:

```bash
NEXT_PUBLIC_AGENT_URL=http://localhost:8000
```

## 🧪 Testing

The implementation includes comprehensive tests:

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_agent.py -v
pytest tests/test_tools.py -v
```

**Test Coverage:**

- ✅ Agent configuration validation
- ✅ Tool function behavior
- ✅ Project structure verification
- ✅ Import validation
- ✅ FastAPI endpoint configuration
- ✅ Error handling

## 🚢 Deployment

### Option 1: Development (Local)

```bash
make dev
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

### Option 2: Production (Cloud Run + Vercel)

**Backend (Google Cloud Run):**

```bash
cd agent
gcloud run deploy customer-support-agent \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_API_KEY=your_key"
```

**Frontend (Vercel):**

```bash
cd nextjs_frontend
vercel

# Set environment variable
vercel env add NEXT_PUBLIC_AGENT_URL production
# Enter: https://customer-support-agent-xyz.run.app
```

## 🔑 Authentication

This implementation supports two authentication methods:

### Method 1: API Key (Gemini API)

```bash
export GOOGLE_API_KEY=your_api_key_here
# Get a free key at: https://aistudio.google.com/app/apikey
```

### Method 2: Service Account (VertexAI)

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
export GOOGLE_CLOUD_PROJECT=your_project_id
# Create at: https://console.cloud.google.com/iam-admin/serviceaccounts
```

## 🐛 Troubleshooting

### Backend Issues

**Problem:** `ImportError: No module named 'ag_ui_adk'`

```bash
# Solution: Install dependencies
make setup-backend
```

**Problem:** `Authentication failed`

```bash
# Solution: Check API key
echo $GOOGLE_API_KEY  # Should show your key
# Or set it:
export GOOGLE_API_KEY=your_key
```

### Frontend Issues

**Problem:** Frontend can't connect to backend

```bash
# Solution: Check backend is running
curl http://localhost:8000/health
# Should return: {"status": "healthy"}
```

**Problem:** CORS errors in browser console

```bash
# Solution: Check CORS configuration in agent/agent.py
# Make sure your frontend URL is in allow_origins list
```

### Connection Issues

**Problem:** Chat doesn't respond

## 🐛 Troubleshooting

### Common Issues

#### 1. 422 Unprocessable Entity Errors ✅ NORMAL

**Symptom**: Browser console shows:
```
Failed to load resource: the server responded with a status of 422 (Unprocessable Entity)
POST http://localhost:8000/api/copilotkit 422
```

**This is EXPECTED and HARMLESS!** 

CopilotKit sends initial handshake requests during page load that don't match the AG-UI protocol schema. FastAPI's validation returns 422, CopilotKit automatically retries, and the connection succeeds when you send your first message.

**Action**: ✅ No action needed - this is by design

**Want the full explanation?** See [TROUBLESHOOTING_422.md](./TROUBLESHOOTING_422.md) for a complete technical breakdown with verification steps.

#### 1b. "Agent Not Found" Error ⚠️ FIXED

**Symptom**: Red banner at bottom of chat interface says:
```
The requested agent was not found. Please set up at least one agent before proceeding.
```

**Fix Applied**: Removed the `agent="customer_support_agent"` prop from `<CopilotKit>` component. The AG-UI protocol automatically discovers the agent from the backend.

**If you still see this error**:
1. Make sure backend is running: `curl http://localhost:8000/health`
2. Check browser console for connection errors
3. Verify `/api/copilotkit` endpoint exists: `curl http://localhost:8000/docs`

#### 1c. EmptyAdapter Requires Agent Lock Mode ✅ FIXED

**Symptom**: Error in browser console:
```
Invalid adapter configuration: EmptyAdapter is only meant to be used with agent lock mode.
For non-agent components like useCopilotChatSuggestions, CopilotTextarea, or CopilotTask,
please use an LLM adapter instead.
```

**Root Cause**: When using `ExperimentalEmptyAdapter` (which delegates all LLM calls to your AG-UI agent), CopilotKit requires "agent lock mode" to be enabled. This ensures all requests go through your specific agent rather than trying to use non-existent LLM adapters.

**Fix Applied**:

1. **Frontend (`page.tsx`)**: Added `agent` prop to CopilotKit component:
```tsx
<CopilotKit runtimeUrl="/api/copilotkit" agent="customer_support_agent">
  <ChatInterface />
</CopilotKit>
```

2. **Backend Route (`route.ts`)**: Ensured agent name matches:
```typescript
const runtime = new CopilotRuntime({
  agents: {
    customer_support_agent: new HttpAgent({ url: `${backendUrl}/api/copilotkit` }),
  },
});
```

**Why This Is Required**:
- `ExperimentalEmptyAdapter` has no LLM - it only proxies to your agents
- CopilotKit features like `useCopilotChatSuggestions` need an LLM
- Agent lock mode tells CopilotKit: "Use this specific agent for everything"
- Without it, CopilotKit tries to use EmptyAdapter's non-existent LLM → Error

**Verification**:
1. Check browser console - error should be gone
2. Agent name in `page.tsx` matches agent name in `route.ts`
3. Agent name in `route.ts` matches backend agent name (`customer_support_agent`)

#### 1d. [Network] Unknown Error Occurred ⚠️ KNOWN ISSUE

**Symptom**: Red banner at bottom of chat interface says:
```
[Network] Unknown error occurred
```

**Root Cause**: CopilotKit 1.10.6+ sends messages without the `id` field that AG-UI protocol requires. The backend validation rejects these messages, preventing the connection from establishing.

**Why This Happens**:
- AG-UI protocol requires UserMessage to have: `{id, role, content}`
- CopilotKit 1.10.6 only sends: `{role, content}`  
- FastAPI validation returns 422 for missing `id` field
- CopilotKit shows generic "Unknown error" instead of specific validation error

**Verification**:
1. Open Browser DevTools (F12) → Console tab
2. Look for: `{"detail":[{"type":"missing","loc":["body","messages",0,"user","id"],"msg":"Field required"...}]}`
3. This confirms the `id` field is missing

**Workaround Options**:

1. **Try Sending a Message Anyway**: Sometimes the error resolves after typing and sending
2. **Wait for ag_ui_adk Update**: The package maintainers are aware of this compatibility issue
3. **Use Alternative UI Framework**: Tutorial 32 (Streamlit) doesn't have this issue
4. **Check for Updates**: Run `pip install --upgrade ag-ui-adk` and restart backend

**Status**: 🔴 Known compatibility issue between CopilotKit 1.10.6 and ag_ui_adk 0.1.0

#### 2. Hydration Mismatch Warnings

**Want the full explanation?** See [TROUBLESHOOTING_422.md](./TROUBLESHOOTING_422.md) for a complete technical breakdown with verification steps.

#### 2. Hydration Mismatch Warnings

**Symptom**:
```
Warning: Prop `className` did not match. Server: "..." Client: "..."
```

**Cause**: Browser extensions (password managers, Grammarly) modify HTML before React loads

**Solutions**:
- Ignore the warning (doesn't affect functionality)
- Test in incognito mode
- Disable browser extensions temporarily

#### 3. Backend Won't Start

**Symptom**: `Error: GOOGLE_API_KEY not configured`

**Solutions**:
1. Create `agent/.env` file:
   ```bash
   cp agent/.env.example agent/.env
   ```
2. Add your API key:
   ```
   GOOGLE_API_KEY=your_key_here
   ```
3. Restart backend: `make dev`

#### 4. Frontend Build Errors

**Symptom**: `Cannot find module '@copilotkit/react-core'`

**Solutions**:
1. Install dependencies:
   ```bash
   cd nextjs_frontend && npm install
   ```
2. Or use Makefile:
   ```bash
   make setup
   ```

#### 5. Port Already in Use

**Symptom**: `Error: Address already in use`

**Solutions**:
1. Stop existing processes:
   ```bash
   # Find processes
   lsof -i :8000  # Backend
   lsof -i :3000  # Frontend
   
   # Kill processes
   kill -9 <PID>
   ```
2. Or use different ports in `.env` files

### Debugging Steps

1. **Check Backend Health**:
   ```bash
   curl http://localhost:8000/health
   ```
   Should return: `{"status": "healthy", ...}`

2. **Check API Documentation**:
   Open http://localhost:8000/docs

3. **Test Backend Directly**:
   ```bash
   cd agent && python agent.py
   ```
   Look for startup messages and errors

4. **Check Frontend Build**:
   ```bash
   cd nextjs_frontend && npm run build
   ```
   Should complete without errors

5. **View Network Requests**:
   - Open Browser DevTools (F12)
   - Go to Network tab
   - Send a chat message
   - Check request/response details

### Still Having Issues?

1. Check backend logs for errors
2. Verify API key is configured correctly
3. Ensure all dependencies are installed
4. Try `make clean && make setup`
5. Check the [implementation log](../../log/20251012_224000_tutorial30_implementation_complete.md) for detailed troubleshooting

## 📚 Learn More

- [Tutorial 30 Documentation](../../docs/tutorial/30_nextjs_adk_integration.md)
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [CopilotKit Documentation](https://docs.copilotkit.ai/adk)
- [Next.js 15 Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🎯 Key Features

### Customer Support Tools

1. **Knowledge Base Search** (`search_knowledge_base`)
   - Searches FAQs and documentation
   - Returns formatted articles
   - Handles unknown queries gracefully

2. **Order Status Lookup** (`lookup_order_status`)
   - Retrieves order details
   - Shows tracking information
   - Estimates delivery dates

3. **Support Ticket Creation** (`create_support_ticket`)
   - Generates unique ticket IDs
   - Priority-based response times
   - Detailed issue tracking

### Frontend Features

- Real-time streaming responses
- Beautiful Tailwind CSS styling
- Responsive design
- CopilotKit pre-built chat UI
- Environment-based configuration

### Backend Features

- FastAPI with auto-documentation
- AG-UI protocol integration
- CORS configuration for development
- Health check endpoint
- Structured logging

## 🔐 Security Notes

- ⚠️ Never commit `.env` files to version control
- ✅ Always use `.env.example` for templates
- ✅ Store API keys in environment variables
- ✅ Use service accounts for production
- ✅ Enable HTTPS in production
- ✅ Implement rate limiting for production deployments

## 📝 Next Steps

After completing this tutorial, explore:

- **Tutorial 31**: React Vite + ADK Integration (lighter weight alternative)
- **Tutorial 32**: Streamlit + ADK Integration (Python-only stack)
- **Tutorial 35**: Advanced AG-UI features (generative UI, HITL)

## 🤝 Contributing

Found an issue or have suggestions? Please open an issue in the [ADK Training Repository](https://github.com/raphaelmansuy/adk_training).

## 📄 License

This tutorial implementation is part of the ADK Training project.

---

**Built with ❤️ using Google ADK, Next.js 15, and CopilotKit**
