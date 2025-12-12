"""
Tests for Deep Research Agent

These tests validate configuration and structure without making API calls.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from dataclasses import is_dataclass


class TestImports:
    """Test module imports."""
    
    def test_import_main_module(self):
        """Test importing main module."""
        from research_agent import (
            DeepResearchAgent,
            start_research,
            poll_research,
            run_research,
            DEEP_RESEARCH_AGENT_ID,
        )
        assert DeepResearchAgent is not None
        assert callable(start_research)
        assert callable(poll_research)
        assert callable(run_research)
        assert DEEP_RESEARCH_AGENT_ID == "deep-research-pro-preview-12-2025"
    
    def test_import_streaming(self):
        """Test importing streaming utilities."""
        from research_agent import (
            stream_research,
            ResearchProgress,
        )
        assert callable(stream_research)
        assert is_dataclass(ResearchProgress)


class TestDeepResearchAgentConfig:
    """Test DeepResearchAgent configuration."""
    
    def test_agent_requires_api_key(self):
        """Test that agent raises without API key."""
        from research_agent import DeepResearchAgent
        
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError) as exc_info:
                DeepResearchAgent()
            assert "GOOGLE_API_KEY" in str(exc_info.value)
    
    def test_agent_accepts_api_key(self):
        """Test that agent accepts explicit API key."""
        from research_agent import DeepResearchAgent
        
        agent = DeepResearchAgent(api_key="test-key")
        assert agent.api_key == "test-key"
    
    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'env-key'})
    def test_agent_uses_env_key(self):
        """Test that agent uses environment key."""
        from research_agent import DeepResearchAgent
        
        agent = DeepResearchAgent()
        assert agent.api_key == "env-key"
    
    def test_client_lazy_initialization(self):
        """Test that client is not created until accessed."""
        from research_agent import DeepResearchAgent
        
        agent = DeepResearchAgent(api_key="test-key")
        assert agent._client is None


class TestResearchResult:
    """Test ResearchResult dataclass."""
    
    def test_research_result_structure(self):
        """Test ResearchResult has expected fields."""
        from research_agent.agent import ResearchResult, ResearchStatus
        
        result = ResearchResult(
            id="test-id",
            status=ResearchStatus.COMPLETED,
            report="Test report",
            citations=["https://example.com"],
            elapsed_seconds=10.5,
        )
        
        assert result.id == "test-id"
        assert result.status == ResearchStatus.COMPLETED
        assert result.report == "Test report"
        assert len(result.citations) == 1
        assert result.elapsed_seconds == 10.5
        assert result.error is None
    
    def test_research_result_with_error(self):
        """Test ResearchResult with error."""
        from research_agent.agent import ResearchResult, ResearchStatus
        
        result = ResearchResult(
            id="test-id",
            status=ResearchStatus.FAILED,
            report="",
            citations=[],
            elapsed_seconds=5.0,
            error="Something went wrong",
        )
        
        assert result.status == ResearchStatus.FAILED
        assert result.error == "Something went wrong"


class TestResearchProgress:
    """Test ResearchProgress dataclass."""
    
    def test_progress_structure(self):
        """Test ResearchProgress has expected fields."""
        from research_agent.streaming import ResearchProgress, ProgressType
        
        progress = ResearchProgress(
            type=ProgressType.THOUGHT,
            content="Analyzing data...",
            interaction_id="int-123",
        )
        
        assert progress.type == ProgressType.THOUGHT
        assert progress.content == "Analyzing data..."
        assert progress.interaction_id == "int-123"
    
    def test_progress_types(self):
        """Test all ProgressType values exist."""
        from research_agent.streaming import ProgressType
        
        assert ProgressType.START.value == "start"
        assert ProgressType.THOUGHT.value == "thought"
        assert ProgressType.CONTENT.value == "content"
        assert ProgressType.COMPLETE.value == "complete"
        assert ProgressType.ERROR.value == "error"


class TestResearchMethods:
    """Test research methods with mocked client."""
    
    @patch('research_agent.agent.genai.Client')
    def test_start_research(self, mock_client_class):
        """Test start_research function."""
        from research_agent import start_research
        
        # Setup mock
        mock_client = MagicMock()
        mock_interaction = MagicMock()
        mock_interaction.id = "research-id-123"
        mock_interaction.status = "in_progress"
        mock_client.interactions.create.return_value = mock_interaction
        mock_client_class.return_value = mock_client
        
        # Test
        result = start_research("Test query", api_key="test-key")
        
        assert result["id"] == "research-id-123"
        assert result["status"] == "in_progress"
        
        # Verify correct parameters
        call_kwargs = mock_client.interactions.create.call_args[1]
        assert call_kwargs["agent"] == "deep-research-pro-preview-12-2025"
        assert call_kwargs["background"] == True
    
    @patch('research_agent.agent.genai.Client')
    def test_poll_research_in_progress(self, mock_client_class):
        """Test poll_research when in progress."""
        from research_agent import poll_research
        
        # Setup mock
        mock_client = MagicMock()
        mock_interaction = MagicMock()
        mock_interaction.id = "research-id-123"
        mock_interaction.status = "in_progress"
        mock_client.interactions.get.return_value = mock_interaction
        mock_client_class.return_value = mock_client
        
        # Test
        result = poll_research("research-id-123", api_key="test-key")
        
        assert result["id"] == "research-id-123"
        assert result["status"] == "in_progress"
        assert "report" not in result
    
    @patch('research_agent.agent.genai.Client')
    def test_poll_research_completed(self, mock_client_class):
        """Test poll_research when completed."""
        from research_agent import poll_research
        
        # Setup mock
        mock_client = MagicMock()
        mock_output = MagicMock()
        mock_output.text = "Research findings..."
        mock_interaction = MagicMock()
        mock_interaction.id = "research-id-123"
        mock_interaction.status = "completed"
        mock_interaction.outputs = [mock_output]
        mock_client.interactions.get.return_value = mock_interaction
        mock_client_class.return_value = mock_client
        
        # Test
        result = poll_research("research-id-123", api_key="test-key")
        
        assert result["status"] == "completed"
        assert result["report"] == "Research findings..."


class TestCitationExtraction:
    """Test citation extraction from research text."""
    
    def test_extract_citations(self):
        """Test URL extraction from text."""
        from research_agent import DeepResearchAgent
        
        agent = DeepResearchAgent(api_key="test-key")
        
        text = """
        According to https://example.com/article1 and 
        https://research.org/paper, the findings suggest...
        See also: http://legacy-site.com/doc
        """
        
        citations = agent._extract_citations(text)
        
        assert len(citations) == 3
        assert "https://example.com/article1" in citations
        assert "https://research.org/paper" in citations
        assert "http://legacy-site.com/doc" in citations
    
    def test_extract_no_citations(self):
        """Test with text containing no URLs."""
        from research_agent import DeepResearchAgent
        
        agent = DeepResearchAgent(api_key="test-key")
        
        text = "This text has no citations."
        citations = agent._extract_citations(text)
        
        assert len(citations) == 0
    
    def test_extract_deduplicates_citations(self):
        """Test that duplicate URLs are removed."""
        from research_agent import DeepResearchAgent
        
        agent = DeepResearchAgent(api_key="test-key")
        
        text = """
        See https://example.com for more.
        As mentioned in https://example.com, this is important.
        """
        
        citations = agent._extract_citations(text)
        
        # Should only have one entry despite duplicate URLs
        assert citations.count("https://example.com") == 1


class TestStreamReconnector:
    """Test stream reconnection functionality."""
    
    def test_reconnector_initialization(self):
        """Test ResearchStreamReconnector initialization."""
        from research_agent.streaming import ResearchStreamReconnector
        
        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'test-key'}):
            reconnector = ResearchStreamReconnector()
            
            assert reconnector.api_key == "test-key"
            assert reconnector.interaction_id is None
            assert reconnector.last_event_id is None
            assert reconnector.max_retries == 3
    
    def test_reconnector_with_explicit_key(self):
        """Test reconnector with explicit API key."""
        from research_agent.streaming import ResearchStreamReconnector
        
        reconnector = ResearchStreamReconnector(api_key="explicit-key")
        assert reconnector.api_key == "explicit-key"


class TestConstants:
    """Test module constants."""
    
    def test_agent_id(self):
        """Test Deep Research Agent ID."""
        from research_agent import DEEP_RESEARCH_AGENT_ID
        
        assert DEEP_RESEARCH_AGENT_ID == "deep-research-pro-preview-12-2025"
    
    def test_default_poll_interval(self):
        """Test default poll interval."""
        from research_agent.agent import DEFAULT_POLL_INTERVAL
        
        assert DEFAULT_POLL_INTERVAL == 10
    
    def test_max_research_time(self):
        """Test maximum research time."""
        from research_agent.agent import MAX_RESEARCH_TIME
        
        assert MAX_RESEARCH_TIME == 3600  # 60 minutes
