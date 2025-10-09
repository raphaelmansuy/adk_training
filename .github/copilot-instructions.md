# Google ADK Training Project - AI Coding Guidelines

## Project Overview

This is a comprehensive training repository for Google Agent Development Kit (ADK), featuring 28 tutorials, mental models, research, and automated testing. The project teaches agent development from first principles to production deployment.

## Architecture Patterns

### Agent Hierarchy & Composition

- **Root Agent Convention**: Every agent module must export a `root_agent` variable as the main entry point
- **Sequential Workflows**: Use `SequentialAgent` for ordered pipelines where each step depends on the previous
- **Parallel Workflows**: Use `ParallelAgent` for independent tasks that can run simultaneously
- **Loop Workflows**: Use `LoopAgent` for iterative refinement with critic/refiner patterns
- **State Communication**: Agents communicate via `output_key` (saves to session state) and state interpolation `{key_name}`

### Tool Development Patterns

- **Function Tools**: Python functions become callable tools - return structured dicts with `status`, `report`, and data fields
- **OpenAPI Tools**: Use `OpenAPIToolset` for REST API integration with automatic tool generation
- **MCP Tools**: Use `MCPToolset` for standardized protocol tools (filesystem, databases)
- **Return Format**: Tools return `{'status': 'success/error', 'report': 'human readable', ...data}`

### State Management

- **Session State**: `state['key']` for conversation-scoped data
- **User State**: `state['user:key']` for cross-session user data
- **App State**: `state['app:key']` for global application data
- **Temporary State**: `state['temp:key']` for invocation-only data

## Development Workflow

### Project Structure

```
tutorial_implementation/tutorialXX/
├── Makefile              # Standard commands (setup, dev, test, demo)
├── requirements.txt      # Python dependencies
├── agent_name/           # Agent implementation
│   ├── __init__.py
│   ├── agent.py          # Main agent (exports root_agent)
│   └── .env.example      # Environment variables
└── tests/                # Comprehensive test suite
    ├── test_agent.py     # Agent configuration tests
    ├── test_imports.py   # Import validation
    └── test_structure.py # Project structure tests
```

### Testing Patterns

- **Unit Tests**: Mock external dependencies, test agent configuration and tool logic
- **Integration Tests**: Test with real ADK components when GOOGLE_API_KEY available
- **Test Organization**: Group by functionality (TestAgentConfig, TestTools, TestIntegration)
- **Test Runner**: Use `pytest` with `pytest-cov` for coverage reporting

### Common Commands

```bash
# Setup environment
make setup              # Install dependencies
export GOOGLE_API_KEY=your_key

# Development
make dev                # Start ADK web interface (localhost:8000)
make demo               # Show demo prompts and usage

# Testing
make test               # Run all tests
pytest tests/ -v        # Detailed test output

# Cleanup
make clean              # Remove cache files and artifacts
```

## Integration Points

### UI Frameworks

- **Next.js**: Use CopilotKit for React integration (`/api/copilotkit` endpoint)
- **Vite**: Similar CopilotKit setup with different build configuration
- **Streamlit**: Direct ADK integration without CopilotKit middleware
- **FastAPI Backend**: Standard REST API with CORS configuration for frontend origins

### External Services

- **Google ADK**: Core agent framework with Gemini models
- **CopilotKit**: React component library for AI chat interfaces
- **Google Cloud**: Vertex AI, Cloud Run, Cloud Storage for production deployment
- **Google Search**: Built-in grounding tool for web search capabilities

## Code Conventions

### Agent Definition

```python
# Standard agent pattern
root_agent = Agent(
    name="agent_name",                    # snake_case, descriptive
    model="gemini-2.5-flash",            # Use latest Gemini models
    description="What this agent does",  # Clear, concise description
    instruction="Detailed behavior...",  # Comprehensive prompt
    tools=[tool1, tool2],                # List of tool functions
    output_key="result_key"              # Optional: save to state
)
```

### Tool Functions

```python
def tool_name(param: Type) -> Dict[str, Any]:
    """
    Docstring explaining what the tool does.

    Args:
        param: Description of parameter

    Returns:
        Dict with status, report, and data fields
    """
    try:
        # Tool logic here
        result = {...}
        return {
            'status': 'success',
            'report': 'Human-readable success message',
            'data': result
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': 'Human-readable error message'
        }
```

### Workflow Composition

```python
# Sequential pipeline
sequential_agent = SequentialAgent(
    name="PipelineName",
    sub_agents=[agent1, agent2, agent3],  # Execute in order
    description="What the pipeline does"
)

# Parallel execution
parallel_agent = ParallelAgent(
    name="ParallelName",
    sub_agents=[agent1, agent2, agent3],  # Execute simultaneously
    description="What the parallel tasks do"
)

# Iterative refinement
loop_agent = LoopAgent(
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=5,  # Prevent infinite loops
    description="Iterative improvement process"
)
```

## Key Files & Directories

- `overview.md`: Mental models and architectural concepts
- `docs/tutorial/`: 28 comprehensive tutorials (01_hello_world_agent.md through 34_pubsub_adk_integration.md)
- `tutorial_implementation/`: Executable code for each tutorial
- `research/`: ADK source code analysis and integration examples
- `test_tutorials/`: Automated testing framework with 70+ tests
- `https://github.com/google/adk-python`: Official ADK source code and documentation

## Deployment Options

- **Local Development**: `adk web` for interactive development
- **Cloud Run**: `adk deploy cloud_run` for serverless production
- **Vertex AI Agent Engine**: `adk deploy agent_engine` for managed enterprise deployment
- **GKE**: `adk deploy gke` for custom Kubernetes infrastructure

## Quality Standards

- **Error Handling**: All tools return structured error responses
- **Documentation**: Comprehensive docstrings for all public functions
- **Testing**: 100% test coverage for implemented tutorials
- **State Safety**: Use appropriate state scopes (temp, session, user, app)
- **Performance**: Prefer parallel execution for independent tasks

## Common Patterns to Avoid

- Don't create agents without proper error handling in tools
- Don't use generic Exception catching - be specific
- Don't hardcode API keys - use environment variables
- Don't create infinite loops in LoopAgent - always set max_iterations
- Don't mix state scopes inappropriately (session data in app scope)

## Getting Help

- Read `overview.md` first for mental models and decision frameworks
- Check `docs/tutorial/XX_tutorial_name.md` for detailed implementation guides
- Run `make demo` in any tutorial directory for quick examples
- Use `adk web` for interactive experimentation
- Check `test_tutorials/` for working examples and test patterns

## Tips and lessons learned

- Always pipe your command with cat to avoid issues with certain shells example, to avoid pagination issues in zsh:

```bash
ls -la | cat
```

- If you are not sure seek the truth in ./research where we have the complete source code of ADK and associated projects. You can also check the official documentation of each project and Github repositories.
- Never edit or producte .env files directly in the repository. Always use .env.example as a template and create your own .env file for local development.

### ADK Agent Discovery (Critical for Web Interface)

**Problem**: `adk web agent_name` fails to load agents in the web interface.

**Root Cause**: ADK requires agents to be installed as Python packages to be discoverable.

**Solution**:

1. Create `setup.py` in tutorial root directory:

```python
from setuptools import setup, find_packages

setup(
    name="agent_name",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["google-genai>=1.15.0"],
)
```

2. Update Makefile setup command:

```makefile
setup:
	pip install -r requirements.txt
	pip install -e .  # Installs agent as discoverable package
```

3. Use `adk web` (not `adk web agent_name`) to show agent dropdown in web interface.

**Key Difference from Tutorial 01**: Tutorial 01 uses `pip install -e .` and `adk web` dropdown, while initial Tutorial 10 tried `adk web support_agent` which doesn't work without package installation.

**Learned During**: Tutorial 10 implementation - agent couldn't be selected in ADK web interface until proper package installation was implemented.

## What you must ensure

- If you want to report what you have done, updated or achieve never report that in the tutorial or in the implementation. It must be done in a ./log directory at the root of the project.

Use path: ./log/YYYYMMDD_HHMMSS_description_of_your_change.md

- Never commit any file that contains secrets or API keys.

- Prefer a pyproject instead of a setup.py file.
