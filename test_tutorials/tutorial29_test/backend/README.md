# Tutorial 29 Test - Quickstart Agent

This directory contains the test implementation for Tutorial 29: Introduction to UI Integration & AG-UI Protocol.

## Test Structure

```
tutorial29_test/
├── backend/
│   ├── agent.py              # Quickstart agent implementation
│   ├── test_agent.py         # Test suite
│   ├── requirements.txt      # Python dependencies
│   └── README.md            # This file
```

## Setup

1. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set environment variable**:
```bash
export GOOGLE_GENAI_API_KEY="your-api-key"
```

## Running Tests

### Run all tests:
```bash
pytest test_agent.py -v
```

### Run specific test class:
```bash
pytest test_agent.py::TestTutorial29QuickstartAgent -v
```

### Run with coverage:
```bash
pytest test_agent.py --cov=agent --cov-report=html
```

## Running the Agent

To run the agent server:
```bash
python agent.py
```

The server will start at `http://localhost:8000`.

Test the health endpoint:
```bash
curl http://localhost:8000/health
```

## Test Coverage

The test suite covers:

✅ **Health Endpoint**: Verifies server is running correctly  
✅ **CORS Configuration**: Tests cross-origin resource sharing  
✅ **CopilotKit Endpoint**: Verifies AG-UI endpoint registration  
✅ **Agent Configuration**: Tests agent setup and model  
✅ **API Response Structure**: Validates response formats  

## Expected Test Results

All tests should pass:
```
test_agent.py::TestTutorial29QuickstartAgent::test_health_endpoint PASSED
test_agent.py::TestTutorial29QuickstartAgent::test_cors_headers PASSED
test_agent.py::TestTutorial29QuickstartAgent::test_copilotkit_endpoint_exists PASSED
test_agent.py::TestTutorial29QuickstartAgent::test_app_metadata PASSED
test_agent.py::TestTutorial29QuickstartAgent::test_cors_origins_configured PASSED
test_agent.py::TestAgentConfiguration::test_agent_import PASSED
test_agent.py::TestAgentConfiguration::test_agent_has_correct_model PASSED
test_agent.py::TestAPIEndpoints::test_health_response_structure PASSED
```

## Integration with Frontend

To test with the frontend from Tutorial 29:

1. Start the backend server:
```bash
python agent.py
```

2. In a separate terminal, create and run the frontend:
```bash
cd ../../
npm create vite@latest frontend -- --template react-ts
cd frontend
npm install @copilotkit/react-core @copilotkit/react-ui
npm install
npm run dev
```

3. Update `frontend/src/App.tsx` with the code from Tutorial 29

4. Open `http://localhost:5173` and test the chat interface

## Troubleshooting

### Import Error: `ag_ui_adk`
- Ensure you've installed the correct package: `pip install ag_ui_adk`
- NOT `adk-middleware` (that package doesn't exist)

### CORS Error in Browser
- Check that the backend is running on port 8000
- Verify frontend is running on port 5173 or 3000
- Check CORS middleware configuration in `agent.py`

### API Key Error
- Verify `GOOGLE_GENAI_API_KEY` environment variable is set
- Check the API key is valid at https://aistudio.google.com/

## Notes

- This test uses the corrected `ag_ui_adk` package (not `adk-middleware`)
- Agent uses latest `google.adk.agents.LlmAgent` API
- Tests can run without a real API key for basic endpoint verification
- Full agent functionality requires a valid Google AI API key
