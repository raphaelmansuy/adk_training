"""Tool Use Quality Evaluation Agent.

This agent demonstrates different tool usage patterns for evaluation:
- Good tool sequencing
- Bad tool sequencing
- Tool efficiency
- Error recovery
"""

from typing import Any
from google.adk.agents import Agent


def analyze_data(dataset: str) -> dict[str, Any]:
    """Analyze a dataset (simulated).

    Args:
        dataset: Name of the dataset to analyze

    Returns:
        Dict with analysis results and metadata
    """
    if not dataset:
        return {
            "status": "error",
            "report": "Dataset name required",
        }

    return {
        "status": "success",
        "report": f"Analyzed dataset: {dataset}",
        "data": {
            "records": 1000,
            "columns": 15,
            "types": ["numeric", "categorical", "date"],
        },
    }


def extract_features(data: dict[str, Any]) -> dict[str, Any]:
    """Extract features from analysis data.

    Args:
        data: Input data dictionary from analysis

    Returns:
        Dict with extracted features
    """
    if not data:
        return {
            "status": "error",
            "report": "Data required for feature extraction",
        }

    return {
        "status": "success",
        "report": "Extracted features from data",
        "data": {
            "features": ["mean", "median", "std_dev", "correlation"],
            "count": 4,
        },
    }


def validate_quality(features: dict[str, Any]) -> dict[str, Any]:
    """Validate feature quality (simulated).

    Args:
        features: Features to validate

    Returns:
        Dict with validation results
    """
    if not features:
        return {
            "status": "error",
            "report": "Features required for validation",
        }

    return {
        "status": "success",
        "report": "Feature quality validation passed",
        "data": {
            "quality_score": 0.92,
            "valid_features": 4,
            "issues": [],
        },
    }


def apply_model(features: dict[str, Any], model: str) -> dict[str, Any]:
    """Apply ML model to features.

    Args:
        features: Features to apply model to
        model: Model name to apply

    Returns:
        Dict with model application results
    """
    if not features or not model:
        return {
            "status": "error",
            "report": "Features and model name required",
        }

    return {
        "status": "success",
        "report": f"Applied {model} model to features",
        "data": {
            "model": model,
            "predictions": 1000,
            "accuracy": 0.87,
        },
    }


# Define the agent for evaluating tool usage
root_agent = Agent(
    name="tool_use_evaluator",
    model="gemini-2.0-flash",
    description="Agent for demonstrating tool use quality evaluation",
    instruction="""
You are a data analysis assistant demonstrating proper tool sequencing.

When asked to analyze data:
1. FIRST: Analyze the dataset
2. THEN: Extract features from the analysis
3. THEN: Validate feature quality
4. FINALLY: Apply ML model

This sequence demonstrates:
- Proper tool ordering (prerequisites first)
- Tool dependencies (each step builds on previous)
- Complete pipelines (all steps included)
- Error handling (proper validation)

Do NOT skip steps or call tools out of order.
Always follow: analyze → extract → validate → apply
""",
    tools=[
        analyze_data,
        extract_features,
        validate_quality,
        apply_model,
    ],
    output_key="analysis_result",
)
