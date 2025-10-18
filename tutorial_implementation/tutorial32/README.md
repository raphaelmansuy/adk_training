# Data Analysis Agent with Streamlit + ADK

A production-ready Streamlit application that integrates Google ADK agents for intelligent data analysis. Upload any CSV file and chat with an AI assistant to explore your data, discover insights, and perform analyses.

## 🌟 Features

- **📊 Interactive Chat Interface**: Ask questions about your data in natural language
- **🔄 Direct ADK Integration**: No HTTP overhead - agent runs in-process with Streamlit
- **📁 CSV Upload**: Load and analyze any CSV file
- **🧠 Gemini 2.0 Flash**: State-of-the-art language model for analysis
- **📈 Dynamic Visualizations**: Python code execution for matplotlib/plotly charts
- **✨ Proactive Analysis**: Agent suggests analyses and visualizations automatically
- **⚡ Real-time Streaming**: Stream responses and visualization generation as they happen
- **🎯 Smart Routing**: Automatic selection between analysis tools and code execution
- **⏳ Better UX**: Loading indicators and status messages while processing
- **🔒 Secure**: Never commits secrets, uses environment variables

## 📋 Prerequisites

- **Python 3.9+**
- **Google AI API Key** from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **pip** (Python package manager)

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Clone and navigate to this directory
cd tutorial_implementation/tutorial32

# Install dependencies and package
make setup
```

### 2. Configure API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Google API key
# GOOGLE_API_KEY=your_api_key_here
```

**Get your API key:**

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Get API key"
3. Copy the key into your `.env` file

### 3. Run the App

```bash
make dev
```

The app opens at `http://localhost:8501` 🎉

## 💡 Usage

### Basic Workflow

1. **Upload CSV**: Use the sidebar to upload your data
2. **Review Data**: See columns, types, and statistics
3. **Choose Mode**:
   - **Smart Mode** (recommended): Uses ADK Code Execution for visualizations
   - **Chat Mode**: Uses direct Gemini API for text analysis
4. **Ask Questions**: Chat with the AI about your data
5. **Get Insights**: Receive analysis, visualizations, and recommendations

### Code Execution Mode (NEW!)

Enable "Use Code Execution for Visualizations" in the sidebar to unlock advanced features:

✨ **Proactive Agent**: The AI automatically suggests analyses and visualizations
📊 **Dynamic Charts**: matplotlib and plotly charts generated via Python code execution
⚡ **Real-time Display**: Charts appear as they're generated with loading indicators
🎯 **Smart Routing**: Agent intelligently chooses between tools and code execution

**Example requests that trigger visualizations:**

```
"Show me a pie chart of categories"
"Create a line plot of trends over time"
"Visualize the distribution of values"
"Compare these metrics with scatter plots"
"Generate a comprehensive dashboard"
```

### Sample Data

Create a simple CSV to test:

```csv
name,age,salary,department
Alice,30,75000,Engineering
Bob,28,68000,Engineering
Carol,35,82000,Sales
David,32,70000,Marketing
```

Save as `sample.csv` and upload it!

## 🏗️ Project Structure

```
tutorial32/
├── app.py                      # Main Streamlit application
├── data_analysis_agent/        # ADK agent module
│   ├── __init__.py            # Package initialization
│   └── agent.py               # Agent definition and tools
├── tests/                      # Comprehensive test suite
│   ├── test_agent.py          # Agent and tool tests
│   ├── test_imports.py        # Import validation tests
│   └── test_structure.py      # Project structure tests
├── pyproject.toml             # Modern Python packaging
├── requirements.txt           # Python dependencies
├── .env.example               # Environment template
├── Makefile                   # Development commands
└── README.md                  # This file
```

## 🛠️ Development Commands

All commands use the Makefile for consistency:

### Setup & Installation

```bash
# Install dependencies and package for development
make setup
```

### Running

```bash
# Start the Streamlit app (localhost:8501)
make dev

# Show demo with usage examples
make demo
```

### Testing

```bash
# Run all tests with coverage
make test

# Check code quality
make lint

# Format code with black and isort
make format
```

### Cleanup

```bash
# Remove cache and generated files
make clean
```

### Help

```bash
# Show all available commands
make help
```

## 🧪 Testing

The project includes comprehensive tests covering:

- **Agent Configuration** (`test_agent.py`): Agent setup, tools, return formats
- **Tool Functions** (`test_agent.py`): Each tool's behavior and error handling
- **Import System** (`test_imports.py`): Module imports and accessibility
- **Project Structure** (`test_structure.py`): Required files and configuration

### Run Tests

```bash
# Full test suite
make test

# Specific test file
pytest tests/test_agent.py -v

# With coverage
pytest tests/ --cov=data_analysis_agent
```

### Test Coverage

The test suite covers:

- ✅ Agent initialization and configuration
- ✅ Tool function behavior and error handling
- ✅ Return format consistency
- ✅ Module imports and accessibility
- ✅ Project file structure
- ✅ Environment configuration
- ✅ Code quality aspects

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

## 🏛️ Architecture

### Dual-Runner Pattern for Data Passing

Tutorial 32 implements a sophisticated multi-runner architecture to solve the context-passing problem:

**The Challenge**: Multi-agent coordination through AgentTool delegation loses context data (like CSV data).

**The Solution**: Direct runner for visualization agents that bypasses multi-agent routing.

### Key Components

1. **viz_runner**: Direct visualization_agent without routing

   - Receives full CSV data in context
   - Executes Python code via BuiltInCodeExecutor
   - Returns matplotlib/plotly charts as inline_data
   - Independent session service

2. **runner**: Multi-agent root_agent with tool delegation
   - Routes to analysis_agent for statistics
   - Routes to visualization_agent via AgentTool for simple viz
   - Good for text-based analysis

### Data Flow for Visualizations

1. User requests visualization
2. App prepares context_message with CSV data
3. viz_runner sends directly to visualization_agent
4. visualization_agent loads: df = pd.read_csv(StringIO(csv_data))
5. Agent generates Python code with matplotlib/plotly
6. BuiltInCodeExecutor runs code and generates PNG
7. Chart returned as Part.inline_data
8. app.py extracts inline_data and displays with st.image()
9. User sees visualization in Streamlit UI

## 🚀 Deployment

### Streamlit Cloud (Easiest)

1. **Create `secrets.toml`**:

   ```toml
   GOOGLE_API_KEY = "your_production_key"
   ```

2. **Push to GitHub**:

   ```bash
   git push origin main
   ```

3. **Deploy on Streamlit**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select repository
   - Set main file: `app.py`
   - Add secret in settings
   - Click "Deploy"

### Google Cloud Run

```bash
# Build and deploy
gcloud run deploy data-analysis-agent \
  --source=. \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated \
  --port=8501

# Output: https://data-analysis-agent-xyz.run.app
```

## 🔐 Security Best Practices

✅ **What we do:**

- Use `.env.example` as template (never commit real keys)
- Load secrets from environment variables
- Use `python-dotenv` for local development
- Validate all inputs

❌ **What we don't do:**

- Commit `.env` files
- Hardcode API keys
- Log sensitive information
- Trust user input directly

## 🐛 Troubleshooting

### "Please set GOOGLE_API_KEY"

**Solution**:

```bash
# Create .env from template
cp .env.example .env

# Edit and add your key
nano .env  # or your favorite editor

# Verify it loads
source .env
echo $GOOGLE_API_KEY
```

### App won't start

**Check dependencies**:

```bash
# Reinstall everything
make clean
make setup

# Run with verbose output
streamlit run app.py --logger.level=debug
```

### Tests fail

**Run with verbose output**:

```bash
pytest tests/ -vv --tb=long

# Run specific test
pytest tests/test_agent.py::TestAgentTools::test_analyze_column_tool -vv
```

### Slow responses

**Streamlit caching**:

```python
@st.cache_data
def process_data(df):
    return df.describe()

# Will cache results for repeated calls
```

## 📖 Learning Path

1. **Quick Start** (10 min): Upload CSV, ask questions
2. **Architecture** (20 min): Read `app.py` and understand flow
3. **Agent Tools** (15 min): Study `data_analysis_agent/agent.py`
4. **Testing** (10 min): Run and understand tests
5. **Customization** (30+ min): Modify and extend

## 🎯 Next Steps

### Extend the App

1. **Add more tools**:

   - Visualization generation
   - Statistical tests
   - Machine learning predictions

2. **Enhance UI**:

   - Custom CSS styling
   - Export reports
   - Data validation

3. **Production features**:
   - User authentication
   - Data persistence
   - Rate limiting
   - Monitoring

### Related Tutorials

- **Tutorial 30**: Next.js + CopilotKit (web apps)
- **Tutorial 31**: React Vite + CopilotKit (lightweight)
- **Tutorial 33**: Slack bot integration
- **Tutorial 34**: Google Cloud Pub/Sub events

## 📚 Resources

- [Streamlit Docs](https://docs.streamlit.io)
- [Google ADK Docs](https://google.github.io/adk-docs/)
- [Google AI Studio](https://makersuite.google.com/app/apikey)
- [Gemini API](https://ai.google.dev/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

## 🤝 Contributing

Found an issue? Have an improvement?

1. Check existing issues
2. Create detailed bug reports
3. Suggest enhancements
4. Submit pull requests

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Google ADK Team
- Streamlit Community
- Pandas & NumPy creators
- Tutorial 32 Contributors

---

**🎉 Happy analyzing!**

For questions or feedback, open an issue on the [ADK Training Repository](https://github.com/raphaelmansuy/adk_training).
