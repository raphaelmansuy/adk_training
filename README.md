# Google ADK Training Hub

A comprehensive training repository for Google Agent Development Kit (ADK), featuring 34 tutorials, mental models, research, and automated testing. The project teaches agent development from first principles to production deployment.

This project provides a complete learning journey through Google ADK, featuring:

- **34 comprehensive tutorials** covering everything from basic agents to production deployment
- **12 completed tutorials** with working implementations and automated testing
- **22 draft tutorials** with detailed documentation ready for implementation
- **Mental models framework** for understanding ADK patterns and Generative AI concepts
- **Research and integration examples** for various UI frameworks and deployment scenarios
- **Production-ready code examples** and best practices

> **📊 Completion Status: 12/34 tutorials implemented (35%)**

## 📚 Documentation

📚 **[View Interactive Documentation](https://raphaelmansuy.github.io/adk_training/)** - Complete tutorial series with working examples, mental models, and Mermaid diagrams

## 📚 What's ADK?

Google Agent Development Kit (ADK) is a powerful framework for building AI agents that combine:

- **Large Language Models** (Gemini, GPT-4, Claude, etc.)
- **Tools and Capabilities** (APIs, databases, custom functions)
- **State Management** (session context, long-term memory)
- **Workflow Orchestration** (sequential, parallel, loop patterns)
- **Production Deployment** (Cloud Run, Vertex AI, Kubernetes)

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
│   ├── 13_code_execution.md       # 📝 DRAFT - Code execution
│   ├── 14_streaming_sse.md        # 📝 DRAFT - Real-time streaming
│   ├── 15_live_api_audio.md       # 📝 DRAFT - Audio processing
│   ├── 16_mcp_integration.md      # 📝 DRAFT - MCP protocol
│   ├── 17_agent_to_agent.md       # 📝 DRAFT - Inter-agent communication
│   ├── 18_events_observability.md # 📝 DRAFT - Monitoring & events
│   ├── 19_artifacts_files.md      # 📝 DRAFT - File handling
│   ├── 20_yaml_configuration.md   # 📝 DRAFT - Configuration management
│   ├── 21_multimodal_image.md     # 📝 DRAFT - Image processing
│   ├── 22_model_selection.md      # 📝 DRAFT - Model optimization
│   ├── 23_production_deployment.md # 📝 DRAFT - Production deployment
│   ├── 24_advanced_observability.md # 📝 DRAFT - Advanced monitoring
│   ├── 25_best_practices.md       # 📝 DRAFT - Best practices
│   ├── 26_google_agentspace.md    # 📝 DRAFT - AgentSpace platform
│   ├── 27_third_party_tools.md    # 📝 DRAFT - Third-party integrations
│   ├── 28_using_other_llms.md     # 📝 DRAFT - Multi-provider LLMs
│   ├── 29_ui_integration_intro.md # 📝 DRAFT - UI integration overview
│   ├── 30_nextjs_adk_integration.md # 📝 DRAFT - Next.js integration
│   ├── 31_react_vite_adk_integration.md # 📝 DRAFT - React/Vite integration
│   ├── 32_streamlit_adk_integration.md # 📝 DRAFT - Streamlit integration
│   ├── 33_slack_adk_integration.md # 📝 DRAFT - Slack integration
│   └── 34_pubsub_adk_integration.md # 📝 DRAFT - PubSub integration
├── tutorial_implementation/       # ✅ 12 working implementations
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
│   └── tutorial12/                # Planners & Thinking
├── research/                      # Integration research and examples
│   ├── adk_ui_integration/        # UI framework integrations
│   ├── adk-java/                  # Java ADK implementation
│   ├── adk-python/                # Python ADK source and examples
│   ├── adk-web/                   # Web components
│   └── ag-ui/                     # AG UI framework
├── test_tutorials/                # Automated testing framework
├── agent-starter-pack/            # Ready-to-use agent templates
└── how-to-build-ai-agent/         # Step-by-step agent building guide
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Google Cloud API key (for Gemini models)
- Basic Python knowledge

### Installation

```bash
# Install Google ADK
pip install google-adk

# Set your API key
export GOOGLE_API_KEY=your_google_api_key_here
```

### First Agent

```bash
# Clone this repository
git clone <repository-url>
cd adk_training

# Start with Tutorial 01
# Follow the docs/tutorial/01_hello_world_agent.md guide
```

## 📖 Learning Path

### 1. Foundation (✅ COMPLETED - Tutorials 01-03)

Master the foundations of agent development.

- Read `overview.md` - Mental models for ADK mastery
- **Tutorial 01: Hello World Agent** ✅ - Agent basics
- **Tutorial 02: Function Tools** ✅ - Custom tools
- **Tutorial 03: OpenAPI Tools** ✅ - REST API integration

### 2. Workflows (✅ COMPLETED - Tutorials 04-07)

Build sophisticated multi-agent workflows.

- **Tutorial 04: Sequential Workflows** ✅ - Ordered pipelines
- **Tutorial 05: Parallel Processing** ✅ - Concurrent tasks
- **Tutorial 06: Multi-Agent Systems** ✅ - Complex orchestration
- **Tutorial 07: Loop Agents** ✅ - Iterative refinement

### 3. Production (✅ COMPLETED - Tutorials 08-12)

Master production-ready features.

- **Tutorial 08: State & Memory** ✅ - Session context & persistence
- **Tutorial 09: Callbacks & Guardrails** ✅ - Control & quality assurance
- **Tutorial 10: Evaluation & Testing** ✅ - Comprehensive testing framework
- **Tutorial 11: Built-in Tools & Grounding** ✅ - Google search & grounding
- **Tutorial 12: Planners & Thinking** ✅ - Advanced reasoning patterns

### 4. Advanced Features (📝 DRAFT - Tutorials 13-28)

Advanced capabilities and integrations.

- **Tutorial 13: Code Execution** 📝 - Safe code execution environments
- **Tutorial 14: Streaming & SSE** 📝 - Real-time responses
- **Tutorial 15: Live API Audio** 📝 - Audio processing & voice
- **Tutorial 16: MCP Integration** 📝 - Model Context Protocol
- **Tutorial 17: Agent-to-Agent Communication** 📝 - Inter-agent messaging
- **Tutorial 18: Events & Observability** 📝 - Monitoring & logging
- **Tutorial 19: Artifacts & Files** 📝 - File handling & processing
- **Tutorial 20: YAML Configuration** 📝 - Declarative configuration
- **Tutorial 21: Multimodal Image** 📝 - Image analysis & vision
- **Tutorial 22: Model Selection** 📝 - Model optimization & comparison
- **Tutorial 23: Production Deployment** 📝 - Enterprise deployment
- **Tutorial 24: Advanced Observability** 📝 - Performance monitoring
- **Tutorial 25: Best Practices** 📝 - Production patterns
- **Tutorial 26: Google AgentSpace** 📝 - AgentSpace platform
- **Tutorial 27: Third-Party Tools** 📝 - External integrations
- **Tutorial 28: Using Other LLMs** 📝 - Multi-provider support

### 5. UI Integration (📝 DRAFT - Tutorials 29-34)

User interface integration with modern frameworks.

- **Tutorial 29: UI Integration Intro** 📝 - Integration patterns overview
- **Tutorial 30: Next.js ADK Integration** 📝 - React web applications
- **Tutorial 31: React Vite ADK Integration** 📝 - Modern React development
- **Tutorial 32: Streamlit ADK Integration** 📝 - Python-based interfaces
- **Tutorial 33: Slack ADK Integration** 📝 - Enterprise messaging
- **Tutorial 34: PubSub ADK Integration** 📝 - Event-driven systems

## 🔧 Key Features Covered

- **Agent Types**: LLM Agents, Workflow Agents, Remote Agents
- **Tools**: Function Tools, OpenAPI Tools, MCP Tools, Built-in Google Tools
- **Workflows**: Sequential, Parallel, Loop patterns
- **State Management**: Session state, Memory service, Artifacts
- **Deployment**: Local development, Cloud Run, Vertex AI Agent Engine, GKE
- **Integrations**: REST APIs, Databases, UI frameworks, Third-party tools
- **Multi-Provider**: Gemini, OpenAI, Claude, Ollama, Azure OpenAI
- **Production Features**: Callbacks, Guardrails, Evaluation, Observability

## 🎓 Tutorials Overview

| Tutorial | Topic | Status | Complexity | Time |
|----------|-------|--------|------------|------|
| 01 | Hello World Agent | ✅ Completed | Beginner | 30min |
| 02 | Function Tools | ✅ Completed | Beginner | 45min |
| 03 | OpenAPI Tools | ✅ Completed | Beginner | 1hr |
| 04 | Sequential Workflows | ✅ Completed | Intermediate | 1hr |
| 05 | Parallel Processing | ✅ Completed | Intermediate | 1hr |
| 06 | Multi-Agent Systems | ✅ Completed | Intermediate | 1.5hr |
| 07 | Loop Agents | ✅ Completed | Advanced | 1hr |
| 08 | State & Memory | ✅ Completed | Advanced | 1.5hr |
| 09 | Callbacks & Guardrails | ✅ Completed | Advanced | 2hr |
| 10 | Evaluation & Testing | ✅ Completed | Advanced | 1.5hr |
| 11 | Built-in Tools & Grounding | ✅ Completed | Intermediate | 1hr |
| 12 | Planners & Thinking | ✅ Completed | Advanced | 1.5hr |
| 13 | Code Execution | 📝 Draft | Advanced | 1.5hr |
| 14 | Streaming & SSE | 📝 Draft | Intermediate | 1hr |
| 15 | Live API Audio | 📝 Draft | Advanced | 1hr |
| 16 | MCP Integration | 📝 Draft | Advanced | 1.5hr |
| 17 | Agent-to-Agent Communication | 📝 Draft | Advanced | 1hr |
| 18 | Events & Observability | 📝 Draft | Advanced | 1.5hr |
| 19 | Artifacts & Files | 📝 Draft | Intermediate | 1hr |
| 20 | YAML Configuration | 📝 Draft | Intermediate | 1hr |
| 21 | Multimodal Image | 📝 Draft | Advanced | 1hr |
| 22 | Model Selection | 📝 Draft | Advanced | 1.5hr |
| 23 | Production Deployment | 📝 Draft | Advanced | 1.5hr |
| 24 | Advanced Observability | 📝 Draft | Advanced | 1hr |
| 25 | Best Practices | 📝 Draft | Advanced | 1.5hr |
| 26 | Google AgentSpace | 📝 Draft | Advanced | 2hr |
| 27 | Third-Party Framework Tools | 📝 Draft | Advanced | 1.5hr |
| 28 | Using Other LLMs | 📝 Draft | Advanced | 2hr |
| 29 | UI Integration Intro | 📝 Draft | Intermediate | 1.5hr |
| 30 | Next.js ADK Integration | 📝 Draft | Advanced | 2hr |
| 31 | React Vite ADK Integration | 📝 Draft | Advanced | 1.5hr |
| 32 | Streamlit ADK Integration | 📝 Draft | Advanced | 2hr |
| 33 | Slack ADK Integration | 📝 Draft | Advanced | 2hr |
| 34 | PubSub ADK Integration | 📝 Draft | Advanced | 2hr |

## 📊 Project Completion Status

### ✅ Completed Tutorials (12/34)

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

**All completed tutorials include:**

- ✅ Working code implementations in `tutorial_implementation/`
- ✅ Comprehensive test suites with pytest
- ✅ Proper project structure (Makefile, requirements.txt, pyproject.toml)
- ✅ Environment configuration (.env.example)
- ✅ Documentation and usage examples
- ✅ Integration with ADK web interface

### 📝 Draft Tutorials (22/34)

The following tutorials have detailed documentation but require implementation:

**Advanced Features (Tutorials 13-28):**

- Code execution environments, streaming responses, audio processing
- MCP protocol integration, inter-agent communication, observability
- File handling, configuration management, multimodal capabilities
- Model optimization, enterprise deployment, best practices
- Third-party integrations and multi-provider LLM support

**UI Integration (Tutorials 29-34):**

- Framework integration patterns (Next.js, React, Streamlit)
- Enterprise messaging (Slack) and event-driven systems (PubSub)

**Next Steps for Draft Tutorials:**

1. Implement working code examples following established patterns
2. Add comprehensive test coverage
3. Create proper project structure and dependencies
4. Verify integration with ADK ecosystem
5. Update documentation based on implementation experience

## 🛠️ Development Tools

- **ADK Web UI**: `adk web` - Interactive development interface
- **Testing Framework**: Comprehensive evaluation and testing tools
- **Deployment CLI**: `adk deploy` - Multiple deployment options
- **Code Generation**: Automated agent and tool scaffolding

## 🤝 Contributing

This project welcomes contributions! Areas for contribution:

- Tutorial improvements and corrections
- Additional integration examples
- New research on emerging patterns
- Documentation enhancements
- Code examples and best practices

## 👨‍💻 About the Creator

This project was created by **Raphaël MANSUY**, a Chief Technology Officer, Author, AI Strategist, and Data Engineering Expert based in Hong Kong SAR, China.

With over 20 years of experience in AI and innovation across various sectors, Raphaël is dedicated to democratizing data management and artificial intelligence. As CTO and Co-Founder of Elitizon, a technology venture studio, he leads the development of AI strategies tailored to meet specific business goals.

Raphaël serves as a consultant for prominent organizations including Quantmetry (Capgemini Invent) and DECATHLON, providing insights on data governance, engineering, and analytics operating models. He is also the co-founder of QuantaLogic (PARIS), focusing on unlocking the potential of generative AI for businesses.

A thought leader in the AI community, Raphaël conducts daily reviews of AI research and shares insights with his 31,000 LinkedIn followers. He holds a Master's degree in Database and Artificial Intelligence from Université de Bourgogne and various certifications in machine learning and data science.

Raphaël teaches AI courses at the University of Oxford's Lifelong Learning program, where he covers topics including Generative AI, Cloud computing, and MLOps.

## 📄 License

See individual component licenses:

- `adk-python/LICENSE`
- `adk-java/LICENSE`
- `adk-web/LICENSE` (if applicable)

## 📚 Resources

- **Official ADK Documentation**: [https://google.github.io/adk-docs/](https://google.github.io/adk-docs/)
- **ADK Python Repository**: [https://github.com/google/adk-python](https://github.com/google/adk-python)
- **Google AI Studio**: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
- **ADK Web Interface**: Run `adk web` after installation

## 🎯 Mission

To provide the most comprehensive and practical guide for mastering Google ADK and building production-ready AI agents, from concept to deployment.

---

**🚀 Ready to build amazing AI agents? Start with `overview.md` and Tutorial 01!**
