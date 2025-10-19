# Tutorial 34: Google Cloud Pub/Sub + Event-Driven Agents

Build scalable, event-driven document processing pipelines with Google
Cloud Pub/Sub and ADK agents for real-time asynchronous processing.

## Quick Start

### Setup (5 minutes)

```bash
# Install dependencies
make setup

# Run tests to verify setup
make test
```

### Understanding the Architecture

This tutorial implements an **event-driven document processing pipeline**:

```text
┌─────────────────────────────────────────────────────────────┐
│  Publisher                                                  │
│  └─ Sends documents to Pub/Sub topic                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│  Google Cloud Pub/Sub                                       │
│  └─ Buffers and distributes messages                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
      ┌───────────────┼───────────────┐
      │               │               │
┌─────▼──────┐  ┌────▼────┐  ┌───────▼──────┐
│ Summarizer │  │Extractor│  │  Classifier  │
│ Subscriber │  │Subscriber  │  Subscriber  │
└────────────┘  └─────────┘  └──────────────┘
      │               │               │
      └───────────────┼───────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│  Results Storage                                            │
│  └─ Save processed results and status                       │
└─────────────────────────────────────────────────────────────┘
```

## Components

### Multi-Agent Architecture

This tutorial implements a **coordinator + specialized agents** pattern:

```
┌──────────────────────────────────────┐
│   root_agent (Coordinator)           │
│   - Routes documents to specialists  │
│   - Determines document type         │
│   - Orchestrates sub-agent calls     │
└──────────────────────────────────────┘
         │      │       │       │
         ▼      ▼       ▼       ▼
    ┌─────────┬─────────┬──────────┬──────────┐
    │Financial│Technical│ Sales    │Marketing │
    │Analyzer │Analyzer │Analyzer  │ Analyzer │
    └─────────┴─────────┴──────────┴──────────┘
         │      │       │       │
         └──────┴───────┴───────┘
              │
       Returns Structured JSON
       (Pydantic Models)
```

### `pubsub_agent/agent.py`

Defines a coordinator agent that routes documents to specialized analyzers:

#### Coordinator Agent: `root_agent`

The main ADK agent that intelligently routes documents:

```python
from pubsub_agent.agent import root_agent

# Agent properties
root_agent.name           # "pubsub_processor"
root_agent.model          # "gemini-2.5-flash"
root_agent.description    # "Event-driven document processing coordinator"
root_agent.tools          # [financial_tool, technical_tool, sales_tool, marketing_tool]
```

#### Specialized Sub-Agents

Each sub-agent is configured with a Pydantic output schema for structured JSON responses:

1. **Financial Analyzer** - Analyzes financial reports, earnings, budgets
   - Extracts: revenue, profit, margins, growth rates, fiscal periods
   - Returns: `FinancialAnalysisOutput` (Pydantic model)

2. **Technical Analyzer** - Analyzes technical docs, architecture, specifications
   - Extracts: technologies, components, deployment info
   - Returns: `TechnicalAnalysisOutput` (Pydantic model)

3. **Sales Analyzer** - Analyzes sales pipelines, deals, forecasts
   - Extracts: customer deals, pipeline value, stages
   - Returns: `SalesAnalysisOutput` (Pydantic model)

4. **Marketing Analyzer** - Analyzes marketing campaigns, engagement metrics
   - Extracts: campaigns, engagement rates, conversion rates
   - Returns: `MarketingAnalysisOutput` (Pydantic model)

#### Using the Coordinator

The agent automatically routes documents based on content analysis:

```python
from google.adk.agents import Runner
from pubsub_agent.agent import root_agent
import asyncio

async def process_document(content: str):
    runner = Runner(root_agent)
    result = await runner.run_async(
        user_id="processor",
        session_id="session_001",
        new_message=f"Analyze this document:\n{content}"
    )
    return result

# Example financial document
financial_doc = "Q4 2024 Financial Report: Revenue $1.2M, Profit 33%"
result = asyncio.run(process_document(financial_doc))
# Agent automatically routes to financial_analyzer
# Returns structured JSON with revenue, profit, recommendations
```

#### Output Schemas

All sub-agents enforce structured JSON output using Pydantic models:

```python
from pubsub_agent.agent import (
    FinancialAnalysisOutput,
    TechnicalAnalysisOutput,
    SalesAnalysisOutput,
    MarketingAnalysisOutput,
    EntityExtraction,
    DocumentSummary
)

# Example: FinancialAnalysisOutput structure
{
    "summary": {
        "main_points": [...],
        "key_insight": "...",
        "summary": "..."
    },
    "entities": {
        "dates": ["2024-10-08"],
        "currency_amounts": ["$1.2M"],
        "percentages": ["35%"],
        "numbers": [...]
    },
    "financial_metrics": {
        "revenue": "$1.2M",
        "profit": "$400K",
        "margin": "33%",
        "growth_rate": "15%"
    },
    "fiscal_periods": ["Q4 2024"],
    "recommendations": [...]
}
```

## Usage Examples

### Local Testing (without GCP)

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_agent.py -v

# Run with coverage
make test-cov
```

### Testing the Coordinator Agent Locally

```python
import asyncio
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pubsub_agent.agent import root_agent

async def test_agent():
    session_service = InMemorySessionService()
    runner = Runner(
        app_name="document_analyzer",
        agent=root_agent,
        session_service=session_service
    )
    
    # Create a session for this test
    session = await session_service.create_session(
        app_name="document_analyzer",
        user_id="test_user"
    )
    
    # Send a test prompt and stream the events
    prompt_content = types.Content(
        role="user",
        parts=[types.Part(text="Analyze this document: [test content]")]
    )
    
    final_result = None
    async for event in runner.run_async(
        user_id="test_user",
        session_id=session.id,
        new_message=prompt_content
    ):
        # Events are streamed as the agent processes
        final_result = event
    
    # Print the final result
    print("Agent response:", final_result)
    return final_result

# Run the test
asyncio.run(test_agent())
```

### Using the ADK Web Interface

For interactive testing with the web UI:

```bash
# Start the ADK web server
adk web

# Visit http://localhost:8000 in your browser
# Select "pubsub_processor" coordinator agent from the dropdown
# Type your document analysis request
```

## Google Cloud Setup (Optional)

To deploy this as a real event-driven pipeline on Google Cloud:

### 0. Prerequisites: gcloud CLI Setup

Before creating resources, you need to authenticate with Google Cloud:

#### A. Install gcloud CLI

If not already installed:

```bash
# macOS (using Homebrew)
brew install --cask google-cloud-sdk

# Or download directly
# https://cloud.google.com/sdk/docs/install

# Verify installation
gcloud --version
```

#### B. Authenticate with Google Cloud

```bash
# Login to your Google Cloud account
gcloud auth login

# This opens a browser window. Sign in with your Google account.
# You'll be asked to grant permissions to the gcloud CLI.
```

#### C. Set Default Project

After authentication, set your default GCP project:

```bash
# List available projects
gcloud projects list

# Set default project (replace with your project ID)
gcloud config set project your-project-id

# Verify it's set
gcloud config get-value project

# You should see: your-project-id
```

#### D. Configure Application Default Credentials (optional but recommended)

```bash
# Set up credentials for local development
gcloud auth application-default login

# This creates local credentials that Python libraries can use
# without additional configuration
```

#### E. Verify Your Setup

```bash
# Show current configuration
gcloud config list

# Example output:
# [core]
# account = you@example.com
# project = your-project-id

# Test authentication
gcloud auth list

# Example output:
# ACTIVE  ACCOUNT
# *       you@example.com
```

### 1. Create GCP Project

```bash
# Create project
gcloud projects create my-agent-pipeline --name="Agent Pipeline"

# Set as active project
gcloud config set project my-agent-pipeline

# Enable APIs
gcloud services enable \
  pubsub.googleapis.com \
  run.googleapis.com \
  aiplatform.googleapis.com
```

### 2. Set Up Pub/Sub

```bash
# Create topic for uploads
gcloud pubsub topics create document-uploads

# Create subscriptions
gcloud pubsub subscriptions create document-processor \
  --topic=document-uploads \
  --ack-deadline=600
```

### 3. Configure Authentication

```bash
# Create service account
gcloud iam service-accounts create agent-pipeline \
  --display-name="Agent Pipeline"

# Grant Pub/Sub permissions
gcloud projects add-iam-policy-binding my-agent-pipeline \
  --member="serviceAccount:agent-pipeline@my-agent-pipeline.iam.gserviceaccount.com" \
  --role="roles/pubsub.publisher"

gcloud projects add-iam-policy-binding my-agent-pipeline \
  --member="serviceAccount:agent-pipeline@my-agent-pipeline.iam.gserviceaccount.com" \
  --role="roles/pubsub.subscriber"

# Create credentials key
gcloud iam service-accounts keys create key.json \
  --iam-account=agent-pipeline@my-agent-pipeline.iam.gserviceaccount.com

# Set environment
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/key.json"
export GCP_PROJECT="my-agent-pipeline"
```

### 4. Publish Documents

Create `publisher.py`:

```python
import os
import json
from google.cloud import pubsub_v1
from datetime import datetime

project_id = os.environ.get("GCP_PROJECT")
topic_id = "document-uploads"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

def publish_document(document_id: str, content: str):
    """Publish a document for processing."""
    message_data = {
        "document_id": document_id,
        "content": content,
        "uploaded_at": datetime.now().isoformat(),
    }

    data = json.dumps(message_data).encode("utf-8")
    future = publisher.publish(topic_path, data)
    message_id = future.result()

    print(f"✅ Published {document_id} (message ID: {message_id})")
    return message_id

# Example: Publish various document types
if __name__ == "__main__":
    # Financial document
    publish_document(
        "DOC-FINANCIAL-001",
        "Q4 2024 Financial Report: Revenue $1.2M, Profit 33%, Growth 15%"
    )
    
    # Technical document
    publish_document(
        "DOC-TECH-001",
        "API Architecture: Using REST with PostgreSQL database, deployed on Kubernetes"
    )
    
    # Sales document
    publish_document(
        "DOC-SALES-001",
        "Sales Pipeline: Acme Corp $500K deal (negotiating), TechStart $250K (open)"
    )
    
    # Marketing document
    publish_document(
        "DOC-MARKETING-001",
        "Campaign Results: 45% engagement, 3.2% conversion, 100K reach, $5K cost"
    )
```

```bash
# Publish documents
python publisher.py
```

### 5. Process Documents with Coordinator Agent

The `subscriber.py` uses the coordinator agent to automatically route and analyze documents:

```python
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
    # Initialize runner with app_name, agent, and session service
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
    
    prompt = f"""Analyze this document and route it to the appropriate analyzer:

Document ID: {document_id}

Content:
{content}

Analyze the document type and extract relevant information."""
    
    # Create a proper Content object for the agent
    message_content = types.Content(
        role="user",
        parts=[types.Part(text=prompt)]
    )
    
    # Agent automatically routes based on document type
    # Note: run_async returns AsyncGenerator, iterate through events
    final_result = None
    async for event in runner.run_async(
        user_id="pubsub_subscriber",
        session_id=session.id,
        new_message=message_content
    ):
        final_result = event
    
    return final_result

def process_message(message):
    """Process Pub/Sub message with async agent processing."""
    try:
        data = json.loads(message.data.decode("utf-8"))
        document_id = data.get("document_id")
        content = data.get("content")

        print(f"\n� Processing: {document_id}")

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

```bash
# Terminal 1 - Subscribe and process
python subscriber.py

# Terminal 2 - Publish (in another terminal)
python publisher.py
```

## Project Structure

```
tutorial34/
├── pubsub_agent/              # Main agent package
│   ├── __init__.py            # Package marker
│   ├── agent.py               # Agent definition with tools
│   └── .env.example           # Environment template
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_agent.py          # Agent and tool tests
│   ├── test_imports.py        # Import validation
│   └── test_structure.py      # Project structure
├── Makefile                   # Development commands
├── pyproject.toml             # Package configuration
├── requirements.txt           # Dependencies
├── README.md                  # This file
├── publisher.py               # Example publisher (optional)
└── subscriber.py              # Example subscriber (optional)
```

## Key Concepts

### Pub/Sub Guarantees

| Feature                    | Benefit                                        |
| -------------------------- | ---------------------------------------------- |
| **At-least-once delivery** | Messages delivered ≥1 time (handle duplicates) |
| **Asynchronous**           | Non-blocking, fast user experience             |
| **Scalable**               | Auto-scales from 0 to millions of messages     |
| **Reliable**               | Built-in retries and error handling            |
| **Fan-out**                | One topic → Multiple subscriptions             |

### Agent Responsibilities

The `root_agent` processes documents by:

1. **Analyzing** document structure and content
2. **Summarizing** key points and findings
3. **Extracting** entities (dates, numbers, currency, etc.)
4. **Classifying** documents by type and topic
5. **Identifying** critical information

### Tool Functions

Each tool returns a structured response:

```python
{
    'status': 'success' | 'error',
    'report': 'Human-readable message',
    'data': {...}  # Tool-specific data
}
```

## Advanced Patterns

### Multiple Subscribers (Fan-out)

One topic can have multiple subscriptions:

```bash
# Create multiple subscriptions
gcloud pubsub subscriptions create summarizer \
  --topic=document-uploads
gcloud pubsub subscriptions create extractor \
  --topic=document-uploads
gcloud pubsub subscriptions create classifier \
  --topic=document-uploads

# Each subscription gets same message independently
```

### Dead Letter Queue (Error Handling)

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

### Message Ordering

Ensure ordered processing:

```bash
# Create ordered topic
gcloud pubsub topics create ordered-documents --message-ordering

# Publish with ordering key
publisher.publish(
    topic_path,
    data,
    ordering_key=f"user_{user_id}"  # Messages ordered per key
)
```

## Troubleshooting

### Issue: "gcloud command not found"

**Solution**: Install Google Cloud CLI

```bash
# macOS
brew install --cask google-cloud-sdk

# Or download from:
# https://cloud.google.com/sdk/docs/install

# After installation, initialize:
gcloud init
```

### Issue: "ERROR: (gcloud.pubsub.topics.create) User does not have permission"

**Cause**: Not authenticated or no project set

**Solution**:

```bash
# 1. Check if logged in
gcloud auth list

# 2. If no active account, login
gcloud auth login

# 3. Check project is set
gcloud config get-value project

# 4. If not set, set it now
gcloud config set project your-project-id

# 5. Verify permissions
gcloud projects get-iam-policy your-project-id
```

### Issue: "ERROR: (gcloud.config.set) Unable to find project"

**Cause**: Project doesn't exist or ID is incorrect

**Solution**:

```bash
# List all your projects
gcloud projects list

# Look for your project ID (not display name)
# Set the correct ID
gcloud config set project correct-project-id

# Verify it's set
gcloud config get-value project
```

### Issue: Application Credentials Error

**Error**: `DefaultCredentialsError: Could not automatically determine credentials`

**Cause**: Application credentials not set for local development

**Solution**:

```bash
# Set up application default credentials
gcloud auth application-default login

# This creates a credentials file at:
# ~/.config/gcloud/application_default_credentials.json

# Python will automatically use this
```

### Issue: "PERMISSION_DENIED: User does not have permission to access topic"

**Cause**: Service account lacks Pub/Sub permissions

**Solution**:

```bash
# Grant Pub/Sub roles to your user account
gcloud projects add-iam-policy-binding your-project-id \
  --member="user:your-email@example.com" \
  --role="roles/pubsub.editor"

# Or for specific permissions only:
gcloud projects add-iam-policy-binding your-project-id \
  --member="user:your-email@example.com" \
  --role="roles/pubsub.admin"
```

### Issue: "Messages Not Delivered"

**Solution**: Check subscription exists and has listeners

```bash
# List subscriptions
gcloud pubsub subscriptions list

# Pull a message manually
gcloud pubsub subscriptions pull document-processor --limit=1
```

### Issue: "High Latency"

**Solution**: Increase parallelism

```python
flow_control = pubsub_v1.types.FlowControl(
    max_messages=10,  # Process 10 at once
    max_bytes=10 * 1024 * 1024
)

subscriber.subscribe(
    subscription_path,
    callback=process_message,
    flow_control=flow_control
)
```

### Issue: "Messages Re-delivered"

**Solution**: Implement idempotency

```python
processed_ids = set()

def process_message(message):
    if message.message_id in processed_ids:
        message.ack()  # Already processed
        return

    # Process...
    processed_ids.add(message.message_id)
    message.ack()
```

## Testing

### Run All Tests

```bash
make test
```

### Run Specific Tests

```bash
# Agent functionality tests
pytest tests/test_agent.py -v

# Import and module tests
pytest tests/test_imports.py -v

# Project structure tests
pytest tests/test_structure.py -v
```

### Test Coverage

```bash
make test-cov
```

## Next Steps

1. **Deploy to Cloud Run**: Scale agent processing across regions
2. **Add UI**: Build real-time dashboard with WebSocket updates
3. **Monitor**: Set up Cloud Monitoring and alerts
4. **Optimize**: Use message ordering and batch processing
5. **Integrate**: Connect to external services (Firestore, Storage, etc.)

## Resources

- [Google Cloud Pub/Sub Documentation](https://cloud.google.com/pubsub/docs)
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Python Pub/Sub Client](https://cloud.google.com/python/docs/reference/pubsub)
- [Pub/Sub Best Practices](https://cloud.google.com/pubsub/docs/best-practices)
- [Tutorial 34 Full Guide](../../docs/tutorial/34_pubsub_adk_integration.md)

## Commands Summary

```bash
# Setup
make setup              # Install dependencies

# Development
make demo               # Show demo instructions
make test               # Run all tests
make test-cov           # Run tests with coverage

# Cleanup
make clean              # Remove cache and artifacts
```

## Author Notes

This tutorial demonstrates how to build event-driven architectures with
Google ADK. The key insight is that **decoupling publishers from
processors** enables:

- **Scalability**: Process millions of messages
- **Reliability**: Built-in retries and error handling
- **Flexibility**: Add new subscribers without modifying publishers
- **Efficiency**: Asynchronous processing doesn't block users

The patterns here apply to document processing, image analysis, data
classification, and many other real-world scenarios.

---

**Tutorial 34** | [Tutorial Index](../../docs/tutorial/)
