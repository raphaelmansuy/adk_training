# Tutorial 31: React Vite + ADK Integration with AG-UI

A modern, fast data analysis dashboard built with Vite, React, TypeScript, and Google ADK. Upload CSV files and get instant insights through natural language conversations with a custom UI implementation using AG-UI protocol.

## Features

- 📊 **CSV Data Analysis**: Load and analyze CSV files with pandas
- 📈 **Interactive Charts**: Generate line, bar, and scatter plots with Chart.js
- 🤖 **AI-Powered**: Natural language queries powered by Gemini 2.0 Flash
- ⚡ **Lightning Fast**: Built with Vite for instant HMR and fast builds
- 🎨 **Modern UI**: Beautiful gradient design with responsive layout
- 📌 **Fixed Sidebar**: Charts stay visible while scrolling conversations
- 🎯 **AG-UI Protocol**: Real-time streaming with TOOL_CALL_RESULT events
- 💬 **Markdown Rendering**: Rich text formatting in chat messages
- ♿ **Accessible**: WCAG AA compliant with ARIA attributes

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Frontend (Vite + React + TypeScript)                       │
│  http://localhost:5173                                       │
│  ├─ Custom chat UI (no CopilotKit)                          │
│  ├─ File upload via drag-and-drop                           │
│  ├─ Fixed sidebar for chart visualization                   │
│  ├─ Markdown rendering (react-markdown)                     │
│  └─ Chart.js for data visualization                         │
└───────────────────┬─────────────────────────────────────────┘
                    │ Direct HTTP + SSE → /api/copilotkit
┌───────────────────▼─────────────────────────────────────────┐
│  Backend (FastAPI + AG-UI ADK)                               │
│  http://localhost:8000                                       │
│  ├─ ag_ui_adk middleware (AG-UI Protocol)                   │
│  ├─ ADKAgent wrapping Agent                                 │
│  │  ├─ Agent: gemini-2.0-flash-exp                          │
│  │  └─ Tools: load_csv_data, analyze_data, create_chart    │
│  └─ /api/copilotkit endpoint (SSE streaming)                │
└─────────────────────────────────────────────────────────────┘
```

**Key Architectural Features:**
- **AG-UI Protocol**: Uses `ag-ui-adk` for standardized agent-UI communication
- **No CopilotKit**: Custom React frontend without CopilotKit dependency
- **Event Streaming**: Real-time SSE (Server-Sent Events) for instant updates
- **TOOL_CALL_RESULT Events**: Charts transmitted via AG-UI protocol events
- **Fixed Sidebar**: Charts stay visible with independent scrolling
- **Direct Fetch API**: Simple HTTP requests, no proxy configuration needed

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

## Testing the Application

### Automated Tests

Run the test suite to verify functionality:

```bash
make test
```

This runs:
- **Import tests**: Verifies all dependencies are installed
- **Agent configuration tests**: Validates agent setup and tools
- **Structure tests**: Checks project file organization

### Manual Testing Guide

#### 1. Backend Health Check

```bash
# Check backend is running
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "agent": "data_analyst",
#   "datasets_loaded": [],
#   "num_datasets": 0
# }
```

#### 2. Upload CSV Data

1. Open http://localhost:5173 in your browser
2. Click "Drop CSV files here or browse"
3. Upload `sample_sales_data.csv` (provided in project root)
4. Verify success message appears

#### 3. Test Chart Generation

**Create a Bar Chart:**
- Type: "Create a bar chart of Product vs Revenue"
- Expected: Bar chart appears in fixed sidebar on the right
- Verify: Chart stays visible when scrolling the main chat area

**Create a Line Chart:**
- Type: "Create a line chart of Revenue over Date"
- Expected: Line chart with trend visualization
- Verify: Chart metadata shows (Type, X-Axis, Y-Axis, Data Points)

**Create Multiple Charts:**
- Generate 2-3 different charts
- Scroll the chat area up and down
- Verify: Sidebar remains fixed and visible
- Click ✕ button to close sidebar
- Generate new chart to reopen sidebar

#### 4. Test Data Analysis

**Summary Statistics:**
```
Ask: "What are the summary statistics for this dataset?"
Expected: Markdown-formatted statistics with bold headers
```

**Correlation Analysis:**
```
Ask: "Show me correlations between Sales and Revenue"
Expected: Correlation coefficients and interpretation
```

**Trend Analysis:**
```
Ask: "What's the trend in revenue over time?"
Expected: Upward/downward trend analysis with insights
```

#### 5. Test UI Features

**Fixed Sidebar:**
1. Generate a chart
2. Send 10+ chat messages to create a long conversation
3. Scroll the main chat area
4. **Expected**: Sidebar stays fixed on the right side
5. **Expected**: Sidebar content scrolls independently

**Close Button:**
1. Click ✕ in sidebar header
2. **Expected**: Sidebar disappears smoothly
3. Generate new chart
4. **Expected**: Sidebar slides back in from right

**Markdown Rendering:**
- Agent responses should render:
  - **Bold text**
  - *Italic text*
  - `Code blocks`
  - Bullet lists
  - Numbered lists

#### 6. Test Error Handling

**Missing File:**
```
Ask: "Analyze the file data.csv"
Expected: Error message "Dataset data.csv not found"
```

**Invalid Chart Request:**
```
Ask: "Create a chart of ProductXYZ vs Revenue"
Expected: Error message about invalid column
```

**Network Issues:**
1. Stop the backend (Ctrl+C in agent terminal)
2. Try to send a message
3. **Expected**: "Error: Could not get response from server"
4. Restart backend
5. **Expected**: Chat resumes working

### Performance Testing

**Load Time:**
- Frontend cold start: < 2 seconds
- Backend cold start: < 3 seconds
- HMR updates: < 50ms

**Chart Rendering:**
- First chart: < 500ms
- Subsequent charts: < 200ms
- Smooth animations and transitions

**File Upload:**
- Small files (< 1MB): < 1 second
- Medium files (1-5MB): < 3 seconds
- Large files (5-10MB): < 10 seconds

### Browser Compatibility

Tested and working on:
- ✅ Chrome/Edge 120+
- ✅ Firefox 120+
- ✅ Safari 17+

### Accessibility Testing

**Keyboard Navigation:**
1. Tab through all interactive elements
2. Press Space/Enter on buttons
3. **Expected**: All controls accessible via keyboard

**Screen Reader:**
1. Enable VoiceOver (Mac) or NVDA (Windows)
2. Navigate through the interface
3. **Expected**: All elements properly announced

**Color Contrast:**
- All text meets WCAG AA standards (4.5:1 ratio)
- Buttons have sufficient contrast in all states

## Usage Examples

### Upload CSV Data

1. Click "📁 Drop CSV files here or browse"
2. Select a CSV file from your computer (or use provided `sample_sales_data.csv`)
3. Wait for success confirmation in chat

### Sample CSV Data

The project includes `sample_sales_data.csv` with 15 rows:

```csv
Date,Product,Sales,Revenue,Region
2024-01-01,Widget A,5,2400,North
2024-01-02,Widget B,3,1800,South
2024-01-03,Widget A,4,1920,East
...
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
- **Google ADK** (`google-genai`): Agent framework
- **Gemini 2.0 Flash**: LLM model (`gemini-2.0-flash-exp`)
- **FastAPI**: Web framework with CORS middleware
- **ag_ui_adk**: AG-UI protocol integration (ADKAgent wrapper)
- **pandas**: Data analysis and manipulation
- **uvicorn**: ASGI server

### Frontend
- **Vite** 6.x: Next-generation build tool
- **React** 18.x: UI framework (custom implementation, no CopilotKit)
- **TypeScript** 5.x: Type-safe JavaScript
- **Tailwind CSS** 3.x: Utility-first CSS framework
- **Chart.js** 4.x + **react-chartjs-2** 5.x: Interactive data visualizations
- **react-markdown** 10.x: Markdown rendering with GitHub Flavored Markdown
- **remark-gfm** 4.x: GFM support (tables, task lists, strikethrough)
- **rehype-highlight** 7.x: Syntax highlighting for code blocks
- **rehype-raw** 7.x: HTML support in markdown
- **highlight.js** 11.x: Syntax highlighting styles

## Troubleshooting

### SSE Connection Issues

**Symptom**: No response from agent, messages not sending

**Causes & Solutions**:

1. **Backend not running**

   ```bash
   # Check if backend is running
   curl http://localhost:8000/api/copilotkit
   
   # If not running, start it
   make dev-agent
   ```

2. **Invalid JSON in request body**
   - Check browser console for `JSON.parse` errors
   - Ensure message format matches AG-UI protocol spec

3. **Agent name mismatch**
   - Verify agent name in `agent/agent.py` matches request body
   
   ```python
   adk_agent = Agent(
       name="data_analyst",  # ← Agent name
       # ...
   )
   ```

### 404 Error on `/api/copilotkit`

**Symptom**: Browser shows 404 (Not Found) for `/api/copilotkit`

**Causes & Solutions**:

1. **Backend not running**

   ```bash
   # Check if backend is running
   curl http://localhost:8000/api/copilotkit
   
   # If not running, start it
   make dev-agent
   ```

2. **Port conflict**

   ```bash
   # Check if port 8000 is in use
   lsof -i :8000
   
   # Kill process if needed
   kill -9 <PID>
   ```

3. **Frontend URL mismatch**
   - Verify frontend connects to correct backend URL
   - Check `App.tsx` fetch URL: `http://localhost:8000/api/copilotkit`
   - No Vite proxy needed (direct connection)

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

### Charts Not Displaying

**Symptom**: Charts don't display or sidebar is empty

**Solutions**:

1. **Chart is scrolled away**
   - Check if sidebar is visible on the right side
   - Try scrolling the main chat area up
   - Charts stay fixed but may be off-screen initially

2. **Chart data not extracted from TOOL_CALL_RESULT**
   - Check browser console for event parsing errors
   - Verify `create_chart` tool returns proper format:

   ```python
   {
     "status": "success",
     "chart_type": "line",  # Must match Line, Bar, or Scatter
     "data": {
       "labels": [...],  # Array of strings
       "values": [...]   # Array of numbers
     },
     "options": {...}
   }
   ```

3. **Chart.js not registered** in `App.tsx`:
   - Verify all Chart.js components are imported and registered
   - Check browser console for Chart.js registration errors

4. **Close button clicked accidentally**
   - Chart sidebar auto-hides when you click the ✕ button
   - Generate a new chart to show sidebar again

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
- [AG-UI ADK Documentation](https://github.com/google/adk-python/tree/main/ag_ui_adk)
- [Vite Documentation](https://vitejs.dev/)
- [React Documentation](https://react.dev/)
- [Chart.js Documentation](https://www.chartjs.org/)
