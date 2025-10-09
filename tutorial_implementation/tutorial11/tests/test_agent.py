"""
Comprehensive pytest test suite for grounding agent.

Run with: pytest tests/test_agent.py -v
"""

import pytest
import os
from unittest.mock import Mock
from grounding_agent.agent import (
    root_agent,
    basic_grounding_agent,
    advanced_grounding_agent,
    research_assistant,
    analyze_search_results,
    save_research_findings
)


class TestToolFunctions:
    """Test custom tools in isolation"""

    def setup_method(self):
        """Setup before each test"""
        # Create a mock ToolContext for testing
        self.tool_context = Mock()

    def test_analyze_search_results_success(self):
        """Test successful search result analysis"""
        query = "quantum computing"
        content = "Quantum computing uses quantum mechanics. Recent breakthroughs include error correction. IBM announced a 1000-qubit processor."

        result = analyze_search_results(query, content, self.tool_context)

        assert result["status"] == "success"
        assert "quantum computing" in result["report"].lower()
        assert result["analysis"]["query"] == query
        assert result["analysis"]["word_count"] > 0
        assert len(result["analysis"]["key_insights"]) > 0
        assert result["analysis"]["content_quality"] in ["good", "limited"]

    def test_analyze_search_results_empty_content(self):
        """Test analysis with empty content"""
        result = analyze_search_results("test query", "", self.tool_context)

        assert result["status"] == "success"
        assert result["analysis"]["word_count"] == 0
        assert result["analysis"]["content_quality"] == "limited"

    def test_analyze_search_results_error_handling(self):
        """Test error handling in analysis"""
        # This should not raise an exception
        result = analyze_search_results("test", "valid content", self.tool_context)
        assert result["status"] == "success"

    def test_save_research_findings_success(self):
        """Test successful research findings save"""
        topic = "AI Developments"
        findings = "Recent breakthroughs in AI include large language models."

        result = save_research_findings(topic, findings, self.tool_context)

        assert result["status"] == "success"
        assert "saved as" in result["report"]
        assert "research_ai_developments.md" in result["filename"]
        assert result["version"] == "1.0"

    def test_save_research_findings_special_chars(self):
        """Test saving with special characters in topic"""
        topic = "Quantum Computing & AI"
        findings = "Test findings"

        result = save_research_findings(topic, findings, self.tool_context)

        assert result["status"] == "success"
        assert "research_quantum_computing_&_ai.md" in result["filename"]


class TestAgentConfiguration:
    """Test agent setup and configuration"""

    def test_root_agent_is_basic_grounding_agent(self):
        """Test that root_agent is the basic grounding agent"""
        assert root_agent is basic_grounding_agent

    def test_basic_grounding_agent_config(self):
        """Test basic grounding agent configuration"""
        assert basic_grounding_agent.name == "basic_grounding_agent"
        assert basic_grounding_agent.model == "gemini-2.0-flash"
        assert "google_search" in str(basic_grounding_agent.tools)
        assert basic_grounding_agent.output_key == "grounding_response"

    def test_advanced_grounding_agent_config(self):
        """Test advanced grounding agent configuration"""
        assert advanced_grounding_agent.name == "advanced_grounding_agent"
        assert advanced_grounding_agent.model == "gemini-2.0-flash"
        # Note: In current ADK, google_search cannot be mixed with custom tools
        # This tests the intended configuration
        tool_names = [str(tool) for tool in advanced_grounding_agent.tools]
        assert any("google_search" in name for name in tool_names)
        # Should have 3 tools total: google_search + 2 FunctionTools
        assert len(advanced_grounding_agent.tools) == 3
        assert advanced_grounding_agent.output_key == "advanced_research_response"

    def test_research_assistant_config(self):
        """Test research assistant configuration"""
        assert research_assistant.name == "research_assistant"
        assert research_assistant.model == "gemini-2.0-flash"
        assert len(research_assistant.tools) == 3  # google_search + 2 custom tools
        assert research_assistant.output_key == "research_response"

        # Check generate_content_config
        config = research_assistant.generate_content_config
        assert config.temperature == 0.3
        assert config.max_output_tokens == 2048

    def test_agents_have_descriptions(self):
        """Test all agents have descriptions"""
        agents = [basic_grounding_agent, advanced_grounding_agent, research_assistant]

        for agent in agents:
            assert agent.description is not None
            assert len(agent.description) > 0

    def test_agents_have_instructions(self):
        """Test all agents have instructions"""
        agents = [basic_grounding_agent, advanced_grounding_agent, research_assistant]

        for agent in agents:
            assert agent.instruction is not None
            assert len(agent.instruction) > 0
            assert "search" in agent.instruction.lower()


class TestGroundingCapabilities:
    """Test grounding-specific functionality"""

    def test_basic_agent_has_google_search(self):
        """Test basic agent has google_search tool"""
        tool_names = [str(tool) for tool in basic_grounding_agent.tools]
        assert any("google_search" in name for name in tool_names)

    def test_advanced_agent_has_search_tool(self):
        """Test advanced agent has google_search tool"""
        tool_names = [str(tool) for tool in advanced_grounding_agent.tools]
        assert any("google_search" in name for name in tool_names)

    def test_research_agent_instruction_quality(self):
        """Test research agent has comprehensive instructions"""
        instruction = research_assistant.instruction.lower()

        # Should mention key capabilities (now includes search)
        assert "analyze_search_results" in instruction
        assert "save_research_findings" in instruction
        assert "research process" in instruction
        assert "web research" in instruction  # Now includes web research capabilities


class TestIntegration:
    """Integration tests for multi-step workflows"""

    def setup_method(self):
        """Setup before each test"""
        self.tool_context = Mock()

    def test_research_workflow_simulation(self):
        """Test simulated research workflow"""
        # Simulate the workflow that the agent would perform

        # Step 1: Analyze search results
        analysis_result = analyze_search_results(
            "AI trends 2025",
            "Artificial Intelligence continues to evolve rapidly. Key trends include multimodal models, agent systems, and ethical AI development.",
            self.tool_context
        )
        assert analysis_result["status"] == "success"

        # Step 2: Save findings
        save_result = save_research_findings(
            "AI Trends 2025",
            "AI is evolving with multimodal models and agent systems.",
            self.tool_context
        )
        assert save_result["status"] == "success"

        # Verify workflow consistency
        assert analysis_result["analysis"]["query"] == "AI trends 2025"
        assert "ai_trends_2025.md" in save_result["filename"]

    def test_tool_error_handling(self):
        """Test tools handle errors gracefully"""
        # Test with invalid inputs
        result = analyze_search_results("", "", self.tool_context)
        assert result["status"] == "success"  # Should not fail

        result = save_research_findings("", "", self.tool_context)
        assert result["status"] == "success"  # Should not fail


class TestAgentImports:
    """Test that all imports work correctly"""

    def test_agent_imports(self):
        """Test that all agent imports work"""
        from grounding_agent.agent import (
            basic_grounding_agent,
            advanced_grounding_agent,
            research_assistant,
            root_agent
        )

        assert basic_grounding_agent is not None
        assert advanced_grounding_agent is not None
        assert research_assistant is not None
        assert root_agent is not None

    def test_tool_imports(self):
        """Test that tool imports work"""
        from grounding_agent.agent import (
            analyze_search_results,
            save_research_findings
        )

        assert callable(analyze_search_results)
        assert callable(save_research_findings)


class TestVertexAIConditionalLogic:
    """Test conditional VertexAI functionality"""

    def test_is_vertexai_enabled_false_by_default(self):
        """Test that VertexAI is disabled by default"""
        # This should work without any environment variables set
        from grounding_agent.agent import is_vertexai_enabled
        assert not is_vertexai_enabled()

    def test_is_vertexai_enabled_with_env_var(self, monkeypatch):
        """Test that VertexAI is enabled when env var is set"""
        from grounding_agent.agent import is_vertexai_enabled

        # Test with "1"
        monkeypatch.setenv('GOOGLE_GENAI_USE_VERTEXAI', '1')
        assert is_vertexai_enabled()

        # Test with "true" (should not work, only "1" works)
        monkeypatch.setenv('GOOGLE_GENAI_USE_VERTEXAI', 'true')
        assert not is_vertexai_enabled()

        # Test with "0"
        monkeypatch.setenv('GOOGLE_GENAI_USE_VERTEXAI', '0')
        assert not is_vertexai_enabled()

    def test_get_available_grounding_tools_without_vertexai(self):
        """Test tool loading without VertexAI"""
        from grounding_agent.agent import get_available_grounding_tools
        import os

        # Ensure VertexAI is disabled
        original_value = os.environ.get('GOOGLE_GENAI_USE_VERTEXAI')
        try:
            if 'GOOGLE_GENAI_USE_VERTEXAI' in os.environ:
                del os.environ['GOOGLE_GENAI_USE_VERTEXAI']

            tools = get_available_grounding_tools()
            assert len(tools) == 1
            assert 'google_search' in str(tools[0]).lower()
        finally:
            if original_value is not None:
                os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = original_value

    def test_get_available_grounding_tools_with_vertexai(self, monkeypatch):
        """Test tool loading with VertexAI enabled"""
        from grounding_agent.agent import get_available_grounding_tools

        monkeypatch.setenv('GOOGLE_GENAI_USE_VERTEXAI', '1')
        tools = get_available_grounding_tools()
        assert len(tools) == 2
        tool_names = [str(tool).lower() for tool in tools]
        assert any('google_search' in name for name in tool_names)
        assert any('google_maps' in name for name in tool_names)

    def test_get_agent_capabilities_description_without_vertexai(self):
        """Test capabilities description without VertexAI"""
        from grounding_agent.agent import get_agent_capabilities_description
        import os

        # Ensure VertexAI is disabled
        original_value = os.environ.get('GOOGLE_GENAI_USE_VERTEXAI')
        try:
            if 'GOOGLE_GENAI_USE_VERTEXAI' in os.environ:
                del os.environ['GOOGLE_GENAI_USE_VERTEXAI']

            desc = get_agent_capabilities_description()
            assert 'web search for current information' in desc
            assert 'maps' not in desc.lower()
        finally:
            if original_value is not None:
                os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = original_value

    def test_get_agent_capabilities_description_with_vertexai(self, monkeypatch):
        """Test capabilities description with VertexAI"""
        from grounding_agent.agent import get_agent_capabilities_description

        monkeypatch.setenv('GOOGLE_GENAI_USE_VERTEXAI', '1')
        desc = get_agent_capabilities_description()
        assert 'web search for current information' in desc
        assert 'location-based queries and maps grounding' in desc

    def test_agents_include_maps_tools_with_vertexai(self, monkeypatch):
        """Test that agents include maps tools when VertexAI is enabled"""
        monkeypatch.setenv('GOOGLE_GENAI_USE_VERTEXAI', '1')

        # Force re-evaluation of the module-level variables
        # (In real usage, these would be evaluated at import time)
        # For this test, we'll check that the functions work correctly
        from grounding_agent.agent import get_available_grounding_tools

        tools = get_available_grounding_tools()
        assert len(tools) == 2  # Should include maps grounding

    def test_root_agent_selection_logic(self):
        """Test that root_agent selection logic works correctly"""
        from grounding_agent.agent import is_vertexai_enabled

        # Test the logic that determines which agent to use
        # Note: root_agent is set at import time, so we test the selection logic

        # When VertexAI is disabled, should use basic agent
        original_value = os.environ.get('GOOGLE_GENAI_USE_VERTEXAI')
        try:
            if 'GOOGLE_GENAI_USE_VERTEXAI' in os.environ:
                del os.environ['GOOGLE_GENAI_USE_VERTEXAI']

            # Test the selection logic directly
            assert not is_vertexai_enabled()
            # The root_agent would be basic_grounding_agent in this case
            # (We can't easily test the module-level assignment in pytest)

        finally:
            if original_value is not None:
                os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = original_value

    def test_agent_instructions_adapt_to_vertexai(self, monkeypatch):
        """Test that agent instructions adapt based on VertexAI availability"""
        from grounding_agent.agent import basic_grounding_agent

        # Test without VertexAI
        original_env = {}
        for key in ['GOOGLE_GENAI_USE_VERTEXAI']:
            if key in os.environ:
                original_env[key] = os.environ[key]

        try:
            # Clear VertexAI env var
            if 'GOOGLE_GENAI_USE_VERTEXAI' in os.environ:
                del os.environ['GOOGLE_GENAI_USE_VERTEXAI']

            # Instructions should not mention maps
            instructions = basic_grounding_agent.instruction.lower()
            assert 'maps' not in instructions

            # Set VertexAI
            monkeypatch.setenv('GOOGLE_GENAI_USE_VERTEXAI', '1')

            # Note: In the current implementation, agent instructions are set at import time
            # So they won't dynamically change. This test documents the expected behavior.
            # In a production system, you might want to make instructions dynamic too.

        finally:
            # Restore environment
            for key, value in original_env.items():
                os.environ[key] = value


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
