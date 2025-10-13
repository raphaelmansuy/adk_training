"""
Test tool functions for the artifact agent.
"""

import pytest
from unittest.mock import AsyncMock
from artifact_agent.agent import (
    extract_text_tool,
    summarize_document_tool,
    translate_document_tool,
    create_final_report_tool,
    list_artifacts_tool,
    load_artifact_tool,
)


@pytest.fixture
def mock_tool_context():
    """Create a mock ToolContext for testing."""
    context = AsyncMock()
    context.save_artifact = AsyncMock(return_value=0)  # Return version 0
    context.load_artifact = AsyncMock(return_value=None)
    context.list_artifacts = AsyncMock(return_value=[])
    return context


class TestExtractTextTool:
    """Test the extract_text_tool function."""

    @pytest.mark.asyncio
    async def test_extract_text_success(self, mock_tool_context):
        """Test successful text extraction."""
        test_text = "This is a sample document for testing."
        result = await extract_text_tool(test_text, mock_tool_context)

        assert result['status'] == 'success'
        assert 'extracted' in result['report'].lower()
        assert 'data' in result
        assert result['data']['filename'] == 'document_extracted.txt'
        assert result['data']['content'] == test_text
        assert result['data']['word_count'] == len(test_text.split())
        assert result['data']['character_count'] == len(test_text)
        mock_tool_context.save_artifact.assert_called_once()

    @pytest.mark.asyncio
    async def test_extract_text_empty(self, mock_tool_context):
        """Test extraction with empty text."""
        result = await extract_text_tool("", mock_tool_context)

        assert result['status'] == 'error'
        assert 'failed to extract text from document' in result['report'].lower()

    @pytest.mark.asyncio
    async def test_extract_text_whitespace_only(self, mock_tool_context):
        """Test extraction with whitespace only."""
        result = await extract_text_tool("   \n\t   ", mock_tool_context)

        assert result['status'] == 'error'
        assert 'failed to extract text from document' in result['report'].lower()


class TestSummarizeDocumentTool:
    """Test the summarize_document_tool function."""

    @pytest.mark.asyncio
    async def test_summarize_success(self, mock_tool_context):
        """Test successful document summarization."""
        test_text = "This is a long document that should be summarized. " * 10
        result = await summarize_document_tool(test_text, mock_tool_context)

        assert result['status'] == 'success'
        assert 'summary' in result['report'].lower()
        assert 'data' in result
        assert result['data']['filename'] == 'document_summary.txt'
        assert len(result['data']['content']) <= len(test_text)
        mock_tool_context.save_artifact.assert_called_once()

    @pytest.mark.asyncio
    async def test_summarize_no_text(self, mock_tool_context):
        """Test summarization with no text provided."""
        result = await summarize_document_tool(None, mock_tool_context)

        assert result['status'] == 'error'
        assert 'please provide document text' in result['report'].lower()

    @pytest.mark.asyncio
    async def test_summarize_short_text(self, mock_tool_context):
        """Test summarization of short text."""
        short_text = "Short text."
        result = await summarize_document_tool(short_text, mock_tool_context)

        assert result['status'] == 'success'
        # Short text should be returned as-is
        assert result['data']['content'] == short_text
        mock_tool_context.save_artifact.assert_called_once()


class TestTranslateDocumentTool:
    """Test the translate_document_tool function."""

    @pytest.mark.asyncio
    async def test_translate_success(self, mock_tool_context):
        """Test successful document translation."""
        test_text = "Hello world"
        target_lang = "Spanish"
        result = await translate_document_tool(test_text, target_lang, mock_tool_context)

        assert result['status'] == 'success'
        assert target_lang.lower() in result['report'].lower()
        assert 'data' in result
        assert result['data']['filename'] == f'document_{target_lang.lower()}.txt'
        assert target_lang in result['data']['content']
        assert result['data']['target_language'] == target_lang
        mock_tool_context.save_artifact.assert_called_once()

    @pytest.mark.asyncio
    async def test_translate_empty_text(self, mock_tool_context):
        """Test translation with empty text."""
        result = await translate_document_tool("", "French", mock_tool_context)

        assert result['status'] == 'error'
        assert 'please provide text to translate' in result['report'].lower()


class TestCreateFinalReportTool:
    """Test the create_final_report_tool function."""

    @pytest.mark.asyncio
    async def test_create_report_success(self, mock_tool_context):
        """Test successful final report creation."""
        mock_tool_context.list_artifacts.return_value = ['document_extracted.txt', 'document_summary.txt']
        
        result = await create_final_report_tool(mock_tool_context)

        assert result['status'] == 'success'
        assert 'final report' in result['report'].lower()
        assert 'data' in result
        assert result['data']['filename'] == 'document_FINAL_REPORT.md'
        assert 'artifacts_combined' in result['data']
        assert isinstance(result['data']['artifacts_combined'], list)
        mock_tool_context.save_artifact.assert_called_once()


class TestListArtifactsTool:
    """Test the list_artifacts_tool function."""

    @pytest.mark.asyncio
    async def test_list_artifacts_success(self, mock_tool_context):
        """Test successful artifact listing."""
        mock_tool_context.list_artifacts.return_value = ['file1.txt', 'file2.txt']
        
        result = await list_artifacts_tool(mock_tool_context)

        assert result['status'] == 'success'
        assert 'artifacts' in result['report'].lower()
        assert 'data' in result
        assert 'artifacts' in result['data']
        assert 'count' in result['data']
        assert isinstance(result['data']['artifacts'], list)
        assert result['data']['count'] == 2
        mock_tool_context.list_artifacts.assert_called_once()


class TestLoadArtifactTool:
    """Test the load_artifact_tool function."""

    @pytest.mark.asyncio
    async def test_load_artifact_success(self, mock_tool_context):
        """Test successful artifact loading."""
        filename = "test_artifact.txt"
        mock_artifact = AsyncMock()
        mock_artifact.text = "Test content"
        mock_tool_context.load_artifact.return_value = mock_artifact
        
        result = await load_artifact_tool(filename, mock_tool_context)

        assert result['status'] == 'success'
        assert filename in result['report']
        assert 'data' in result
        assert result['data']['filename'] == filename
        mock_tool_context.load_artifact.assert_called_once()

    @pytest.mark.asyncio
    async def test_load_artifact_with_version(self, mock_tool_context):
        """Test loading artifact with specific version."""
        filename = "test_artifact.txt"
        version = 1
        mock_artifact = AsyncMock()
        mock_artifact.text = "Test content v1"
        mock_tool_context.load_artifact.return_value = mock_artifact
        
        result = await load_artifact_tool(filename, mock_tool_context, version=version)

        assert result['status'] == 'success'
        assert filename in result['report']
        assert str(version) in result['report']
        assert result['data']['version'] == version
        mock_tool_context.load_artifact.assert_called_once()

    @pytest.mark.asyncio
    async def test_load_artifact_no_filename(self, mock_tool_context):
        """Test loading artifact without filename."""
        result = await load_artifact_tool("", mock_tool_context)

        assert result['status'] == 'error'
        assert 'please specify an artifact filename' in result['report'].lower()


class TestToolReturnFormats:
    """Test that all tools return proper formats."""

    @pytest.mark.asyncio
    async def test_all_tools_return_dict(self, mock_tool_context):
        """Test that all tools return dictionary results."""
        mock_artifact = AsyncMock()
        mock_artifact.text = "Test content"
        mock_tool_context.load_artifact.return_value = mock_artifact
        mock_tool_context.list_artifacts.return_value = []
        
        test_cases = [
            extract_text_tool("test", mock_tool_context),
            summarize_document_tool("test", mock_tool_context),
            translate_document_tool("test", "Spanish", mock_tool_context),
            create_final_report_tool(mock_tool_context),
            list_artifacts_tool(mock_tool_context),
            load_artifact_tool("test.txt", mock_tool_context),
        ]

        for test_coro in test_cases:
            result = await test_coro
            assert isinstance(result, dict), f"Tool should return dict"
            assert 'status' in result, f"Tool should have status"
            assert 'report' in result, f"Tool should have report"

    @pytest.mark.asyncio
    async def test_tools_have_status_in_result(self, mock_tool_context):
        """Test that all tools include status in results."""
        mock_artifact = AsyncMock()
        mock_artifact.text = "Test content"
        mock_tool_context.load_artifact.return_value = mock_artifact
        mock_tool_context.list_artifacts.return_value = []
        
        test_cases = [
            extract_text_tool("test", mock_tool_context),
            summarize_document_tool("test", mock_tool_context),
            translate_document_tool("test", "French", mock_tool_context),
            create_final_report_tool(mock_tool_context),
            list_artifacts_tool(mock_tool_context),
            load_artifact_tool("test.txt", mock_tool_context),
        ]

        for test_coro in test_cases:
            result = await test_coro
            assert 'status' in result
            assert result['status'] in ['success', 'error']

    @pytest.mark.asyncio
    async def test_success_tools_have_data(self, mock_tool_context):
        """Test that successful tools include data field."""
        mock_artifact = AsyncMock()
        mock_artifact.text = "Test content"
        mock_tool_context.load_artifact.return_value = mock_artifact
        mock_tool_context.list_artifacts.return_value = []
        
        test_cases = [
            extract_text_tool("test document", mock_tool_context),
            summarize_document_tool("test document", mock_tool_context),
            translate_document_tool("test", "German", mock_tool_context),
            create_final_report_tool(mock_tool_context),
            list_artifacts_tool(mock_tool_context),
            load_artifact_tool("test.txt", mock_tool_context),
        ]

        for test_coro in test_cases:
            result = await test_coro
            if result['status'] == 'success':
                assert 'data' in result, f"Success result should have data: {result}"