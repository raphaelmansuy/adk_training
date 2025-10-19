# Google ADK Training Hub

**Build production-ready AI agents tutorials that solve real problems.**

You're here because AI agents are transforming software development, and you want practical skills you can use at work tomorrow. This training hub gives you exactly that—no fluff, just working code and proven patterns from 34 completed tutorials.

## What You'll Gain

**Professionally:**

- Ship AI features faster with reusable agent patterns
- Architect multi-agent systems that scale
- Debug and test AI agents like traditional software
- Deploy to production with confidence

**Practically:**

- 34 working implementations you can run today
- Copy-paste code patterns for common scenarios
- Testing frameworks you can adapt to your projects
- Integration examples for Next.js, React, Streamlit, Slack, PubSub, and more

**Completion Status: 34/34 tutorials ready to use (100%)** ✅

> Built by developers, for developers. Every tutorial has working code, not just theory.

## 📚 Documentation

**[View Interactive Documentation →](https://raphaelmansuy.github.io/adk_training/)**

## Why Google ADK?

ADK solves the messy reality of production AI agents: how do you connect LLMs to your APIs, manage conversation state, orchestrate complex workflows, and actually deploy something reliable?

**ADK gives you:**

- **Tool integration** that just works (REST APIs, databases, custom functions)
- **Workflow patterns** you can copy (sequential, parallel, error handling)
- **State management** without the headache (sessions, memory, artifacts)
- **Production deployment** to Google Cloud (Cloud Run, Vertex AI, GKE)

Think of it as the missing framework between "ChatGPT API call" and "production AI system."

## 🏗️ Project Structure

```text
├── overview.md                    # Mental models for ADK mastery
├── TABLE_OF_CONTENTS.md           # Complete tutorial series guide
├── scratchpad.md                  # Quick reference patterns
├── thought.md                     # Tutorial design and research notes
├── docs/tutorial/                 # 34 comprehensive tutorials
│   ├── 01_hello_world_agent.md    # ✅ COMPLETED - Agent basics
│   ├── 02_function_tools.md       # ✅ COMPLETED - Custom tools
│   ├── 03_openapi_tools.md        # ✅ COMPLETED - REST API integration
│   ├── 04_sequential_workflows.md # ✅ COMPLETED - Sequential pipelines
│   ├── 05_parallel_processing.md  # ✅ COMPLETED - Parallel execution
│   ├── 06_multi_agent_systems.md  # ✅ COMPLETED - Multi-agent orchestration
│   ├── 07_loop_agents.md          # ✅ COMPLETED - Iterative refinement
│   ├── 08_state_memory.md         # ✅ COMPLETED - State management
│   ├── 09_callbacks_guardrails.md # ✅ COMPLETED - Control & quality
│   ├── 10_evaluation_testing.md   # ✅ COMPLETED - Testing framework
│   ├── 11_built_in_tools_grounding.md # ✅ COMPLETED - Built-in tools
│   ├── 12_planners_thinking.md    # ✅ COMPLETED - Advanced planning
│   ├── 13_code_execution.md       # ✅ COMPLETED - Code execution
│   ├── 14_streaming_sse.md        # ✅ COMPLETED - Real-time streaming
│   ├── 15_live_api_audio.md       # ✅ COMPLETED - Audio processing
│   ├── 16_mcp_integration.md      # ✅ COMPLETED - MCP protocol
│   ├── 17_agent_to_agent.md       # ✅ COMPLETED - Inter-agent communication
│   ├── 18_events_observability.md # ✅ COMPLETED - Monitoring & events
│   ├── 19_artifacts_files.md      # ✅ COMPLETED - File handling
│   ├── 20_yaml_configuration.md   # ✅ COMPLETED - Configuration management
│   ├── 21_multimodal_image.md     # ✅ COMPLETED - Image processing
│   ├── 22_model_selection.md      # ✅ COMPLETED - Model optimization
│   ├── 23_production_deployment.md # ✅ COMPLETED - Production deployment
│   ├── 24_advanced_observability.md # ✅ COMPLETED - Advanced monitoring
│   ├── 25_best_practices.md       # ✅ COMPLETED - Best practices
│   ├── 26_google_agentspace.md    # ✅ COMPLETED - Gemini Enterprise platform
│   ├── 27_third_party_tools.md    # ✅ COMPLETED - Third-party integrations
│   ├── 28_using_other_llms.md     # ✅ COMPLETED - Multi-provider LLMs
│   ├── 29_ui_integration_intro.md # ✅ COMPLETED - UI integration overview
│   ├── 30_nextjs_adk_integration.md # ✅ COMPLETED - Next.js integration
│   ├── 31_react_vite_adk_integration.md # ✅ COMPLETED - React/Vite integration
│   ├── 32_streamlit_adk_integration.md # ✅ COMPLETED - Streamlit integration
│   ├── 33_slack_adk_integration.md # ✅ COMPLETED - Slack integration
│   └── 34_pubsub_adk_integration.md # ✅ COMPLETED - PubSub integration
├── tutorial_implementation/       # ✅ 34 working implementations
│   ├── tutorial01/                # Hello World Agent
│   ├── tutorial02/                # Function Tools
│   ├── tutorial03/                # OpenAPI Tools
│   ├── tutorial04/                # Sequential Workflows
│   ├── tutorial05/                # Parallel Processing
│   ├── tutorial06/                # Multi-Agent Systems
│   ├── tutorial07/                # Loop Agents
│   ├── tutorial08/                # State & Memory
│   ├── tutorial09/                # Callbacks & Guardrails
│   ├── tutorial10/                # Evaluation & Testing
│   ├── tutorial11/                # Built-in Tools & Grounding
│   ├── tutorial12/                # Planners & Thinking
│   ├── tutorial13/                # Code Execution
│   ├── tutorial14/                # Streaming & SSE
│   ├── tutorial15/                # Live API Audio
│   ├── tutorial16/                # MCP Integration
│   ├── tutorial17/                # Agent-to-Agent Communication
│   ├── tutorial18/                # Events & Observability
│   ├── tutorial19/                # Artifacts & Files
│   ├── tutorial20/                # YAML Configuration
│   ├── tutorial21/                # Multimodal Image
│   ├── tutorial22/                # Model Selection
│   ├── tutorial23/                # Production Deployment
│   ├── tutorial24/                # Advanced Observability
│   ├── tutorial25/                # Best Practices
│   ├── tutorial26/                # Google AgentSpace
│   ├── tutorial27/                # Third-Party Framework Tools
│   ├── tutorial28/                # Using Other LLMs
│   ├── tutorial29/                # UI Integration Intro
│   ├── tutorial30/                # Next.js ADK Integration
│   ├── tutorial31/                # React Vite ADK Integration
│   ├── tutorial32/                # Streamlit ADK Integration
│   ├── tutorial33/                # Slack ADK Integration
│   └── tutorial34/                # PubSub ADK Integration
```

## 🚀 Get Started (5 minutes)

**Prerequisites:** Python 3.9+, Google Cloud API key ([get one free](https://makersuite.google.com/app/apikey))

```bash
# 1. Install
pip install google-adk

# 2. Set your API key
export GOOGLE_API_KEY=your_key_here

# 3. Clone and run your first agent
git clone <repository-url>
cd adk_training/tutorial_implementation/tutorial01
make setup && adk web
```

**That's it.** You now have a working agent you can modify and learn from.

Start with [Tutorial 01](docs/tutorial/01_hello_world_agent.md) (30 min) to understand what you just built.

## 📖 Learning Paths (Choose Your Journey)

### 🎯 "I need results this week" (4-6 hours)

**For:** Developers who need to ship AI features quickly

1. **Tutorials 01-03** - Foundation (2 hrs)
   - Build your first agent, add custom tools, connect REST APIs
2. **Tutorial 04** - Sequential workflows (1 hr)
   - Chain agents together for complex tasks
3. **Tutorial 14** - Streaming (1 hr)
   - Add real-time responses to your UI

**You'll ship:** A working AI agent integrated with your APIs, streaming responses to users.

### 🏗️ "I'm building a serious AI product" (2-3 days)

**For:** Teams architecting multi-agent systems

1. **Foundation** (Tutorials 01-03) - Basics
2. **Workflows** (Tutorials 04-07) - Orchestration patterns
3. **Production** (Tutorials 08-12) - State, testing, guardrails
4. **Advanced** (Tutorials 13-21) - Streaming, MCP, A2A, multimodal

**You'll ship:** A production-grade multi-agent system with proper testing, monitoring, and deployment.

### 🚀 "I'm architecting enterprise AI" (3-5 days)

**For:** Senior engineers and architects

Complete all 34 tutorials, focusing on:

- Multi-agent orchestration patterns
- Production observability and testing
- Enterprise deployment strategies
- UI integration with Next.js/React
- Advanced integrations (MCP, A2A, streaming, audio)

**You'll gain:** Deep expertise in agent architecture and the patterns to make critical design decisions.

## � Today I Learn (TIL) - Quick Daily Insights

Introducing **Today I Learn (TIL)** - short, focused articles on specific ADK
features and patterns. Perfect for learning one concept at a time!

**What are TILs?**

- ✅ **Focused** - One feature, one pattern, one solution
- ✅ **Quick** - 5-10 minute read
- ✅ **Practical** - Working code examples with full implementations
- ✅ **Dated** - Published daily with specific ADK versions
- ✅ **Standalone** - Complete on their own

### Featured TILs

#### Context Compaction (October 19, 2025)

Learn how to automatically summarize conversation history to reduce token usage
in long-running agent conversations. Perfect for production systems handling
extended user interactions.

- **Time**: 8 minutes
- **ADK Version**: 1.16+
- **Implementation**: Full working code with tests
- **Read**: [TIL: Context Compaction →](./docs/til/til_context_compaction_20250119.md)

### TIL Guidelines

Want to create your own TIL? See our comprehensive guide:

- [TIL Template & Guidelines →](./docs/til/TIL_TEMPLATE.md)
- **New TIL every week** - Stay current with ADK features
- **Your submissions welcome** - Contribute your own TILs

---

## 📚 All Tutorials (34/34 Complete)

See the complete tutorial list in the [Project Structure](#project-structure) section above, or browse the [interactive documentation](https://raphaelmansuy.github.io/adk_training/).

## 🎓 Tutorials Overview

| Tutorial                                                                                         | Topic                        | Status       | Complexity   | Time  |
| ------------------------------------------------------------------------------------------------ | ---------------------------- | ------------ | ------------ | ----- |
| [01](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial01) | Hello World Agent            | ✅ Completed | Beginner     | 30min |
| [02](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial02) | Function Tools               | ✅ Completed | Beginner     | 45min |
| [03](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial03) | OpenAPI Tools                | ✅ Completed | Beginner     | 1hr   |
| [04](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial04) | Sequential Workflows         | ✅ Completed | Intermediate | 1hr   |
| [05](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial05) | Parallel Processing          | ✅ Completed | Intermediate | 1hr   |
| [06](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial06) | Multi-Agent Systems          | ✅ Completed | Intermediate | 1.5hr |
| [07](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial07) | Loop Agents                  | ✅ Completed | Advanced     | 1hr   |
| [08](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial08) | State & Memory               | ✅ Completed | Advanced     | 1.5hr |
| [09](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial09) | Callbacks & Guardrails       | ✅ Completed | Advanced     | 2hr   |
| [10](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial10) | Evaluation & Testing         | ✅ Completed | Advanced     | 1.5hr |
| [11](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial11) | Built-in Tools & Grounding   | ✅ Completed | Intermediate | 1hr   |
| [12](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial12) | Planners & Thinking          | ✅ Completed | Advanced     | 1.5hr |
| [13](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial13) | Code Execution               | ✅ Completed | Advanced     | 1.5hr |
| [14](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial14) | Streaming & SSE              | ✅ Completed | Intermediate | 1hr   |
| [15](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial15) | Live API Audio               | ✅ Completed | Advanced     | 1hr   |
| [16](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial16) | MCP Integration              | ✅ Completed | Advanced     | 1.5hr |
| [17](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial17) | Agent-to-Agent Communication | ✅ Completed | Advanced     | 1hr   |
| [18](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial18) | Events & Observability       | ✅ Completed | Advanced     | 1.5hr |
| [19](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial19) | Artifacts & Files            | ✅ Completed | Intermediate | 1hr   |
| [20](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial20) | YAML Configuration           | ✅ Completed | Intermediate | 1hr   |
| [21](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial21) | Multimodal Image             | ✅ Completed | Advanced     | 1hr   |
| [22](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial22) | Model Selection              | ✅ Completed | Advanced     | 1.5hr |
| [23](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial23) | Production Deployment        | ✅ Completed | Advanced     | 1.5hr |
| [24](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial24) | Advanced Observability       | ✅ Completed | Advanced     | 1hr   |
| [25](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial25) | Best Practices               | ✅ Completed | Advanced     | 1.5hr |
| [26](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial26) | Google AgentSpace            | ✅ Completed | Advanced     | 2hr   |
| [27](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial27) | Third-Party Framework Tools  | ✅ Completed | Advanced     | 1.5hr |
| [28](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial28) | Using Other LLMs             | ✅ Completed | Advanced     | 2hr   |
| [29](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial29) | UI Integration Intro         | ✅ Completed | Intermediate | 1.5hr |
| [30](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial30) | Next.js ADK Integration      | ✅ Completed | Advanced     | 2hr   |
| [31](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial31) | React Vite ADK Integration   | ✅ Completed | Advanced     | 1.5hr |
| [32](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial32) | Streamlit ADK Integration    | ✅ Completed | Advanced     | 2hr   |
| [33](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial33) | Slack ADK Integration        | ✅ Completed | Advanced     | 2hr   |
| [34](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial34) | PubSub ADK Integration       | ✅ Completed | Advanced     | 2hr   |

## 📊 Project Completion Status

### ✅ Completed Tutorials (34/34)

The following tutorials have been fully implemented with working code, comprehensive tests, and verified functionality:

**Foundation Layer:**

- **Tutorial 01**: Hello World Agent - Basic agent creation and interaction
- **Tutorial 02**: Function Tools - Custom Python functions as callable tools
- **Tutorial 03**: OpenAPI Tools - REST API integration via OpenAPI specifications

**Workflow Layer:**

- **Tutorial 04**: Sequential Workflows - Ordered pipeline execution with SequentialAgent
- **Tutorial 05**: Parallel Processing - Concurrent task execution with ParallelAgent
- **Tutorial 06**: Multi-Agent Systems - Complex hierarchical agent orchestration
- **Tutorial 07**: Loop Agents - Iterative refinement patterns with LoopAgent

**Production Layer:**

- **Tutorial 08**: State & Memory - Session management and persistent context
- **Tutorial 09**: Callbacks & Guardrails - Quality control and monitoring systems
- **Tutorial 10**: Evaluation & Testing - Comprehensive testing framework with trajectory metrics
- **Tutorial 11**: Built-in Tools & Grounding - Google Search and location-based tools
- **Tutorial 12**: Planners & Thinking - Advanced reasoning and planning patterns

**Advanced Features:**

- **Tutorial 13**: Code Execution - Safe code execution environments and sandboxing
- **Tutorial 14**: Streaming & SSE - Real-time streaming responses with Server-Sent Events
- **Tutorial 15**: Live API Audio - Audio processing and voice interactions with Gemini Live API
- **Tutorial 16**: MCP Integration - Model Context Protocol for standardized tool integration
- **Tutorial 17**: Agent-to-Agent Communication - Distributed multi-agent systems with A2A protocol
- **Tutorial 18**: Events & Observability - Advanced monitoring, logging, and event tracking
- **Tutorial 19**: Artifacts & Files - File handling and artifact management systems
- **Tutorial 20**: YAML Configuration - Configuration-driven agent development
- **Tutorial 21**: Multimodal Image - Image processing and vision capabilities
- **Tutorial 22**: Model Selection - Model optimization and selection strategies
- **Tutorial 23**: Production Deployment - Enterprise deployment strategies and patterns
- **Tutorial 24**: Advanced Observability - Enhanced monitoring patterns
- **Tutorial 25**: Best Practices - Production-ready agent development patterns
- **Tutorial 26**: Google AgentSpace - Enterprise agent platform deployment

**UI Integration:**

- **Tutorial 27**: Third-Party Framework Tools - LangChain, CrewAI integration
- **Tutorial 28**: Using Other LLMs - Multi-provider LLM support
- **Tutorial 29**: UI Integration Intro - Frontend integration patterns
- **Tutorial 30**: Next.js ADK Integration - React web applications with CopilotKit
- **Tutorial 31**: React Vite ADK Integration - Custom React frontend with AG-UI protocol
- **Tutorial 32**: Streamlit ADK Integration - Data science applications with Streamlit
- **Tutorial 33**: Slack ADK Integration - Slack bot development and integration

**All completed tutorials include:**

- ✅ Working code implementations in `tutorial_implementation/`
- ✅ Comprehensive test suites with pytest
- ✅ Proper project structure (Makefile, requirements.txt, pyproject.toml)
- ✅ Environment configuration (.env.example)
- ✅ Documentation and usage examples
- ✅ Integration with ADK web interface

### ✅ All Tutorials Complete (34/34)

The comprehensive ADK Training Hub now includes all 34 tutorials with full implementations.

## 🛠️ Development Tools

- **ADK Web UI**: `adk web` - Interactive development interface
- **Testing Framework**: Comprehensive evaluation and testing tools
- **Deployment CLI**: `adk deploy` - Multiple deployment options
- **Code Generation**: Automated agent and tool scaffolding

## 🤝 Found This Useful?

If these tutorials helped you ship faster or learn something valuable:

- ⭐ **Star this repo** to help others discover it
- 🐛 **Report issues** if something's broken or unclear
- 💡 **Share your use case** - what did you build with ADK?
- 📝 **Contribute** improvements or additional examples

Your feedback makes this better for everyone.

## 👨‍💻 About

Created by **Raphaël MANSUY** ([LinkedIn](https://linkedin.com/in/raphaelmansuy)), CTO and AI educator. Built from real-world experience deploying AI agents in production.

Why I built this: Most AI agent tutorials show toy examples. I wanted practical patterns that work in production.

## Resources

- **[Official ADK Docs](https://google.github.io/adk-docs/)** - Google's documentation
- **[ADK Source Code](https://github.com/google/adk-python)** - When docs aren't enough
- **[Get API Key](https://makersuite.google.com/app/apikey)** - Free Google AI Studio access

## 📄 License

MIT for tutorial code. See component licenses in respective directories.

---

**Ready to ship AI agents? [Start here](docs/tutorial/01_hello_world_agent.md) →**
