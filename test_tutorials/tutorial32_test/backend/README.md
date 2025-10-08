# Tutorial 32: Streamlit + ADK Data Analysis Agent - Test Suite

## Overview

This directory contains the test suite for **Tutorial 32: Streamlit + ADK Integration**, which demonstrates how to build a data analysis assistant using pure Python integration (no HTTP server needed).

**Key Features Tested:**
- Data analysis tools (analyze_column, calculate_correlation, filter_data)
- Dataset summary generation
- Numeric and categorical data handling
- Missing value detection
- Tool parameter validation
- Agent configuration
- Error handling and edge cases

## Test Structure

```
tutorial32_test/backend/
├── agent.py              # Data analysis agent implementation
├── test_agent.py         # Comprehensive test suite (48 tests)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Test Coverage

### 1. Tool Function Tests (38 tests)

**TestAnalyzeColumn** (8 tests):
- ✅ Numeric column summary statistics
- ✅ Categorical column summary
- ✅ Numeric distribution with quartiles and outliers
- ✅ Categorical distribution (value counts)
- ✅ Top values analysis
- ✅ Error handling (nonexistent columns, no dataset, unknown types)

**TestCalculateCorrelation** (7 tests):
- ✅ Positive correlation (perfect correlation = 1.0)
- ✅ Negative correlation detection
- ✅ Weak/no correlation detection
- ✅ Error handling (nonexistent columns, non-numeric columns, mixed types)
- ✅ No dataset error handling

**TestFilterData** (11 tests):
- ✅ Equals operator (numeric and string)
- ✅ Greater_than operator
- ✅ Less_than operator
- ✅ Contains operator (case-insensitive)
- ✅ No matches scenario
- ✅ Error handling (nonexistent column, unknown operator, invalid numeric)
- ✅ No dataset error handling

**TestGetDatasetSummary** (5 tests):
- ✅ Basic summary (shape, columns, types)
- ✅ Missing values detection
- ✅ Memory usage calculation
- ✅ Large dataset handling
- ✅ No dataset error handling

**TestAgentConfiguration** (7 tests):
- ✅ Tool declarations validation
- ✅ Tool mapping completeness
- ✅ Agent config structure
- ✅ Agent creation with API key
- ✅ Error handling without API key
- ✅ Dynamic instruction generation (with/without data)

### 2. Tool Parameters Tests (4 tests)
- ✅ analyze_column parameter validation
- ✅ calculate_correlation parameter validation
- ✅ filter_data parameter validation
- ✅ get_dataset_summary parameter validation

### 3. Integration Tests (3 tests)
- ✅ Full numeric analysis workflow
- ✅ Categorical analysis workflow
- ✅ Error recovery workflow

## Running the Tests

### Prerequisites

```bash
# Python 3.9 or later
python --version

# Install dependencies
pip install -r requirements.txt
```

### Set API Key (Optional for basic tests)

```bash
export GOOGLE_API_KEY="your_gemini_api_key"
```

Most tests work without an API key since they test the tools directly. Only agent creation tests require an API key.

### Run All Tests

```bash
pytest test_agent.py -v
```

**Expected output:**
```
Test session starts (platform: darwin, Python 3.12.11, pytest 8.4.1)
collected 48 items

test_agent.py::TestAnalyzeColumn::test_numeric_summary PASSED                                [ 2%]
test_agent.py::TestAnalyzeColumn::test_categorical_summary PASSED                            [ 4%]
...
test_agent.py::TestIntegration::test_error_recovery PASSED                                   [100%]

================================================= 48 passed in 3.25s =================================================
```

### Run Specific Test Classes

```bash
# Test only tool functions
pytest test_agent.py::TestAnalyzeColumn -v

# Test only integration
pytest test_agent.py::TestIntegration -v
```

### Generate JSON Report

```bash
pytest test_agent.py --json-report --json-report-file=test_report.json
```

## Test Data

### Sample DataFrame (8 rows)

```
product     price  sales  category      region
Widget A    29.99    150  Electronics   North
Widget B    49.99    230  Electronics   South
Gadget X    15.99    450  Accessories   East
Gadget Y    25.99    320  Accessories   West
Device 1   199.99     45  Electronics   North
Device 2   299.99     30  Electronics   South
Tool A      35.00    280  Hardware      North
Tool B      42.50    195  Hardware      East
```

### Large DataFrame (100 rows)
- 100 rows with random values
- Includes missing values (None in 'status' column)
- Multiple categories
- Used for testing performance and missing value handling

## Key Features

### 1. Pure Python Integration
Unlike Tutorials 30 and 31 (Next.js and Vite), this agent runs directly in the Streamlit process:
- No FastAPI server needed
- No HTTP requests
- No AG-UI middleware
- Direct function calls (in-process)

### 2. Comprehensive Data Analysis
Four powerful tools for data exploration:
- **analyze_column**: Statistics, distributions, top values
- **calculate_correlation**: Find relationships between numeric columns
- **filter_data**: Subset data with conditions
- **get_dataset_summary**: Overview of entire dataset

### 3. Pandas Integration
Full pandas DataFrame support:
- Numeric and categorical columns
- Missing value detection
- Memory usage tracking
- Efficient filtering and aggregation

### 4. Error Handling
Robust error handling for:
- Nonexistent columns
- Wrong data types
- Invalid operators
- Missing datasets
- Invalid numeric conversions

## Differences from Other Tutorials

| Aspect | Tutorial 30 (Next.js) | Tutorial 31 (Vite) | Tutorial 32 (Streamlit) |
|--------|----------------------|-------------------|------------------------|
| **Framework** | Next.js + FastAPI | React + FastAPI | Streamlit only |
| **Backend** | Separate server | Separate server | In-process |
| **Communication** | HTTP/WebSocket | HTTP/WebSocket | Direct function calls |
| **Latency** | ~50-100ms | ~50-100ms | ~0ms (in-process) |
| **Deployment** | 2 services | 2 services | 1 service |
| **Complexity** | High | Medium | Low |
| **Best for** | Production web apps | Lightweight apps | Data tools, dashboards |

## Example Usage

### Analyze a Column

```python
import pandas as pd
from agent import analyze_column

df = pd.read_csv("sales_data.csv")

# Get summary statistics
result = analyze_column("revenue", "summary", df)
print(result)
# {
#   "column": "revenue",
#   "type": "numeric",
#   "mean": 1250.50,
#   "median": 980.00,
#   "std": 425.30,
#   ...
# }
```

### Calculate Correlation

```python
from agent import calculate_correlation

result = calculate_correlation("price", "sales", df)
print(result)
# {
#   "column1": "price",
#   "column2": "sales",
#   "correlation": -0.65,
#   "interpretation": "moderate negative"
# }
```

### Filter Data

```python
from agent import filter_data

result = filter_data("revenue", "greater_than", "1000", df)
print(result)
# {
#   "original_rows": 100,
#   "filtered_rows": 42,
#   "filter": "revenue greater_than 1000",
#   "sample": [...]
# }
```

## Common Issues

### Issue 1: "No dataset provided" Error

**Cause**: Function called without dataframe parameter.

**Solution**:
```python
# ❌ Wrong
result = analyze_column("price", "summary")

# ✅ Correct
result = analyze_column("price", "summary", df)
```

### Issue 2: "Column not found" Error

**Cause**: Column name doesn't exist in dataframe.

**Solution**:
```python
# Check columns first
print(df.columns.tolist())

# Use exact column name (case-sensitive)
result = analyze_column("Price", "summary", df)  # ❌ Wrong case
result = analyze_column("price", "summary", df)  # ✅ Correct
```

### Issue 3: "Both columns must be numeric" Error

**Cause**: Trying to calculate correlation between non-numeric columns.

**Solution**:
```python
# Check column types
print(df.dtypes)

# Only use numeric columns for correlation
result = calculate_correlation("price", "quantity", df)  # ✅ Both numeric
```

## Performance

Test execution times (on M1 Mac):
- Individual tool tests: < 10ms each
- Integration tests: < 50ms each
- Full test suite (48 tests): ~3-5 seconds

The agent is designed for fast in-process execution:
- No network latency
- Direct pandas operations
- Minimal overhead

## Next Steps

After mastering Tutorial 32, continue with:

- **Tutorial 33**: Slack Bot Integration - Build team support bots
- **Tutorial 34**: Pub/Sub Integration - Event-driven architectures
- **Tutorial 35**: AG-UI Deep Dive - Advanced CopilotKit features

## Contributing

Found an issue or want to improve the tests? Please open an issue or submit a pull request!

## License

Same as ADK Training repository.
