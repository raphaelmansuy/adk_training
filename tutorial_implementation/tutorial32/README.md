# 📊 Data Analysis Agent: Streamlit + ADK

Chat with AI about your CSV data. Pure Python, no backend needed. Upload a file, ask questions, get instant insights and beautiful charts.

**What you get**:
- 💬 Natural language data exploration
- � Automatic chart generation
- ⚡ Real-time streaming responses
- 🚀 Deploy in minutes
- � Secure (API keys in `.env` only)

## � Get Started in 2 Minutes

### Prerequisites
- Python 3.9+
- Google API key (free) from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Setup
```bash
cd tutorial_implementation/tutorial32
make setup              # Install dependencies
cp .env.example .env    # Create config
# Add your API key to .env
make dev                # Start app at localhost:8501
```

**That's it!** Open the browser and start analyzing. 📊

## 💡 How It Works

### 1. Upload your data
```
┌─ Sidebar ────────────────────┐
│ 📁 Upload CSV                │
│                              │
│ [Choose file...]             │
│                              │
│ ✅ Loaded: sales.csv         │
│    📊 500 rows × 8 columns   │
└──────────────────────────────┘
```

### 2. Chat with your data
```
You:  "Show me sales by region"
      ↓
🤖 AI analyzes context with data
      ↓
Bot:  "Based on your data...
       
       📊 Chart: Sales by Region
       
       Top regions: West ($50k), 
       North ($45k), South ($38k)"
```

### 3. Two modes available

**Code Execution Mode** (recommended for charts)
- Automatic visualizations with matplotlib/plotly
- AI generates and executes Python code
- Professional charts appear inline

**Chat Mode** (for analysis)
- Direct AI responses
- Perfect for questions and insights
- Faster feedback

## 🎯 Try It Now

**Sample CSV** to test:
```csv
date,product,sales,region
2024-01-01,Widget A,1200,North
2024-01-01,Widget B,980,West
2024-01-02,Widget A,1450,South
```

**Example Questions**:
- "What are the top products by sales?"
- "Create a chart of sales over time"
- "Compare regions - which is growing fastest?"
- "Any trends or patterns you notice?"

## 📁 Project Layout

```
tutorial32/
├── app.py                    Main Streamlit app
├── data_analysis_agent/      AI agent code
│   ├── __init__.py
│   └── agent.py
├── tests/                    Tests
├── Makefile                  Quick commands
├── requirements.txt          Dependencies
├── pyproject.toml           Python config
├── .env.example             API key template
└── README.md                This file
```

**Key files**:
- `app.py` - User interface and chat logic
- `data_analysis_agent/agent.py` - AI agent configuration
- `Makefile` - Run `make help` to see all commands

## ⚙️ Commands

```bash
make setup       # Install dependencies
make dev         # Start app (localhost:8501)
make demo        # Show usage examples
make test        # Run tests
make clean       # Clean cache
make help        # Show all commands
```

## 🧪 Testing

Tests verify agent setup and tools work correctly:

```bash
make test                  # Run all tests
pytest tests/ -v           # Detailed output
pytest tests/ --cov        # Coverage report
```

Tests cover:
- Agent configuration ✓
- Tool functionality ✓
- Import system ✓
- Project structure ✓

## 🔧 Configuration

### Streamlit Settings

Customize in `app.py`:

```python
st.set_page_config(
    page_title="Data Analysis Assistant",
    page_icon="📊",
    layout="wide",
)
```

### Agent Configuration

Modify in `data_analysis_agent/agent.py`:

```python
root_agent = Agent(
    name="data_analysis_agent",
    model="gemini-2.0-flash",
    description="...",
    instruction="...",
    tools=[...],
)
```

## 📚 Key Components

### 1. Streamlit App (`app.py`)

- User interface with chat and file upload
- Session state management
- Real-time response streaming
- Data preview and statistics display

### 2. ADK Agent (`data_analysis_agent/agent.py`)

- **root_agent**: Main agent exported for ADK discovery
- **Tools**:
  - `analyze_column`: Statistical analysis
  - `calculate_correlation`: Find relationships
  - `filter_data`: Subset exploration
  - `get_dataset_summary`: Overview information

### 3. Tools

Each tool returns consistent format:

```python
{
    "status": "success" | "error",
    "report": "Human-readable message",
    "data": {...},  # Specific to tool
}
```

## 🏛️ How It's Built

```
Your Browser
     ↓
  Streamlit App (localhost:8501)
     │
     ├─ File Upload → Load CSV with pandas
     ├─ Chat UI → Display messages
     └─ Agent Call → Direct in-process execution
                     (no HTTP server!)
     ↓
  Google Gemini API
     └─ Analyze data, generate code
```

**Two execution paths**:

1. **Code Execution Mode** (Smart)
   - You ask for a chart
   - AI generates Python code
   - Code runs, matplotlib/plotly creates image
   - Chart displays in chat

2. **Chat Mode** (Fast)
   - You ask a question
   - AI responds directly
   - No code execution, just insights

**Architecture benefits**:
- Pure Python (no JavaScript needed)
- Direct in-process execution (fast!)
- Single service to deploy
- Perfect for data tools

## 🚀 Share Your App

### Streamlit Cloud (Easiest)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" → select repo → `app.py`
4. Add secret: `GOOGLE_API_KEY = your_key`
5. Done! Your app is live 🎉

### Google Cloud Run

```bash
# Deploy (takes 1-2 minutes)
gcloud run deploy data-analysis-agent \
  --source=. \
  --allow-unauthenticated

# View logs
gcloud run logs read data-analysis-agent
```

## 🐛 Issues?

### Please set GOOGLE_API_KEY

```bash
cp .env.example .env
# Edit .env and add your key
```

### App won't start

```bash
make clean
make setup
streamlit run app.py --logger.level=debug
```

### Tests fail

```bash
pytest tests/ -vv
```

## � Learn More

**Understand the code**:
1. Read `app.py` - how Streamlit UI works
2. Check `data_analysis_agent/agent.py` - AI configuration
3. Run tests - verify everything works

**Customize it**:
- Change agent instructions for different analysis styles
- Add more tools (statistical tests, ML predictions)
- Modify charts and visualizations
- Add user authentication

**Related tutorials**:
- Tutorial 30: Web apps with Next.js + CopilotKit
- Tutorial 31: Lightweight UI with React + Vite
- Tutorial 33: Slack bot integration
- Tutorial 34: Event-driven agents with Pub/Sub

## � Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Google ADK](https://google.github.io/adk-docs/)
- [Gemini API](https://ai.google.dev/)
- [Pandas Guide](https://pandas.pydata.org/docs/)

---

**Questions?** Open an issue on [GitHub](https://github.com/raphaelmansuy/adk_training)

**Ready to build?** Start with `make dev` 🚀
