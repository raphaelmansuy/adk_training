# Tutorial 22: Model Selection & Optimization - Agent Tests
# Validates agent configuration and tool functionality

import pytest
from unittest.mock import Mock, patch, MagicMock


class TestAgentConfiguration:
    """Test that the agent is properly configured."""

    def test_root_agent_import(self):
        """Test that root_agent can be imported."""
        from model_selector.agent import root_agent
        assert root_agent is not None

    def test_agent_is_agent_instance(self):
        """Test that root_agent is an Agent instance."""
        from model_selector.agent import root_agent
        from google.adk.agents import Agent

        assert isinstance(root_agent, Agent)

    def test_agent_name(self):
        """Test that agent has correct name."""
        from model_selector.agent import root_agent

        assert hasattr(root_agent, 'name')
        assert root_agent.name == "model_selector_agent"

    def test_agent_model(self):
        """Test that agent uses recommended model."""
        from model_selector.agent import root_agent

        assert hasattr(root_agent, 'model')
        assert root_agent.model == "gemini-2.5-flash"

    def test_agent_description(self):
        """Test that agent has description."""
        from model_selector.agent import root_agent

        assert hasattr(root_agent, 'description')
        assert ("model selection" in root_agent.description.lower() or 
                "selecting" in root_agent.description.lower())

    def test_agent_instruction(self):
        """Test that agent has comprehensive instruction."""
        from model_selector.agent import root_agent

        assert hasattr(root_agent, 'instruction')
        instruction = root_agent.instruction.lower()
        assert "model selection" in instruction
        assert "recommend" in instruction
        assert "gemini" in instruction

    def test_agent_has_tools(self):
        """Test that agent has tools configured."""
        from model_selector.agent import root_agent

        assert hasattr(root_agent, 'tools')
        assert len(root_agent.tools) > 0

    def test_agent_tools_count(self):
        """Test that agent has expected number of tools."""
        from model_selector.agent import root_agent

        # Should have 2 tools: recommend_model_for_use_case, get_model_info
        assert len(root_agent.tools) == 2


class TestToolFunctions:
    """Test individual tool functions."""

    def setup_method(self):
        """Setup before each test."""
        self.tool_context = Mock()

    def test_recommend_model_for_use_case_realtime(self):
        """Test model recommendation for real-time use case."""
        from model_selector.agent import recommend_model_for_use_case

        result = recommend_model_for_use_case(
            "real-time voice assistant",
            self.tool_context
        )

        assert result["status"] == "success"
        assert result["model"] == "gemini-2.0-flash-live"
        assert "real-time" in result["reason"].lower()
        assert "use_case" in result

    def test_recommend_model_for_use_case_complex(self):
        """Test model recommendation for complex reasoning."""
        from model_selector.agent import recommend_model_for_use_case

        result = recommend_model_for_use_case(
            "complex strategic planning",
            self.tool_context
        )

        assert result["status"] == "success"
        assert result["model"] == "gemini-2.5-pro"
        assert "complex" in result["reason"].lower() or "reasoning" in result["reason"].lower()

    def test_recommend_model_for_use_case_high_volume(self):
        """Test model recommendation for high-volume simple tasks."""
        from model_selector.agent import recommend_model_for_use_case

        result = recommend_model_for_use_case(
            "high-volume content moderation",
            self.tool_context
        )

        assert result["status"] == "success"
        assert result["model"] == "gemini-2.5-flash-lite"
        assert "fast" in result["reason"].lower() or "cheap" in result["reason"].lower()

    def test_recommend_model_for_use_case_critical(self):
        """Test model recommendation for critical operations."""
        from model_selector.agent import recommend_model_for_use_case

        result = recommend_model_for_use_case(
            "critical business operations",
            self.tool_context
        )

        assert result["status"] == "success"
        assert result["model"] == "gemini-2.5-pro"
        assert "quality" in result["reason"].lower() or "critical" in result["reason"].lower()

    def test_recommend_model_for_use_case_general(self):
        """Test model recommendation for general use case."""
        from model_selector.agent import recommend_model_for_use_case

        result = recommend_model_for_use_case(
            "general customer service",
            self.tool_context
        )

        assert result["status"] == "success"
        assert result["model"] == "gemini-2.5-flash"
        assert "price-performance" in result["reason"].lower() or "general" in result["reason"].lower()

    def test_recommend_model_for_use_case_extended_context(self):
        """Test model recommendation for large documents."""
        from model_selector.agent import recommend_model_for_use_case

        result = recommend_model_for_use_case(
            "extended context document analysis",
            self.tool_context
        )

        assert result["status"] == "success"
        assert result["model"] == "gemini-1.5-pro"
        assert "context" in result["reason"].lower() or "2m" in result["reason"].lower()

    def test_get_model_info_flash(self):
        """Test getting info for gemini-2.5-flash."""
        from model_selector.agent import get_model_info

        result = get_model_info("gemini-2.5-flash", self.tool_context)

        assert result["status"] == "success"
        assert result["model"] == "gemini-2.5-flash"
        assert "info" in result
        assert "context_window" in result["info"]
        assert "features" in result["info"]
        assert "best_for" in result["info"]

    def test_get_model_info_pro(self):
        """Test getting info for gemini-2.5-pro."""
        from model_selector.agent import get_model_info

        result = get_model_info("gemini-2.5-pro", self.tool_context)

        assert result["status"] == "success"
        assert result["model"] == "gemini-2.5-pro"
        assert "2M tokens" in result["info"]["context_window"]
        assert "High" in result["info"]["pricing"]

    def test_get_model_info_lite(self):
        """Test getting info for gemini-2.5-flash-lite."""
        from model_selector.agent import get_model_info

        result = get_model_info("gemini-2.5-flash-lite", self.tool_context)

        assert result["status"] == "success"
        assert result["model"] == "gemini-2.5-flash-lite"
        assert "Ultra-fast" in result["info"]["speed"]

    def test_get_model_info_invalid(self):
        """Test getting info for non-existent model."""
        from model_selector.agent import get_model_info

        result = get_model_info("nonexistent-model", self.tool_context)

        assert result["status"] == "error"
        assert "not found" in result["report"].lower()
        assert "error" in result


class TestModelSelector:
    """Test ModelSelector class functionality."""

    def test_model_selector_creation(self):
        """Test that ModelSelector can be created."""
        from model_selector.agent import ModelSelector

        selector = ModelSelector()
        assert selector is not None
        assert hasattr(selector, 'benchmarks')

    def test_model_selector_benchmarks_init(self):
        """Test that benchmarks dict is initialized empty."""
        from model_selector.agent import ModelSelector

        selector = ModelSelector()
        assert isinstance(selector.benchmarks, dict)
        assert len(selector.benchmarks) == 0


class TestModelBenchmark:
    """Test ModelBenchmark dataclass."""

    def test_model_benchmark_creation(self):
        """Test that ModelBenchmark can be created."""
        from model_selector.agent import ModelBenchmark

        benchmark = ModelBenchmark(
            model="gemini-2.5-flash",
            avg_latency=1.5,
            avg_tokens=100,
            quality_score=0.8,
            cost_estimate=0.0001,
            success_rate=1.0
        )

        assert benchmark.model == "gemini-2.5-flash"
        assert benchmark.avg_latency == 1.5
        assert benchmark.avg_tokens == 100
        assert benchmark.quality_score == 0.8
        assert benchmark.cost_estimate == 0.0001
        assert benchmark.success_rate == 1.0


@pytest.mark.integration
class TestAgentIntegration:
    """Integration tests that require real ADK (optional)."""

    def test_agent_can_be_created_without_error(self):
        """Test that agent can be created without raising exceptions."""
        try:
            from model_selector.agent import root_agent
            # If we get here without exception, basic creation works
            assert True
        except Exception as e:
            pytest.fail(f"Agent creation failed: {e}")

    def test_tool_context_in_tools(self):
        """Test that tools have tool_context parameter."""
        from model_selector.agent import (
            recommend_model_for_use_case,
            get_model_info
        )
        import inspect

        # Check recommend_model_for_use_case signature
        sig1 = inspect.signature(recommend_model_for_use_case)
        assert 'tool_context' in sig1.parameters

        # Check get_model_info signature
        sig2 = inspect.signature(get_model_info)
        assert 'tool_context' in sig2.parameters

    def test_tools_return_dict(self):
        """Test that tools return dictionaries."""
        from model_selector.agent import (
            recommend_model_for_use_case,
            get_model_info
        )

        mock_context = Mock()

        result1 = recommend_model_for_use_case("test use case", mock_context)
        assert isinstance(result1, dict)

        result2 = get_model_info("gemini-2.5-flash", mock_context)
        assert isinstance(result2, dict)
