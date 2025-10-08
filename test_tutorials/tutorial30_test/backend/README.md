# Tutorial 30 Test - Next.js + Customer Support Agent

This directory contains the test implementation for Tutorial 30: Next.js 15 + ADK Integration with Customer Support Agent.

## Overview

This test verifies a production-ready customer support chatbot with three tools:
1. **search_knowledge_base()** - Search company knowledge base
2. **lookup_order_status()** - Check order status
3. **create_support_ticket()** - Create support tickets

## Test Structure

```
tutorial30_test/
├── backend/
│   ├── agent.py              # Customer support agent
│   ├── test_agent.py         # Comprehensive test suite
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example          # Environment variables template
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

3. **Configure environment**:
```bash
cp .env.example .env
# Edit .env and add your Google API key
```

## Running Tests

### Run all tests:
```bash
pytest test_agent.py -v
```

### Run specific test class:
```bash
pytest test_agent.py::TestKnowledgeBaseSearch -v
pytest test_agent.py::TestOrderStatusLookup -v
pytest test_agent.py::TestSupportTicketCreation -v
```

### Run with coverage:
```bash
pytest test_agent.py --cov=agent --cov-report=html
```

## Running the Agent

Start the FastAPI server:
```bash
python agent.py
```

Server runs at `http://localhost:8000`.

Test endpoints:
```bash
# Health check
curl http://localhost:8000/health

# Test knowledge base search
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "refund policy"}'
```

## Test Coverage

The test suite includes **9 test classes** with **40+ tests**:

### ✅ API Tests
- Health endpoint
- CORS configuration
- CopilotKit endpoint registration
- FastAPI app configuration

### ✅ Knowledge Base Tests
- Search refund policy
- Search shipping info
- Search warranty coverage
- Search account management
- Fallback to general support

### ✅ Order Lookup Tests
- Lookup existing orders (3 test orders)
- Case-insensitive lookup
- Nonexistent order handling

### ✅ Support Ticket Tests
- Create ticket with normal priority
- Create ticket with high priority
- Default priority handling
- Unique ticket ID generation

### ✅ Agent Configuration Tests
- Agent initialization
- Tool configuration
- ADKAgent wrapper setup

### ✅ Integration Tests
- All three tools working together
- Multiple knowledge base topics

## Expected Test Results

All tests should pass:
```
test_agent.py::TestTutorial30CustomerSupportAgent::test_health_endpoint PASSED
test_agent.py::TestTutorial30CustomerSupportAgent::test_cors_configuration PASSED
test_agent.py::TestTutorial30CustomerSupportAgent::test_copilotkit_endpoint_registered PASSED
test_agent.py::TestKnowledgeBaseSearch::test_search_refund_policy PASSED
test_agent.py::TestKnowledgeBaseSearch::test_search_shipping_info PASSED
test_agent.py::TestKnowledgeBaseSearch::test_search_warranty PASSED
test_agent.py::TestKnowledgeBaseSearch::test_search_account_management PASSED
test_agent.py::TestKnowledgeBaseSearch::test_search_no_match_returns_general_support PASSED
test_agent.py::TestOrderStatusLookup::test_lookup_existing_order_12345 PASSED
test_agent.py::TestOrderStatusLookup::test_lookup_existing_order_67890 PASSED
test_agent.py::TestOrderStatusLookup::test_lookup_existing_order_11111 PASSED
test_agent.py::TestOrderStatusLookup::test_lookup_case_insensitive PASSED
test_agent.py::TestOrderStatusLookup::test_lookup_nonexistent_order PASSED
test_agent.py::TestSupportTicketCreation::test_create_ticket_normal_priority PASSED
test_agent.py::TestSupportTicketCreation::test_create_ticket_high_priority PASSED
test_agent.py::TestSupportTicketCreation::test_create_ticket_default_priority PASSED
test_agent.py::TestSupportTicketCreation::test_create_ticket_generates_unique_id PASSED
... (40+ tests total)
```

## Tool Details

### 1. search_knowledge_base(query: str)
**Mock knowledge base with 4 articles**:
- Refund Policy
- Shipping Information
- Warranty Coverage
- Account Management

**Production**: Replace with vector store (Pinecone, Weaviate)

### 2. lookup_order_status(order_id: str)
**Mock orders database**:
- ORD-12345: Shipped
- ORD-67890: Processing
- ORD-11111: Delivered

**Production**: Connect to real order management system

### 3. create_support_ticket(issue_description: str, priority: str)
**Generates unique ticket IDs**: TICKET-XXXXXXXX

**Production**: Integrate with ticketing system (Zendesk, Freshdesk, Jira Service Desk)

## Frontend Integration

To test with Next.js frontend (from Tutorial 30):

1. Create Next.js app:
```bash
cd ../..
npx create-next-app@latest frontend --typescript --tailwind --app
cd frontend
npm install @copilotkit/react-core @copilotkit/react-ui
```

2. Update `app/page.tsx` with code from Tutorial 30

3. Start frontend:
```bash
npm run dev
```

4. Open `http://localhost:3000` and test chat:
   - "What is your refund policy?"
   - "Where is my order ORD-12345?"
   - "I need help with my account"

## Troubleshooting

### Tests Fail to Import `ag_ui_adk`
- Ensure correct package: `pip install ag_ui_adk`
- NOT `adk-middleware` (doesn't exist)

### Order Lookup Returns "Not Found"
- Use exact order IDs: ORD-12345, ORD-67890, ORD-11111
- Case doesn't matter: ord-12345 works too

### Ticket IDs Not Unique
- Check uuid import: `import uuid`
- Tests verify uniqueness

### CORS Errors
- Backend must run on port 8000
- Frontend on port 3000 (Next.js) or 5173 (Vite)
- Check CORS middleware configuration

## Production Considerations

### Replace Mock Data
1. **Knowledge Base**: Use vector store with real articles
2. **Orders**: Connect to order management API
3. **Tickets**: Integrate with support ticket system

### Add Authentication
```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/api/copilotkit", dependencies=[Depends(security)])
# ... endpoint with auth
```

### Add Rate Limiting
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

### Monitor Performance
```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("knowledge_search"):
    result = search_knowledge_base(query)
```

## Notes

- Uses corrected `ag_ui_adk` package (not `adk-middleware`)
- Agent uses latest `google.adk.agents.LlmAgent` API
- Direct Python function references for tools (not FunctionDeclaration)
- Mock data for testing without external dependencies
- Production-ready structure with health checks and CORS
- Comprehensive test coverage (40+ tests)
