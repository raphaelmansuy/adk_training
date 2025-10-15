# Tutorial 31: Data Analysis Dashboard with Vite + React + ADK

A modern, fast data analysis dashboard built with Vite, React, CopilotKit, and Google ADK. Upload CSV files and get instant insights through natural language conversations.

## Features

- 📊 **CSV Data Analysis**: Load and analyze CSV files with pandas
- 📈 **Interactive Charts**: Generate line, bar, and scatter plots with Chart.js
- 🤖 **AI-Powered**: Natural language queries powered by Gemini 2.0 Flash
- ⚡ **Lightning Fast**: Built with Vite for instant HMR and fast builds
- 🎨 **Modern UI**: Beautiful gradient design with CopilotKit integration

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Frontend (Vite + React)                                     │
│  http://localhost:5173                                       │
│  ├─ File upload interface                                    │
│  ├─ CopilotKit chat UI                                       │
│  └─ Chart.js visualizations                                  │
└───────────────────┬─────────────────────────────────────────┘
                    │ Vite Proxy → /api/copilotkit
┌───────────────────▼─────────────────────────────────────────┐
│  Backend (FastAPI + ADK)                                     │
│  http://localhost:8000                                       │
│  ├─ ADK Agent (gemini-2.0-flash-exp)                        │
│  │  └─ Invoked via InMemoryRunner                           │
│  ├─ pandas data analysis tools                              │
│  └─ Direct /api/copilotkit endpoint                         │
└─────────────────────────────────────────────────────────────┘
```

**Key Architectural Decision:**
This implementation uses a **Python-only solution** without `ag-ui-adk`. The FastAPI backend directly handles CopilotKit requests and invokes the ADK agent using `InMemoryRunner`. This is simpler than the Next.js approach (which uses API routes + CopilotRuntime + HttpAgent for protocol translation) and works perfectly with Vite.

## Quick Start

### 1. Install Dependencies

```bash
make setup
```

This will:
- Create Python virtual environment
- Install agent dependencies
- Install frontend npm packages
- Install package in editable mode

### 2. Configure Environment

```bash
cp agent/.env.example agent/.env
# Edit agent/.env and add your GOOGLE_API_KEY
```

Get your API key from: https://makersuite.google.com/app/apikey

### 3. Run Backend (Terminal 1)

```bash
make dev-agent
```

Backend will be available at http://localhost:8000

### 4. Run Frontend (Terminal 2)

```bash
make dev-frontend
```

Frontend will be available at http://localhost:5173

### 5. Open in Browser

Navigate to http://localhost:5173 and start analyzing data!

## Usage Examples

### Upload CSV Data

1. Click "📁 Upload CSV File" button
2. Select a CSV file from your computer
3. Wait for confirmation

### Example CSV

```csv
month,sales,expenses
Jan,10000,7000
Feb,12000,7500
Mar,11500,7200
Apr,13000,7800
```

### Sample Queries

**Data Summary:**
- "Summarize the data for me"
- "What are the key statistics?"
- "Show me missing values"

**Visualizations:**
- "Create a line chart of sales over time"
- "Show me a bar chart comparing expenses"
- "Make a scatter plot of sales vs expenses"

**Analysis:**
- "What correlations exist in the data?"
- "Analyze trends in sales"
- "What's the relationship between sales and expenses?"

## Tools Available

### 1. `load_csv_data(file_name, csv_content)`

Loads CSV data into memory for analysis.

**Returns:**
```python
{
    "status": "success",
    "file_name": "data.csv",
    "rows": 100,
    "columns": ["col1", "col2"],
    "preview": [...],
    "dtypes": {...}
}
```

### 2. `analyze_data(file_name, analysis_type, columns=None)`

Performs statistical analysis on loaded datasets.

**Analysis Types:**
- `"summary"`: Descriptive statistics, missing values, unique counts
- `"correlation"`: Correlation matrix for numeric columns
- `"trend"`: Time series trend analysis

**Returns:**
```python
{
    "status": "success",
    "analysis_type": "summary",
    "data": {...}
}
```

### 3. `create_chart(file_name, chart_type, x_column, y_column)`

Generates chart data for visualization.

**Chart Types:**
- `"line"`: Line chart for trends
- `"bar"`: Bar chart for comparisons
- `"scatter"`: Scatter plot for relationships

**Returns:**
```python
{
    "status": "success",
    "chart_type": "line",
    "data": {
        "labels": [...],
        "values": [...]
    },
    "options": {
        "x_label": "column",
        "y_label": "column",
        "title": "Chart Title"
    }
}
```

## Development

### Run Tests

```bash
make test
```

Runs pytest with coverage reporting.

### View Demo

```bash
make demo
```

Shows usage examples and sample prompts.

### Clean Up

```bash
make clean
```

Removes cache files, build artifacts, and node_modules.

## Project Structure

```
tutorial31/
├── agent/                  # Backend agent
│   ├── __init__.py
│   ├── agent.py           # Main agent with pandas tools
│   ├── requirements.txt
│   └── .env.example
├── frontend/              # Vite + React frontend
│   ├── src/
│   │   ├── App.tsx       # Main application
│   │   ├── components/
│   │   │   ├── ChartRenderer.tsx
│   │   │   └── DataTable.tsx
│   │   ├── App.css
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── tests/                 # Test suite
│   ├── test_agent.py
│   ├── test_imports.py
│   └── test_structure.py
├── Makefile              # Build and run commands
├── pyproject.toml        # Python package config
└── README.md
```

## Technologies

### Backend
- **Google ADK**: Agent framework
- **Gemini 2.0 Flash**: LLM model
- **FastAPI**: Web framework
- **ag_ui_adk**: AG-UI protocol integration
- **pandas**: Data analysis
- **uvicorn**: ASGI server

### Frontend
- **Vite**: Build tool
- **React 18**: UI framework
- **TypeScript**: Type safety
- **CopilotKit**: AI chat UI
- **Chart.js**: Charting library
- **react-chartjs-2**: React wrapper for Chart.js

## Troubleshooting

### 422 Unprocessable Entity Error

**Symptom**: Browser console shows `Failed to load resource: 422 (Unprocessable Entity)` for `/api/copilotkit`

**Cause**: Missing or incorrect `agent` prop in `CopilotKit` component

**Solution**:

```tsx
// ❌ WRONG - Missing agent prop
<CopilotKit runtimeUrl="/api/copilotkit">
  {/* ... */}
</CopilotKit>

// ✅ CORRECT - Must specify which agent to use
<CopilotKit runtimeUrl="/api/copilotkit" agent="data_analyst">
  {/* ... */}
</CopilotKit>
```

The `agent` prop must match the agent name in your backend (`agent/agent.py`):
```python
adk_agent = Agent(
    name="data_analyst",  # ← Must match frontend agent prop
    # ...
)
```

### 404 Error on `/api/copilotkit`

**Symptom**: Browser console shows `Failed to load resource: 404 (Not Found)` for `/api/copilotkit`

**Causes & Solutions**:

1. **Backend not running**
   ```bash
   # Check if backend is running
   curl http://localhost:8000/health
   
   # If not running, start it
   make dev-agent
   ```

2. **Proxy configuration mismatch**
   - Verify `vite.config.ts` forwards `/api` to `http://localhost:8000`
   - **Do NOT** use path rewriting that removes `/api` prefix
   - Backend endpoint is `/api/copilotkit`, not `/copilotkit`

3. **Port conflict**
   ```bash
   # Check if port 8000 is in use
   lsof -i :8000
   
   # Kill process if needed
   kill -9 <PID>
   ```

### CORS Errors

**Symptom**: Console shows CORS policy errors

**Solutions**:

1. **Development**: Update `agent/agent.py` CORS middleware
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "http://localhost:5173",  # Your Vite port
           "http://localhost:3000",
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Production**: Add production domain to `allow_origins`
   ```python
   allow_origins=[
       "https://your-app.netlify.app",
       "https://your-domain.com",
   ]
   ```

### Charts Not Rendering

**Symptom**: Charts don't display or show blank space

**Solutions**:

1. **Check Chart.js registration** in `ChartRenderer.tsx`:
   ```typescript
   ChartJS.register(
     CategoryScale,
     LinearScale,
     PointElement,
     LineElement,
     BarElement,
     Title,
     Tooltip,
     Legend
   );
   ```

2. **Verify data format**:
   - Labels must be strings
   - Values must be numbers
   - Check browser console for Chart.js warnings

3. **Check component rendering**:
   ```typescript
   // Data must have labels and values
   const chartData = {
     labels: ['Jan', 'Feb', 'Mar'],
     values: [100, 200, 150]
   };
   ```

### File Upload Issues

**Symptom**: CSV files not loading or showing errors

**Solutions**:

1. **Check file size**: Large files may timeout
   - Limit to < 10MB for best performance
   - Use `pandas.read_csv()` chunking for larger files

2. **Check CSV format**:
   - Must have header row
   - Use standard delimiters (`,` or `;`)
   - Avoid special characters in column names

3. **Check encoding**:
   ```python
   # In load_csv_data function
   df = pd.read_csv(io.StringIO(csv_content), encoding='utf-8')
   ```

### Agent Not Responding

**Symptom**: Chat messages sent but no response

**Solutions**:

1. **Check API key**:
   ```bash
   # Verify GOOGLE_API_KEY is set
   cd agent
   source venv/bin/activate
   python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('API Key:', os.getenv('GOOGLE_API_KEY')[:10] + '...')"
   ```

2. **Check backend logs**:
   - Look for errors in terminal running `make dev-agent`
   - Check for rate limiting or quota errors

3. **Test agent directly**:
   ```bash
   # Test health endpoint
   curl http://localhost:8000/health
   
   # Test datasets endpoint
   curl http://localhost:8000/datasets
   ```

### Vite Build Errors

**Symptom**: `npm run build` or `make setup-frontend` fails

**Solutions**:

1. **Clear node_modules**:
   ```bash
   cd frontend
   rm -rf node_modules package-lock.json
   npm install
   ```

2. **Check Node version**:
   ```bash
   node --version  # Should be >= 18.x
   npm --version   # Should be >= 9.x
   ```

3. **Fix TypeScript errors**:
   - Run `npm run build` to see specific errors
   - Check `tsconfig.json` for correct settings

### Common Mistakes

1. **Forgetting to activate venv**:
   ```bash
   # Always activate before running agent
   cd agent
   source venv/bin/activate
   python agent.py
   ```

2. **Wrong working directory**:
   ```bash
   # Commands should be run from tutorial31 root
   cd /path/to/tutorial_implementation/tutorial31
   make dev-agent
   ```

3. **Missing environment variables**:
   ```bash
   # Copy example and add your key
   cp agent/.env.example agent/.env
   # Edit agent/.env and add GOOGLE_API_KEY
   ```

### Getting Help

If you're still stuck:

1. Check the [full tutorial documentation](../../docs/tutorial/31_react_vite_adk_integration.md)
2. Review working examples in [tutorial30](../tutorial30)
3. Enable debug logging in `agent/agent.py`:
   ```python
   uvicorn.run("agent:app", host="0.0.0.0", port=8000, log_level="debug")
   ```

## Deployment

### Backend (Cloud Run)

```bash
cd agent
gcloud run deploy data-analysis-agent \
  --source=. \
  --region=us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_API_KEY=your_key"
```

### Frontend (Netlify)

```bash
cd frontend
npm run build
netlify deploy --prod --dir=dist
```

Update `frontend/src/config.ts` with production backend URL.

## License

MIT License - See repository root for details.

## Learn More

- [Tutorial Documentation](../../docs/tutorial/31_react_vite_adk_integration.md)
- [Google ADK Documentation](https://github.com/google/adk-python)
- [CopilotKit Documentation](https://docs.copilotkit.ai/)
- [Vite Documentation](https://vitejs.dev/)
