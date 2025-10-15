"""Data analysis ADK agent with pandas tools and AG-UI integration.

This agent provides data analysis functionality with tools for CSV data loading,
statistical analysis, and chart generation. It integrates with Vite+React
frontends via the AG-UI protocol.
"""

import os
import io
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# AG-UI ADK integration imports
try:
    from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
except ImportError:
    raise ImportError(
        "ag_ui_adk not found. Install with: pip install ag-ui-adk"
    )

# Google ADK imports
from google.adk.agents import Agent

# Data analysis imports
try:
    import pandas as pd
except ImportError:
    raise ImportError(
        "pandas not found. Install with: pip install pandas"
    )

# Load environment variables
load_dotenv()


# ============================================================================
# In-memory data storage (use Redis/DB in production)
# ============================================================================

uploaded_data: Dict[str, pd.DataFrame] = {}


# ============================================================================
# Tool Definitions
# ============================================================================


def load_csv_data(file_name: str, csv_content: str) -> Dict[str, Any]:
    """
    Load CSV data into memory for analysis.

    Args:
        file_name: Name of the CSV file
        csv_content: CSV file content as string

    Returns:
        Dict with status, report, dataset info, and preview
    """
    try:
        # Parse CSV
        df = pd.read_csv(io.StringIO(csv_content))

        # Store in memory
        uploaded_data[file_name] = df

        # Return summary
        return {
            "status": "success",
            "report": (
                f"Successfully loaded {file_name} with {len(df)} rows "
                f"and {len(df.columns)} columns."
            ),
            "file_name": file_name,
            "rows": len(df),
            "columns": list(df.columns),
            "preview": df.head(5).to_dict(orient='records'),
            "dtypes": df.dtypes.astype(str).to_dict()
        }
    except Exception as e:
        return {
            "status": "error",
            "report": f"Failed to load {file_name}: {str(e)}",
            "error": str(e)
        }


def analyze_data(
    file_name: str,
    analysis_type: str,
    columns: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Perform statistical analysis on loaded dataset.

    Args:
        file_name: Name of dataset to analyze
        analysis_type: Type of analysis ('summary', 'correlation', 'trend')
        columns: Optional list of specific columns to analyze

    Returns:
        Dict with status, report, and analysis results
    """
    if file_name not in uploaded_data:
        return {
            "status": "error",
            "report": f"Dataset {file_name} not found. Please load it first.",
            "error": f"Dataset {file_name} not found"
        }

    try:
        df = uploaded_data[file_name]

        # Filter columns if specified
        if columns:
            missing_cols = [col for col in columns if col not in df.columns]
            if missing_cols:
                return {
                    "status": "error",
                    "report": f"Columns not found: {', '.join(missing_cols)}",
                    "error": f"Invalid columns: {missing_cols}"
                }
            df = df[columns]

        results = {
            "status": "success",
            "file_name": file_name,
            "analysis_type": analysis_type
        }

        if analysis_type == "summary":
            # Statistical summary
            numeric_df = df.select_dtypes(include=['number'])
            results["report"] = (
                f"Generated statistical summary for {len(numeric_df.columns)} "
                f"numeric columns in {file_name}."
            )
            results["data"] = {
                "describe": numeric_df.describe().to_dict(),
                "missing": df.isnull().sum().to_dict(),
                "unique": df.nunique().to_dict()
            }

        elif analysis_type == "correlation":
            # Correlation analysis
            numeric_df = df.select_dtypes(include=['number'])
            if len(numeric_df.columns) < 2:
                return {
                    "status": "error",
                    "report": "Need at least 2 numeric columns for correlation analysis",
                    "error": "Insufficient numeric columns"
                }
            results["report"] = (
                f"Calculated correlations for {len(numeric_df.columns)} "
                f"numeric columns in {file_name}."
            )
            results["data"] = numeric_df.corr().to_dict()

        elif analysis_type == "trend":
            # Time series trend analysis
            numeric_df = df.select_dtypes(include=['number'])
            if len(numeric_df) < 2:
                return {
                    "status": "error",
                    "report": "Need at least 2 rows for trend analysis",
                    "error": "Insufficient data points"
                }
            
            # Calculate mean trends
            means = numeric_df.mean().to_dict()
            first_sum = numeric_df.iloc[0].sum()
            last_sum = numeric_df.iloc[-1].sum()
            trend_direction = "upward" if last_sum > first_sum else "downward"
            
            results["report"] = (
                f"Analyzed trends in {file_name}. Overall trend is {trend_direction}."
            )
            results["data"] = {
                "mean": means,
                "trend": trend_direction,
                "first_row_sum": float(first_sum),
                "last_row_sum": float(last_sum)
            }

        else:
            return {
                "status": "error",
                "report": f"Unknown analysis type: {analysis_type}",
                "error": f"Invalid analysis_type: {analysis_type}"
            }

        return results

    except Exception as e:
        return {
            "status": "error",
            "report": f"Analysis failed: {str(e)}",
            "error": str(e)
        }


def create_chart(
    file_name: str,
    chart_type: str,
    x_column: str,
    y_column: str
) -> Dict[str, Any]:
    """
    Generate chart data for visualization.

    Args:
        file_name: Name of dataset
        chart_type: Type of chart ('line', 'bar', 'scatter')
        x_column: Column for x-axis
        y_column: Column for y-axis

    Returns:
        Dict with status, report, and chart configuration
    """
    if file_name not in uploaded_data:
        return {
            "status": "error",
            "report": f"Dataset {file_name} not found. Please load it first.",
            "error": f"Dataset {file_name} not found"
        }

    try:
        df = uploaded_data[file_name]

        # Validate columns
        if x_column not in df.columns:
            return {
                "status": "error",
                "report": f"Column {x_column} not found in dataset",
                "error": f"Invalid x_column: {x_column}"
            }
        if y_column not in df.columns:
            return {
                "status": "error",
                "report": f"Column {y_column} not found in dataset",
                "error": f"Invalid y_column: {y_column}"
            }

        # Validate chart type
        valid_types = ['line', 'bar', 'scatter']
        if chart_type not in valid_types:
            return {
                "status": "error",
                "report": f"Invalid chart type. Use: {', '.join(valid_types)}",
                "error": f"Invalid chart_type: {chart_type}"
            }

        # Prepare chart data
        # Convert to simple types to ensure JSON serialization
        x_data = df[x_column].tolist()
        y_data = df[y_column].tolist()

        # Convert numpy types to Python types
        x_data = [str(x) for x in x_data]
        y_data = [float(y) if pd.notna(y) else 0 for y in y_data]

        chart_data = {
            "status": "success",
            "report": (
                f"Generated {chart_type} chart for {y_column} vs {x_column} "
                f"from {file_name} with {len(x_data)} data points."
            ),
            "chart_type": chart_type,
            "data": {
                "labels": x_data,
                "values": y_data
            },
            "options": {
                "x_label": x_column,
                "y_label": y_column,
                "title": f"{y_column} vs {x_column}"
            }
        }

        return chart_data

    except Exception as e:
        return {
            "status": "error",
            "report": f"Chart generation failed: {str(e)}",
            "error": str(e)
        }


# ============================================================================
# ADK Agent Configuration
# ============================================================================

# Create ADK agent with data analysis tools
adk_agent = Agent(
    name="data_analyst",
    model="gemini-2.0-flash-exp",
    instruction="""You are an expert data analysis assistant with expertise in statistical analysis and data visualization.

Your capabilities:
- Load CSV datasets using load_csv_data(file_name, csv_content)
- Perform statistical analysis using analyze_data(file_name, analysis_type, columns)
- Generate visualizations using create_chart(file_name, chart_type, x_column, y_column)

Analysis types available:
- "summary": Descriptive statistics, missing values, unique counts
- "correlation": Correlation matrix for numeric columns
- "trend": Time series trend analysis

Chart types available:
- "line": Line chart for trends over time
- "bar": Bar chart for categorical comparisons
- "scatter": Scatter plot for relationships

Guidelines:
1. Always start by loading data if not already loaded
2. Explain your analysis clearly with markdown formatting
3. Suggest relevant visualizations based on data type
4. Highlight key insights with **bold** text
5. Use statistical terms appropriately
6. When analyzing data, first understand the structure
7. Perform appropriate analysis (summary, correlation, or trend)
8. Generate visualizations when helpful
9. Provide actionable insights

Workflow:
1. Load the CSV data
2. Examine the data structure (columns, types, sample data)
3. Perform requested analysis or suggest appropriate analyses
4. Create visualizations if relevant
5. Summarize findings with clear insights

Be concise but thorough in your explanations. Use markdown tables for better readability.""",
    tools=[load_csv_data, analyze_data, create_chart]
)

# Export for testing
root_agent = adk_agent


# ============================================================================
# FastAPI Application Setup
# ============================================================================

app = FastAPI(
    title="Data Analysis Agent API",
    description="ADK agent for CSV data analysis with pandas and Chart.js visualization",
    version="1.0.0"
)

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:5174",  # Alternative Vite port
        "http://localhost:3000",  # Alternative frontend port
        "http://localhost:8080",  # Alternative frontend port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# CopilotKit Endpoint (Using AG-UI ADK)
# ============================================================================

# Wrap ADK agent with AG-UI middleware
ag_ui_agent = ADKAgent(
    adk_agent=adk_agent,
    app_name="data_analysis_dashboard",
    user_id="demo_user"
)

# Add CopilotKit info endpoint - Required for CopilotKit 1.10.x
@app.get("/api/copilotkit")
async def copilotkit_info():
    """
    CopilotKit info endpoint for agent discovery.
    Returns agent information in CopilotKit-expected format.
    """
    return {
        "agents": [
            {
                "name": "data_analyst",
                "description": "Expert data analysis assistant with CSV tools",
                "tools": ["load_csv_data", "analyze_data", "create_chart"]
            }
        ],
        "version": "1.0.0"
    }


# Add AG-UI ADK endpoint for CopilotKit
# This creates a /api/copilotkit endpoint that CopilotKit can connect to directly
add_adk_fastapi_endpoint(app, ag_ui_agent, path="/api/copilotkit")


# ============================================================================
# Additional API Endpoints
# ============================================================================

@app.get("/info")
def info() -> Dict[str, Any]:
    """
    CopilotKit info endpoint - provides agent capabilities.

    Returns:
        Dict with agent information
    """
    return {
        "agents": [
            {
                "name": "data_analyst",
                "description": "Expert data analysis assistant with CSV tools",
                "capabilities": ["data_analysis", "visualization", "statistics"]
            }
        ]
    }


@app.get("/health")
def health_check() -> Dict[str, Any]:
    """
    Health check endpoint.

    Returns:
        Dict with status, agent name, and loaded datasets
    """
    return {
        "status": "healthy",
        "agent": "data_analyst",
        "datasets_loaded": list(uploaded_data.keys()),
        "num_datasets": len(uploaded_data)
    }


@app.get("/datasets")
def list_datasets() -> Dict[str, Any]:
    """
    List all loaded datasets.

    Returns:
        Dict with loaded dataset names and their info
    """
    datasets_info = {}
    for name, df in uploaded_data.items():
        datasets_info[name] = {
            "rows": len(df),
            "columns": list(df.columns),
            "dtypes": df.dtypes.astype(str).to_dict()
        }
    
    return {
        "status": "success",
        "datasets": datasets_info,
        "count": len(uploaded_data)
    }


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "agent:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
