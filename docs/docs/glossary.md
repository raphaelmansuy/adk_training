---
id: glossary
title: Glossary - ADK Terms and Concepts
description: Comprehensive glossary of Google Agent Development Kit (ADK) terms, concepts, and terminology used throughout the tutorials.
sidebar_label: Glossary
keywords:
  [
    "ADK glossary",
    "agent development kit terms",
    "ADK concepts",
    "terminology",
    "definitions",
  ]
---

# Glossary - ADK Terms and Concepts

**🎯 Purpose**: Comprehensive reference for Google Agent Development Kit (ADK) terminology and concepts used throughout the tutorials.

**📚 Source of Truth**: [google/adk-python](https://github.com/google/adk-python) (ADK 1.15) + Official Google Documentation

---

## A

### Agent

A complete AI system powered by a Large Language Model (LLM) that can perform tasks through tools, maintain state, and interact with users. Agents are more than just LLMs - they include reasoning, tools, memory, and instructions.

**See Also**: [Tutorial 01: Hello World Agent](01_hello_world_agent.md)

### Agent-to-Agent (A2A) Communication

Protocol for agents to communicate and collaborate with each other, enabling distributed multi-agent systems.

**See Also**: [Tutorial 17: Agent-to-Agent Communication](17_agent_to_agent.md)

### Agent Engine

Google Cloud's managed service for deploying and scaling agents on Vertex AI, providing built-in scaling, monitoring, and version management.

**See Also**: [Tutorial 23: Production Deployment](23_production_deployment.md)

## B

### Built-in Tools

Pre-built tools provided by Google ADK for common operations like web search, location services, and code execution.

**See Also**: [Tutorial 11: Built-in Tools & Grounding](11_built_in_tools_grounding.md)

## C

### Callbacks

Functions that execute at specific points in an agent's lifecycle (before/after agent runs, tool calls, etc.) for monitoring, guardrails, and control flow.

**See Also**: [Tutorial 09: Callbacks & Guardrails](09_callbacks_guardrails.md)

### Context Window

The maximum amount of text (measured in tokens) that an LLM can process at once. Exceeding this limit causes errors.

### CopilotKit

React component library for building AI chat interfaces that integrate with ADK agents.

## E

### Evaluation

Systematic testing and quality assessment of agent behavior using automated metrics and human review.

**See Also**: [Tutorial 10: Evaluation & Testing](10_evaluation_testing.md)

### Events

Structured logging system that tracks agent execution, state changes, tool calls, and errors for debugging and monitoring.

**See Also**: [Tutorial 18: Events & Observability](18_events_observability.md)

## F

### Function Tools

Regular Python functions that agents can call to perform specific tasks. ADK automatically generates schemas from function signatures and docstrings.

**See Also**: [Tutorial 02: Function Tools](02_function_tools.md)

## G

### Gemini

Google's family of multimodal large language models, including Gemini 1.5, Gemini 2.0, etc.

**See Also**: [Tutorial 22: Model Selection](22_model_selection.md)

### Grounding

Connecting LLM responses to real-world data and facts through tools like web search, databases, and APIs to ensure accuracy.

**See Also**: [Tutorial 11: Built-in Tools & Grounding](11_built_in_tools_grounding.md)

### Guardrails

Safety mechanisms and validation rules that prevent agents from performing harmful actions or generating inappropriate content.

**See Also**: [Tutorial 09: Callbacks & Guardrails](09_callbacks_guardrails.md)

## L

### Large Language Model (LLM)

AI models trained on vast amounts of text data that can understand and generate human-like text. Examples: Gemini, GPT-4, Claude.

### Loop Agent

Workflow agent that iteratively refines output through critic/refiner patterns until quality criteria are met.

**See Also**: [Tutorial 07: Loop Agents](07_loop_agents.md)

## M

### Memory Service

Persistent storage system for long-term agent memory, enabling agents to recall information across sessions.

**See Also**: [Tutorial 08: State & Memory](08_state_memory.md)

### Model Context Protocol (MCP)

Standardized protocol for tool communication between agents and external services, enabling interoperability.

**See Also**: [Tutorial 16: MCP Integration](16_mcp_integration.md)

### Multi-Agent Systems

Architectures where multiple specialized agents work together to accomplish complex tasks.

**See Also**: [Tutorial 06: Multi-Agent Systems](06_multi_agent_systems.md)

## O

### Observability

The ability to monitor, debug, and understand agent behavior through logging, metrics, and tracing.

**See Also**: [Tutorial 18: Events & Observability](18_events_observability.md), [Tutorial 24: Advanced Observability](24_advanced_observability.md)

### OpenAPI Tools

Tools automatically generated from OpenAPI/Swagger specifications, allowing agents to call REST APIs without manual coding.

**See Also**: [Tutorial 03: OpenAPI Tools](03_openapi_tools.md)

### Output Key

Configuration that automatically saves an agent's response to session state for later retrieval.

**See Also**: [Tutorial 08: State & Memory](08_state_memory.md)

## P

### Parallel Agent

Workflow agent that executes multiple sub-agents simultaneously for improved performance on independent tasks.

**See Also**: [Tutorial 05: Parallel Processing](05_parallel_processing.md)

### Planners

Advanced reasoning components that help agents break down complex tasks and create execution plans.

**See Also**: [Tutorial 12: Planners & Thinking](12_planners_thinking.md)

### Production Deployment

Strategies for deploying agents to production environments with scalability, reliability, and monitoring.

**See Also**: [Tutorial 23: Production Deployment](23_production_deployment.md)

## R

### Runner

ADK component that executes agents, manages state, and coordinates tool calls.

## S

### Sequential Agent

Workflow agent that executes sub-agents in order, where each step depends on the previous step's output.

**See Also**: [Tutorial 04: Sequential Workflows](04_sequential_workflows.md)

### Session State

Key-value storage that persists data within a conversation session but is discarded when the session ends.

**See Also**: [Tutorial 08: State & Memory](08_state_memory.md)

### State Management

System for storing and retrieving data across agent interactions, with different scopes (session, user, app, temp).

**See Also**: [Tutorial 08: State & Memory](08_state_memory.md)

### Streaming

Real-time response generation where the agent sends partial responses as they are generated, rather than waiting for completion.

**See Also**: [Tutorial 14: Streaming & SSE](14_streaming_sse.md)

### Server-Sent Events (SSE)

HTTP standard for real-time communication from server to client, used for streaming agent responses.

**See Also**: [Tutorial 14: Streaming & SSE](14_streaming_sse.md)

## T

### Tool Context

Object passed to tool functions containing state, session information, and execution context.

### Tools

Capabilities that extend agent functionality beyond LLM reasoning. Types include function tools, OpenAPI tools, MCP tools, and built-in tools.

**See Also**: [Tools & Capabilities](tools-capabilities.md)

## V

### Vertex AI

Google Cloud's machine learning platform that provides managed AI services including Gemini models and Agent Engine.

## W

### Workflow Agents

Agents that orchestrate other agents in structured patterns: sequential, parallel, and loop workflows.

**See Also**: [Workflows & Orchestration](workflows-orchestration.md)

---

## Quick Reference Tables

### Agent Types

| Type                 | Purpose                             | Example Use Case                   |
| -------------------- | ----------------------------------- | ---------------------------------- |
| **LLM Agent**        | Flexible reasoning and conversation | Customer support, content creation |
| **Sequential Agent** | Ordered, dependent steps            | Blog writing pipeline              |
| **Parallel Agent**   | Independent concurrent tasks        | Research gathering                 |
| **Loop Agent**       | Iterative refinement                | Code review and improvement        |

### State Scopes

| Prefix  | Scope              | Persistence              | Example                  |
| ------- | ------------------ | ------------------------ | ------------------------ |
| (none)  | Current session    | SessionService dependent | `state['topic']`         |
| `user:` | All user sessions  | Persistent               | `state['user:language']` |
| `app:`  | All users/sessions | Persistent               | `state['app:settings']`  |
| `temp:` | Current invocation | Never persisted          | `state['temp:calc']`     |

### Tool Types

| Type               | Source           | Example                      |
| ------------------ | ---------------- | ---------------------------- |
| **Function Tools** | Python functions | Custom business logic        |
| **OpenAPI Tools**  | REST API specs   | Weather, news APIs           |
| **MCP Tools**      | MCP servers      | Filesystem, databases        |
| **Built-in Tools** | Google ADK       | Search, maps, code execution |

### Workflow Patterns

| Pattern        | Execution                 | Use Case                   |
| -------------- | ------------------------- | -------------------------- |
| **Sequential** | One after another         | Assembly line processes    |
| **Parallel**   | All at once               | Independent research tasks |
| **Loop**       | Repeat until criteria met | Quality improvement cycles |

---

## Contributing to the Glossary

This glossary is maintained alongside the ADK tutorials. When new concepts are introduced:

1. Add the term with a clear definition
2. Include "See Also" links to relevant tutorials
3. Update related terms if needed
4. Keep definitions concise but comprehensive

**Last Updated**: October 2025
**ADK Version**: 1.15
