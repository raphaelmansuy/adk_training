"""ADK App configuration with Context Compaction enabled."""

from google.adk.apps import App
from google.adk.apps.app import EventsCompactionConfig
from context_compaction_agent import root_agent

# Configure context compaction
# This automatically summarizes conversation history to reduce token usage
compaction_config = EventsCompactionConfig(
    # How many new interactions before compaction occurs
    compaction_interval=5,
    # How many previous interactions to keep for context continuity
    overlap_size=1,
)

# Create app with compaction enabled
app = App(
    name="context_compaction_app",
    root_agent=root_agent,
    events_compaction_config=compaction_config,
)

__all__ = ["app"]
