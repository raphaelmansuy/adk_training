"""Tests for Context Compaction Agent structure and configuration."""

from context_compaction_agent import root_agent


class TestAgentConfiguration:
  """Test agent configuration and basic setup."""

  def test_agent_exists(self):
    """Test that root_agent is properly defined."""
    assert root_agent is not None
    assert hasattr(root_agent, "name")

  def test_agent_name(self):
    """Test agent has correct name."""
    assert root_agent.name == "context_compaction_agent"

  def test_agent_model(self):
    """Test agent uses correct model."""
    assert root_agent.model == "gemini-2.0-flash"

  def test_agent_description(self):
    """Test agent has meaningful description."""
    assert root_agent.description
    assert "context compaction" in root_agent.description.lower()

  def test_agent_instruction(self):
    """Test agent has comprehensive instructions."""
    assert root_agent.instruction
    assert len(root_agent.instruction) > 100

  def test_agent_has_tools(self):
    """Test agent has tools configured."""
    assert hasattr(root_agent, "tools")
    assert root_agent.tools is not None
    # Should have at least the tools defined in agent.py
    assert len(root_agent.tools) >= 2

  def test_agent_tool_names(self):
    """Test agent tools have expected names."""
    tool_names = [tool.__name__ for tool in root_agent.tools]
    assert "summarize_text" in tool_names
    assert "calculate_complexity" in tool_names


class TestToolFunctionality:
  """Test the tools available to the agent."""

  def test_summarize_text_tool(self):
    """Test summarize_text tool works correctly."""
    from context_compaction_agent.agent import summarize_text

    # Test with long text
    long_text = "x" * 300
    result = summarize_text(long_text)
    assert result["status"] == "success"
    assert "report" in result
    assert "summary" in result
    assert len(result["summary"]) < len(long_text)

  def test_summarize_text_short_text(self):
    """Test summarize_text with short input."""
    from context_compaction_agent.agent import summarize_text

    short_text = "Hello world"
    result = summarize_text(short_text)
    assert result["status"] == "success"
    assert result["summary"] == short_text

  def test_calculate_complexity_tool(self):
    """Test calculate_complexity tool works correctly."""
    from context_compaction_agent.agent import calculate_complexity

    # Test with complex question
    complex_q = "What is the best way to implement context compaction in multi-turn conversations?"
    result = calculate_complexity(complex_q)
    assert result["status"] == "success"
    assert "complexity_level" in result
    assert result["complexity_level"] in ["low", "medium", "high"]
    assert "word_count" in result

  def test_calculate_complexity_simple(self):
    """Test calculate_complexity with simple input."""
    from context_compaction_agent.agent import calculate_complexity

    simple_q = "Hi"
    result = calculate_complexity(simple_q)
    assert result["status"] == "success"
    assert result["complexity_level"] == "low"

  def test_calculate_complexity_medium(self):
    """Test calculate_complexity with medium input."""
    from context_compaction_agent.agent import calculate_complexity

    medium_q = "How do you use context compaction?"
    result = calculate_complexity(medium_q)
    assert result["status"] == "success"
    assert result["complexity_level"] in ["low", "medium"]


class TestImports:
  """Test that required modules can be imported."""

  def test_import_agent_module(self):
    """Test agent module imports successfully."""
    from context_compaction_agent import agent
    assert agent is not None

  def test_import_root_agent(self):
    """Test root_agent can be imported."""
    from context_compaction_agent.agent import root_agent as imported_agent
    assert imported_agent is not None
    assert imported_agent.name == "context_compaction_agent"

  def test_import_tools(self):
    """Test tools can be imported."""
    from context_compaction_agent.agent import (
        summarize_text,
        calculate_complexity,
    )
    assert callable(summarize_text)
    assert callable(calculate_complexity)


class TestAppConfiguration:
  """Test App configuration with compaction."""

  def test_app_imports(self):
    """Test app configuration can be imported."""
    from app import app
    assert app is not None

  def test_app_has_root_agent(self):
    """Test app has root_agent configured."""
    from app import app
    assert hasattr(app, "root_agent")

  def test_compaction_config_imports(self):
    """Test EventsCompactionConfig can be imported."""
    from google.adk.apps.app import EventsCompactionConfig
    assert EventsCompactionConfig is not None

  def test_compaction_config_creation(self):
    """Test EventsCompactionConfig can be created."""
    from google.adk.apps.app import EventsCompactionConfig

    config = EventsCompactionConfig(
        compaction_interval=5,
        overlap_size=1,
    )
    assert config.compaction_interval == 5
    assert config.overlap_size == 1
