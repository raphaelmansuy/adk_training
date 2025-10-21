"""Tests for agent configuration and tools."""

from tool_use_evaluator.agent import root_agent


class TestAgentConfiguration:
    """Test agent configuration."""

    def test_agent_name(self):
        """Test agent has correct name."""
        assert root_agent.name == "tool_use_evaluator"

    def test_agent_model(self):
        """Test agent uses correct model."""
        assert root_agent.model == "gemini-2.0-flash"

    def test_agent_description(self):
        """Test agent has description."""
        assert root_agent.description
        assert "tool use quality" in root_agent.description.lower()

    def test_agent_instruction(self):
        """Test agent has instruction."""
        assert root_agent.instruction
        assert "data" in root_agent.instruction.lower()

    def test_agent_has_tools(self):
        """Test agent has all required tools."""
        tool_names = [tool.__name__ for tool in root_agent.tools]
        assert "analyze_data" in tool_names
        assert "extract_features" in tool_names
        assert "validate_quality" in tool_names
        assert "apply_model" in tool_names

    def test_agent_has_output_key(self):
        """Test agent has output key configured."""
        assert root_agent.output_key == "analysis_result"


class TestToolFunctionality:
    """Test individual tool functions."""

    def test_analyze_data_success(self):
        """Test analyze_data with valid input."""
        from tool_use_evaluator.agent import analyze_data
        result = analyze_data("customer_data")
        assert result["status"] == "success"
        assert "analyzed" in result["report"].lower()
        assert "data" in result

    def test_analyze_data_error(self):
        """Test analyze_data with empty input."""
        from tool_use_evaluator.agent import analyze_data
        result = analyze_data("")
        assert result["status"] == "error"

    def test_extract_features_success(self):
        """Test extract_features with valid input."""
        from tool_use_evaluator.agent import extract_features
        result = extract_features({"test": "data"})
        assert result["status"] == "success"
        assert "features" in result["data"]

    def test_extract_features_error(self):
        """Test extract_features with empty input."""
        from tool_use_evaluator.agent import extract_features
        result = extract_features(None)
        assert result["status"] == "error"

    def test_validate_quality_success(self):
        """Test validate_quality with valid input."""
        from tool_use_evaluator.agent import validate_quality
        result = validate_quality({"features": "data"})
        assert result["status"] == "success"
        assert "quality_score" in result["data"]

    def test_validate_quality_error(self):
        """Test validate_quality with empty input."""
        from tool_use_evaluator.agent import validate_quality
        result = validate_quality(None)
        assert result["status"] == "error"

    def test_apply_model_success(self):
        """Test apply_model with valid inputs."""
        from tool_use_evaluator.agent import apply_model
        result = apply_model({"features": "data"}, "random_forest")
        assert result["status"] == "success"
        assert "model" in result["data"]

    def test_apply_model_error_no_features(self):
        """Test apply_model without features."""
        from tool_use_evaluator.agent import apply_model
        result = apply_model(None, "random_forest")
        assert result["status"] == "error"

    def test_apply_model_error_no_model(self):
        """Test apply_model without model name."""
        from tool_use_evaluator.agent import apply_model
        result = apply_model({"features": "data"}, "")
        assert result["status"] == "error"
