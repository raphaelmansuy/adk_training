import pytest
from unittest.mock import Mock, patch
from essay_refiner.agent import (
    root_agent,
    essay_refinement_system,
    refinement_loop,
    initial_writer,
    critic,
    refiner,
    exit_loop
)


class TestIndividualAgents:
    """Test individual agent configurations and properties."""

    def test_root_agent_configuration(self):
        """Test that root_agent is properly configured."""
        assert root_agent.name == "EssayRefinementSystem"
        assert len(root_agent.sub_agents) == 2
        assert root_agent.sub_agents[0].name == "InitialWriter"
        assert root_agent.sub_agents[1].name == "RefinementLoop"

    def test_initial_writer_agent(self):
        """Test InitialWriter agent configuration."""
        assert initial_writer.name == "InitialWriter"
        assert initial_writer.model == "gemini-2.0-flash"
        assert initial_writer.output_key == "current_essay"
        assert "first draft" in initial_writer.instruction.lower()
        assert "3-4 paragraphs" in initial_writer.instruction

    def test_critic_agent(self):
        """Test Critic agent configuration."""
        assert critic.name == "Critic"
        assert critic.model == "gemini-2.0-flash"
        assert critic.output_key == "critique"
        assert "evaluation criteria" in critic.instruction.lower()
        assert "approved - essay is complete" in critic.instruction.lower()

    def test_refiner_agent(self):
        """Test Refiner agent configuration."""
        assert refiner.name == "Refiner"
        assert refiner.model == "gemini-2.0-flash"
        assert refiner.output_key == "current_essay"
        assert len(refiner.tools) == 1
        assert "exit_loop" in refiner.instruction.lower()
        assert "APPROVED - Essay is complete" in refiner.instruction

    def test_refinement_loop_agent(self):
        """Test LoopAgent configuration."""
        assert refinement_loop.name == "RefinementLoop"
        assert len(refinement_loop.sub_agents) == 2
        assert refinement_loop.max_iterations == 5
        assert refinement_loop.sub_agents[0].name == "Critic"
        assert refinement_loop.sub_agents[1].name == "Refiner"


class TestSequentialAgentStructure:
    """Test the overall SequentialAgent structure."""

    def test_essay_refinement_system_structure(self):
        """Test that the complete system has correct structure."""
        assert essay_refinement_system.name == "EssayRefinementSystem"
        assert len(essay_refinement_system.sub_agents) == 2

        # Phase 1: Initial writer
        phase1 = essay_refinement_system.sub_agents[0]
        assert phase1.name == "InitialWriter"

        # Phase 2: Refinement loop
        phase2 = essay_refinement_system.sub_agents[1]
        assert phase2.name == "RefinementLoop"
        assert hasattr(phase2, 'max_iterations')
        assert phase2.max_iterations == 5


class TestLoopAgentLogic:
    """Test LoopAgent-specific logic and termination conditions."""

    def test_loop_max_iterations(self):
        """Test that loop has proper safety limits."""
        assert refinement_loop.max_iterations == 5

    def test_exit_loop_tool_function(self):
        """Test the exit_loop tool function."""
        mock_context = Mock()
        mock_context.agent_name = "TestRefiner"

        # Call the exit_loop function
        result = exit_loop(mock_context)

        # Verify end_of_agent is set to True
        assert mock_context.actions.end_of_agent is True
        # Verify valid content dict returned (prevents generic error)
        expected_content = {"text": "Loop exited successfully. The agent has determined the task is complete."}
        assert result == expected_content

    @patch('builtins.print')
    def test_exit_loop_tool_print(self, mock_print):
        """Test that exit_loop prints the expected message."""
        mock_context = Mock()
        mock_context.agent_name = "TestRefiner"

        exit_loop(mock_context)

        mock_print.assert_called_once_with(
            "  [Exit Loop] Called by TestRefiner - Essay approved!"
        )


class TestStateManagement:
    """Test state key management and data flow."""

    def test_output_keys_consistency(self):
        """Test that output keys are used consistently for state management."""
        # Initial writer creates current_essay
        assert initial_writer.output_key == "current_essay"

        # Refiner overwrites current_essay (state versioning)
        assert refiner.output_key == "current_essay"

        # Critic creates critique
        assert critic.output_key == "critique"

    def test_state_key_usage_pattern(self):
        """Test the state overwriting pattern for iterative refinement."""
        # This pattern allows:
        # 1. Initial writer creates v1
        # 2. Refiner overwrites with v2, v3, etc.
        # 3. Critic always evaluates the latest version

        # Verify the pattern is implemented
        writer_key = initial_writer.output_key
        refiner_key = refiner.output_key

        assert writer_key == refiner_key == "current_essay"

        # Critic reads the current essay via template
        assert "{current_essay}" in critic.instruction
        assert "{critique}" in refiner.instruction


class TestAgentInstructions:
    """Test that agent instructions contain required elements."""

    def test_initial_writer_instruction_completeness(self):
        """Test that initial writer has complete instructions."""
        instr = initial_writer.instruction

        required_phrases = [
            "creative writer",
            "first draft",
            "3-4 paragraphs",
            "opening paragraph",
            "body paragraphs",
            "concluding paragraph",
            "output only the essay text"
        ]

        for phrase in required_phrases:
            assert phrase in instr.lower()

    def test_critic_instruction_completeness(self):
        """Test that critic has complete evaluation instructions."""
        instr = critic.instruction

        required_phrases = [
            "essay critic",
            "evaluation criteria",
            "clear thesis",
            "supporting arguments",
            "grammar and style",
            "approved - essay is complete",
            "specific, actionable improvements"
        ]

        for phrase in required_phrases:
            assert phrase in instr.lower()

    def test_refiner_instruction_completeness(self):
        """Test that refiner has complete improvement instructions."""
        instr = refiner.instruction

        required_phrases = [
            "essay editor",
            "exit_loop",
            "approved - essay is complete",
            "apply the suggested improvements",
            "output only the improved essay",
            "either call exit_loop or output improved essay"
        ]

        for phrase in required_phrases:
            assert phrase in instr.lower()


class TestToolIntegration:
    """Test tool integration and function calling."""

    def test_refiner_has_exit_tool(self):
        """Test that refiner agent has the exit_loop tool."""
        assert len(refiner.tools) == 1
        # The tool should be the exit_loop function
        assert refiner.tools[0] == exit_loop

    def test_exit_tool_context_handling(self):
        """Test that exit_loop properly handles ToolContext."""
        mock_context = Mock()
        mock_context.actions = Mock()

        exit_loop(mock_context)

        # Verify that end_of_agent is set
        assert mock_context.actions.end_of_agent is True


class TestSystemIntegration:
    """Test complete system integration and imports."""

    def test_all_agents_importable(self):
        """Test that all agents can be imported without errors."""
        # This test ensures the module loads correctly
        from essay_refiner.agent import (
            root_agent,
            essay_refinement_system,
            refinement_loop,
            initial_writer,
            critic,
            refiner,
            exit_loop
        )

        # Verify all are defined
        assert root_agent is not None
        assert essay_refinement_system is not None
        assert refinement_loop is not None
        assert initial_writer is not None
        assert critic is not None
        assert refiner is not None
        assert exit_loop is not None

    def test_agent_type_consistency(self):
        """Test that agents are of correct types."""
        from google.adk.agents import Agent, LoopAgent, SequentialAgent

        # Test agent types
        assert isinstance(initial_writer, Agent)
        assert isinstance(critic, Agent)
        assert isinstance(refiner, Agent)
        assert isinstance(refinement_loop, LoopAgent)
        assert isinstance(essay_refinement_system, SequentialAgent)
        assert isinstance(root_agent, SequentialAgent)

    def test_nested_agent_structure(self):
        """Test the nested agent structure is correct."""
        # Root agent contains sequential system
        assert root_agent == essay_refinement_system

        # Sequential system contains initial writer + loop
        assert len(essay_refinement_system.sub_agents) == 2
        assert essay_refinement_system.sub_agents[0] == initial_writer
        assert essay_refinement_system.sub_agents[1] == refinement_loop

        # Loop contains critic + refiner
        assert len(refinement_loop.sub_agents) == 2
        assert refinement_loop.sub_agents[0] == critic
        assert refinement_loop.sub_agents[1] == refiner


class TestConfigurationValidation:
    """Test configuration-specific validation."""

    def test_model_consistency(self):
        """Test that all agents use the same model."""
        expected_model = "gemini-2.0-flash"

        assert initial_writer.model == expected_model
        assert critic.model == expected_model
        assert refiner.model == expected_model

    def test_agent_descriptions_exist(self):
        """Test that all agents have descriptions."""
        assert initial_writer.description is not None
        assert critic.description is not None
        assert refiner.description is not None
        assert refinement_loop.description is not None
        assert essay_refinement_system.description is not None

        # Descriptions should be meaningful
        assert len(initial_writer.description) > 10
        assert len(critic.description) > 10
        assert len(refiner.description) > 10

    def test_agent_names_uniqueness(self):
        """Test that all agents have unique names."""
        names = [
            initial_writer.name,
            critic.name,
            refiner.name,
            refinement_loop.name,
            essay_refinement_system.name
        ]

        assert len(names) == len(set(names)), f"Duplicate names found: {names}"


if __name__ == "__main__":
    pytest.main([__file__])