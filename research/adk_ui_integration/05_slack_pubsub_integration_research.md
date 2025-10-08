# Slack & Google Cloud Pub/Sub Integration Research

**Research Date**: 2025-10-08  
**Sources**:
- Slack Bolt SDK documentation  
- Google Cloud Pub/Sub documentation
- ADK API analysis

---

## Part 1: Slack Integration

### Overview

Integrating ADK agents with Slack creates conversational AI assistants within team workspaces. Slack Bot integration uses the **Slack Bolt framework** (Python) and ADK's native API.

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Slack Workspace                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  User Messages (@bot or DM)                        │  │
│  └───────────────┬───────────────────────────────────┘  │
└──────────────────┼─────────────────────────────────────┘
                   │ Slack Events API (HTTP POST)
                   ▼
┌─────────────────────────────────────────────────────────┐
│  Slack Bot Server (Python)                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Slack Bolt Framework                              │  │
│  │  @app.event("message")                             │  │
│  │  @app.event("app_mention")                         │  │
│  └───────────────┬───────────────────────────────────┘  │
│                  │                                        │
│  ┌───────────────▼───────────────────────────────────┐  │
│  │  Google ADK Agent                                  │  │
│  │  - Direct Python integration                       │  │
│  │  - Session per Slack thread                        │  │
│  └─────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
                   │
                   ▼ Slack Web API
┌─────────────────────────────────────────────────────────┐
│  Post messages back to Slack                             │
│  - chat.postMessage                                      │
│  - Threaded replies                                      │
│  - Rich formatting (blocks)                              │
└─────────────────────────────────────────────────────────┘
```

---

### Implementation

#### Project Structure

```
slack-adk-bot/
├── bot.py                    # Main bot application
├── agents/
│   ├── __init__.py
│   └── assistant.py          # ADK agent definition
├── requirements.txt
├── .env                      # Slack tokens + GOOGLE_API_KEY
└── README.md
```

#### Step 1: Slack App Setup

1. **Create Slack App** at https://api.slack.com/apps
2. **Enable Socket Mode** (for local development) or **Event Subscriptions** (production)
3. **Bot Token Scopes**:
   - `app_mentions:read`
   - `chat:write`
   - `im:history`
   - `im:read`
   - `im:write`
4. **Subscribe to Events**:
   - `app_mention`
   - `message.im`
5. **Install to Workspace** and copy tokens:
   - `SLACK_BOT_TOKEN` (xoxb-...)
   - `SLACK_APP_TOKEN` (xapp-...)

#### Step 2: Agent Definition

**agents/assistant.py**:

```python
from google.adk.agents import LlmAgent
from google.adk.tools import tool

@tool
def get_team_info(team_id: str) -> dict:
    """Get information about a team member."""
    # Mock data - replace with real lookup
    return {
        "name": "John Doe",
        "role": "Engineer",
        "email": "john@example.com"
    }

def create_agent():
    """Factory function to create ADK agent."""
    return LlmAgent(
        name="slack_assistant",
        model="gemini-2.0-flash",
        instruction="""You are a helpful Slack assistant.
        Keep responses concise and use Slack-friendly formatting.
        Use bullet points and emojis where appropriate.""",
        tools=[get_team_info]
    )
```

#### Step 3: Slack Bot Implementation

**bot.py**:

```python
import os
import re
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from google.adk.agents import Runner, Session
from agents.assistant import create_agent
from dotenv import load_dotenv

load_dotenv()

# Initialize Slack app
app = App(token=os.environ["SLACK_BOT_TOKEN"])

# Initialize ADK components
agent = create_agent()
runner = Runner()

# Store sessions per thread
sessions = {}

def get_or_create_session(thread_ts: str, channel: str) -> Session:
    """Get existing session or create new one for Slack thread."""
    session_key = f"{channel}:{thread_ts}"
    
    if session_key not in sessions:
        sessions[session_key] = Session()
        sessions[session_key].state["channel"] = channel
        sessions[session_key].state["thread_ts"] = thread_ts
    
    return sessions[session_key]

@app.event("app_mention")
def handle_mention(event, say, logger):
    """Handle @bot mentions in channels."""
    try:
        # Extract message and metadata
        text = event["text"]
        channel = event["channel"]
        user = event["user"]
        thread_ts = event.get("thread_ts", event["ts"])
        
        # Remove bot mention from text
        text = re.sub(r"<@\w+>", "", text).strip()
        
        # Get or create session for this thread
        session = get_or_create_session(thread_ts, channel)
        
        # Post "thinking" message
        thinking_response = say(
            text="🤔 Thinking...",
            thread_ts=thread_ts
        )
        
        # Run agent
        result = runner.run(
            text,
            agent=agent,
            session=session
        )
        response_text = result.content.parts[0].text
        
        # Update message with actual response
        app.client.chat_update(
            channel=channel,
            ts=thinking_response["ts"],
            text=response_text,
            thread_ts=thread_ts
        )
        
    except Exception as e:
        logger.error(f"Error handling mention: {e}")
        say(
            text=f"❌ Sorry, I encountered an error: {str(e)}",
            thread_ts=thread_ts
        )

@app.event("message")
def handle_direct_message(event, say, logger):
    """Handle direct messages to bot."""
    # Ignore bot's own messages
    if event.get("bot_id"):
        return
    
    # Only handle DMs (im channel type)
    if event.get("channel_type") != "im":
        return
    
    try:
        text = event["text"]
        channel = event["channel"]
        thread_ts = event.get("thread_ts", event["ts"])
        
        # Get or create session
        session = get_or_create_session(thread_ts, channel)
        
        # Show typing indicator
        app.client.chat_postMessage(
            channel=channel,
            text="🤔 Thinking...",
            thread_ts=thread_ts
        )
        
        # Run agent
        result = runner.run(
            text,
            agent=agent,
            session=session
        )
        response_text = result.content.parts[0].text
        
        # Send response
        say(text=response_text, thread_ts=thread_ts)
        
    except Exception as e:
        logger.error(f"Error handling DM: {e}")
        say(
            text=f"❌ Sorry, I encountered an error: {str(e)}",
            thread_ts=thread_ts
        )

# Start bot
if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    print("⚡️ Slack bot is running!")
    handler.start()
```

#### Step 4: Requirements

**requirements.txt**:

```txt
slack-bolt>=1.18.0
google-adk>=1.0.0
python-dotenv>=1.0.0
```

#### Step 5: Environment Variables

**.env**:

```bash
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
GOOGLE_API_KEY=your-gemini-api-key
```

#### Step 6: Run the Bot

```bash
pip install -r requirements.txt
python bot.py
```

---

### Advanced Features

#### 1. Rich Slack Blocks

**bot.py** (with rich formatting):

```python
@app.event("app_mention")
def handle_mention(event, say, logger):
    try:
        text = re.sub(r"<@\w+>", "", event["text"]).strip()
        channel = event["channel"]
        thread_ts = event.get("thread_ts", event["ts"])
        
        session = get_or_create_session(thread_ts, channel)
        
        # Run agent
        result = runner.run(text, agent=agent, session=session)
        response_text = result.content.parts[0].text
        
        # Send as Slack blocks (rich formatting)
        say(
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"🤖 *AI Assistant*\n{response_text}"
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"Powered by Google ADK • Session: {session.id[:8]}"
                        }
                    ]
                }
            ],
            thread_ts=thread_ts
        )
        
    except Exception as e:
        logger.error(f"Error: {e}")
```

#### 2. Slash Commands

**bot.py** (add slash command):

```python
@app.command("/ask-ai")
def handle_slash_command(ack, command, say):
    """Handle /ask-ai [question] slash command."""
    ack()  # Acknowledge command immediately
    
    try:
        question = command["text"]
        channel = command["channel_id"]
        user = command["user_id"]
        
        # Create ephemeral session for slash commands
        session = Session()
        session.state["user_id"] = user
        session.state["channel"] = channel
        
        # Run agent
        result = runner.run(question, agent=agent, session=session)
        response_text = result.content.parts[0].text
        
        # Respond in channel
        say(f"<@{user}> asked: _{question}_\n\n{response_text}")
        
    except Exception as e:
        say(f"❌ Error: {str(e)}")
```

Configure slash command in Slack App settings:
- Command: `/ask-ai`
- Request URL: Your bot's URL + `/slack/events`
- Description: "Ask AI assistant a question"

#### 3. Interactive Buttons

**bot.py** (interactive components):

```python
@app.action("approve_action")
def handle_approve(ack, action, say):
    """Handle approval button clicks."""
    ack()
    say(f"✅ Action approved by <@{action['user']['id']}>")

@app.event("app_mention")
def handle_mention_with_buttons(event, say):
    text = re.sub(r"<@\w+>", "", event["text"]).strip()
    thread_ts = event.get("thread_ts", event["ts"])
    
    # Check if agent suggests an action requiring approval
    result = runner.run(text, agent=agent, session=session)
    response_text = result.content.parts[0].text
    
    if "approve" in result.actions:  # Custom logic
        # Show approval buttons
        say(
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": response_text}
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "✅ Approve"},
                            "action_id": "approve_action",
                            "style": "primary"
                        },
                        {
                            "type": "button",
                            "text": {"type": "plain_text", "text": "❌ Reject"},
                            "action_id": "reject_action",
                            "style": "danger"
                        }
                    ]
                }
            ],
            thread_ts=thread_ts
        )
```

---

### Deployment

#### Option 1: Socket Mode (Development)

Uses WebSocket connection, no public URL needed.

```bash
# .env
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...  # Required for Socket Mode

# Run
python bot.py
```

#### Option 2: HTTP Mode (Production)

**bot.py** (HTTP mode):

```python
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=3000)
```

**Deploy to Cloud Run**:

```bash
gcloud run deploy slack-adk-bot \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars SLACK_BOT_TOKEN=xoxb-...,GOOGLE_API_KEY=...
```

Configure Slack App Event Subscriptions:
- Request URL: `https://your-bot-xyz.run.app/slack/events`

---

## Part 2: Google Cloud Pub/Sub Integration

### Overview

Google Cloud Pub/Sub enables **event-driven** and **asynchronous** agent architectures. Instead of synchronous HTTP requests, messages are published to topics and processed by subscribers.

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Message Producers                                       │
│  - Web UI (Next.js, React)                               │
│  - Mobile apps                                           │
│  - Slack bot                                             │
│  - API Gateway                                           │
└───────────────┬─────────────────────────────────────────┘
                │ Publish message
                ▼
┌─────────────────────────────────────────────────────────┐
│  Google Cloud Pub/Sub Topic                              │
│  (e.g., "agent-requests")                                │
└───────────────┬─────────────────────────────────────────┘
                │ Subscribe
                ▼
┌─────────────────────────────────────────────────────────┐
│  ADK Agent Subscriber (Cloud Run/GKE)                    │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Pull messages from subscription                  │  │
│  │  Process with ADK agent                            │  │
│  │  Publish result to response topic                  │  │
│  └─────────────────────────────────────────────────────┘│
└───────────────┬─────────────────────────────────────────┘
                │ Publish result
                ▼
┌─────────────────────────────────────────────────────────┐
│  Pub/Sub Response Topic                                  │
│  (e.g., "agent-responses")                               │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│  Result Consumers                                        │
│  - WebSocket server (pushes to UI)                      │
│  - Database (stores results)                             │
│  - Analytics                                             │
└─────────────────────────────────────────────────────────┘
```

---

### Use Cases

1. **High-Volume Processing**: Handle thousands of concurrent agent requests
2. **Asynchronous Workflows**: Long-running agent tasks
3. **Multi-Service Architecture**: Decouple producers and consumers
4. **Message Queuing**: Reliable delivery with retries
5. **Event-Driven**: React to events from multiple sources

---

### Implementation

#### Project Structure

```
pubsub-adk-agent/
├── publisher.py              # Publish messages to Pub/Sub
├── subscriber.py             # Subscribe and process with ADK
├── agents/
│   └── assistant.py          # ADK agent
├── requirements.txt
└── .env
```

#### Step 1: Setup Pub/Sub

**Create topics and subscriptions**:

```bash
# Create request topic
gcloud pubsub topics create agent-requests

# Create response topic
gcloud pubsub topics create agent-responses

# Create subscriptions
gcloud pubsub subscriptions create agent-requests-sub \
  --topic=agent-requests \
  --ack-deadline=600

gcloud pubsub subscriptions create agent-responses-sub \
  --topic=agent-responses \
  --ack-deadline=60
```

#### Step 2: Publisher (Send Requests)

**publisher.py**:

```python
import json
import uuid
from google.cloud import pubsub_v1

project_id = "your-project-id"
topic_id = "agent-requests"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def publish_agent_request(user_query: str, user_id: str, session_id: str = None):
    """Publish an agent request to Pub/Sub."""
    
    message_data = {
        "request_id": str(uuid.uuid4()),
        "user_id": user_id,
        "session_id": session_id or str(uuid.uuid4()),
        "query": user_query,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Publish message
    data_bytes = json.dumps(message_data).encode("utf-8")
    future = publisher.publish(topic_path, data_bytes)
    
    print(f"Published message {future.result()} to {topic_path}")
    return message_data["request_id"]

# Example usage
if __name__ == "__main__":
    request_id = publish_agent_request(
        user_query="What is AI?",
        user_id="user123",
        session_id="sess456"
    )
    print(f"Request ID: {request_id}")
```

#### Step 3: Subscriber (Process with ADK)

**subscriber.py**:

```python
import json
import time
from google.cloud import pubsub_v1
from google.adk.agents import Runner, Session
from agents.assistant import create_agent
from concurrent.futures import TimeoutError

project_id = "your-project-id"
request_subscription_id = "agent-requests-sub"
response_topic_id = "agent-responses"

# Initialize ADK components
agent = create_agent()
runner = Runner()
sessions = {}

# Pub/Sub clients
subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()

subscription_path = subscriber.subscription_path(project_id, request_subscription_id)
response_topic_path = publisher.topic_path(project_id, response_topic_id)

def get_or_create_session(session_id: str) -> Session:
    """Get or create ADK session."""
    if session_id not in sessions:
        sessions[session_id] = Session()
    return sessions[session_id]

def process_message(message):
    """Process a single Pub/Sub message with ADK agent."""
    try:
        # Parse message
        data = json.loads(message.data.decode("utf-8"))
        request_id = data["request_id"]
        user_id = data["user_id"]
        session_id = data["session_id"]
        query = data["query"]
        
        print(f"Processing request {request_id}: {query}")
        
        # Get session
        session = get_or_create_session(session_id)
        session.state["user_id"] = user_id
        
        # Run agent
        result = runner.run(query, agent=agent, session=session)
        response_text = result.content.parts[0].text
        
        # Publish response
        response_data = {
            "request_id": request_id,
            "user_id": user_id,
            "session_id": session_id,
            "response": response_text,
            "status": "success",
            "timestamp": time.time()
        }
        
        response_bytes = json.dumps(response_data).encode("utf-8")
        publisher.publish(response_topic_path, response_bytes)
        
        print(f"✅ Completed request {request_id}")
        
        # Acknowledge message
        message.ack()
        
    except Exception as e:
        print(f"❌ Error processing message: {e}")
        
        # Publish error response
        error_data = {
            "request_id": data.get("request_id", "unknown"),
            "status": "error",
            "error": str(e),
            "timestamp": time.time()
        }
        error_bytes = json.dumps(error_data).encode("utf-8")
        publisher.publish(response_topic_path, error_bytes)
        
        # Acknowledge to avoid retries for unrecoverable errors
        message.ack()

def start_subscriber():
    """Start subscribing to Pub/Sub messages."""
    print(f"Listening for messages on {subscription_path}...")
    
    # Subscribe with callback
    streaming_pull_future = subscriber.subscribe(
        subscription_path,
        callback=process_message
    )
    
    print("Subscriber is running. Press Ctrl+C to exit.")
    
    try:
        # Block and listen
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        print("Subscriber stopped.")

if __name__ == "__main__":
    start_subscriber()
```

#### Step 4: Requirements

**requirements.txt**:

```txt
google-cloud-pubsub>=2.18.0
google-adk>=1.0.0
```

#### Step 5: Run

Terminal 1 (Subscriber):

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
python subscriber.py
```

Terminal 2 (Publisher):

```bash
python publisher.py
```

---

### Advanced Patterns

#### 1. Fan-Out (Multiple Subscribers)

Multiple agent workers process messages in parallel:

```bash
# Create multiple subscriptions for same topic
gcloud pubsub subscriptions create agent-requests-worker-1 --topic=agent-requests
gcloud pubsub subscriptions create agent-requests-worker-2 --topic=agent-requests
gcloud pubsub subscriptions create agent-requests-worker-3 --topic=agent-requests

# Run multiple subscribers
python subscriber.py --subscription=agent-requests-worker-1 &
python subscriber.py --subscription=agent-requests-worker-2 &
python subscriber.py --subscription=agent-requests-worker-3 &
```

#### 2. Priority Queues

**Different topics for different priorities**:

```python
# High priority requests
gcloud pubsub topics create agent-requests-high
gcloud pubsub topics create agent-requests-low

# Publisher
def publish_request(query: str, priority: str = "normal"):
    topic_id = f"agent-requests-{priority}"
    # ... publish to appropriate topic
```

#### 3. Dead Letter Queue (DLQ)

**Handle failed messages**:

```bash
# Create dead letter topic
gcloud pubsub topics create agent-requests-dlq

# Update subscription with DLQ
gcloud pubsub subscriptions update agent-requests-sub \
  --dead-letter-topic=agent-requests-dlq \
  --max-delivery-attempts=5
```

#### 4. Pub/Sub + Next.js UI

**Real-time updates via WebSocket**:

**backend/websocket_server.py**:

```python
import asyncio
import websockets
import json
from google.cloud import pubsub_v1

# WebSocket connections
connections = {}

async def handle_websocket(websocket, path):
    """Handle WebSocket connection."""
    user_id = path.split("/")[-1]
    connections[user_id] = websocket
    
    try:
        await websocket.wait_closed()
    finally:
        del connections[user_id]

def response_callback(message):
    """Callback for Pub/Sub response messages."""
    data = json.loads(message.data.decode("utf-8"))
    user_id = data["user_id"]
    
    # Send to WebSocket client
    if user_id in connections:
        asyncio.run(connections[user_id].send(json.dumps(data)))
    
    message.ack()

# Start Pub/Sub subscriber
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, "agent-responses-sub")
streaming_pull_future = subscriber.subscribe(subscription_path, callback=response_callback)

# Start WebSocket server
async def main():
    async with websockets.serve(handle_websocket, "0.0.0.0", 8765):
        await asyncio.Future()  # Run forever

asyncio.run(main())
```

**frontend/pages/index.tsx**:

```typescript
"use client";
import { useEffect, useState } from "react";

export default function Chat() {
  const [messages, setMessages] = useState<string[]>([]);
  const [ws, setWs] = useState<WebSocket | null>(null);
  
  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8765/user123");
    
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages(prev => [...prev, data.response]);
    };
    
    setWs(socket);
    
    return () => socket.close();
  }, []);
  
  const sendMessage = async (text: string) => {
    // Publish to Pub/Sub via API
    await fetch("/api/publish", {
      method: "POST",
      body: JSON.stringify({ query: text, user_id: "user123" }),
    });
  };
  
  return (
    <div>
      {messages.map((msg, i) => <div key={i}>{msg}</div>)}
      <button onClick={() => sendMessage("Hello!")}>Send</button>
    </div>
  );
}
```

---

### Deployment

#### Cloud Run (Subscriber)

**Dockerfile**:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "subscriber.py"]
```

**Deploy**:

```bash
gcloud run deploy pubsub-adk-subscriber \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars GOOGLE_CLOUD_PROJECT=your-project
```

#### GKE (Horizontal Scaling)

**deployment.yaml**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: adk-subscriber
spec:
  replicas: 3  # Horizontal scaling
  selector:
    matchLabels:
      app: adk-subscriber
  template:
    metadata:
      labels:
        app: adk-subscriber
    spec:
      containers:
      - name: subscriber
        image: gcr.io/your-project/adk-subscriber
        env:
        - name: GOOGLE_CLOUD_PROJECT
          value: "your-project-id"
```

---

## Key Findings

### ✅ High Confidence

1. **Slack Integration**: Straightforward with Bolt SDK + ADK
2. **Pub/Sub Integration**: Well-documented Google Cloud pattern
3. **Event-Driven Architecture**: Native Python support
4. **Production Ready**: Both patterns battle-tested

### ⚠️ Considerations

1. **Slack Rate Limits**: 1 message/second per channel
2. **Pub/Sub Latency**: ~100ms overhead vs. direct HTTP
3. **Session Management**: Need external store (Firestore, Redis) for Pub/Sub
4. **Cost**: Pub/Sub charges per message

### 🎯 Recommendations

**Use Slack When**:
- Team collaboration
- Internal tools
- Support bots

**Use Pub/Sub When**:
- High-volume processing
- Asynchronous workflows
- Multi-service architectures
- Event-driven systems

---

## Next Steps

1. ✅ **Completed**: Slack and Pub/Sub research
2. ⏳ **Next**: Verify ADK version compatibility
3. ⏳ **Next**: Define tutorial structure
4. ⏳ **Next**: Begin writing tutorials

---

## Resources

- **Slack Bolt**: https://slack.dev/bolt-python/
- **Pub/Sub Docs**: https://cloud.google.com/pubsub/docs
- **ADK API**: https://google.github.io/adk-docs/
- **Slack API**: https://api.slack.com/
