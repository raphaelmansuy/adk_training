"""
Parallel Execution Demo Agent - Tutorial 02: Function Tools

This agent demonstrates ADK's automatic parallel tool execution capabilities.
It uses the same financial calculation tools but is configured to showcase
how Gemini can execute multiple tools simultaneously for better performance.

Key differences from main agent:
- Optimized for parallel execution scenarios
- Uses Gemini 2.0-flash model for best parallel performance
- Includes examples of multi-tool queries
"""

from google.adk.agents import Agent

# Import the same tools from the main agent
from finance_assistant.agent import (
    calculate_compound_interest,
    calculate_loan_payment,
    calculate_monthly_savings
)


# Create the parallel execution demo agent
root_agent = Agent(
    name="parallel_finance_assistant",
    model="gemini-2.0-flash",  # Best model for parallel execution
    description="""
    A high-performance financial calculation assistant optimized for parallel execution.

    This agent can perform multiple financial calculations simultaneously, making it
    perfect for comparing investment options, analyzing multiple loan scenarios,
    or calculating savings goals for different timeframes.

    Key capabilities:
    - Parallel compound interest calculations for investment comparisons
    - Simultaneous loan payment analysis for different scenarios
    - Multi-goal savings planning with parallel computations

    Performance: Up to 3x faster for multiple independent calculations!

    Example queries that trigger parallel execution:
    - "Compare these investments: $10k at 5% for 10 years, $15k at 4% for 10 years, $12k at 6% for 10 years"
    - "Calculate payments for: 30-year mortgage at 4.5%, 20-year mortgage at 4.0%, 15-year mortgage at 3.5%"
    - "How much to save monthly for: $50k in 3 years, $100k in 5 years, $200k in 10 years"
    """,
    tools=[
        calculate_compound_interest,
        calculate_loan_payment,
        calculate_monthly_savings
    ]
)


def demo_parallel_execution():
    """
    Demonstrate parallel execution by running multiple calculations simultaneously.

    This function shows how the same tools can be called multiple times in parallel,
    which is exactly what ADK does automatically when Gemini requests multiple tools.
    """
    import asyncio
    import time

    async def run_parallel_calculations():
        """Run multiple financial calculations in parallel."""
        print("🚀 Parallel Execution Demo")
        print("=" * 50)

        # Start timing
        start_time = time.time()

        # Execute three compound interest calculations in parallel
        tasks = [
            asyncio.to_thread(calculate_compound_interest, 10000, 0.05, 10),  # $10k at 5% for 10 years
            asyncio.to_thread(calculate_compound_interest, 15000, 0.04, 10),  # $15k at 4% for 10 years
            asyncio.to_thread(calculate_compound_interest, 12000, 0.06, 10),  # $12k at 6% for 10 years
        ]

        # Wait for all calculations to complete
        results = await asyncio.gather(*tasks)

        # Calculate elapsed time
        elapsed = time.time() - start_time

        print(f"⚡ All calculations completed in {elapsed:.2f} seconds!")
        print()

        # Display results
        scenarios = [
            "$10,000 at 5% for 10 years",
            "$15,000 at 4% for 10 years",
            "$12,000 at 6% for 10 years"
        ]

        for i, (scenario, result) in enumerate(zip(scenarios, results), 1):
            print(f"Option {i}: {scenario}")
            if result['status'] == 'success':
                print(f"  Final Amount: ${result['final_amount']:,.0f}")
                print(f"  Interest Earned: ${result['interest_earned']:,.0f}")
            else:
                print(f"Error: {result.get('error', 'Unknown error')}")
            print()

        print("💡 Key Insights:")
        print("- All calculations completed simultaneously")
        print("- Results returned in parallel (not sequentially)")
        print("- Performance scales with independent calculations")
        print("- ADK handles the complexity automatically!")

    # Run the async demo
    asyncio.run(run_parallel_calculations())


if __name__ == "__main__":
    print("Parallel Finance Assistant Demo")
    print("=" * 50)
    print()
    print("This agent is optimized for parallel tool execution.")
    print("It can perform multiple financial calculations simultaneously.")
    print()
    print("Try these example queries:")
    print()
    print("1. Investment Comparison:")
    print('"Compare these three investment options: $10k at 5% for 10 years, $15k at 4% for 10 years, $12k at 6% for 10 years"')
    print()
    print("2. Loan Analysis:")
    print('"Calculate monthly payments for: $300k at 4.5% for 30 years, $300k at 4.0% for 20 years, $300k at 3.5% for 15 years"')
    print()
    print("3. Savings Goals:")
    print('"How much do I need to save monthly to reach: $50k in 3 years, $100k in 5 years, $200k in 10 years"')
    print()
    print("Starting parallel execution demo...")
    print()

    # Run the parallel demo
    demo_parallel_execution()

    print()
    print("Demo complete! 🎉")
    print()
    print("To start the ADK server with this parallel agent:")
    print("  make parallel-demo")
    print()
    print("To start the regular agent:")
    print("  make dev")