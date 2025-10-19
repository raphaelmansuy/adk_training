---
id: pubsub_adk_integration
title: "Tutorial 34: Google Cloud Pub/Sub + Event-Driven Agents"
description: "Build scalable, event-driven document processing pipelines with Google Cloud Pub/Sub and ADK agents for real-time asynchronous processing."
sidebar_label: "34. Pub/Sub Event Agents"
sidebar_position: 34
tags: ["cloud", "pubsub", "event-driven", "python", "scalability"]
keywords:
  ["pubsub", "google cloud", "event-driven", "agent", "python", "scalability"]
status: "updated"
difficulty: "advanced"
estimated_time: "2 hours"
prerequisites:
  [
    "Tutorial 01: Hello World Agent",
    "Google Cloud project",
    "Python experience",
  ]
learning_objectives:
  - "Build event-driven architectures with Pub/Sub"
  - "Scale ADK agents to millions of messages"
  - "Deploy to Cloud Run with DLQ handling"
  - "Implement real-time WebSocket updates"
implementation_link: "https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial34"
---

:::info VERIFIED WITH LATEST SOURCES

This tutorial has been verified against official Google Cloud Pub/Sub Python
SDK (latest), Cloud Run deployment patterns, and ADK async best practices.
FlowControl parameter syntax and at-least-once delivery semantics confirmed
current as of October 2025.

**Estimated Reading Time**: 70-80 minutes  
**Difficulty Level**: Advanced  
**Prerequisites**: Tutorial 29 (UI Integration Intro), Tutorial 1-3 (ADK Basics), Google Cloud project

---

## 🚀 Quick Start - Working Implementation

The easiest way to get started is with our **complete working implementation**:

```bash
cd tutorial_implementation/tutorial34
make setup      # Install dependencies
make test       # Run all tests
make demo       # See example usage
```

[📁 View Full Implementation](../../tutorial_implementation/tutorial34)

**What's included:**

- ✅ Complete `pubsub_agent` with document processing tools
- ✅ 66 comprehensive tests (all passing)
- ✅ Tool functions: summarization, entity extraction, classification
- ✅ Real-world example code ready to run

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites & Setup](#prerequisites--setup)
3. [Quick Start (20 Minutes)](#quick-start-20-minutes)
4. [Understanding the Architecture](#understanding-the-architecture)
5. [Building a Document Processing Pipeline](#building-a-document-processing-pipeline)
6. [Advanced Patterns](#advanced-patterns)
7. [Production Deployment](#production-deployment)
8. [Troubleshooting](#troubleshooting)
9. [Next Steps](#next-steps)

---

## Overview

### What You'll Build

In this tutorial, you'll build a **scalable document processing system** using:

- **Google Cloud Pub/Sub** (Event messaging)
- **Google ADK** (Agent processing)
- **Gemini 2.0 Flash** (Document analysis)
- **Cloud Run** (Serverless compute)
- **WebSocket** (Real-time UI updates)

**Final Result**:

```text
┌─────────────────────────────────────────────────────────────┐
│  Document Processing Pipeline                               │
│  ├─ Upload documents (PDF, DOCX, TXT)                       │
│  ├─ Asynchronous agent processing                           │
│  ├─ Multiple subscribers (summarize, extract, classify)     │
│  ├─ Real-time status updates via WebSocket                  │
│  ├─ Scales to 1000s of documents/minute                     │
│  └─ Resilient with automatic retries                        │
└─────────────────────────────────────────────────────────────┘
```

### Why Pub/Sub + ADK?

| Feature          | Benefit                                    |
| ---------------- | ------------------------------------------ |
| **Asynchronous** | Non-blocking, fast user experience         |
| **Scalable**     | Auto-scales from 0 to millions of messages |
| **Decoupled**    | Publishers and subscribers independent     |
| **Reliable**     | At-least-once delivery, retries, DLQ       |
| **Fan-out**      | One message → Multiple agents              |
| **Ordering**     | Optional message ordering per key          |

**When to use Pub/Sub + ADK:**

✅ Document/image processing pipelines  
✅ Batch data analysis jobs  
✅ Microservices architectures  
✅ Event-driven workflows  
✅ High-throughput systems (1000+ requests/sec)

❌ Synchronous chat UIs → Use Next.js (Tutorial 30)  
❌ Simple scripts → Use direct API calls

---

## Prerequisites & Setup

### System Requirements

```bash
# Python 3.9 or later
python --version  # Should be >= 3.9

# Google Cloud SDK
gcloud --version  # Should be installed
```

### Google Cloud Setup

**1. Create GCP Project**

```bash
# Create project
gcloud projects create my-agent-pipeline --name="Agent Pipeline"

# Set active project
gcloud config set project my-agent-pipeline

# Enable billing (required for Pub/Sub)
# Go to: https://console.cloud.google.com/billing
```

**2. Enable APIs**

```bash
# Enable required APIs
gcloud services enable \
  pubsub.googleapis.com \
  run.googleapis.com \
  aiplatform.googleapis.com

# Verify
gcloud services list --enabled | grep -E 'pubsub|run|aiplatform'
```

**3. Set Up Authentication**

```bash
# Create service account
gcloud iam service-accounts create agent-pipeline \
  --display-name="Agent Pipeline Service Account"

# Grant Pub/Sub permissions
gcloud projects add-iam-policy-binding my-agent-pipeline \
  --member="serviceAccount:agent-pipeline@my-agent-pipeline.iam.gserviceaccount.com" \
  --role="roles/pubsub.publisher"

gcloud projects add-iam-policy-binding my-agent-pipeline \
  --member="serviceAccount:agent-pipeline@my-agent-pipeline.iam.gserviceaccount.com" \
  --role="roles/pubsub.subscriber"

# Create key for local development
gcloud iam service-accounts keys create key.json \
  --iam-account=agent-pipeline@my-agent-pipeline.iam.gserviceaccount.com

# Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/key.json"
```

**4. Get API Keys**

```bash
# Gemini API key
export GOOGLE_API_KEY="your_gemini_api_key_here"
```

---

## Quick Start (20 Minutes)

### Step 1: Create Pub/Sub Resources

```bash
# Create topic for document uploads
gcloud pubsub topics create document-uploads

# Create subscription for processor agent
gcloud pubsub subscriptions create document-processor \
  --topic=document-uploads \
  --ack-deadline=600

# Verify
gcloud pubsub topics list
gcloud pubsub subscriptions list
```

---

### Step 2: Create Publisher

Create `publisher.py`:

```python
"""
Document Publisher
Publishes document upload events to Pub/Sub
"""

import os
import json
import base64
from google.cloud import pubsub_v1
from datetime import datetime

# Initialize publisher
project_id = os.environ.get("GCP_PROJECT", "my-agent-pipeline")
topic_id = "document-uploads"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def publish_document(document_id: str, content: str, document_type: str = "text"):
    """
    Publish a document processing event.

    Args:
        document_id: Unique document identifier
        content: Document content (text or base64 for binary)
        document_type: Type of document (text, pdf, docx)

    Returns:
        Message ID
    """
    # Create message
    message_data = {
        "document_id": document_id,
        "content": content,
        "document_type": document_type,
        "uploaded_at": datetime.now().isoformat(),
        "status": "pending"
    }

    # Encode as JSON
    data = json.dumps(message_data).encode("utf-8")

    # Publish to topic
    future = publisher.publish(
        topic_path,
        data,
        # Attributes for filtering
        document_type=document_type,
        document_id=document_id
    )

    message_id = future.result()

    print(f"Published document {document_id} (message ID: {message_id})")
    return message_id

# Example usage
if __name__ == "__main__":
    # Publish sample document
    sample_doc = """
    This is a sample sales report for Q4 2024.

    Revenue: $1.2M
    Expenses: $800K
    Net Profit: $400K

    Key achievements:
    - Launched 3 new products
    - Expanded to 2 new markets
    - Grew customer base by 35%

    Challenges:
    - Supply chain delays
    - Increased competition
    - Rising costs
    """

    message_id = publish_document(
        document_id="DOC-001",
        content=sample_doc,
        document_type="text"
    )

    print(f"✅ Published! Message ID: {message_id}")
```

---

### Step 3: Create Subscriber (Agent Processor)

Create `subscriber.py`:

```python
"""
Document Processor Subscriber
Processes documents using ADK agent coordinator
"""

import os
import sys
import json
import asyncio
import logging
from google.cloud import pubsub_v1
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pubsub_agent.agent import root_agent

# Suppress noisy debug messages from libraries
logging.getLogger('google.auth').setLevel(logging.WARNING)
logging.getLogger('google.cloud').setLevel(logging.WARNING)
logging.getLogger('google.genai').setLevel(logging.WARNING)
logging.getLogger('absl').setLevel(logging.ERROR)

project_id = os.environ.get("GCP_PROJECT")
subscription_id = "document-processor"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

async def process_document_with_agent(document_id: str, content: str):
    """Process document using the ADK root_agent coordinator."""
    try:
        # Create a runner for the agent with required session service
        session_service = InMemorySessionService()
        runner = Runner(
            app_name="pubsub_processor",
            agent=root_agent,
            session_service=session_service
        )
        
        # Create a session for this document processing
        session = await session_service.create_session(
            app_name="pubsub_processor",
            user_id="pubsub_subscriber"
        )
        
        # Prepare the message for the agent
        prompt_text = f"""Analyze this document and route it to the appropriate analyzer:

Document ID: {document_id}

Content:
{content}

Analyze the document type and extract relevant information."""
        
        # Create a proper Content object for the agent
        prompt = types.Content(
            role="user",
            parts=[types.Part(text=prompt_text)]
        )
        
        # Run the agent and collect the result
        final_result = None
        async for event in runner.run_async(
            user_id="pubsub_subscriber",
            session_id=session.id,
            new_message=prompt
        ):
            # Events are streamed, capture the final one
            final_result = event
        
        return final_result
        
    except Exception as e:
        print(f"❌ Agent processing error: {e}")
        raise

def process_message(message):
    """Process Pub/Sub message with async agent processing."""
    try:
        data = json.loads(message.data.decode("utf-8"))
        document_id = data.get("document_id")
        content = data.get("content")

        print(f"\n📄 Processing: {document_id}")

        # Run the async agent processing
        result = asyncio.run(process_document_with_agent(document_id, content))

        if result:
            # Extract text from the event's content
            response_text = ""
            if hasattr(result, 'content') and result.content and result.content.parts:
                for part in result.content.parts:
                    if part.text:
                        response_text += part.text
            
            if response_text:
                # Clean up the response text for display
                display_text = response_text.strip()[:200]
                print(f"✅ Success: {document_id}")
                print(f"   └─ {display_text}...")
            else:
                print(f"✅ Completed {document_id} (no text response)")
        else:
            print(f"✅ Completed {document_id}")

        # Acknowledge message (remove from queue)
        message.ack()

    except Exception as e:
        print(f"❌ Error: {document_id} - {str(e)[:100]}")
        message.nack()

# Subscribe and process
print("\n" + "="*70)
print("🚀 Document Processing Coordinator")
print("="*70)
print(f"Subscription: {subscription_id}")
print(f"Project:      {project_id or '(not set - local mode)'}")
print(f"Agent:        root_agent (multi-analyzer coordinator)")
print("="*70)
print("Waiting for messages...\n")

streaming_pull_future = subscriber.subscribe(
    subscription_path,
    callback=process_message
)

try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
    print("\n" + "="*70)
    print("✋ Processor stopped")
    print("="*70)
```

---

### Step 4: Run the System

**Terminal 1 - Start Subscriber**:

```bash
# Install dependencies
pip install google-cloud-pubsub google-genai

# Set environment
export GCP_PROJECT="my-agent-pipeline"
export GOOGLE_API_KEY="your_api_key"
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/key.json"

# Run subscriber
python subscriber.py

# Output: 🚀 Document processor is running!
```

**Terminal 2 - Publish Documents**:

```bash
# Set same environment
export GCP_PROJECT="my-agent-pipeline"
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/key.json"

# Publish document
python publisher.py

# Output:
# Published document DOC-001 (message ID: 123456789)
# ✅ Published! Message ID: 123456789
```

**Check Terminal 1** - You'll see:

```text
Received message: 123456789
Document ID: DOC-001
Processing document DOC-001...
✅ Completed processing DOC-001
Result: completed
```

🎉 **Your event-driven agent pipeline is working!**

---

## Understanding the Architecture

### Component Diagram

```text
┌─────────────────────────────────────────────────────────────┐
│                    DOCUMENT SOURCES                         │
│  ┌──────────────┐  ┌──────────────┐   ┌──────────────┐      │
│  │  Web Upload  │  │  API Endpoint│   │  Cloud Storage      │
│  └──────┬───────┘  └──────┬───────┘   └──────┬───────┘      │
└─────────┼─────────────────┼───────── ────────┼──────────────┘
          │                 │                  │
          │   Publish       │   Publish        │   Trigger
          │                 │                  │
┌─────────▼─────────────────▼──────────────────▼─────────────┐
│              GOOGLE CLOUD PUB/SUB                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Topic: document-uploads                             │  │
│  │  ├─ Message queue (buffered)                         │  │
│  │  ├─ At-least-once delivery                           │  │
│  │  └─ Automatic retries                                │  │
│  └──────────┬───────────────────────────────────────────┘  │
└─────────────┼───────────────────────────────────────────────┘
              │
              │ Fan-out (multiple subscribers)
              │
      ┌───────┴───────┬───────────────┬───────────────┐
      │               │               │               │
┌─────▼──────┐  ┌────▼────┐  ┌───────▼──────┐  ┌────▼────┐
│ Summarizer │  │Extractor│  │  Classifier  │  │ Notifier│
│ Subscriber │  │Subscriber  │  Subscriber  │  │Subscriber
│            │  │         │  │              │  │         │
│ ADK Agent  │  │ADK Agent│  │  ADK Agent   │  │ Webhook │
│ (Summary)  │  │(Entities)  │ (Category)   │  │ (Email) │
└────────────┘  └─────────┘  └──────────────┘  └─────────┘
      │               │               │               │
      │   Store       │   Store       │   Store       │   Send
      │               │               │               │
┌─────▼───────────────▼───────────────▼───────────────▼───────┐
│              RESULTS & NOTIFICATIONS                        │
│  ├─ Firestore (structured data)                             │
│  ├─ Cloud Storage (processed documents)                     │
│  └─ WebSocket (real-time UI updates)                        │
└─────────────────────────────────────────────────────────────┘
```

### Event Flow

**1. User uploads document** via web UI

**2. Publisher creates Pub/Sub message**:

```json
{
  "document_id": "DOC-001",
  "content": "This is a sales report...",
  "document_type": "text",
  "uploaded_at": "2025-10-08T10:00:00Z",
  "status": "pending"
}
```

**3. Pub/Sub distributes to subscribers**:

- Message stored in topic
- Multiple subscriptions receive copy
- Each subscriber processes independently

**4. Subscriber receives message**:

```python
def callback(message):
    # Parse message
    data = json.loads(message.data)

    # Process with ADK agent
    result = process_document(data)

    # Acknowledge (removes from queue)
    message.ack()
```

**5. Agent processes document**:

```text
User: Analyze this text document: [content]
Agent: {
  "summary": "Q4 2024 sales report...",
  "key_info": {
    "revenue": "$1.2M",
    "expenses": "$800K",
    "profit": "$400K"
  },
  "classification": "Financial Report",
  "sentiment": "Positive"
}
```

**6. Result stored** and **user notified**!

---

### Pub/Sub Guarantees

| Guarantee                  | Description                               |
| -------------------------- | ----------------------------------------- |
| **At-least-once delivery** | Message delivered ≥1 time (may duplicate) |
| **Ordering**               | Optional per message key                  |
| **Retention**              | 7 days default (configurable)             |
| **Throughput**             | 100,000s messages/sec                     |
| **Latency**                | &lt;100ms p99                             |
| **Durability**             | Replicated across zones                   |

---

## Building a Document Processing Pipeline

### Feature 1: Multiple Processing Agents

Create specialized agents:

**Summarizer Agent** (`summarizer.py`):

```python
"""Summarizer Agent - Generates document summaries"""

from google.cloud import pubsub_v1
from google import genai
import json
import os

project_id = os.environ.get("GCP_PROJECT")
subscription_id = "summarizer-subscription"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

# Specialized summarization agent using ADK
from google.adk.agents import Agent

agent = Agent(
    model="gemini-2.0-flash-exp",
    name="summarizer",
    instruction="""You are an expert document summarizer.

Your task:
- Create concise, informative summaries
- Capture main points and key takeaways
- Use 2-3 sentences for short docs, 1 paragraph for long
- Highlight critical information

Format:
- Start with document type
- Main topic/purpose
- Key findings or conclusions
- Action items (if any)

Be clear, precise, and actionable."""
)

# Initialize runner for summarizer agent
from google.adk.runners import InMemoryRunner

runner = InMemoryRunner(agent=agent, app_name='summarizer')

def summarize_document(content: str, doc_id: str = 'default') -> str:
    """Generate summary using agent."""
    # Proper ADK execution pattern with InMemoryRunner
    import asyncio
    from google.genai import types

    async def get_summary(text: str):
        """Helper to execute agent in async context."""
        # Create session for this document
        session = await runner.session_service.create_session(
            app_name='summarizer',
            user_id='system'
        )

        new_message = types.Content(
            role='user',
            parts=[types.Part(text=f"Summarize this document:\n\n{text}")]
        )

        summary_text = ""
        async for event in runner.run_async(
            user_id='system',
            session_id=session.id,
            new_message=new_message
        ):
            if event.content and event.content.parts:
                summary_text += event.content.parts[0].text

        return summary_text

    summary = asyncio.run(get_summary(content))
    return summary

def callback(message):
    try:
        data = json.loads(message.data.decode("utf-8"))
        document_id = data["document_id"]
        content = data["content"]

        print(f"📝 Summarizing {document_id}...")

        summary = summarize_document(content)

        result = {
            "document_id": document_id,
            "type": "summary",
            "result": summary
        }

        print(f"✅ Summary: {summary[:100]}...")

        # Store result (to Firestore, etc.)
        # store_result(result)

        message.ack()

    except Exception as e:
        print(f"❌ Error: {e}")
        message.nack()

# Subscribe
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print("🚀 Summarizer agent running!")

try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
```

**Entity Extractor Agent** (`extractor.py`):

```python
"""Entity Extractor Agent - Extracts entities from documents"""

from google.cloud import pubsub_v1
from google import genai
from google.genai.types import Tool, FunctionDeclaration
import json
import os
import re

project_id = os.environ.get("GCP_PROJECT")
subscription_id = "extractor-subscription"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

client = genai.Client(
    api_key=os.environ.get("GOOGLE_API_KEY"),
    http_options={'api_version': 'v1alpha'}
)

def extract_dates(text: str) -> list:
    """Extract dates from text."""
    # Simple regex for dates (YYYY-MM-DD, MM/DD/YYYY, etc.)
    patterns = [
        r'\d{4}-\d{2}-\d{2}',  # 2024-10-08
        r'\d{1,2}/\d{1,2}/\d{4}',  # 10/08/2024
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}'  # October 8, 2024
    ]

    dates = []
    for pattern in patterns:
        dates.extend(re.findall(pattern, text, re.IGNORECASE))

    return list(set(dates))

def extract_numbers(text: str) -> list:
    """Extract numbers (currency, percentages, quantities)."""
    patterns = {
        'currency': r'\$[\d,]+(?:\.\d{2})?',  # $1,200.00
        'percentage': r'\d+(?:\.\d+)?%',  # 35%
        'quantity': r'\d+(?:,\d{3})*'  # 1,000
    }

    results = {}
    for name, pattern in patterns.items():
        results[name] = re.findall(pattern, text)

    return results

# Entity extraction agent using ADK
from google.adk.agents import Agent

agent = Agent(
    model="gemini-2.0-flash-exp",
    name="entity_extractor",
    instruction="""You are an expert entity extraction agent.

Extract from documents:
- People names
- Organizations/companies
- Locations
- Dates (use extract_dates tool)
- Numbers/metrics (use extract_numbers tool)
- Key terms/concepts

Return as structured JSON:
{
  "people": ["John Doe", "Jane Smith"],
  "organizations": ["Acme Corp", "TechCo"],
  "locations": ["San Francisco", "New York"],
  "dates": ["2024-10-08"],
  "metrics": {
    "revenue": "$1.2M",
    "growth": "35%"
  },
  "key_terms": ["sales", "Q4", "expansion"]
}

Be thorough and accurate.""",
    tools=[
        Tool(
            function_declarations=[
                FunctionDeclaration(
                    name="extract_dates",
                    description="Extract dates from text",
                    parameters={
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "Text to extract dates from"
                            }
                        },
                        "required": ["text"]
                    }
                ),
                FunctionDeclaration(
                    name="extract_numbers",
                    description="Extract numbers (currency, percentages) from text",
                    parameters={
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "Text to extract numbers from"
                            }
                        },
                        "required": ["text"]
                    }
                )
            ]
        )
    ],
    tool_config={
        "function_calling_config": {
            "mode": "AUTO"
        }
    }
)

# Initialize runner for entity extractor agent
from google.adk.runners import InMemoryRunner

runner = InMemoryRunner(agent=agent, app_name='entity_extractor')

TOOLS = {
    "extract_dates": extract_dates,
    "extract_numbers": extract_numbers
}

def extract_entities(content: str, doc_id: str = 'default') -> dict:
    """Extract entities using agent."""
    # Proper ADK execution pattern with InMemoryRunner
    import asyncio
    from google.genai import types

    async def get_entities(text: str):
        """Helper to execute agent in async context."""
        # Create session for this document
        session = await runner.session_service.create_session(
            app_name='entity_extractor',
            user_id='system'
        )

        new_message = types.Content(
            role='user',
            parts=[types.Part(text=f"Extract all entities from:\n\n{text}")]
        )

        result_text = ""
        async for event in runner.run_async(
            user_id='system',
            session_id=session.id,
            new_message=new_message
        ):
            if event.content and event.content.parts:
                result_text += event.content.parts[0].text

        return result_text

    result = asyncio.run(get_entities(content))
    return result

def callback(message):
    try:
        data = json.loads(message.data.decode("utf-8"))
        document_id = data["document_id"]
        content = data["content"]

        print(f"🔍 Extracting entities from {document_id}...")

        entities = extract_entities(content)

        result = {
            "document_id": document_id,
            "type": "entities",
            "result": entities
        }

        print(f"✅ Extracted entities")

        message.ack()

    except Exception as e:
        print(f"❌ Error: {e}")
        message.nack()

# Subscribe
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print("🚀 Entity extractor running!")

try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
```

**Create subscriptions**:

```bash
# Summarizer subscription
gcloud pubsub subscriptions create summarizer-subscription \
  --topic=document-uploads \
  --ack-deadline=600

# Extractor subscription
gcloud pubsub subscriptions create extractor-subscription \
  --topic=document-uploads \
  --ack-deadline=600

# Now ONE published message goes to BOTH agents! 🚀
```

**Run all agents**:

```bash
# Terminal 1
python summarizer.py

# Terminal 2
python extractor.py

# Terminal 3 - Publish
python publisher.py
```

Both agents process the same document independently! ⚡

---

### Feature 2: Real-Time UI Updates

Add WebSocket server for live status:

**Create `websocket_server.py`**:

```python
"""
WebSocket Server for Real-Time Updates
Listens to Pub/Sub results topic and broadcasts to connected clients
"""

import asyncio
import websockets
import json
import os
from google.cloud import pubsub_v1
from threading import Thread

# Connected WebSocket clients
connected_clients = set()

# Pub/Sub subscriber for results
project_id = os.environ.get("GCP_PROJECT")
subscription_id = "results-websocket-subscription"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

async def handle_client(websocket, path):
    """Handle WebSocket client connection."""
    # Register client
    connected_clients.add(websocket)
    print(f"✅ Client connected. Total: {len(connected_clients)}")

    try:
        # Keep connection alive
        async for message in websocket:
            # Echo or handle client messages if needed
            pass
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        # Unregister client
        connected_clients.remove(websocket)
        print(f"❌ Client disconnected. Total: {len(connected_clients)}")

async def broadcast_update(update: dict):
    """Broadcast update to all connected clients."""
    if connected_clients:
        message = json.dumps(update)
        await asyncio.gather(
            *[client.send(message) for client in connected_clients],
            return_exceptions=True
        )

def pubsub_callback(message):
    """Callback for Pub/Sub messages."""
    try:
        data = json.loads(message.data.decode("utf-8"))

        print(f"📡 Broadcasting update: {data['document_id']}")

        # Broadcast to WebSocket clients
        asyncio.run(broadcast_update(data))

        message.ack()

    except Exception as e:
        print(f"Error: {e}")
        message.nack()

def start_pubsub_listener():
    """Start Pub/Sub listener in background thread."""
    streaming_pull_future = subscriber.subscribe(
        subscription_path,
        callback=pubsub_callback
    )

    print("🚀 Pub/Sub listener started")

    try:
        streaming_pull_future.result()
    except Exception as e:
        print(f"Pub/Sub error: {e}")
        streaming_pull_future.cancel()

# Start WebSocket server
async def main():
    # Start Pub/Sub listener in background
    pubsub_thread = Thread(target=start_pubsub_listener, daemon=True)
    pubsub_thread.start()

    # Start WebSocket server
    async with websockets.serve(handle_client, "0.0.0.0", 8765):
        print("🌐 WebSocket server running on ws://localhost:8765")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
```

**Frontend HTML** (`index.html`):

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document Processing Status</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        max-width: 800px;
        margin: 50px auto;
        padding: 20px;
        background: #f5f5f5;
      }
      .status-card {
        background: white;
        padding: 20px;
        margin: 10px 0;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }
      .status-pending {
        border-left: 4px solid #ff9800;
      }
      .status-processing {
        border-left: 4px solid #2196f3;
      }
      .status-completed {
        border-left: 4px solid #4caf50;
      }
      .status-error {
        border-left: 4px solid #f44336;
      }
      .timestamp {
        color: #666;
        font-size: 0.9em;
      }
      #connection-status {
        padding: 10px;
        text-align: center;
        border-radius: 4px;
        margin-bottom: 20px;
      }
      .connected {
        background: #4caf50;
        color: white;
      }
      .disconnected {
        background: #f44336;
        color: white;
      }
    </style>
  </head>
  <body>
    <h1>📄 Document Processing Status</h1>

    <div id="connection-status" class="disconnected">
      Connecting to server...
    </div>

    <div id="documents"></div>

    <script>
      const ws = new WebSocket("ws://localhost:8765");
      const statusDiv = document.getElementById("connection-status");
      const documentsDiv = document.getElementById("documents");

      const documents = new Map();

      ws.onopen = () => {
        statusDiv.textContent = "✅ Connected";
        statusDiv.className = "connected";
      };

      ws.onclose = () => {
        statusDiv.textContent = "❌ Disconnected";
        statusDiv.className = "disconnected";
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        updateDocument(data);
      };

      function updateDocument(data) {
        documents.set(data.document_id, data);
        renderDocuments();
      }

      function renderDocuments() {
        documentsDiv.innerHTML = Array.from(documents.values())
          .sort(
            (a, b) =>
              new Date(b.updated_at || b.uploaded_at) -
              new Date(a.updated_at || a.uploaded_at)
          )
          .map(
            (doc) => `
                    <div class="status-card status-${doc.status}">
                        <h3>${doc.document_id}</h3>
                        <p><strong>Status:</strong> ${doc.status}</p>
                        <p><strong>Type:</strong> ${doc.type || "Unknown"}</p>
                        ${
                          doc.result
                            ? `<p><strong>Result:</strong> ${doc.result.substring(
                                0,
                                100
                              )}...</p>`
                            : ""
                        }
                        <p class="timestamp">${
                          doc.updated_at || doc.uploaded_at
                        }</p>
                    </div>
                `
          )
          .join("");
      }
    </script>
  </body>
</html>
```

**Test it**:

```bash
# Terminal 1 - WebSocket server
pip install websockets
python websocket_server.py

# Terminal 2 - Open browser
open index.html

# Terminal 3 - Publish documents
python publisher.py
```

Watch documents update in real-time in your browser! 🌐

---

## Advanced Patterns

### Pattern 1: Message Ordering

Ensure messages process in order:

```bash
# Create topic with ordering
gcloud pubsub topics create ordered-documents \
  --message-ordering

# Create subscription with ordering
gcloud pubsub subscriptions create ordered-processor \
  --topic=ordered-documents \
  --enable-message-ordering
```

```python
# Publish with ordering key
future = publisher.publish(
    topic_path,
    data,
    ordering_key=f"user_{user_id}"  # All messages with same key ordered
)
```

---

### Pattern 2: Dead Letter Queue

Handle failed messages:

```bash
# Create DLQ topic
gcloud pubsub topics create document-dlq

# Create subscription with DLQ
gcloud pubsub subscriptions create document-processor \
  --topic=document-uploads \
  --dead-letter-topic=document-dlq \
  --max-delivery-attempts=5
```

```python
# Monitor DLQ
def monitor_dlq():
    """Check dead letter queue for failed messages."""
    dlq_subscription = "document-dlq-subscription"
    dlq_path = subscriber.subscription_path(project_id, dlq_subscription)

    def callback(message):
        print(f"⚠️ Failed message: {message.message_id}")
        data = json.loads(message.data)
        print(f"Document: {data['document_id']}")

        # Alert team, retry manually, or discard
        send_alert(f"Document {data['document_id']} failed after 5 attempts")

        message.ack()

    subscriber.subscribe(dlq_path, callback=callback)
```

---

### Pattern 3: Batch Processing

Process multiple messages at once:

```python
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

subscriber = pubsub_v1.SubscriberClient()

# Configure flow control
flow_control = pubsub_v1.types.FlowControl(
    max_messages=10,  # Pull 10 messages at once
    max_bytes=10 * 1024 * 1024,  # 10 MB
)

def callback(message):
    # Process message
    pass

streaming_pull_future = subscriber.subscribe(
    subscription_path,
    callback=callback,
    flow_control=flow_control
)
```

---

### Pattern 4: Priority Queues

Use multiple topics for priorities:

```bash
# Create priority topics
gcloud pubsub topics create urgent-documents
gcloud pubsub topics create normal-documents
gcloud pubsub topics create low-priority-documents

# Create subscriptions
gcloud pubsub subscriptions create urgent-processor \
  --topic=urgent-documents \
  --ack-deadline=300

gcloud pubsub subscriptions create normal-processor \
  --topic=normal-documents \
  --ack-deadline=600

gcloud pubsub subscriptions create low-processor \
  --topic=low-priority-documents \
  --ack-deadline=3600
```

```python
def publish_with_priority(document_id, content, priority="normal"):
    """Publish to appropriate topic based on priority."""
    topics = {
        "urgent": "urgent-documents",
        "normal": "normal-documents",
        "low": "low-priority-documents"
    }

    topic = topics.get(priority, "normal-documents")
    topic_path = publisher.topic_path(project_id, topic)

    # Publish
    future = publisher.publish(topic_path, data)
    return future.result()
```

---

## Production Deployment

### Architecture Overview

```text
┌────────────────────────────────────────────────────────────┐
│  Cloud Run (Auto-scaling)                                  │
│  ├─ Publisher Service (HTTP API)                           │
│  ├─ Summarizer Service (Pub/Sub triggered)                 │
│  ├─ Extractor Service (Pub/Sub triggered)                  │
│  └─ WebSocket Service (Real-time updates)                  │
└────────────────────────────────────────────────────────────┘
                            ▲
                            │
┌───────────────────────────┴────────────────────────────────┐
│  Pub/Sub                                                   │
│  ├─ document-uploads (main topic)                          │
│  ├─ document-results (processed results)                   │
│  └─ document-dlq (failed messages)                         │
└────────────────────────────────────────────────────────────┘
```

### Deploy Publisher API

**Create `api.py`**:

```python
"""
Publisher API
HTTP endpoint for uploading documents
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.cloud import pubsub_v1
import os
import json
import uuid
from datetime import datetime

app = FastAPI(title="Document Processing API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pub/Sub setup
project_id = os.environ.get("GCP_PROJECT")
topic_id = "document-uploads"
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload document for processing.

    Returns:
        Document ID and message ID
    """
    try:
        # Generate document ID
        document_id = f"DOC-{uuid.uuid4().hex[:8].upper()}"

        # Read file content
        content = await file.read()
        content_str = content.decode("utf-8")

        # Create message
        message_data = {
            "document_id": document_id,
            "content": content_str,
            "document_type": file.content_type or "text/plain",
            "filename": file.filename,
            "uploaded_at": datetime.now().isoformat(),
            "status": "pending"
        }

        # Publish
        data = json.dumps(message_data).encode("utf-8")
        future = publisher.publish(topic_path, data)
        message_id = future.result()

        return {
            "document_id": document_id,
            "message_id": message_id,
            "status": "queued"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status/{document_id}")
def get_status(document_id: str):
    """Get document processing status."""
    # Query Firestore/database for status
    # For demo, return mock status
    return {
        "document_id": document_id,
        "status": "processing",
        "updated_at": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

**Deploy**:

```bash
# Create requirements.txt
cat > requirements.txt << EOF
fastapi==0.115.0
uvicorn[standard]==0.30.0
google-cloud-pubsub==2.23.0
python-multipart==0.0.9
EOF

# Create Dockerfile
cat > Dockerfile << EOF
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api.py .

EXPOSE 8080

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
EOF

# Deploy to Cloud Run
gcloud run deploy document-api \
  --source=. \
  --region=us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GCP_PROJECT=my-agent-pipeline"

# Output: https://document-api-abc123.run.app
```

**Test API**:

```bash
# Upload document
curl -X POST https://document-api-abc123.run.app/upload \
  -F "file=@sample.txt"

# Output:
# {
#   "document_id": "DOC-A1B2C3D4",
#   "message_id": "123456789",
#   "status": "queued"
# }
```

---

### Deploy Processor Services

Each agent as separate Cloud Run service:

```bash
# Deploy summarizer
gcloud run deploy summarizer \
  --source=. \
  --region=us-central1 \
  --no-allow-unauthenticated \
  --set-env-vars="GCP_PROJECT=my-agent-pipeline,GOOGLE_API_KEY=xxx" \
  --min-instances=0 \
  --max-instances=10

# Create Pub/Sub subscription to trigger Cloud Run
gcloud pubsub subscriptions create summarizer-cloudrun \
  --topic=document-uploads \
  --push-endpoint=https://summarizer-abc123.run.app/process

# Repeat for other agents (extractor, classifier, etc.)
```

---

### Monitoring & Alerting

```python
# Add monitoring
from google.cloud import monitoring_v3
import time

def log_processing_metrics(document_id, latency, success):
    """Log processing metrics."""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{os.environ['GCP_PROJECT']}"

    # Log latency
    series = monitoring_v3.TimeSeries()
    series.metric.type = "custom.googleapis.com/document_processing/latency"
    series.resource.type = "global"

    point = monitoring_v3.Point({
        "interval": {"end_time": {"seconds": int(time.time())}},
        "value": {"double_value": latency}
    })
    series.points = [point]

    client.create_time_series(name=project_name, time_series=[series])

    # Log success/failure
    # ... similar for success rate
```

**Set up alerts**:

```bash
# Create alert policy
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="High Processing Latency" \
  --condition-display-name="Latency > 10s" \
  --condition-threshold-value=10 \
  --condition-threshold-duration=300s
```

---

## Troubleshooting

### Common Issues

**Issue 1: Messages Not Delivered**

**Symptoms**:

- Publisher succeeds but subscriber doesn't receive
- No messages in subscription

**Solutions**:

```bash
# Check subscription exists
gcloud pubsub subscriptions describe document-processor

# Check messages in subscription
gcloud pubsub subscriptions pull document-processor --limit=1

# Check IAM permissions
gcloud pubsub subscriptions get-iam-policy document-processor

# Verify subscriber is running
ps aux | grep subscriber.py
```

---

**Issue 2: Messages Re-delivered Multiple Times**

**Symptoms**:

- Same message processed multiple times
- Duplicate results

**Solutions**:

```python
# Implement idempotency
processed_messages = set()

def callback(message):
    message_id = message.message_id

    # Check if already processed
    if message_id in processed_messages:
        print(f"⏭️  Skipping duplicate: {message_id}")
        message.ack()
        return

    # Process message
    result = process_document(data)

    # Mark as processed
    processed_messages.add(message_id)

    # Store in persistent storage (Redis, Firestore)
    # store_processed_id(message_id)

    message.ack()
```

---

**Issue 3: High Latency**

**Symptoms**:

- Messages take minutes to process
- Slow end-to-end pipeline

**Solutions**:

```python
# Increase parallelism
executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

streaming_pull_future = subscriber.subscribe(
    subscription_path,
    callback=callback,
    flow_control=pubsub_v1.types.FlowControl(
        max_messages=10,  # Process 10 at once
    ),
    executor=executor
)

# Reduce ack deadline for faster retries
gcloud pubsub subscriptions update document-processor \
  --ack-deadline=60  # 60 seconds

# Scale Cloud Run instances
gcloud run services update summarizer \
  --max-instances=50 \
  --concurrency=10
```

---

**Issue 4: Messages Stuck in DLQ**

**Symptoms**:

- Messages in dead letter queue
- Repeated failures

**Solutions**:

```python
# Investigate DLQ messages
def investigate_dlq():
    """Pull and analyze DLQ messages."""
    dlq_subscription = "document-dlq-subscription"
    dlq_path = subscriber.subscription_path(project_id, dlq_subscription)

    # Pull messages
    response = subscriber.pull(
        request={"subscription": dlq_path, "max_messages": 10}
    )

    for msg in response.received_messages:
        data = json.loads(msg.message.data)
        print(f"Failed document: {data['document_id']}")
        print(f"Error: {msg.message.attributes.get('error')}")

        # Analyze why it failed
        # Fix issue
        # Re-publish if needed

        # Acknowledge to remove from DLQ
        subscriber.acknowledge(
            request={
                "subscription": dlq_path,
                "ack_ids": [msg.ack_id]
            }
        )

investigate_dlq()
```

---

**Issue 5: Cost Optimization**

**Symptoms**:

- High Pub/Sub costs
- Many small messages

**Solutions**:

```python
# Batch messages
batch_settings = pubsub_v1.types.BatchSettings(
    max_messages=100,  # Batch up to 100 messages
    max_bytes=1024 * 1024,  # 1 MB
    max_latency=1.0,  # Wait up to 1 second
)

publisher = pubsub_v1.PublisherClient(batch_settings=batch_settings)

# Filter messages at subscription level
gcloud pubsub subscriptions create filtered-processor \
  --topic=document-uploads \
  --message-filter='attributes.document_type="pdf"'

# Set message retention
gcloud pubsub subscriptions update document-processor \
  --message-retention-duration=1d  # 1 day instead of 7
```

---

## Next Steps

### You've Mastered Pub/Sub + ADK! 🎉

You now know how to:

✅ Build event-driven agent architectures  
✅ Use Google Cloud Pub/Sub for messaging  
✅ Create fan-out patterns with multiple agents  
✅ Implement real-time UI updates with WebSocket  
✅ Deploy scalable systems to Cloud Run  
✅ Handle failures with DLQ and retries  
✅ Monitor and optimize production pipelines

### Architectural Patterns Learned

| Pattern               | Use Case                              |
| --------------------- | ------------------------------------- |
| **Fan-out**           | One message → Multiple processors     |
| **Dead Letter Queue** | Handle failed messages                |
| **Message Ordering**  | Sequential processing per key         |
| **Batch Processing**  | High-throughput optimization          |
| **Priority Queues**   | Different SLAs for different messages |

### Continue Learning

**Tutorial 35**: AG-UI Deep Dive - Building Custom Components  
Master advanced CopilotKit features for sophisticated web UIs

**Tutorial 29**: UI Integration Overview  
Compare all integration approaches (Pub/Sub, Web, Slack, Streamlit)

**Tutorial 30-33**: Other Integration Patterns  
Learn Next.js, Vite, Streamlit, and Slack integrations

### Additional Resources

- [Pub/Sub Documentation](https://cloud.google.com/pubsub/docs)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [ADK Documentation](https://google.github.io/adk-docs/)
- [Pub/Sub Best Practices](https://cloud.google.com/pubsub/docs/best-practices)

---

**🎉 Tutorial 34 Complete!**

🎊 **Congratulations!** You've completed all 34 tutorials in the ADK Training series. You now have comprehensive knowledge of Google Agent Development Kit from basic concepts to production deployment.

---

**Questions or feedback?** Open an issue on the [ADK Training Repository](https://github.com/google/adk-training).
