"""
Import and structure validation tests
"""


class TestImports:
    """Test that all modules can be imported successfully."""
    
    def test_import_agent_module(self):
        """Test that agent module can be imported."""
        from data_analysis_agent import agent
        assert agent is not None
    
    def test_import_root_agent(self):
        """Test that root_agent can be imported from module."""
        from data_analysis_agent import root_agent
        assert root_agent is not None
    
    def test_import_from_package(self):
        """Test that root_agent can be imported from package."""
        from data_analysis_agent import root_agent
        assert hasattr(root_agent, 'name')
        assert hasattr(root_agent, 'model')
    
    def test_tool_functions_exist(self):
        """Test that all tool functions exist and are callable."""
        from data_analysis_agent.agent import (
            analyze_column,
            calculate_correlation,
            filter_data,
            get_dataset_summary,
        )
        
        assert callable(analyze_column)
        assert callable(calculate_correlation)
        assert callable(filter_data)
        assert callable(get_dataset_summary)
    
    def test_agent_has_required_attributes(self):
        """Test that agent has required attributes."""
        from data_analysis_agent import root_agent
        
        assert hasattr(root_agent, 'name')
        assert hasattr(root_agent, 'model')
        assert hasattr(root_agent, 'description')
        assert hasattr(root_agent, 'instruction')
        assert hasattr(root_agent, 'tools')
