"""
Test project structure
"""

import os
import pytest


def test_pyproject_exists():
    """Test that pyproject.toml exists."""
    assert os.path.exists("pyproject.toml")


def test_agent_module_exists():
    """Test that agent module exists."""
    assert os.path.isdir("data_viz_agent")
    assert os.path.exists("data_viz_agent/__init__.py")
    assert os.path.exists("data_viz_agent/agent.py")


def test_main_file_exists():
    """Test that main.py exists."""
    assert os.path.exists("main.py")


def test_env_example_exists():
    """Test that .env.example exists."""
    assert os.path.exists(".env.example")


def test_readme_exists():
    """Test that README.md exists."""
    assert os.path.exists("README.md")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
