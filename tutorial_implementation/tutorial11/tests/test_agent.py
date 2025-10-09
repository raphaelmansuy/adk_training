"""
Comprehensive pytest test suite for grounding agent.

Run with: pytest tests/test_agent.py -v
"""

import pytest
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
        assert len(research_assistant.tools) == 2  # 2 custom tools (no search in current ADK)
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

        # Should mention key capabilities (no search_tool in current version)
        assert "analyze_search_results" in instruction
        assert "save_research_findings" in instruction
        assert "research process" in instruction

        # Should mention research process
        assert "research process" in instruction or "process" in instruction


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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
