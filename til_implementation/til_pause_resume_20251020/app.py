"""ADK App configuration with Pause/Resume Invocation support."""

from google.adk.apps import App, ResumabilityConfig
from pause_resume_agent import root_agent

# Configure resumable invocations
# This enables the agent to support pause/resume functionality
resumability_config = ResumabilityConfig(
    # Enables pause/resume support for this app's invocations
    is_resumable=True,
)

# Create app with resumable invocation support enabled
app = App(
    name="pause_resume_app",
    root_agent=root_agent,
    resumability_config=resumability_config,
)

__all__ = ["app"]
