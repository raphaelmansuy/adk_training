"""
Comprehensive tests for Tutorial 08: Personal Learning Tutor

Tests state management, memory operations, and agent functionality.
"""

import pytest
from unittest.mock import Mock
from personal_tutor.agent import (
    root_agent,
    set_user_preferences,
    record_topic_completion,
    get_user_progress,
    start_learning_session,
    calculate_quiz_grade,
    search_past_lessons
)


class TestStateManagement:
    """Test state management functionality."""

    def test_set_user_preferences_basic(self):
        """Test setting basic user preferences."""
        mock_context = Mock()
        mock_context.state = {}

        result = set_user_preferences("en", "intermediate", mock_context)

        assert result['status'] == 'success'
        assert result['message'] == 'Preferences saved: en, intermediate level'
        assert mock_context.state['user:language'] == 'en'
        assert mock_context.state['user:difficulty_level'] == 'intermediate'

    def test_set_user_preferences_overwrite(self):
        """Test overwriting existing preferences."""
        mock_context = Mock()
        mock_context.state = {
            'user:language': 'es',
            'user:difficulty_level': 'beginner'
        }

        result = set_user_preferences("fr", "advanced", mock_context)

        assert result['status'] == 'success'
        assert mock_context.state['user:language'] == 'fr'
        assert mock_context.state['user:difficulty_level'] == 'advanced'

    def test_record_topic_completion_new_topic(self):
        """Test recording completion of a new topic."""
        mock_context = Mock()
        mock_context.state = {}

        result = record_topic_completion("Python Basics", 85, mock_context)

        assert result['status'] == 'success'
        assert result['topics_count'] == 1
        assert result['message'] == 'Recorded: Python Basics with score 85/100'
        assert mock_context.state['user:topics_covered'] == ['Python Basics']
        assert mock_context.state['user:quiz_scores'] == {'Python Basics': 85}

    def test_record_topic_completion_existing_topic(self):
        """Test updating score for existing topic."""
        mock_context = Mock()
        mock_context.state = {
            'user:topics_covered': ['Python Basics'],
            'user:quiz_scores': {'Python Basics': 75}
        }

        result = record_topic_completion("Python Basics", 90, mock_context)

        assert result['status'] == 'success'
        assert result['topics_count'] == 1  # Should not add duplicate
        assert mock_context.state['user:topics_covered'] == ['Python Basics']
        assert mock_context.state['user:quiz_scores'] == {'Python Basics': 90}

    def test_get_user_progress_empty(self):
        """Test getting progress for new user."""
        mock_context = Mock()
        mock_context.state = {}

        result = get_user_progress(mock_context)

        assert result['status'] == 'success'
        assert result['language'] == 'en'  # default
        assert result['difficulty_level'] == 'beginner'  # default
        assert result['topics_completed'] == 0
        assert result['topics'] == []
        assert result['average_quiz_score'] == 0
        assert result['all_scores'] == {}

    def test_get_user_progress_with_data(self):
        """Test getting progress with existing data."""
        mock_context = Mock()
        mock_context.state = {
            'user:language': 'es',
            'user:difficulty_level': 'advanced',
            'user:topics_covered': ['Python', 'JavaScript'],
            'user:quiz_scores': {'Python': 90, 'JavaScript': 85}
        }

        result = get_user_progress(mock_context)

        assert result['status'] == 'success'
        assert result['language'] == 'es'
        assert result['difficulty_level'] == 'advanced'
        assert result['topics_completed'] == 2
        assert result['topics'] == ['Python', 'JavaScript']
        assert result['average_quiz_score'] == 87.5
        assert result['all_scores'] == {'Python': 90, 'JavaScript': 85}


class TestSessionManagement:
    """Test session-level state management."""

    def test_start_learning_session_basic(self):
        """Test starting a basic learning session."""
        mock_context = Mock()
        mock_context.state = {}

        result = start_learning_session("Data Structures", mock_context)

        assert result['status'] == 'success'
        assert result['topic'] == 'Data Structures'
        assert result['difficulty_level'] == 'beginner'  # default
        assert result['message'] == ('Started learning session: Data Structures at '
                                     'beginner level')
        assert mock_context.state['current_topic'] == 'Data Structures'
        assert mock_context.state['session_start_time'] == 'now'

    def test_start_learning_session_with_preferences(self):
        """Test starting session with user preferences."""
        mock_context = Mock()
        mock_context.state = {
            'user:difficulty_level': 'advanced'
        }

        result = start_learning_session("Algorithms", mock_context)

        assert result['status'] == 'success'
        assert result['difficulty_level'] == 'advanced'
        assert result['message'] == ('Started learning session: Algorithms at '
                                     'advanced level')


class TestTemporaryState:
    """Test temporary (temp:) state management."""

    def test_calculate_quiz_grade_perfect_score(self):
        """Test calculating grade for perfect score."""
        mock_context = Mock()
        mock_context.state = {}

        result = calculate_quiz_grade(10, 10, mock_context)

        assert result['status'] == 'success'
        assert result['score'] == '10/10'
        assert result['percentage'] == 100.0
        assert result['grade'] == 'A'
        assert result['message'] == 'Quiz grade: A (100.0%)'
        assert mock_context.state['temp:raw_score'] == 10
        assert mock_context.state['temp:quiz_percentage'] == 100.0

    def test_calculate_quiz_grade_failing_score(self):
        """Test calculating grade for failing score."""
        mock_context = Mock()
        mock_context.state = {}

        result = calculate_quiz_grade(3, 10, mock_context)

        assert result['status'] == 'success'
        assert result['score'] == '3/10'
        assert result['percentage'] == 30.0
        assert result['grade'] == 'F'
        assert result['message'] == 'Quiz grade: F (30.0%)'
        assert mock_context.state['temp:raw_score'] == 3
        assert mock_context.state['temp:quiz_percentage'] == 30.0

    def test_calculate_quiz_grade_all_grades(self):
        """Test all grade boundaries."""
        test_cases = [
            (9, 10, 90.0, 'A'),
            (8, 10, 80.0, 'B'),
            (7, 10, 70.0, 'C'),
            (6, 10, 60.0, 'D'),
            (5, 10, 50.0, 'F'),
        ]

        for correct, total, expected_pct, expected_grade in test_cases:
            mock_context = Mock()
            mock_context.state = {}

            result = calculate_quiz_grade(correct, total, mock_context)

            assert result['percentage'] == expected_pct
            assert result['grade'] == expected_grade


class TestMemoryOperations:
    """Test memory search functionality."""

    def test_search_past_lessons_found(self):
        """Test searching for lessons that exist."""
        mock_context = Mock()
        mock_context.state = {
            'user:topics_covered': ['Python Functions', 'JavaScript Arrays',
                                    'Data Structures']
        }

        result = search_past_lessons("python", mock_context)

        assert result['status'] == 'success'
        assert result['found'] is True
        assert result['relevant_topics'] == ['Python Functions']
        assert result['message'] == 'Found 1 past sessions related to "python"'

    def test_search_past_lessons_multiple_found(self):
        """Test searching for lessons with multiple matches."""
        mock_context = Mock()
        mock_context.state = {
            'user:topics_covered': ['Python Basics', 'Python Functions', 'JavaScript']
        }

        result = search_past_lessons("python", mock_context)

        assert result['status'] == 'success'
        assert result['found'] is True
        assert len(result['relevant_topics']) == 2
        assert 'Python Basics' in result['relevant_topics']
        assert 'Python Functions' in result['relevant_topics']

    def test_search_past_lessons_not_found(self):
        """Test searching for lessons that don't exist."""
        mock_context = Mock()
        mock_context.state = {
            'user:topics_covered': ['JavaScript', 'HTML', 'CSS']
        }

        result = search_past_lessons("python", mock_context)

        assert result['status'] == 'success'
        assert result['found'] is False
        assert result['message'] == 'No past sessions found for "python"'

    def test_search_past_lessons_empty_topics(self):
        """Test searching with no topics covered."""
        mock_context = Mock()
        mock_context.state = {}

        result = search_past_lessons("anything", mock_context)

        assert result['status'] == 'success'
        assert result['found'] is False


class TestAgentConfiguration:
    """Test agent configuration and structure."""

    def test_root_agent_configuration(self):
        """Test that root agent is properly configured."""
        assert root_agent.name == "personal_tutor"
        assert root_agent.model == "gemini-2.0-flash"
        assert root_agent.output_key == "last_tutor_response"

    def test_root_agent_has_description(self):
        """Test that agent has proper description."""
        assert root_agent.description is not None
        assert "personal learning tutor" in root_agent.description.lower()
        assert "progress" in root_agent.description.lower()

    def test_root_agent_has_instruction(self):
        """Test that agent has comprehensive instruction."""
        assert root_agent.instruction is not None
        assert "personalized learning tutor" in root_agent.instruction
        assert "user: prefix" in root_agent.instruction
        assert "temp: prefix" in root_agent.instruction

    def test_root_agent_has_all_tools(self):
        """Test that agent has all required tools."""
        tool_functions = [tool.__name__ if hasattr(tool, '__name__') else str(tool)
                          for tool in root_agent.tools]

        expected_tools = [
            'set_user_preferences',
            'record_topic_completion',
            'get_user_progress',
            'start_learning_session',
            'calculate_quiz_grade',
            'search_past_lessons'
        ]

        for expected_tool in expected_tools:
            assert any(expected_tool in tool for tool in tool_functions), \
                f"Missing tool: {expected_tool}"


class TestIntegrationScenarios:
    """Test complete user workflows."""

    def test_complete_learning_workflow(self):
        """Test a complete learning session workflow."""
        mock_context = Mock()
        mock_context.state = {}

        # 1. Set preferences
        result1 = set_user_preferences("en", "intermediate", mock_context)
        assert result1['status'] == 'success'
        assert mock_context.state['user:language'] == 'en'
        assert mock_context.state['user:difficulty_level'] == 'intermediate'

        # 2. Start learning session
        result2 = start_learning_session("Python Classes", mock_context)
        assert result2['status'] == 'success'
        assert mock_context.state['current_topic'] == 'Python Classes'
        assert result2['difficulty_level'] == 'intermediate'  # Uses preference

        # 3. Complete quiz
        result3 = calculate_quiz_grade(8, 10, mock_context)
        assert result3['status'] == 'success'
        assert result3['grade'] == 'B'
        assert mock_context.state['temp:quiz_percentage'] == 80.0

        # 4. Record completion
        result4 = record_topic_completion("Python Classes", 80, mock_context)
        assert result4['status'] == 'success'
        assert mock_context.state['user:topics_covered'] == ['Python Classes']
        assert mock_context.state['user:quiz_scores'] == {'Python Classes': 80}

        # 5. Check progress
        result5 = get_user_progress(mock_context)
        assert result5['status'] == 'success'
        assert result5['topics_completed'] == 1
        assert result5['average_quiz_score'] == 80.0

        # 6. Search past lessons
        result6 = search_past_lessons("classes", mock_context)
        assert result6['status'] == 'success'
        assert result6['found'] is True
        assert result6['relevant_topics'] == ['Python Classes']

    def test_multiple_topics_workflow(self):
        """Test workflow with multiple topics."""
        mock_context = Mock()
        mock_context.state = {}

        # Learn multiple topics
        topics_scores = [
            ("Python Basics", 90),
            ("Python Functions", 85),
            ("Python Classes", 88)
        ]

        for topic, score in topics_scores:
            # Start session
            start_learning_session(topic, mock_context)

            # Record completion
            record_topic_completion(topic, score, mock_context)

        # Check final progress
        result = get_user_progress(mock_context)
        assert result['topics_completed'] == 3
        assert result['average_quiz_score'] == 87.7  # (90+85+88)/3
        assert len(result['topics']) == 3
        assert len(result['all_scores']) == 3

        # Search should find relevant topics
        search_result = search_past_lessons("python", mock_context)
        assert search_result['found'] is True
        assert len(search_result['relevant_topics']) == 3


if __name__ == "__main__":
    pytest.main([__file__])
