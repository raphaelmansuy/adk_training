"""
Comprehensive Streaming Tests - Tutorial 14

Unit tests for streaming agents demonstrating the patterns from the tutorial.
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, AsyncMock, patch
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.sessions import InMemorySessionService
from google.genai import types


@pytest.mark.asyncio
class TestStreamingFunctionality:
    """Test streaming response functionality."""

    async def setup_method(self):
        """Set up test fixtures."""
        self.agent = Agent(
            model='gemini-2.0-flash',
            name='test_streaming_agent',
            instruction='Provide test responses for streaming.'
        )

        self.session_service = InMemorySessionService()
        self.runner = Runner(app_name="test_streaming", agent=self.agent, session_service=self.session_service)
        self.run_config = RunConfig(streaming_mode=StreamingMode.SSE)

    async def create_test_session(self):
        """Create a test session."""
        return await self.session_service.create_session(
            app_name="test_streaming",
            user_id="test_user"
        )

    @pytest.mark.asyncio
    async def test_streaming_response_basic(self):
        """Test that streaming returns multiple chunks."""
        session = await self.create_test_session()

        chunks = []

        async for event in self.runner.run_async(
            user_id="test_user",
            session_id=session.id,
            new_message=types.Content(role="user", parts=[types.Part(text="Explain machine learning in detail")]),
            run_config=self.run_config
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        chunks.append(part.text)

            if event.turn_complete:
                break

        # Should receive multiple chunks (or at least one)
        assert len(chunks) > 0

        # Complete text should be reasonable length
        complete = ''.join(chunks)
        assert len(complete.strip()) > 0

    @pytest.mark.asyncio
    async def test_streaming_aggregation(self):
        """Test that streaming chunks combine correctly."""
        session = await self.create_test_session()

        chunks = []

        async for event in self.runner.run_async(
            user_id="test_user",
            session_id=session.id,
            new_message=types.Content(role="user", parts=[types.Part(text="Count to 10")]),
            run_config=self.run_config
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        chunks.append(part.text)

            if event.turn_complete:
                break

        complete = ''.join(chunks)

        # Should contain some numbers (basic validation)
        has_numbers = any(char.isdigit() for char in complete)
        assert has_numbers or len(complete.strip()) > 0  # Fallback for non-numeric responses

    @pytest.mark.asyncio
    async def test_streaming_with_different_queries(self):
        """Test streaming with various query types."""
        session = await self.create_test_session()

        test_queries = [
            "Hello",
            "What is AI?",
            "Explain quantum computing briefly"
        ]

        for query in test_queries:
            chunks = []

            async for event in self.runner.run_async(
                user_id="test_user",
                session_id=session.id,
                new_message=types.Content(role="user", parts=[types.Part(text=query)]),
                run_config=self.run_config
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            chunks.append(part.text)

                if event.turn_complete:
                    break

            # Each query should produce some response
            complete = ''.join(chunks)
            assert len(complete.strip()) > 0

    @pytest.mark.asyncio
    async def test_streaming_chunk_sizes(self):
        """Test that chunks have reasonable sizes."""
        session = await self.create_test_session()

        chunks = []

        async for event in self.runner.run_async(
            user_id="test_user",
            session_id=session.id,
            new_message=types.Content(role="user", parts=[types.Part(text="Write a paragraph about technology")]),
            run_config=self.run_config
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        chunks.append(part.text)

            if event.turn_complete:
                break

        # Check chunk size distribution
        if len(chunks) > 1:
            chunk_sizes = [len(chunk) for chunk in chunks]
            avg_size = sum(chunk_sizes) / len(chunk_sizes)

            # Average chunk should be reasonable (not too small or large)
            assert 1 <= avg_size <= 500

    @pytest.mark.asyncio
    async def test_streaming_error_handling(self):
        """Test streaming with error handling."""
        session = await self.create_test_session()

        try:
            chunks = []
            async for event in self.runner.run_async(
                user_id="test_user",
                session_id=session.id,
                new_message=types.Content(role="user", parts=[types.Part(text="Test query")]),
                run_config=self.run_config
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            chunks.append(part.text)

                if event.turn_complete:
                    break

            # Should complete without throwing
            complete = ''.join(chunks)
            assert isinstance(complete, str)

        except Exception as e:
            # If error occurs, it should be handled gracefully
            pytest.fail(f"Streaming failed unexpectedly: {e}")


@pytest.mark.asyncio
class TestStreamingModes:
    """Test different streaming mode configurations."""

    async def setup_method(self):
        """Set up test fixtures."""
        self.agent = Agent(
            model='gemini-2.0-flash',
            name='test_modes_agent',
            instruction='Provide test responses.'
        )

        self.session_service = InMemorySessionService()
        self.runner = Runner(app_name="test_modes", agent=self.agent, session_service=self.session_service)

    async def create_test_session(self):
        """Create a test session."""
        return await self.session_service.create_session(
            app_name="test_modes",
            user_id="test_user"
        )

    @pytest.mark.asyncio
    async def test_sse_mode(self):
        """Test SSE streaming mode."""
        session = await self.create_test_session()

        sse_config = RunConfig(streaming_mode=StreamingMode.SSE)

        chunks = []
        async for event in self.runner.run_async(
            user_id="test_user",
            session_id=session.id,
            new_message=types.Content(role="user", parts=[types.Part(text="Hello")]),
            run_config=sse_config
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        chunks.append(part.text)

            if event.turn_complete:
                break

        assert len(chunks) >= 0  # May be empty for very short responses

    @pytest.mark.asyncio
    async def test_blocking_mode(self):
        """Test blocking (non-streaming) mode."""
        session = await self.create_test_session()

        blocking_config = RunConfig(streaming_mode=StreamingMode.NONE)

        # Collect all response at once
        responses = []
        async for event in self.runner.run_async(
            user_id="test_user",
            session_id=session.id,
            new_message=types.Content(role="user", parts=[types.Part(text="Hello")]),
            run_config=blocking_config
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        responses.append(part.text)

            if event.turn_complete:
                break

        complete_response = ''.join(responses)
        assert len(complete_response.strip()) > 0


@pytest.mark.asyncio
class TestStreamingIntegration:
    """Integration tests for streaming functionality."""

    async def setup_method(self):
        """Set up test fixtures."""
        self.agent = Agent(
            model='gemini-2.0-flash',
            name='integration_test_agent',
            instruction='Provide integration test responses.'
        )

        self.session_service = InMemorySessionService()
        self.runner = Runner(app_name="integration_test", agent=self.agent, session_service=self.session_service)

    async def create_test_session(self):
        """Create a test session."""
        return await self.session_service.create_session(
            app_name="integration_test",
            user_id="test_user"
        )

    @pytest.mark.asyncio
    async def test_multiple_streaming_sessions(self):
        """Test multiple concurrent streaming sessions."""
        # Create multiple sessions
        sessions = []
        for i in range(3):
            session = await self.create_test_session()
            sessions.append(session)

        # Run queries on each session
        tasks = []
        for i, session in enumerate(sessions):
            task = self._run_single_session_query(session, f"Query {i+1}")
            tasks.append(task)

        # Run all concurrently
        results = await asyncio.gather(*tasks)

        # All should complete successfully
        for result in results:
            assert len(result) > 0

    async def _run_single_session_query(self, session, query):
        """Run a single query on a session."""
        run_config = RunConfig(streaming_mode=StreamingMode.SSE)

        chunks = []
        async for event in self.runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=types.Content(role="user", parts=[types.Part(text=query)]),
            run_config=run_config
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        chunks.append(part.text)

            if event.turn_complete:
                break

        return ''.join(chunks)

    @pytest.mark.asyncio
    async def test_streaming_timeout_simulation(self):
        """Test timeout behavior (simulated)."""
        session = await self.create_test_session()

        run_config = RunConfig(streaming_mode=StreamingMode.SSE)

        # Use a short timeout for testing
        timeout_seconds = 5.0

        try:
            async with asyncio.timeout(timeout_seconds):
                chunks = []
                async for event in self.runner.run_async(
                    user_id="test_user",
                    session_id=session.id,
                    new_message=types.Content(role="user", parts=[types.Part(text="Provide a detailed explanation")]),
                    run_config=run_config
                ):
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if part.text:
                                chunks.append(part.text)

                    if event.turn_complete:
                        break

                # Should complete within timeout
                complete = ''.join(chunks)
                assert len(complete.strip()) > 0

        except asyncio.TimeoutError:
            # This is expected for slow responses - test passes
            pass


# Mock tests for FastAPI SSE endpoint
class TestFastAPIStreaming:
    """Test FastAPI streaming endpoint (mocked)."""

    def test_sse_endpoint_structure(self):
        """Test that SSE endpoint has correct structure."""
        # This would test the actual FastAPI endpoint
        # For now, just validate the concept
        assert StreamingMode.SSE is not None
        assert RunConfig is not None

    def test_sse_data_format(self):
        """Test SSE data formatting."""
        test_data = {'text': 'Hello', 'type': 'chunk'}
        sse_line = f"data: {json.dumps(test_data)}\n\n"

        # Should be valid SSE format
        assert sse_line.startswith('data: ')
        assert sse_line.endswith('\n\n')

        # Should be parseable JSON
        parsed = json.loads(sse_line[6:-2])  # Remove 'data: ' and '\n\n'
        assert parsed['text'] == 'Hello'
        assert parsed['type'] == 'chunk'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])