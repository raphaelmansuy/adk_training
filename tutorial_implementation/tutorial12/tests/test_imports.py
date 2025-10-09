"""
Test imports and basic agent structure for Strategic Problem Solver.
"""

import importlib.util
import os

import pytest


class TestImports:
    """Test that all modules can be imported correctly."""

    def test_strategic_solver_agent_import(self):
        """Test that strategic_solver.agent module can be imported."""
        spec = importlib.util.find_spec("strategic_solver.agent")
        assert spec is not None, "strategic_solver.agent module not found"

    def test_strategic_solver_agent_has_root_agent(self):
        """Test that strategic_solver.agent has root_agent."""
        import strategic_solver.agent
        assert hasattr(strategic_solver.agent, 'root_agent')

    def test_root_agent_is_agent_instance(self):
        """Test that root_agent is an Agent instance."""
        from strategic_solver.agent import root_agent
        from google.adk.agents import Agent
        assert isinstance(root_agent, Agent)

    def test_all_planner_agents_exist(self):
        """Test that all planner agent variants exist."""
        from strategic_solver.agent import (
            builtin_planner_agent,
            plan_react_agent,
            strategic_planner_agent
        )

        from google.adk.agents import Agent

        assert isinstance(builtin_planner_agent, Agent)
        assert isinstance(plan_react_agent, Agent)
        assert isinstance(strategic_planner_agent, Agent)

    def test_planner_imports(self):
        """Test that planner classes can be imported."""
        from google.adk.planners import BuiltInPlanner, PlanReActPlanner, BasePlanner

        # These should not raise ImportError
        assert BuiltInPlanner is not None
        assert PlanReActPlanner is not None
        assert BasePlanner is not None


class TestProjectStructure:
    """Test that project structure is correct."""

    def test_strategic_solver_directory_exists(self):
        """Test that strategic_solver directory exists."""
        assert os.path.exists("strategic_solver")

    def test_init_file_exists(self):
        """Test that __init__.py exists."""
        assert os.path.exists("strategic_solver/__init__.py")

    def test_agent_file_exists(self):
        """Test that agent.py exists."""
        assert os.path.exists("strategic_solver/agent.py")

    def test_env_example_exists(self):
        """Test that .env.example exists."""
        assert os.path.exists("strategic_solver/.env.example")

    def test_init_file_content(self):
        """Test that __init__.py has correct content."""
        with open("strategic_solver/__init__.py", "r") as f:
            content = f.read()
            assert "Strategic Problem Solver" in content
            assert "Tutorial 12" in content

    def test_env_example_content(self):
        """Test that .env.example has required variables."""
        with open("strategic_solver/.env.example", "r") as f:
            content = f.read()
            assert "GOOGLE_API_KEY" in content
            assert "GOOGLE_GENAI_USE_VERTEXAI" in content

    def test_agent_file_is_python(self):
        """Test that agent.py is a valid Python file."""
        import strategic_solver.agent
        assert strategic_solver.agent.__file__.endswith("agent.py")


class TestTools:
    """Test that tools are properly defined."""

    def test_tools_can_be_imported(self):
        """Test that tool functions can be imported."""
        from strategic_solver.agent import (
            analyze_market,
            calculate_roi,
            assess_risk,
            save_strategy_report
        )

        # These should be functions
        assert callable(analyze_market)
        assert callable(calculate_roi)
        assert callable(assess_risk)
        assert callable(save_strategy_report)

    def test_tools_have_docstrings(self):
        """Test that tools have proper docstrings."""
        from strategic_solver.agent import (
            analyze_market,
            calculate_roi,
            assess_risk,
            save_strategy_report
        )

        assert analyze_market.__doc__ is not None
        assert "Analyze market conditions" in analyze_market.__doc__

        assert calculate_roi.__doc__ is not None
        assert "Calculate return on investment" in calculate_roi.__doc__

        assert assess_risk.__doc__ is not None
        assert "Assess business risks" in assess_risk.__doc__

        assert save_strategy_report.__doc__ is not None
        assert "Save strategic plan" in save_strategy_report.__doc__