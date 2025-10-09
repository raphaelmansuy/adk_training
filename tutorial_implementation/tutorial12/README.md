# Strategic Problem Solver - Tutorial 12 Implementation

This implementation demonstrates **advanced reasoning capabilities** using BuiltInPlanner, PlanReActPlanner, and custom BasePlanner implementations for complex business problem solving.

## Overview

The Strategic Problem Solver showcases three different planning approaches:

- **BuiltInPlanner**: Uses Gemini 2.0+'s native thinking capabilities with transparent reasoning
- **PlanReActPlanner**: Implements structured Plan → Reason → Act → Observe → Replan workflow
- **StrategicPlanner**: Custom BasePlanner subclass for domain-specific business strategy analysis

## Features

### 🤖 Multiple Planning Strategies

- Transparent thinking with BuiltInPlanner
- Structured reasoning with PlanReActPlanner
- Domain-specific workflows with custom planners

### 🛠️ Business Analysis Tools

- **Market Analysis**: Industry research and trend identification
- **ROI Calculator**: Financial projections and investment analysis
- **Risk Assessment**: Business risk evaluation and mitigation strategies
- **Strategy Reports**: Document and save strategic recommendations

### 📊 Comprehensive Testing

- 30+ unit tests covering all functionality
- Integration tests for complete workflows
- Error handling and edge case coverage

## Quick Start

### 1. Setup Environment

```bash
# Clone and navigate to the implementation
cd tutorial_implementation/tutorial12

# Install dependencies
make setup

# Copy environment template
cp strategic_solver/.env.example strategic_solver/.env

# Edit .env and add your Google AI API key
# GOOGLE_API_KEY=your_actual_api_key_here
```

### 2. Run Development Server

```bash
# Start ADK web interface
make dev

# Open http://localhost:8000 in your browser
# Select "strategic_solver" from the agent dropdown
```

### 3. Test the Implementation

```bash
# Run comprehensive test suite
make test

# See example queries you can test
make examples

# Run demo examples
make demo
```

## Project Structure

```
tutorial12/
├── strategic_solver/           # Agent implementation
│   ├── __init__.py            # Package marker
│   ├── agent.py               # Main agent with planners and tools
│   └── .env.example           # Environment configuration template
├── tests/                     # Comprehensive test suite
│   ├── __init__.py
│   ├── test_imports.py        # Import and structure tests
│   ├── test_tools.py          # Tool functionality tests
│   ├── test_agents.py         # Agent and planner tests
│   └── test_integration.py    # Integration and workflow tests
├── pyproject.toml             # Modern Python packaging configuration
├── requirements.txt           # Runtime dependencies
├── Makefile                  # Development commands
└── README.md                 # This file
```

## Agent Variants

### BuiltInPlanner Agent (`builtin_planner_agent`)

- **Purpose**: Demonstrates transparent thinking capabilities
- **Features**: Shows internal reasoning process to users
- **Use Case**: Educational applications, debugging, trust-building
- **Configuration**: `ThinkingConfig(include_thoughts=True)`

### PlanReActPlanner Agent (`plan_react_agent`)

- **Purpose**: Structured problem-solving with explicit planning phases
- **Features**: Plan → Reason → Act → Observe → Replan workflow
- **Use Case**: Complex multi-step problems requiring systematic approach
- **Configuration**: Standard PlanReActPlanner with XML tags

### StrategicPlanner Agent (`strategic_planner_agent`)

- **Purpose**: Domain-specific business strategy analysis
- **Features**: Custom workflow: Analysis → Evaluation → Strategy → Validation
- **Use Case**: Business consulting and strategic planning
- **Configuration**: Custom BasePlanner subclass

## Business Analysis Tools

### Market Analysis Tool

```python
result = analyze_market("healthcare", "North America", tool_context)
# Returns: growth_rate, competition, trends, opportunities, threats
```

### ROI Calculator Tool

```python
result = calculate_roi(100000, 8.5, 5, tool_context)
# Returns: final_value, total_profit, roi_percentage, annual_breakdown
```

### Risk Assessment Tool

```python
result = assess_risk(["competition", "regulatory_changes"], tool_context)
# Returns: risk_level, mitigation_suggestions, factor_scores
```

### Strategy Report Tool

```python
result = await save_strategy_report(problem, strategy, tool_context)
# Saves formatted markdown report with timestamp
```

## Example Usage

### Basic Strategic Analysis

```
User: "Should we expand into the Asian healthcare market?"

Agent Response:
[Thinking]
This is a complex strategic decision requiring market analysis,
financial projections, and risk assessment...

Market Analysis: Healthcare sector growing at 8.5% annually
Financial Projection: 5-year ROI of 46.8% with $500K investment
Risk Assessment: Medium risk with regulatory mitigation needed

Recommendation: Proceed with phased approach...
```

### Structured Planning Example

```
User: "How should we mitigate cybersecurity risks?"

Agent Response:
<PLANNING>
1. Assess current risk posture
2. Identify critical vulnerabilities
3. Evaluate mitigation strategies
4. Create implementation timeline
</PLANNING>

<ACTION>
Analyzing risk factors...
</ACTION>

<OBSERVATION>
High-risk factors identified: phishing, data breaches, insider threats
</OBSERVATION>

<FINAL_ANSWER>
Implement comprehensive cybersecurity framework:
1. Employee training program
2. Multi-factor authentication
3. Regular security audits
4. Incident response plan
</FINAL_ANSWER>
```

## Testing

### Run All Tests

```bash
make test
```

### Test Coverage

- **Import Tests**: Module loading and structure validation
- **Tool Tests**: Individual tool functionality (25+ test cases)
- **Agent Tests**: Planner configuration and agent setup
- **Integration Tests**: Complete workflow testing

### Test Categories

#### Unit Tests

- Tool input validation and error handling
- Calculation accuracy (ROI, risk scores)
- Data structure correctness

#### Integration Tests

- Multi-tool workflow execution
- Error propagation handling
- Planner comparison and validation

## Configuration

### Environment Variables

```bash
# Required
GOOGLE_API_KEY=your_google_ai_api_key

# Optional
GOOGLE_GENAI_USE_VERTEXAI=0  # Set to 1 for VertexAI
GOOGLE_CLOUD_PROJECT=your_project
GOOGLE_CLOUD_LOCATION=us-central1
```

### Model Configuration

- **Model**: `gemini-2.0-flash` (supports thinking capabilities)
- **Temperature**: 0.3-0.4 (balanced for strategic analysis)
- **Max Tokens**: 3000 (sufficient for detailed analysis)

## Development Commands

```bash
# Setup and installation
make setup          # Install dependencies and package in development mode
make dev           # Start ADK web interface (http://localhost:8000)

# Testing and examples
make test          # Run comprehensive test suite (60+ tests)
make examples      # Show example queries you can test with the agents
make demo          # Run automated strategic problem-solving examples

# Code quality
make lint          # Check code style with flake8
make format        # Format code with black

# Cleanup
make clean         # Remove cache files and artifacts
```

## Troubleshooting

### Common Issues

#### "Planner not showing thinking"

- Ensure using Gemini 2.0+ model
- Check `ThinkingConfig(include_thoughts=True)` for BuiltInPlanner
- Verify API key has access to thinking-enabled models

#### "PlanReAct tags not appearing"

- Check that PlanReActPlanner is properly instantiated
- Ensure agent instruction doesn't override planning format
- Try increasing temperature slightly for more structured output

#### "Tool execution fails"

- Verify tool functions are properly imported
- Check tool context is passed correctly
- Ensure async tools are awaited properly

#### "Import errors"

- Run `make setup` to install dependencies
- Check Python path includes strategic_solver directory
- Verify all required packages are installed

### Debug Mode

Enable detailed logging by setting environment variable:

```bash
export ADK_DEBUG=1
```

## API Reference

### Planner Classes

- `BuiltInPlanner(thinking_config)` - Native model thinking
- `PlanReActPlanner()` - Structured planning workflow
- `StrategicPlanner()` - Custom business strategy planner

### Tool Functions

- `analyze_market(industry, region, context)` - Market research
- `calculate_roi(investment, return_rate, years, context)` - Financial analysis
- `assess_risk(factors, context)` - Risk evaluation
- `save_strategy_report(problem, strategy, context)` - Report generation

## Performance Considerations

### Planner Overhead

- **BuiltInPlanner**: 4-6s (thinking transparency)
- **PlanReActPlanner**: 5-8s (structured workflow)
- **StrategicPlanner**: 5-7s (domain-specific analysis)

### Optimization Tips

- Use BuiltInPlanner for transparency needs
- Choose PlanReActPlanner for complex structured problems
- Reserve StrategicPlanner for business consulting scenarios
- Consider streaming for long responses

## Contributing

### Adding New Tools

1. Create tool function in `agent.py`
2. Add comprehensive tests in `test_tools.py`
3. Update agent tool lists
4. Add documentation and examples

### Adding New Planners

1. Extend `BasePlanner` class
2. Implement `build_planning_instruction` and `process_planning_response`
3. Add agent configuration
4. Create comprehensive tests

## Links

- **Tutorial**: [Tutorial 12: Planners & Thinking Configuration](../../../docs/tutorial/12_planners_thinking.md)
- **ADK Documentation**: https://google.github.io/adk-docs/
- **Gemini Models**: https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/gemini

## License

This implementation follows the same license as the ADK training repository.
