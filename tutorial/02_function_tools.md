# Tutorial 02: Function Tools - Give Your Agent Superpowers

## Overview

Transform your agent from a conversationalist into a problem-solver! In this tutorial, you'll learn how to give your agent custom abilities by adding Python functions as tools. Your agent will automatically decide when to use these tools based on user requests.

## Prerequisites

- **Completed Tutorial 01** - You should have a working hello agent
- **Python functions knowledge** - Understanding of function definitions, parameters, and return values
- **Installed ADK** - `pip install google-adk`
- **API key configured** - From Tutorial 01

## Core Concepts

### Function Tools
**Function tools** are regular Python functions that you give to your agent. The agent can call these functions when it needs to perform specific tasks. ADK automatically:
- Reads your function signature (parameters, types, defaults)
- Reads your docstring (what the function does)
- Generates a schema the LLM can understand
- Lets the LLM decide WHEN to call your function

### Tool Discovery
The **LLM is smart** - it reads your function's name, docstring, and parameters, then decides if it should call that function based on the user's request. You don't manually trigger tools!

### Return Values
Tools should return **dictionaries** with:
- `"status"`: `"success"` or `"error"`
- `"report"`: The actual result or error message

This helps the LLM understand what happened.

## Use Case

We're building a **Personal Finance Assistant** that can:
- Calculate compound interest for savings
- Compute monthly loan payments
- Determine how much to save monthly for a goal
- Explain financial concepts

This demonstrates real-world tool use - calculations the LLM can't do accurately on its own!

## Step 1: Create Project Structure

Create a new directory for the finance assistant:

```bash
mkdir finance_assistant
cd finance_assistant
touch __init__.py agent.py .env
```

Copy your `.env` file from Tutorial 01, or create it with your API key.

## Step 2: Set Up Package Import

**finance_assistant/__init__.py**
```python
from . import agent
```

## Step 3: Define Tool Functions

Now the fun part - create Python functions that do the actual calculations!

**finance_assistant/agent.py**
```python
from __future__ import annotations

from google.adk.agents import Agent

# Tool 1: Calculate compound interest
def calculate_compound_interest(
    principal: float, 
    annual_rate: float, 
    years: int,
    compounds_per_year: int = 12
) -> dict:
    """Calculate compound interest for savings or investments.
    
    Args:
        principal: The initial amount invested (in dollars)
        annual_rate: The annual interest rate as a percentage (e.g., 5.5 for 5.5%)
        years: Number of years to calculate for
        compounds_per_year: How many times per year interest compounds (default: 12 for monthly)
        
    Returns:
        dict: Dictionary with status and calculation results
    """
    try:
        # Convert percentage to decimal
        rate_decimal = annual_rate / 100
        
        # Compound interest formula: A = P(1 + r/n)^(nt)
        final_amount = principal * (1 + rate_decimal / compounds_per_year) ** (compounds_per_year * years)
        interest_earned = final_amount - principal
        
        return {
            "status": "success",
            "report": (
                f"Initial investment: ${principal:,.2f}\n"
                f"Final amount after {years} years: ${final_amount:,.2f}\n"
                f"Total interest earned: ${interest_earned:,.2f}\n"
                f"Effective annual return: {annual_rate}%"
            )
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Calculation error: {str(e)}"
        }


# Tool 2: Calculate loan payments
def calculate_loan_payment(
    loan_amount: float,
    annual_rate: float,
    years: int
) -> dict:
    """Calculate monthly payment for a loan (mortgage, car, personal loan).
    
    Args:
        loan_amount: Total amount borrowed (in dollars)
        annual_rate: Annual interest rate as a percentage (e.g., 4.5 for 4.5%)
        years: Loan term in years
        
    Returns:
        dict: Dictionary with status and payment calculations
    """
    try:
        # Convert to monthly rate and number of payments
        monthly_rate = (annual_rate / 100) / 12
        num_payments = years * 12
        
        # Monthly payment formula: M = P[r(1+r)^n]/[(1+r)^n-1]
        if monthly_rate == 0:  # Handle 0% interest case
            monthly_payment = loan_amount / num_payments
        else:
            monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
        
        total_paid = monthly_payment * num_payments
        total_interest = total_paid - loan_amount
        
        return {
            "status": "success",
            "report": (
                f"Loan amount: ${loan_amount:,.2f}\n"
                f"Monthly payment: ${monthly_payment:,.2f}\n"
                f"Total paid over {years} years: ${total_paid:,.2f}\n"
                f"Total interest paid: ${total_interest:,.2f}"
            )
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Calculation error: {str(e)}"
        }


# Tool 3: Calculate savings needed
def calculate_monthly_savings(
    target_amount: float,
    years: int,
    annual_return: float = 5.0
) -> dict:
    """Calculate how much to save monthly to reach a financial goal.
    
    Args:
        target_amount: The amount you want to save (in dollars)
        years: Number of years to reach the goal
        annual_return: Expected annual return rate as percentage (default: 5.0%)
        
    Returns:
        dict: Dictionary with status and savings plan
    """
    try:
        months = years * 12
        monthly_rate = (annual_return / 100) / 12
        
        # Future value of annuity formula rearranged to solve for payment:
        # PMT = FV / [((1+r)^n - 1) / r]
        if monthly_rate == 0:
            monthly_savings = target_amount / months
        else:
            monthly_savings = target_amount / (((1 + monthly_rate)**months - 1) / monthly_rate)
        
        total_contributed = monthly_savings * months
        interest_earned = target_amount - total_contributed
        
        return {
            "status": "success",
            "report": (
                f"To reach ${target_amount:,.2f} in {years} years:\n"
                f"Save ${monthly_savings:,.2f} per month\n"
                f"Total you'll contribute: ${total_contributed:,.2f}\n"
                f"Estimated interest earned: ${interest_earned:,.2f}\n"
                f"Assuming {annual_return}% annual return"
            )
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Calculation error: {str(e)}"
        }


# Define the agent with all tools
root_agent = Agent(
    name="finance_assistant",
    model="gemini-2.0-flash",
    description="A personal finance assistant that helps with savings, loans, and financial planning calculations",
    instruction=(
        "You are a helpful personal finance assistant. You can help users with:\n"
        "- Calculating compound interest for savings and investments\n"
        "- Computing monthly payments for loans (mortgages, car loans, etc.)\n"
        "- Determining how much to save monthly to reach financial goals\n"
        "\n"
        "When users ask financial questions:\n"
        "1. Use the appropriate calculation tool\n"
        "2. Explain the results in simple terms\n"
        "3. Provide context and advice when relevant\n"
        "4. Be encouraging and positive about their financial planning!\n"
        "\n"
        "You are NOT a licensed financial advisor - remind users to consult professionals for major decisions."
    ),
    tools=[calculate_compound_interest, calculate_loan_payment, calculate_monthly_savings]
)
```

### Code Breakdown

**Function Signature Best Practices:**
1. **Type hints** - `principal: float`, `years: int` - tell the LLM what types to use
2. **Clear parameter names** - `annual_rate` not just `rate`
3. **Defaults for optional params** - `compounds_per_year: int = 12`
4. **Comprehensive docstring** - explain WHAT the function does and WHEN to use it

**Return Value Pattern:**
```python
return {
    "status": "success",  # or "error"
    "report": "Human-readable result"  # or "error_message" for errors
}
```

This structured format helps the LLM understand what happened and generate better responses.

**Tool Registration:**
Notice we just pass the functions directly to `tools=[...]` - ADK automatically converts them to tools!

## Step 4: Run Your Finance Assistant

Navigate to the parent directory and launch the Dev UI:

```bash
cd ..  # Go to parent of finance_assistant/
adk web
```

Open `http://localhost:8000` and select "finance_assistant" from the dropdown.

### Try These Prompts

**Savings Calculation:**
```
If I invest $10,000 at 6% annual interest for 5 years, how much will I have?
```

**Loan Payment:**
```
I want to buy a $300,000 house with a 30-year mortgage at 4.5% interest. 
What will my monthly payment be?
```

**Savings Goal:**
```
I want to save $50,000 for a down payment in 3 years. 
How much should I save each month?
```

**Mixed Question (LLM decides NOT to use tools):**
```
What's the difference between a Roth IRA and a traditional IRA?
```

Notice on this last one - the agent WON'T call any tools because none of them help answer that question. The LLM will just use its knowledge!

## Understanding Tool Execution

Open the **Events tab** in the Dev UI after sending a message. You'll see:

1. **User Message**: Your original question
2. **Function Call Event**: Shows which tool was called with what parameters
3. **Function Response Event**: Shows what the tool returned
4. **Model Response**: The final answer combining tool results with explanation

This is incredibly powerful for debugging - you can see EXACTLY when and how tools are used!

## Expected Behavior

**Example 1: Savings Calculation**
```
User: If I invest $10,000 at 6% annual interest for 5 years, how much will I have?

Agent: Let me calculate that for you!

[Tool Call: calculate_compound_interest(principal=10000, annual_rate=6, years=5)]

Based on the calculation, if you invest $10,000 at 6% annual interest compounded 
monthly for 5 years, you'll have approximately $13,488.50. That means you'll earn 
$3,488.50 in interest - not bad! This assumes the interest compounds monthly, which 
is common for savings accounts and many investment vehicles.
```

**Example 2: No Tool Needed**
```
User: Should I invest in stocks or bonds?

Agent: That's a great question about investment strategy! The choice between stocks 
and bonds depends on several factors: your age, risk tolerance, financial goals, and 
time horizon...

[No tools called - the LLM just uses its knowledge]
```

## How It Works (Behind the Scenes)

1. **User sends message** → ADK receives it
2. **ADK packages the message** with:
   - Your agent's instructions
   - Tool schemas (generated from your function signatures)
3. **Gemini (LLM) decides**: "Do I need a tool for this?"
   - **YES** → Returns a function call request
   - **NO** → Returns a text response
4. **If tool needed**, ADK:
   - Executes your Python function with the parameters Gemini provided
   - Gets the return value
   - Sends it back to Gemini
5. **Gemini generates final response** using the tool result

**You never manually call tools** - the LLM does it automatically!

## 🚀 Advanced: Parallel Tool Calling

**Source**: `google/adk/flows/llm_flows/functions.py`

One of ADK's most powerful features is **automatic parallel tool execution**. When the LLM requests multiple tools in a single turn, ADK executes them **simultaneously** using `asyncio.gather()` - dramatically improving performance!

### How It Works

When Gemini decides to call multiple tools, instead of executing them one-by-one:

```python
# ❌ Sequential execution (slow)
result1 = await tool1()  # Wait...
result2 = await tool2()  # Wait...
result3 = await tool3()  # Wait...
# Total time: ~6 seconds

# ✅ Parallel execution (fast) - ADK does this automatically!
results = await asyncio.gather(tool1(), tool2(), tool3())
# Total time: ~2 seconds (limited by slowest tool)
```

**You don't need to do anything** - ADK handles this automatically! Just define your tools normally.

### Real-World Example: Multi-City Financial Planning

Let's extend our finance assistant to handle parallel calculations:

```python
from __future__ import annotations
import asyncio
from google.adk.agents import Agent

def calculate_compound_interest(
    principal: float, 
    annual_rate: float, 
    years: int,
    compounds_per_year: int = 12
) -> dict:
    """Calculate compound interest for savings or investments.
    
    Args:
        principal: The initial amount invested (in dollars)
        annual_rate: The annual interest rate as a percentage (e.g., 5.5 for 5.5%)
        years: Number of years to calculate for
        compounds_per_year: How many times per year interest compounds (default: 12)
        
    Returns:
        dict: Dictionary with status and calculation results
    """
    # Add simulated delay to show parallel execution benefit
    import time
    time.sleep(0.5)  # Simulate API call or heavy computation
    
    rate_decimal = annual_rate / 100
    final_amount = principal * (1 + rate_decimal / compounds_per_year) ** (compounds_per_year * years)
    interest_earned = final_amount - principal
    
    return {
        "status": "success",
        "report": (
            f"Investment: ${principal:,.2f}\n"
            f"Final amount: ${final_amount:,.2f}\n"
            f"Interest earned: ${interest_earned:,.2f}"
        )
    }


def calculate_loan_payment(
    loan_amount: float,
    annual_rate: float,
    years: int
) -> dict:
    """Calculate monthly payment for a loan."""
    import time
    time.sleep(0.5)  # Simulate processing
    
    monthly_rate = (annual_rate / 100) / 12
    num_payments = years * 12
    
    if monthly_rate == 0:
        monthly_payment = loan_amount / num_payments
    else:
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
    
    return {
        "status": "success",
        "report": f"Monthly payment: ${monthly_payment:,.2f}"
    }


def calculate_monthly_savings(
    target_amount: float,
    years: int,
    annual_return: float = 5.0
) -> dict:
    """Calculate monthly savings needed to reach a goal."""
    import time
    time.sleep(0.5)  # Simulate calculation
    
    months = years * 12
    monthly_rate = (annual_return / 100) / 12
    
    if monthly_rate == 0:
        monthly_savings = target_amount / months
    else:
        monthly_savings = target_amount / (((1 + monthly_rate)**months - 1) / monthly_rate)
    
    return {
        "status": "success",
        "report": f"Save ${monthly_savings:,.2f} per month"
    }


parallel_finance_agent = Agent(
    name="parallel_finance_assistant",
    model="gemini-2.5-flash",  # Supports parallel tool calling!
    description="Financial assistant with parallel computation",
    instruction=(
        "You are a financial planning assistant. When users ask about multiple "
        "scenarios or calculations, call ALL necessary tools at once to be efficient. "
        "For example, if comparing investment options, call the calculation tool for "
        "EACH option simultaneously."
    ),
    tools=[
        calculate_compound_interest,
        calculate_loan_payment,
        calculate_monthly_savings
    ]
)
```

### Try This Prompt (Triggers Parallel Execution)

```
Compare these three investment options for me:
1. $10,000 at 5% for 10 years
2. $15,000 at 4% for 10 years  
3. $12,000 at 6% for 10 years
```

**What happens**:
1. Gemini recognizes it needs to call `calculate_compound_interest` THREE times
2. ADK receives THREE `FunctionCall` objects from Gemini
3. ADK executes all three **simultaneously** with `asyncio.gather()`
4. All results come back in ~0.5s instead of ~1.5s (sequential)
5. Gemini receives all results and generates comparative analysis

### Performance Comparison

**Sequential Execution** (if you did it manually):
```python
# ❌ Slow approach (not how ADK works)
result1 = calculate_compound_interest(10000, 5, 10)   # 0.5s
result2 = calculate_compound_interest(15000, 4, 10)   # 0.5s
result3 = calculate_compound_interest(12000, 6, 10)   # 0.5s
# Total: ~1.5 seconds
```

**Parallel Execution** (ADK automatic):
```python
# ✅ Fast - ADK does this for you!
results = await asyncio.gather(
    calculate_compound_interest(10000, 5, 10),
    calculate_compound_interest(15000, 4, 10),
    calculate_compound_interest(12000, 6, 10)
)
# Total: ~0.5 seconds (limited by slowest tool)
```

**Speedup**: 3x faster for 3 parallel tools!

### Example Output

```
User: Compare these three investment options for me:
1. $10,000 at 5% for 10 years
2. $15,000 at 4% for 10 years  
3. $12,000 at 6% for 10 years

Agent: Let me calculate all three options for you...

[Tool Calls - EXECUTED SIMULTANEOUSLY]:
- calculate_compound_interest(principal=10000, annual_rate=5, years=10)
- calculate_compound_interest(principal=15000, annual_rate=4, years=10)
- calculate_compound_interest(principal=12000, annual_rate=6, years=10)

Great question! Here's how your three investment options compare:

**Option 1**: $10,000 at 5% for 10 years
- Final amount: $16,470.09
- Interest earned: $6,470.09

**Option 2**: $15,000 at 4% for 10 years
- Final amount: $22,280.97
- Interest earned: $7,280.97

**Option 3**: $12,000 at 6% for 10 years
- Final amount: $21,791.23
- Interest earned: $9,791.23

Option 3 gives you the highest return ($9,791.23 in interest), even with a lower 
principal than Option 2. That extra 2% rate makes a big difference over 10 years!
```

### When Does Parallel Execution Happen?

Parallel execution occurs when:

✅ **Multiple tool calls in single turn** - Gemini decides to call 2+ tools at once
✅ **Tools are independent** - Results don't depend on each other
✅ **Model supports parallel calling** - Gemini 2.5-flash, 2.5-pro, 2.0-flash support this

**Does NOT happen when**:
❌ **Sequential dependencies** - Tool B needs result from Tool A
❌ **Single tool call** - Only one tool invoked
❌ **Manual sequential instructions** - You explicitly tell the model to do things step-by-step

### Optimizing for Parallel Execution

**✅ DO: Design independent tools**
```python
# Good - These can run in parallel
def get_weather(city: str): ...
def get_exchange_rate(currency: str): ...
def get_stock_price(symbol: str): ...

# User: "What's the weather in Tokyo, EUR/USD rate, and AAPL stock price?"
# → All 3 execute simultaneously!
```

**❌ DON'T: Create dependencies**
```python
# Bad - These create a dependency chain
def search_database(query: str) -> dict:
    """Find database records."""
    return {"status": "success", "record_id": "123"}

def fetch_record_details(record_id: str) -> dict:
    """Get full details for a record (needs record_id first)."""
    return {"status": "success", "details": "..."}

# These MUST run sequentially - can't parallelize
```

### Verification: Check the Events Tab

Open the Dev UI Events tab after sending a multi-tool query. Look for:

```
[FunctionCall] calculate_compound_interest(principal=10000, ...)
[FunctionCall] calculate_compound_interest(principal=15000, ...)  
[FunctionCall] calculate_compound_interest(principal=12000, ...)

[FunctionResponse] result for 10000
[FunctionResponse] result for 15000
[FunctionResponse] result for 12000
```

Notice all `FunctionCall` events are emitted **before** any `FunctionResponse` - proof they executed in parallel!

### Source Code Reference

The parallel execution implementation is in `google/adk/flows/llm_flows/functions.py`:

```python
# Simplified version of what ADK does internally
async def execute_function_calls(calls: list[FunctionCall]):
    """Execute multiple function calls in parallel."""
    
    tasks = [execute_single_function(call) for call in calls]
    results = await asyncio.gather(*tasks)
    
    return results
```

**You get this for free** - just define your tools normally!

### Performance Tips

1. **For I/O-bound tools** (API calls, database queries):
   - Parallel execution provides **massive speedup** (3-10x)
   - Each tool waits on network, not CPU

2. **For CPU-bound tools** (calculations, data processing):
   - Parallel execution still helps if tools are independent
   - Python GIL limits pure CPU parallelism, but asyncio scheduling still improves responsiveness

3. **Mixed workloads** (some I/O, some CPU):
   - I/O tools finish during CPU tool execution
   - Best of both worlds!

### Advanced Example: Multi-Source Data Aggregation

```python
def get_market_data(symbol: str) -> dict:
    """Fetch stock market data (simulated API call)."""
    import time
    time.sleep(1.0)  # Simulate API latency
    return {
        "status": "success",
        "report": f"{symbol}: $150.32 (+2.1%)"
    }

def get_company_news(symbol: str) -> dict:
    """Fetch latest news for a company (simulated API call)."""
    import time
    time.sleep(1.2)  # Simulate API latency
    return {
        "status": "success",
        "report": f"{symbol} announces Q4 earnings beat"
    }

def get_analyst_ratings(symbol: str) -> dict:
    """Fetch analyst ratings (simulated API call)."""
    import time
    time.sleep(0.8)  # Simulate API latency
    return {
        "status": "success",
        "report": f"{symbol}: 12 Buy, 3 Hold, 1 Sell"
    }

aggregator_agent = Agent(
    name="market_aggregator",
    model="gemini-2.5-flash",
    description="Aggregates market data from multiple sources",
    instruction="When asked about a stock, fetch ALL relevant data simultaneously.",
    tools=[get_market_data, get_company_news, get_analyst_ratings]
)

# Query: "Tell me everything about AAPL"
# → All 3 tools execute in parallel (~1.2s total vs ~3s sequential)
```

### Sample Reference

Check out `contributing/samples/parallel_functions/agent.py` for a complete working example of parallel tool execution.

## Key Takeaways

✅ **Tools are just Python functions** - No special classes needed, just regular functions!

✅ **LLM decides when to use tools** - You don't manually trigger them. The LLM reads the docstring and decides.

✅ **Parallel execution is automatic** - When multiple tools are called, ADK runs them simultaneously via `asyncio.gather()`

✅ **Type hints are critical** - They tell the LLM what data types to use for parameters

✅ **Docstrings = tool descriptions** - Write clear docstrings explaining WHEN and HOW to use the tool

✅ **Return dicts with status** - Use `{"status": "success", "report": "..."}` pattern for clarity

✅ **Default parameters = optional** - Functions with defaults can be called without those params

✅ **Events tab is your debugging friend** - See every tool call, parameter, and response (and verify parallel execution!)

✅ **Tools extend LLM capabilities** - Use tools for calculations, API calls, database queries - anything the LLM can't do alone

✅ **Design for independence** - Tools that don't depend on each other enable parallel execution and better performance

## Best Practices

**DO:**
- Write descriptive function names (`calculate_compound_interest` not `calc_int`)
- Include comprehensive docstrings
- Use type hints for all parameters
- Return structured dictionaries
- Handle errors gracefully
- Keep tools focused (one function = one task)

**DON'T:**
- Use generic names (`process_data`, `do_stuff`)
- Rely on `*args` or `**kwargs` for LLM-facing parameters (they're ignored!)
- Return complex objects (stick to dicts, strings, numbers)
- Make tools that do too many things
- Forget to handle error cases

## Common Issues

**Problem**: "Tool not being called"
- **Check**: Is your docstring clear about WHEN to use the tool?
- **Check**: Does the function name match what the user is asking for?
- **Tip**: Look at Events tab - did Gemini even consider the tool?

**Problem**: "Wrong parameters passed"
- **Check**: Are your type hints correct?
- **Check**: Is your docstring describing parameters clearly?
- **Try**: Add examples in the docstring

**Problem**: "Tool returns error"
- **Check**: Add try/except blocks to catch errors
- **Return**: Error status dict instead of raising exceptions

## What We Built

You now have a finance assistant agent that:
- Performs accurate compound interest calculations
- Computes loan payments
- Plans savings goals
- Explains results in human-friendly language

And you learned HOW ADK tools work under the hood!

## Next Steps

🚀 **Tutorial 03: OpenAPI Tools** - Connect to real web APIs (weather, stock prices, news, etc.)

📖 **Further Reading**:
- [Function Tools Documentation](https://google.github.io/adk-docs/tools/function-tools/)
- [Tool Performance (Parallel Execution)](https://google.github.io/adk-docs/tools/performance/)
- [Built-in Tools](https://google.github.io/adk-docs/tools/built-in-tools/)

## Exercises (Try On Your Own!)

1. **Add a budgeting tool** - Calculate if someone can afford something based on income
2. **Add debt payoff tool** - Calculate how long to pay off credit card debt
3. **Add retirement savings tool** - Estimate retirement savings needs
4. **Handle more edge cases** - What if someone enters negative numbers?

## Complete Code Reference

**finance_assistant/__init__.py**
```python
from . import agent
```

**finance_assistant/.env**
```bash
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your-api-key-here
```

**finance_assistant/agent.py**
```python
# See Step 3 above for the complete agent.py code
```

Congratulations! Your agent now has superpowers! 🚀💰
