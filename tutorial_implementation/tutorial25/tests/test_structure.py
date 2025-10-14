"""Test project structure and configuration."""

import os
import pytest
from pathlib import Path


def test_project_structure():
    """Test that required files and directories exist."""
    base_dir = Path(__file__).parent.parent
    
    # Required files
    assert (base_dir / "README.md").exists(), "README.md is missing"
    assert (base_dir / "requirements.txt").exists(), "requirements.txt is missing"
    assert (base_dir / "pyproject.toml").exists(), "pyproject.toml is missing"
    assert (base_dir / "Makefile").exists(), "Makefile is missing"
    assert (base_dir / ".env.example").exists(), ".env.example is missing"
    
    # Required directories
    assert (base_dir / "best_practices_agent").is_dir(), "best_practices_agent directory is missing"
    assert (base_dir / "tests").is_dir(), "tests directory is missing"
    
    # Agent module files
    assert (base_dir / "best_practices_agent" / "__init__.py").exists()
    assert (base_dir / "best_practices_agent" / "agent.py").exists()


def test_requirements_txt():
    """Test that requirements.txt has necessary dependencies."""
    base_dir = Path(__file__).parent.parent
    requirements_file = base_dir / "requirements.txt"
    
    content = requirements_file.read_text()
    
    assert "google-genai" in content, "google-genai not in requirements.txt"
    assert "google-adk" in content, "google-adk not in requirements.txt"
    assert "pydantic" in content, "pydantic not in requirements.txt"


def test_pyproject_toml():
    """Test that pyproject.toml is properly configured."""
    base_dir = Path(__file__).parent.parent
    pyproject_file = base_dir / "pyproject.toml"
    
    content = pyproject_file.read_text()
    
    assert "best_practices_agent" in content
    assert "google-genai" in content
    assert "google-adk" in content
    assert "pydantic" in content


def test_env_example():
    """Test that .env.example exists and has required variables."""
    base_dir = Path(__file__).parent.parent
    env_example = base_dir / ".env.example"
    
    content = env_example.read_text()
    
    assert "GOOGLE_API_KEY" in content


def test_makefile_targets():
    """Test that Makefile has required targets."""
    base_dir = Path(__file__).parent.parent
    makefile = base_dir / "Makefile"
    
    content = makefile.read_text()
    
    # Check for essential targets
    assert "setup:" in content
    assert "dev:" in content
    assert "test:" in content
    assert "clean:" in content
    assert "demo:" in content
