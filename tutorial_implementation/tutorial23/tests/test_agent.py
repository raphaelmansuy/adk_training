"""Test agent configuration and functionality."""

import pytest
from production_agent import root_agent
from production_agent.agent import (
    check_deployment_status,
    get_deployment_options,
    get_best_practices
)


class TestAgentConfiguration:
    """Test suite for agent configuration."""
    
    def test_agent_exists(self):
        """Test that root_agent is defined."""
        assert root_agent is not None
    
    def test_agent_name(self):
        """Test agent has correct name."""
        assert root_agent.name == "production_deployment_agent"
    
    def test_agent_model(self):
        """Test agent uses correct model."""
        assert root_agent.model == "gemini-2.0-flash"
    
    def test_agent_has_description(self):
        """Test agent has a description."""
        assert root_agent.description is not None
        assert len(root_agent.description) > 0
    
    def test_agent_has_instruction(self):
        """Test agent has instructions."""
        assert root_agent.instruction is not None
        assert len(root_agent.instruction) > 0
    
    def test_agent_has_tools(self):
        """Test agent has tools configured."""
        assert root_agent.tools is not None
        assert len(root_agent.tools) > 0
    
    def test_agent_has_generate_config(self):
        """Test agent has generation config."""
        assert root_agent.generate_content_config is not None
    
    def test_temperature_configured(self):
        """Test temperature is configured."""
        config = root_agent.generate_content_config
        assert hasattr(config, 'temperature')
        assert config.temperature == 0.5
    
    def test_max_tokens_configured(self):
        """Test max_output_tokens is configured."""
        config = root_agent.generate_content_config
        assert hasattr(config, 'max_output_tokens')
        assert config.max_output_tokens == 2048


class TestToolFunctions:
    """Test suite for tool functions."""
    
    def test_check_deployment_status(self):
        """Test check_deployment_status tool."""
        result = check_deployment_status()
        
        assert isinstance(result, dict)
        assert result["status"] == "success"
        assert "report" in result
        assert "deployment_type" in result
        assert "features" in result
        assert isinstance(result["features"], list)
    
    def test_get_deployment_options(self):
        """Test get_deployment_options tool."""
        result = get_deployment_options()
        
        assert isinstance(result, dict)
        assert result["status"] == "success"
        assert "options" in result
        
        options = result["options"]
        assert "local_api_server" in options
        assert "cloud_run" in options
        assert "agent_engine" in options
        assert "gke" in options
        
        # Verify structure of each option
        for option_key, option_data in options.items():
            assert "command" in option_data
            assert "description" in option_data
            assert "features" in option_data
    
    def test_get_best_practices(self):
        """Test get_best_practices tool."""
        result = get_best_practices()
        
        assert isinstance(result, dict)
        assert result["status"] == "success"
        assert "best_practices" in result
        
        practices = result["best_practices"]
        assert "security" in practices
        assert "monitoring" in practices
        assert "scalability" in practices
        assert "reliability" in practices
        
        # Verify each category has practices
        for category, items in practices.items():
            assert isinstance(items, list)
            assert len(items) > 0


class TestToolCommands:
    """Test that tool outputs contain correct deployment commands."""
    
    def test_deployment_commands_accuracy(self):
        """Test that deployment commands in tools are accurate."""
        result = get_deployment_options()
        options = result["options"]
        
        # Verify commands match official ADK CLI
        assert options["local_api_server"]["command"] == "adk api_server"
        assert options["cloud_run"]["command"] == "adk deploy cloud_run"
        assert options["agent_engine"]["command"] == "adk deploy agent_engine"
        assert options["gke"]["command"] == "adk deploy gke"
    
    def test_deployment_features_completeness(self):
        """Test that each deployment option has meaningful features."""
        result = get_deployment_options()
        options = result["options"]
        
        for option_name, option_data in options.items():
            features = option_data["features"]
            assert len(features) >= 3, f"{option_name} should have at least 3 features"
            
            # Features should be non-empty strings
            for feature in features:
                assert isinstance(feature, str)
                assert len(feature) > 0


class TestAgentIntegration:
    """Integration tests requiring GOOGLE_API_KEY."""
    
    @pytest.mark.skipif(
        not pytest.importorskip("os").environ.get("GOOGLE_API_KEY"),
        reason="GOOGLE_API_KEY not set"
    )
    async def test_agent_invocation(self):
        """Test actual agent invocation."""
        from google.adk.agents import Runner
        
        runner = Runner()
        query = "What deployment options are available?"
        
        result = await runner.run_async(query, agent=root_agent)
        
        assert result is not None
        assert hasattr(result, 'content')
        assert hasattr(result.content, 'parts')
        assert len(result.content.parts) > 0
