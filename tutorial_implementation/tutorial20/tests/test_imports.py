# Tutorial 20: YAML Configuration - Import Tests
# Validates that all modules can be imported correctly

import pytest


class TestImports:
    """Test that all modules can be imported."""

    def test_tools_import(self):
        """Test that tools package can be imported."""
        try:
            from tutorial_implementation.tutorial20.customer_support import tools
            assert tools is not None
        except ImportError as e:
            pytest.fail(f"Failed to import tools package: {e}")

    def test_customer_tools_import(self):
        """Test that customer_tools module can be imported."""
        try:
            from tutorial20.tools import customer_tools
            assert customer_tools is not None
        except ImportError as e:
            pytest.fail(f"Failed to import customer_tools: {e}")

    def test_all_tool_functions_importable(self):
        """Test that all tool functions can be imported."""
        try:
            from tutorial20.tools.customer_tools import (
                check_customer_status,
                log_interaction,
                get_order_status,
                track_shipment,
                cancel_order,
                search_knowledge_base,
                run_diagnostic,
                create_ticket,
                get_billing_history,
                process_refund,
                update_payment_method,
            )
            # If we get here, all imports succeeded
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import tool functions: {e}")

    def test_adk_config_utils_import(self):
        """Test that ADK config utils can be imported."""
        try:
            from google.adk.agents import config_agent_utils
            assert config_agent_utils is not None
        except ImportError as e:
            pytest.fail(f"Failed to import config_agent_utils: {e}")

    def test_run_agent_import(self):
        """Test that run_agent script can be imported."""
        try:
            import run_agent
            assert run_agent is not None
        except ImportError as e:
            pytest.fail(f"Failed to import run_agent: {e}")


class TestToolFunctionSignatures:
    """Test that tool functions have correct signatures."""

    def test_tool_functions_are_callable(self):
        """Test that imported tool functions are callable."""
        from tutorial20.tools.customer_tools import check_customer_status

        assert callable(check_customer_status)

    def test_tool_function_returns_dict(self):
        """Test that tool function returns a dictionary."""
        from tutorial20.tools.customer_tools import check_customer_status

        result = check_customer_status('test')
        assert isinstance(result, dict)