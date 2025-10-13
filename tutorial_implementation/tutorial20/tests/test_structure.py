# Tutorial 20: YAML Configuration - Structure Tests
# Validates project structure and file organization

import os
import pytest


class TestProjectStructure:
    """Test that project has correct file structure."""

    def test_root_agent_yaml_exists(self):
        """Test that root_agent.yaml exists in customer_support package."""
        assert os.path.exists('customer_support/root_agent.yaml'), "customer_support/root_agent.yaml should exist"

    def test_tools_directory_exists(self):
        """Test that tools directory exists within customer_support package."""
        assert os.path.exists('customer_support/tools'), "customer_support/tools directory should exist"
        assert os.path.isdir('customer_support/tools'), "customer_support/tools should be a directory"

    def test_tools_init_exists(self):
        """Test that customer_support/tools/__init__.py exists."""
        assert os.path.exists('customer_support/tools/__init__.py'), "customer_support/tools/__init__.py should exist"

    def test_customer_tools_exists(self):
        """Test that customer_support/tools/customer_tools.py exists."""
        assert os.path.exists('customer_support/tools/customer_tools.py'), "customer_support/tools/customer_tools.py should exist"

    def test_run_agent_exists(self):
        """Test that run_agent.py exists."""
        assert os.path.exists('run_agent.py'), "run_agent.py should exist"

    def test_tests_directory_exists(self):
        """Test that tests directory exists."""
        assert os.path.exists('tests'), "tests directory should exist"
        assert os.path.isdir('tests'), "tests should be a directory"

    def test_test_files_exist(self):
        """Test that test files exist."""
        test_files = [
            'tests/__init__.py',
            'tests/test_agent.py',
            'tests/test_tools.py',
            'tests/test_imports.py',
            'tests/test_structure.py',
        ]

        for test_file in test_files:
            assert os.path.exists(test_file), f"{test_file} should exist"

    def test_project_files_exist(self):
        """Test that project configuration files exist."""
        project_files = [
            'pyproject.toml',
            'requirements.txt',
            'Makefile',
        ]

        for project_file in project_files:
            assert os.path.exists(project_file), f"{project_file} should exist"


class TestYAMLStructure:
    """Test YAML configuration file structure."""

    def test_yaml_is_valid(self):
        """Test that root_agent.yaml is valid YAML."""
        import yaml

        with open('customer_support/root_agent.yaml', 'r') as f:
            config = yaml.safe_load(f)

        assert config is not None, "YAML should be valid"
        assert isinstance(config, dict), "YAML should parse to dictionary"

    def test_yaml_has_required_fields(self):
        """Test that YAML has required top-level fields."""
        import yaml

        with open('customer_support/root_agent.yaml', 'r') as f:
            config = yaml.safe_load(f)

        required_fields = ['name', 'model', 'description', 'instruction']
        for field in required_fields:
            assert field in config, f"YAML should have {field} field"
            assert config[field], f"{field} should not be empty"

    def test_yaml_has_no_sub_agents(self):
        """Test that YAML has no sub_agents (single-agent configuration)."""
        import yaml

        with open('customer_support/root_agent.yaml', 'r') as f:
            config = yaml.safe_load(f)

        # Single-agent configuration should not have sub_agents
        assert 'sub_agents' not in config, "YAML should not have sub_agents field for single-agent config"

    def test_yaml_has_tools(self):
        """Test that YAML has tools configuration."""
        import yaml

        with open('customer_support/root_agent.yaml', 'r') as f:
            config = yaml.safe_load(f)

        assert 'tools' in config, "YAML should have tools field"
        assert isinstance(config['tools'], list), "tools should be a list"
        assert len(config['tools']) > 0, "should have at least one tool"

    def test_yaml_tools_have_correct_format(self):
        """Test that YAML tools are in correct format."""
        import yaml

        with open('customer_support/root_agent.yaml', 'r') as f:
            config = yaml.safe_load(f)

        for i, tool in enumerate(config['tools']):
            assert isinstance(tool, dict), f"Tool {i} should be a dict"
            assert 'name' in tool, f"Tool {i} should have name field"
            assert tool['name'].startswith('customer_support.tools.'), f"Tool {i} name should reference customer_support.tools module: {tool['name']}"


class TestToolFunctionStructure:
    """Test tool function structure and organization."""

    def test_all_tool_functions_defined(self):
        """Test that all expected tool functions are defined."""
        from customer_support.tools.customer_tools import (
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

        # All functions should be callable
        tool_functions = [
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
        ]

        for func in tool_functions:
            assert callable(func), f"{func.__name__} should be callable"

    def test_tools_init_exports_all_functions(self):
        """Test that customer_support.tools package exports all functions."""
        from customer_support import tools

        expected_exports = [
            'check_customer_status',
            'log_interaction',
            'get_order_status',
            'track_shipment',
            'cancel_order',
            'search_knowledge_base',
            'run_diagnostic',
            'create_ticket',
            'get_billing_history',
            'process_refund',
            'update_payment_method',
        ]

        for export in expected_exports:
            assert hasattr(tools, export), f"tutorial20.tools should export {export}"