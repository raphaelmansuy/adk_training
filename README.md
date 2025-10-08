# Google ADK Training Project

A comprehensive training and research project for mastering Google Agent Development Kit (ADK) and Generative AI concepts from first principles.

## 🎯 Overview

This project provides a complete learning journey through Google ADK, featuring:

- **28 comprehensive tutorials** covering everything from basic agents to production deployment
- **Mental models framework** for understanding ADK patterns and Generative AI concepts
- **Research and integration examples** for various UI frameworks and deployment scenarios
- **Production-ready code examples** and best practices

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
├── tutorial/                      # 28 comprehensive tutorials
│   ├── 01_hello_world_agent.md    # Agent basics
│   ├── 02_function_tools.md       # Custom tools
│   ├── 03_openapi_tools.md        # REST API integration
│   ├── ...                        # Workflows, state, deployment
│   └── 34_pubsub_adk_integration.md
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
# Follow the tutorial/01_hello_world_agent.md guide
```

## 📖 Learning Path

### 1. Foundation (Start Here)

- Read `overview.md` - Mental models for ADK mastery
- Tutorial 01: Hello World Agent
- Tutorial 02: Function Tools
- Tutorial 08: State & Memory

### 2. Workflows (Orchestration)

- Tutorial 04: Sequential Workflows
- Tutorial 05: Parallel Processing
- Tutorial 06: Multi-Agent Systems
- Tutorial 07: Loop Agents

### 3. Production (Deployment)

- Tutorial 09: Callbacks & Guardrails
- Tutorial 10: Evaluation & Testing
- Tutorial 26: Google AgentSpace Deployment

### 4. Integration (Extend)

- Tutorial 03: OpenAPI Tools
- Tutorial 16: MCP Integration
- Tutorial 27: Third-Party Tools
- Tutorial 28: Multi-Provider LLMs

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

| Tutorial | Topic | Complexity | Time |
|----------|-------|------------|------|
| 01 | Hello World Agent | Beginner | 30min |
| 02 | Function Tools | Beginner | 45min |
| 03 | OpenAPI Tools | Beginner | 1hr |
| 04 | Sequential Workflows | Intermediate | 1hr |
| 05 | Parallel Processing | Intermediate | 1hr |
| 06 | Multi-Agent Systems | Intermediate | 1.5hr |
| 07 | Loop Agents | Advanced | 1hr |
| 08 | State & Memory | Advanced | 1.5hr |
| 09 | Callbacks & Guardrails | Advanced | 2hr |
| 10 | Evaluation & Testing | Advanced | 1.5hr |
| ... | ... | ... | ... |
| 28 | Using Other LLMs | Advanced | 2hr |

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
