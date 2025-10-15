"""Test data analysis agent configuration and functionality."""

import os

# Set a mock API key for testing if not present
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "test_api_key_for_testing"


class TestAgentConfiguration:
    """Test agent configuration and setup."""

    def test_agent_imports(self):
        """Test that agent imports correctly."""
        from agent import agent, root_agent, app
        
        assert agent is not None
        assert root_agent is not None
        assert app is not None

    def test_root_agent_properties(self):
        """Test that root_agent has correct properties."""
        from agent import root_agent
        
        assert hasattr(root_agent, 'name')
        assert root_agent.name == "data_analyst"
        assert hasattr(root_agent, 'model')
        assert hasattr(root_agent, 'instruction')
        assert hasattr(root_agent, 'tools')

    def test_agent_has_tools(self):
        """Test that agent has the required tools."""
        from agent import root_agent
        
        # Should have 3 tools: load_csv_data, analyze_data, create_chart
        assert len(root_agent.tools) == 3
        
        tool_names = [tool.__name__ for tool in root_agent.tools]
        assert "load_csv_data" in tool_names
        assert "analyze_data" in tool_names
        assert "create_chart" in tool_names

    def test_fastapi_app_configuration(self):
        """Test that FastAPI app is configured correctly."""
        from agent import app
        
        assert app.title == "Data Analysis Agent API"
        assert "version" in app.__dict__ or hasattr(app, "version")


class TestLoadCSVData:
    """Test load_csv_data tool."""

    def test_load_csv_data_success(self):
        """Test successful CSV data loading."""
        from agent.agent import load_csv_data
        
        csv_content = "name,age,score\nAlice,30,95\nBob,25,87\nCarol,35,92"
        result = load_csv_data("test.csv", csv_content)
        
        assert result["status"] == "success"
        assert result["file_name"] == "test.csv"
        assert result["rows"] == 3
        assert "name" in result["columns"]
        assert "age" in result["columns"]
        assert "score" in result["columns"]
        assert len(result["preview"]) <= 5

    def test_load_csv_data_with_headers(self):
        """Test CSV loading with headers."""
        from agent.agent import load_csv_data
        
        csv_content = "product,quantity,price\nApple,10,1.50\nBanana,20,0.75"
        result = load_csv_data("products.csv", csv_content)
        
        assert result["status"] == "success"
        assert result["columns"] == ["product", "quantity", "price"]
        assert result["rows"] == 2

    def test_load_csv_data_error_handling(self):
        """Test CSV loading with invalid data."""
        from agent.agent import load_csv_data
        
        # Invalid CSV content
        csv_content = "invalid csv format with no structure"
        result = load_csv_data("invalid.csv", csv_content)
        
        # Should handle error gracefully
        assert "status" in result

    def test_load_csv_data_empty(self):
        """Test CSV loading with empty content."""
        from agent.agent import load_csv_data
        
        csv_content = ""
        result = load_csv_data("empty.csv", csv_content)
        
        # Should handle error gracefully
        assert "status" in result


class TestAnalyzeData:
    """Test analyze_data tool."""

    def setup_method(self):
        """Set up test data before each test."""
        from agent.agent import load_csv_data
        
        # Load sample data
        csv_content = "name,age,score\nAlice,30,95\nBob,25,87\nCarol,35,92"
        load_csv_data("test.csv", csv_content)

    def test_analyze_data_summary(self):
        """Test summary analysis."""
        from agent.agent import analyze_data
        
        result = analyze_data("test.csv", "summary")
        
        assert result["status"] == "success"
        assert result["analysis_type"] == "summary"
        assert "data" in result
        assert "describe" in result["data"]
        assert "missing" in result["data"]
        assert "unique" in result["data"]

    def test_analyze_data_with_columns(self):
        """Test analysis with specific columns."""
        from agent.agent import analyze_data
        
        result = analyze_data("test.csv", "summary", columns=["age", "score"])
        
        assert result["status"] == "success"
        assert "data" in result

    def test_analyze_data_correlation(self):
        """Test correlation analysis."""
        from agent.agent import analyze_data
        
        result = analyze_data("test.csv", "correlation")
        
        assert result["status"] == "success"
        assert result["analysis_type"] == "correlation"
        assert "data" in result

    def test_analyze_data_trend(self):
        """Test trend analysis."""
        from agent.agent import analyze_data
        
        result = analyze_data("test.csv", "trend")
        
        assert result["status"] == "success"
        assert result["analysis_type"] == "trend"
        assert "data" in result
        assert "trend" in result["data"]
        assert result["data"]["trend"] in ["upward", "downward"]

    def test_analyze_data_not_found(self):
        """Test analysis with non-existent dataset."""
        from agent.agent import analyze_data
        
        result = analyze_data("nonexistent.csv", "summary")
        
        assert result["status"] == "error"
        assert "not found" in result["report"].lower()

    def test_analyze_data_invalid_columns(self):
        """Test analysis with invalid columns."""
        from agent.agent import analyze_data
        
        result = analyze_data("test.csv", "summary", columns=["invalid_col"])
        
        assert result["status"] == "error"

    def test_analyze_data_invalid_type(self):
        """Test analysis with invalid analysis type."""
        from agent.agent import analyze_data
        
        result = analyze_data("test.csv", "invalid_type")
        
        assert result["status"] == "error"


class TestCreateChart:
    """Test create_chart tool."""

    def setup_method(self):
        """Set up test data before each test."""
        from agent.agent import load_csv_data
        
        # Load sample data
        csv_content = "month,sales\nJan,100\nFeb,120\nMar,115"
        load_csv_data("sales.csv", csv_content)

    def test_create_chart_line(self):
        """Test line chart creation."""
        from agent.agent import create_chart
        
        result = create_chart("sales.csv", "line", "month", "sales")
        
        assert result["status"] == "success"
        assert result["chart_type"] == "line"
        assert "data" in result
        assert "labels" in result["data"]
        assert "values" in result["data"]
        assert len(result["data"]["labels"]) == 3
        assert len(result["data"]["values"]) == 3

    def test_create_chart_bar(self):
        """Test bar chart creation."""
        from agent.agent import create_chart
        
        result = create_chart("sales.csv", "bar", "month", "sales")
        
        assert result["status"] == "success"
        assert result["chart_type"] == "bar"

    def test_create_chart_scatter(self):
        """Test scatter chart creation."""
        from agent.agent import create_chart
        
        result = create_chart("sales.csv", "scatter", "month", "sales")
        
        assert result["status"] == "success"
        assert result["chart_type"] == "scatter"

    def test_create_chart_not_found(self):
        """Test chart creation with non-existent dataset."""
        from agent.agent import create_chart
        
        result = create_chart("nonexistent.csv", "line", "x", "y")
        
        assert result["status"] == "error"
        assert "not found" in result["report"].lower()

    def test_create_chart_invalid_column(self):
        """Test chart creation with invalid column."""
        from agent.agent import create_chart
        
        result = create_chart("sales.csv", "line", "invalid_col", "sales")
        
        assert result["status"] == "error"

    def test_create_chart_invalid_type(self):
        """Test chart creation with invalid chart type."""
        from agent.agent import create_chart
        
        result = create_chart("sales.csv", "invalid_type", "month", "sales")
        
        assert result["status"] == "error"

    def test_create_chart_options(self):
        """Test that chart has proper options."""
        from agent.agent import create_chart
        
        result = create_chart("sales.csv", "line", "month", "sales")
        
        assert result["status"] == "success"
        assert "options" in result
        assert "x_label" in result["options"]
        assert "y_label" in result["options"]
        assert "title" in result["options"]
        assert result["options"]["x_label"] == "month"
        assert result["options"]["y_label"] == "sales"


class TestFastAPIEndpoints:
    """Test FastAPI endpoints."""

    def test_health_endpoint(self):
        """Test health check endpoint."""
        from agent import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["agent"] == "data_analyst"
        assert "datasets_loaded" in data

    def test_datasets_endpoint(self):
        """Test datasets list endpoint."""
        from agent import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        response = client.get("/datasets")
        
        assert response.status_code == 200
        data = response.json()
        assert "datasets" in data
        assert "count" in data
