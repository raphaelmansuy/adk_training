# Tutorial 04: Sequential Workflows - Blog Creation Pipeline

A complete implementation of a blog post creation pipeline using ADK's `SequentialAgent`. This demonstrates how to chain multiple agents in a strict sequence where each agent's output feeds into the next.

## Pipeline Overview

The blog creation pipeline consists of 4 agents that run in sequence:

1. **Research Agent** - Gathers key facts and information about the topic
2. **Writer Agent** - Creates an engaging blog post draft from the research
3. **Editor Agent** - Reviews the draft and provides constructive feedback
4. **Formatter Agent** - Applies editorial feedback and formats as markdown

## Quick Start

```bash
# Install dependencies
make setup

# Start the development server
make dev
```

Then open `http://localhost:8000` in your browser and select "blog_pipeline".

## Try These Prompts

- "Write a blog post about artificial intelligence"
- "Create a blog post explaining how solar panels work"
- "Write about the history of the Internet"
- "Blog post about electric vehicles and their impact on climate"

## How It Works

### State Flow
```
User Input → Research Agent → state['research_findings']
    ↓
Writer Agent (reads {research_findings}) → state['draft_post']
    ↓
Editor Agent (reads {draft_post}) → state['editorial_feedback']
    ↓
Formatter Agent (reads {draft_post} + {editorial_feedback}) → Final Output
```

### Key Concepts

- **`SequentialAgent`**: Orchestrates agents in strict order
- **`output_key`**: Saves agent response to shared state
- **`{key}` syntax**: Injects state values into agent instructions
- **Shared `InvocationContext`**: All agents access the same state

## Project Structure

```
tutorial04/
├── blog_pipeline/           # Agent implementation
│   ├── __init__.py         # Package marker
│   ├── agent.py            # Pipeline definition
│   └── .env.example        # Environment template
├── tests/                  # Comprehensive tests
│   ├── __init__.py
│   ├── test_agent.py       # Agent and pipeline tests
│   ├── test_imports.py     # Import validation
│   └── test_structure.py   # Project structure tests
├── requirements.txt        # Dependencies
├── Makefile               # Development commands
└── README.md              # This file
```

## Testing

```bash
# Run the full test suite
make test

# Tests cover:
# - Agent configuration and imports
# - SequentialAgent pipeline structure
# - State management and data flow
# - Individual agent functionality
# - Integration testing
```

## Development

### Adding New Agents

To extend the pipeline, add new agents to the `sub_agents` list:

```python
# Add a new fact-checker agent
fact_checker_agent = Agent(
    name="fact_checker",
    model="gemini-2.0-flash",
    instruction="Verify facts in: {draft_post}",
    output_key="fact_check_results"
)

blog_creation_pipeline = SequentialAgent(
    sub_agents=[
        research_agent,
        writer_agent,
        fact_checker_agent,  # Insert before editor
        editor_agent,
        formatter_agent
    ]
)
```

### Modifying Agent Instructions

Each agent has a focused instruction. Update them to customize behavior:

```python
writer_agent = Agent(
    instruction=(
        "Write a technical blog post based on: {research_findings}\n"
        "Include code examples and be very detailed..."
    ),
    output_key="draft_post"
)
```

## Configuration

Copy `.env.example` to `.env` and add your API key:

```bash
cp blog_pipeline/.env.example blog_pipeline/.env
# Edit .env with your GOOGLE_API_KEY
```

## Events & Debugging

Open the **Events tab** in the ADK web UI to see:
- Each agent starting and completing
- State values being saved and injected
- The exact sequence of execution

This is invaluable for understanding and debugging pipelines.

## Real-World Applications

Sequential workflows are perfect for:

- **Content Creation**: Research → Write → Edit → Publish
- **Data Processing**: Extract → Transform → Validate → Load
- **Quality Control**: Create → Review → Fix → Approve
- **Analysis Pipelines**: Gather → Analyze → Visualize → Report
- **Code Workflows**: Write → Review → Refactor → Test

## Related Tutorials

- [Tutorial 01](../tutorial01/): Hello World Agent - Basic agent setup
- [Tutorial 02](../tutorial02/): Function Tools - Adding custom tools
- [Tutorial 03](../tutorial03/): OpenAPI Tools - API integration
- Tutorial 05: Parallel Processing - Running agents concurrently

## Contributing

This implementation follows the patterns established in previous tutorials. For changes:

1. Update the agent code in `blog_pipeline/agent.py`
2. Add corresponding tests in `tests/`
3. Update this README if needed
4. Run `make test` to ensure everything works

## License

This tutorial is part of the ADK training series.