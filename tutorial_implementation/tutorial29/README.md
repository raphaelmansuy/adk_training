# Tutorial 29: Introduction to UI Integration - Quick Start

A minimal implementation demonstrating ADK agent integration with React UI using the AG-UI Protocol. This is the Quick Start example from Tutorial 29.

## 🚀 Quick Start

```bash
# 1. Install dependencies
make setup

# 2. Configure API key
cp agent/.env.example agent/.env
# Edit agent/.env and add your GOOGLE_API_KEY

# 3. Start both backend and frontend
make dev

# 4. Open http://localhost:5173 in your browser
```

## 📋 What's Included

This minimal implementation demonstrates:

- ✅ **Python ADK Agent** - Simple conversational assistant
- ✅ **FastAPI backend** with AG-UI integration
- ✅ **React + Vite frontend** with CopilotKit
- ✅ **Real-time chat interface** with streaming
- ✅ **Comprehensive test suite** (15+ tests)
- ✅ **Quick setup** (< 10 minutes)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  USER'S BROWSER                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  React + Vite App (Port 5173)                        │  │
│  │  ├─ App.tsx (Chat UI)                                │  │
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
│  │  ├─ tools: (none - simple assistant)                 │  │
│  │  └─ instruction: Helpful AI assistant                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                        │
                        │ Gemini API
                        │
┌───────────────────────▼─────────────────────────────────────┐
│  GEMINI 2.0 FLASH                                            │
│  ├─ Text generation                                          │
│  └─ Streaming responses                                      │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
tutorial29/
├── agent/                      # Python backend
│   ├── __init__.py
│   ├── agent.py               # ADK agent + FastAPI app
│   └── .env.example           # Environment template
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── App.tsx            # Main app with CopilotKit
│   │   ├── App.css            # Styles
│   │   └── main.tsx           # Entry point
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── index.html
├── tests/                     # Test suite
│   ├── test_imports.py        # Import tests
│   ├── test_structure.py      # Structure tests
│   └── test_agent.py          # Agent tests
├── Makefile                   # Build commands
├── requirements.txt           # Python dependencies
├── pyproject.toml            # Python project config
└── README.md                  # This file
```

## 🎯 What You'll Learn

This implementation demonstrates the core concepts from Tutorial 29:

1. **AG-UI Protocol Integration** - How to connect ADK agents to React UIs
2. **Minimal Setup** - The simplest possible working example
3. **Backend Architecture** - FastAPI + ag_ui_adk pattern
4. **Frontend Architecture** - React + CopilotKit pattern
5. **Development Workflow** - From setup to running application

## 💬 Try These Prompts

Once the app is running, try:

- "What is Google ADK?"
- "How does the AG-UI Protocol work?"
- "Explain the benefits of UI integration"
- "What can you help me with?"
- "Tell me about different UI integration approaches"

## 🧪 Testing

```bash
# Run all tests
make test

# Tests verify:
# - All imports work correctly
# - Project structure is correct
# - Agent is properly configured
# - FastAPI app is set up correctly
# - AG-UI integration is working
```

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check if API key is set
echo $GOOGLE_API_KEY

# If not set, configure it
cp agent/.env.example agent/.env
# Edit agent/.env with your API key
export GOOGLE_API_KEY=your_key_here
```

### Frontend can't connect to backend

1. Verify backend is running on port 8000
2. Check CORS is enabled in `agent/agent.py`
3. Verify `runtimeUrl` in frontend matches backend URL

### "ag_ui_adk not found" error

```bash
# Install AG-UI ADK package
pip install ag-ui-adk
```

### Tests failing

```bash
# Make sure you're in tutorial29 directory
cd tutorial_implementation/tutorial29

# Run setup first
make setup

# Then run tests
make test
```

## 📚 Learn More

This is a minimal Quick Start example. For more advanced features, see:

- **Tutorial 30**: Next.js + ADK with tools and advanced features
- **Tutorial 31**: React Vite + ADK with more complex examples
- **Tutorial 32**: Streamlit direct integration
- **Tutorial 33**: Slack bot integration

## 🔑 Key Differences from Tutorial 30

Tutorial 29 (this):
- Minimal example for learning
- No custom tools (just conversation)
- Vite + React (simpler)
- Focus on the integration pattern

Tutorial 30:
- Production-ready example
- Multiple custom tools
- Next.js 15 (more features)
- Advanced features (Generative UI, HITL, Shared State)

## 🎉 What's Next?

Now that you understand the basics:

1. ✅ You've seen how AG-UI Protocol works
2. ✅ You understand the backend/frontend architecture
3. ✅ You can set up and run the integration

**Next Steps**:
- Add custom tools to the agent (see Tutorial 30)
- Deploy to production (Cloud Run + Vercel)
- Implement advanced features (Generative UI, HITL)
- Try other integration approaches (Streamlit, Slack)

## 📝 Notes

- This is based on the Quick Start section from Tutorial 29
- Uses the exact same pattern as the tutorial documentation
- All code uses correct ADK v1.16+ Runner API pattern
- Verified to work with latest ADK and CopilotKit versions

---

**Questions or feedback?** Open an issue on the [ADK Training Repository](https://github.com/raphaelmansuy/adk-training).
