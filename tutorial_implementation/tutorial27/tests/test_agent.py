"""
Test suite for Third-Party Tools Integration - Tutorial 27

Tests the agent configuration, tool registration, and LangChain integration.
"""

import pytest
from third_party_agent.agent import root_agent, create_wikipedia_tool


class TestAgentConfiguration:
    """Test agent configuration and setup."""

    def test_agent_creation(self):
        """Test that the agent is created successfully."""
        assert root_agent is not None
        assert root_agent.name == "third_party_agent"
        assert root_agent.model == "gemini-2.0-flash"

    def test_agent_description(self):
        """Test that agent has proper description."""
        description = root_agent.description
        assert "research assistant" in description.lower()
        assert "wikipedia" in description.lower()
        assert "third-party" in description.lower()

    def test_agent_instruction(self):
        """Test that agent has comprehensive instructions."""
        instruction = root_agent.instruction
        assert "wikipedia" in instruction.lower()
        assert "research" in instruction.lower()
        assert "factual" in instruction.lower()

    def test_agent_tools_registration(self):
        """Test that tools are registered correctly."""
        tools = root_agent.tools
        assert len(tools) == 1, "Should have 1 tool (Wikipedia)"
        
    def test_agent_output_key(self):
        """Test that output_key is configured."""
        assert root_agent.output_key == "research_response"


class TestWikipediaTool:
    """Test Wikipedia tool creation and configuration."""

    def test_create_wikipedia_tool(self):
        """Test that Wikipedia tool can be created."""
        wiki_tool = create_wikipedia_tool()
        assert wiki_tool is not None
        
    def test_wikipedia_tool_type(self):
        """Test that Wikipedia tool has correct type."""
        from google.adk.tools.langchain_tool import LangchainTool
        wiki_tool = create_wikipedia_tool()
        # Tool should be a LangchainTool wrapper
        assert isinstance(wiki_tool, LangchainTool)

    def test_wikipedia_tool_configuration(self):
        """Test that Wikipedia tool is properly configured."""
        wiki_tool = create_wikipedia_tool()
        # Verify the tool has required ADK tool attributes
        assert hasattr(wiki_tool, 'name')
        assert hasattr(wiki_tool, 'description')
        assert hasattr(wiki_tool, 'func')


class TestImports:
    """Test that all imports work correctly."""

    def test_adk_imports(self):
        """Test ADK core imports."""
        from google.adk.agents import Agent
        assert Agent is not None

    def test_langchain_tool_import(self):
        """Test LangchainTool import path (critical for tutorial)."""
        from google.adk.tools.langchain_tool import LangchainTool
        assert LangchainTool is not None

    def test_langchain_community_imports(self):
        """Test LangChain community imports."""
        from langchain_community.tools import WikipediaQueryRun
        from langchain_community.utilities import WikipediaAPIWrapper
        assert WikipediaQueryRun is not None
        assert WikipediaAPIWrapper is not None

    def test_wikipedia_import(self):
        """Test wikipedia package is available."""
        import wikipedia
        assert wikipedia is not None


class TestAgentIntegration:
    """Test agent integration and functionality."""

    def test_agent_can_be_imported(self):
        """Test that agent can be imported successfully."""
        from third_party_agent.agent import root_agent as imported_agent
        assert imported_agent is not None
        assert imported_agent.name == "third_party_agent"

    def test_agent_has_wikipedia_capability(self):
        """Test that agent description mentions Wikipedia."""
        assert "wikipedia" in root_agent.description.lower()
        assert "wikipedia" in root_agent.instruction.lower()

    def test_tool_callable(self):
        """Test that the Wikipedia tool has execution capabilities."""
        wiki_tool = create_wikipedia_tool()
        # Tool should have async execution method
        assert hasattr(wiki_tool, 'run_async')
        assert hasattr(wiki_tool, 'func')


class TestProjectStructure:
    """Test project structure and packaging."""

    def test_module_structure(self):
        """Test that the module has expected structure."""
        import third_party_agent
        assert hasattr(third_party_agent, 'root_agent')

    def test_module_all_export(self):
        """Test that __all__ is properly defined."""
        import third_party_agent
        assert hasattr(third_party_agent, '__all__')
        assert 'root_agent' in third_party_agent.__all__

    def test_imports_work(self):
        """Test that all imports work correctly."""
        from third_party_agent import root_agent
        from third_party_agent.agent import create_wikipedia_tool
        assert root_agent is not None
        assert create_wikipedia_tool is not None


class TestLangChainIntegration:
    """Test LangChain-specific integration."""

    def test_langchain_wrapper_usage(self):
        """Test that LangchainTool wrapper is used correctly."""
        from google.adk.tools.langchain_tool import LangchainTool
        wiki_tool = create_wikipedia_tool()
        assert isinstance(wiki_tool, LangchainTool)

    def test_wikipedia_api_wrapper_config(self):
        """Test Wikipedia API wrapper configuration."""
        from langchain_community.utilities import WikipediaAPIWrapper
        # Create wrapper with same config as agent
        wrapper = WikipediaAPIWrapper(
            top_k_results=3,
            doc_content_chars_max=4000
        )
        assert wrapper is not None


class TestDocumentation:
    """Test that code is properly documented."""

    def test_module_docstring(self):
        """Test that module has docstring."""
        import third_party_agent.agent as agent_module
        assert agent_module.__doc__ is not None
        assert len(agent_module.__doc__) > 0

    def test_function_docstrings(self):
        """Test that functions have docstrings."""
        assert create_wikipedia_tool.__doc__ is not None
        assert "Wikipedia" in create_wikipedia_tool.__doc__

    def test_agent_has_description(self):
        """Test that agent has description field."""
        assert root_agent.description is not None
        assert len(root_agent.description) > 0

    def test_agent_has_instruction(self):
        """Test that agent has instruction field."""
        assert root_agent.instruction is not None
        assert len(root_agent.instruction) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
