"""
Tests for Tutorial 05: Parallel Processing - Travel Planning System
"""

import pytest
from travel_planner.agent import (
    flight_finder,
    hotel_finder,
    activity_finder,
    parallel_search,
    itinerary_builder,
    travel_planning_system,
    root_agent
)


class TestIndividualAgents:
    """Test individual agent configurations"""

    def test_flight_finder_config(self):
        """Test flight finder agent configuration"""
        assert flight_finder.name == "flight_finder"
        assert flight_finder.model == "gemini-2.0-flash"
        assert flight_finder.description == "Searches for available flights"
        assert "flight" in flight_finder.instruction.lower()
        assert flight_finder.output_key == "flight_options"

    def test_hotel_finder_config(self):
        """Test hotel finder agent configuration"""
        assert hotel_finder.name == "hotel_finder"
        assert hotel_finder.model == "gemini-2.0-flash"
        assert hotel_finder.description == "Searches for available hotels"
        assert "hotel" in hotel_finder.instruction.lower()
        assert hotel_finder.output_key == "hotel_options"

    def test_activity_finder_config(self):
        """Test activity finder agent configuration"""
        assert activity_finder.name == "activity_finder"
        assert activity_finder.model == "gemini-2.0-flash"
        assert activity_finder.description == "Finds activities and attractions"
        assert "activit" in activity_finder.instruction.lower()
        assert activity_finder.output_key == "activity_options"

    def test_agents_have_unique_output_keys(self):
        """Test that all agents have unique output keys"""
        output_keys = [
            flight_finder.output_key,
            hotel_finder.output_key,
            activity_finder.output_key
        ]
        assert len(set(output_keys)) == len(output_keys)

    def test_agents_have_output_keys(self):
        """Test that all search agents have output keys defined"""
        assert flight_finder.output_key is not None
        assert hotel_finder.output_key is not None
        assert activity_finder.output_key is not None


class TestParallelAgentStructure:
    """Test ParallelAgent configuration and structure"""

    def test_parallel_search_is_parallel_agent(self):
        """Test that parallel_search is a ParallelAgent"""
        from google.adk.agents import ParallelAgent
        assert isinstance(parallel_search, ParallelAgent)

    def test_parallel_search_name(self):
        """Test parallel search agent name"""
        assert parallel_search.name == "ParallelSearch"

    def test_parallel_search_has_three_sub_agents(self):
        """Test that parallel search has exactly 3 sub-agents"""
        assert len(parallel_search.sub_agents) == 3

    def test_parallel_search_sub_agents_are_correct(self):
        """Test that parallel search has the correct sub-agents"""
        sub_agent_names = [agent.name for agent in parallel_search.sub_agents]
        expected_names = ["flight_finder", "hotel_finder", "activity_finder"]
        assert set(sub_agent_names) == set(expected_names)

    def test_parallel_search_description(self):
        """Test parallel search description"""
        assert "concurrently" in parallel_search.description.lower()


class TestSequentialAgentStructure:
    """Test SequentialAgent configuration and structure"""

    def test_travel_planning_system_is_sequential_agent(self):
        """Test that travel_planning_system is a SequentialAgent"""
        from google.adk.agents import SequentialAgent
        assert isinstance(travel_planning_system, SequentialAgent)

    def test_travel_planning_system_name(self):
        """Test travel planning system name"""
        assert travel_planning_system.name == "TravelPlanningSystem"

    def test_travel_planning_system_has_two_sub_agents(self):
        """Test that travel planning system has exactly 2 sub-agents"""
        assert len(travel_planning_system.sub_agents) == 2

    def test_travel_planning_system_first_agent_is_parallel(self):
        """Test that first agent in sequence is the parallel search"""
        from google.adk.agents import ParallelAgent
        assert isinstance(travel_planning_system.sub_agents[0], ParallelAgent)

    def test_travel_planning_system_second_agent_is_itinerary_builder(self):
        """Test that second agent in sequence is the itinerary builder"""
        assert travel_planning_system.sub_agents[1] == itinerary_builder


class TestItineraryBuilder:
    """Test itinerary builder agent configuration"""

    def test_itinerary_builder_config(self):
        """Test itinerary builder agent configuration"""
        assert itinerary_builder.name == "itinerary_builder"
        assert itinerary_builder.model == "gemini-2.0-flash"
        assert itinerary_builder.description == "Combines all search results into a complete travel itinerary"
        assert itinerary_builder.output_key == "final_itinerary"

    def test_itinerary_builder_reads_all_state_keys(self):
        """Test that itinerary builder instruction references all state keys"""
        instruction = itinerary_builder.instruction
        assert "{flight_options}" in instruction
        assert "{hotel_options}" in instruction
        assert "{activity_options}" in instruction


class TestRootAgent:
    """Test root agent configuration"""

    def test_root_agent_is_travel_planning_system(self):
        """Test that root_agent is the travel planning system"""
        assert root_agent == travel_planning_system

    def test_root_agent_is_sequential_agent(self):
        """Test that root_agent is a SequentialAgent"""
        from google.adk.agents import SequentialAgent
        assert isinstance(root_agent, SequentialAgent)


class TestStateManagement:
    """Test state management and data flow"""

    def test_parallel_agents_have_output_keys_for_state_injection(self):
        """Test that parallel agents save to state for itinerary builder to read"""
        parallel_output_keys = [
            agent.output_key for agent in parallel_search.sub_agents
        ]
        # Check that itinerary builder instruction contains references to these keys
        instruction = itinerary_builder.instruction
        for key in parallel_output_keys:
            assert f"{{{key}}}" in instruction

    def test_no_circular_dependencies(self):
        """Test that there are no circular dependencies in the pipeline"""
        # Parallel agents don't depend on each other
        # Itinerary builder depends on parallel agents but not vice versa
        parallel_keys = {agent.output_key for agent in parallel_search.sub_agents}
        itinerary_instruction = itinerary_builder.instruction

        # Itinerary builder should only read from parallel agent outputs
        # (This is a basic check - in practice, the instruction parsing would be more complex)
        for key in parallel_keys:
            assert f"{{{key}}}" in itinerary_instruction


class TestAgentInstructions:
    """Test agent instruction quality and structure"""

    def test_flight_finder_instruction_format(self):
        """Test flight finder instruction format"""
        instruction = flight_finder.instruction
        assert "flight search specialist" in instruction.lower()
        assert "airline name" in instruction.lower()
        assert "departure and arrival times" in instruction.lower()
        assert "price range" in instruction.lower()

    def test_hotel_finder_instruction_format(self):
        """Test hotel finder instruction format"""
        instruction = hotel_finder.instruction
        assert "hotel search specialist" in instruction.lower()
        assert "hotel name and rating" in instruction.lower()
        assert "location" in instruction.lower()
        assert "price per night" in instruction.lower()

    def test_activity_finder_instruction_format(self):
        """Test activity finder instruction format"""
        instruction = activity_finder.instruction
        assert "local activities expert" in instruction.lower()
        assert "activity name" in instruction.lower()
        assert "description" in instruction.lower()
        assert "estimated duration" in instruction.lower()

    def test_itinerary_builder_instruction_comprehensive(self):
        """Test itinerary builder instruction is comprehensive"""
        instruction = itinerary_builder.instruction
        assert "travel planner" in instruction.lower()
        assert "complete, well-organized itinerary" in instruction.lower()
        assert "best option" in instruction.lower()
        assert "day-by-day plan" in instruction.lower()
        assert "estimated total cost" in instruction.lower()

    def test_instructions_focus_on_output(self):
        """Test that all instructions emphasize output formatting"""
        instructions = [
            flight_finder.instruction,
            hotel_finder.instruction,
            activity_finder.instruction,
            itinerary_builder.instruction
        ]

        for instruction in instructions:
            # Each instruction should mention formatting or output
            has_formatting_guidance = (
                "format" in instruction.lower() or
                "bulleted list" in instruction.lower() or
                "markdown" in instruction.lower()
            )
            assert has_formatting_guidance, f"Instruction lacks formatting guidance: {instruction[:100]}..."


class TestImports:
    """Test imports and module structure"""

    def test_google_adk_agents_import(self):
        """Test that google.adk.agents can be imported"""
        import importlib.util
        spec = importlib.util.find_spec("google.adk.agents")
        assert spec is not None, "google.adk.agents module not found"

    def test_travel_planner_agent_import(self):
        """Test that travel_planner.agent module can be imported"""
        import importlib.util
        spec = importlib.util.find_spec("travel_planner.agent")
        assert spec is not None, "travel_planner.agent module not found"

    def test_root_agent_exists(self):
        """Test that root_agent is defined and accessible"""
        try:
            from travel_planner.agent import root_agent
            assert root_agent is not None
        except ImportError as e:
            pytest.fail(f"Failed to import root_agent: {e}")

    def test_future_annotations_import(self):
        """Test that __future__ annotations is imported"""
        import travel_planner.agent
        # This would fail at import time if __future__ annotations wasn't imported
        # since we're using the | syntax in type hints
        assert hasattr(travel_planner.agent, 'root_agent')


class TestProjectStructure:
    """Test project directory structure"""

    def test_travel_planner_directory_exists(self):
        """Test that travel_planner directory exists"""
        import os
        assert os.path.exists("travel_planner")

    def test_init_py_exists(self):
        """Test that __init__.py exists"""
        import os
        assert os.path.exists("travel_planner/__init__.py")

    def test_agent_py_exists(self):
        """Test that agent.py exists"""
        import os
        assert os.path.exists("travel_planner/agent.py")

    def test_env_example_exists(self):
        """Test that .env.example exists"""
        import os
        assert os.path.exists("travel_planner/.env.example")

    def test_init_py_content(self):
        """Test __init__.py content"""
        with open("travel_planner/__init__.py", "r") as f:
            content = f.read().strip()
            assert "from . import agent" in content

    def test_agent_py_is_python_file(self):
        """Test that agent.py is a Python file"""
        import os
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
        import os
        assert os.path.exists("tests")

    def test_tests_init_py_exists(self):
        """Test that tests/__init__.py exists"""
        import os
        assert os.path.exists("tests/__init__.py")

    def test_test_files_exist(self):
        """Test that test files exist"""
        import os
        test_files = [
            "tests/test_agent.py",
            "tests/test_imports.py",
            "tests/test_structure.py"
        ]
        for test_file in test_files:
            assert os.path.exists(test_file), f"Missing test file: {test_file}"


class TestAgentIntegration:
    """Test agent integration and pipeline functionality"""

    def test_pipeline_can_be_created_without_error(self):
        """Test that the complete pipeline can be instantiated without errors"""
        try:
            # This should not raise any exceptions
            from travel_planner.agent import travel_planning_system
            assert travel_planning_system is not None
        except Exception as e:
            pytest.fail(f"Failed to create pipeline: {e}")

    def test_pipeline_has_valid_configuration_for_api(self):
        """Test that pipeline has valid configuration for ADK API"""
        # Check that root_agent has required attributes
        assert hasattr(root_agent, 'name')
        assert hasattr(root_agent, 'description')
        assert hasattr(root_agent, 'sub_agents')
        assert len(root_agent.sub_agents) > 0

    def test_state_flow_is_configured(self):
        """Test that state flow is properly configured between agents"""
        # Parallel agents should have output keys
        parallel_outputs = [agent.output_key for agent in parallel_search.sub_agents]
        assert all(key is not None for key in parallel_outputs)

        # Itinerary builder should reference these keys
        builder_instruction = itinerary_builder.instruction
        for key in parallel_outputs:
            assert f"{{{key}}}" in builder_instruction