# ADK HTTP API Analysis

**Research Date**: 2025-01-08  
**Source**: `research/adk-python/src/google/adk/cli/adk_web_server.py` (v1.0+)  
**Purpose**: Document all available HTTP/WebSocket endpoints for UI integration

---

## Overview

The ADK (Agent Development Kit) provides a comprehensive REST API built on FastAPI for integrating agents into user interfaces. The API server can be started with:

```bash
adk api_server --agent-dir ./agents --web
```

Or programmatically:

```python
from google.adk.cli.fast_api import get_fast_api_app

app = get_fast_api_app(
    agent_dir="./agents",
    web=True,
    allow_origins=["*"]
)
```

---

## Core Integration Patterns

### 1. **Standard HTTP (Non-Streaming)**
- Endpoint: `POST /run`
- Returns: Complete list of events after agent execution
- Use Case: Simple request/response interfaces

### 2. **Server-Sent Events (SSE)**
- Endpoint: `POST /run_sse`
- Returns: Streaming events as they occur
- Use Case: Real-time UI updates, chat interfaces

### 3. **WebSocket (Bidirectional)**
- Endpoint: `WS /run_live`
- Returns: Real-time bidirectional communication
- Use Case: Voice interactions, streaming audio, complex multi-turn conversations

---

## Complete API Reference

### Agent Execution Endpoints

#### `POST /run`
Execute agent and return all events after completion.

**Request Body** (`RunAgentRequest`):
```json
{
  "app_name": "my_agent",
  "user_id": "user123",
  "session_id": "sess456",
  "new_message": {
    "role": "user",
    "parts": [{"text": "Hello"}]
  },
  "streaming": false,
  "state_delta": {"key": "value"},
  "invocation_id": "optional-id"
}
```

**Response**: Array of `Event` objects
```json
[
  {
    "id": "event1",
    "author": "assistant",
    "content": {
      "parts": [{"text": "Hello! How can I help?"}]
    },
    "actions": {
      "stateDelta": {"conversation_count": 1}
    }
  }
]
```

#### `POST /run_sse`
Stream agent execution events in real-time.

**Request Body**: Same as `/run`

**Response**: Server-Sent Events stream
```
data: {"id":"event1","author":"assistant","content":{"parts":[{"text":"Hello"}]}}

data: {"id":"event2","author":"assistant","content":{"parts":[{"text":" there!"}]}}
```

**Headers**:
- `Content-Type: text/event-stream`
- `Cache-Control: no-cache`
- `Connection: keep-alive`

#### `WS /run_live`
Bidirectional WebSocket communication for live interactions.

**Query Parameters**:
- `app_name`: Agent name
- `user_id`: User identifier
- `session_id`: Session identifier
- `modalities`: Array of `["TEXT", "AUDIO"]`

**Client → Server** (`LiveRequest`):
```json
{
  "type": "text" | "audio",
  "data": "message content" | "base64_audio",
  "end_of_turn": false
}
```

**Server → Client** (`Event`):
```json
{
  "id": "event1",
  "author": "assistant",
  "content": {
    "parts": [{"text": "Response"}]
  }
}
```

---

### Session Management

#### `POST /apps/{app_name}/users/{user_id}/sessions`
Create a new session.

**Request Body** (`CreateSessionRequest`):
```json
{
  "session_id": "optional-custom-id",
  "state": {"key": "initial_value"},
  "events": []
}
```

**Response**: `Session` object

#### `GET /apps/{app_name}/users/{user_id}/sessions/{session_id}`
Retrieve session details.

**Response**:
```json
{
  "id": "sess123",
  "app_name": "my_agent",
  "user_id": "user456",
  "state": {"conversation_count": 5},
  "events": [...],
  "creation_time": 1704067200
}
```

#### `GET /apps/{app_name}/users/{user_id}/sessions`
List all sessions for a user (excludes eval sessions).

**Response**: Array of `Session` objects

#### `DELETE /apps/{app_name}/users/{user_id}/sessions/{session_id}`
Delete a session.

#### `PATCH /apps/{app_name}/users/{user_id}/sessions/{session_id}`
Update session state without running agent.

**Request Body** (`UpdateSessionRequest`):
```json
{
  "state_delta": {"key": "new_value"}
}
```

---

### Artifact Management

#### `GET /apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts/{artifact_name}`
Load an artifact (image, file, etc.).

**Query Parameters**:
- `version`: Optional version number (default: latest)

**Response**: `Part` object (may contain inline_data or file_data)

#### `GET /apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts`
List all artifact names for a session.

**Response**: Array of strings

#### `GET /apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts/{artifact_name}/versions`
List all versions of an artifact.

**Response**: Array of integers

#### `DELETE /apps/{app_name}/users/{user_id}/sessions/{session_id}/artifacts/{artifact_name}`
Delete an artifact and all its versions.

---

### Memory Management

#### `PATCH /apps/{app_name}/users/{user_id}/memory`
Add session to memory service (for RAG/context).

**Request Body** (`UpdateMemoryRequest`):
```json
{
  "session_id": "sess123"
}
```

---

### Application Management

#### `GET /list-apps`
List all available agents.

**Response**: Array of agent names
```json
["agent1", "agent2", "chatbot"]
```

---

### Evaluation Endpoints (Testing/Quality)

#### `POST /apps/{app_name}/eval-sets`
Create an evaluation set.

#### `GET /apps/{app_name}/eval-sets`
List all evaluation sets.

#### `POST /apps/{app_name}/eval-sets/{eval_set_id}/add-session`
Add a session to an evaluation set for testing.

#### `POST /apps/{app_name}/eval-sets/{eval_set_id}/run`
Run evaluation metrics on test cases.

#### `GET /apps/{app_name}/eval-results/{eval_result_id}`
Get evaluation results.

#### `GET /apps/{app_name}/metrics-info`
List available evaluation metrics.

---

### Debug/Development Endpoints

#### `GET /debug/trace/{event_id}`
Get OpenTelemetry trace for an event.

**Response**: Trace attributes
```json
{
  "trace_id": 123456789,
  "span_id": 987654321,
  "gcp.vertex.agent.event_id": "event1",
  "attributes": {...}
}
```

#### `GET /debug/trace/session/{session_id}`
Get all traces for a session.

#### `GET /apps/{app_name}/users/{user_id}/sessions/{session_id}/events/{event_id}/graph`
Get agent execution graph for an event (Graphviz DOT format).

---

## Integration Architecture

### Service Configuration

When creating a FastAPI app, ADK supports multiple service backends:

1. **Session Service**
   - `InMemorySessionService` (development)
   - `DatabaseSessionService` (production with Cloud SQL)
   - `VertexAiSessionService` (Google Cloud Agent Engine)

2. **Artifact Service**
   - `InMemoryArtifactService` (development)
   - `GcsArtifactService` (production with Cloud Storage)

3. **Memory Service**
   - `InMemoryMemoryService` (development)
   - `VertexAiMemoryBankService` (production with Vertex AI)
   - `VertexAiRagMemoryService` (RAG with Vertex AI Search)

4. **Credential Service**
   - `InMemoryCredentialService` (stores API keys, OAuth tokens)

### CORS Configuration

For web UI integrations, enable CORS:

```python
app = get_fast_api_app(
    agent_dir="./agents",
    allow_origins=["http://localhost:3000", "https://myapp.com"]
)
```

### Authentication

ADK supports:
- **OAuth2** callback integration
- **API Keys** via credential service
- **Google Cloud IAM** for production deployments

### Observability

- **OpenTelemetry**: Built-in tracing with `trace_to_cloud` flag
- **Cloud Logging**: Automatic logging with `otel_to_cloud` flag
- **Custom Metrics**: Available via `/debug/trace/*` endpoints

---

## Integration Examples

### Example 1: Simple Chat (HTTP)

```python
import httpx

async def chat(message: str, session_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/run",
            json={
                "app_name": "chatbot",
                "user_id": "user123",
                "session_id": session_id,
                "new_message": {
                    "role": "user",
                    "parts": [{"text": message}]
                },
                "streaming": False
            }
        )
        events = response.json()
        return events[-1]["content"]["parts"][0]["text"]
```

### Example 2: Streaming Chat (SSE)

```python
import httpx

async def stream_chat(message: str, session_id: str):
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            "http://localhost:8000/run_sse",
            json={
                "app_name": "chatbot",
                "user_id": "user123",
                "session_id": session_id,
                "new_message": {
                    "role": "user",
                    "parts": [{"text": message}]
                },
                "streaming": True
            }
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data:"):
                    event_json = line[5:].strip()
                    if event_json:
                        event = json.loads(event_json)
                        if event.get("content"):
                            yield event["content"]["parts"][0]["text"]
```

### Example 3: WebSocket Live Chat

```python
import websockets
import json

async def live_chat(session_id: str):
    uri = f"ws://localhost:8000/run_live?app_name=chatbot&user_id=user123&session_id={session_id}"
    
    async with websockets.connect(uri) as websocket:
        # Send message
        await websocket.send(json.dumps({
            "type": "text",
            "data": "Hello!",
            "end_of_turn": True
        }))
        
        # Receive response
        async for message in websocket:
            event = json.loads(message)
            if event.get("content"):
                print(event["content"]["parts"][0]["text"])
```

---

## Key Findings for UI Integration

### ✅ **Strong Integration Points**

1. **RESTful API**: Complete CRUD operations for sessions, artifacts
2. **Multiple Streaming Options**: HTTP, SSE, WebSocket
3. **State Management**: Built-in session state with deltas
4. **Artifact Support**: File uploads/downloads (images, documents)
5. **Memory Integration**: RAG/context via memory service
6. **Production Ready**: GCS, Cloud SQL, Vertex AI backends
7. **CORS Support**: Easy web integration
8. **OpenTelemetry**: Built-in observability

### ⚠️ **Considerations**

1. **Authentication**: Requires custom implementation for OAuth2/API keys
2. **Rate Limiting**: Not built-in, needs middleware
3. **File Uploads**: Binary data via artifacts, not multipart/form-data
4. **Real-time**: WebSocket recommended for voice/audio
5. **Error Handling**: HTTP exceptions for 404/400/500

### 🎯 **Recommended Integration Patterns**

| Use Case | Endpoint | Protocol |
|----------|----------|----------|
| Simple Chatbot | `/run` | HTTP POST |
| Streaming Chat | `/run_sse` | SSE |
| Voice Assistant | `/run_live` | WebSocket |
| File Processing | `/artifacts/*` | HTTP GET/DELETE |
| Multi-Agent | `/run` + state_delta | HTTP POST |
| Analytics | `/debug/trace/*` | HTTP GET |

---

## Next Steps

1. ✅ **Completed**: Full ADK API documentation
2. ⏳ **Next**: Research AG-UI framework (found in search results!)
3. ⏳ **Next**: Research official Google ADK documentation
4. ⏳ **Next**: Web research for integration examples

---

## Additional Resources

- **Source Code**: `research/adk-python/src/google/adk/cli/adk_web_server.py`
- **FastAPI App**: `research/adk-python/src/google/adk/cli/fast_api.py`
- **Client Example**: `research/adk-python/src/google/adk/cli/conformance/adk_web_server_client.py`
- **Tutorial**: `tutorial/14_streaming_sse.md` (already written)
