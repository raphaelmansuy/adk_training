"""
Deep Research Agent Implementation

This module provides a high-level interface to Google's Deep Research Agent,
which autonomously plans, executes, and synthesizes multi-step research tasks.

The Deep Research Agent:
- Plans a research strategy
- Searches the web for information
- Reads and analyzes sources
- Iterates to fill knowledge gaps
- Produces comprehensive reports with citations

Requirements:
- google-genai >= 1.55.0
- GOOGLE_API_KEY environment variable
"""

import os
import re
import time
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass
from enum import Enum

try:
    from google import genai
except ImportError:
    raise ImportError(
        "google-genai >= 1.55.0 is required. "
        "Install with: pip install 'google-genai>=1.55.0'"
    )

from dotenv import load_dotenv

# Load .env from the package directory
import pathlib
_env_path = pathlib.Path(__file__).parent / ".env"
load_dotenv(_env_path)

# Check if using Vertex AI
USE_VERTEX_AI = os.getenv("USE_VERTEX_AI", "false").lower() == "true"
if USE_VERTEX_AI:
    try:
        import vertexai
        from google.auth import default
    except ImportError:
        raise ImportError(
            "vertexai and google-auth packages are required for Vertex AI support. "
            "Install with: pip install 'google-cloud-aiplatform>=1.40.0' 'google-auth>=2.0.0'"
        )

# Deep Research Agent identifier
DEEP_RESEARCH_AGENT_ID = "deep-research-pro-preview-12-2025"

# Default polling interval in seconds
DEFAULT_POLL_INTERVAL = 10

# Maximum research time (60 minutes)
MAX_RESEARCH_TIME = 60 * 60


def extract_citations(text: str) -> List[str]:
    """
    Extract URLs and citations from text.
    
    Args:
        text: The text to extract citations from.
        
    Returns:
        List of unique URLs found in the text.
    """
    # Pattern to match http/https URLs
    url_pattern = r'https?://[^\s\)"\'\]]+'
    citations = list(set(re.findall(url_pattern, text)))
    return sorted(citations)


class ResearchStatus(Enum):
    """Status of a research task."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ResearchResult:
    """Result of a completed research task."""
    id: str
    status: ResearchStatus
    report: str
    citations: List[str]
    elapsed_seconds: float
    error: Optional[str] = None


class DeepResearchAgent:
    """
    High-level interface for the Deep Research Agent.
    
    This class provides methods for:
    - Starting background research tasks
    - Polling for completion
    - Streaming results with progress updates
    - Follow-up questions on completed research
    
    Example:
        >>> agent = DeepResearchAgent()
        >>> result = agent.research("Analyze AI trends in 2025")
        >>> print(result.report)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Deep Research Agent.
        
        Uses the Interactions API (genai.Client) in all cases.
        For Vertex AI, uses Application Default Credentials.
        For Google AI Studio, uses the provided API key.
        
        Args:
            api_key: Google API key. Uses GOOGLE_API_KEY env var if not provided.
                     Not needed for Vertex AI (uses Application Default Credentials).
        """
        self.use_vertex_ai = USE_VERTEX_AI
        self._client = None
        
        if self.use_vertex_ai:
            # Initialize Vertex AI context for credentials
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("VERTEX_AI_PROJECT_ID")
            region = os.getenv("VERTEX_AI_REGION", "us-central1")
            
            if not project_id:
                raise ValueError(
                    "GOOGLE_CLOUD_PROJECT or VERTEX_AI_PROJECT_ID is required for Vertex AI. "
                    "Set with: export GOOGLE_CLOUD_PROJECT='your-project-id'"
                )
            
            # Initialize Vertex AI to set up credentials context
            vertexai.init(project=project_id, location=region)
            self.project_id = project_id
            self.region = region
            
            # For genai.Client with Vertex AI, we'll use Application Default Credentials
            # The genai client will automatically use the credentials set up by vertexai.init()
            print(f"✓ Initialized Vertex AI (project={project_id}, region={region})")
            print(f"✓ Using Interactions API with Application Default Credentials")
        else:
            # Initialize Google AI SDK with API key
            self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
            if not self.api_key:
                raise ValueError(
                    "GOOGLE_API_KEY is required. "
                    "Get your key at: https://aistudio.google.com/apikey"
                )
            print(f"✓ Using Interactions API with API Key authentication")
    
    @property
    def client(self):
        """
        Lazy-initialize the genai.Client (Interactions API).
        
        Uses Interactions API for both Vertex AI and Google AI Studio.
        For Vertex AI, credentials are set up via Application Default Credentials.
        For Google AI Studio, uses the provided API key.
        """
        if self._client is None:
            if self.use_vertex_ai:
                # For Vertex AI, genai.Client uses Application Default Credentials
                # No API key needed - credentials come from vertexai.init() and gcloud auth
                self._client = genai.Client()
            else:
                # For Google AI Studio, use explicit API key
                self._client = genai.Client(api_key=self.api_key)
        return self._client
    
    def research(
        self,
        query: str,
        poll_interval: int = DEFAULT_POLL_INTERVAL,
        on_status: Optional[Callable[[str, float], None]] = None,
        timeout: int = MAX_RESEARCH_TIME,
    ) -> ResearchResult:
        """
        Run a complete research task and return the result.
        
        This method starts the research, polls for completion, and returns
        the final report. For streaming progress, use research_stream instead.
        
        Args:
            query: The research query/topic.
            poll_interval: Seconds between status checks (default: 10).
            on_status: Optional callback for status updates (status, elapsed_time).
            timeout: Maximum time to wait in seconds (default: 3600).
            
        Returns:
            ResearchResult with the report and metadata.
            
        Example:
            >>> result = agent.research(
            ...     "What are the latest developments in fusion energy?"
            ... )
            >>> print(result.report[:500])
        """
        start_time = time.time()
        
        # Start research in background using Interactions API
        # Both Vertex AI and Google AI Studio use the same Interactions API
        print("Starting research using Interactions API...")
        
        interaction = self.client.interactions.create(
            input=query,
            agent=DEEP_RESEARCH_AGENT_ID,
            background=True
        )
        
        interaction_id = interaction.id
        
        # Poll for completion using Interactions API
        while True:
            elapsed = time.time() - start_time
            
            if elapsed > timeout:
                return ResearchResult(
                    id=interaction_id,
                    status=ResearchStatus.FAILED,
                    report="",
                    citations=[],
                    elapsed_seconds=elapsed,
                    error=f"Research timed out after {timeout} seconds"
                )
            
            # Get current status via Interactions API (same for both Vertex AI and Google AI)
            interaction = self.client.interactions.get(interaction_id)
            status = interaction.status
            
            # Notify callback
            if on_status:
                on_status(status, elapsed)
            
            if status == "completed":
                report_text = interaction.outputs[-1].text if interaction.outputs else ""
                citations = extract_citations(report_text)
                
                return ResearchResult(
                    id=interaction_id,
                    status=ResearchStatus.COMPLETED,
                    report=report_text,
                    citations=citations,
                    elapsed_seconds=elapsed,
                )
            
            elif status == "failed":
                error_msg = getattr(interaction, 'error', 'Unknown error')
                return ResearchResult(
                    id=interaction_id,
                    status=ResearchStatus.FAILED,
                    report="",
                    citations=[],
                    elapsed_seconds=elapsed,
                    error=str(error_msg)
                )
            
            time.sleep(poll_interval)
    
    def research_with_format(
        self,
        query: str,
        format_instructions: str,
        **kwargs
    ) -> ResearchResult:
        """
        Run research with specific output formatting.
        
        Args:
            query: The research topic.
            format_instructions: Formatting requirements for the output.
            **kwargs: Additional arguments passed to research().
            
        Returns:
            ResearchResult with formatted report.
            
        Example:
            >>> result = agent.research_with_format(
            ...     "EV battery market analysis",
            ...     format_instructions='''
            ...     Format as:
            ...     1. Executive Summary
            ...     2. Key Players (table)
            ...     3. Market Trends
            ...     '''
            ... )
        """
        formatted_query = f"{query}\n\n{format_instructions}"
        return self.research(formatted_query, **kwargs)
    
    def follow_up(
        self,
        interaction_id: str,
        question: str,
        model: str = "gemini-3-pro-preview"
    ) -> str:
        """
        Ask a follow-up question about completed research.
        
        Args:
            interaction_id: The ID of the completed research interaction.
            question: Your follow-up question.
            model: Model to use for follow-up (default: gemini-3-pro-preview).
            
        Returns:
            The model's response to the follow-up.
            
        Example:
            >>> result = agent.research("AI trends 2025")
            >>> follow_up = agent.follow_up(
            ...     result.id,
            ...     "Elaborate on the first trend you mentioned"
            ... )
        """
        interaction = self.client.interactions.create(
            model=model,
            input=question,
            previous_interaction_id=interaction_id
        )
        return interaction.outputs[-1].text if interaction.outputs else ""
    
    def _extract_citations(self, text: str) -> List[str]:
        """Extract citation URLs from research text."""
        import re
        # URL extraction pattern - captures URLs and strips trailing punctuation
        url_pattern = r'https?://[^\s\)\]<>"\']+'
        urls = re.findall(url_pattern, text)
        # Strip trailing punctuation that might have been captured
        cleaned_urls = [url.rstrip(',.;:!?') for url in urls]
        return list(set(cleaned_urls))  # Deduplicate


# Convenience functions for simple usage

def start_research(
    query: str,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Start a background research task.
    
    Args:
        query: The research query.
        api_key: Optional API key.
        
    Returns:
        Dictionary with 'id' and 'status'.
    """
    key = api_key or os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=key)
    
    interaction = client.interactions.create(
        input=query,
        agent=DEEP_RESEARCH_AGENT_ID,
        background=True
    )
    
    return {
        "id": interaction.id,
        "status": interaction.status,
    }


def poll_research(
    interaction_id: str,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Check the status of a research task.
    
    Args:
        interaction_id: The interaction ID from start_research.
        api_key: Optional API key.
        
    Returns:
        Dictionary with status and content (if completed).
    """
    key = api_key or os.getenv("GOOGLE_API_KEY")
    client = genai.Client(api_key=key)
    
    interaction = client.interactions.get(interaction_id)
    
    result = {
        "id": interaction.id,
        "status": interaction.status,
    }
    
    if interaction.status == "completed":
        result["report"] = interaction.outputs[-1].text if interaction.outputs else ""
    elif interaction.status == "failed":
        result["error"] = getattr(interaction, 'error', 'Unknown error')
    
    return result


def run_research(
    query: str,
    api_key: Optional[str] = None,
    poll_interval: int = DEFAULT_POLL_INTERVAL,
    verbose: bool = False
) -> str:
    """
    Run a complete research task and return the report.
    
    This is the simplest way to use Deep Research - it handles
    all the background execution and polling for you.
    
    Args:
        query: The research query.
        api_key: Optional API key.
        poll_interval: Seconds between polls.
        verbose: Whether to print status updates.
        
    Returns:
        The research report text.
        
    Example:
        >>> report = run_research("Latest developments in quantum computing")
        >>> print(report)
    """
    def status_callback(status: str, elapsed: float):
        if verbose:
            mins = int(elapsed // 60)
            secs = int(elapsed % 60)
            print(f"[{mins:02d}:{secs:02d}] Status: {status}")
    
    agent = DeepResearchAgent(api_key=api_key)
    result = agent.research(query, poll_interval=poll_interval, on_status=status_callback)
    
    if result.status == ResearchStatus.FAILED:
        raise RuntimeError(f"Research failed: {result.error}")
    
    return result.report
