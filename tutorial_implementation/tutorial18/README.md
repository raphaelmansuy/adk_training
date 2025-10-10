# Tutorial 18: Events and Observability

Comprehensive observability implementation for Google ADK agents with event tracking, metrics collection, and monitoring dashboards.

## Features

- **Event Tracking**: Monitor all agent actions, tool calls, and state changes
- **Metrics Collection**: Track performance, errors, and escalations
- **Real-time Alerting**: Alert on specific event patterns
- **Customer Service Agent**: Full implementation with observability
- **Comprehensive Testing**: 49 tests covering all observability features

## Quick Start

```bash
# Setup environment
make setup

# Set your Google API key
export GOOGLE_API_KEY=your_api_key_here

# Run the agent with ADK web interface
make dev

# Or run demo scenarios
make demo
```

## Installation

### Prerequisites

- Python 3.10 or higher
- Google API Key (Gemini)

### Setup

```bash
# Install dependencies
make setup

# Run tests
make test

# View test coverage
make coverage
```

## Usage

### Running with ADK Web Interface

```bash
make dev
# Opens http://localhost:8000
# Select "observability_agent" from dropdown
# Try example queries to see event tracking
```

### Demo Scenarios

The `make demo` command runs four customer service scenarios:

1. **Order Status Inquiry** - Simple query with tool call
2. **Small Refund** - Refund under threshold (approved)
3. **Large Refund** - Refund over threshold (escalated)
4. **Inventory Check** - Product availability query

Each scenario demonstrates:
- Event creation and tracking
- Tool call logging
- State management
- Escalation handling
- Comprehensive reports

### Example Queries

```python
# Order status inquiry
"What is the status of my order ORD-001?"

# Refund request (small)
"I want a refund of $50 for order ORD-002"

# Refund request (large - triggers escalation)
"I need a refund of $150 for order ORD-003"

# Inventory check
"Is product PROD-B in stock?"
```

## Event Tracking

The agent tracks all interactions:

### Event Types

- **customer_query**: User requests
- **tool_call**: Tool invocations with arguments
- **agent_response**: Agent replies
- **escalation**: Requests escalated to supervisor

### Metrics Collected

- **Total Events**: All events generated
- **Tool Calls**: Number and types of tools used
- **Escalations**: Escalation count and reasons
- **Response Times**: Agent latency metrics
- **Error Rates**: Tool and agent errors

### Event Reports

Two comprehensive reports are generated:

1. **Event Summary Report**:
   - Total events by type
   - Tool usage statistics
   - Escalation summary

2. **Detailed Timeline**:
   - Chronological event log
   - Full event details
   - Tool arguments and results

## Project Structure

```
tutorial18/
├── observability_agent/
│   ├── __init__.py           # Package initialization, exports root_agent
│   └── agent.py              # CustomerServiceMonitor implementation
├── tests/
│   ├── test_agent.py         # Agent configuration tests
│   ├── test_events.py        # Event tracking tests
│   ├── test_imports.py       # Import validation
│   ├── test_observability.py # Metrics and logging tests
│   └── test_structure.py     # Project structure tests
├── Makefile                  # Development commands
├── pyproject.toml            # Project configuration
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .env.example              # Environment variable template
```

## Testing

### Run All Tests

```bash
make test
```

### Test Coverage

```bash
make coverage
```

### Test Structure

- **test_agent.py**: Agent configuration and initialization (11 tests)
- **test_events.py**: Event creation and tracking (8 tests)
- **test_observability.py**: Metrics, logging, alerting (18 tests)
- **test_imports.py**: Import validation (7 tests)
- **test_structure.py**: Project structure (5 tests)

**Total**: 49 comprehensive tests (100% passing)

## Architecture

### CustomerServiceMonitor

Main class implementing observability:

```python
class CustomerServiceMonitor:
    """Customer service with comprehensive event monitoring."""
    
    def __init__(self):
        # Event storage
        self.events: List[Dict] = []
        
        # Customer service agent with tools
        self.agent = Agent(...)
        
    async def handle_customer_query(self, customer_id, query):
        # Track query, execute agent, log response
        ...
        
    def get_event_summary(self) -> str:
        # Generate summary report
        ...
        
    def get_detailed_timeline(self) -> str:
        # Generate timeline report
        ...
```

### Observability Classes

1. **EventLogger**: Structured logging for events
2. **MetricsCollector**: Performance metrics tracking
3. **EventAlerter**: Real-time alerting on patterns

## Configuration

### Environment Variables

Create `.env` file from template:

```bash
cp .env.example .env
```

Required variables:

```bash
GOOGLE_API_KEY=your_api_key_here
```

Optional (for Vertex AI):

```bash
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

## Best Practices

### Event Tracking

✅ **DO**:
- Log all critical state changes
- Include rich context in events
- Track tool calls with arguments
- Use escalation for risky operations

❌ **DON'T**:
- Log sensitive data (passwords, tokens)
- Create events without context
- Ignore error events
- Skip escalation rules

### Metrics Collection

✅ **DO**:
- Track latency for all operations
- Monitor error rates
- Set up alerting thresholds
- Aggregate metrics over time

❌ **DON'T**:
- Block on metrics collection
- Store unbounded metrics
- Ignore performance degradation
- Skip error tracking

## Troubleshooting

### Events not appearing

**Solution**: Ensure events are properly created:

```python
event = Event(
    invocation_id='inv-123',  # Required
    author='agent_name',       # Required
    content=types.Content(...) # Required
)
```

### State not persisting

**Solution**: Use session for state:

```python
session = Session()
result = await runner.run_async(query, agent=agent, session=session)
```

### ADK web agent not appearing

**Solution**: Ensure package is installed:

```bash
pip install -e .
adk web  # Not "adk web observability_agent"
```

## Resources

- [Tutorial 18 Documentation](../../docs/tutorial/18_events_observability.md)
- [ADK Events Documentation](https://google.github.io/adk-docs/events/)
- [Google ADK Python](https://github.com/google/adk-python)

## License

Apache License 2.0
