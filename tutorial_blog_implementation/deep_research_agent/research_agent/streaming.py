"""
Streaming utilities for Deep Research Agent.

This module provides streaming functionality for real-time progress updates
during research tasks.
"""

import os
from typing import Optional, Generator, Dict, Any, Callable
from dataclasses import dataclass, field
from enum import Enum

try:
    from google import genai
except ImportError:
    raise ImportError("google-genai >= 1.55.0 required")

from dotenv import load_dotenv

load_dotenv()

# Agent ID
DEEP_RESEARCH_AGENT_ID = "deep-research-pro-preview-12-2025"


class ProgressType(Enum):
    """Types of progress updates during research."""
    START = "start"
    THOUGHT = "thought"
    CONTENT = "content"
    COMPLETE = "complete"
    ERROR = "error"


@dataclass
class ResearchProgress:
    """A progress update from the research stream."""
    type: ProgressType
    content: str = ""
    interaction_id: Optional[str] = None
    event_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


def stream_research(
    query: str,
    api_key: Optional[str] = None,
    include_thoughts: bool = True,
) -> Generator[ResearchProgress, None, None]:
    """
    Stream research progress with real-time updates.
    
    This generator yields progress updates as the Deep Research Agent
    works through the research task, including:
    - Start event with interaction ID
    - Thought summaries (reasoning steps)
    - Content chunks (report text)
    - Completion event
    
    Args:
        query: The research query.
        api_key: Optional API key.
        include_thoughts: Whether to enable thought summaries.
        
    Yields:
        ResearchProgress objects with updates.
        
    Example:
        >>> for progress in stream_research("AI trends 2025"):
        ...     if progress.type == ProgressType.THOUGHT:
        ...         print(f"💭 {progress.content}")
        ...     elif progress.type == ProgressType.CONTENT:
        ...         print(progress.content, end="")
    """
    key = api_key or os.getenv("GOOGLE_API_KEY")
    if not key:
        raise ValueError("GOOGLE_API_KEY required")
    
    client = genai.Client(api_key=key)
    
    # Build agent config
    agent_config = {"type": "deep-research"}
    if include_thoughts:
        agent_config["thinking_summaries"] = "auto"
    
    # Start streaming request
    stream = client.interactions.create(
        input=query,
        agent=DEEP_RESEARCH_AGENT_ID,
        background=True,
        stream=True,
        agent_config=agent_config
    )
    
    interaction_id = None
    last_event_id = None
    
    for chunk in stream:
        # Track interaction ID
        if chunk.event_type == "interaction.start":
            interaction_id = chunk.interaction.id
            yield ResearchProgress(
                type=ProgressType.START,
                content=f"Research started",
                interaction_id=interaction_id,
            )
        
        # Track event ID for potential reconnection
        if hasattr(chunk, 'event_id') and chunk.event_id:
            last_event_id = chunk.event_id
        
        # Handle content deltas
        if chunk.event_type == "content.delta":
            if hasattr(chunk.delta, 'type'):
                if chunk.delta.type == "text":
                    yield ResearchProgress(
                        type=ProgressType.CONTENT,
                        content=chunk.delta.text,
                        interaction_id=interaction_id,
                        event_id=last_event_id,
                    )
                elif chunk.delta.type == "thought_summary":
                    thought_text = ""
                    if hasattr(chunk.delta, 'content') and hasattr(chunk.delta.content, 'text'):
                        thought_text = chunk.delta.content.text
                    yield ResearchProgress(
                        type=ProgressType.THOUGHT,
                        content=thought_text,
                        interaction_id=interaction_id,
                        event_id=last_event_id,
                    )
        
        # Handle completion
        if chunk.event_type == "interaction.complete":
            yield ResearchProgress(
                type=ProgressType.COMPLETE,
                content="Research complete",
                interaction_id=interaction_id,
            )
        
        # Handle errors
        if chunk.event_type == "error":
            error_msg = getattr(chunk, 'message', 'Unknown error')
            yield ResearchProgress(
                type=ProgressType.ERROR,
                content=str(error_msg),
                interaction_id=interaction_id,
            )


def stream_research_with_callback(
    query: str,
    on_thought: Optional[Callable[[str], None]] = None,
    on_content: Optional[Callable[[str], None]] = None,
    on_complete: Optional[Callable[[str], None]] = None,
    api_key: Optional[str] = None,
) -> str:
    """
    Stream research with callback handlers.
    
    A convenience function that handles streaming and calls your
    callbacks for different event types.
    
    Args:
        query: The research query.
        on_thought: Callback for thought summaries.
        on_content: Callback for content chunks.
        on_complete: Callback when research completes.
        api_key: Optional API key.
        
    Returns:
        The complete research report.
        
    Example:
        >>> report = stream_research_with_callback(
        ...     "Quantum computing advances",
        ...     on_thought=lambda t: print(f"💭 {t}"),
        ...     on_content=lambda c: print(c, end=""),
        ... )
    """
    full_content = []
    
    for progress in stream_research(query, api_key=api_key):
        if progress.type == ProgressType.THOUGHT and on_thought:
            on_thought(progress.content)
        elif progress.type == ProgressType.CONTENT:
            full_content.append(progress.content)
            if on_content:
                on_content(progress.content)
        elif progress.type == ProgressType.COMPLETE and on_complete:
            on_complete(progress.interaction_id or "")
    
    return "".join(full_content)


class ResearchStreamReconnector:
    """
    Handles reconnection to a research stream after disconnection.
    
    Network interruptions can occur during long research tasks.
    This class helps resume from where you left off.
    
    Example:
        >>> reconnector = ResearchStreamReconnector(api_key)
        >>> for progress in reconnector.stream(query):
        ...     process(progress)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.interaction_id: Optional[str] = None
        self.last_event_id: Optional[str] = None
        self.max_retries = 3
        self.retry_delay = 2
    
    def stream(
        self,
        query: str,
        include_thoughts: bool = True
    ) -> Generator[ResearchProgress, None, None]:
        """
        Stream research with automatic reconnection on failure.
        
        Args:
            query: The research query.
            include_thoughts: Whether to include thought summaries.
            
        Yields:
            ResearchProgress objects.
        """
        import time
        
        retries = 0
        is_complete = False
        
        while not is_complete and retries <= self.max_retries:
            try:
                # First attempt: start new research
                if self.interaction_id is None:
                    for progress in self._initial_stream(query, include_thoughts):
                        yield progress
                        if progress.type == ProgressType.COMPLETE:
                            is_complete = True
                else:
                    # Reconnection: resume from last event
                    for progress in self._resume_stream():
                        yield progress
                        if progress.type == ProgressType.COMPLETE:
                            is_complete = True
                            
            except Exception as e:
                retries += 1
                if retries > self.max_retries:
                    yield ResearchProgress(
                        type=ProgressType.ERROR,
                        content=f"Max retries exceeded: {e}"
                    )
                    break
                time.sleep(self.retry_delay)
    
    def _initial_stream(
        self,
        query: str,
        include_thoughts: bool
    ) -> Generator[ResearchProgress, None, None]:
        """Start initial streaming request."""
        for progress in stream_research(query, self.api_key, include_thoughts):
            # Track IDs for potential reconnection
            if progress.interaction_id:
                self.interaction_id = progress.interaction_id
            if progress.event_id:
                self.last_event_id = progress.event_id
            yield progress
    
    def _resume_stream(self) -> Generator[ResearchProgress, None, None]:
        """Resume stream from last known position."""
        if not self.interaction_id:
            raise ValueError("No interaction ID to resume from")
        
        client = genai.Client(api_key=self.api_key)
        
        # Resume with last_event_id to continue from where we left off
        kwargs = {"id": self.interaction_id, "stream": True}
        if self.last_event_id:
            kwargs["last_event_id"] = self.last_event_id
        
        stream = client.interactions.get(**kwargs)
        
        for chunk in stream:
            if hasattr(chunk, 'event_id') and chunk.event_id:
                self.last_event_id = chunk.event_id
            
            if chunk.event_type == "content.delta":
                if hasattr(chunk.delta, 'type'):
                    if chunk.delta.type == "text":
                        yield ResearchProgress(
                            type=ProgressType.CONTENT,
                            content=chunk.delta.text,
                            interaction_id=self.interaction_id,
                        )
                    elif chunk.delta.type == "thought_summary":
                        yield ResearchProgress(
                            type=ProgressType.THOUGHT,
                            content=getattr(chunk.delta.content, 'text', ''),
                            interaction_id=self.interaction_id,
                        )
            
            if chunk.event_type == "interaction.complete":
                yield ResearchProgress(
                    type=ProgressType.COMPLETE,
                    content="Research complete",
                    interaction_id=self.interaction_id,
                )
