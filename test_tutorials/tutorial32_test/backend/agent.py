"""
Tutorial 32: Streamlit + ADK Data Analysis Agent
Pure Python integration - agent runs in-process (no HTTP server)

This module provides the data analysis agent that can be integrated
directly into Streamlit apps for analyzing CSV data.
"""

import os
import pandas as pd
from typing import Dict, Optional, List, Any
from google import genai
from google.genai.types import Tool, FunctionDeclaration, Content, Part, GenerateContentConfig
from google.adk.agents import Agent


# Tool Functions
def analyze_column(column_name: str, analysis_type: str, dataframe: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """
    Analyze a specific column in the dataset.
    
    Args:
        column_name: Name of the column to analyze
        analysis_type: Type of analysis (summary, distribution, top_values)
        dataframe: DataFrame to analyze (for testing)
        
    Returns:
        Dict with analysis results
    """
    if dataframe is None:
        return {"error": "No dataset provided"}
    
    if column_name not in dataframe.columns:
        return {"error": f"Column '{column_name}' not found"}
    
    column = dataframe[column_name]
    
    if analysis_type == "summary":
        if pd.api.types.is_numeric_dtype(column):
            return {
                "column": column_name,
                "type": "numeric",
                "count": int(column.count()),
                "mean": float(column.mean()),
                "median": float(column.median()),
                "std": float(column.std()),
                "min": float(column.min()),
                "max": float(column.max())
            }
        else:
            return {
                "column": column_name,
                "type": "categorical",
                "count": int(column.count()),
                "unique": int(column.nunique()),
                "most_common": str(column.mode()[0]) if len(column.mode()) > 0 else None
            }
    
    elif analysis_type == "distribution":
        if pd.api.types.is_numeric_dtype(column):
            q1 = column.quantile(0.25)
            q3 = column.quantile(0.75)
            iqr = q3 - q1
            outliers = ((column < (q1 - 1.5 * iqr)) | (column > (q3 + 1.5 * iqr))).sum()
            
            return {
                "column": column_name,
                "quartiles": {
                    "25%": float(q1),
                    "50%": float(column.quantile(0.50)),
                    "75%": float(q3)
                },
                "outliers": int(outliers)
            }
        else:
            value_counts = column.value_counts().head(10)
            return {
                "column": column_name,
                "distribution": {str(k): int(v) for k, v in value_counts.items()}
            }
    
    elif analysis_type == "top_values":
        value_counts = column.value_counts().head(10)
        return {
            "column": column_name,
            "top_values": [
                {"value": str(k), "count": int(v)}
                for k, v in value_counts.items()
            ]
        }
    
    return {"error": "Unknown analysis type"}


def calculate_correlation(column1: str, column2: str, dataframe: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """
    Calculate correlation between two numeric columns.
    
    Args:
        column1: First column name
        column2: Second column name
        dataframe: DataFrame to analyze (for testing)
        
    Returns:
        Dict with correlation coefficient
    """
    if dataframe is None:
        return {"error": "No dataset provided"}
    
    if column1 not in dataframe.columns or column2 not in dataframe.columns:
        return {"error": "Column not found"}
    
    col1 = dataframe[column1]
    col2 = dataframe[column2]
    
    if not (pd.api.types.is_numeric_dtype(col1) and pd.api.types.is_numeric_dtype(col2)):
        return {"error": "Both columns must be numeric"}
    
    correlation = col1.corr(col2)
    
    return {
        "column1": column1,
        "column2": column2,
        "correlation": float(correlation),
        "interpretation": (
            "strong positive" if correlation > 0.7 else
            "moderate positive" if correlation > 0.3 else
            "weak positive" if correlation > 0 else
            "weak negative" if correlation > -0.3 else
            "moderate negative" if correlation > -0.7 else
            "strong negative"
        )
    }


def filter_data(
    column_name: str,
    operator: str,
    value: str,
    dataframe: Optional[pd.DataFrame] = None
) -> Dict[str, Any]:
    """
    Filter dataset by condition.
    
    Args:
        column_name: Column to filter on
        operator: Comparison operator (equals, greater_than, less_than, contains)
        value: Value to compare against
        dataframe: DataFrame to filter (for testing)
        
    Returns:
        Dict with filtered data summary
    """
    if dataframe is None:
        return {"error": "No dataset provided"}
    
    if column_name not in dataframe.columns:
        return {"error": f"Column '{column_name}' not found"}
    
    column = dataframe[column_name]
    
    try:
        if operator == "equals":
            if pd.api.types.is_numeric_dtype(column):
                mask = column == float(value)
            else:
                mask = column == value
        elif operator == "greater_than":
            mask = column > float(value)
        elif operator == "less_than":
            mask = column < float(value)
        elif operator == "contains":
            mask = column.astype(str).str.contains(value, case=False, na=False)
        else:
            return {"error": "Unknown operator"}
        
        filtered_df = dataframe[mask]
        
        return {
            "original_rows": len(dataframe),
            "filtered_rows": len(filtered_df),
            "filter": f"{column_name} {operator} {value}",
            "sample": filtered_df.head(5).to_dict(orient="records")
        }
    
    except Exception as e:
        return {"error": f"Filter error: {str(e)}"}


def get_dataset_summary(dataframe: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
    """
    Get comprehensive summary of the dataset.
    
    Args:
        dataframe: DataFrame to summarize (for testing)
        
    Returns:
        Dict with dataset summary
    """
    if dataframe is None:
        return {"error": "No dataset provided"}
    
    numeric_cols = dataframe.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = dataframe.select_dtypes(exclude=['number']).columns.tolist()
    
    return {
        "shape": {
            "rows": dataframe.shape[0],
            "columns": dataframe.shape[1]
        },
        "columns": {
            "all": dataframe.columns.tolist(),
            "numeric": numeric_cols,
            "categorical": categorical_cols
        },
        "memory_usage_mb": float(dataframe.memory_usage(deep=True).sum() / 1024 / 1024),
        "missing_values": {
            col: int(dataframe[col].isna().sum())
            for col in dataframe.columns
            if dataframe[col].isna().sum() > 0
        }
    }


# Tool declarations for agent
TOOL_DECLARATIONS = [
    FunctionDeclaration(
        name="analyze_column",
        description="Analyze a specific column in the dataset (summary statistics, distribution, top values)",
        parameters={
            "type": "object",
            "properties": {
                "column_name": {
                    "type": "string",
                    "description": "Name of the column to analyze"
                },
                "analysis_type": {
                    "type": "string",
                    "description": "Type of analysis to perform",
                    "enum": ["summary", "distribution", "top_values"]
                }
            },
            "required": ["column_name", "analysis_type"]
        }
    ),
    FunctionDeclaration(
        name="calculate_correlation",
        description="Calculate correlation coefficient between two numeric columns",
        parameters={
            "type": "object",
            "properties": {
                "column1": {
                    "type": "string",
                    "description": "First column name"
                },
                "column2": {
                    "type": "string",
                    "description": "Second column name"
                }
            },
            "required": ["column1", "column2"]
        }
    ),
    FunctionDeclaration(
        name="filter_data",
        description="Filter the dataset by a condition and return summary",
        parameters={
            "type": "object",
            "properties": {
                "column_name": {
                    "type": "string",
                    "description": "Column to filter on"
                },
                "operator": {
                    "type": "string",
                    "description": "Comparison operator",
                    "enum": ["equals", "greater_than", "less_than", "contains"]
                },
                "value": {
                    "type": "string",
                    "description": "Value to compare against"
                }
            },
            "required": ["column_name", "operator", "value"]
        }
    ),
    FunctionDeclaration(
        name="get_dataset_summary",
        description="Get comprehensive summary of the entire dataset including shape, column types, and missing values",
        parameters={
            "type": "object",
            "properties": {}
        }
    )
]


# Tool mapping for execution
TOOLS = {
    "analyze_column": analyze_column,
    "calculate_correlation": calculate_correlation,
    "filter_data": filter_data,
    "get_dataset_summary": get_dataset_summary
}


class DataAnalysisAgent:
    """
    Data Analysis Agent for Streamlit integration using ADK.
    
    This agent provides data analysis capabilities through tool calling.
    It's designed to run in-process with Streamlit (no HTTP server needed).
    
    Uses google.adk.agents.Agent for direct, in-process agent execution.
    """
    
    def __init__(self, api_key: Optional[str] = None, dataframe: Optional[pd.DataFrame] = None):
        """
        Initialize the data analysis agent.
        
        Args:
            api_key: Google AI API key (uses env var if not provided)
            dataframe: Initial dataframe to analyze
        """
        key = api_key or os.getenv("GOOGLE_API_KEY")
        if not key:
            raise ValueError("GOOGLE_API_KEY not found")
        
        # Set API key in environment for ADK
        os.environ["GOOGLE_API_KEY"] = key
        
        self.dataframe = dataframe
        self.model = "gemini-2.0-flash-exp"
        
        # Create tools list for agent
        self.tools = self._create_tools()
        
        # Create the ADK agent
        self.agent = self._create_agent()
    
    def _create_tools(self) -> List:
        """Create tool functions that capture the dataframe."""
        tools = []
        
        # Wrap each tool function to inject dataframe
        def make_tool(func_name, original_func):
            def wrapped_func(**kwargs):
                kwargs['dataframe'] = self.dataframe
                return original_func(**kwargs)
            wrapped_func.__name__ = func_name
            wrapped_func.__doc__ = original_func.__doc__
            return wrapped_func
        
        # Create wrapped tools
        for tool_name, tool_func in TOOLS.items():
            tools.append(make_tool(tool_name, tool_func))
        
        return tools
    
    def _create_agent(self) -> Agent:
        """Create the agent with tools using ADK."""
        instruction = get_agent_instruction(self.dataframe)
        
        agent = Agent(
            model=self.model,
            name="data_analysis_agent",
            instruction=instruction,
            tools=self.tools
        )
        
        return agent
    
    def set_dataframe(self, df: pd.DataFrame):
        """
        Set the dataframe to analyze and recreate agent with new context.
        
        Args:
            df: Pandas DataFrame to analyze
        """
        self.dataframe = df
        # Recreate tools and agent with new dataframe context
        self.tools = self._create_tools()
        self.agent = self._create_agent()
    
    def analyze(self, query: str) -> str:
        """
        Analyze data based on user query.
        
        Args:
            query: User's question about the data
            
        Returns:
            Agent's response as string
        """
        if self.dataframe is None:
            return "No dataset loaded. Please provide a dataset first."
        
        try:
            # Call agent directly
            response = self.agent(query)
            
            # Extract text from response
            if hasattr(response, 'text'):
                return response.text
            elif isinstance(response, str):
                return response
            else:
                return str(response)
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_dataset_info(self) -> Dict[str, Any]:
        """Get information about the current dataset."""
        if self.dataframe is None:
            return {"error": "No dataset loaded"}
        
        return get_dataset_summary(self.dataframe)


def create_data_analysis_agent(api_key: Optional[str] = None, dataframe: Optional[pd.DataFrame] = None):
    """
    Create a data analysis agent configured with analysis tools.
    
    Args:
        api_key: Google AI API key (uses env var if not provided)
        dataframe: Initial dataframe to analyze
        
    Returns:
        DataAnalysisAgent instance
    """
    return DataAnalysisAgent(api_key=api_key, dataframe=dataframe)


def get_agent_instruction(dataframe: Optional[pd.DataFrame] = None) -> str:
    """
    Generate dynamic agent instruction based on current dataset.
    
    Args:
        dataframe: Current dataset (if any)
        
    Returns:
        Agent instruction string
    """
    base_instruction = """You are an expert data analyst assistant.

Your responsibilities:
- Help users understand and analyze their datasets
- Use tools to perform actual data analysis
- Provide clear, actionable insights
- Suggest interesting patterns and correlations
- Be concise but thorough

Guidelines:
- Always use tools when performing analysis
- Reference actual data from the dataset
- Use markdown formatting for better readability
- Provide context for statistical findings
- Suggest next analysis steps

When the user asks about their data:
1. Use analyze_column for column-specific insights
2. Use calculate_correlation to find relationships
3. Use filter_data to explore subsets
4. Use get_dataset_summary for overview
5. Explain findings in plain language
6. Suggest visualizations when relevant"""
    
    if dataframe is not None:
        numeric_cols = dataframe.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = dataframe.select_dtypes(exclude=['number']).columns.tolist()
        
        dataset_context = f"""

Current dataset context:
- Shape: {dataframe.shape[0]} rows × {dataframe.shape[1]} columns
- Numeric columns: {', '.join(numeric_cols) if numeric_cols else 'None'}
- Categorical columns: {', '.join(categorical_cols) if categorical_cols else 'None'}
- Columns: {', '.join(dataframe.columns.tolist())}"""
        
        return base_instruction + dataset_context
    
    return base_instruction + "\n\nNo dataset is currently loaded. Prompt the user to provide data."


# Agent configuration
AGENT_CONFIG = {
    "name": "data_analysis_agent",
    "model": "gemini-2.0-flash-exp",
    "description": "Expert data analyst that can analyze CSV data using pandas",
    "tools": TOOL_DECLARATIONS
}


if __name__ == "__main__":
    # Example usage
    import io
    
    # Create sample dataset
    csv_data = """product,price,sales,category
Widget A,29.99,150,Electronics
Widget B,49.99,230,Electronics
Gadget X,15.99,450,Accessories
Gadget Y,25.99,320,Accessories
Device 1,199.99,45,Electronics
Device 2,299.99,30,Electronics"""
    
    df = pd.read_csv(io.StringIO(csv_data))
    
    print("Dataset loaded:")
    print(df.head())
    print()
    
    # Test tools
    print("1. Analyze price column (summary):")
    result = analyze_column("price", "summary", df)
    print(result)
    print()
    
    print("2. Calculate correlation between price and sales:")
    result = calculate_correlation("price", "sales", df)
    print(result)
    print()
    
    print("3. Filter products with price > 50:")
    result = filter_data("price", "greater_than", "50", df)
    print(result)
    print()
    
    print("4. Get dataset summary:")
    result = get_dataset_summary(df)
    print(result)
