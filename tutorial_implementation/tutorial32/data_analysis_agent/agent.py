"""
Data Analysis Agent with ADK
Multi-agent system: analysis tools + visualization code execution
"""

from typing import Any, Dict
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

# Import visualization agent
from .visualization_agent import visualization_agent


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


# Create the analysis agent with traditional tools
analysis_agent = Agent(
    name="analysis_agent",
    model="gemini-2.0-flash",
    description="Data analysis and insights agent with statistical tools",
    instruction="""You are an expert data analyst. Your role is to help users understand their datasets 
and provide insights through analysis.

When users ask about data analysis:
1. Use available tools to analyze the data
2. Provide clear, actionable insights
3. Suggest patterns and correlations
4. Recommend visualizations when relevant
5. Guide users to deeper exploration

Available tools:
- analyze_column: Get statistics about specific columns
- calculate_correlation: Find relationships between variables
- filter_data: Explore data subsets and patterns
- get_dataset_summary: Get overview of the dataset""",
    tools=[analyze_column, calculate_correlation, filter_data, get_dataset_summary],
)


# Create the root coordinator agent using multi-agent pattern
# This solves the "one built-in tool per agent" limitation by separating concerns
root_agent = Agent(
    name="data_analysis_coordinator",
    model="gemini-2.0-flash",
    description="Intelligent data analysis assistant with visualization and analysis capabilities",
    instruction="""You are an expert data analyst and visualization specialist. Your role is to help users 
understand and explore their datasets through analysis and visualization.

When users interact with you:
1. For analysis questions (statistics, correlations, patterns):
   - Use the analysis_agent to compute insights
   - Explain the findings clearly
   
2. For visualization requests (plots, charts, graphs):
   - Immediately delegate to the visualization_agent
   - The visualization_agent will execute Python code to generate the chart
   - Do NOT ask clarifying questions about visualizations
   - Do NOT describe what you will do - just delegate
   
3. For general questions:
   - Provide context and recommendations
   - Suggest both analysis and visualization approaches

Guidelines:
- Be concise but thorough
- Use clear language and examples
- Reference actual data characteristics
- Provide context for findings
- When users ask about data, suggest both analyses and visualizations
- For visualization requests, ALWAYS immediately delegate to visualization_agent without questions

Remember: The visualization_agent specializes in creating publication-quality charts 
using Python code execution. The analysis_agent specializes in statistical insights. 
Do NOT ask clarifying questions about visualizations!""",
    tools=[
        AgentTool(agent=analysis_agent),
        AgentTool(agent=visualization_agent),
    ],
)
