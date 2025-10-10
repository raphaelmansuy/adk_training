"""
Test suite for Tutorial 14: Streaming Agent

Tests agent configuration, streaming functionality, and tool functions.
"""

import pytest
import asyncio
from streaming_agent.agent import (
    create_streaming_agent,
    root_agent,
    stream_agent_response,
    get_complete_response,
    format_streaming_info,
    analyze_streaming_performance
)


class TestAgentConfiguration:
    """Test agent creation and configuration."""

    def test_create_streaming_agent(self):
        """Test that streaming agent is created with correct configuration."""
        agent = create_streaming_agent()

        assert agent is not None
        assert agent.name == 'streaming_assistant'
        assert 'streaming' in agent.description.lower()
        assert agent.model == 'gemini-2.0-flash'

    def test_root_agent_exists(self):
        """Test that root_agent is properly instantiated."""
        assert root_agent is not None
        assert hasattr(root_agent, 'name')
        assert hasattr(root_agent, 'model')


class TestStreamingFunctionality:
    """Test streaming response functionality."""

    @pytest.mark.asyncio
    async def test_stream_agent_response_basic(self):
        """Test basic streaming response functionality."""
        query = "Hello world"
        chunks = []

        async for chunk in stream_agent_response(query):
            chunks.append(chunk)

        assert len(chunks) > 0
        response_text = ''.join(chunks)
        # Response should contain some text (either real AI response or fallback)
        assert len(response_text.strip()) > 0

    @pytest.mark.asyncio
    async def test_stream_agent_response_empty_query(self):
        """Test streaming with empty query."""
        query = ""
        chunks = []

        async for chunk in stream_agent_response(query):
            chunks.append(chunk)

        assert len(chunks) > 0
        response_text = ''.join(chunks)
        # Should handle empty query gracefully
        assert len(response_text.strip()) > 0

    @pytest.mark.asyncio
    async def test_get_complete_response(self):
        """Test complete response functionality."""
        query = "Test query"
        response = await get_complete_response(query)

        assert isinstance(response, str)
        # Response should contain some text (either real AI response or fallback)
        assert len(response.strip()) > 0


class TestToolFunctions:
    """Test tool functions."""

    def test_format_streaming_info(self):
        """Test streaming info tool."""
        result = format_streaming_info()

        assert result['status'] == 'success'
        assert 'streaming_modes' in result['data']
        assert 'SSE' in result['data']['streaming_modes']
        assert 'benefits' in result['data']
        assert 'use_cases' in result['data']

    def test_analyze_streaming_performance_default(self):
        """Test performance analysis with default parameters."""
        result = analyze_streaming_performance()

        assert result['status'] == 'success'
        assert 'estimated_chunks' in result['data']
        assert 'estimated_total_time_seconds' in result['data']
        assert result['data']['memory_efficient'] is True

    def test_analyze_streaming_performance_custom_length(self):
        """Test performance analysis with custom query length."""
        query_length = 500
        result = analyze_streaming_performance(query_length)

        assert result['status'] == 'success'
        assert result['data']['estimated_chunks'] >= 1
        assert result['data']['estimated_total_time_seconds'] > 0

    def test_analyze_streaming_performance_zero_length(self):
        """Test performance analysis with zero query length."""
        result = analyze_streaming_performance(0)

        assert result['status'] == 'success'
        assert result['data']['estimated_chunks'] == 1  # Minimum 1 chunk


class TestIntegration:
    """Integration tests for agent functionality."""

    def test_agent_has_tools(self):
        """Test that agent has the expected tools."""
        assert hasattr(root_agent, 'tools')
        assert len(root_agent.tools) == 2

        tool_names = [tool.__name__ for tool in root_agent.tools]
        assert 'format_streaming_info' in tool_names
        assert 'analyze_streaming_performance' in tool_names

    def test_agent_instruction_content(self):
        """Test that agent has appropriate instructions."""
        # Check that instruction contains key phrases
        instruction = root_agent.instruction
        assert 'helpful' in instruction.lower()
        assert 'streaming' in instruction.lower()
        assert 'conversational' in instruction.lower()


if __name__ == '__main__':
    pytest.main([__file__])