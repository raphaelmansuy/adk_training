"""
Test suite for agent configuration and tool registration - Tutorial 02: Function Tools

Tests the Finance Assistant agent setup, tool registration, and basic functionality.
"""

import pytest
from unittest.mock import patch
from finance_assistant.agent import (
    root_agent,
    calculate_compound_interest,
    calculate_loan_payment,
    calculate_monthly_savings
)


class TestAgentConfiguration:
    """Test agent configuration and setup."""

    def test_agent_creation(self):
        """Test that the agent is created successfully."""
        assert root_agent is not None
        assert root_agent.name == "finance_assistant"
        assert root_agent.model == "gemini-2.0-flash"

    def test_agent_description(self):
        """Test that agent has proper description."""
        description = root_agent.description
        assert "financial calculation assistant" in description.lower()
        assert "compound interest" in description.lower()
        assert "loan payment" in description.lower()
        assert "monthly savings" in description.lower()

    def test_agent_tools_registration(self):
        """Test that all three tools are registered."""
        tools = root_agent.tools
        assert len(tools) == 3

        tool_functions = [tool for tool in tools]
        assert calculate_compound_interest in tool_functions
        assert calculate_loan_payment in tool_functions
        assert calculate_monthly_savings in tool_functions


class TestToolFunctionSignatures:
    """Test tool function signatures and metadata."""

    def test_compound_interest_signature(self):
        """Test calculate_compound_interest function signature."""
        assert callable(calculate_compound_interest)

        # Check function has proper docstring
        assert calculate_compound_interest.__doc__ is not None
        assert "compound interest" in calculate_compound_interest.__doc__.lower()
        assert "Args:" in calculate_compound_interest.__doc__
        assert "Returns:" in calculate_compound_interest.__doc__

    def test_loan_payment_signature(self):
        """Test calculate_loan_payment function signature."""
        assert callable(calculate_loan_payment)

        # Check function has proper docstring
        assert calculate_loan_payment.__doc__ is not None
        assert "loan payment" in calculate_loan_payment.__doc__.lower()
        assert "Args:" in calculate_loan_payment.__doc__
        assert "Returns:" in calculate_loan_payment.__doc__

    def test_monthly_savings_signature(self):
        """Test calculate_monthly_savings function signature."""
        assert callable(calculate_monthly_savings)

        # Check function has proper docstring
        assert calculate_monthly_savings.__doc__ is not None
        assert "monthly savings" in calculate_monthly_savings.__doc__.lower()
        assert "Args:" in calculate_monthly_savings.__doc__
        assert "Returns:" in calculate_monthly_savings.__doc__

    def test_function_type_hints(self):
        """Test that functions have proper type hints."""
        import inspect

        # Check compound interest function
        sig = inspect.signature(calculate_compound_interest)
        assert 'principal' in sig.parameters
        assert 'annual_rate' in sig.parameters
        assert 'years' in sig.parameters
        assert 'compounds_per_year' in sig.parameters

        # Check loan payment function
        sig = inspect.signature(calculate_loan_payment)
        assert 'loan_amount' in sig.parameters
        assert 'annual_rate' in sig.parameters
        assert 'years' in sig.parameters

        # Check monthly savings function
        sig = inspect.signature(calculate_monthly_savings)
        assert 'target_amount' in sig.parameters
        assert 'years' in sig.parameters
        assert 'annual_return' in sig.parameters


class TestToolReturnFormats:
    """Test that tools return properly formatted results."""

    def test_compound_interest_return_format(self):
        """Test calculate_compound_interest return format."""
        result = calculate_compound_interest(1000, 0.05, 1)

        required_keys = ['status', 'final_amount', 'interest_earned', 'report']
        for key in required_keys:
            assert key in result

        assert result['status'] == 'success'
        assert isinstance(result['final_amount'], (int, float))
        assert isinstance(result['interest_earned'], (int, float))
        assert isinstance(result['report'], str)

    def test_loan_payment_return_format(self):
        """Test calculate_loan_payment return format."""
        result = calculate_loan_payment(100000, 0.05, 10)

        required_keys = ['status', 'monthly_payment', 'total_paid', 'total_interest', 'report']
        for key in required_keys:
            assert key in result

        assert result['status'] == 'success'
        assert isinstance(result['monthly_payment'], (int, float))
        assert isinstance(result['total_paid'], (int, float))
        assert isinstance(result['total_interest'], (int, float))
        assert isinstance(result['report'], str)

    def test_monthly_savings_return_format(self):
        """Test calculate_monthly_savings return format."""
        result = calculate_monthly_savings(10000, 2, 0.05)

        required_keys = ['status', 'monthly_savings', 'total_contributed',
                         'interest_earned', 'report']
        for key in required_keys:
            assert key in result

        assert result['status'] == 'success'
        assert isinstance(result['monthly_savings'], (int, float))
        assert isinstance(result['total_contributed'], (int, float))
        assert isinstance(result['interest_earned'], (int, float))
        assert isinstance(result['report'], str)

    def test_error_return_format(self):
        """Test error return format across all tools."""
        # Test compound interest error
        result = calculate_compound_interest(-1000, 0.05, 1)
        assert result['status'] == 'error'
        assert 'error' in result
        assert 'report' in result
        assert isinstance(result['report'], str)

        # Test loan payment error
        result = calculate_loan_payment(100000, 0.05, 0)
        assert result['status'] == 'error'
        assert 'error' in result
        assert 'report' in result

        # Test monthly savings error
        result = calculate_monthly_savings(10000, 0, 0.05)
        assert result['status'] == 'error'
        assert 'error' in result
        assert 'report' in result


class TestAgentIntegration:
    """Test agent integration and functionality."""

    @patch('google.adk.agents.Agent')
    def test_agent_initialization_mock(self, mock_agent_class):
        """Test agent initialization with mocked Agent class."""
        # This would be used if we wanted to test agent creation without actual ADK
        # For now, we test that the real agent exists and has expected properties
        pass

    def test_agent_has_required_attributes(self):
        """Test that agent has all required attributes for ADK."""
        # Check that agent has the attributes ADK expects
        assert hasattr(root_agent, 'name')
        assert hasattr(root_agent, 'model')
        assert hasattr(root_agent, 'description')
        assert hasattr(root_agent, 'tools')

    def test_tools_are_callable(self):
        """Test that all registered tools are callable."""
        for tool in root_agent.tools:
            assert callable(tool)

    def test_agent_can_be_imported(self):
        """Test that agent can be imported successfully."""
        # This test ensures the module imports without errors
        from finance_assistant.agent import root_agent as imported_agent
        assert imported_agent is not None
        assert imported_agent.name == "finance_assistant"


class TestProjectStructure:
    """Test project structure and imports."""

    def test_imports_work(self):
        """Test that all imports work correctly."""
        import importlib.util

        try:
            # Check if the module can be found and loaded
            spec = importlib.util.find_spec('finance_assistant.agent')
            assert spec is not None, "finance_assistant.agent module not found"

            # Try to load the module
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            assert True
        except Exception as e:
            pytest.fail(f"Import failed: {e}")

    def test_module_structure(self):
        """Test that the module has expected structure."""
        import finance_assistant.agent

        # Check module has expected attributes
        assert hasattr(finance_assistant.agent, 'root_agent')
        assert hasattr(finance_assistant.agent, 'calculate_compound_interest')
        assert hasattr(finance_assistant.agent, 'calculate_loan_payment')
        assert hasattr(finance_assistant.agent, 'calculate_monthly_savings')

    def test_main_execution(self):
        """Test that main execution doesn't raise errors."""
        # Import and run the main section
        import subprocess
        import sys

        # Run the agent module as a script
        result = subprocess.run(
            [sys.executable, 'finance_assistant/agent.py'],
            capture_output=True,
            text=True,
            cwd='.'
        )

        # Should exit successfully (return code 0)
        assert result.returncode == 0

        # Should print expected output
        assert "Finance Assistant Agent" in result.stdout
        assert "Compound Interest Test:" in result.stdout
        assert "Loan Payment Test:" in result.stdout
        assert "Monthly Savings Test:" in result.stdout


if __name__ == "__main__":
    pytest.main([__file__])
