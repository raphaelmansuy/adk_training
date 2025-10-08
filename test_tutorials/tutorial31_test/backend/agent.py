"""Tutorial 31 - Data Analysis Agent with Pandas Tools."""

import io
import os
from typing import Any, Dict, List

import pandas as pd
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.adk.agents import LlmAgent
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint

# In-memory storage for uploaded datasets
uploaded_data: Dict[str, pd.DataFrame] = {}


def load_csv_data(file_name: str, csv_content: str) -> Dict[str, Any]:
    """
    Load CSV data into memory for analysis.
    
    Args:
        file_name: Name of the CSV file
        csv_content: CSV file content as string
        
    Returns:
        Dict with dataset info and preview
    """
    try:
        # Parse CSV
        df = pd.read_csv(io.StringIO(csv_content))
        
        # Store in memory
        uploaded_data[file_name] = df
        
        # Return summary
        return {
            "status": "success",
            "file_name": file_name,
            "rows": len(df),
            "columns": list(df.columns),
            "preview": df.head(5).to_dict(orient='records'),
            "dtypes": df.dtypes.astype(str).to_dict()
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def analyze_data(
    file_name: str,
    analysis_type: str,
    columns: List[str] = None
) -> Dict[str, Any]:
    """
    Perform analysis on loaded dataset.
    
    Args:
        file_name: Name of dataset to analyze
        analysis_type: Type of analysis (summary, correlation, trend)
        columns: Optional list of columns to analyze
        
    Returns:
        Dict with analysis results
    """
    if file_name not in uploaded_data:
        return {"status": "error", "error": f"Dataset {file_name} not found"}
    
    df = uploaded_data[file_name]
    
    if columns:
        try:
            df = df[columns]
        except KeyError as e:
            return {"status": "error", "error": f"Column not found: {str(e)}"}
    
    results = {
        "status": "success",
        "file_name": file_name,
        "analysis_type": analysis_type
    }
    
    if analysis_type == "summary":
        results["data"] = {
            "describe": df.describe().to_dict(),
            "missing": df.isnull().sum().to_dict(),
            "unique": df.nunique().to_dict()
        }
    
    elif analysis_type == "correlation":
        # Only numeric columns
        numeric_df = df.select_dtypes(include=['number'])
        if numeric_df.empty:
            return {"status": "error", "error": "No numeric columns found"}
        results["data"] = numeric_df.corr().to_dict()
    
    elif analysis_type == "trend":
        # Time series analysis
        if len(df) > 0:
            numeric_df = df.select_dtypes(include=['number'])
            if numeric_df.empty:
                return {"status": "error", "error": "No numeric columns for trend analysis"}
            results["data"] = {
                "mean": numeric_df.mean().to_dict(),
                "trend": "upward" if numeric_df.iloc[-1].sum() > numeric_df.iloc[0].sum() else "downward"
            }
    else:
        return {"status": "error", "error": f"Unknown analysis type: {analysis_type}"}
    
    return results


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
        chart_type: Type of chart (line, bar, scatter)
        x_column: Column for x-axis
        y_column: Column for y-axis
        
    Returns:
        Dict with chart configuration
    """
    if file_name not in uploaded_data:
        return {"status": "error", "error": f"Dataset {file_name} not found"}
    
    df = uploaded_data[file_name]
    
    if x_column not in df.columns or y_column not in df.columns:
        return {"status": "error", "error": "Invalid columns"}
    
    # Prepare chart data
    chart_data = {
        "status": "success",
        "chart_type": chart_type,
        "data": {
            "labels": df[x_column].tolist(),
            "values": df[y_column].tolist()
        },
        "options": {
            "x_label": x_column,
            "y_label": y_column,
            "title": f"{y_column} vs {x_column}"
        }
    }
    
    return chart_data


# Create ADK agent using the new API
adk_agent = LlmAgent(
    name="data_analyst",
    model="gemini-2.0-flash-exp",
    instruction="""You are a data analysis expert assistant.

Your capabilities:
- Load and analyze CSV datasets using load_csv_data()
- Perform statistical analysis using analyze_data()
- Generate insights and trends
- Create visualizations using create_chart()

Guidelines:
- Always start by loading data if not already loaded
- Explain your analysis clearly with markdown formatting
- Suggest relevant visualizations
- Highlight key insights with **bold** text
- Use statistical terms appropriately

When analyzing data:
1. Understand the dataset structure first
2. Perform appropriate analysis (summary, correlation, or trend)
3. Generate visualizations if helpful
4. Provide actionable insights

Be concise but thorough in your explanations.""",
    tools=[load_csv_data, analyze_data, create_chart]
)

# Wrap ADK agent with AG-UI middleware
agent = ADKAgent(
    adk_agent=adk_agent,
    app_name="data_analysis_app",
    user_id="demo_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True
)

# Create FastAPI app
app = FastAPI(title="Tutorial 31 Data Analysis Agent")

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add ADK endpoint for CopilotKit
add_adk_fastapi_endpoint(app, agent, path="/api/copilotkit")


# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agent": "data_analyst",
        "tutorial": "31",
        "datasets_loaded": list(uploaded_data.keys())
    }


# Clear datasets endpoint (useful for testing)
@app.post("/clear")
def clear_datasets():
    """Clear all loaded datasets."""
    uploaded_data.clear()
    return {
        "status": "success",
        "message": "All datasets cleared"
    }


# Run with: uvicorn agent:app --reload --port 8000
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "agent:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
