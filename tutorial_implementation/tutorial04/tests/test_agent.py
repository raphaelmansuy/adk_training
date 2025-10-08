"""
Tests for Tutorial 04: Sequential Workflows - Blog Creation Pipeline

Tests cover:
- Agent configuration and imports
- SequentialAgent pipeline structure
- Individual agent functionality
- State management and data flow
- Integration testing
"""

import pytest

from blog_pipeline.agent import (
    root_agent,
    research_agent,
    writer_agent,
    editor_agent,
    formatter_agent
)
from google.adk.agents import SequentialAgent, Agent


class TestAgentConfiguration:
    """Test agent configuration and basic setup"""

    def test_root_agent_import(self):
        """Test root_agent can be imported"""
        assert root_agent is not None

    def test_root_agent_is_sequential_agent(self):
        """Test root_agent is a SequentialAgent instance"""
        assert isinstance(root_agent, SequentialAgent)

    def test_pipeline_name(self):
        """Test pipeline has correct name"""
        assert root_agent.name == "BlogCreationPipeline"

    def test_pipeline_description(self):
        """Test pipeline has description"""
        assert "blog post creation" in root_agent.description.lower()

    def test_pipeline_has_sub_agents(self):
        """Test pipeline has 4 sub-agents"""
        assert hasattr(root_agent, 'sub_agents')
        assert len(root_agent.sub_agents) == 4

    def test_sub_agents_are_agents(self):
        """Test all sub-agents are Agent instances"""
        for agent in root_agent.sub_agents:
            assert isinstance(agent, Agent)


class TestIndividualAgents:
    """Test individual agent configurations"""

    def test_research_agent_config(self):
        """Test research agent configuration"""
        assert research_agent.name == "researcher"
        assert research_agent.model == "gemini-2.0-flash"
        assert research_agent.output_key == "research_findings"
        assert "research" in research_agent.instruction.lower()

    def test_writer_agent_config(self):
        """Test writer agent configuration"""
        assert writer_agent.name == "writer"
        assert writer_agent.model == "gemini-2.0-flash"
        assert writer_agent.output_key == "draft_post"
        assert "{research_findings}" in writer_agent.instruction

    def test_editor_agent_config(self):
        """Test editor agent configuration"""
        assert editor_agent.name == "editor"
        assert editor_agent.model == "gemini-2.0-flash"
        assert editor_agent.output_key == "editorial_feedback"
        assert "{draft_post}" in editor_agent.instruction

    def test_formatter_agent_config(self):
        """Test formatter agent configuration"""
        assert formatter_agent.name == "formatter"
        assert formatter_agent.model == "gemini-2.0-flash"
        assert formatter_agent.output_key == "final_post"
        assert "{draft_post}" in formatter_agent.instruction
        assert "{editorial_feedback}" in formatter_agent.instruction

    def test_agents_have_unique_output_keys(self):
        """Test all agents have unique output keys"""
        output_keys = [agent.output_key for agent in root_agent.sub_agents]
        assert len(output_keys) == len(set(output_keys))  # All unique

    def test_agents_have_output_keys(self):
        """Test all agents have output_key defined"""
        for agent in root_agent.sub_agents:
            assert hasattr(agent, 'output_key')
            assert agent.output_key is not None
            assert isinstance(agent.output_key, str)


class TestSequentialAgentStructure:
    """Test SequentialAgent pipeline structure"""

    def test_pipeline_execution_order(self):
        """Test agents are in correct execution order"""
        agents = root_agent.sub_agents
        assert agents[0].name == "researcher"
        assert agents[1].name == "writer"
        assert agents[2].name == "editor"
        assert agents[3].name == "formatter"

    def test_pipeline_is_deterministic(self):
        """Test pipeline always executes in same order"""
        # SequentialAgent should always execute in defined order
        agents = root_agent.sub_agents
        expected_order = ["researcher", "writer", "editor", "formatter"]
        actual_order = [agent.name for agent in agents]
        assert actual_order == expected_order


class TestStateManagement:
    """Test state management and data flow"""

    def test_state_key_injection_research_to_writer(self):
        """Test research findings flow to writer"""
        assert "{research_findings}" in writer_agent.instruction

    def test_state_key_injection_writer_to_editor(self):
        """Test draft post flow to editor"""
        assert "{draft_post}" in editor_agent.instruction

    def test_state_key_injection_multiple_to_formatter(self):
        """Test both draft and feedback flow to formatter"""
        assert "{draft_post}" in formatter_agent.instruction
        assert "{editorial_feedback}" in formatter_agent.instruction

    def test_no_circular_dependencies(self):
        """Test no agent reads its own output key"""
        for agent in root_agent.sub_agents:
            # Agent should not reference its own output key
            assert f"{{{agent.output_key}}}" not in agent.instruction


class TestAgentInstructions:
    """Test agent instruction quality"""

    def test_research_instruction_format(self):
        """Test research agent asks for bulleted list"""
        instruction = research_agent.instruction
        assert "bulleted list" in instruction.lower()
        assert "•" in instruction

    def test_writer_instruction_creativity(self):
        """Test writer agent focuses on engaging content"""
        instruction = writer_agent.instruction
        assert "engaging" in instruction.lower()
        assert "conversational" in instruction.lower()

    def test_editor_instruction_feedback(self):
        """Test editor agent provides constructive feedback"""
        instruction = editor_agent.instruction
        assert "constructive feedback" in instruction.lower()
        assert "improvements" in instruction.lower()

    def test_formatter_instruction_markdown(self):
        """Test formatter agent creates markdown output"""
        instruction = formatter_agent.instruction
        assert "markdown" in instruction.lower()
        assert "#" in instruction  # Heading syntax

    def test_instructions_focus_on_output(self):
        """Test all instructions emphasize output format"""
        for agent in root_agent.sub_agents:
            instruction = agent.instruction
            assert "output only" in instruction.lower() or "output only" in instruction.lower()


class TestImports:
    """Test import functionality"""

    def test_google_adk_agents_import(self):
        """Test google.adk.agents import works"""
        from google.adk.agents import Agent, SequentialAgent
        assert Agent is not None
        assert SequentialAgent is not None

    def test_blog_pipeline_agent_import(self):
        """Test blog_pipeline.agent import works"""
        from blog_pipeline.agent import root_agent
        assert root_agent is not None

    def test_root_agent_exists(self):
        """Test root_agent is properly defined"""
        assert root_agent is not None
        assert hasattr(root_agent, 'name')
        assert hasattr(root_agent, 'sub_agents')

    def test_future_annotations_import(self):
        """Test __future__ annotations import works"""
        import __future__
        assert hasattr(__future__, 'annotations')


class TestProjectStructure:
    """Test project structure and file organization"""

    def test_blog_pipeline_directory_exists(self):
        """Test blog_pipeline directory exists"""
        import os
        assert os.path.exists("blog_pipeline")

    def test_init_py_exists(self):
        """Test __init__.py exists"""
        import os
        assert os.path.exists("blog_pipeline/__init__.py")

    def test_agent_py_exists(self):
        """Test agent.py exists"""
        import os
        assert os.path.exists("blog_pipeline/agent.py")

    def test_env_example_exists(self):
        """Test .env.example exists"""
        import os
        assert os.path.exists("blog_pipeline/.env.example")

    def test_init_py_content(self):
        """Test __init__.py has correct content"""
        with open("blog_pipeline/__init__.py", "r") as f:
            content = f.read()
            assert "from .agent import root_agent" in content
            assert "__all__" in content

    def test_agent_py_is_python_file(self):
        """Test agent.py is a valid Python file"""
        with open("blog_pipeline/agent.py", "r") as f:
            content = f.read()
            assert "from __future__ import annotations" in content
            assert "SequentialAgent" in content

    def test_env_example_content(self):
        """Test .env.example has required variables"""
        with open("blog_pipeline/.env.example", "r") as f:
            content = f.read()
            assert "GOOGLE_GENAI_USE_VERTEXAI" in content
            assert "GOOGLE_API_KEY" in content


class TestTestStructure:
    """Test test file organization"""

    def test_tests_directory_exists(self):
        """Test tests directory exists"""
        import os
        assert os.path.exists("tests")

    def test_tests_init_py_exists(self):
        """Test tests/__init__.py exists"""
        import os
        assert os.path.exists("tests/__init__.py")

    def test_test_files_exist(self):
        """Test test files exist"""
        import os
        test_files = [f for f in os.listdir("tests") if f.startswith("test_")]
        assert len(test_files) > 0


@pytest.mark.integration
class TestAgentIntegration:
    """Integration tests that require API access"""

    def test_pipeline_can_be_created_without_error(self):
        """Test that pipeline can be created without throwing exceptions"""
        try:
            # Just accessing root_agent should not raise errors
            agent = root_agent
            assert agent is not None
            assert agent.name == "BlogCreationPipeline"
            assert len(agent.sub_agents) == 4
        except Exception as e:
            pytest.fail(f"Pipeline creation failed: {e}")

    def test_pipeline_has_valid_configuration_for_api(self):
        """Test pipeline has all required configuration for API usage"""
        assert root_agent.name is not None
        assert root_agent.description is not None
        assert hasattr(root_agent, 'sub_agents')
        assert len(root_agent.sub_agents) > 0

        # Check that all sub-agents have required attributes
        for agent in root_agent.sub_agents:
            assert agent.name is not None
            assert agent.model is not None
            assert agent.instruction is not None
            assert agent.output_key is not None

    def test_state_flow_is_configured(self):
        """Test that state flow between agents is properly configured"""
        agents = root_agent.sub_agents

        # Research → Writer
        assert "{research_findings}" in agents[1].instruction  # writer reads research

        # Writer → Editor
        assert "{draft_post}" in agents[2].instruction  # editor reads draft

        # Writer + Editor → Formatter
        assert "{draft_post}" in agents[3].instruction  # formatter reads draft
        assert "{editorial_feedback}" in agents[3].instruction  # formatter reads feedback