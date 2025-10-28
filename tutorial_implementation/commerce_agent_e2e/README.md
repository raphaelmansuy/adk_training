# Commerce Agent E2E - End-to-End Implementation

**A production-ready multi-user commerce agent** demonstrating advanced Google ADK v1.17.0 capabilities including:
- ✅ Persistent session management with SQLite
- ✅ **Grounding metadata extraction** for source attribution
- ✅ Multi-user isolation with complete data security
- ✅ Tool integration patterns overcoming ADK limitations
- ✅ Custom tools with database backing
- ✅ Multi-agent coordination
- ✅ Comprehensive testing suite

## 🎯 What You'll Learn

This tutorial demonstrates:

- ✅ **Session Persistence**: SQLite database with ADK's DatabaseSessionService
- ✅ **Grounding Metadata**: Extract and display source attribution from Google Search
- ✅ **Citation Management**: Track which sources support which product claims
- ✅ **URL Verification**: Prevent hallucination by using only real search result URLs
- ✅ **Multi-User Support**: Complete data isolation between users
- ✅ **Tool Architecture**: Overcoming ADK limitations with sub-agent patterns
- ✅ **Custom Tools**: Database-backed preference management and citation validation
- ✅ **Multi-Agent Coordination**: Root agent orchestrating 3 specialized sub-agents
- ✅ **Comprehensive Testing**: Unit, integration, and end-to-end test suites
- ✅ **Production Patterns**: Error handling, confirmation flows, state management
- ✅ **Type Safety**: TypedDict definitions for all tool interfaces
- ✅ **Observability**: GroundingMetadataCallback for source attribution tracking

### 🌟 Grounding Metadata Features

**NEW: Source Attribution & Citations**

The commerce agent now extracts and preserves grounding metadata from Google Search results:

| Feature | Benefit |
|---------|---------|
| **Source Chunks** | Exact URLs and titles from search results |
| **Segment Attribution** | Know which sources support which claims |
| **Confidence Scores** | Multiple sources = higher confidence |
| **URL Verification** | All URLs validated against search results |
| **Citation Validation** | Tool to detect URL hallucination |
| **Quality Scoring** | Overall grounding quality metrics |

**Customer Experience Impact**:
- 🎯 **Trust**: Every product fact is traceable to authoritative sources
- 🔗 **Verification**: Users can click to verify information independently  
- 💯 **Accuracy**: Multiple sources reduce hallucination risk
- 🏪 **Transparency**: Know exactly which retailer each link is from

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Vertex AI Service Account (recommended) OR Google API Key
- SQLite3 (pre-installed on macOS/Linux)

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Vertex AI Service Account (recommended) OR Google API Key
- SQLite3 (pre-installed on macOS/Linux)

### Two Ways to Run

**Option 1: ADK Web Interface** (Default - uses ADK state)
```bash
make dev  # Visit http://localhost:8000
```

**Option 2: SQLite Persistent Sessions** (Advanced - survives restarts)
```bash
python runner_with_sqlite.py
```

See **[Session Persistence Options](#-session-persistence-options)** below for comparison.

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

## � Session Persistence Options

Choose the right persistence strategy for your use case:

### Option 1: ADK State (Default - Simple)

**What is it?**
ADK's built-in state management with `user:` prefix for cross-session persistence.

**How it works:**
```python
# Tools modify state
def save_preferences(sport: str, tool_context: ToolContext):
    tool_context.state["user:sport"] = sport  # Persisted automatically
    return {"status": "success"}

# State persists across invocations
def get_preferences(tool_context: ToolContext):
    return {"data": tool_context.state.get("user:sport")}
```

**Best for:**
- ✅ Simple user preferences (sport, budget, experience level)
- ✅ Quick prototyping and development
- ✅ Single-server deployments
- ✅ Key-value data patterns

**Current Implementation:** This is what the commerce agent uses today.

### Option 2: DatabaseSessionService with SQLite (Advanced)

**What is it?**
ADK's built-in SQL persistence for sessions, state, and conversation history.

**How it works:**
```python
from google.adk.sessions import DatabaseSessionService

# One-time setup
session_service = DatabaseSessionService(
    db_url="sqlite:///./sessions.db?mode=wal"
)

runner = Runner(
    agent=root_agent,
    session_service=session_service
)

# Everything persists: state, events, timestamps
session = await session_service.get_session("app", "user", "session_id")
# Data survives app restarts! ✅
```

**Using with adk web (OFFICIAL SUPPORT):**
```bash
# SQLite persistence (sessions survive restarts)
adk web --session_service_uri sqlite:///./sessions.db

# With WAL mode (recommended)
adk web --session_service_uri "sqlite:///./sessions.db?mode=wal"

# PostgreSQL (production)
adk web --session_service_uri postgresql://user:pass@localhost/adk_sessions
```

**Reference:** [ADK CLI Documentation](https://google.github.io/adk-docs/api-reference/cli/cli.html#web)

**Best for:**
- ✅ Multi-user applications with isolation requirements
- ✅ Conversation history preservation
- ✅ Complex queries (SQL JOINs, filters)
- ✅ Production deployments

**Try it now:**
```bash
# Run the SQLite demo
python runner_with_sqlite.py

# See comprehensive guide
cat docs/SQLITE_SESSION_PERSISTENCE_GUIDE.md
```

### Comparison Table

| Feature | ADK State (`user:` prefix) | DatabaseSessionService (SQLite) |
|---------|----------------------------|----------------------------------|
| **Setup** | ✅ Zero config | ⚠️ Database URL required |
| **Persistence** | ✅ Cross-session | ✅ Cross-restart |
| **Conversation History** | ❌ Not stored | ✅ Full event log |
| **Multi-User Isolation** | ✅ Good (via state keys) | ✅ Excellent (via DB rows) |
| **Queries** | ❌ Key-value only | ✅ SQL queries, JOINs |
| **Scalability** | ✅ Good for simple data | ✅ Better for complex data |
| **Production Databases** | ❌ In-memory/temp storage | ✅ PostgreSQL/MySQL/Spanner |
| **Current Commerce Agent** | ✅ **Using this** | ⏳ Available as option |

### When to Switch?

**Keep ADK State if:**
- You have simple user preferences (sport, budget, experience)
- You're prototyping or in development
- You don't need conversation history

**Switch to DatabaseSessionService if:**
- You need conversation history across restarts
- You have complex multi-user requirements
- You want SQL query capabilities
- You're deploying to production at scale

**Documentation:**
- **SQLite Guide**: `docs/SQLITE_SESSION_PERSISTENCE_GUIDE.md` (comprehensive)
- **Working Example**: `runner_with_sqlite.py` (ready to run)
- **ADK Docs**: https://google.github.io/adk-docs/sessions/

## �📁 Project Structure

```
commerce_agent_e2e/
├── commerce_agent/              # Main package
│   ├── __init__.py             # Package exports
│   ├── agent.py                # Basic agent (root + 3 sub-agents)
│   ├── agent_enhanced.py       # Enhanced multi-agent coordinator
│   ├── tools.py                # Custom preference & curation tools
│   ├── models.py               # Pydantic data models
│   ├── types.py                # Enhanced type definitions
│   ├── config.py               # Configuration constants
│   ├── database.py             # SQLite persistence layer
│   ├── callbacks.py            # Agent lifecycle callbacks
│   ├── grounding_metadata.py   # Source attribution handling
│   ├── search_agent.py         # Product search specialist
│   ├── search_product.py       # Search tool implementation
│   ├── preferences_agent.py    # User preference manager
│   ├── sub_agents/             # Enhanced specialized sub-agents
│   │   ├── preference_collector.py
│   │   ├── product_advisor.py
│   │   ├── visual_assistant.py
│   │   └── checkout_assistant.py
│   └── tools/                  # Enhanced tool modules
│       ├── cart_tools.py
│       └── multimodal_tools.py
│
├── tests/                      # Comprehensive test suite
│   ├── conftest.py             # Test fixtures and configuration
│   ├── test_tools.py           # Unit tests for tools
│   ├── test_integration.py     # Integration tests
│   ├── test_e2e.py             # End-to-end user scenarios
│   └── test_agent_instructions.py # Agent instruction tests
│
├── eval/                       # Evaluation framework
│   ├── eval_data/              # Test scenarios and datasets
│   └── test_eval.py            # Evaluation tests
│
├── scripts/                    # Setup and utility scripts
│   └── setup-vertex-ai.sh      # Vertex AI authentication setup
│
├── credentials/                # Service account keys (gitignored)
├── pyproject.toml              # Python project metadata
├── requirements.txt            # Dependencies
├── Makefile                    # Common commands
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
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

### Testing with Specific User Identities

**⚠️ Important: The ADK web UI does NOT have a panel for setting User IDs**

The `adk web` browser interface uses a fixed default user ID ("user") for all sessions. To test with specific user identities (alice, bob, etc.), you **must use the API endpoints directly**.

**Complete Guide**: See [docs/TESTING_WITH_USER_IDENTITIES.md](docs/TESTING_WITH_USER_IDENTITIES.md) for:
- � **API testing with curl** (the ONLY way to set custom User IDs)
- 🐍 **Python scripts** for automated multi-user testing
- 👥 **Multi-user isolation testing** (Alice vs Bob scenario)
- 💾 **SQLite persistence verification** across restarts
- 🎯 **Common test scenarios** (onboarding, returning customer, multi-user household)
- 🐛 **Debugging tips** for preference issues

**Quick view guide**:
```bash
make test-guide   # View API testing instructions in terminal
```

**Quick API Example**:
```bash
# Create session for alice
curl -X POST http://localhost:8000/apps/commerce_agent/users/alice/sessions/s1 \
  -H "Content-Type: application/json" -d '{"state": {}}'

# Send message as alice
curl -X POST http://localhost:8000/run -H "Content-Type: application/json" -d '{
  "app_name": "commerce_agent", "user_id": "alice", "session_id": "s1",
  "new_message": {"role": "user", "parts": [{"text": "I want running shoes"}]}
}'
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

### 4. Grounding Metadata Callback (NEW)

Extract source attribution from Google Search results:

```python
from commerce_agent import root_agent, create_grounding_callback
from google.adk.runners import Runner

runner = Runner(
    agent=root_agent,
    after_model_callbacks=[create_grounding_callback(verbose=True)]
)

async for event in runner.run_async(...):
    if event.is_final_response():
        # Access extracted sources from callback_context.state
        # (Note: callback stores in state during after_model phase)
        print("Response with grounded sources generated")
```

**Benefits**:
- ✅ Console logs show source attribution during development
- ✅ Monitor grounding quality in real-time
- ✅ Verify URLs are from real search results
- ✅ Debug which sources support which claims

**Note**: For `adk web` usage, the callback runs automatically but output appears in server logs, not the web UI.

**Documentation**: See `docs/GROUNDING_CALLBACK_GUIDE.md` for complete usage guide.

### 5. Type Safety with TypedDict (NEW)

All tool interfaces now use TypedDict for better IDE support:

```python
from commerce_agent.types import ToolResult, UserPreferences

def my_tool(param: str, tool_context: ToolContext) -> ToolResult:
    return {
        "status": "success",
        "report": "Operation completed",
        "data": {"result": "value"}
    }
```

**Benefits**:
- ✅ Full IDE autocomplete
- ✅ Type checking with mypy
- ✅ Clear API contracts
- ✅ Reduced runtime errors

### 6. Tool Confirmation Flow

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
