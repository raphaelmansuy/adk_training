# Tutorial 02: Function Tools Implementation

A complete, working implementation of the Function Tools tutorial. Transform your agent from a conversationalist into a problem-solver with custom Python functions that automatically execute based on user requests.

## Quick Start

```bash
# Setup and install
make setup

# Run the finance assistant
make dev

# Run comprehensive tests
make test

# Clean up
make clean
```

## What This Agent Does

- **Personal Finance Assistant**: Calculates compound interest, loan payments, and savings goals
- **Automatic Tool Selection**: LLM decides when to use tools based on user requests
- **Parallel Tool Execution**: ADK automatically runs multiple tools simultaneously for better performance
- **Real-World Calculations**: Accurate financial math with human-friendly explanations

## Project Structure

```
tutorial02/
├── README.md                    # This file
├── Makefile                     # Build and test commands
├── finance_assistant/           # Agent implementation
│   ├── __init__.py             # Python package marker
│   ├── agent.py                # Agent with 3 financial calculation tools
│   └── .env.example            # Environment template
├── tests/                       # Comprehensive test suite
│   ├── __init__.py
│   ├── test_agent.py           # Agent configuration tests
│   ├── test_tools.py           # Tool function tests
│   ├── test_imports.py         # Import validation tests
│   └── test_structure.py       # Project structure tests
├── requirements.txt            # Python dependencies
└── parallel_demo/               # Advanced parallel execution demo
    ├── __init__.py
    ├── agent.py                # Parallel tool calling example
    └── .env.example
```

## Prerequisites

- Python 3.9+
- Google API key (get free at [Google AI Studio](https://aistudio.google.com/app/apikey))
- Completed Tutorial 01 (basic agent setup)

## Setup Instructions

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API key**:

   ```bash
   cp finance_assistant/.env.example finance_assistant/.env
   # Edit finance_assistant/.env and add your GOOGLE_API_KEY
   ```

3. **Run the agent**:

   ```bash
   make dev
   ```

   Then open <http://localhost:8000> in your browser

## Demo Scenarios

### Basic Financial Calculations

**Compound Interest**:

```text
User: If I invest $10,000 at 6% annual interest for 5 years, how much will I have?

Agent: Let me calculate that for you!

[Tool Call: calculate_compound_interest(principal=10000, annual_rate=6, years=5)]

Based on the calculation, if you invest $10,000 at 6% annual interest compounded
monthly for 5 years, you'll have approximately $13,488.50. That means you'll earn
$3,488.50 in interest - not bad!
```

**Loan Payments**:

```text
User: What's the monthly payment for a $300,000 mortgage at 4.5% for 30 years?

Agent: I'll calculate that mortgage payment for you.

[Tool Call: calculate_loan_payment(loan_amount=300000, annual_rate=4.5, years=30)]

For a $300,000 loan at 4.5% interest over 30 years, your monthly payment would be
$1,520.06. Over the life of the loan, you'll pay $547,221.60 total, with
$247,221.60 being interest.
```

**Savings Goals**:

```text
User: I want to save $50,000 for a down payment in 3 years. How much per month?

Agent: Great goal! Let me calculate your monthly savings needed.

[Tool Call: calculate_monthly_savings(target_amount=50000, years=3)]

To reach $50,000 in 3 years with a 5% annual return, you need to save $1,315.07
per month. You'll contribute $47,342.52 total, with the rest coming from investment
returns. Keep up the great work!
```

### Parallel Tool Execution Demo

Try the advanced parallel execution example:

```bash
make parallel-demo
```

**Parallel Query**:

```text
Compare these three investment options:
1. $10,000 at 5% for 10 years
2. $15,000 at 4% for 10 years
3. $12,000 at 6% for 10 years
```

**What happens**:

- Gemini recognizes it needs 3 separate calculations
- ADK executes ALL THREE tools simultaneously (not sequentially)
- Results return in ~0.5s instead of ~1.5s
- Agent provides comparative analysis

## Key Features Demonstrated

- **Function Tools**: Regular Python functions become LLM-callable tools
- **Automatic Tool Selection**: LLM reads docstrings and decides when to use tools
- **Parallel Execution**: Multiple tools run simultaneously via `asyncio.gather()`
- **Type Hints**: Parameter types guide LLM tool usage
- **Structured Returns**: Dict format with status and human-readable reports
- **Error Handling**: Graceful error handling with meaningful messages
- **Real-World Use Case**: Practical financial calculations

## Development Commands

| Command | Description |
|---------|-------------|
| `make setup` | Install dependencies and setup environment |
| `make dev` | Start ADK development server (main agent) |
| `make parallel-demo` | Start ADK dev server (parallel execution demo) |
| `make test` | Run all tests |
| `make test-unit` | Run unit tests only |
| `make test-tools` | Test financial calculation functions |
| `make test-integration` | Run integration tests |
| `make clean` | Remove generated files |
| `make help` | Show all available commands |

## Testing

Run the comprehensive test suite:

```bash
make test
```

Tests cover:

- Agent configuration and tool registration
- Financial calculation accuracy
- Tool function error handling
- Import validation
- Project structure compliance
- Parallel execution patterns (when API key available)

## Tool Functions Implemented

### 1. `calculate_compound_interest()`

- **Purpose**: Calculate investment growth with compound interest
- **Formula**: `A = P(1 + r/n)^(nt)`
- **Parameters**: principal, annual_rate, years, compounds_per_year
- **Returns**: Final amount, interest earned, formatted report

### 2. `calculate_loan_payment()`

- **Purpose**: Calculate monthly payments for loans/mortgages
- **Formula**: `M = P[r(1+r)^n]/[(1+r)^n-1]`
- **Parameters**: loan_amount, annual_rate, years
- **Returns**: Monthly payment, total paid, total interest

### 3. `calculate_monthly_savings()`

- **Purpose**: Determine monthly savings needed to reach a goal
- **Formula**: `PMT = FV / [((1+r)^n - 1) / r]`
- **Parameters**: target_amount, years, annual_return
- **Returns**: Monthly savings amount, total contributed, interest earned

## Advanced Features

### Parallel Tool Calling

ADK automatically executes multiple tools in parallel when:

- LLM requests multiple tools in a single turn
- Tools are independent (no sequential dependencies)
- Using Gemini 2.5-flash or 2.0-flash models

**Performance**: 3x speedup for 3 parallel tools (0.5s vs 1.5s)

### Tool Design Best Practices

- **Clear Names**: `calculate_compound_interest` not `calc_int`
- **Comprehensive Docstrings**: Explain when and how to use
- **Type Hints**: Guide LLM parameter usage
- **Structured Returns**: `{"status": "success", "report": "..."}`
- **Error Handling**: Return error dicts, don't raise exceptions
- **Focused Scope**: One function = one specific task

## Troubleshooting

### Agent not calling tools

- Check Events tab - did Gemini consider the tool?
- Verify docstring clearly explains when to use the tool
- Ensure function name matches user intent

### Wrong parameters passed

- Review type hints and parameter descriptions
- Add examples in docstrings
- Check for parameter name conflicts

### Tool execution errors

- Add try/except blocks in tool functions
- Return error status dicts instead of raising exceptions
- Test tools independently before integration

### Parallel execution not working

- Use Gemini 2.5-flash or 2.0-flash models
- Ensure tools are truly independent
- Check Events tab for parallel FunctionCall events

## Next Steps

- **Tutorial 03**: OpenAPI Tools - Connect to real web APIs
- **Tutorial 04**: Sequential Workflows - Chain agents together
- **Tutorial 05**: Parallel Processing - Coordinate multiple agents

## Files Overview

- **`finance_assistant/agent.py`**: Main agent with 3 financial calculation tools
- **`parallel_demo/agent.py`**: Advanced parallel tool execution example
- **`tests/test_tools.py`**: Validates financial calculation accuracy
- **`tests/test_agent.py`**: Tests agent configuration and tool registration

## Performance Notes

- **Parallel Execution**: 3x faster for multiple independent calculations
- **CPU-bound**: Python GIL limits pure CPU parallelism but asyncio helps
- **I/O-bound**: Network calls benefit most from parallel execution
- **Mixed workloads**: Best performance with combination of both

Built with ❤️ using Google ADK. Your agent now has superpowers! 🚀💰
