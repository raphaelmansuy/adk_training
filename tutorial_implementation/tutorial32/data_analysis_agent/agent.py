"""
Data Analysis Agent with ADK
Provides tools for analyzing datasets
"""

from typing import Any, Dict
from google.adk.agents import Agent


def analyze_column(column_name: str, analysis_type: str = "summary", data_context: str = "") -> Dict[str, Any]:
    """
    Analyze a specific column in the dataset.

    Args:
        column_name: Name of the column to analyze
        analysis_type: Type of analysis (summary, distribution, top_values)
        data_context: JSON context about available data

    Returns:
        Dict with status, report, and analysis results
    """
    try:
        if not column_name or not isinstance(column_name, str):
            return {
                "status": "error",
                "report": "Invalid column name provided",
                "error": "column_name must be a non-empty string",
            }

        return {
            "status": "success",
            "report": f"Analysis of {analysis_type} for column '{column_name}' would be performed",
            "analysis_type": analysis_type,
            "column_name": column_name,
            "note": "In the Streamlit app, actual data analysis is performed with real datasets",
        }
    except Exception as e:
        return {
            "status": "error",
            "report": f"Error analyzing column: {str(e)}",
            "error": str(e),
        }


def calculate_correlation(column1: str, column2: str = "", data_context: str = "") -> Dict[str, Any]:
    """
    Calculate correlation between two numeric columns.

    Args:
        column1: First column name
        column2: Second column name
        data_context: JSON context about available data

    Returns:
        Dict with status, report, and correlation data
    """
    try:
        if not column1 or not column2:
            return {
                "status": "error",
                "report": "Both column names must be provided",
                "error": "Missing column names",
            }

        return {
            "status": "success",
            "report": f"Correlation calculation between '{column1}' and '{column2}' configured",
            "column1": column1,
            "column2": column2,
            "note": "In the Streamlit app, actual correlation is computed with real data",
        }
    except Exception as e:
        return {
            "status": "error",
            "report": f"Error calculating correlation: {str(e)}",
            "error": str(e),
        }


def filter_data(
    column_name: str, operator: str = "equals", value: str = "", data_context: str = ""
) -> Dict[str, Any]:
    """
    Filter dataset by condition.

    Args:
        column_name: Column to filter on
        operator: Comparison operator (equals, greater_than, less_than, contains)
        value: Value to compare against
        data_context: JSON context about available data

    Returns:
        Dict with status, report, and filtered data summary
    """
    try:
        if not column_name or not operator or not value:
            return {
                "status": "error",
                "report": "Column name, operator, and value must be provided",
                "error": "Missing filter parameters",
            }

        return {
            "status": "success",
            "report": f"Filter configured: {column_name} {operator} {value}",
            "column_name": column_name,
            "operator": operator,
            "value": value,
            "note": "In the Streamlit app, actual filtering is performed with real data",
        }
    except Exception as e:
        return {
            "status": "error",
            "report": f"Error filtering data: {str(e)}",
            "error": str(e),
        }


def get_dataset_summary(data_context: str = "") -> Dict[str, Any]:
    """
    Get summary information about the current dataset.

    Args:
        data_context: JSON context about available data

    Returns:
        Dict with status, report, and dataset summary
    """
    try:
        return {
            "status": "success",
            "report": "Dataset summary tool configured for analysis",
            "available_tools": ["analyze_column", "calculate_correlation", "filter_data"],
            "note": "In the Streamlit app, actual dataset info is provided in real-time",
        }
    except Exception as e:
        return {
            "status": "error",
            "report": f"Error getting dataset summary: {str(e)}",
            "error": str(e),
        }


# Create the root agent
root_agent = Agent(
    name="data_analysis_agent",
    model="gemini-2.0-flash",
    description="Intelligent data analysis assistant for exploring and understanding datasets",
    instruction="""You are an expert data analyst assistant. Your role is to help users understand and analyze their datasets.

When users ask about their data:
1. Understand what analysis they need
2. Ask clarifying questions if needed
3. Provide clear, actionable insights
4. Suggest interesting patterns or correlations
5. Recommend next steps for further analysis

Guidelines:
- Be concise but thorough
- Use clear language and examples
- Reference actual data characteristics
- Provide context for findings
- Suggest visualizations when relevant

Available tools:
- analyze_column: Analyze specific columns for insights
- calculate_correlation: Find relationships between variables
- filter_data: Explore data subsets
- get_dataset_summary: Get overview of available data

When the user provides data context, use it to make informed suggestions about what analyses would be most valuable.""",
    tools=[analyze_column, calculate_correlation, filter_data, get_dataset_summary],
)
