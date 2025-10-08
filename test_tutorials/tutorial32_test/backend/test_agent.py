"""
Test Suite for Tutorial 32: Streamlit + ADK Data Analysis Agent
Tests the data analysis tools and agent configuration for pure Python integration.
"""

import pytest
import pandas as pd
import io
from agent import (
    analyze_column,
    calculate_correlation,
    filter_data,
    get_dataset_summary,
    create_data_analysis_agent,
    get_agent_instruction,
    DataAnalysisAgent,
    TOOL_DECLARATIONS,
    TOOLS,
    AGENT_CONFIG
)


# Test Fixtures
@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    csv_data = """product,price,sales,category,region
Widget A,29.99,150,Electronics,North
Widget B,49.99,230,Electronics,South
Gadget X,15.99,450,Accessories,East
Gadget Y,25.99,320,Accessories,West
Device 1,199.99,45,Electronics,North
Device 2,299.99,30,Electronics,South
Tool A,35.00,280,Hardware,North
Tool B,42.50,195,Hardware,East"""
    
    return pd.read_csv(io.StringIO(csv_data))


@pytest.fixture
def large_dataframe():
    """Create a larger DataFrame with missing values."""
    import numpy as np
    
    data = {
        'id': range(1, 101),
        'value': np.random.rand(100) * 100,
        'category': [f'Cat{i%5}' for i in range(100)],
        'status': ['active' if i % 3 == 0 else 'inactive' if i % 3 == 1 else None for i in range(100)]
    }
    return pd.DataFrame(data)


# Test analyze_column function
class TestAnalyzeColumn:
    """Test the analyze_column tool."""
    
    def test_numeric_summary(self, sample_dataframe):
        """Test summary analysis of numeric column."""
        result = analyze_column("price", "summary", sample_dataframe)
        
        assert "column" in result
        assert result["column"] == "price"
        assert result["type"] == "numeric"
        assert "mean" in result
        assert "median" in result
        assert "std" in result
        assert "min" in result
        assert "max" in result
        assert result["count"] == 8
        assert result["min"] == 15.99
        assert result["max"] == 299.99
    
    def test_categorical_summary(self, sample_dataframe):
        """Test summary analysis of categorical column."""
        result = analyze_column("category", "summary", sample_dataframe)
        
        assert result["column"] == "category"
        assert result["type"] == "categorical"
        assert result["count"] == 8
        assert result["unique"] == 3
        assert result["most_common"] in ["Electronics", "Accessories", "Hardware"]
    
    def test_numeric_distribution(self, sample_dataframe):
        """Test distribution analysis of numeric column."""
        result = analyze_column("sales", "distribution", sample_dataframe)
        
        assert result["column"] == "sales"
        assert "quartiles" in result
        assert "25%" in result["quartiles"]
        assert "50%" in result["quartiles"]
        assert "75%" in result["quartiles"]
        assert "outliers" in result
        assert isinstance(result["outliers"], int)
    
    def test_categorical_distribution(self, sample_dataframe):
        """Test distribution analysis of categorical column."""
        result = analyze_column("category", "distribution", sample_dataframe)
        
        assert result["column"] == "category"
        assert "distribution" in result
        assert isinstance(result["distribution"], dict)
        assert len(result["distribution"]) <= 10  # Top 10
    
    def test_top_values(self, sample_dataframe):
        """Test top values analysis."""
        result = analyze_column("category", "top_values", sample_dataframe)
        
        assert result["column"] == "category"
        assert "top_values" in result
        assert isinstance(result["top_values"], list)
        assert len(result["top_values"]) <= 10
        
        # Check structure
        if len(result["top_values"]) > 0:
            assert "value" in result["top_values"][0]
            assert "count" in result["top_values"][0]
    
    def test_nonexistent_column(self, sample_dataframe):
        """Test error handling for nonexistent column."""
        result = analyze_column("nonexistent", "summary", sample_dataframe)
        
        assert "error" in result
        assert "not found" in result["error"].lower()
    
    def test_no_dataframe(self):
        """Test error handling when no dataframe provided."""
        result = analyze_column("price", "summary", None)
        
        assert "error" in result
        assert "no dataset" in result["error"].lower()
    
    def test_unknown_analysis_type(self, sample_dataframe):
        """Test error handling for unknown analysis type."""
        result = analyze_column("price", "unknown_type", sample_dataframe)
        
        assert "error" in result
        assert "unknown" in result["error"].lower()


# Test calculate_correlation function
class TestCalculateCorrelation:
    """Test the calculate_correlation tool."""
    
    def test_positive_correlation(self, sample_dataframe):
        """Test calculation of positive correlation."""
        result = calculate_correlation("price", "price", sample_dataframe)
        
        assert result["column1"] == "price"
        assert result["column2"] == "price"
        assert result["correlation"] == 1.0
        assert "strong positive" in result["interpretation"]
    
    def test_negative_correlation(self):
        """Test calculation of negative correlation."""
        # Create data with negative correlation
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [5, 4, 3, 2, 1]
        })
        
        result = calculate_correlation("x", "y", df)
        
        assert result["correlation"] < 0
        assert "negative" in result["interpretation"]
    
    def test_no_correlation(self):
        """Test calculation with no correlation."""
        import numpy as np
        np.random.seed(42)
        
        df = pd.DataFrame({
            'x': np.random.rand(100),
            'y': np.random.rand(100)
        })
        
        result = calculate_correlation("x", "y", df)
        
        assert -0.2 < result["correlation"] < 0.2
        assert "weak" in result["interpretation"]
    
    def test_nonexistent_columns(self, sample_dataframe):
        """Test error handling for nonexistent columns."""
        result = calculate_correlation("nonexistent1", "nonexistent2", sample_dataframe)
        
        assert "error" in result
        assert "not found" in result["error"].lower()
    
    def test_non_numeric_columns(self, sample_dataframe):
        """Test error handling for non-numeric columns."""
        result = calculate_correlation("category", "region", sample_dataframe)
        
        assert "error" in result
        assert "numeric" in result["error"].lower()
    
    def test_mixed_column_types(self, sample_dataframe):
        """Test error handling for mixed column types."""
        result = calculate_correlation("price", "category", sample_dataframe)
        
        assert "error" in result
        assert "numeric" in result["error"].lower()
    
    def test_no_dataframe(self):
        """Test error handling when no dataframe provided."""
        result = calculate_correlation("col1", "col2", None)
        
        assert "error" in result
        assert "no dataset" in result["error"].lower()


# Test filter_data function
class TestFilterData:
    """Test the filter_data tool."""
    
    def test_filter_equals_numeric(self, sample_dataframe):
        """Test filtering with equals operator on numeric column."""
        result = filter_data("price", "equals", "29.99", sample_dataframe)
        
        assert result["original_rows"] == 8
        assert result["filtered_rows"] == 1
        assert "filter" in result
        assert "sample" in result
        assert len(result["sample"]) == 1
    
    def test_filter_equals_string(self, sample_dataframe):
        """Test filtering with equals operator on string column."""
        result = filter_data("category", "equals", "Electronics", sample_dataframe)
        
        assert result["filtered_rows"] == 4
        assert len(result["sample"]) <= 5
    
    def test_filter_greater_than(self, sample_dataframe):
        """Test filtering with greater_than operator."""
        result = filter_data("price", "greater_than", "50", sample_dataframe)
        
        assert result["filtered_rows"] == 2  # Prices > 50
        assert all(float(row["price"]) > 50 for row in result["sample"])
    
    def test_filter_less_than(self, sample_dataframe):
        """Test filtering with less_than operator."""
        result = filter_data("sales", "less_than", "100", sample_dataframe)
        
        assert result["filtered_rows"] == 2  # Sales < 100
        assert all(int(row["sales"]) < 100 for row in result["sample"])
    
    def test_filter_contains(self, sample_dataframe):
        """Test filtering with contains operator."""
        result = filter_data("product", "contains", "Widget", sample_dataframe)
        
        assert result["filtered_rows"] == 2
        assert all("Widget" in row["product"] for row in result["sample"])
    
    def test_filter_contains_case_insensitive(self, sample_dataframe):
        """Test that contains filter is case-insensitive."""
        result = filter_data("product", "contains", "widget", sample_dataframe)
        
        assert result["filtered_rows"] == 2  # Should match "Widget" despite lowercase
    
    def test_filter_no_matches(self, sample_dataframe):
        """Test filtering that returns no matches."""
        result = filter_data("price", "greater_than", "1000", sample_dataframe)
        
        assert result["filtered_rows"] == 0
        assert len(result["sample"]) == 0
    
    def test_filter_nonexistent_column(self, sample_dataframe):
        """Test error handling for nonexistent column."""
        result = filter_data("nonexistent", "equals", "value", sample_dataframe)
        
        assert "error" in result
        assert "not found" in result["error"].lower()
    
    def test_filter_unknown_operator(self, sample_dataframe):
        """Test error handling for unknown operator."""
        result = filter_data("price", "unknown_op", "50", sample_dataframe)
        
        assert "error" in result
        assert "unknown" in result["error"].lower()
    
    def test_filter_no_dataframe(self):
        """Test error handling when no dataframe provided."""
        result = filter_data("column", "equals", "value", None)
        
        assert "error" in result
        assert "no dataset" in result["error"].lower()
    
    def test_filter_invalid_numeric_conversion(self, sample_dataframe):
        """Test error handling for invalid numeric conversion."""
        result = filter_data("price", "greater_than", "not_a_number", sample_dataframe)
        
        assert "error" in result


# Test get_dataset_summary function
class TestGetDatasetSummary:
    """Test the get_dataset_summary tool."""
    
    def test_basic_summary(self, sample_dataframe):
        """Test basic dataset summary."""
        result = get_dataset_summary(sample_dataframe)
        
        assert "shape" in result
        assert result["shape"]["rows"] == 8
        assert result["shape"]["columns"] == 5
        
        assert "columns" in result
        assert "all" in result["columns"]
        assert "numeric" in result["columns"]
        assert "categorical" in result["columns"]
        
        assert len(result["columns"]["all"]) == 5
        assert "price" in result["columns"]["numeric"]
        assert "sales" in result["columns"]["numeric"]
        assert "category" in result["columns"]["categorical"]
    
    def test_summary_with_missing_values(self, large_dataframe):
        """Test summary with missing values."""
        result = get_dataset_summary(large_dataframe)
        
        assert "missing_values" in result
        assert "status" in result["missing_values"]  # Has None values
        assert result["missing_values"]["status"] > 0
    
    def test_memory_usage(self, sample_dataframe):
        """Test memory usage calculation."""
        result = get_dataset_summary(sample_dataframe)
        
        assert "memory_usage_mb" in result
        assert isinstance(result["memory_usage_mb"], float)
        assert result["memory_usage_mb"] > 0
    
    def test_no_dataframe(self):
        """Test error handling when no dataframe provided."""
        result = get_dataset_summary(None)
        
        assert "error" in result
        assert "no dataset" in result["error"].lower()
    
    def test_large_dataset(self, large_dataframe):
        """Test summary with larger dataset."""
        result = get_dataset_summary(large_dataframe)
        
        assert result["shape"]["rows"] == 100
        assert result["shape"]["columns"] == 4
        assert len(result["columns"]["all"]) == 4


# Test agent configuration
class TestAgentConfiguration:
    """Test agent setup and configuration."""
    
    def test_tool_declarations_exist(self):
        """Test that tool declarations are properly defined."""
        assert len(TOOL_DECLARATIONS) == 4
        
        tool_names = [decl.name for decl in TOOL_DECLARATIONS]
        assert "analyze_column" in tool_names
        assert "calculate_correlation" in tool_names
        assert "filter_data" in tool_names
        assert "get_dataset_summary" in tool_names
    
    def test_tool_mapping_complete(self):
        """Test that all tools are mapped to functions."""
        assert len(TOOLS) == 4
        assert "analyze_column" in TOOLS
        assert "calculate_correlation" in TOOLS
        assert "filter_data" in TOOLS
        assert "get_dataset_summary" in TOOLS
        
        # Verify they are callable
        assert callable(TOOLS["analyze_column"])
        assert callable(TOOLS["calculate_correlation"])
        assert callable(TOOLS["filter_data"])
        assert callable(TOOLS["get_dataset_summary"])
    
    def test_agent_config_structure(self):
        """Test agent configuration structure."""
        assert "name" in AGENT_CONFIG
        assert AGENT_CONFIG["name"] == "data_analysis_agent"
        
        assert "model" in AGENT_CONFIG
        assert "gemini" in AGENT_CONFIG["model"]
        
        assert "description" in AGENT_CONFIG
        assert "tools" in AGENT_CONFIG
        assert len(AGENT_CONFIG["tools"]) == 4
    
    def test_create_agent_with_api_key(self):
        """Test agent creation with explicit API key."""
        import os
        
        # Skip if no API key
        if not os.getenv("GOOGLE_API_KEY"):
            pytest.skip("GOOGLE_API_KEY not set")
        
        client = create_data_analysis_agent()
        assert client is not None
    
    def test_create_agent_no_api_key(self):
        """Test error handling when no API key provided."""
        import os
        
        # Temporarily clear API key
        original = os.getenv("GOOGLE_API_KEY")
        if original:
            os.environ.pop("GOOGLE_API_KEY", None)
        
        with pytest.raises(ValueError, match="GOOGLE_API_KEY"):
            create_data_analysis_agent()
        
        # Restore
        if original:
            os.environ["GOOGLE_API_KEY"] = original
    
    def test_get_agent_instruction_no_data(self):
        """Test agent instruction generation without dataset."""
        instruction = get_agent_instruction(None)
        
        assert "data analyst" in instruction.lower()
        assert "no dataset" in instruction.lower()
        assert "tools" in instruction.lower()
    
    def test_get_agent_instruction_with_data(self, sample_dataframe):
        """Test agent instruction generation with dataset."""
        instruction = get_agent_instruction(sample_dataframe)
        
        assert "data analyst" in instruction.lower()
        assert "8 rows" in instruction
        assert "5 columns" in instruction
        assert "price" in instruction
        assert "category" in instruction


# Test tool parameters
class TestToolParameters:
    """Test tool parameter validation."""
    
    def test_analyze_column_parameters(self):
        """Test analyze_column tool parameters."""
        tool = next(t for t in TOOL_DECLARATIONS if t.name == "analyze_column")
        
        # Access Schema object attributes
        params_schema = tool.parameters
        assert hasattr(params_schema, 'properties')
        assert "column_name" in params_schema.properties
        assert "analysis_type" in params_schema.properties
        
        # Check enum values
        analysis_type_prop = params_schema.properties["analysis_type"]
        assert hasattr(analysis_type_prop, 'enum')
        assert "summary" in analysis_type_prop.enum
        assert "distribution" in analysis_type_prop.enum
        assert "top_values" in analysis_type_prop.enum
        
        # Check required fields
        assert hasattr(params_schema, 'required')
        assert "column_name" in params_schema.required
        assert "analysis_type" in params_schema.required
    
    def test_calculate_correlation_parameters(self):
        """Test calculate_correlation tool parameters."""
        tool = next(t for t in TOOL_DECLARATIONS if t.name == "calculate_correlation")
        
        params_schema = tool.parameters
        assert "column1" in params_schema.properties
        assert "column2" in params_schema.properties
        
        assert "column1" in params_schema.required
        assert "column2" in params_schema.required
    
    def test_filter_data_parameters(self):
        """Test filter_data tool parameters."""
        tool = next(t for t in TOOL_DECLARATIONS if t.name == "filter_data")
        
        params_schema = tool.parameters
        assert "column_name" in params_schema.properties
        assert "operator" in params_schema.properties
        assert "value" in params_schema.properties
        
        # Check operator enum
        operator_prop = params_schema.properties["operator"]
        assert hasattr(operator_prop, 'enum')
        operators = operator_prop.enum
        assert "equals" in operators
        assert "greater_than" in operators
        assert "less_than" in operators
        assert "contains" in operators
        
        # Check required fields
        assert len(params_schema.required) == 3
    
    def test_get_dataset_summary_parameters(self):
        """Test get_dataset_summary tool parameters."""
        tool = next(t for t in TOOL_DECLARATIONS if t.name == "get_dataset_summary")
        
        # Should have empty properties dict (no parameters needed)
        params_schema = tool.parameters
        assert hasattr(params_schema, 'properties')
        assert len(params_schema.properties) == 0


# Test DataAnalysisAgent class
class TestDataAnalysisAgent:
    """Test the DataAnalysisAgent class."""
    
    def test_agent_initialization(self, sample_dataframe):
        """Test agent can be initialized with dataframe."""
        import os
        
        # Skip if no API key
        if not os.getenv("GOOGLE_API_KEY"):
            pytest.skip("GOOGLE_API_KEY not set")
        
        from agent import DataAnalysisAgent
        
        agent = DataAnalysisAgent(dataframe=sample_dataframe)
        assert agent is not None
        assert agent.dataframe is not None
        assert agent.model == "gemini-2.0-flash-exp"
    
    def test_agent_initialization_no_api_key(self):
        """Test error when no API key provided."""
        import os
        from agent import DataAnalysisAgent
        
        # Temporarily clear API key
        original = os.getenv("GOOGLE_API_KEY")
        if original:
            os.environ.pop("GOOGLE_API_KEY", None)
        
        with pytest.raises(ValueError, match="GOOGLE_API_KEY"):
            DataAnalysisAgent()
        
        # Restore
        if original:
            os.environ["GOOGLE_API_KEY"] = original
    
    def test_agent_set_dataframe(self, sample_dataframe):
        """Test setting dataframe after initialization."""
        import os
        
        if not os.getenv("GOOGLE_API_KEY"):
            pytest.skip("GOOGLE_API_KEY not set")
        
        from agent import DataAnalysisAgent
        
        agent = DataAnalysisAgent()
        assert agent.dataframe is None
        
        agent.set_dataframe(sample_dataframe)
        assert agent.dataframe is not None
        assert len(agent.dataframe) == 8
    
    def test_agent_get_dataset_info(self, sample_dataframe):
        """Test getting dataset info from agent."""
        import os
        
        if not os.getenv("GOOGLE_API_KEY"):
            pytest.skip("GOOGLE_API_KEY not set")
        
        from agent import DataAnalysisAgent
        
        agent = DataAnalysisAgent(dataframe=sample_dataframe)
        info = agent.get_dataset_info()
        
        assert "shape" in info
        assert info["shape"]["rows"] == 8
        assert info["shape"]["columns"] == 5
    
    def test_agent_no_dataframe(self):
        """Test agent behavior without dataframe."""
        import os
        
        if not os.getenv("GOOGLE_API_KEY"):
            pytest.skip("GOOGLE_API_KEY not set")
        
        from agent import DataAnalysisAgent
        
        agent = DataAnalysisAgent()
        info = agent.get_dataset_info()
        
        assert "error" in info
    
    def test_agent_analyze_without_dataframe(self):
        """Test analysis fails gracefully without dataframe."""
        import os
        
        if not os.getenv("GOOGLE_API_KEY"):
            pytest.skip("GOOGLE_API_KEY not set")
        
        from agent import DataAnalysisAgent
        
        agent = DataAnalysisAgent()
        response = agent.analyze("What is the average price?")
        
        assert "No dataset" in response or "no dataset" in response.lower()
    
    def test_create_agent_helper(self, sample_dataframe):
        """Test the create_data_analysis_agent helper function."""
        import os
        
        if not os.getenv("GOOGLE_API_KEY"):
            pytest.skip("GOOGLE_API_KEY not set")
        
        agent = create_data_analysis_agent(dataframe=sample_dataframe)
        assert agent is not None
        assert agent.dataframe is not None


# Integration tests
class TestIntegration:
    """Integration tests for complete workflows."""
    
    def test_full_analysis_workflow(self, sample_dataframe):
        """Test a complete analysis workflow."""
        # 1. Get dataset summary
        summary = get_dataset_summary(sample_dataframe)
        assert summary["shape"]["rows"] == 8
        
        # 2. Analyze a numeric column
        price_analysis = analyze_column("price", "summary", sample_dataframe)
        assert price_analysis["type"] == "numeric"
        assert "mean" in price_analysis
        
        # 3. Calculate correlation
        correlation = calculate_correlation("price", "sales", sample_dataframe)
        assert "correlation" in correlation
        
        # 4. Filter data
        filtered = filter_data("price", "greater_than", "50", sample_dataframe)
        assert filtered["filtered_rows"] < filtered["original_rows"]
    
    def test_categorical_analysis_workflow(self, sample_dataframe):
        """Test categorical data analysis workflow."""
        # 1. Analyze categorical column
        category_analysis = analyze_column("category", "summary", sample_dataframe)
        assert category_analysis["type"] == "categorical"
        assert category_analysis["unique"] == 3
        
        # 2. Get distribution
        distribution = analyze_column("category", "distribution", sample_dataframe)
        assert "distribution" in distribution
        
        # 3. Get top values
        top_values = analyze_column("category", "top_values", sample_dataframe)
        assert len(top_values["top_values"]) > 0
        
        # 4. Filter by category
        filtered = filter_data("category", "equals", "Electronics", sample_dataframe)
        assert filtered["filtered_rows"] == 4
    
    def test_error_recovery(self, sample_dataframe):
        """Test error handling and recovery."""
        # Try invalid operations
        result1 = analyze_column("nonexistent", "summary", sample_dataframe)
        assert "error" in result1
        
        result2 = calculate_correlation("price", "category", sample_dataframe)
        assert "error" in result2
        
        result3 = filter_data("price", "invalid_op", "50", sample_dataframe)
        assert "error" in result3
        
        # Verify valid operations still work
        valid_result = get_dataset_summary(sample_dataframe)
        assert "error" not in valid_result
        assert valid_result["shape"]["rows"] == 8
    
    def test_agent_workflow(self, sample_dataframe):
        """Test complete agent-based workflow."""
        import os
        
        if not os.getenv("GOOGLE_API_KEY"):
            pytest.skip("GOOGLE_API_KEY not set")
        
        from agent import DataAnalysisAgent
        
        # Create agent with dataframe
        agent = DataAnalysisAgent(dataframe=sample_dataframe)
        
        # Get dataset info
        info = agent.get_dataset_info()
        assert info["shape"]["rows"] == 8
        
        # Test with different dataframe
        new_df = pd.DataFrame({
            'a': [1, 2, 3],
            'b': [4, 5, 6]
        })
        agent.set_dataframe(new_df)
        
        info = agent.get_dataset_info()
        assert info["shape"]["rows"] == 3
        assert info["shape"]["columns"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
