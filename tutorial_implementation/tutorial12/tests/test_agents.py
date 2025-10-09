"""
Test agents and planners for Strategic Problem Solver.
"""

import pytest
from unittest.mock import MagicMock

from strategic_solver.agent import (
    builtin_planner_agent,
    plan_react_agent,
    strategic_planner_agent,
    root_agent,
    StrategicPlanner
)
from google.adk.agents import Agent
from google.adk.planners import BuiltInPlanner, PlanReActPlanner, BasePlanner


class TestAgentConfiguration:
    """Test agent configurations."""

    def test_builtin_planner_agent_config(self):
        """Test BuiltInPlanner agent configuration."""
        assert isinstance(builtin_planner_agent, Agent)
        assert builtin_planner_agent.name == "builtin_planner_strategic_solver"
        assert builtin_planner_agent.model == "gemini-2.0-flash"
        assert isinstance(builtin_planner_agent.planner, BuiltInPlanner)

    def test_plan_react_agent_config(self):
        """Test PlanReActPlanner agent configuration."""
        assert isinstance(plan_react_agent, Agent)
        assert plan_react_agent.name == "plan_react_strategic_solver"
        assert isinstance(plan_react_agent.planner, PlanReActPlanner)

    def test_strategic_planner_agent_config(self):
        """Test StrategicPlanner agent configuration."""
        assert isinstance(strategic_planner_agent, Agent)
        assert strategic_planner_agent.name == "strategic_planner_solver"
        assert isinstance(strategic_planner_agent.planner, StrategicPlanner)

    def test_root_agent_is_plan_react(self):
        """Test that root_agent uses PlanReActPlanner."""
        assert root_agent is plan_react_agent
        assert isinstance(root_agent.planner, PlanReActPlanner)

    def test_agents_have_tools(self):
        """Test that all agents have the required tools."""
        agents = [builtin_planner_agent, plan_react_agent, strategic_planner_agent]

        for agent in agents:
            assert len(agent.tools) == 4  # 4 business analysis tools
            tool_names = [tool.func.__name__ for tool in agent.tools]
            assert "analyze_market" in tool_names
            assert "calculate_roi" in tool_names
            assert "assess_risk" in tool_names
            assert "save_strategy_report" in tool_names

    def test_agents_have_output_keys(self):
        """Test that agents have appropriate output keys."""
        assert builtin_planner_agent.output_key == "builtin_strategy_result"
        assert plan_react_agent.output_key == "plan_react_strategy_result"
        assert strategic_planner_agent.output_key == "strategic_planner_result"


class TestPlannerConfiguration:
    """Test planner configurations."""

    def test_builtin_planner_thinking_config(self):
        """Test BuiltInPlanner has thinking config enabled."""
        planner = builtin_planner_agent.planner
        assert isinstance(planner, BuiltInPlanner)
        assert planner.thinking_config.include_thoughts is True

    def test_plan_react_planner_instance(self):
        """Test PlanReActPlanner is properly instantiated."""
        planner = plan_react_agent.planner
        assert isinstance(planner, PlanReActPlanner)

    def test_strategic_planner_inheritance(self):
        """Test StrategicPlanner inherits from BasePlanner."""
        planner = strategic_planner_agent.planner
        assert isinstance(planner, StrategicPlanner)
        assert isinstance(planner, BasePlanner)


class TestStrategicPlanner:
    """Test custom StrategicPlanner implementation."""

    def test_strategic_planner_creation(self):
        """Test StrategicPlanner can be created."""
        planner = StrategicPlanner()
        assert isinstance(planner, StrategicPlanner)
        assert isinstance(planner, BasePlanner)

    def test_build_planning_instruction(self):
        """Test StrategicPlanner builds planning instruction."""
        planner = StrategicPlanner()
        mock_context = MagicMock()
        mock_request = MagicMock()

        instruction = planner.build_planning_instruction(mock_context, mock_request)

        assert instruction is not None
        assert "ANALYSIS" in instruction
        assert "EVALUATION" in instruction
        assert "STRATEGY" in instruction
        assert "VALIDATION" in instruction
        assert "FINAL_RECOMMENDATION" in instruction

    def test_process_planning_response(self):
        """Test StrategicPlanner processes planning response."""
        planner = StrategicPlanner()
        mock_callback_context = MagicMock()
        mock_parts = [MagicMock()]

        result = planner.process_planning_response(mock_callback_context, mock_parts)

        # Should return the parts unchanged for this implementation
        assert result == mock_parts


class TestAgentInstructions:
    """Test agent instruction content."""

    def test_builtin_planner_instruction(self):
        """Test BuiltInPlanner agent has appropriate instruction."""
        instruction = builtin_planner_agent.instruction
        assert "strategic consultant" in instruction.lower()
        assert "analyze_market" in instruction
        assert "calculate_roi" in instruction
        assert "assess_risk" in instruction

    def test_plan_react_instruction(self):
        """Test PlanReActPlanner agent has structured instruction."""
        instruction = plan_react_agent.instruction
        assert "systematic" in instruction.lower()
        assert "planning tags" in instruction.lower()
        assert "structured format" in instruction.lower()

    def test_strategic_planner_instruction(self):
        """Test StrategicPlanner agent has domain-specific instruction."""
        instruction = strategic_planner_agent.instruction
        assert "business strategy consultant" in instruction.lower()
        assert "ANALYSIS" in instruction
        assert "EVALUATION" in instruction
        assert "STRATEGY" in instruction


class TestGenerateContentConfig:
    """Test content generation configurations."""

    def test_temperature_settings(self):
        """Test temperature settings for different agents."""
        # Strategic agents should have lower temperature for consistency
        assert builtin_planner_agent.generate_content_config.temperature == 0.3
        assert plan_react_agent.generate_content_config.temperature == 0.4
        assert strategic_planner_agent.generate_content_config.temperature == 0.3

    def test_max_output_tokens(self):
        """Test max output token settings."""
        agents = [builtin_planner_agent, plan_react_agent, strategic_planner_agent]
        for agent in agents:
            assert agent.generate_content_config.max_output_tokens == 3000


@pytest.mark.asyncio
class TestDemoFunction:
    """Test demo functionality."""

    async def test_demo_function_exists(self):
        """Test that demo function can be imported."""
        from strategic_solver.agent import demo_strategic_planning
        assert callable(demo_strategic_planning)

    async def test_demo_function_runs_without_error(self):
        """Test that demo function runs without throwing exceptions."""
        from strategic_solver.agent import demo_strategic_planning

        # This should not raise an exception (though it may not do much without API keys)
        try:
            await demo_strategic_planning()
        except Exception as e:
            # Allow certain expected errors (like missing API keys)
            if "API key" not in str(e) and "GOOGLE_API_KEY" not in str(e):
                raise