"""
Test suite for Third-Party Tools Integration - Tutorial 27

Tests the agent configuration, tool registration, and LangChain integration.
"""

import pytest
from third_party_agent.agent import root_agent


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
        assert "comprehensive research" in description.lower()
        assert "wikipedia" in description.lower()
        assert "web search" in description.lower()
        assert "file system" in description.lower()
        assert "crewai" in description.lower()
        assert "third-party" in description.lower()

    def test_agent_instruction(self):
        """Test that agent has comprehensive instructions."""
        instruction = root_agent.instruction
        assert "wikipedia" in instruction.lower()
        assert "web search" in instruction.lower()
        assert "directory reading" in instruction.lower()
        assert "file reading" in instruction.lower()
        assert "research" in instruction.lower()
        assert "factual" in instruction.lower()

    def test_agent_tools_registration(self):
        """Test that tools are registered correctly."""
        tools = root_agent.tools
        assert len(tools) == 4, "Should have 4 tools (Wikipedia, Web Search, Directory Read, File Read)"
        
    def test_agent_output_key(self):
        """Test that output_key is configured."""
        assert root_agent.output_key == "research_response"


class TestWebSearchTool:
    """Test Web Search tool creation and configuration."""

    def test_create_web_search_tool(self):
        """Test that Web Search tool can be created."""
        from third_party_agent.agent import create_web_search_tool
        search_tool = create_web_search_tool()
        assert search_tool is not None
        
    def test_web_search_tool_type(self):
        """Test that Web Search tool has correct type."""
        from third_party_agent.agent import create_web_search_tool
        from google.adk.tools.langchain_tool import LangchainTool
        search_tool = create_web_search_tool()
        # Tool should be a LangchainTool wrapper
        assert isinstance(search_tool, LangchainTool)

    def test_web_search_tool_configuration(self):
        """Test that Web Search tool is properly configured."""
        from third_party_agent.agent import create_web_search_tool
        search_tool = create_web_search_tool()
        # Verify the tool has required ADK tool attributes
        assert hasattr(search_tool, 'name')
        assert hasattr(search_tool, 'description')
        assert hasattr(search_tool, 'func')


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
        from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
        from langchain_community.utilities import WikipediaAPIWrapper
        assert WikipediaQueryRun is not None
        assert DuckDuckGoSearchRun is not None
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
        """Test that agent description mentions all tools."""
        assert "wikipedia" in root_agent.description.lower()
        assert "web search" in root_agent.description.lower()
        assert "directoryreadtool" in root_agent.description.lower()
        assert "filereadtool" in root_agent.description.lower()
        assert "wikipedia" in root_agent.instruction.lower()
        assert "web search" in root_agent.instruction.lower()
        assert "directory reading" in root_agent.instruction.lower()
        assert "file reading" in root_agent.instruction.lower()

    def test_tool_callable(self):
        """Test that the Wikipedia tool has execution capabilities."""
        from third_party_agent.agent import create_wikipedia_tool
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
        from third_party_agent.agent import create_wikipedia_tool, create_web_search_tool, create_directory_read_tool, create_file_read_tool
        assert root_agent is not None
        assert create_wikipedia_tool is not None
        assert create_web_search_tool is not None
        assert create_directory_read_tool is not None
        assert create_file_read_tool is not None


class TestWikipediaTool:
    """Test Wikipedia tool creation and configuration."""

    def test_create_wikipedia_tool(self):
        """Test that Wikipedia tool can be created."""
        from third_party_agent.agent import create_wikipedia_tool
        wiki_tool = create_wikipedia_tool()
        assert wiki_tool is not None
        
    def test_wikipedia_tool_type(self):
        """Test that Wikipedia tool has correct type."""
        from third_party_agent.agent import create_wikipedia_tool
        from google.adk.tools.langchain_tool import LangchainTool
        wiki_tool = create_wikipedia_tool()
        # Tool should be a LangchainTool wrapper
        assert isinstance(wiki_tool, LangchainTool)

    def test_wikipedia_tool_configuration(self):
        """Test that Wikipedia tool is properly configured."""
        from third_party_agent.agent import create_wikipedia_tool
        wiki_tool = create_wikipedia_tool()
        # Verify the tool has required ADK tool attributes
        assert hasattr(wiki_tool, 'name')
        assert hasattr(wiki_tool, 'description')
        assert hasattr(wiki_tool, 'func')


class TestDocumentation:
    """Test that code is properly documented."""

    def test_module_docstring(self):
        """Test that module has docstring."""
        import third_party_agent.agent as agent_module
        assert agent_module.__doc__ is not None
        assert len(agent_module.__doc__) > 0

    def test_function_docstrings(self):
        """Test that functions have docstrings."""
        from third_party_agent.agent import create_wikipedia_tool, create_web_search_tool
        assert create_wikipedia_tool.__doc__ is not None
        assert "Wikipedia" in create_wikipedia_tool.__doc__
        assert create_web_search_tool.__doc__ is not None
        assert "web search" in create_web_search_tool.__doc__.lower()

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
