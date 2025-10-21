---
id: pubsub_adk_integration
title: "Tutorial 34: Google Cloud Pub/Sub + Event-Driven Agents"
description: "Build event-driven document processing pipelines with Google Cloud Pub/Sub and ADK agents for asynchronous processing."
sidebar_label: "34. Pub/Sub Event Agents"
sidebar_position: 34
tags: ["cloud", "pubsub", "event-driven", "python", "agents"]
keywords:
  ["pubsub", "google cloud", "event-driven", "agent", "python", "coordinator"]
status: "updated"
difficulty: "advanced"
estimated_time: "1 hour"
prerequisites:
  [
    "Tutorial 01: Hello World Agent",
    "Google Cloud project",
    "Python experience",
  ]
learning_objectives:
  - "Build multi-agent systems with a coordinator agent"
  - "Use Pydantic for structured JSON output"
  - "Implement event-driven document processing"
  - "Deploy to Google Cloud Pub/Sub for asynchronous processing"
implementation_link: "https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial34"
---

import Comments from '@site/src/components/Comments';


This tutorial implements a real event-driven document processing system using
Google Cloud Pub/Sub and ADK agents. It demonstrates a coordinator + specialist
agents pattern with structured JSON output using Pydantic models.
Verified as of October 2025 with latest ADK and Gemini 2.5 Flash.

**Estimated Reading Time**: 50-60 minutes  
**Difficulty Level**: Advanced  
**Prerequisites**: Tutorial 01-03 (ADK Basics), Google Cloud project

---

## 🚀 Quick Start - Working Implementation

The easiest way to get started is with our **complete working implementation**:

```bash
cd tutorial_implementation/tutorial34
make setup      # Install dependencies
make test       # Run all tests
```

[📁 View Full Implementation](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial34)

**What's included:**

- ✅ `root_agent`: Coordinator agent that routes documents to specialists
- ✅ 4 Specialist agents: Financial, Technical, Sales, Marketing analyzers
- ✅ Pydantic output schemas: Structured JSON results
- ✅ 66 comprehensive tests (all passing)
- ✅ Real-world example code ready to run

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites & Setup](#prerequisites--setup)
3. [Understanding the Architecture](#understanding-the-architecture)
4. [Core Components](#core-components)
5. [Running Locally](#running-locally)
6. [Google Cloud Deployment](#google-cloud-deployment)
7. [Troubleshooting](#troubleshooting)
8. [Next Steps](#next-steps)

---

## Overview

### What You'll Build

In this tutorial, you'll build an **event-driven document processing system** using:

- **Google Cloud Pub/Sub** (Event messaging)
- **Google ADK** (Multi-agent coordination)
- **Gemini 2.5 Flash** (Document analysis)
- **Pydantic Models** (Structured JSON output)

**Architecture**:

```text
┌─────────────────────────────────────────────────────┐
│  Publisher: Sends documents to Pub/Sub              │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────▼────────────┐
         │  Google Cloud Pub/Sub  │
         │  (document-uploads)    │
         └───────────┬────────────┘
                     │
         ┌───────────▼────────────┐
         │  root_agent (Coordinator)
         │  - Routes documents    │
         │  - Coordinates analysis│
         └───────────┬────────────┘
                     │
         ┌──┬──┬──┬──┘
         │  │  │  │
    ┌────▼┐ │ ┌┴────┬─────────┐
    │Fin. │ │ │Tech │ Sales  Marketing
    │Anal.│ │ │Anal.│Analyst Analyst
    └─────┘ │ └─────┴────────┘
```

### Why Pub/Sub + ADK?

| Feature          | Benefit                        |
| ---------------- | ------------------------------ |
| **Asynchronous** | Non-blocking processing        |
| **Decoupled**    | Publishers and subscribers independent |
| **Scalable**     | Auto-scales message volume     |
| **Structured**   | Pydantic models for JSON       |
| **Reliable**     | At-least-once delivery, retries|

**When to use Pub/Sub + ADK:**

✅ Asynchronous document processing  
✅ Multi-step workflows  
✅ Event-driven architectures  
✅ Systems with strict output schemas  
✅ Google Cloud deployments

❌ Real-time chat interfaces → Use Next.js/WebSocket  
❌ Simple synchronous calls → Use direct API

---

## Prerequisites & Setup

### Local Testing (No GCP Required)

To get started without Google Cloud:

```bash
# Install dependencies
cd tutorial_implementation/tutorial34
make setup

# Run tests - verifies agent configuration
make test

# This works completely locally using in-memory processing
```

### Google Cloud Setup (Optional - For Real Pub/Sub)

To deploy with real Google Cloud Pub/Sub:

#### 1. Install gcloud CLI

```bash
# macOS
brew install --cask google-cloud-sdk

# Then initialize
gcloud init
```

#### 2. Authenticate

```bash
# Login to Google Cloud
gcloud auth login

# Set default project
gcloud config set project your-project-id

# Verify authentication
gcloud auth list
```

#### 3. Create Pub/Sub Resources

```bash
# Enable Pub/Sub API
gcloud services enable pubsub.googleapis.com

# Create topic
gcloud pubsub topics create document-uploads

# Create subscription
gcloud pubsub subscriptions create document-processor \
  --topic=document-uploads \
  --ack-deadline=600
```

#### 4. Set Environment Variables

```bash
# Set your GCP project
export GCP_PROJECT="your-project-id"

# Set Gemini API key
export GOOGLE_API_KEY="your_gemini_api_key"

# Set application credentials
gcloud auth application-default login
```

---

## Understanding the Architecture

### The Coordinator + Specialist Pattern

This implementation uses a **coordinator agent** that intelligently routes documents to specialized analyzers:

```text
┌──────────────────────────────────────────────────────┐
│  root_agent (Coordinator)                            │
│  - Analyzes document type                            │
│  - Routes to appropriate analyzer                    │
│  - Coordinates specialized agents                    │
└───────┬──────────────────────────────────────────────┘
        │
    ┌───┴───┬─────────────┬──────────────┐
    │       │             │              │
┌───▼──┐ ┌──▼───┐ ┌───────▼───┐   ┌──────▼──┐
│Finan.│ │Tech. │ │Sales      │   │Marketing
│Anal. │ │Anal. │ │Analyst    │   │Analyst
└──────┘ └──────┘ └───────────┘   └─────────┘
    │        │             │              │
    └────────┴─────────────┴──────────────┘
              │
     Structured JSON Output
     (Pydantic Models)
```

### Key Components

1. **root_agent** (`pubsub_agent/agent.py`):
   - Coordinator that routes documents to specialists
   - Analyzes document type and content
   - Calls appropriate sub-agent tool
   - Returns structured analysis

2. **Sub-Agents** (financial, technical, sales, marketing):
   - Specialized analyzers for document types
   - Enforce structured JSON via Pydantic output_schema
   - Extract type-specific metrics and insights

3. **Pydantic Output Schemas**:
   - `FinancialAnalysisOutput`: Revenue, profit, metrics
   - `TechnicalAnalysisOutput`: Technologies, components
   - `SalesAnalysisOutput`: Deals, pipeline value
   - `MarketingAnalysisOutput`: Campaigns, engagement metrics

### Pub/Sub Guarantees

| Feature          | Description                      |
| ---------------- | -------------------------------- |
| **At-least-once**| Messages delivered ≥1 time       |
| **Asynchronous** | Non-blocking processing          |
| **Scalable**     | Auto-scales message volume       |
| **Durable**      | Messages stored in topics        |
| **Reliable**     | Automatic retries on failure     |

---

## Core Components

### Agent Configuration

View the agent at `pubsub_agent/agent.py`:

```python
# Coordinator agent
root_agent = LlmAgent(
    name="pubsub_processor",
    model="gemini-2.5-flash",
    description="Event-driven document processing coordinator",
    instruction="Routes documents to specialized analyzers",
    tools=[financial_tool, technical_tool, sales_tool, marketing_tool],
)

# Sub-agents (financial, technical, sales, marketing)
# Each configured with output_schema for structured JSON
```

### Output Schemas

All sub-agents return structured Pydantic models:

```python
# Financial documents return:
FinancialAnalysisOutput(
    summary: DocumentSummary,
    entities: EntityExtraction,
    financial_metrics: FinancialMetrics,
    fiscal_periods: list[str],
    recommendations: list[str]
)

# Technical documents return:
TechnicalAnalysisOutput(
    summary: DocumentSummary,
    entities: EntityExtraction,
    technologies: list[str],
    components: list[str],
    recommendations: list[str]
)

# Similar for Sales and Marketing analyzers
```

### Example Usage

**Locally without GCP**:

```bash
cd tutorial_implementation/tutorial34
make test
```

**Test the agent in code**:

```python
import asyncio
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pubsub_agent.agent import root_agent

async def test_document_analysis():
    session_service = InMemorySessionService()
    runner = Runner(
        app_name="document_analyzer",
        agent=root_agent,
        session_service=session_service
    )
    
    session = await session_service.create_session(
        app_name="document_analyzer",
        user_id="test_user"
    )
    
    prompt = types.Content(
        role="user",
        parts=[types.Part(
            text="Analyze: Revenue $1.2M, Profit 33%, Q4 2024"
        )]
    )
    
    async for event in runner.run_async(
        user_id="test_user",
        session_id=session.id,
        new_message=prompt
    ):
        print("Response:", event)

asyncio.run(test_document_analysis())
```

**Using ADK Web Interface**:

```bash
adk web
```

Then visit `http://localhost:8000` and select `pubsub_processor` from
the agent dropdown.

---

## Running Locally

### Without Pub/Sub (Local Testing)

```bash
cd tutorial_implementation/tutorial34

# Run all tests
make test

# See test coverage
make test-cov
```

Tests validate:
- Agent configuration
- Sub-agent setup
- Pydantic output schemas
- Agent imports and structure

### With Pub/Sub (Google Cloud)

After setting up GCP (see Prerequisites), run publisher and subscriber:

**Terminal 1 - Start subscriber**:

```bash
export GCP_PROJECT="your-project-id"
export GOOGLE_API_KEY="your_api_key"

python subscriber.py
```

**Terminal 2 - Publish documents**:

```bash
export GCP_PROJECT="your-project-id"

python publisher.py
```

The subscriber will process each document with the coordinator agent.

---

## Google Cloud Deployment

### Step 1: Set Up Pub/Sub Resources

```bash
gcloud pubsub topics create document-uploads
gcloud pubsub subscriptions create document-processor \
  --topic=document-uploads \
  --ack-deadline=600
```

### Step 2: Run Subscriber

```bash
export GCP_PROJECT=$(gcloud config get-value project)
export GOOGLE_API_KEY="your_api_key"

python subscriber.py
```

### Step 3: Publish Documents

```bash
python publisher.py
```

The subscriber will automatically process each Pub/Sub message using
the coordinator agent.


---

## Troubleshooting

### Common Issues

#### Issue 1: gcloud command not found

**Cause**: Google Cloud CLI not installed

**Solution**:

```bash
# macOS
brew install --cask google-cloud-sdk

# After installation, verify
gcloud --version
```

---

#### Issue 2: Agent not found when running locally

**Cause**: Agent module not properly installed

**Solution**:

```bash
cd tutorial_implementation/tutorial34

# Install in development mode
pip install -e .

# Verify agent imports
python -c "from pubsub_agent.agent import root_agent; print(root_agent.name)"
```

---

#### Issue 3: Tests fail with import errors

**Cause**: Dependencies not installed

**Solution**:

```bash
cd tutorial_implementation/tutorial34

# Install dependencies
make setup

# Or manually
pip install -r requirements.txt

# Run tests
make test
```

---

#### Issue 4: Messages Not Delivered on Pub/Sub

**Cause**: Subscription not receiving published messages

**Solution**:

```bash
# Verify subscription exists
gcloud pubsub subscriptions list

# Check subscription details
gcloud pubsub subscriptions describe document-processor

# Manually pull a message to test
gcloud pubsub subscriptions pull document-processor --limit=1

# Check IAM permissions
gcloud pubsub subscriptions get-iam-policy document-processor
```

---

#### Issue 5: Pub/Sub Authentication Error

**Error**: `DefaultCredentialsError: Could not automatically determine credentials`

**Solution**:

```bash
# Set up application default credentials
gcloud auth application-default login

# Or set explicit credentials
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"

# Verify setup
gcloud auth list
```

---

#### Issue 6: Tests fail with "GOOGLE_API_KEY not set"

**Cause**: Gemini API key not configured

**Solution**:

```bash
# Set your Gemini API key
export GOOGLE_API_KEY="your_actual_api_key"

# Verify it's set
echo $GOOGLE_API_KEY

# Run tests again
make test
```

---

#### Issue 7: Agent processes documents but returns empty results

**Cause**: Model not returning expected output format

**Solution**:

- Verify GOOGLE_API_KEY is set and valid
- Check that the document content is clear and valid
- Review agent instructions in `pubsub_agent/agent.py`
- Test with a simple document first

```python
# Test the agent directly
import asyncio
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pubsub_agent.agent import root_agent

async def test():
    session_service = InMemorySessionService()
    runner = Runner(
        app_name="test",
        agent=root_agent,
        session_service=session_service
    )
    session = await session_service.create_session(
        app_name="test",
        user_id="test"
    )
    message = types.Content(
        role="user",
        parts=[types.Part(text="Revenue $1M, Profit 30%")]
    )
    async for event in runner.run_async(
        user_id="test",
        session_id=session.id,
        new_message=message
    ):
        print(event)

asyncio.run(test())
```

---

## Next Steps

### You've Mastered Event-Driven Agents with Pub/Sub! 🎉

You now know how to:

✅ Build multi-agent coordinator systems  
✅ Use Pydantic for structured JSON output  
✅ Implement async agent processing  
✅ Route documents to specialized analyzers  
✅ Use Google Cloud Pub/Sub for event-driven processing  
✅ Test agents locally without GCP  
✅ Deploy to production with Pub/Sub integration

### Key Patterns Learned

- **Coordinator + Specialist**: One agent routes to many specialized agents
- **Structured Output**: Pydantic models enforce JSON schemas
- **Async Processing**: Non-blocking document analysis
- **Event-Driven**: Pub/Sub handles message buffering and retries
- **Tool Composition**: Sub-agents as tools within coordinator

### Continue Learning

**Tutorial 29**: UI Integration Overview  
Compare all integration approaches (Next.js, Vite, Streamlit, etc.)

**Tutorial 30**: Next.js + CopilotKit Integration  
Build real-time chat interfaces with React

**Tutorial 35+**: Advanced Patterns  
Master deployment, scaling, and production optimization

### Additional Resources

- [Google Cloud Pub/Sub Documentation](https://cloud.google.com/pubsub/docs)
- [ADK Documentation](https://google.github.io/adk-docs/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Gemini API Reference](https://ai.google.dev/docs)

---

**🎉 Tutorial 34 Complete!**

You've successfully built an event-driven document processing system
with a multi-agent coordinator architecture. This pattern scales to
millions of documents while maintaining structured, validated output.

---

**Questions or feedback?** Open an issue on the
[ADK Training Repository](https://github.com/raphaelmansuy/adk_training).
<Comments />
