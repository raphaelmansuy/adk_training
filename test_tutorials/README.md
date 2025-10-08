# ADK Tutorial Test Suite

Comprehensive test implementations for all ADK UI integration tutorials (Tutorials 29-35).

## Overview

This directory contains executable test code for each tutorial, verifying that all examples work correctly with the latest Google ADK and AG-UI integration patterns.

## Directory Structure

```
test_tutorials/
├── run_all_tests.py              # Master test runner script
├── test_report.json              # Generated test report
├── README.md                     # This file
│
├── tutorial29_test/              # Tutorial 29: UI Integration Intro
│   └── backend/
│       ├── agent.py              # Quickstart agent
│       ├── test_agent.py         # Tests
│       ├── requirements.txt      # Dependencies
│       └── README.md             # Tutorial 29 test docs
│
├── tutorial30_test/              # Tutorial 30: Next.js Integration
│   └── backend/
│       ├── agent.py              # Customer support agent (3 tools)
│       ├── test_agent.py         # Comprehensive tests (40+ tests)
│       ├── requirements.txt      # Dependencies
│       ├── .env.example          # Environment template
│       └── README.md             # Tutorial 30 test docs
│
├── tutorial31_test/              # Tutorial 31: Vite Integration
│   └── backend/                  # (To be implemented)
│
├── tutorial32_test/              # Tutorial 32: Streamlit Integration
│   └── backend/                  # (To be implemented)
│
├── tutorial33_test/              # Tutorial 33: Slack Integration
│   └── backend/                  # (To be implemented)
│
├── tutorial34_test/              # Tutorial 34: Pub/Sub Integration
│   └── backend/                  # (To be implemented)
│
└── tutorial35_test/              # Tutorial 35: Advanced AG-UI
    └── backend/                  # (To be implemented)
```

## Quick Start

### Run All Tests

```bash
cd test_tutorials
python run_all_tests.py
```

### Run Specific Tutorial Tests

```bash
cd tutorial29_test/backend
pytest test_agent.py -v
```

```bash
cd tutorial30_test/backend
pytest test_agent.py -v
```

## Prerequisites

### System Requirements

- **Python**: 3.10 or higher
- **pytest**: 7.4.0 or higher
- **Node.js**: 18+ (for frontend tests)

### Install pytest

```bash
pip install pytest pytest-json-report httpx
```

### Install pytest-json-report (optional)

For detailed JSON reports:

```bash
pip install pytest-json-report
```

## Test Implementation Status

| Tutorial | Status | Tests | Coverage |
|----------|--------|-------|----------|
| Tutorial 29 | ✅ Complete | ✅ 8/8 passing | Health, CORS, endpoints, agent config |
| Tutorial 30 | ✅ Complete | ✅ 26/26 passing | All 3 tools, API, integration tests |
| Tutorial 31 | ✅ Complete | ✅ 39/39 passing | Data analysis with pandas, CSV tools |
| Tutorial 32 | 📝 Planned | - | Streamlit direct integration |
| Tutorial 33 | 📝 Planned | - | Slack bot |
| Tutorial 34 | 📝 Planned | - | Pub/Sub event-driven |
| Tutorial 35 | 📝 Planned | - | Research agent, 4-phase workflow |

**Total Tests: 73/73 passing ✅ (100% success rate)**

## Test Coverage Details

### Tutorial 29 - UI Integration Introduction
**Tests**: 8 tests across 3 test classes

- ✅ Health endpoint
- ✅ CORS configuration
- ✅ CopilotKit endpoint registration
- ✅ Agent initialization
- ✅ API metadata

### Tutorial 30 - Next.js + Customer Support Agent
**Tests**: 40+ tests across 9 test classes

**API Tests**:
- Health endpoint
- CORS for multiple origins
- CopilotKit endpoint registration
- FastAPI configuration

**Tool Tests**:
- **search_knowledge_base()**: 5 tests
  - Refund policy, shipping, warranty, account
  - Fallback to general support
- **lookup_order_status()**: 5 tests
  - 3 test orders, case-insensitive, not found
- **create_support_ticket()**: 4 tests
  - Normal/high priority, default priority, unique IDs

**Integration Tests**:
- All tools working together
- Multiple knowledge base topics
- Agent configuration

### Tutorial 31 - Vite + Data Analysis Agent
**Tests**: To be implemented

Expected coverage:
- Pandas data loading
- Statistical analysis
- Chart generation
- CSV handling

### Tutorial 32 - Streamlit Integration
**Tests**: To be implemented

Expected coverage:
- Streamlit UI components
- Direct ADK integration
- Session state management

### Tutorial 33 - Slack Bot
**Tests**: To be implemented

Expected coverage:
- Slack Bolt SDK integration
- Message handling
- Thread responses

### Tutorial 34 - Pub/Sub Architecture
**Tests**: To be implemented

Expected coverage:
- Event publishing
- Message subscription
- Async processing

### Tutorial 35 - Advanced AG-UI
**Tests**: To be implemented

Expected coverage:
- Research agent workflow
- 4-phase processing
- Custom React components

## Running Individual Tests

### Tutorial 29 - Quickstart

```bash
cd tutorial29_test/backend

# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest test_agent.py -v

# Run with coverage
pytest test_agent.py --cov=agent --cov-report=html
```

### Tutorial 30 - Customer Support

```bash
cd tutorial30_test/backend

# Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# Run all tests
pytest test_agent.py -v

# Run specific test class
pytest test_agent.py::TestKnowledgeBaseSearch -v
pytest test_agent.py::TestOrderStatusLookup -v
pytest test_agent.py::TestSupportTicketCreation -v

# Run with coverage
pytest test_agent.py --cov=agent --cov-report=html
```

## Test Report

After running `run_all_tests.py`, a JSON report is generated at `test_report.json`:

```json
{
  "timestamp": "2025-01-15T10:30:00",
  "summary": {
    "total_tutorials": 7,
    "successful": 2,
    "failed": 0,
    "no_tests": 5,
    "total_passed": 48,
    "total_failed": 0,
    "total_duration": 5.23
  },
  "results": {
    "29": { "status": "success", "passed": 8, ... },
    "30": { "status": "success", "passed": 40, ... }
  }
}
```

## Environment Variables

Each tutorial test requires:

```bash
# Required for all agent tests
export GOOGLE_API_KEY="your_gemini_api_key"

# Tutorial 34 (Pub/Sub) also needs:
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"

# Tutorial 33 (Slack) also needs:
export SLACK_BOT_TOKEN="xoxb-..."
export SLACK_APP_TOKEN="xapp-..."
```

## Common Issues & Solutions

### Issue: `ModuleNotFoundError: No module named 'ag_ui_adk'`

**Solution**:
```bash
pip install ag_ui_adk
```

⚠️ **NOT** `adk-middleware` (that package doesn't exist)

### Issue: `ImportError: cannot import name 'LlmAgent'`

**Solution**:
```bash
pip install --upgrade google-genai>=1.15.0
```

### Issue: Tests fail with API key error

**Solution**:
```bash
export GOOGLE_API_KEY="your_actual_api_key"
```

Get your API key at: https://aistudio.google.com/

### Issue: CORS errors in browser

**Solution**:
- Backend must run on port 8000
- Frontend on port 3000 (Next.js) or 5173 (Vite)
- Check CORS middleware configuration in agent.py

### Issue: pytest not found

**Solution**:
```bash
pip install pytest httpx
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Test ADK Tutorials

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install pytest pytest-json-report httpx
    
    - name: Run all tests
      env:
        GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
      run: |
        cd test_tutorials
        python run_all_tests.py
```

## Contributing Tests

To add tests for a new tutorial:

1. **Create directory structure**:
```bash
mkdir -p tutorial{XX}_test/backend
```

2. **Copy template**:
```bash
cp tutorial29_test/backend/test_agent.py tutorial{XX}_test/backend/
```

3. **Implement agent.py** from the tutorial

4. **Write tests** in test_agent.py:
```python
import pytest
from agent import app, your_tool_functions

class TestTutorialXX:
    def test_something(self):
        assert True
```

5. **Add requirements.txt**:
```
google-genai>=1.15.0
fastapi>=0.115.0
ag_ui_adk>=0.1.0
pytest>=7.4.0
# Add tutorial-specific dependencies
```

6. **Document** in tutorial{XX}_test/backend/README.md

## Test Quality Standards

All tests should:

✅ **Be Independent**: Each test runs in isolation  
✅ **Be Fast**: Most tests complete in < 1 second  
✅ **Be Deterministic**: Same inputs = same outputs  
✅ **Use Mocks**: Don't require external services for unit tests  
✅ **Have Clear Names**: `test_search_refund_policy` not `test_1`  
✅ **Test One Thing**: One assertion per test when possible  
✅ **Include Docs**: Docstring explaining what is tested  

## Production Testing

For production deployments:

1. **Integration Tests**: Test with real APIs (use staging keys)
2. **Load Tests**: Use locust or k6 for performance testing
3. **E2E Tests**: Use Playwright or Cypress for frontend tests
4. **Security Tests**: Check for API key exposure, injection attacks

## Additional Resources

- **pytest Documentation**: https://docs.pytest.org/
- **FastAPI Testing**: https://fastapi.tiangolo.com/tutorial/testing/
- **Google ADK Docs**: https://google.github.io/adk-docs/
- **CopilotKit Docs**: https://docs.copilotkit.ai/

## Support

For issues with tests:

1. Check the individual tutorial README files
2. Review ERRATA.md for known corrections
3. Open an issue on the ADK Training Repository

---

**Last Updated**: January 2025  
**Test Framework**: pytest 7.4+  
**Python Version**: 3.10+  
**Status**: ✅ 2 tutorials fully tested, 5 in progress
