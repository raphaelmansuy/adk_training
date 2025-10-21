"""ADK App configuration with Tool Use Quality evaluation."""

from google.adk.apps import App
from tool_use_evaluator import root_agent

# Create app with the tool use evaluation agent
app = App(
    name="tool_use_quality_app",
    root_agent=root_agent,
)

__all__ = ["app"]
