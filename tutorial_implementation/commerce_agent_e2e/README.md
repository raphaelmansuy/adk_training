# Commerce Agent E2E - End-to-End Implementation

**A production-ready multi-user commerce agent** demonstrating advanced Google ADK v1.17.0 capabilities including persistent session management, tool integration, multi-user isolation, and comprehensive testing.

## 🎯 What You'll Learn

This tutorial demonstrates:

- ✅ **Session Persistence**: SQLite database with ADK's DatabaseSessionService
- ✅ **Multi-User Support**: Complete data isolation between users
- ✅ **Tool Architecture**: Overcoming ADK limitations with sub-agent patterns
- ✅ **Custom Tools**: Database-backed preference management
- ✅ **Multi-Agent Coordination**: Root agent orchestrating 3 specialized sub-agents
- ✅ **Comprehensive Testing**: Unit, integration, and end-to-end test suites
- ✅ **Production Patterns**: Error handling, confirmation flows, state management

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Vertex AI Service Account (recommended) OR Google API Key
- SQLite3 (pre-installed on macOS/Linux)

### Authentication Setup

**⚠️ IMPORTANT:** This agent works best with **Vertex AI authentication**. Using Gemini API (GOOGLE_API_KEY) breaks the "site:decathlon.com.hk" search operator.

#### Option A: Vertex AI (Recommended)

```bash
# Navigate to tutorial
cd tutorial_implementation/commerce_agent_e2e

# Run Vertex AI setup script (handles environment variables)
make setup-vertex-ai

# Follow the prompts to configure service account
```

The script will:
1. ✅ Verify service account credentials at `./credentials/commerce-agent-key.json`
2. ✅ Unset any conflicting Gemini API keys
3. ✅ Set `GOOGLE_CLOUD_PROJECT` and `GOOGLE_APPLICATION_CREDENTIALS`
4. ✅ Test that credentials work correctly

#### Option B: Gemini API (Limited)

```bash
# Navigate to tutorial
cd tutorial_implementation/commerce_agent_e2e

# Set API key
export GOOGLE_API_KEY=your_key_here
# Get free key at: https://aistudio.google.com/app/apikey
```

**⚠️ Limitation:** The "site:decathlon.com.hk" search operator won't work with Gemini API.

### Setup (2 minutes)

```bash
# Install dependencies
make setup

# Run tests (optional)
make test

# Start development UI
make dev

# Open http://localhost:8000 in your browser
# Select "commerce_agent" from the dropdown
```

## 📁 Project Structure

```
commerce_agent_e2e/
├── commerce_agent/              # Main package
│   ├── __init__.py             # Package exports
│   ├── agent.py                # Agent definitions (root + 3 sub-agents)
│   ├── tools.py                # Custom preference & curation tools
│   ├── models.py               # Pydantic data models
│   ├── config.py               # Configuration constants
│   └── database.py             # SQLite persistence layer
│
├── tests/                      # Comprehensive test suite
│   ├── conftest.py             # Test fixtures and configuration
│   ├── test_tools.py           # Unit tests for tools
│   ├── test_integration.py     # Integration tests
│   └── test_e2e.py             # End-to-end user scenarios
│
├── pyproject.toml              # Python project metadata
├── requirements.txt            # Dependencies
├── Makefile                    # Common commands
├── .env.example                # Environment template
└── README.md                   # This file
```

## 🏗️ Agent Architecture

### Root Agent: CommerceCoordinator

Orchestrates three specialized sub-agents:

```
CommerceCoordinator (Root)
├── ProductSearchAgent (Google Search tool)
├── PreferenceManager (Custom preference tool)
└── StorytellerAgent (Pure LLM narratives)
```

### State Management

Three-tier state scope system:

| Scope | Prefix | Lifetime | Example |
|-------|--------|----------|---------|
| Session | none | Current chat | `current_query` |
| User | `user:` | Persisted | `user:preferences` |
| App | `app:` | Global | `app:product_cache` |
| Temp | `temp:` | Current turn | `temp:buffer` |

**Critical**: User-scoped data (`user:*`) is completely isolated by user_id in SQLite.

### Database Schema

```sql
user_preferences      -- User sports, price range, brands
interaction_history   -- Search queries and results tracking
user_favorites        -- Wishlist and saved products
product_cache         -- Search result caching (app-wide)
```

## 🧪 Testing

### Run All Tests

```bash
make test
```

### Test Tiers

**Tier 1: Unit Tests** (test_tools.py)
- Individual tool functions in isolation
- Database operations
- Error handling

**Tier 2: Integration Tests** (test_integration.py)
- Agent configuration
- Tool integration
- Database integration
- Import paths

**Tier 3: End-to-End Tests** (test_e2e.py)
- Complete user workflows
- Multi-user scenarios
- Session persistence
- Engagement tracking
- Error recovery

### Test Coverage

```bash
make test
# Generates: htmlcov/index.html
open htmlcov/index.html
```

## 📚 Key Features

### 1. Session Persistence

```python
from commerce_agent import root_agent
from google.adk.sessions import DatabaseSessionService

session_service = DatabaseSessionService(
    db_url="sqlite:///./sessions.db"
)

# Data survives app restarts
session = await session_service.get_session(
    "commerce_agent", "user123", "session456"
)
```

### 2. Multi-User Isolation

```python
# Alice's session
alice_prefs = await get_user_preferences("alice")
# Returns: {"sports": ["running"]}

# Bob's session
bob_prefs = await get_user_preferences("bob")
# Returns: {"sports": ["cycling"]}

# Complete isolation guaranteed
```

### 3. Custom Tools with Databases

```python
from commerce_agent import manage_user_preferences

result = manage_user_preferences(
    action="update",
    user_id="athlete_1",
    data={"sports": ["running", "cycling"]}
)
```

### 4. Tool Confirmation Flow

For expensive items (€100+), the agent requests confirmation before recommending.

### 5. Multi-Agent Coordination

Root agent delegates to specialists:
- Search agent handles Decathlon product discovery
- Preference agent manages user profiles
- Storyteller agent creates engaging narratives

## 🔧 Configuration

### Environment Variables

Create `.env` from `.env.example`:

```bash
cp .env.example .env
```

Edit `.env`:

```bash
# Authentication (choose one)
GOOGLE_API_KEY=your_key

# Database
DATABASE_URL=sqlite:///./commerce_agent_sessions.db

# Logging
ADK_LOG_LEVEL=INFO
```

### ADK Web Configuration

```bash
adk web --port 8000
```

Open http://localhost:8000

## 📖 Tutorial Documentation

Full tutorial guide: [docs/docs/35_commerce_agent_e2e.md](../../docs/docs/35_commerce_agent_e2e.md)

Covers:
- Complete architecture overview
- Database schema details
- Testing strategies
- Deployment scenarios
- Production checklist

## 🎓 Learning Path

1. **Start Here**: `make demo` - See what's possible
2. **Understand**: Read the [tutorial documentation](../../docs/docs/35_commerce_agent_e2e.md)
3. **Explore**: `make dev` - Interact with the agent
4. **Learn**: Review the [test files](tests/) to see patterns
5. **Extend**: Modify tools and agents in [commerce_agent/](commerce_agent/)
6. **Test**: `make test` - Verify changes

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Agent not in dropdown | Run `pip install -e .` in this directory |
| "database is locked" | Ensure only one process accesses db |
| No search results | Verify GOOGLE_API_KEY is set and valid |
| Tests fail | Run `make setup` first |
| SQLite errors | Delete `commerce_agent_sessions.db` and restart |

## � Authentication Troubleshooting

### "site:decathlon.com.hk" operator not working

**Problem:** Search returns results from other retailers (Amazon, eBay, Adidas)

**Cause:** Using Gemini API instead of Vertex AI

**Solution:**

```bash
# 1. Check which credentials are set
echo $GOOGLE_API_KEY
echo $GOOGLE_APPLICATION_CREDENTIALS

# 2. If both are set, unset the API key:
unset GOOGLE_API_KEY

# 3. Re-run the agent
make dev
```

### Both GOOGLE_API_KEY and GOOGLE_APPLICATION_CREDENTIALS set

**Problem:** Agent uses Gemini API instead of Vertex AI, breaking search

**Warning:** The Makefile will show this warning during `make dev`

**Solution:**

```bash
# Run the setup script to fix credentials
make setup-vertex-ai

# Or manually unset and re-run
unset GOOGLE_API_KEY
make dev
```

### Vertex AI credentials not loading

**Problem:** Error like "Could not authenticate with Google Cloud"

**Solution:**

```bash
# 1. Verify credentials file exists
ls -la ./credentials/commerce-agent-key.json

# 2. Verify environment variables
echo $GOOGLE_CLOUD_PROJECT
echo $GOOGLE_APPLICATION_CREDENTIALS

# 3. Test with gcloud CLI
gcloud auth list

# 4. If gcloud shows wrong account, switch:
gcloud config set project $GOOGLE_CLOUD_PROJECT
gcloud auth application-default login

# 5. Re-run setup
make setup-vertex-ai
```

## �📈 Deployment

### Local Development

```bash
make dev
# Persists to local SQLite
```

### Production (Cloud Run)

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa-key.json
adk deploy cloud_run \
  --session-db "sqlite:///./sessions.db" \
  --name commerce-agent
```

### Enterprise Scale (Agent Engine)

Switch to Cloud Spanner for multi-region deployment:

```python
session_service = DatabaseSessionService(
    db_url="spanner://projects/MY_PROJECT/instances/MY_INSTANCE/databases/commerce"
)
```

## 📚 References

- [Official ADK Documentation](https://google.github.io/adk-docs/)
- [Session Management](https://google.github.io/adk-docs/sessions/)
- [Tool Integration](https://google.github.io/adk-docs/tools/)
- [Multi-Agent Systems](https://google.github.io/adk-docs/agents/multi-agents/)
- [Testing Guide](https://google.github.io/adk-docs/get-started/testing/)

## 📝 License

MIT License - See LICENSE file

## 💬 Questions?

Check the [ADK Community](https://reddit.com/r/agentdevelopmentkit/) or [GitHub Discussions](https://github.com/google/adk-python/discussions)

---

**Next Steps**:
- [ ] Run `make setup`
- [ ] Run `make test`
- [ ] Run `make dev`
- [ ] Try demo scenarios with `make demo`
- [ ] Read the full [tutorial guide](../../docs/docs/35_commerce_agent_e2e.md)
- [ ] Modify tools in `commerce_agent/tools.py`
- [ ] Add new sub-agents to the root agent
