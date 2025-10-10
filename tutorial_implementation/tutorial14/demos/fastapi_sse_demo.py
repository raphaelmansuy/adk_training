"""
FastAPI SSE Endpoint Demo - Tutorial 14

Demonstrates building web APIs with streaming Server-Sent Events (SSE).
"""

import asyncio
import os
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Environment setup
os.environ.setdefault('GOOGLE_GENAI_USE_VERTEXAI', 'FALSE')

# Create FastAPI app
app = FastAPI(title="Streaming Chat API", description="ADK Streaming Chat API with SSE")

# Create agent (global for demo)
agent = Agent(
    model='gemini-2.0-flash',
    name='api_assistant',
    instruction='You are a helpful API assistant. Provide clear, concise responses.'
)

# Global runner and session service
session_service = InMemorySessionService()
runner = Runner(app_name="fastapi_demo", agent=agent, session_service=session_service)


async def generate_stream(query: str):
    """
    Generate SSE stream for a query.

    Args:
        query: User query

    Yields:
        SSE formatted data chunks
    """
    # Create session for this request
    session = await session_service.create_session(
        app_name="fastapi_demo",
        user_id=f"api_user_{hash(query) % 10000}"  # Simple user ID
    )

    run_config = RunConfig(streaming_mode=StreamingMode.SSE)

    try:
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=types.Content(role="user", parts=[types.Part(text=query)]),
            run_config=run_config
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        # Format as SSE
                        chunk = part.text
                        data = json.dumps({'text': chunk, 'type': 'chunk'})
                        yield f"data: {data}\n\n"

            if event.turn_complete:
                break

        # Send completion signal
        completion_data = json.dumps({'type': 'done', 'message': 'Response complete'})
        yield f"data: {completion_data}\n\n"

    except Exception as e:
        # Send error signal
        error_data = json.dumps({'type': 'error', 'message': str(e)})
        yield f"data: {error_data}\n\n"


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Streaming Chat API", "endpoints": ["/chat/stream", "/docs"]}


@app.post("/chat/stream")
async def chat_stream(query: str):
    """
    Streaming chat endpoint.

    Args:
        query: User's question

    Returns:
        StreamingResponse with SSE
    """
    return StreamingResponse(
        generate_stream(query),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
        }
    )


@app.get("/chat/stream")
async def chat_stream_get(query: str):
    """
    GET version of streaming chat endpoint for browser testing.

    Args:
        query: User's question

    Returns:
        StreamingResponse with SSE
    """
    return StreamingResponse(
        generate_stream(query),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
        }
    )


# Client-side JavaScript for testing
CLIENT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Streaming Chat Client</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        #messages { border: 1px solid #ccc; padding: 10px; height: 300px; overflow-y: auto; }
        #input { width: 300px; padding: 5px; }
        button { padding: 5px 10px; }
    </style>
</head>
<body>
    <h1>Streaming Chat Client</h1>
    <div id="messages"></div>
    <br>
    <input type="text" id="input" placeholder="Ask a question...">
    <button onclick="sendMessage()">Send</button>

    <script>
        const messages = document.getElementById('messages');
        const input = document.getElementById('input');
        let eventSource = null;

        function sendMessage() {
            const query = input.value.trim();
            if (!query) return;

            // Close existing connection
            if (eventSource) {
                eventSource.close();
            }

            // Clear previous messages
            messages.innerHTML = '';

            // Add user message
            addMessage('You', query);

            // Start new SSE connection
            eventSource = new EventSource(`/chat/stream?query=${encodeURIComponent(query)}`);

            eventSource.onmessage = (event) => {
                if (event.data === "[DONE]") {
                    eventSource.close();
                    return;
                }

                try {
                    const data = JSON.parse(event.data);
                    if (data.type === 'chunk') {
                        addToAgentMessage(data.text);
                    } else if (data.type === 'done') {
                        // Response complete
                    } else if (data.type === 'error') {
                        addMessage('Error', data.message);
                    }
                } catch (e) {
                    console.error('Parse error:', e);
                }
            };

            eventSource.onerror = (error) => {
                console.error('SSE Error:', error);
                addMessage('Error', 'Connection failed');
                eventSource.close();
            };

            input.value = '';
        }

        function addMessage(sender, text) {
            const div = document.createElement('div');
            div.innerHTML = `<strong>${sender}:</strong> ${text}`;
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }

        function addToAgentMessage(text) {
            let agentDiv = messages.querySelector('.agent-message');
            if (!agentDiv) {
                agentDiv = document.createElement('div');
                agentDiv.className = 'agent-message';
                agentDiv.innerHTML = '<strong>Agent:</strong> ';
                messages.appendChild(agentDiv);
            }
            agentDiv.innerHTML += text;
            messages.scrollTop = messages.scrollHeight;
        }

        // Send message on Enter key
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
"""


@app.get("/client")
async def client_page():
    """Serve the client HTML page."""
    from fastapi.responses import HTMLResponse
    return HTMLResponse(content=CLIENT_HTML)


async def demo_server():
    """
    Demo function to show how the API works.
    This would normally be run with: uvicorn fastapi_sse_demo:app --reload
    """
    print("=" * 70)
    print("FASTAPI SSE ENDPOINT DEMO")
    print("=" * 70)
    print("This demo shows how to create streaming SSE endpoints with FastAPI.")
    print("\nTo run the server:")
    print("  uvicorn demos.fastapi_sse_demo:app --reload")
    print("\nThen visit:")
    print("  http://localhost:8000/docs    - API documentation")
    print("  http://localhost:8000/client  - Test client")
    print("\nOr test directly:")
    print("  curl \"http://localhost:8000/chat/stream?query=Hello\"")
    print("=" * 70)


if __name__ == '__main__':
    # Run demo instead of server
    asyncio.run(demo_server())