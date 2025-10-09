# Tutorial 10: Evaluation & Testing - Working Implementation

This is the complete working implementation of **Tutorial 10: Evaluation & Testing** from the ADK Training repository.

## Overview

This implementation demonstrates comprehensive testing patterns for ADK agents, including:

- **Unit Tests**: Individual tool testing with pytest
- **Integration Tests**: Multi-step workflow validation
- **Evaluation Tests**: Trajectory and response quality assessment
- **Configuration Tests**: Agent setup validation

## Quick Start

```bash
# Install dependencies
make setup

# Run the agent in development mode
make dev

# Run comprehensive tests
make test
```

## Project Structure

```text
tutorial10/
├── support_agent/           # Agent implementation
│   ├── __init__.py         # Package exports
│   ├── agent.py            # Customer support agent
│   └── .env.example        # Environment template
├── tests/                  # Comprehensive test suite
│   ├── test_agent.py       # pytest test suite
│   ├── test_config.json    # Evaluation criteria
│   ├── simple.test.json    # Basic evaluation test
│   ├── ticket_creation.test.json  # Workflow test
│   └── complex.evalset.json       # Multi-turn test
├── requirements.txt        # Python dependencies
├── Makefile               # Development commands
└── README.md              # This file
```

## Agent Features

The **Customer Support Agent** provides:

- **Knowledge Base Search**: Answers common customer questions
- **Ticket Creation**: Creates support tickets with priority levels
- **Ticket Status Checks**: Monitors existing ticket progress

### Available Tools

1. `search_knowledge_base(query)` - Search for answers
2. `create_ticket(issue, priority)` - Create support tickets
3. `check_ticket_status(ticket_id)` - Check ticket status

## Testing

### Unit Tests

Run individual tool and configuration tests:

```bash
make test
```

**Test Coverage:**

- ✅ Tool function behavior (16 tests)
- ✅ Agent configuration validation (6 tests)
- ✅ Integration workflows (2 tests)
- ✅ Evaluation framework tests (3 async tests)

### Evaluation Tests

Run trajectory and response quality assessments:

```bash
make eval
```

**Evaluation Files:**

- `simple.test.json` - Basic knowledge base search
- `ticket_creation.test.json` - Multi-step ticket workflow
- `complex.evalset.json` - Multi-turn conversation

## Demo Prompts

Try these example prompts in the ADK web interface:

```bash
make demo
```

**Example Interactions:**

1. **Password Reset**: "How do I reset my password?"
2. **Urgent Issue**: "My account is completely locked!"
3. **Policy Question**: "What's your refund policy?"
4. **Status Check**: "Check status of ticket TICK-ABC123"

## Configuration

1. **Copy environment template:**

   ```bash
   cp support_agent/.env.example support_agent/.env
   ```

2. **Add your API key:**

   ```bash
   # Edit support_agent/.env
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

## Development Commands

```bash
make setup      # Install dependencies
make dev        # Start ADK web interface
make test       # Run all tests
make test-cov   # Run tests with coverage report
make eval       # Run evaluation tests
make demo       # Show demo prompts
make clean      # Clean cache files
```

## Test Results

**Expected Test Output:**

```
**Expected Test Output:**

```text
tests/test_agent.py::TestToolFunctions::test_search_knowledge_base_password_reset PASSED
tests/test_agent.py::TestToolFunctions::test_create_ticket_normal_priority PASSED
tests/test_agent.py::TestAgentConfiguration::test_agent_name PASSED
tests/test_agent.py::TestIntegration::test_ticket_creation_workflow PASSED
tests/test_agent.py::test_simple_kb_search PASSED
tests/test_agent.py::test_ticket_creation PASSED
tests/test_agent.py::test_multi_turn_conversation PASSED

=============== 28 passed in 8.43s ===============
```
```

## Evaluation Metrics

**Trajectory Score**: Measures tool call accuracy (0.0-1.0)

- 1.0 = Perfect tool sequence match
- 0.8 = Good match with minor variations

**Response Score**: Measures answer quality (0.0-1.0)

- 0.9+ = Excellent match
- 0.7-0.8 = Good match
- 0.5-0.6 = Acceptable match

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure dependencies are installed with `make setup`

2. **API Key Issues**: Verify `GOOGLE_API_KEY` is set in `.env`

3. **Test Failures**: Check that all dependencies are compatible

4. **Evaluation Errors**: Ensure test JSON files are valid

### Debug Mode

Run tests with verbose output:

```bash
pytest tests/ -v -s
```

## Links

- **Tutorial**: [Tutorial 10: Evaluation & Testing](../../../docs/tutorial/10_evaluation_testing.md)
- **ADK Documentation**: <https://google.github.io/adk-docs/>
- **Google AI Studio**: <https://aistudio.google.com/>

## Contributing

This implementation follows the patterns established in the ADK Training repository. For contributions:

1. Ensure all tests pass: `make test`
2. Add new test cases for new features
3. Update documentation for API changes
4. Follow the established code patterns

---

*This implementation demonstrates production-ready testing patterns for ADK agents, with 28 comprehensive tests covering unit testing, integration testing, and evaluation frameworks.*

