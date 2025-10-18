"""
Agent configuration and tools tests
"""


class TestAgentConfiguration:
    """Test agent configuration and properties."""
    
    def test_root_agent_exists(self):
        """Test that root_agent is properly defined."""
        from data_analysis_agent import root_agent
        
        assert root_agent is not None
    
    def test_agent_has_correct_name(self):
        """Test that agent has correct name.
        
        Note: After multi-agent refactor, the root agent is now a coordinator
        that delegates to specialized sub-agents (analysis and visualization).
        """
        from data_analysis_agent import root_agent
        
        # The coordinator agent has a different name but the pattern is correct
        assert root_agent.name in ["data_analysis_agent", "data_analysis_coordinator"]
    
    def test_agent_has_correct_model(self):
        """Test that agent uses the correct model."""
        from data_analysis_agent import root_agent
        
        assert root_agent.model == "gemini-2.0-flash"
    
    def test_agent_has_description(self):
        """Test that agent has a description."""
        from data_analysis_agent import root_agent
        
        assert root_agent.description is not None
        assert len(root_agent.description) > 0
    
    def test_agent_has_instruction(self):
        """Test that agent has instruction."""
        from data_analysis_agent import root_agent
        
        assert root_agent.instruction is not None
        assert len(root_agent.instruction) > 0
    
    def test_agent_has_tools(self):
        """Test that agent has tools configured."""
        from data_analysis_agent import root_agent
        
        assert hasattr(root_agent, 'tools')
        assert root_agent.tools is not None
        assert len(root_agent.tools) > 0
    
    def test_agent_tools_count(self):
        """Test that agent has expected number of tools.
        
        Note: After multi-agent refactor, the root agent now has 2 AgentTools
        (analysis_agent and visualization_agent) instead of 4 direct tools.
        This is the correct pattern as it allows the visualization_agent
        to have BuiltInCodeExecutor while analysis_agent has traditional tools.
        """
        from data_analysis_agent import root_agent
        
        # Now we have AgentTools instead of direct tools
        # 2 AgentTools: analysis_agent and visualization_agent
        assert len(root_agent.tools) >= 2


class TestAgentTools:
    """Test individual agent tools."""
    
    def test_analyze_column_tool(self):
        """Test analyze_column tool."""
        from data_analysis_agent.agent import analyze_column
        
        result = analyze_column("test_column", "summary")
        
        assert isinstance(result, dict)
        assert "status" in result
        assert "report" in result
        assert result["status"] in ["success", "error"]
    
    def test_analyze_column_success(self):
        """Test analyze_column with valid input."""
        from data_analysis_agent.agent import analyze_column
        
        result = analyze_column("age", "summary")
        
        assert result["status"] == "success"
        assert "report" in result
    
    def test_analyze_column_invalid_column(self):
        """Test analyze_column with invalid column name."""
        from data_analysis_agent.agent import analyze_column
        
        result = analyze_column("", "summary")
        
        assert result["status"] == "error"
        assert "report" in result
    
    def test_calculate_correlation_tool(self):
        """Test calculate_correlation tool."""
        from data_analysis_agent.agent import calculate_correlation
        
        result = calculate_correlation("col1", "col2")
        
        assert isinstance(result, dict)
        assert "status" in result
        assert "report" in result
        assert result["status"] in ["success", "error"]
    
    def test_calculate_correlation_missing_params(self):
        """Test calculate_correlation with missing parameters."""
        from data_analysis_agent.agent import calculate_correlation
        
        result = calculate_correlation("col1", "")
        
        assert result["status"] == "error"
    
    def test_filter_data_tool(self):
        """Test filter_data tool."""
        from data_analysis_agent.agent import filter_data
        
        result = filter_data("age", "greater_than", "30")
        
        assert isinstance(result, dict)
        assert "status" in result
        assert "report" in result
    
    def test_filter_data_missing_params(self):
        """Test filter_data with missing parameters."""
        from data_analysis_agent.agent import filter_data
        
        result = filter_data("", "equals", "value")
        
        assert result["status"] == "error"
    
    def test_get_dataset_summary_tool(self):
        """Test get_dataset_summary tool."""
        from data_analysis_agent.agent import get_dataset_summary
        
        result = get_dataset_summary()
        
        assert isinstance(result, dict)
        assert "status" in result
        assert result["status"] == "success"
        assert "report" in result
    
    def test_tool_return_format(self):
        """Test that tools return consistent format."""
        from data_analysis_agent.agent import (
            analyze_column,
            calculate_correlation,
            filter_data,
            get_dataset_summary,
        )
        
        tools = [
            analyze_column("col", "summary"),
            calculate_correlation("col1", "col2"),
            filter_data("col", "equals", "val"),
            get_dataset_summary(),
        ]
        
        for result in tools:
            assert isinstance(result, dict)
            assert "status" in result
            assert "report" in result
            assert result["status"] in ["success", "error"]


class TestToolExceptionHandling:
    """Test that tools handle exceptions gracefully."""
    
    def test_analyze_column_handles_exception(self):
        """Test that analyze_column handles exceptions."""
        from data_analysis_agent.agent import analyze_column
        
        # This should not raise an exception even with bad input
        result = analyze_column(None, None)  # type: ignore
        
        assert isinstance(result, dict)
        assert "status" in result
    
    def test_filter_data_handles_exception(self):
        """Test that filter_data handles exceptions."""
        from data_analysis_agent.agent import filter_data
        
        # This should not raise an exception even with bad input
        result = filter_data(None, None, None)  # type: ignore
        
        assert isinstance(result, dict)
        assert "status" in result
