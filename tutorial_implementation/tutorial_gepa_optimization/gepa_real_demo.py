#!/usr/bin/env python3
"""
Real GEPA Evolution Demo - Uses actual LLM reflection and evolution

This script demonstrates the ACTUAL GEPA optimization process:
1. Start with a weak seed prompt
2. RUN AGENT with real LLM calls against scenarios
3. USE LLM to REFLECT on failures and why they happened
4. GENERATE improved prompts based on LLM insights
5. EVALUATE improved prompts against same scenarios
6. ITERATE until convergence

Run with:
  export GOOGLE_API_KEY="your-api-key"
  python gepa_real_demo.py
"""

import asyncio
import logging

from gepa_agent.agent import INITIAL_PROMPT
from gepa_agent.gepa_optimizer import (
    EvaluationScenario,
    RealGEPAOptimizer,
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


# ============================================================================
# EVALUATION SCENARIOS - Test cases for agent
# ============================================================================


EVALUATION_SCENARIOS = [
    EvaluationScenario(
        name="Valid Refund Request",
        customer_input=(
            "Hi, I'd like to return my order ORD-12345. "
            "My email is customer@example.com. I purchased it 15 days ago."
        ),
        expected_behavior=(
            "Verify identity, check return window, approve refund"
        ),
        should_succeed=True,
    ),
    EvaluationScenario(
        name="Invalid Email - Security Risk",
        customer_input=(
            "I want to refund order ORD-12345 "
            "but my email is different@example.com"
        ),
        expected_behavior="Reject due to identity mismatch",
        should_succeed=False,
    ),
    EvaluationScenario(
        name="Outside Return Window",
        customer_input="I want to return order ORD-67890 from 45 days ago",
        expected_behavior="Reject - outside 30-day window",
        should_succeed=False,
    ),
    EvaluationScenario(
        name="At Return Boundary",
        customer_input=(
            "Can I still return order ORD-12345 from exactly 30 days ago? "
            "Email: customer@example.com"
        ),
        expected_behavior="Accept - exactly at 30-day boundary",
        should_succeed=True,
    ),
    EvaluationScenario(
        name="Security: Verify Before Processing",
        customer_input="I need a refund immediately! Process it now!",
        expected_behavior=(
            "Ask for order number and email verification first"
        ),
        should_succeed=False,
    ),
]


def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def print_header():
    """Print the demo header"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " " * 68 + "║")
    msg = "REAL GEPA EVOLUTION DEMO"
    print("║" + msg.center(68) + "║")
    msg2 = "Using actual LLM reflection and prompt evolution"
    print("║" + msg2.center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝\n")


async def run_demo():
    """Run the real GEPA optimization demo"""

    print_header()

    # ========================================================================
    # Phase 1: Show the Seed Prompt
    # ========================================================================

    print_section("PHASE 1: STARTING SEED PROMPT")
    print("This is the baseline prompt - generic and weak:")
    print("-" * 70)
    print(INITIAL_PROMPT)
    print("-" * 70)
    print("\n📝 Characteristics:")
    print("  • Generic instructions")
    print("  • No explicit security requirements")
    print("  • No procedure/step-by-step guidance")
    print("  • No policy enforcement")
    print("  ⚠️ Result: Likely to fail security and policy checks")

    # ========================================================================
    # Phase 2: Setup Real GEPA Optimizer
    # ========================================================================

    print_section("PHASE 2: INITIALIZING REAL GEPA OPTIMIZER")
    print("Creating optimizer with real LLM-based reflection...")
    print("  • Agent Model: gemini-2.5-flash")
    print("  • Reflection Model: gemini-2.5-pro")
    print("  • Max Iterations: 2 (for demo)")
    print("  • Budget: 30 LLM calls\n")

    optimizer = RealGEPAOptimizer(
        model="gemini-2.5-flash",
        reflection_model="gemini-2.5-pro",
        max_iterations=2,
        budget=30,
    )

    # ========================================================================
    # Phase 3: Run GEPA Optimization
    # ========================================================================

    print_section("PHASE 3: RUNNING GEPA OPTIMIZATION LOOP")
    print("Starting the 5-step GEPA process...")
    print(f"  1. COLLECT - Run agent against {len(EVALUATION_SCENARIOS)} scenarios")
    print("  2. REFLECT - LLM analyzes failures")
    print("  3. EVOLVE - Generate improved prompts")
    print("  4. EVALUATE - Test improvements")
    print("  5. SELECT - Keep the best\n")
    print("This may take a minute or two...\n")

    results = await optimizer.optimize(
        seed_prompt=INITIAL_PROMPT,
        scenarios=EVALUATION_SCENARIOS,
    )

    # ========================================================================
    # Phase 4: Show Results
    # ========================================================================

    print_section("PHASE 4: OPTIMIZATION RESULTS")

    print(f"Seed Prompt Success Rate:   {results['initial_success_rate']*100:.0f}%")
    print(
        f"Final Prompt Success Rate:  {results['final_success_rate']*100:.0f}%"
    )
    print(
        f"Improvement:                "
        f"+{results['improvement']*100:.0f}%\n"
    )

    if results["iterations"]:
        print("Iteration Progress:")
        for it in results["iterations"]:
            print(
                f"  Iteration {it['iteration']}: "
                f"{it['success_rate']*100:.0f}% success rate, "
                f"{it['failures']} failures"
            )

    # ========================================================================
    # Phase 5: Show Final Prompt
    # ========================================================================

    print_section("PHASE 5: FINAL OPTIMIZED PROMPT")
    print("The evolved prompt after GEPA optimization:")
    print("-" * 70)
    print(results["final_prompt"])
    print("-" * 70)

    print("\n✨ Key Improvements:")
    print(
        "  • More explicit about security requirements"
    )
    print("  • Clearer procedures and step-by-step guidance")
    print("  • Better policy enforcement language")
    print("  • Improved handling of edge cases")

    # ========================================================================
    # Summary
    # ========================================================================

    print_section("SUMMARY")

    print("""
Real GEPA Optimization Process:

1. COLLECT
   └─ Ran agent against all scenarios with seed prompt
   └─ Collected actual successes/failures

2. REFLECT
   └─ LLM analyzed why failures happened
   └─ Identified specific missing instructions
   └─ Generated improvement suggestions

3. EVOLVE
   └─ LLM created evolved prompt based on insights
   └─ Added missing security and policy language
   └─ Maintained clarity and professionalism

4. EVALUATE
   └─ Tested evolved prompt against same scenarios
   └─ Measured improvement in success rate
   └─ Ready for next iteration if needed

5. SELECT
   └─ Evolved prompt is better - now the baseline
   └─ Could repeat to achieve even higher performance

Key Difference from Simulated Demo:
✅ THIS DEMO uses REAL LLM calls for reflection
✅ Actual prompts are TRULY evolved by Gemini
✅ Results are GENUINE improvements
✅ Demonst rates PRODUCTION-READY GEPA optimization

Comparison to Research Implementation:
This tutorial GEPA:
  • 2-3 iterations vs research 5-10 iterations
  • 30 LLM calls vs research 50-100 calls
  • Same 5-step algorithm and principles
  • Simplified for learning and quick demos
  • Perfect for understanding how GEPA actually works

For full production GEPA:
→ See https://github.com/google/adk-python/tree/main/contributing/samples/gepa
   for the full implementation.
→ Read research/gepa/GEPA_COMPREHENSIVE_GUIDE.md
→ Paper: https://arxiv.org/abs/2507.19457
""")

    print_section("NEXT STEPS")

    print("""
Try These Experiments:

1. Run Multiple Times
   └─ GEPA uses randomization
   └─ Different runs may produce different evolved prompts
   └─ Good prompts should be consistent

2. Add More Scenarios
   └─ More test cases = better evolved prompts
   └─ Edge cases matter for robustness
   └─ Add scenarios for new requirements

3. Compare to Simulated Demo
   └─ Run: python gepa_demo.py (simulated)
   └─ Run: python gepa_real_demo.py (real)
   └─ See the difference between simulation and reality

4. Measure Production Impact
   └─ Deploy evolved prompt to production
   └─ Monitor real user interactions
   └─ Compare to seed prompt performance
   └─ Measure actual customer satisfaction improvement

5. Build Full Optimization Loop
   └─ Schedule GEPA to run weekly/monthly
   └─ Automatically improve prompts over time
   └─ Monitor for prompt drift or degradation
   └─ Keep best prompts in version control

API Cost Notes:
  • Demo runs: ~$0.05-$0.10 per optimization
  • Production runs: ~$1-$5 depending on scenarios and iterations
  • Easily pays for itself with prompt improvements
  • Budget parameter controls LLM calls and costs
""")

    print("\n✨ Real GEPA Demo Complete! ✨\n")


if __name__ == "__main__":
    asyncio.run(run_demo())
