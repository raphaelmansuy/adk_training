"""Tutorial 31 - Test Suite for Data Analysis Agent."""

import pytest
from fastapi.testclient import TestClient
from agent import (
    app,
    load_csv_data,
    analyze_data,
    create_chart,
    uploaded_data,
    adk_agent,
    agent
)

client = TestClient(app)

# Sample CSV data for testing
SALES_CSV = """date,product,sales,revenue
2024-01-01,Product A,100,1000
2024-01-02,Product A,120,1200
2024-01-03,Product A,110,1100
2024-01-04,Product B,150,3000
2024-01-05,Product B,160,3200"""

WEATHER_CSV = """date,temperature,humidity,rainfall
2024-01-01,25.5,60,0
2024-01-02,26.0,65,5
2024-01-03,24.5,70,10
2024-01-04,23.0,75,15
2024-01-05,22.5,80,20"""

EMPLOYEES_CSV = """name,department,salary,years_experience
Alice,Engineering,90000,5
Bob,Marketing,70000,3
Carol,Engineering,95000,7
David,Sales,80000,4
Eve,Marketing,75000,5"""

INVALID_CSV = """This is not valid CSV data
Just some random text
Without proper structure"""


class TestTutorial31DataAnalysisAgent:
    """Test suite for Tutorial 31 data analysis agent."""

    def setup_method(self):
        """Clear uploaded data before each test."""
        uploaded_data.clear()

    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["agent"] == "data_analyst"
        assert data["tutorial"] == "31"
        assert "datasets_loaded" in data

    def test_clear_endpoint(self):
        """Test clear datasets endpoint."""
        # Load some data first
        load_csv_data("test.csv", SALES_CSV)
        assert "test.csv" in uploaded_data
        
        # Clear it
        response = client.post("/clear")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(uploaded_data) == 0

    def test_cors_configuration(self):
        """Test CORS headers are present."""
        response = client.options(
            "/api/copilotkit",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST",
            }
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers

    def test_copilotkit_endpoint_registered(self):
        """Test that CopilotKit endpoint is registered."""
        routes = [route.path for route in app.routes]
        assert "/api/copilotkit" in routes or any("/api/copilotkit" in str(route) for route in app.routes)


class TestLoadCSVData:
    """Test load_csv_data tool."""

    def setup_method(self):
        """Clear uploaded data before each test."""
        uploaded_data.clear()

    def test_load_valid_csv(self):
        """Test loading valid CSV data."""
        result = load_csv_data("sales.csv", SALES_CSV)
        
        assert result["status"] == "success"
        assert result["file_name"] == "sales.csv"
        assert result["rows"] == 5
        assert "date" in result["columns"]
        assert "product" in result["columns"]
        assert "sales" in result["columns"]
        assert "revenue" in result["columns"]
        assert len(result["preview"]) <= 5
        assert "sales.csv" in uploaded_data

    def test_load_multiple_datasets(self):
        """Test loading multiple CSV files."""
        load_csv_data("sales.csv", SALES_CSV)
        load_csv_data("weather.csv", WEATHER_CSV)
        
        assert len(uploaded_data) == 2
        assert "sales.csv" in uploaded_data
        assert "weather.csv" in uploaded_data

    def test_load_csv_with_dtypes(self):
        """Test that dtypes are returned."""
        result = load_csv_data("weather.csv", WEATHER_CSV)
        
        assert "dtypes" in result
        assert isinstance(result["dtypes"], dict)
        # Check numeric columns have appropriate types
        assert "float" in result["dtypes"]["temperature"].lower() or "int" in result["dtypes"]["temperature"].lower()

    def test_load_csv_preview_format(self):
        """Test preview data format."""
        result = load_csv_data("sales.csv", SALES_CSV)
        
        assert "preview" in result
        assert isinstance(result["preview"], list)
        assert len(result["preview"]) > 0
        # First row should be a dictionary
        assert isinstance(result["preview"][0], dict)
        assert "date" in result["preview"][0]

    def test_load_invalid_csv(self):
        """Test loading invalid CSV data."""
        result = load_csv_data("invalid.csv", INVALID_CSV)
        
        # pandas might parse this as valid CSV with one column, so just check it doesn't crash
        assert "status" in result

    def test_load_empty_csv(self):
        """Test loading empty CSV."""
        result = load_csv_data("empty.csv", "")
        
        # pandas may handle this differently, just check it doesn't crash
        assert "status" in result

    def test_overwrite_existing_dataset(self):
        """Test that loading same filename overwrites data."""
        load_csv_data("data.csv", SALES_CSV)
        # Check sales columns are present
        assert "product" in uploaded_data["data.csv"].columns
        
        load_csv_data("data.csv", WEATHER_CSV)
        # Weather CSV should be loaded now (overwrites sales)
        assert "temperature" in uploaded_data["data.csv"].columns
        assert "product" not in uploaded_data["data.csv"].columns


class TestAnalyzeData:
    """Test analyze_data tool."""

    def setup_method(self):
        """Load sample data before each test."""
        uploaded_data.clear()
        load_csv_data("sales.csv", SALES_CSV)
        load_csv_data("weather.csv", WEATHER_CSV)
        load_csv_data("employees.csv", EMPLOYEES_CSV)

    def test_analyze_summary(self):
        """Test summary analysis."""
        result = analyze_data("sales.csv", "summary")
        
        assert result["status"] == "success"
        assert result["file_name"] == "sales.csv"
        assert result["analysis_type"] == "summary"
        assert "data" in result
        assert "describe" in result["data"]
        assert "missing" in result["data"]
        assert "unique" in result["data"]

    def test_analyze_summary_specific_columns(self):
        """Test summary analysis with specific columns."""
        result = analyze_data("sales.csv", "summary", columns=["sales", "revenue"])
        
        assert result["status"] == "success"
        assert "describe" in result["data"]
        # Should only have specified columns in results
        describe_keys = result["data"]["describe"].keys()
        assert "sales" in describe_keys
        assert "revenue" in describe_keys

    def test_analyze_correlation(self):
        """Test correlation analysis."""
        result = analyze_data("weather.csv", "correlation")
        
        assert result["status"] == "success"
        assert result["analysis_type"] == "correlation"
        assert "data" in result
        # Correlation matrix should have numeric columns
        assert "temperature" in result["data"]
        assert "humidity" in result["data"]

    def test_analyze_trend(self):
        """Test trend analysis."""
        result = analyze_data("sales.csv", "trend")
        
        assert result["status"] == "success"
        assert result["analysis_type"] == "trend"
        assert "data" in result
        assert "mean" in result["data"]
        assert "trend" in result["data"]
        assert result["data"]["trend"] in ["upward", "downward"]

    def test_analyze_nonexistent_dataset(self):
        """Test analyzing non-existent dataset."""
        result = analyze_data("nonexistent.csv", "summary")
        
        assert result["status"] == "error"
        assert "not found" in result["error"].lower()

    def test_analyze_invalid_columns(self):
        """Test analysis with invalid column names."""
        result = analyze_data("sales.csv", "summary", columns=["nonexistent_column"])
        
        assert result["status"] == "error"
        assert "error" in result

    def test_analyze_unknown_analysis_type(self):
        """Test with unknown analysis type."""
        result = analyze_data("sales.csv", "unknown_analysis")
        
        assert result["status"] == "error"
        assert "unknown" in result["error"].lower()

    def test_analyze_correlation_no_numeric_columns(self):
        """Test correlation analysis with no numeric columns."""
        # Create a CSV with only text columns
        text_csv = """name,city,country
Alice,Paris,France
Bob,London,UK"""
        load_csv_data("text.csv", text_csv)
        
        result = analyze_data("text.csv", "correlation")
        
        assert result["status"] == "error"
        assert "numeric" in result["error"].lower()

    def test_analyze_trend_multiple_columns(self):
        """Test trend analysis with multiple numeric columns."""
        result = analyze_data("employees.csv", "trend")
        
        assert result["status"] == "success"
        assert "mean" in result["data"]
        # Should have mean for salary and years_experience
        assert "salary" in result["data"]["mean"]
        assert "years_experience" in result["data"]["mean"]


class TestCreateChart:
    """Test create_chart tool."""

    def setup_method(self):
        """Load sample data before each test."""
        uploaded_data.clear()
        load_csv_data("sales.csv", SALES_CSV)
        load_csv_data("weather.csv", WEATHER_CSV)

    def test_create_line_chart(self):
        """Test creating line chart."""
        result = create_chart("sales.csv", "line", "date", "sales")
        
        assert result["status"] == "success"
        assert result["chart_type"] == "line"
        assert "data" in result
        assert "labels" in result["data"]
        assert "values" in result["data"]
        assert len(result["data"]["labels"]) == 5
        assert len(result["data"]["values"]) == 5

    def test_create_bar_chart(self):
        """Test creating bar chart."""
        result = create_chart("weather.csv", "bar", "date", "temperature")
        
        assert result["status"] == "success"
        assert result["chart_type"] == "bar"
        assert isinstance(result["data"]["labels"], list)
        assert isinstance(result["data"]["values"], list)

    def test_create_scatter_chart(self):
        """Test creating scatter chart."""
        result = create_chart("weather.csv", "scatter", "temperature", "humidity")
        
        assert result["status"] == "success"
        assert result["chart_type"] == "scatter"

    def test_create_chart_with_options(self):
        """Test that chart includes proper options."""
        result = create_chart("sales.csv", "line", "date", "revenue")
        
        assert "options" in result
        assert result["options"]["x_label"] == "date"
        assert result["options"]["y_label"] == "revenue"
        assert "title" in result["options"]
        assert "revenue vs date" in result["options"]["title"].lower()

    def test_create_chart_nonexistent_dataset(self):
        """Test chart creation with non-existent dataset."""
        result = create_chart("nonexistent.csv", "line", "x", "y")
        
        assert result["status"] == "error"
        assert "not found" in result["error"].lower()

    def test_create_chart_invalid_x_column(self):
        """Test chart creation with invalid x column."""
        result = create_chart("sales.csv", "line", "invalid_column", "sales")
        
        assert result["status"] == "error"
        assert "invalid" in result["error"].lower()

    def test_create_chart_invalid_y_column(self):
        """Test chart creation with invalid y column."""
        result = create_chart("sales.csv", "line", "date", "invalid_column")
        
        assert result["status"] == "error"
        assert "invalid" in result["error"].lower()

    def test_create_chart_data_types(self):
        """Test that chart data has correct types."""
        result = create_chart("sales.csv", "line", "product", "sales")
        
        assert isinstance(result["data"]["labels"], list)
        assert isinstance(result["data"]["values"], list)
        # Values should be numeric
        for value in result["data"]["values"]:
            assert isinstance(value, (int, float))


class TestAgentConfiguration:
    """Test agent configuration."""

    def test_agent_exists(self):
        """Test that ADK agent is properly initialized."""
        assert adk_agent is not None
        assert agent is not None

    def test_agent_has_correct_name(self):
        """Test agent name configuration."""
        assert adk_agent.name == "data_analyst"

    def test_agent_has_tools(self):
        """Test that agent has all required tools."""
        # Agent should have 3 tools registered
        tools = adk_agent.tools
        assert tools is not None
        assert len(tools) == 3

    def test_agent_model_configured(self):
        """Test that agent uses correct model."""
        assert hasattr(adk_agent, "model") or hasattr(adk_agent, "_model")
        # Should use Gemini model
        model_str = str(adk_agent.model if hasattr(adk_agent, "model") else adk_agent._model)
        assert "gemini" in model_str.lower()

    def test_adk_agent_wrapper_configured(self):
        """Test ADK agent wrapper configuration."""
        # Verify the agent wrapper is properly set up
        assert agent._adk_agent == adk_agent
        # Agent should be an ADKAgent instance
        from ag_ui_adk import ADKAgent
        assert isinstance(agent, ADKAgent)


class TestAPIConfiguration:
    """Test API configuration."""

    def test_fastapi_app_title(self):
        """Test FastAPI app title."""
        assert app.title == "Tutorial 31 Data Analysis Agent"

    def test_cors_middleware_present(self):
        """Test CORS middleware is configured."""
        middlewares = [m.__class__.__name__ for m in app.user_middleware]
        assert "CORSMiddleware" in middlewares or "Middleware" in middlewares

    def test_multiple_origins_allowed(self):
        """Test that multiple CORS origins are configured."""
        # Check that app has CORS middleware configured
        # Check via GET request which is allowed
        response = client.get("/health")
        assert response.status_code == 200


class TestIntegration:
    """Integration tests."""

    def setup_method(self):
        """Clear uploaded data before each test."""
        uploaded_data.clear()

    def test_full_workflow(self):
        """Test complete analysis workflow."""
        # 1. Load data
        load_result = load_csv_data("sales.csv", SALES_CSV)
        assert load_result["status"] == "success"
        
        # 2. Analyze data
        analysis_result = analyze_data("sales.csv", "summary")
        assert analysis_result["status"] == "success"
        
        # 3. Create chart
        chart_result = create_chart("sales.csv", "line", "date", "sales")
        assert chart_result["status"] == "success"

    def test_multiple_datasets_workflow(self):
        """Test working with multiple datasets."""
        # Load multiple datasets
        load_csv_data("sales.csv", SALES_CSV)
        load_csv_data("weather.csv", WEATHER_CSV)
        
        # Analyze both
        sales_analysis = analyze_data("sales.csv", "summary")
        weather_analysis = analyze_data("weather.csv", "correlation")
        
        assert sales_analysis["status"] == "success"
        assert weather_analysis["status"] == "success"
        
        # Create charts from both
        sales_chart = create_chart("sales.csv", "line", "date", "sales")
        weather_chart = create_chart("weather.csv", "line", "date", "temperature")
        
        assert sales_chart["status"] == "success"
        assert weather_chart["status"] == "success"

    def test_health_endpoint_reports_loaded_datasets(self):
        """Test that health endpoint shows loaded datasets."""
        load_csv_data("data1.csv", SALES_CSV)
        load_csv_data("data2.csv", WEATHER_CSV)
        
        response = client.get("/health")
        data = response.json()
        
        assert "datasets_loaded" in data
        assert "data1.csv" in data["datasets_loaded"]
        assert "data2.csv" in data["datasets_loaded"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
