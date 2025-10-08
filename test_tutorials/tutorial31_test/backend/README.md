# Tutorial 31 - Data Analysis Agent Tests

Comprehensive test suite for Tutorial 31: React Vite + ADK Integration with Data Analysis Agent.

## Overview

This test implementation covers a data analysis agent with pandas tools that can:
- Load and parse CSV datasets
- Perform statistical analysis (summary, correlation, trend)
- Generate chart data for visualizations
- Handle multiple datasets simultaneously

## Agent Features

### Tools

1. **load_csv_data(file_name, csv_content)**
   - Loads CSV data into memory
   - Returns dataset summary with preview
   - Provides column types and basic info

2. **analyze_data(file_name, analysis_type, columns)**
   - Performs statistical analysis
   - Analysis types: `summary`, `correlation`, `trend`
   - Optional column selection

3. **create_chart(file_name, chart_type, x_column, y_column)**
   - Generates chart configuration
   - Chart types: `line`, `bar`, `scatter`
   - Returns data formatted for Chart.js

### API Endpoints

- `GET /health` - Health check with loaded datasets list
- `POST /clear` - Clear all loaded datasets
- `POST /api/copilotkit` - CopilotKit endpoint (AG-UI integration)

## Test Coverage

### Test Classes

1. **TestTutorial31DataAnalysisAgent** (4 tests)
   - Health endpoint verification
   - Clear datasets functionality
   - CORS configuration
   - CopilotKit endpoint registration

2. **TestLoadCSVData** (8 tests)
   - Valid CSV loading
   - Multiple dataset handling
   - Data type detection
   - Preview data format
   - Invalid CSV handling
   - Empty CSV handling
   - Dataset overwriting

3. **TestAnalyzeData** (10 tests)
   - Summary analysis
   - Column-specific analysis
   - Correlation matrices
   - Trend detection
   - Error handling for missing datasets
   - Invalid column handling
   - Unknown analysis types
   - Non-numeric data handling

4. **TestCreateChart** (8 tests)
   - Line chart generation
   - Bar chart generation
   - Scatter chart generation
   - Chart options and metadata
   - Error handling for invalid datasets/columns
   - Data type validation

5. **TestAgentConfiguration** (5 tests)
   - Agent initialization
   - Tool registration (3 tools)
   - Model configuration
   - Wrapper configuration

6. **TestAPIConfiguration** (3 tests)
   - FastAPI app title
   - CORS middleware presence
   - Multiple origin support

7. **TestIntegration** (3 tests)
   - Full analysis workflow (load → analyze → chart)
   - Multiple dataset workflows
   - Health endpoint dataset reporting

**Total Tests**: 41 tests

## Setup

### Prerequisites

- Python 3.9+
- Google API key (Gemini)

### Installation

```bash
cd tutorial31_test/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### Running Tests

```bash
# Run all tests
pytest test_agent.py -v

# Run specific test class
pytest test_agent.py::TestLoadCSVData -v

# Run with coverage
pytest test_agent.py --cov=agent --cov-report=html

# Run from master test runner
cd ../..
python run_all_tests.py
```

## Sample CSV Data

The test suite uses three sample datasets:

### Sales Data
```csv
date,product,sales,revenue
2024-01-01,Product A,100,1000
2024-01-02,Product A,120,1200
...
```

### Weather Data
```csv
date,temperature,humidity,rainfall
2024-01-01,25.5,60,0
2024-01-02,26.0,65,5
...
```

### Employee Data
```csv
name,department,salary,years_experience
Alice,Engineering,90000,5
Bob,Marketing,70000,3
...
```

## Usage Example

```python
# Load CSV data
result = load_csv_data("sales.csv", csv_content)
# Returns: {
#   "status": "success",
#   "file_name": "sales.csv",
#   "rows": 5,
#   "columns": ["date", "product", "sales", "revenue"],
#   "preview": [...],
#   "dtypes": {...}
# }

# Analyze data
analysis = analyze_data("sales.csv", "summary")
# Returns: {
#   "status": "success",
#   "file_name": "sales.csv",
#   "analysis_type": "summary",
#   "data": {
#     "describe": {...},
#     "missing": {...},
#     "unique": {...}
#   }
# }

# Create chart
chart = create_chart("sales.csv", "line", "date", "sales")
# Returns: {
#   "status": "success",
#   "chart_type": "line",
#   "data": {
#     "labels": [...],
#     "values": [...]
#   },
#   "options": {
#     "x_label": "date",
#     "y_label": "sales",
#     "title": "sales vs date"
#   }
# }
```

## Frontend Integration

This backend is designed to work with a Vite + React frontend using CopilotKit:

```tsx
// Frontend (Vite + React)
import { CopilotKit } from "@copilotkit/react-core";

function App() {
  return (
    <CopilotKit runtimeUrl="http://localhost:8000/api/copilotkit">
      <DataAnalysisDashboard />
    </CopilotKit>
  );
}
```

See the full tutorial at `/tutorial/31_react_vite_adk_integration.md`.

## Production Considerations

### Data Persistence

Current implementation uses in-memory storage (`uploaded_data` dict). For production:

```python
# Consider using Redis for session storage
import redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Or use agent's state management
agent.state["uploaded_data"] = df
```

### File Size Limits

Add file size validation:

```python
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def load_csv_data(file_name: str, csv_content: str):
    if len(csv_content) > MAX_FILE_SIZE:
        return {"status": "error", "error": "File too large"}
    # ... rest of function
```

### Security

- Validate file contents before parsing
- Sanitize column names
- Limit number of datasets per session
- Add authentication if needed

### Performance

- Stream large CSV files instead of loading entirely into memory
- Use chunked processing for large datasets
- Add caching for expensive analyses
- Consider using Dask for very large datasets

## Troubleshooting

### Import Errors

```bash
# Make sure all dependencies are installed
pip install -r requirements.txt

# Check pandas version
python -c "import pandas; print(pandas.__version__)"
```

### Test Failures

```bash
# Clear any existing data
python -c "from agent import uploaded_data; uploaded_data.clear()"

# Run tests with verbose output
pytest test_agent.py -v --tb=short

# Check specific test
pytest test_agent.py::TestLoadCSVData::test_load_valid_csv -v
```

### Memory Issues

If handling large datasets causes memory issues:

```python
# Use chunked reading
for chunk in pd.read_csv(io.StringIO(csv_content), chunksize=1000):
    # Process chunk
    pass
```

## Next Steps

- Add support for Excel files (`.xlsx`)
- Implement data transformation tools
- Add export functionality (CSV, JSON)
- Create custom chart types
- Add data validation and cleaning tools
- Implement machine learning analysis tools

## Related Tutorials

- Tutorial 29: UI Integration Introduction
- Tutorial 30: Next.js + ADK Integration
- Tutorial 32: Streamlit + ADK Integration
- Tutorial 35: Advanced AG-UI Features

---

**Test Status**: 41/41 tests (Ready to run)  
**Coverage**: All tools, API endpoints, and integration workflows  
**Execution Time**: ~5-8 seconds
