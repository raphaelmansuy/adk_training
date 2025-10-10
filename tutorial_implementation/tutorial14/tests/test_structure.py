"""
Test project structure and configuration.
"""

from pathlib import Path


def test_project_structure():
    """Test that the project has the expected directory structure."""
    base_path = Path(__file__).parent.parent

    # Check for required directories
    assert (base_path / "streaming_agent").exists()
    assert (base_path / "streaming_agent").is_dir()

    assert (base_path / "tests").exists()
    assert (base_path / "tests").is_dir()

    # Check for required files
    required_files = [
        "pyproject.toml",
        "requirements.txt",
        "Makefile",
        "streaming_agent/__init__.py",
        "streaming_agent/agent.py",
        "streaming_agent/.env.example",
        "tests/__init__.py",
        "tests/test_agent.py",
        "tests/test_imports.py",
        "tests/test_structure.py"
    ]

    for file_path in required_files:
        assert (base_path / file_path).exists(), f"Missing required file: {file_path}"
        assert (base_path / file_path).is_file(), f"Expected file, got directory: {file_path}"


def test_env_example_structure():
    """Test that .env.example has required structure."""
    base_path = Path(__file__).parent.parent
    env_example = base_path / "streaming_agent" / ".env.example"

    assert env_example.exists()

    content = env_example.read_text()

    # Check for required environment variables
    required_vars = [
        "GOOGLE_API_KEY",
        "GOOGLE_GENAI_USE_VERTEXAI"
    ]

    for var in required_vars:
        assert var in content, f"Missing required environment variable in .env.example: {var}"


def test_pyproject_toml_structure():
    """Test that pyproject.toml has required structure."""
    base_path = Path(__file__).parent.parent
    pyproject = base_path / "pyproject.toml"

    assert pyproject.exists()

    content = pyproject.read_text()

    # Check for required sections
    required_sections = [
        "[build-system]",
        "[project]",
        "[tool.setuptools.packages.find]"
    ]

    for section in required_sections:
        assert section in content, f"Missing required section in pyproject.toml: {section}"

    # Check for project name
    assert 'name = "streaming_agent"' in content


def test_requirements_txt_structure():
    """Test that requirements.txt has required dependencies."""
    base_path = Path(__file__).parent.parent
    requirements = base_path / "requirements.txt"

    assert requirements.exists()

    content = requirements.read_text()

    # Check for required dependencies
    required_deps = [
        "google-genai",
        "pytest"
    ]

    for dep in required_deps:
        assert dep in content, f"Missing required dependency in requirements.txt: {dep}"


def test_makefile_structure():
    """Test that Makefile has required targets."""
    base_path = Path(__file__).parent.parent
    makefile = base_path / "Makefile"

    assert makefile.exists()

    content = makefile.read_text()

    # Check for required targets
    required_targets = [
        ".PHONY: setup dev test demo clean help",
        "setup:",
        "dev:",
        "test:",
        "demo:",
        "clean:"
    ]

    for target in required_targets:
        assert target in content, f"Missing required target in Makefile: {target}"


def test_agent_file_structure():
    """Test that agent.py has required structure."""
    base_path = Path(__file__).parent.parent
    agent_file = base_path / "streaming_agent" / "agent.py"

    assert agent_file.exists()

    content = agent_file.read_text()

    # Check for required exports/functions
    required_elements = [
        "root_agent",
        "create_streaming_agent",
        "stream_agent_response",
        "get_complete_response",
        "create_demo_session"
    ]

    for element in required_elements:
        assert element in content, f"Missing required element in agent.py: {element}"


def test_init_file_structure():
    """Test that __init__.py has required exports."""
    base_path = Path(__file__).parent.parent
    init_file = base_path / "streaming_agent" / "__init__.py"

    assert init_file.exists()

    content = init_file.read_text()

    # Check for required exports
    required_exports = [
        "root_agent",
        "stream_agent_response",
        "get_complete_response",
        "create_demo_session"
    ]

    for export in required_exports:
        assert export in content, f"Missing required export in __init__.py: {export}"


def test_no_env_file():
    """Test that .env file does not exist (security check)."""
    base_path = Path(__file__).parent.parent
    env_file = base_path / "streaming_agent" / ".env"

    # .env should NOT exist - only .env.example should
    assert not env_file.exists(), ".env file should not exist - only .env.example should be present"


def test_readme_exists():
    """Test that README.md exists."""
    base_path = Path(__file__).parent.parent
    readme = base_path / "README.md"

    # README is optional but recommended
    if readme.exists():
        assert readme.is_file()
        content = readme.read_text()
        assert len(content.strip()) > 0, "README.md should not be empty"


def test_test_files_executable():
    """Test that test files are properly structured."""
    base_path = Path(__file__).parent

    test_files = [
        "test_agent.py",
        "test_imports.py",
        "test_structure.py"
    ]

    for test_file in test_files:
        file_path = base_path / test_file
        assert file_path.exists()

        content = file_path.read_text()

        # Check for basic test structure
        assert "def test_" in content or "class Test" in content, f"Test file {test_file} lacks test structure"