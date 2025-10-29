# Google ADK Tutorial Series - Table of Contents

**🎉 Status: COMPLETE - All 35 tutorials + Mental Models Overview finished!**

Welcome to the most comprehensive Google Agent Development Kit (ADK) tutorial series. This guide will take you from zero to production-ready AI agents, including enterprise deployment, third-party integrations, multi-provider LLM support, and end-to-end production examples.

---

## 📖 Start Here: Mental Models Overview

**NEW**: Before diving into tutorials, read the comprehensive mental models document!

### **Overview: Mental Models for Mastery**

**File**: `overview.md` (1,446 lines)

**What You'll Learn**:

- 15+ core mental models for understanding ADK
- Agent = Brain + Tools + Memory + Instructions + Workflows + Supervision
- Complete decision frameworks (when to use what)
- Learning paths (Foundation → Advanced)
- Source code navigation map
- The 10 Commandments of ADK development

**Why Read This First**:

- Provides "why" and "when" (tutorials provide "how")
- Clear analogies (RAM vs Hard Drive, Assembly Lines, USB Protocol)
- Decision trees for every major pattern choice
- Synthesizes all 34 tutorials into cohesive frameworks
- Accelerates learning via mental frameworks

**Time**: 2 hours (comprehensive read)

**Recommended**: Read overview → Follow learning path → Deep dive tutorials

---

## 📰 Blog: Deep Dives & Industry Insights

Stay current with in-depth articles exploring AI agent architecture, enterprise deployment, and production best practices. These articles complement the tutorials with strategic insights and decision frameworks.

### Latest Posts

#### Gemini Enterprise: Why Your AI Agents Need Enterprise-Grade Capabilities

**Published**: October 21, 2025
**File**: `docs/blog/2025-10-21-gemini-enterprise.md`
**Read online**: [Gemini Enterprise Guide](https://raphaelmansuy.github.io/adk_training/blog/gemini-enterprise-vs-agent-engine)

**What You'll Learn**:

- **Google's Agent Ecosystem**: Complete overview of Vertex AI Agent Builder, Agent Engine, ADK, Agent Garden, and A2A Protocol
- **Gemini Enterprise Portal**: Architecture, capabilities, and comparison with custom solutions
- **Enterprise Requirements**: Data sovereignty, compliance (HIPAA, FedRAMP), security, and governance
- **Real-World Scenarios**: Healthcare, financial services, and enterprise data analysis use cases
- **Decision Frameworks**: When to use standard vs. enterprise, build vs. buy analysis
- **Migration Strategies**: 4-week phased migration path from development to production
- **Building Alternatives**: Step-by-step guide to building custom portals with ADK and CopilotKit

**Why Read This**:

- Understand the complete Google AI agent product landscape
- Make informed decisions about enterprise deployment
- Learn when Gemini Enterprise is worth the investment
- Discover how to build enterprise-grade solutions with open-source tools

**Time**: 25-30 minutes
**Audience**: Architects, CTOs, senior engineers planning production deployments

---

## Quick Start

1. **Start with**: Read `overview.md` for mental models
2. Install ADK: `pip install google-adk`
3. Set API key: `export GOOGLE_API_KEY=your_key`
4. Follow a learning path from overview (Foundation/Workflows/Production/Integration/Advanced)
5. Deep dive into specific tutorials as needed

---

## Learning Path

### 🟢 Beginner (Tutorials 01-03)

Master the foundations of agent development.

#### Tutorial 01: Hello World Agent

**File**: `docs/tutorial/01_hello_world_agent.md` (438 lines)

**You'll Learn**:

- Agent class basics
- Project structure
- adk web interface
- First working agent

**Use Case**: Simple greeting assistant

**Time**: 30 minutes

---

#### Tutorial 02: Function Tools

**File**: `docs/tutorial/02_function_tools.md` (437 lines)

**You'll Learn**:

- Custom Python functions as tools
- Tool auto-registration
- Return value patterns
- Error handling

**Use Case**: Finance calculator (compound interest, loans, savings)

**Time**: 45 minutes

---

#### Tutorial 03: OpenAPI Tools

**File**: `docs/tutorial/03_openapi_tools.md` (730 lines)

**You'll Learn**:

- OpenAPIToolset usage
- Auto-generated tools
- REST API integration
- Authentication patterns

**Use Case**: Chuck Norris fact assistant

**Time**: 1 hour

---

### 🟡 Intermediate (Tutorials 04-06)

Build sophisticated multi-agent workflows.

#### Tutorial 04: Sequential Workflows

**File**: `docs/tutorial/04_sequential_workflows.md` (600 lines)

**You'll Learn**:

- SequentialAgent orchestration
- Output key pattern
- State injection with {key}
- Pipeline architecture

**Use Case**: Blog post generator (research → write → edit → format)

**Time**: 1 hour

---

#### Tutorial 05: Parallel Processing

**File**: `docs/tutorial/05_parallel_processing.md` (550 lines)

**You'll Learn**:

- ParallelAgent execution
- Fan-out/gather pattern
- Performance optimization
- Concurrent tool calls

**Use Case**: Travel planner (parallel search for flights, hotels, activities)

**Time**: 1 hour

---

#### Tutorial 06: Multi-Agent Systems

**File**: `docs/tutorial/06_multi_agent_systems.md` (650 lines)

**You'll Learn**:

- Nested orchestration
- Complex coordination patterns
- Agent composition
- Production architecture

**Use Case**: Content publishing system (3 parallel pipelines + synthesis)

**Time**: 1.5 hours

---

### 🔴 Advanced (Tutorials 07-28)

Master production-ready features and enterprise deployment.

#### Tutorial 07: Loop Agents

**File**: `docs/tutorial/07_loop_agents.md` (580 lines)

**You'll Learn**:

- LoopAgent patterns
- exit_loop tool
- Iterative refinement
- Quality improvement loops

**Use Case**: Essay refiner (critic-refiner loop)

**Time**: 1 hour

---

#### Tutorial 08: State & Memory

**File**: `docs/tutorial/08_state_memory.md` (650 lines)

**You'll Learn**:

- Session state management
- State prefixes (none, user:, app:, temp:)
- Memory service integration
- Persistent context

**Use Case**: Personal learning tutor

**Time**: 1.5 hours

---

#### Tutorial 09: Callbacks & Guardrails

**File**: `docs/tutorial/09_callbacks_guardrails.md` (1100 lines)

**You'll Learn**:

- All 6 callback types
- Guardrails implementation
- PII filtering
- Usage tracking

**Use Case**: Content moderation assistant

**Time**: 2 hours

---

#### Tutorial 10: Evaluation & Testing

**File**: `docs/tutorial/10_evaluation_testing.md` (2,484 lines)

**You'll Learn**:

- Test file creation
- Trajectory metrics
- Response validation
- CI/CD integration

**Use Case**: Customer support agent testing

**Time**: 1.5 hours

---

#### Tutorial 11: Built-in Tools & Grounding

**File**: `docs/tutorial/11_built_in_tools_grounding.md` (1,881 lines)

**You'll Learn**:

- Using `google_search` for web grounding
- Implementing location-based queries with `google_maps_grounding`
- Enterprise compliance search with `enterprise_web_search`
- Understanding `GoogleSearchAgentTool` workaround
- Tracking grounding metadata
- Building a production research assistant

**Use Case**: Current information access and research assistant

**Time**: 1 hour

---

#### Tutorial 12: Planners & Thinking

**File**: `docs/tutorial/12_planners_thinking.md` (1,231 lines)

**You'll Learn**:

- Advanced planning and reasoning patterns
- Thinking frameworks for complex tasks
- Decision-making strategies
- Problem decomposition techniques
- Strategic agent behavior

**Use Case**: Complex problem-solving and strategic planning

**Time**: 1.5 hours

---

#### Tutorial 13: Code Execution

**File**: `docs/tutorial/13_code_execution.md` (1,086 lines)

**You'll Learn**:

- Safe code execution environments
- Dynamic code generation and testing
- Sandboxed execution patterns
- Code validation and error handling
- Programming assistant capabilities

**Use Case**: Code generation and execution assistant

**Time**: 1.5 hours

---

#### Tutorial 14: Streaming & SSE

**File**: `docs/tutorial/14_streaming_sse.md` (979 lines)

**You'll Learn**:

- Server-Sent Events (SSE) implementation
- Real-time streaming responses
- Progressive output patterns
- WebSocket alternatives
- Performance optimization for streaming

**Use Case**: Real-time chat and streaming interfaces

**Time**: 1 hour

---

#### Tutorial 15: Live API Audio

**File**: `docs/tutorial/15_live_api_audio.md` (938 lines)

**You'll Learn**:

- Audio input processing
- Speech-to-text integration
- Voice command handling
- Audio stream processing
- Multimodal audio capabilities

**Use Case**: Voice-enabled assistant and audio processing

**Time**: 1 hour

---

#### Tutorial 16: MCP Integration

**File**: `docs/tutorial/16_mcp_integration.md` (1,390 lines)

**You'll Learn**:

- Model Context Protocol (MCP) fundamentals
- MCP server integration
- Standardized tool protocols
- Cross-platform agent communication
- MCP ecosystem utilization

**Use Case**: Standardized agent-tool integration

**Time**: 1.5 hours

---

#### Tutorial 17: Agent-to-Agent Communication

**File**: `docs/tutorial/17_agent_to_agent.md` (930 lines)

**You'll Learn**:

- Inter-agent communication patterns
- Message passing protocols
- Agent coordination strategies
- Distributed agent systems
- Communication security and reliability

**Use Case**: Multi-agent collaboration systems

**Time**: 1 hour

---

#### Tutorial 18: Events & Observability

**File**: `docs/tutorial/18_events_observability.md` (998 lines)

**You'll Learn**:

- Event-driven agent patterns
- Observability and monitoring
- Event logging and tracking
- Performance metrics collection
- Debugging and troubleshooting techniques

**Use Case**: Production monitoring and debugging

**Time**: 1.5 hours

---

#### Tutorial 19: Artifacts & Files

**File**: `docs/tutorial/19_artifacts_files.md` (1,004 lines)

**You'll Learn**:

- File handling and processing
- Artifact generation and management
- Document processing capabilities
- File I/O operations
- Data persistence patterns

**Use Case**: Document processing and file management

**Time**: 1 hour

---

#### Tutorial 20: YAML Configuration

**File**: `docs/tutorial/20_yaml_configuration.md` (826 lines)

**You'll Learn**:

- YAML-based agent configuration
- Declarative agent definitions
- Configuration management
- Environment-specific settings
- Configuration validation

**Use Case**: Configurable and deployable agents

**Time**: 1 hour

---

#### Tutorial 21: Multimodal Image

**File**: `docs/tutorial/21_multimodal_image.md` (900 lines)

**You'll Learn**:

- Image processing and analysis
- Vision capabilities integration
- Image understanding and description
- Visual content processing
- Multimodal agent patterns

**Use Case**: Image analysis and visual assistant

**Time**: 1 hour

---

#### Tutorial 22: Model Selection

**File**: `docs/tutorial/22_model_selection.md` (1,297 lines)

**You'll Learn**:

- Gemini model family overview and comparison
- Model capability matrix (vision, thinking, code execution, etc.)
- Performance vs cost tradeoffs
- Context window and token limits
- Model selection decision framework
- Testing and benchmarking strategies
- Migration strategies between models

**Use Case**: Optimal model selection for specific use cases

**Time**: 1.5 hours

---

#### Tutorial 23: Production Deployment

**File**: `docs/tutorial/23_production_deployment.md` (813 lines)

**You'll Learn**:

- Production deployment strategies
- Scalability considerations
- Infrastructure requirements
- Performance optimization
- Production monitoring and maintenance

**Use Case**: Enterprise-grade agent deployment

**Time**: 1.5 hours

---

#### Tutorial 24: Advanced Observability

**File**: `docs/tutorial/24_advanced_observability.md` (720 lines)

**You'll Learn**:

- Advanced monitoring techniques
- Performance profiling
- Error tracking and alerting
- System health monitoring
- Advanced debugging strategies

**Use Case**: Enterprise observability and monitoring

**Time**: 1 hour

---

#### Tutorial 25: Best Practices

**File**: `docs/tutorial/25_best_practices.md` (954 lines)

**You'll Learn**:

- ADK development best practices
- Code organization patterns
- Performance optimization techniques
- Security considerations
- Maintenance and evolution strategies

**Use Case**: Production-ready agent development

**Time**: 1.5 hours

---

#### Tutorial 26: Google AgentSpace

**File**: `docs/tutorial/26_google_agentspace.md` (920 lines)

**You'll Learn**:

- AgentSpace platform overview
- Pre-built Google agents (Idea Generation, Deep Research, NotebookLM)
- Agent Designer (low-code agent creation)
- Agent Gallery (discovery and sharing)
- Deploying ADK agents to AgentSpace
- Data connectors (SharePoint, Drive, Salesforce)
- Governance and orchestration
- Pricing and cost management

**Use Case**: Enterprise agent deployment and management

**Time**: 2 hours

---

#### Tutorial 27: Third-Party Framework Tools

**File**: `docs/tutorial/27_third_party_tools.md` (820 lines)

**You'll Learn**:

- LangChain tools integration (100+ tools)
- CrewAI tools integration (20+ tools)
- AG-UI Protocol for framework-level integration
- Tool-level vs. protocol-level integration
- Multi-framework agent systems
- Real-world research agent example

**Use Case**: Comprehensive research agent with Tavily, Wikipedia, Arxiv, Serper

**Time**: 1.5 hours

---

#### Tutorial 28: Using Other LLMs

**File**: `docs/tutorial/28_using_other_llms.md` (950 lines)

**You'll Learn**:

- OpenAI integration (GPT-4o, GPT-4o-mini)
- Anthropic Claude integration (3.7 Sonnet, Opus, Haiku)
- Local models with Ollama (Llama3.3, Mistral, Phi4)
- Azure OpenAI integration
- Claude via Vertex AI
- Multi-provider comparison
- Cost optimization strategies
- When NOT to use LiteLLM

**Use Case**: Multi-provider agent comparison and cost optimization

**Time**: 2 hours

---

### UI Integration Tutorials

Master user interface integration with modern web frameworks and platforms.

#### Tutorial 29: UI Integration Intro

**File**: `docs/tutorial/29_ui_integration_intro.md` (1,071 lines)

**You'll Learn**:

- AG-UI Protocol fundamentals
- UI integration approaches and patterns
- Decision framework for choosing integration methods
- Architecture patterns for production deployment
- Integration with React, Next.js, Streamlit, and Slack

**Use Case**: Understanding UI integration landscape and choosing the right approach

**Time**: 1.5 hours

---

#### Tutorial 30: Next.js ADK Integration

**File**: `docs/tutorial/30_nextjs_adk_integration.md` (1,360 lines)

**You'll Learn**:

- CopilotKit integration with Next.js
- React component patterns for ADK agents
- Real-time streaming and chat interfaces
- State management between frontend and backend
- Production deployment with Vercel

**Use Case**: Building web applications with ADK agents using Next.js

**Time**: 2 hours

---

#### Tutorial 31: React Vite ADK Integration

**File**: `docs/tutorial/31_react_vite_adk_integration.md` (1,239 lines)

**You'll Learn**:

- CopilotKit integration with Vite + React
- Modern React patterns for AI interfaces
- Component-based agent interactions
- Build optimization and performance
- Development workflow with hot reloading

**Use Case**: Fast development of AI-powered React applications

**Time**: 1.5 hours

---

#### Tutorial 32: Streamlit ADK Integration

**File**: `docs/tutorial/32_streamlit_adk_integration.md` (1,743 lines)

**You'll Learn**:

- Direct ADK integration with Streamlit
- Python-based UI development
- Interactive agent interfaces
- Data visualization with agent outputs
- Rapid prototyping and deployment

**Use Case**: Python-based AI applications and data science interfaces

**Time**: 2 hours

---

#### Tutorial 33: Slack ADK Integration

**File**: `docs/tutorial/33_slack_adk_integration.md` (1,669 lines)

**You'll Learn**:

- Slack app development with ADK
- Event-driven agent interactions
- Real-time messaging and responses
- Slack-specific UI patterns
- Enterprise integration and security

**Use Case**: AI assistants in Slack workspaces and enterprise communication

**Time**: 2 hours

---

#### Tutorial 34: PubSub ADK Integration

**File**: `docs/tutorial/34_pubsub_adk_integration.md` (1,711 lines)

**You'll Learn**:

- Google Cloud Pub/Sub integration
- Event-driven agent architectures
- Asynchronous message processing
- Scalable agent communication
- Enterprise messaging patterns

**Use Case**: Event-driven AI systems and enterprise messaging

**Time**: 2 hours

---

#### Tutorial 35: Commerce Agent E2E (End-to-End Implementation 01)

**File**: `docs/tutorial/35_commerce_agent_e2e.md` (1,126 lines)

**You'll Learn**:

- Production-ready multi-user commerce agent
- Persistent session management with SQLite
- Grounding metadata extraction from Google Search
- Multi-user session isolation with ADK state
- Product discovery via Google Search
- Personalized recommendations
- Type-safe tool interfaces using TypedDict
- Comprehensive testing (unit, integration, e2e)
- Optional SQLite persistence patterns

**Use Case**: Production e-commerce agents with session persistence and source attribution

**Time**: 90 minutes

---

## Reference Documentation

### scratchpad.md

**Lines**: 1,165

**Contents**:

- Core ADK concepts
- Workflow agent patterns
- State & Memory API
- Callbacks API
- Evaluation framework
- Best practices

**Use**: Quick reference for ADK patterns

---

### thought.md

**Lines**: 720

**Contents**:

- Tutorial architecture
- Research notes
- Progress tracking
- Quality standards

**Use**: Understanding tutorial design decisions

---

### MISSION_COMPLETE.md

**Lines**: 300+

**Contents**:

- Achievement summary
- Statistics and metrics
- Quality standards achieved
- Value delivered

**Use**: Overview of entire series

---

## Topic Index

### By Feature

**Agents**:

- Basic agents: Tutorial 01
- Multi-agent: Tutorials 04-06, 17
- Workflow agents: Tutorials 04-07
- Loop agents: Tutorial 07

**Tools**:

- Function tools: Tutorial 02
- OpenAPI tools: Tutorial 03
- Built-in tools: Tutorial 11
- Third-party tools: Tutorial 27
- MCP tools: Tutorial 16

**Workflows**:

- Sequential: Tutorial 04
- Parallel: Tutorial 05
- Loop: Tutorial 07
- Combined: Tutorial 06

**State & Memory**:

- Session state: Tutorial 08
- Memory service: Tutorial 08
- State management: Tutorials 08, 20

**Control & Quality**:

- Callbacks: Tutorial 09
- Guardrails: Tutorial 09
- Evaluation: Tutorial 10
- Testing: Tutorial 10
- Observability: Tutorials 18, 24

**Advanced Features**:

- Streaming & SSE: Tutorial 14
- Code execution: Tutorial 13
- Multimodal: Tutorials 15, 21
- Model selection: Tutorial 22
- Configuration: Tutorial 20
- Files & artifacts: Tutorial 19

**Integration**:

- UI frameworks: Tutorials 29-32
- Slack: Tutorial 33
- PubSub: Tutorial 34
- Enterprise deployment: Tutorials 23, 26

### By Complexity

**Simple** (1 agent):

- Tutorials 01, 02, 03

**Medium** (2-4 agents):

- Tutorials 04, 05, 07, 11-25

**Complex** (5+ agents):

- Tutorial 06

**Production Features**:

- Tutorials 08, 09, 10, 22, 23, 24, 26

**Integration Features**:

- Tutorials 27, 28, 29-34

### By Use Case Domain

**Finance**: Tutorial 02
**Entertainment**: Tutorial 03
**Content Creation**: Tutorials 04, 06, 07
**Travel**: Tutorial 05
**Education**: Tutorial 08
**Moderation**: Tutorial 09
**Customer Support**: Tutorial 10
**Research & Information**: Tutorials 11, 27
**Code & Development**: Tutorial 13
**Real-time Features**: Tutorial 14
**Audio & Multimodal**: Tutorials 15, 21
**Integration & APIs**: Tutorials 16, 17, 19
**Monitoring & Observability**: Tutorials 18, 24
**Configuration**: Tutorial 20
**Model Optimization**: Tutorial 22
**Deployment**: Tutorials 23, 26
**Best Practices**: Tutorial 25
**Multi-Provider AI**: Tutorial 28
**UI Development**: Tutorials 29-34

---

## Prerequisites by Tutorial

| Tutorial | Python | ADK | API Key | Prior Tutorials    |
| -------- | ------ | --- | ------- | ------------------ |
| 01       | 3.9+   | ✓   | ✓       | None               |
| 02       | 3.9+   | ✓   | ✓       | 01                 |
| 03       | 3.9+   | ✓   | ✓       | 01-02              |
| 04       | 3.9+   | ✓   | ✓       | 01-02              |
| 05       | 3.9+   | ✓   | ✓       | 01-02, 04          |
| 06       | 3.9+   | ✓   | ✓       | 01-02, 04-05       |
| 07       | 3.9+   | ✓   | ✓       | 01-02              |
| 08       | 3.9+   | ✓   | ✓       | 01-02              |
| 09       | 3.9+   | ✓   | ✓       | 01-02, 08          |
| 10       | 3.9+   | ✓   | ✓       | 01-02, pytest      |
| 11       | 3.9+   | ✓   | ✓       | 01-02, Gemini 2.0+ |
| 12       | 3.9+   | ✓   | ✓       | 01-02              |
| 13       | 3.9+   | ✓   | ✓       | 01-02              |
| 14       | 3.9+   | ✓   | ✓       | 01-02              |
| 15       | 3.9+   | ✓   | ✓       | 01-02              |
| 16       | 3.9+   | ✓   | ✓       | 01-02              |
| 17       | 3.9+   | ✓   | ✓       | 01-02              |
| 18       | 3.9+   | ✓   | ✓       | 01-02              |
| 19       | 3.9+   | ✓   | ✓       | 01-02              |
| 20       | 3.9+   | ✓   | ✓       | 01-02              |
| 21       | 3.9+   | ✓   | ✓       | 01-02              |
| 22       | 3.9+   | ✓   | ✓       | 01-02              |
| 23       | 3.9+   | ✓   | ✓       | 01-02              |
| 24       | 3.9+   | ✓   | ✓       | 01-02              |
| 25       | 3.9+   | ✓   | ✓       | 01-02              |
| 26       | 3.9+   | ✓   | ✓       | 01-02              |
| 27       | 3.9+   | ✓   | ✓       | 01-02              |
| 28       | 3.9+   | ✓   | ✓       | 01-02              |
| 29       | 3.9+   | ✓   | ✓       | 01-02              |
| 30       | 3.9+   | ✓   | ✓       | 01-02, Node.js     |
| 31       | 3.9+   | ✓   | ✓       | 01-02, Node.js     |
| 32       | 3.9+   | ✓   | ✓       | 01-02              |
| 33       | 3.9+   | ✓   | ✓       | 01-02              |
| 34       | 3.9+   | ✓   | ✓       | 01-02, GCP         |

---

## Recommended Learning Paths

### Path 1: Fastest Route to Production

**Goal**: Build a production agent ASAP

1. Tutorial 01 (basics)
2. Tutorial 02 (tools)
3. Tutorial 08 (state)
4. Tutorial 09 (callbacks)
5. Tutorial 10 (testing)

**Time**: ~6 hours

---

### Path 2: Comprehensive Learning

**Goal**: Master all ADK features

Follow tutorials 01-10 in order.

**Time**: ~12 hours

---

### Path 3: Workflow Specialist

**Goal**: Focus on orchestration

1. Tutorial 01 (basics)
2. Tutorial 02 (tools)
3. Tutorial 04 (sequential)
4. Tutorial 05 (parallel)
5. Tutorial 06 (multi-agent)
6. Tutorial 07 (loops)

**Time**: ~6.5 hours

---

### Path 4: Integration Expert

**Goal**: Connect to external services

1. Tutorial 01 (basics)
2. Tutorial 03 (OpenAPI)
3. Tutorial 08 (state for API data)
4. Tutorial 10 (testing integrations)

**Time**: ~5 hours

---

### Path 5: Enterprise Deployment

**Goal**: Production deployment at scale

1. Tutorial 01 (basics)
2. Tutorial 02 (tools)
3. Tutorial 08 (state)
4. Tutorial 09 (callbacks & guardrails)
5. Tutorial 10 (testing)
6. Tutorial 26 (AgentSpace deployment)

**Time**: ~8 hours

---

### Path 6: Multi-Provider AI

**Goal**: Use multiple LLM providers

1. Tutorial 01 (basics)
2. Tutorial 22 (Gemini models)
3. Tutorial 27 (third-party tools)
4. Tutorial 28 (other LLMs)

**Time**: ~6 hours

---

### Path 7: UI Integration Specialist

**Goal**: Build user interfaces for ADK agents

1. Tutorial 01 (basics)
2. Tutorial 29 (UI integration intro)
3. Tutorial 30 (Next.js) OR Tutorial 31 (React/Vite) OR Tutorial 32 (Streamlit)
4. Tutorial 33 (Slack) OR Tutorial 34 (PubSub)

**Time**: ~6-8 hours

---

### Path 8: Complete Enterprise Solution

**Goal**: Full-stack AI agent development

1. Tutorials 01-10 (foundation)
2. Tutorial 22 (model selection)
3. Tutorial 23 (production deployment)
4. Tutorial 26 (AgentSpace)
5. Tutorial 29-32 (UI integration)

**Time**: ~20 hours

## Code Examples Index

### Project Structures

**Simple Agent** (Tutorial 01):

```
hello_agent/
├── __init__.py
├── agent.py
└── .env
```

**With Tests** (Tutorial 10):

```
support_agent/
├── __init__.py
├── agent.py
├── .env
└── tests/
    ├── simple.test.json
    ├── complex.evalset.json
    └── test_agent.py
```

### Common Patterns

**Basic Agent** (Tutorial 01):

```python
from google.adk.agents import Agent

root_agent = Agent(
    name="my_agent",
    model="gemini-2.0-flash",
    instruction="...",
    tools=[...]
)
```

**Sequential Pipeline** (Tutorial 04):

```python
from google.adk.agents import SequentialAgent

pipeline = SequentialAgent(
    name="pipeline",
    agents=[agent1, agent2, agent3]
)
```

**Parallel Execution** (Tutorial 05):

```python
from google.adk.agents import ParallelAgent

parallel = ParallelAgent(
    name="parallel",
    agents=[agent1, agent2, agent3]
)
```

**Loop Pattern** (Tutorial 07):

```python
from google.adk.agents import LoopAgent

loop = LoopAgent(
    name="loop",
    agent=refiner,
    max_iterations=5
)
```

### Running Agents

**Web UI** (Recommended):

```bash
adk web agent_name
```

**Terminal**:

```bash
adk run agent_name
```

**Tests**:

```bash
pytest tests/test_agent.py
```

---

## Statistics

**Total Content**: 40,000+ lines
**Tutorial Content**: 36,682+ lines (34 tutorials)
**Documentation**: 3,318+ lines

**Average Tutorial Length**: 1,079 lines
**Longest Tutorial**: Tutorial 10 (2,484 lines)
**Shortest Tutorial**: Tutorial 01 (297 lines)

**Real-World Examples**: 34+
**Code Patterns**: 150+
**Best Practices**: 200+
**Troubleshooting Items**: 80+
**Supported LLM Providers**: 6 (Gemini, OpenAI, Claude, Ollama, Azure, Vertex AI)
**Third-Party Tools**: 120+ (LangChain + CrewAI)
**UI Integration Frameworks**: 5 (Next.js, React/Vite, Streamlit, Slack, PubSub)

---

## Common Questions

### Where should I start?

Tutorial 01. Follow the sequence.

### Can I skip tutorials?

Not recommended, but see "Recommended Learning Paths" above.

### How long does it take?

~20 hours for complete series, ~6 hours for production path.

### Do I need to know Python?

Yes, basic Python knowledge required.

### Do I need a Google API key?

Yes, get one from Google AI Studio.

### Are these tutorials up-to-date?

Yes! October 2025 patterns, fully modern.

### Can I use this for production?

Absolutely! All patterns are production-ready.

---

## Getting Help

### Errors in Tutorials

1. Check "Common Issues & Troubleshooting" section
2. Verify Python version (3.9+)
3. Confirm API key is set
4. Review Events tab in adk web

### Understanding Concepts

1. Review scratchpad.md for pattern reference
2. Check official documentation links
3. Study code comments in examples
4. Try modifying examples to learn

### Further Learning

1. Official docs: https://google.github.io/adk-docs/
2. GitHub repo: https://github.com/google/adk-python
3. Example projects in research/ folder

---

## Success Checklist

After completing all tutorials, you should be able to:

- ✅ Create basic agents with tools
- ✅ Integrate REST APIs via OpenAPI
- ✅ Build sequential workflows
- ✅ Implement parallel processing
- ✅ Orchestrate multi-agent systems
- ✅ Use loop agents for refinement
- ✅ Manage state and memory
- ✅ Implement callbacks and guardrails
- ✅ Write comprehensive tests
- ✅ Deploy to production

---

## Next Steps After Completion

1. **Build Your Own Agent**: Apply patterns to your use case
2. **Explore Advanced Topics**: Streaming, deployment, optimization
3. **Contribute**: Share improvements and examples
4. **Stay Updated**: Follow ADK releases and documentation

---

**🚀 Ready to start? Begin with Tutorial 01: Hello World Agent!**

**📚 Happy Learning! Build amazing AI agents with Google ADK!**
