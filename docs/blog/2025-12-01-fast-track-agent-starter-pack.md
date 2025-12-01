---
title: "Fast-track Your GenAI Agents: Deep Dive into the Google Cloud Agent Starter Pack"
authors:
  - name: ADK Training Team
    title: Google ADK Training
    url: https://github.com/raphaelmansuy/adk_training
    image_url: https://github.com/raphaelmansuy.png
tags: [agent-starter-pack, gcp, genai, observability, production, vertex]
---

Building a GenAI agent prototype on your laptop is magic. You write a few lines of Python, hook up an LLM, and suddenly you’re chatting with your data. But taking that magic from a Jupyter notebook to a production environment—secure, scalable, and observable—is where the real headache begins.

Enter the **Google Cloud Agent Starter Pack**.

This open-source repository is Google’s answer to the "prototype purgatory" problem. It’s a comprehensive toolkit designed to bootstrap production-ready generative AI agents on Google Cloud Platform (GCP) in minutes, not months.

<!--truncate-->

## Why Should You Care?

Most tutorials stop at `print(response.text)`. The Agent Starter Pack picks up where they leave off, handling the unsexy-but-critical infrastructure work so you can focus on your agent's cognitive architecture.

Here is what makes it a game-changer:

- **Production-First Mindset:** It doesn't just give you code; it gives you Terraform scripts for infrastructure, CI/CD pipelines (GitHub Actions or Cloud Build), and security best practices out of the box.
- **Observability Built-In:** Debugging LLMs is hard. This pack integrates OpenTelemetry to automatically log traces and metrics to Cloud Logging and BigQuery, letting you inspect exactly what your agent is "thinking." 
- **Flexible Deployment:** Deploy seamlessly to **Cloud Run** for serverless simplicity or the new **Vertex AI Agent Engine** for a managed agent runtime.

## Architecture & Templates

The Agent Starter Pack covers the full lifecycle of agent development—from prototyping and evaluation to deployment and monitoring:

![Agent Starter Pack High-Level Architecture](https://github.com/GoogleCloudPlatform/agent-starter-pack/raw/main/docs/images/ags_high_level_architecture.png)

The starter pack isn't a "one-size-fits-all" monolith. It includes several architectural templates tailored to common use cases:

1.  **LangGraph Base ReAct:** A classic "Reason and Act" agent built with LangChain's LangGraph. Perfect for complex reasoning workflows and graph-based state management.
2.  **Agentic RAG:** A Retrieval-Augmented Generation agent with automated data ingestion, supporting **Vertex AI Search** and **Vertex AI Vector Search**.
3.  **ADK Base:** Google's minimal ReAct agent example—ideal for getting started with ADK and understanding agent fundamentals.
4.  **ADK Live:** A real-time multimodal agent supporting simultaneous audio, video, and text interactions with low-latency WebSocket communication.

### Available ADK Templates

The starter pack includes official Google ADK-based templates:

- **ADK Base (`adk_base`)**: A minimal ReAct agent demonstrating core ADK concepts like agent creation and tool integration. This is the go-to starting point for learning ADK and building general-purpose conversational agents.

- **ADK A2A Base (`adk_a2a_base`)**: An ADK agent with Agent2Agent (A2A) Protocol support for distributed agent communication and interoperability across frameworks and languages. Ideal for building microservices-based agent architectures.

- **Agentic RAG (Built on ADK)**: A production-ready RAG system with automated data ingestion, supporting both Vertex AI Search and Vertex AI Vector Search for semantic retrieval.

- **ADK Live (`adk_live`)**: A real-time multimodal RAG agent powered by Gemini, supporting simultaneous audio, video, and text interactions with low-latency WebSocket communication.

Each template comes with:
- Complete source code and architecture documentation
- Production-grade infrastructure (Terraform scripts for Cloud Run or Vertex AI Agent Engine)
- CI/CD pipelines (GitHub Actions or Google Cloud Build)
- Built-in observability with OpenTelemetry and Cloud Logging
- Comprehensive test suites and deployment guides

## getting Started: From Zero to Deployed

Let’s look at how easy it is to spin up a new project.

### 1. Install the CLI (Quick Start with uvx)

The fastest way—no installation needed:

```bash
uvx agent-starter-pack create my-production-agent
```

Or, install and run locally:

```bash
pip install agent-starter-pack
agent-starter-pack create my-production-agent
```

### 2. Create Your Agent

Run the create command and select your template (e.g., `adk_base`, `langgraph_base`, `agentic_rag`) and deployment target (Cloud Run or Vertex AI Agent Engine).

The `create` command will scaffold your entire project with the chosen template.

### 3. Deploy

The generated project includes a `Makefile` and complete Terraform infrastructure-as-code. Deploy with:

```bash
cd my-production-agent
make deploy
```

This provisions all resources (IAM roles, APIs, CI/CD, monitoring) on Google Cloud automatically.

## Using Google ADK as an example agent runtime

If you already use the Google ADK framework for building agents, the Starter Pack can integrate smoothly with ADK-centric workflows. For example, if you choose the `adk_base` template, the generated code follows standard ADK patterns, allowing you to run it locally via `adk web` for interactive development.

A minimal integration example (based on the `adk_base` template):

```python
# my_production_agent/app/agent.py
from google.adk.agents import Agent
from google.adk.apps.app import App

def get_weather(city: str) -> str:
    return "It's sunny!"

root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    instruction="You are a helpful AI assistant.",
    tools=[get_weather],
)

# The App wrapper enables ADK runtime features
app = App(root_agent=root_agent, name="app")
```

This lets you develop with ADK's rich developer tools (repl, tracing, and testing) while still leveraging the Starter Pack's opinionated infra, CI/CD, and observability patterns.

## The "Secret Sauce": Observability

One of the standout features is how it handles telemetry. By default, the starter pack instruments your agent to capture:

- **Token Usage:** distinct input/output token counts for cost tracking.
- **Latency:** How long each step of the chain takes.
- **Trace Data:** Visualize the entire execution path in the Google Cloud Console.

This means you can go into **BigQuery** and run SQL queries against your agent's conversation history to evaluate performance or spot hallucinations.

## Conclusion

The Google Cloud Agent Starter Pack bridges the gap between "it works on my machine" and "it works for our customers." If you are building agents on GCP, this repository is the best place to start your journey.

**Ready to build?**
Check out the repository here: [github.com/GoogleCloudPlatform/agent-starter-pack](https://github.com/GoogleCloudPlatform/agent-starter-pack)
