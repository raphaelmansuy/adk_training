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
│  Publisher                                                    │
│  └─ Sends documents to Pub/Sub topic                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│  Google Cloud Pub/Sub                                        │
│  └─ Buffers and distributes messages                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
      ┌───────────────┼───────────────┐
      │               │               │
┌─────▼──────┐  ┌────▼────┐  ┌───────▼──────┐
│ Summarizer │  │Extractor│  │  Classifier  │
│ Subscriber │  │Subscriber│  │  Subscriber  │
└────────────┘  └─────────┘  └──────────────┘
      │               │               │
      └───────────────┼───────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│  Results Storage                                             │
│  └─ Save processed results and status                       │
└─────────────────────────────────────────────────────────────┘
```

## Components

### `pubsub_agent/agent.py`

The main document processing agent with three tool functions:

#### 1. `summarize_content(content: str)`

Summarizes document content by extracting key lines.

```python
from pubsub_agent.agent import summarize_content

result = summarize_content("Your document text here...")
print(result)
# {
#     'status': 'success',
#     'report': 'Content summarized successfully',
#     'summary': 'Summary text...',
#     'original_length': 150,
#     'summary_length': 45
# }
```

#### 2. `extract_entities(content: str)`

Extracts structured entities from documents:

- **Dates**: Patterns like `2024-10-08`, `10/15/2024`
- **Currency**: Patterns like `$1,200.50`
- **Percentages**: Patterns like `35%`
- **Numbers**: Integer values in text

```python
from pubsub_agent.agent import extract_entities

result = extract_entities("Revenue: $1.2M (35% growth) on 2024-10-08")
print(result)
# {
#     'status': 'success',
#     'entities': {
#         'dates': ['2024-10-08'],
#         'currency': ['$1.2M'],
#         'percentages': ['35%'],
#         'numbers': [...]
#     },
#     'entity_count': 3
# }
```

#### 3. `classify_document(content: str)`

Classifies documents by type and topic:

```python
from pubsub_agent.agent import classify_document

result = classify_document("Q4 financial report with revenue and profit metrics...")
print(result)
# {
#     'status': 'success',
#     'primary_type': 'financial',
#     'confidence_scores': {'financial': 3},
#     'content_length': 150
# }
```

### `root_agent`

The main ADK agent configured for processing documents in event-driven pipelines:

```python
from pubsub_agent.agent import root_agent

# Agent properties
root_agent.name  # "pubsub_processor"
root_agent.model  # "gemini-2.0-flash"
root_agent.description  # "Event-driven document processing agent"
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

### Testing Tool Functions Locally

```python
from pubsub_agent.agent import summarize_content, extract_entities, classify_document

# Test summarization
document = """
Q4 2024 Sales Report
Date: 2024-10-08

Revenue: $1,200,000
Expenses: $800,000
Profit: $400,000 (33% margin)
"""

summary = summarize_content(document)
print(f"Summary: {summary['summary']}")

entities = extract_entities(document)
print(f"Entities: {entities['entities']}")

classification = classify_document(document)
print(f"Type: {classification['primary_type']}")
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

```pythonpython
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

# Example
if __name__ == "__main__":
    publish_document(
        "DOC-001",
        "Q4 2024 Financial Report: Revenue $1.2M, Profit 33%"
    )
```

```bash
# Publish documents
python publisher.py
```

### 5. Process Documents

Create `subscriber.py`:

```python
import os
import json
from google.cloud import pubsub_v1
from pubsub_agent.agent import summarize_content, extract_entities, classify_document

project_id = os.environ.get("GCP_PROJECT")
subscription_id = "document-processor"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def process_message(message):
    """Process Pub/Sub message."""
    try:
        data = json.loads(message.data.decode("utf-8"))
        document_id = data.get("document_id")
        content = data.get("content")

        print(f"\n🔄 Processing {document_id}...")

        # Use agent's tools
        summary = summarize_content(content)
        entities = extract_entities(content)
        classification = classify_document(content)

        result = {
            "document_id": document_id,
            "summary": summary,
            "entities": entities,
            "classification": classification
        }

        print(f"✅ Completed {document_id}")
        print(f"   Type: {classification['primary_type']}")
        print(f"   Summary: {summary['summary'][:50]}...")

        # Acknowledge message (remove from queue)
        message.ack()

    except Exception as e:
        print(f"❌ Error: {e}")
        message.nack()

# Subscribe and process
streaming_pull_future = subscriber.subscribe(
    subscription_path,
    callback=process_message
)

print(f"🚀 Processor running. Waiting for messages...")

try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
    print("\n✋ Stopped")
```

```bash
# Terminal 1 - Subscribe
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
