"""
Structure tests for Tutorial 05: Parallel Processing
"""

import os


class TestProjectStructure:
    """Test project directory structure"""

    def test_travel_planner_directory_exists(self):
        """Test that travel_planner directory exists"""
        assert os.path.exists("travel_planner")

    def test_init_py_exists(self):
        """Test that __init__.py exists"""
        assert os.path.exists("travel_planner/__init__.py")

    def test_agent_py_exists(self):
        """Test that agent.py exists"""
        assert os.path.exists("travel_planner/agent.py")

    def test_env_example_exists(self):
        """Test that .env.example exists"""
        assert os.path.exists("travel_planner/.env.example")

    def test_init_py_content(self):
        """Test __init__.py content"""
        with open("travel_planner/__init__.py", "r") as f:
            content = f.read().strip()
            assert "from . import agent" in content

    def test_agent_py_is_python_file(self):
        """Test that agent.py is a Python file"""
        import travel_planner.agent
        assert os.path.isfile("travel_planner/agent.py")
        assert travel_planner.agent.__file__.endswith("agent.py")

    def test_env_example_content(self):
        """Test .env.example content"""
        with open("travel_planner/.env.example", "r") as f:
            content = f.read()
            assert "GOOGLE_GENAI_USE_VERTEXAI=FALSE" in content
            assert "GOOGLE_API_KEY=" in content


class TestTestStructure:
    """Test test directory structure"""

    def test_tests_directory_exists(self):
        """Test that tests directory exists"""
        assert os.path.exists("tests")

    def test_tests_init_py_exists(self):
        """Test that tests/__init__.py exists"""
        assert os.path.exists("tests/__init__.py")

    def test_test_files_exist(self):
        """Test that test files exist"""
        test_files = [
            "tests/test_agent.py",
            "tests/test_imports.py",
            "tests/test_structure.py"
        ]
        for test_file in test_files:
            assert os.path.exists(test_file), f"Missing test file: {test_file}"