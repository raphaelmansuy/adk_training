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

## Key Takeaways

✅ **Tools are just Python functions** - No special classes needed, just regular functions!

✅ **LLM decides when to use tools** - You don't manually trigger them. The LLM reads the docstring and decides.

✅ **Type hints are critical** - They tell the LLM what data types to use for parameters

✅ **Docstrings = tool descriptions** - Write clear docstrings explaining WHEN and HOW to use the tool

✅ **Return dicts with status** - Use `{"status": "success", "report": "..."}` pattern for clarity

✅ **Default parameters = optional** - Functions with defaults can be called without those params

✅ **Events tab is your debugging friend** - See every tool call, parameter, and response

✅ **Tools extend LLM capabilities** - Use tools for calculations, API calls, database queries - anything the LLM can't do alone

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
