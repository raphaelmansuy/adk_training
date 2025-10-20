"""Test suite for Pause/Resume Invocation Agent.

Tests agent configuration, tools, imports, and app setup.
"""

from pause_resume_agent import root_agent
from pause_resume_agent.agent import (
    process_data_chunk,
    validate_checkpoint,
    get_resumption_hint,
)
from app import app


class TestAgentConfiguration:
    """Test agent configuration and metadata."""

    def test_agent_name(self):
        """Test agent has correct name."""
        assert root_agent.name == "pause_resume_agent"

    def test_agent_model(self):
        """Test agent uses correct model."""
        assert root_agent.model == "gemini-2.0-flash"

    def test_agent_description(self):
        """Test agent has description."""
        assert root_agent.description is not None
        assert "pause" in root_agent.description.lower()
        assert "resume" in root_agent.description.lower()

    def test_agent_instruction(self):
        """Test agent has instruction."""
        assert root_agent.instruction is not None
        assert len(root_agent.instruction) > 0
        assert "checkpoint" in root_agent.instruction.lower()

    def test_agent_has_tools(self):
        """Test agent has tools configured."""
        assert root_agent.tools is not None
        assert len(root_agent.tools) == 3

    def test_agent_export(self):
        """Test agent is properly exported."""
        from pause_resume_agent import root_agent as exported_agent
        assert exported_agent is not None
        assert exported_agent.name == "pause_resume_agent"


class TestAgentTools:
    """Test agent tools functionality."""

    def test_process_data_chunk_success(self):
        """Test process_data_chunk with valid data."""
        result = process_data_chunk("hello world test")
        assert result["status"] == "success"
        assert "report" in result
        assert result["word_count"] == 3

    def test_process_data_chunk_multiline(self):
        """Test process_data_chunk with multiline data."""
        result = process_data_chunk("line1\nline2\nline3")
        assert result["status"] == "success"
        assert result["lines_processed"] == 3

    def test_process_data_chunk_empty(self):
        """Test process_data_chunk with empty data."""
        result = process_data_chunk("")
        assert result["status"] == "error"
        assert result["error"] == "Empty data string"

    def test_validate_checkpoint_valid(self):
        """Test validate_checkpoint with valid data."""
        result = validate_checkpoint("checkpoint_state")
        assert result["status"] == "success"
        assert result["is_valid"] is True

    def test_validate_checkpoint_empty(self):
        """Test validate_checkpoint with empty data."""
        result = validate_checkpoint("")
        assert result["status"] == "error"
        assert result["is_valid"] is False

    def test_get_resumption_hint_processing(self):
        """Test get_resumption_hint with processing context."""
        result = get_resumption_hint("processing data")
        assert result["status"] == "success"
        assert "processing" in result["hint"].lower()

    def test_get_resumption_hint_validation(self):
        """Test get_resumption_hint with validation context."""
        result = get_resumption_hint("validation check")
        assert result["status"] == "success"
        assert "validation" in result["hint"].lower()

    def test_get_resumption_hint_analysis(self):
        """Test get_resumption_hint with analysis context."""
        result = get_resumption_hint("analysis phase")
        assert result["status"] == "success"
        assert "analysis" in result["hint"].lower()

    def test_get_resumption_hint_unknown(self):
        """Test get_resumption_hint with unknown context."""
        result = get_resumption_hint("unknown context")
        assert result["status"] == "success"
        assert "resume from the beginning" in result["hint"].lower()


class TestImports:
    """Test module imports and exports."""

    def test_import_root_agent(self):
        """Test importing root_agent."""
        from pause_resume_agent import root_agent as agent
        assert agent is not None

    def test_import_agent_module(self):
        """Test importing agent module."""
        from pause_resume_agent import agent as agent_module
        assert agent_module is not None

    def test_import_app(self):
        """Test importing app."""
        from app import app as application
        assert application is not None


class TestAppConfiguration:
    """Test app configuration with pause/resume."""

    def test_app_name(self):
        """Test app has correct name."""
        assert app.name == "pause_resume_app"

    def test_app_has_root_agent(self):
        """Test app has root agent configured."""
        assert app.root_agent is not None
        assert app.root_agent.name == "pause_resume_agent"

    def test_resumability_config_exists(self):
        """Test app has resumability config."""
        assert app.resumability_config is not None

    def test_resumability_enabled(self):
        """Test resumability is enabled."""
        assert app.resumability_config.is_resumable is True
