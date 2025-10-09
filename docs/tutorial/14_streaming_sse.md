---
id: streaming_sse
title: "Tutorial 14: Streaming and Server-Sent Events (SSE) - Real-Time Responses"
description: "Build streaming agents that deliver real-time responses to users, perfect for chat interfaces and live updates using Server-Sent Events."
sidebar_label: "14. Streaming & SSE"
sidebar_position: 14
tags: ["advanced", "streaming", "sse", "real-time", "chat"]
keywords: ["streaming", "server-sent events", "real-time", "chat interface", "live updates"]
status: "draft"
difficulty: "advanced"
estimated_time: "1.5 hours"
prerequisites: ["Tutorial 01: Hello World Agent", "Tutorial 14: Code Execution", "Basic async/await knowledge"]
learning_objectives:
  - "Implement streaming agent responses"
  - "Configure Server-Sent Events (SSE) endpoints"
  - "Build real-time chat interfaces"
  - "Handle streaming errors and reconnection"
implementation_link: "https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial14"
---

# Tutorial 14: Streaming with Server-Sent Events (SSE)

**Goal**: Implement streaming responses using Server-Sent Events (SSE) to provide real-time, progressive output for better user experience in your AI agents.

**Prerequisites**:
- Tutorial 01 (Hello World Agent)
- Tutorial 02 (Function Tools)
- Basic understanding of async/await in Python

**What You'll Learn**:
- Understanding streaming vs. non-streaming responses
- Implementing SSE streaming with `StreamingMode.SSE`
- Using `RunConfig` for streaming configuration
- Building real-time chat interfaces
- Aggregating streaming responses
- Best practices for production streaming applications

**Time to Complete**: 45-60 minutes

---

## Why Streaming Matters

Traditional AI responses are **blocking** - users wait for the complete answer before seeing anything. Streaming provides **progressive output** as the model generates text.

**Without Streaming (Blocking)**:
```
User: "Explain quantum computing"
Agent: [5 seconds of waiting...]
       [Complete response appears at once]
```

**With Streaming (Progressive)**:
```
User: "Explain quantum computing"
Agent: "Quantum computing is a revolutionary..."
       [Text appears word-by-word or chunk-by-chunk]
       [User sees progress immediately]
```

**Benefits**:
- ✅ **Better UX**: Users see progress immediately
- ✅ **Perceived Speed**: Feels faster even if total time is similar
- ✅ **Early Feedback**: Users can interrupt if needed
- ✅ **Real-Time Feel**: More conversational and engaging
- ✅ **Long Responses**: Essential for lengthy outputs

---

## 1. Streaming Basics

### What is Server-Sent Events (SSE)?

**SSE** is a standard protocol for servers to push data to clients over HTTP. In ADK, `StreamingMode.SSE` enables the model to send response chunks as they're generated.

**Source**: `google/adk/agents/run_config.py`, `google/adk/models/google_llm.py`

### Basic Streaming Implementation

```python
import asyncio
from google.adk.agents import Agent, Runner, RunConfig, StreamingMode
from google.genai import types

# Create agent
agent = Agent(
    model='gemini-2.0-flash',
    name='streaming_assistant',
    instruction='Provide detailed, helpful responses.'
)

# Configure streaming
run_config = RunConfig(
    streaming_mode=StreamingMode.SSE
)

async def stream_response(query: str):
    """Stream agent response."""
    runner = Runner()
    
    print(f"User: {query}\n")
    print("Agent: ", end='', flush=True)
    
    # Run with streaming
    async for event in runner.run_async(
        query,
        agent=agent,
        run_config=run_config
    ):
        # Print each chunk as it arrives
        if event.content and event.content.parts:
            text = event.content.parts[0].text
            print(text, end='', flush=True)
    
    print("\n")

# Usage
asyncio.run(stream_response("Explain how neural networks work"))
```

**Output** (progressive):
```
User: Explain how neural networks work

Agent: Neural networks are computational models inspired by...
       [Text appears progressively as generated]
       ...the human brain. They consist of interconnected nodes...
       [Continues streaming...]
       ...making them powerful for pattern recognition tasks.
```

### How Streaming Works

**Internal Flow**:

1. **Request Sent** → Agent receives query with `StreamingMode.SSE`
2. **Model Generates** → Gemini starts generating response
3. **Chunks Emitted** → As text is generated, chunks are sent
4. **Events Yielded** → Each chunk wrapped in event object
5. **Client Receives** → Application receives progressive updates
6. **Complete** → Final event signals completion

**Implementation** (simplified from `google_llm.py`):

```python
# Simplified internal implementation
async def generate_content_async(self, request, streaming_mode):
    if streaming_mode == StreamingMode.SSE:
        # Stream mode
        async for chunk in self.model.generate_content_async(
            contents=request.messages,
            stream=True  # Enable streaming
        ):
            # Yield each chunk as event
            yield self._convert_to_event(chunk)
    else:
        # Non-streaming mode
        response = await self.model.generate_content_async(
            contents=request.messages,
            stream=False
        )
        yield self._convert_to_event(response)
```

---

## 2. StreamingMode Configuration

### Available Streaming Modes

```python
from google.adk.agents import StreamingMode

# SSE - Server-Sent Events (one-way streaming)
StreamingMode.SSE

# BIDI - Bidirectional streaming (two-way, for Live API)
StreamingMode.BIDI

# OFF - No streaming (default, blocking)
StreamingMode.OFF
```

### RunConfig Setup

```python
from google.adk.agents import RunConfig, StreamingMode

# SSE Streaming
sse_config = RunConfig(
    streaming_mode=StreamingMode.SSE
)

# No Streaming (blocking)
blocking_config = RunConfig(
    streaming_mode=StreamingMode.OFF
)

# Use in runner
runner = Runner()

# Streaming
async for event in runner.run_async(query, agent, run_config=sse_config):
    process_event(event)

# Blocking
result = await runner.run_async(query, agent, run_config=blocking_config)
process_complete_result(result)
```

---

## 3. Real-World Example: Interactive Chat Application

Let's build a production-ready streaming chat application.

### Complete Implementation

```python
"""
Streaming Chat Application with SSE
Real-time interactive chat with progressive responses.
"""

import asyncio
import os
from datetime import datetime
from typing import AsyncIterator
from google.adk.agents import Agent, Runner, RunConfig, StreamingMode, Session
from google.genai import types

# Environment setup
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = '1'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'your-project-id'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'


class StreamingChatApp:
    """Interactive streaming chat application."""
    
    def __init__(self):
        """Initialize chat application."""
        
        # Create chat agent
        self.agent = Agent(
            model='gemini-2.0-flash',
            name='chat_assistant',
            description='Helpful assistant with streaming responses',
            instruction="""
You are a helpful, friendly assistant engaging in natural conversation.

Guidelines:
- Be conversational and engaging
- Provide detailed explanations when asked
- Ask clarifying questions if needed
- Remember conversation context
- Be concise for simple queries, detailed for complex ones
            """.strip(),
            generate_content_config=types.GenerateContentConfig(
                temperature=0.7,  # Conversational
                max_output_tokens=2048
            )
        )
        
        # Create session for conversation context
        self.session = Session()
        
        # Configure streaming
        self.run_config = RunConfig(
            streaming_mode=StreamingMode.SSE
        )
        
        self.runner = Runner()
    
    async def stream_response(self, user_message: str) -> AsyncIterator[str]:
        """
        Stream agent response to user message.
        
        Args:
            user_message: User's input message
            
        Yields:
            Text chunks as they're generated
        """
        
        # Run agent with streaming
        async for event in self.runner.run_async(
            user_message,
            agent=self.agent,
            session=self.session,
            run_config=self.run_config
        ):
            # Extract text from event
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        yield part.text
    
    async def chat_turn(self, user_message: str):
        """
        Execute one chat turn with streaming display.
        
        Args:
            user_message: User's input message
        """
        
        # Display user message
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"\n[{timestamp}] User: {user_message}")
        
        # Display agent response with streaming
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] Agent: ", end='', flush=True)
        
        # Stream response chunks
        async for chunk in self.stream_response(user_message):
            print(chunk, end='', flush=True)
        
        print()  # New line after complete response
    
    async def run_interactive(self):
        """Run interactive chat loop."""
        
        print("="*70)
        print("STREAMING CHAT APPLICATION")
        print("="*70)
        print("Type 'exit' or 'quit' to end conversation")
        print("="*70)
        
        while True:
            try:
                # Get user input
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                # Check for exit
                if user_input.lower() in ['exit', 'quit']:
                    print("\nGoodbye!")
                    break
                
                # Process chat turn
                await self.chat_turn(user_input)
                
            except KeyboardInterrupt:
                print("\n\nInterrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}")
    
    async def run_demo(self):
        """Run demo conversation."""
        
        print("="*70)
        print("STREAMING CHAT DEMO")
        print("="*70)
        
        demo_messages = [
            "Hello! What can you help me with?",
            "Explain quantum computing in simple terms",
            "What are the practical applications?",
            "How does it compare to classical computing?"
        ]
        
        for message in demo_messages:
            await self.chat_turn(message)
            await asyncio.sleep(1)  # Pause between turns


async def main():
    """Main entry point."""
    
    chat = StreamingChatApp()
    
    # Run demo
    await chat.run_demo()
    
    # Uncomment for interactive mode:
    # await chat.run_interactive()


if __name__ == '__main__':
    asyncio.run(main())
```

### Expected Output

```
======================================================================
STREAMING CHAT DEMO
======================================================================

[14:23:15] User: Hello! What can you help me with?
[14:23:15] Agent: Hello! I'm here to help with a wide variety of tasks...
[Streams progressively...]
...I can explain concepts, answer questions, help with writing, assist 
with problem-solving, provide information on various topics, and much more. 
What would you like to explore today?

[14:23:18] User: Explain quantum computing in simple terms
[14:23:18] Agent: Imagine regular computers use bits, which are like...
[Streams progressively...]
...light switches that are either ON (1) or OFF (0). Quantum computers use 
quantum bits, or "qubits," which can be both ON and OFF at the same time...
[Continues streaming...]
...This allows quantum computers to explore many possibilities simultaneously, 
making them potentially much faster for certain types of problems.

[14:23:25] User: What are the practical applications?
[14:23:25] Agent: Great question! Here are some key applications...
[Streams progressively...]

1. **Drug Discovery**: Simulating molecular interactions...
2. **Cryptography**: Breaking current encryption and creating quantum-safe...
3. **Optimization**: Solving complex logistics and scheduling...
4. **Financial Modeling**: Analyzing risk and portfolio optimization...
5. **Artificial Intelligence**: Training more sophisticated ML models...

[14:23:32] User: How does it compare to classical computing?
[14:23:32] Agent: Let me break down the key differences...
[Streams progressively...]

**Classical Computing:**
- Sequential processing (one calculation at a time)
- Deterministic (same input → same output)
- Excellent for everyday tasks...

**Quantum Computing:**
- Parallel exploration (many paths simultaneously)
- Probabilistic (results have probabilities)
- Excels at specific complex problems...

Think of it this way: a classical computer is like checking...
```

---

## 4. Advanced Streaming Patterns

### Pattern 1: Response Aggregation

Collect the complete response while streaming:

```python
from typing import List

async def stream_and_aggregate(query: str, agent: Agent) -> tuple[str, List[str]]:
    """
    Stream response while collecting chunks.
    
    Returns:
        (complete_text, chunks_list)
    """
    
    runner = Runner()
    run_config = RunConfig(streaming_mode=StreamingMode.SSE)
    
    chunks = []
    
    async for event in runner.run_async(query, agent=agent, run_config=run_config):
        if event.content and event.content.parts:
            chunk = event.content.parts[0].text
            chunks.append(chunk)
            print(chunk, end='', flush=True)
    
    complete_text = ''.join(chunks)
    return complete_text, chunks


# Usage
complete, chunks = await stream_and_aggregate(
    "Explain machine learning",
    agent
)

print(f"\n\nTotal chunks: {len(chunks)}")
print(f"Total length: {len(complete)} characters")
```

### Pattern 2: Streaming with Progress Indicators

Show progress during streaming:

```python
import sys

async def stream_with_progress(query: str, agent: Agent):
    """Stream with visual progress indicator."""
    
    runner = Runner()
    run_config = RunConfig(streaming_mode=StreamingMode.SSE)
    
    print("Agent: ", end='', flush=True)
    
    chunk_count = 0
    
    async for event in runner.run_async(query, agent=agent, run_config=run_config):
        if event.content and event.content.parts:
            chunk = event.content.parts[0].text
            print(chunk, end='', flush=True)
            
            chunk_count += 1
            
            # Show progress indicator every 10 chunks
            if chunk_count % 10 == 0:
                sys.stderr.write('.')
                sys.stderr.flush()
    
    print()  # New line


# Usage
await stream_with_progress("Write a long essay on AI", agent)
```

### Pattern 3: Streaming to Multiple Outputs

Send streaming response to multiple destinations:

```python
from typing import List, Callable

async def stream_to_multiple(
    query: str,
    agent: Agent,
    outputs: List[Callable[[str], None]]
):
    """
    Stream response to multiple output handlers.
    
    Args:
        query: User query
        agent: Agent to use
        outputs: List of functions to handle each chunk
    """
    
    runner = Runner()
    run_config = RunConfig(streaming_mode=StreamingMode.SSE)
    
    async for event in runner.run_async(query, agent=agent, run_config=run_config):
        if event.content and event.content.parts:
            chunk = event.content.parts[0].text
            
            # Send to all outputs
            for output_fn in outputs:
                output_fn(chunk)


# Usage
async def console_output(chunk: str):
    print(chunk, end='', flush=True)

async def file_output(chunk: str):
    with open('response.txt', 'a') as f:
        f.write(chunk)

async def websocket_output(chunk: str):
    # await websocket.send(chunk)
    pass

await stream_to_multiple(
    "Explain AI safety",
    agent,
    outputs=[console_output, file_output, websocket_output]
)
```

### Pattern 4: Streaming with Timeout

Add timeout protection:

```python
import asyncio

async def stream_with_timeout(
    query: str,
    agent: Agent,
    timeout_seconds: float = 30.0
):
    """Stream response with timeout."""
    
    runner = Runner()
    run_config = RunConfig(streaming_mode=StreamingMode.SSE)
    
    try:
        async with asyncio.timeout(timeout_seconds):
            async for event in runner.run_async(query, agent=agent, run_config=run_config):
                if event.content and event.content.parts:
                    chunk = event.content.parts[0].text
                    print(chunk, end='', flush=True)
    except asyncio.TimeoutError:
        print("\n\n[Timeout: Response took too long]")
    
    print()


# Usage
await stream_with_timeout("Explain the universe", agent, timeout_seconds=10.0)
```

---

## 5. StreamingResponseAggregator

ADK provides `StreamingResponseAggregator` for handling streaming responses:

```python
from google.adk.models.streaming_response_aggregator import StreamingResponseAggregator

async def stream_with_aggregator(query: str, agent: Agent):
    """Use StreamingResponseAggregator for cleaner code."""
    
    runner = Runner()
    run_config = RunConfig(streaming_mode=StreamingMode.SSE)
    
    aggregator = StreamingResponseAggregator()
    
    async for event in runner.run_async(query, agent=agent, run_config=run_config):
        # Aggregator handles chunk collection
        aggregator.add(event)
        
        # Display chunk
        if event.content and event.content.parts:
            print(event.content.parts[0].text, end='', flush=True)
    
    # Get complete response
    complete_response = aggregator.get_response()
    
    print(f"\n\nComplete response has {len(complete_response.content.parts[0].text)} characters")
    
    return complete_response


# Usage
response = await stream_with_aggregator("Explain blockchain", agent)
```

---

## 6. Building Web APIs with Streaming

### FastAPI SSE Endpoint

```python
"""
FastAPI endpoint with SSE streaming.
"""

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from google.adk.agents import Agent, Runner, RunConfig, StreamingMode
from google.adk.cli.adk_web_server import AdkWebServer
import json

app = FastAPI()

# Create agent
agent = Agent(
    model='gemini-2.0-flash',
    name='api_assistant'
)

runner = Runner()


async def generate_stream(query: str):
    """Generate SSE stream."""
    
    run_config = RunConfig(streaming_mode=StreamingMode.SSE)
    
    async for event in runner.run_async(query, agent=agent, run_config=run_config):
        if event.content and event.content.parts:
            # Format as SSE
            chunk = event.content.parts[0].text
            data = json.dumps({'text': chunk})
            yield f"data: {data}\n\n"
    
    # Send completion signal
    yield "data: [DONE]\n\n"


@app.post("/chat/stream")
async def chat_stream(query: str):
    """Streaming chat endpoint."""
    
    return StreamingResponse(
        generate_stream(query),
        media_type="text/event-stream"
    )


# Usage with ADK web server
if __name__ == '__main__':
    # adk api_server automatically sets up streaming endpoints
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Client-Side JavaScript

```javascript
// Connect to SSE endpoint
const eventSource = new EventSource('http://localhost:8000/chat/stream?query=Hello');

eventSource.onmessage = (event) => {
    if (event.data === '[DONE]') {
        eventSource.close();
        return;
    }
    
    const data = JSON.parse(event.data);
    // Display chunk in UI
    document.getElementById('response').innerHTML += data.text;
};

eventSource.onerror = (error) => {
    console.error('SSE Error:', error);
    eventSource.close();
};
```

---

## 7. Best Practices

### ✅ DO: Use Streaming for Long Responses

```python
# ✅ Good - Stream long responses
run_config = RunConfig(streaming_mode=StreamingMode.SSE)

async for event in runner.run_async(
    "Write a detailed essay on climate change",
    agent=agent,
    run_config=run_config
):
    display_chunk(event)

# ❌ Bad - Blocking for long response
result = runner.run(
    "Write a detailed essay on climate change",
    agent=agent
)
# User waits 10+ seconds for complete response
```

### ✅ DO: Handle Async Properly

```python
# ✅ Good - Proper async handling
async def handle_stream():
    async for event in runner.run_async(...):
        await process_event(event)

asyncio.run(handle_stream())

# ❌ Bad - Blocking in async context
async def handle_stream():
    result = runner.run(...)  # Blocks async loop
```

### ✅ DO: Flush Output Immediately

```python
# ✅ Good - Flush for immediate display
print(chunk, end='', flush=True)

# ❌ Bad - Buffered output (delayed display)
print(chunk, end='')  # No flush
```

### ✅ DO: Handle Streaming Errors

```python
# ✅ Good - Error handling
async def safe_stream(query, agent):
    try:
        run_config = RunConfig(streaming_mode=StreamingMode.SSE)
        
        async for event in runner.run_async(query, agent=agent, run_config=run_config):
            if event.content and event.content.parts:
                print(event.content.parts[0].text, end='', flush=True)
    
    except Exception as e:
        print(f"\n[Error during streaming: {e}]")

# ❌ Bad - No error handling
async for event in runner.run_async(...):
    print(event.content.parts[0].text)  # Crashes on error
```

### ✅ DO: Use Sessions for Context

```python
# ✅ Good - Session maintains conversation context
session = Session()

for message in conversation:
    async for event in runner.run_async(
        message,
        agent=agent,
        session=session,  # Context preserved
        run_config=run_config
    ):
        process_event(event)

# ❌ Bad - No session (loses context)
for message in conversation:
    async for event in runner.run_async(message, agent=agent, run_config=run_config):
        process_event(event)
```

---

## 8. Troubleshooting

### Issue: "No streaming happening"

**Problem**: Response appears all at once instead of streaming

**Solutions**:

1. **Verify RunConfig**:
```python
# ❌ Missing or wrong config
runner.run_async(query, agent=agent)  # No streaming

# ✅ Correct config
run_config = RunConfig(streaming_mode=StreamingMode.SSE)
runner.run_async(query, agent=agent, run_config=run_config)
```

2. **Use run_async, not run**:
```python
# ❌ Blocking call
result = runner.run(query, agent=agent, run_config=run_config)

# ✅ Async streaming call
async for event in runner.run_async(query, agent=agent, run_config=run_config):
    ...
```

3. **Check output flushing**:
```python
# ❌ Buffered (appears in chunks)
print(chunk, end='')

# ✅ Flushed immediately
print(chunk, end='', flush=True)
```

### Issue: "Slow streaming performance"

**Problem**: Long delays between chunks

**Solutions**:

1. **Reduce output tokens**:
```python
agent = Agent(
    model='gemini-2.0-flash',
    generate_content_config=types.GenerateContentConfig(
        max_output_tokens=1024  # Shorter responses
    )
)
```

2. **Use faster model**:
```python
# ✅ Flash for speed
agent = Agent(model='gemini-2.0-flash')

# ❌ Pro is slower
agent = Agent(model='gemini-2.0-pro')
```

### Issue: "Memory building up with long streams"

**Problem**: Memory consumption increases during long streaming sessions

**Solution**: Process and discard chunks:
```python
# ✅ Process chunks without accumulating
async for event in runner.run_async(query, agent=agent, run_config=run_config):
    chunk = event.content.parts[0].text
    
    # Process immediately
    display(chunk)
    save_to_db(chunk)
    
    # Don't accumulate in memory
    # No: all_chunks.append(chunk)
```

---

## 9. Testing Streaming Agents

### Unit Tests

```python
import pytest
from google.adk.agents import Agent, Runner, RunConfig, StreamingMode

@pytest.mark.asyncio
async def test_streaming_response():
    """Test that streaming returns multiple chunks."""
    
    agent = Agent(
        model='gemini-2.0-flash',
        instruction='Provide detailed responses.'
    )
    
    runner = Runner()
    run_config = RunConfig(streaming_mode=StreamingMode.SSE)
    
    chunks = []
    
    async for event in runner.run_async(
        "Explain machine learning in detail",
        agent=agent,
        run_config=run_config
    ):
        if event.content and event.content.parts:
            chunks.append(event.content.parts[0].text)
    
    # Should receive multiple chunks
    assert len(chunks) > 1
    
    # Complete text should be reasonable length
    complete = ''.join(chunks)
    assert len(complete) > 100


@pytest.mark.asyncio
async def test_streaming_aggregation():
    """Test that streaming chunks combine correctly."""
    
    agent = Agent(model='gemini-2.0-flash')
    runner = Runner()
    run_config = RunConfig(streaming_mode=StreamingMode.SSE)
    
    chunks = []
    
    async for event in runner.run_async(
        "Count to 10",
        agent=agent,
        run_config=run_config
    ):
        if event.content and event.content.parts:
            chunks.append(event.content.parts[0].text)
    
    complete = ''.join(chunks)
    
    # Should contain all numbers
    for i in range(1, 11):
        assert str(i) in complete
```

---

## Summary

You've mastered streaming responses with SSE:

**Key Takeaways**:
- ✅ `StreamingMode.SSE` enables progressive response output
- ✅ Use `RunConfig` to configure streaming
- ✅ `runner.run_async()` with `async for` for streaming
- ✅ Better UX - users see progress immediately
- ✅ Essential for long responses and real-time applications
- ✅ Works with sessions for conversation context
- ✅ Can combine with tools and code execution
- ✅ `flush=True` for immediate terminal output

**Production Checklist**:
- [ ] Using `RunConfig(streaming_mode=StreamingMode.SSE)`
- [ ] Proper async/await handling
- [ ] Error handling for streaming failures
- [ ] Session management for context
- [ ] Output flushing (`flush=True`)
- [ ] Timeout protection for long streams
- [ ] Testing streaming with multiple queries
- [ ] Monitoring chunk sizes and latency

**Next Steps**:
- **Tutorial 15**: Learn Live API for bidirectional streaming with audio
- **Tutorial 16**: Explore MCP Integration for extended tool ecosystem
- **Tutorial 17**: Implement Agent-to-Agent (A2A) communication

**Resources**:
- [ADK Streaming Docs](https://google.github.io/adk-docs/streaming/)
- [Server-Sent Events Standard](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [FastAPI SSE](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse)

---

**🎉 Tutorial 14 Complete!** You now know how to implement streaming responses for better user experience. Continue to Tutorial 15 to learn about bidirectional streaming with the Live API.
