"""Test tutorial directory structure."""

import os
import pytest


def test_agent_directory_exists():
    """Test that agent directory exists."""
    assert os.path.isdir("agent"), "agent/ directory should exist"


def test_agent_files_exist():
    """Test that required agent files exist."""
    assert os.path.isfile("agent/__init__.py"), "agent/__init__.py should exist"
    assert os.path.isfile("agent/agent.py"), "agent/agent.py should exist"
    assert os.path.isfile("agent/.env.example"), "agent/.env.example should exist"


def test_frontend_directory_exists():
    """Test that frontend directory exists."""
    assert os.path.isdir("frontend"), "frontend/ directory should exist"


def test_tests_directory_exists():
    """Test that tests directory exists."""
    assert os.path.isdir("tests"), "tests/ directory should exist"


def test_root_files_exist():
    """Test that required root files exist."""
    assert os.path.isfile("requirements.txt"), "requirements.txt should exist"
    assert os.path.isfile("pyproject.toml"), "pyproject.toml should exist"
    assert os.path.isfile("Makefile"), "Makefile should exist"
    assert os.path.isfile("README.md"), "README.md should exist"


def test_env_example_content():
    """Test that .env.example contains required variables."""
    with open("agent/.env.example", "r") as f:
        content = f.read()
        assert "GOOGLE_API_KEY" in content, ".env.example should contain GOOGLE_API_KEY"


def test_requirements_content():
    """Test that requirements.txt contains required packages."""
    with open("requirements.txt", "r") as f:
        content = f.read()
        required_packages = [
            "google-adk",
            "fastapi",
            "uvicorn",
            "ag-ui-adk",
            "python-dotenv",
            "pytest"
        ]
        for package in required_packages:
            assert package in content, f"requirements.txt should contain {package}"
