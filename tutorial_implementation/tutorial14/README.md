# Tutorial 14: Streaming Agent with Server-Sent Events (SSE)

This implementation demonstrates real streaming responses using Google ADK
v1.16.0's actual streaming APIs, providing progressive text output for better
user experience.

## Overview

The streaming agent demonstrates how to implement progressive text output where responses appear as they're generated, simulating the streaming behavior that would be used in real-time chat interfaces.

## Features

- **Real ADK Streaming**: Uses Google ADK v1.16.0's actual streaming APIs with `Runner.run_async()`
- **Server-Sent Events**: SSE streaming with `StreamingMode.SSE` for real-time responses
- **Session Management**: Proper conversation context with `InMemorySessionService`
- **Tool Integration**: Additional utilities for streaming analysis
- **Comprehensive Testing**: Full test coverage for all functionality
- **Demo Scripts**: Multiple working examples from the tutorial
- **Web API Examples**: FastAPI SSE endpoints with client code
- **Advanced Patterns**: Aggregation, progress indicators, multiple outputs, timeout handling

## Quick Start

1. **Setup Environment**:
   ```bash
   make setup
   ```

2. **Run Tests**:
   ```bash
   make test
   ```

3. **Run Demo**:
   ```bash
   make demo
   ```

## Project Structure

```
tutorial14/
├── streaming_agent/           # Main agent package
│   ├── __init__.py           # Package exports
│   ├── agent.py              # Agent implementation
│   └── .env.example          # Environment template
├── demos/                    # Working demo scripts from tutorial
│   ├── basic_streaming_demo.py         # Basic streaming example
│   ├── streaming_modes_demo.py         # StreamingMode configurations
│   ├── streaming_chat_app.py           # Complete chat application
│   ├── advanced_patterns_demo.py       # 4 advanced streaming patterns
│   ├── streaming_aggregator_demo.py    # Response aggregation
│   ├── fastapi_sse_demo.py             # FastAPI SSE endpoint
│   ├── sse_client.html                 # Client-side JavaScript
│   └── streaming_tests_demo.py         # Comprehensive tests
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_agent.py         # Agent functionality tests
│   ├── test_imports.py       # Import validation tests
│   └── test_structure.py     # Project structure tests
├── pyproject.toml            # Modern Python packaging
├── requirements.txt          # Dependencies
├── Makefile                 # Development commands
└── README.md                # This file
```

## Key Components

### Agent Configuration

The `root_agent` is configured with:
- **Model**: `gemini-2.0-flash` for fast responses
- **Tools**: `format_streaming_info` and `analyze_streaming_performance`

### Streaming Functions

- `stream_agent_response()`: Core streaming function using real ADK APIs with fallback to simulation
- `get_complete_response()`: Non-streaming version for testing
- `create_demo_session()`: Placeholder for session management

### Tools

1. **format_streaming_info**: Provides information about streaming capabilities
2. **analyze_streaming_performance**: Analyzes streaming performance characteristics

## Demo Scripts

All code snippets and examples from the tutorial documentation have been implemented as working demo scripts:

### 1. Basic Streaming Demo (`demos/basic_streaming_demo.py`)

Demonstrates the fundamental streaming implementation using ADK's real APIs:

```bash
python demos/basic_streaming_demo.py
```

Features:
- Basic `Runner.run_async()` usage
- Proper session management
- Progressive text output
- Multiple demo queries

### 2. Streaming Modes Demo (`demos/streaming_modes_demo.py`)

Shows different `StreamingMode` configurations:

```bash
python demos/streaming_modes_demo.py
```

Demonstrates:
- `StreamingMode.SSE` for Server-Sent Events
- `StreamingMode.NONE` for blocking responses
- Configuration differences and usage patterns

### 3. Streaming Chat Application (`demos/streaming_chat_app.py`)

Complete interactive chat application from the tutorial:

```bash
# Interactive mode
python demos/streaming_chat_app.py

# Or modify the script to run demo mode
```

Features:
- `StreamingChatApp` class with session management
- Interactive and demo conversation modes
- Real-time streaming display
- Error handling and graceful shutdown

### 4. Advanced Patterns Demo (`demos/advanced_patterns_demo.py`)

Implements all 4 advanced streaming patterns:

```bash
python demos/advanced_patterns_demo.py
```

Patterns demonstrated:
- **Response Aggregation**: Collecting complete responses while streaming
- **Progress Indicators**: Visual feedback during streaming
- **Multiple Outputs**: Sending chunks to multiple destinations simultaneously
- **Timeout Protection**: Handling slow responses gracefully

### 5. Streaming Aggregator Demo (`demos/streaming_aggregator_demo.py`)

Shows response aggregation techniques:

```bash
python demos/streaming_aggregator_demo.py
```

Features:
- Manual aggregation implementation
- Chunk analysis and statistics
- Complete response reconstruction

### 6. FastAPI SSE Demo (`demos/fastapi_sse_demo.py`)

Web API with Server-Sent Events streaming:

```bash
# Install FastAPI if needed
pip install fastapi uvicorn

# Run the server
uvicorn demos.fastapi_sse_demo:app --reload

# Visit in browser:
# http://localhost:8000/docs     - API documentation
# http://localhost:8000/client   - Test client interface
```

Features:
- FastAPI `StreamingResponse` with SSE
- RESTful chat endpoints
- Built-in HTML test client
- CORS headers for web applications

### 7. SSE Client (`demos/sse_client.html`)

Client-side JavaScript for testing SSE endpoints:

```bash
# Open in browser or serve with a web server
python -m http.server 8080
# Then visit: http://localhost:8080/demos/sse_client.html
```

Features:
- Real-time SSE connection handling
- Progressive message display
- Error handling and reconnection
- Clean, responsive UI

### 8. Comprehensive Tests (`demos/streaming_tests_demo.py`)

Unit tests demonstrating testing patterns for streaming:

```bash
python -m pytest demos/streaming_tests_demo.py -v
```

Test coverage:
- Basic streaming functionality
- Different streaming modes
- Error handling and timeouts
- Concurrent session testing
- FastAPI endpoint mocking

## Usage Examples

### Basic Streaming

```python
from streaming_agent import stream_agent_response

async def chat():
    print("User: Hello!")
    print("Agent: ", end="", flush=True)

    async for chunk in stream_agent_response("Hello!"):
        print(chunk, end="", flush=True)

    print()
```

### Complete Response

```python
from streaming_agent import get_complete_response

response = await get_complete_response("Explain quantum computing")
print(response)
```

## Testing

Run the comprehensive test suite:

```bash
make test
```

Tests cover:
- Agent configuration and creation
- Streaming functionality simulation
- Tool function behavior
- Import validation
- Project structure compliance

## Development

### Available Make Commands

- `make setup` - Install dependencies and package
- `make test` - Run test suite
- `make demo` - Run streaming demo
- `make clean` - Remove cache files

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=streaming_agent --cov-report=html

# Run specific test file
pytest tests/test_agent.py
```

## API Reference

### Core Functions

#### `stream_agent_response(query)`

Stream agent response for a query (simulated).

**Parameters:**
- `query` (str): User query

**Returns:** AsyncIterator[str] - Text chunks

#### `get_complete_response(query)`

Get complete response (non-streaming).

**Parameters:**
- `query` (str): User query

**Returns:** str - Complete response text

#### `create_demo_session()`

Create a new session placeholder.

**Returns:** None

### Tools

#### `format_streaming_info()`

Get information about streaming capabilities.

**Returns:** Dict with streaming information

#### `analyze_streaming_performance(query_length=100)`

Analyze streaming performance characteristics.

**Parameters:**
- `query_length` (int): Length of query for analysis

**Returns:** Dict with performance analysis

## Implementation Notes

This implementation uses Google ADK v1.16.0's real streaming APIs:

- **Real Streaming APIs**: Uses `Runner.run_async()` with `StreamingMode.SSE` for actual progressive output
- **Session Management**: Proper conversation context with `InMemorySessionService`
- **Fallback Mechanism**: Falls back to simulated streaming if real streaming fails
- **Educational Focus**: Demonstrates both real and fallback streaming patterns
- **Testable**: Easy to test with mocked ADK components

## Related Tutorials

- **Tutorial 01**: Hello World Agent - Basic agent setup
- **Tutorial 02**: Function Tools - Tool integration
- **Tutorial 13**: Code Execution - Advanced agent patterns

## Contributing

1. Follow the testing patterns in `tests/`
2. Add new functionality with corresponding tests
3. Update documentation for any changes
4. Ensure all tests pass before submitting

## License

This implementation is part of the ADK Training repository.