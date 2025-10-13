# Tutorial 20: YAML Configuration - Declarative Agent Setup

**Goal**: Master declarative agent configuration using YAML files to define agents, tools, and behaviors without writing Python code.

**What You'll Learn**:
- Creating agent configurations with `root_agent.yaml`
- Understanding `AgentConfig` and `LlmAgentConfig` schemas
- Configuring tools, models, and instructions in YAML
- Multi-agent systems in configuration files
- Loading and validating configurations

## Project Structure

```
tutorial20/
├── root_agent.yaml      # Agent configuration
├── run_agent.py         # Runner script
├── tools/               # Tool implementations
│   ├── __init__.py
│   └── customer_tools.py
├── tests/               # Comprehensive tests
│   ├── test_agent.py
│   ├── test_tools.py
│   ├── test_imports.py
│   └── test_structure.py
├── pyproject.toml       # Package configuration
├── requirements.txt     # Dependencies
└── Makefile            # Build commands
```

## Quick Start

### 1. Install Dependencies

```bash
make setup
```

### 2. Validate Configuration

```bash
make validate-config
```

### 3. Run the Agent

```bash
make dev
```

Open http://localhost:8000 in your browser and select 'customer_support' from the dropdown.

### 4. Run Demo Queries

Try these prompts in the ADK web UI:

- "I'm customer CUST-001 and I want to check my order ORD-001"
- "I need help with a login error"
- "I'd like a refund of $75 for order ORD-002"

## Configuration Overview

The `root_agent.yaml` defines a customer support system with:

- **Single Agent**: Customer support agent with comprehensive tools
- **Tools**: 11 functions for customer service operations

## Running Tests

```bash
make test
```

Tests cover:
- YAML configuration loading
- Tool function implementations
- Agent creation and validation
- Project structure verification

## Manual Testing

Run the agent directly with test queries:

```bash
python run_agent.py
```

## Configuration Details

### Agent Configuration Schema

```yaml
name: agent_name
model: gemini-2.0-flash
description: "Agent purpose"
instruction: |
  Multi-line instruction
  for the agent

generate_content_config:
  temperature: 0.7
  max_output_tokens: 2048

tools:
  - type: function
    name: tool_name
    description: "Tool description"

sub_agents:
  - name: sub_agent_1
    model: gemini-2.0-flash
    # ... sub-agent config
```

### Tool Implementation

Tools are Python functions that return structured dictionaries:

```python
def tool_name(param: Type) -> Dict[str, Any]:
    return {
        'status': 'success',
        'report': 'Human-readable message',
        'data': { ... }  # Tool-specific data
    }
```

## Environment Setup

### API Key Authentication

```bash
export GOOGLE_API_KEY=your_api_key_here
```

Get a free key at: https://aistudio.google.com/app/apikey

### Service Account Authentication

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
export GOOGLE_CLOUD_PROJECT=your_project_id
```

## Troubleshooting

### Configuration Errors

```bash
# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('root_agent.yaml'))"

# Test agent loading
python -c "from google.adk.agents import config_agent_utils; config_agent_utils.from_config('root_agent.yaml')"
```

### Import Errors

```bash
# Test tool imports
python -c "from tools.customer_tools import check_customer_status; print('OK')"
```

### Authentication Issues

Ensure you have either:
- `GOOGLE_API_KEY` environment variable, or
- `GOOGLE_APPLICATION_CREDENTIALS` and `GOOGLE_CLOUD_PROJECT` variables

## Advanced Usage

### Customizing Configuration

Edit `root_agent.yaml` to:
- Change model parameters
- Add new tools
- Modify agent instructions
- Add sub-agents

### Adding New Tools

1. Implement function in `tools/customer_tools.py`
2. Add to `tools/__init__.py` exports
3. Reference in `root_agent.yaml`

### Environment-Specific Configs

Create multiple YAML files:
- `config/dev/root_agent.yaml`
- `config/prod/root_agent.yaml`

Load with: `config_agent_utils.from_config('config/dev/root_agent.yaml')`

## Key Concepts

- **Declarative Configuration**: Define agents in YAML, not code
- **Tool Functions**: Python functions referenced by name in YAML
- **Multi-Agent Systems**: Orchestrator + specialized sub-agents
- **Configuration Validation**: Test configs before deployment
- **Environment Management**: Separate configs for dev/staging/prod

## Next Steps

- **Tutorial 21**: Learn Multimodal & Image Generation
- **Tutorial 22**: Master Model Selection & Optimization
- **Tutorial 23**: Explore Production Deployment

## Resources

- [ADK Configuration Documentation](https://google.github.io/adk-docs/configuration/)
- [AgentConfig API Reference](https://google.github.io/adk-docs/api/agent-config/)
- [YAML Specification](https://yaml.org/spec/)