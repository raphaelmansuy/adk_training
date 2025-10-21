#!/usr/bin/env python3
"""
Real evaluation of tool use quality using RUBRIC_BASED_TOOL_USE_QUALITY_V1.

This script performs actual evaluations of agent tool usage against custom rubrics.
It demonstrates how to:
1. Create test cases with expected tool sequences
2. Configure evaluation with rubric-based tool use quality metric
3. Run evaluations and interpret results
4. Handle good vs bad tool sequencing patterns

Usage:
    python evaluate_tool_use.py

Requirements:
    - GOOGLE_API_KEY environment variable set
    - google-genai >= 1.16.0
    - Test cases defined in evalset.json
"""

import asyncio
import json
import os
from pathlib import Path

from google.adk.evaluation.agent_evaluator import AgentEvaluator


async def create_evalset_file():
    """Create evalset.json with test cases for evaluation."""
    evalset_path = Path(__file__).parent / "tool_use_quality.evalset.json"
    config_path = Path(__file__).parent / "test_config.json"

    # Define the evalset with good and bad tool use sequences
    evalset_data = {
        "eval_set_id": "tool_use_quality_evaluation",
        "name": "Tool Use Quality Evaluation",
        "description": "Evaluation of agent tool sequencing and quality",
        "eval_cases": [
            {
                "eval_id": "good_sequence_complete_pipeline",
                "conversation": [
                    {
                        "invocation_id": "inv-001",
                        "user_content": {
                            "parts": [
                                {
                                    "text": "Analyze the sales dataset and apply a prediction model"
                                }
                            ],
                            "role": "user",
                        },
                        "final_response": {
                            "parts": [
                                {
                                    "text": "I've analyzed the sales dataset, extracted features, validated quality, and applied the prediction model. The model achieved 87% accuracy on the features."
                                }
                            ],
                            "role": "model",
                        },
                        "intermediate_data": {
                            "tool_uses": [
                                {
                                    "id": "call-001",
                                    "name": "analyze_data",
                                    "args": {"dataset": "sales_dataset"},
                                },
                                {
                                    "id": "call-002",
                                    "name": "extract_features",
                                    "args": {"data": {"type": "analysis_result"}},
                                },
                                {
                                    "id": "call-003",
                                    "name": "validate_quality",
                                    "args": {"features": {"type": "features"}},
                                },
                                {
                                    "id": "call-004",
                                    "name": "apply_model",
                                    "args": {
                                        "features": {"type": "validated_features"},
                                        "model": "random_forest",
                                    },
                                },
                            ],
                            "intermediate_responses": [],
                        },
                    }
                ],
                "session_input": {
                    "app_name": "tool_use_evaluator",
                    "user_id": "test_user",
                    "state": {},
                },
            },
            {
                "eval_id": "bad_sequence_skipped_validation",
                "conversation": [
                    {
                        "invocation_id": "inv-002",
                        "user_content": {
                            "parts": [
                                {
                                    "text": "Process the customer dataset for modeling"
                                }
                            ],
                            "role": "user",
                        },
                        "final_response": {
                            "parts": [
                                {
                                    "text": "I've extracted features and applied the model."
                                }
                            ],
                            "role": "model",
                        },
                        "intermediate_data": {
                            "tool_uses": [
                                {
                                    "id": "call-101",
                                    "name": "extract_features",
                                    "args": {"data": {"type": "raw_data"}},
                                },
                                {
                                    "id": "call-102",
                                    "name": "apply_model",
                                    "args": {
                                        "features": {"type": "features"},
                                        "model": "linear_regression",
                                    },
                                },
                            ],
                            "intermediate_responses": [],
                        },
                    }
                ],
                "session_input": {
                    "app_name": "tool_use_evaluator",
                    "user_id": "test_user",
                    "state": {},
                },
            },
            {
                "eval_id": "good_sequence_proper_analysis",
                "conversation": [
                    {
                        "invocation_id": "inv-003",
                        "user_content": {
                            "parts": [
                                {
                                    "text": "Analyze and prepare the dataset for machine learning"
                                }
                            ],
                            "role": "user",
                        },
                        "final_response": {
                            "parts": [
                                {
                                    "text": "Dataset analyzed and prepared with validated features ready for modeling."
                                }
                            ],
                            "role": "model",
                        },
                        "intermediate_data": {
                            "tool_uses": [
                                {
                                    "id": "call-201",
                                    "name": "analyze_data",
                                    "args": {"dataset": "customer_data"},
                                },
                                {
                                    "id": "call-202",
                                    "name": "extract_features",
                                    "args": {"data": {"type": "analysis"}},
                                },
                                {
                                    "id": "call-203",
                                    "name": "validate_quality",
                                    "args": {"features": {"type": "extracted_features"}},
                                },
                            ],
                            "intermediate_responses": [],
                        },
                    }
                ],
                "session_input": {
                    "app_name": "tool_use_evaluator",
                    "user_id": "test_user",
                    "state": {},
                },
            },
        ],
    }

    # Define the evaluation config with rubric-based tool use quality metric
    eval_config = {
        "criteria": {
            "rubric_based_tool_use_quality_v1": {
                "threshold": 0.7,
                "judge_model_options": {
                    "judge_model": "gemini-2.5-flash",
                    "num_samples": 3,
                },
                "rubrics": [
                    {
                        "rubric_id": "proper_tool_order",
                        "rubric_content": {
                            "text_property": "The agent calls analyze_data BEFORE extract_features. This respects tool dependencies."
                        },
                    },
                    {
                        "rubric_id": "complete_pipeline",
                        "rubric_content": {
                            "text_property": "For a complete analysis, the agent should call: analyze → extract → validate → apply (all 4 steps)"
                        },
                    },
                    {
                        "rubric_id": "validation_before_model",
                        "rubric_content": {
                            "text_property": "The agent validates feature quality before applying the model"
                        },
                    },
                    {
                        "rubric_id": "no_tool_failures",
                        "rubric_content": {
                            "text_property": "All tool calls succeed with proper parameters (no errors or missing args)"
                        },
                    },
                ],
            }
        }
    }

    # Write evalset to file
    with open(evalset_path, "w") as f:
        json.dump(evalset_data, f, indent=2)

    # Write config to file
    with open(config_path, "w") as f:
        json.dump(eval_config, f, indent=2)

    return evalset_path


async def run_evaluation(evalset_path: Path):
    """Run evaluation using RUBRIC_BASED_TOOL_USE_QUALITY_V1 metric.

    Args:
        evalset_path: Path to the evalset.json file
    """
    print("\n" + "=" * 80)
    print("REAL EVALUATION: RUBRIC BASED TOOL USE QUALITY V1")
    print("=" * 80 + "\n")

    # Rubrics are already defined in test_config.json
    rubrics = [
        ("proper_tool_order", "The agent calls analyze_data BEFORE extract_features"),
        ("complete_pipeline", "For complete analysis: analyze → extract → validate → apply"),
        ("validation_before_model", "Agent validates feature quality before modeling"),
        ("no_tool_failures", "All tool calls succeed with proper parameters"),
    ]

    print("📋 EVALUATION CONFIGURATION")
    print("-" * 80)
    print("Threshold: 0.7")
    print("Judge Model: gemini-2.5-flash")
    print(f"Rubrics: {len(rubrics)}")

    for rubric_id, rubric_desc in rubrics:
        print(f"  • {rubric_id}: {rubric_desc[:55]}...")

    print("\n🔍 RUNNING EVALUATION")
    print("-" * 80)

    try:
        # Run the evaluation
        results = await AgentEvaluator.evaluate(
            agent_module="tool_use_evaluator",
            eval_dataset_file_path_or_dir=str(evalset_path),
        )

        print("✅ Evaluation completed successfully!")
        print("\n📊 EVALUATION RESULTS")
        print("-" * 80)
        print(json.dumps(results, indent=2, default=str))

        # Interpret results
        print("\n🧠 RESULT INTERPRETATION")
        print("-" * 80)
        print(
            """
Evaluation Scores Explained:
- Score 1.0: Perfect tool sequencing (all rubrics satisfied)
- Score 0.8-0.99: Excellent, 1-2 minor issues
- Score 0.7-0.79: Good, acceptable but needs improvement
- Score 0.6-0.69: Acceptable with significant issues
- Score <0.6: Poor, fundamental problems with tool sequencing

What each rubric evaluates:
1. proper_tool_order: Are dependencies respected? (analyze before extract)
2. complete_pipeline: Are all necessary steps included?
3. validation_before_model: Is quality validated before modeling?
4. no_tool_failures: Do all tool calls execute successfully?
        """
        )

    except Exception as e:
        error_msg = str(e)
        if "Expected" in error_msg and "got" in error_msg:
            # This is a scoring failure, which actually means evaluation worked!
            print("⚠️  Evaluation ran but test cases failed scoring threshold:")
            print(f"   {error_msg}\n")
            print("This means the evaluation framework is working correctly!")
            print("The test agent didn't match expected tool sequences.")
            print("In a real scenario, you would:\n")
            print("1. Review the expected vs actual tool calls above")
            print("2. Adjust agent instructions to match the expected behavior")
            print("3. Re-run the evaluation to see if scores improve")
        else:
            print(f"❌ Evaluation failed: {e}")
            print("\nNote: Ensure GOOGLE_API_KEY is set:")
            print("  export GOOGLE_API_KEY=your_key")


def show_test_case_details():
    """Show details about the test cases."""
    print("\n📝 TEST CASES SUMMARY")
    print("-" * 80)

    test_cases = [
        {
            "name": "good_sequence_complete_pipeline",
            "description": "Complete 4-step pipeline (analyze → extract → validate → apply)",
            "expected_score": "0.95-1.0 (excellent)",
            "why": "All steps included in correct order, all rubrics satisfied",
        },
        {
            "name": "bad_sequence_skipped_validation",
            "description": "Missing steps (extract → apply, no analyze or validate)",
            "expected_score": "0.25-0.4 (poor)",
            "why": "Skips critical steps, violates proper_tool_order and validation_before_model rubrics",
        },
        {
            "name": "good_sequence_proper_analysis",
            "description": "Good analysis pipeline (analyze → extract → validate)",
            "expected_score": "0.8-0.9 (good)",
            "why": "Proper order and important steps, but doesn't apply model (acceptable for analysis-only tasks)",
        },
    ]

    for i, case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {case['name']}")
        print(f"  Description: {case['description']}")
        print(f"  Expected Score: {case['expected_score']}")
        print(f"  Reasoning: {case['why']}")


async def main():
    """Main evaluation workflow."""
    # Check API key
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("⚠️  WARNING: GOOGLE_API_KEY not set")
        print("    For real evaluation, set: export GOOGLE_API_KEY=your_key")
        print("    Continuing with demo mode...\n")

    # Show test case details
    show_test_case_details()

    # Create evalset file
    print("\n📁 Creating test evalset file...")
    evalset_path = await create_evalset_file()
    print(f"   ✓ Created: {evalset_path}")

    # Run evaluation
    await run_evaluation(evalset_path)

    print("\n" + "=" * 80)
    print("EVALUATION COMPLETE")
    print("=" * 80 + "\n")
    print("💡 Key Insights:")
    print("""
The RUBRIC_BASED_TOOL_USE_QUALITY_V1 metric evaluates agent tool sequencing
by having an LLM judge assess the tool calls against your custom rubrics.

Key Benefits:
• Catches tool dependency violations early
• Ensures agents follow prescribed workflows
• Detects missing or reordered steps
• Flexible rubric definition for your specific needs

Next Steps:
1. Define rubrics for your specific workflows
2. Create test cases with expected and actual tool sequences
3. Run evaluations in your CI/CD pipeline
4. Use results to identify agent behavior issues
5. Iterate on agent instructions to improve scores
    """
    )


if __name__ == "__main__":
    asyncio.run(main())

