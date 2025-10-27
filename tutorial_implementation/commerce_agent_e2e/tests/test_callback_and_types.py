# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for grounding metadata callback and type safety."""

import pytest
from commerce_agent import create_grounding_callback
from commerce_agent.callbacks import _extract_domain, _calculate_confidence
from commerce_agent.types import (
    ToolResult,
    UserPreferences,
    GroundingSource,
    GroundingSupport,
    GroundingMetadata
)
from commerce_agent.tools.preferences import save_preferences, get_preferences
from unittest.mock import Mock


class TestGroundingMetadataCallback:
    """Test the grounding metadata callback function."""
    
    def test_callback_creation(self):
        """Test callback function can be created."""
        callback = create_grounding_callback(verbose=True)
        assert callback is not None
        assert callable(callback)
        
        callback_silent = create_grounding_callback(verbose=False)
        assert callable(callback_silent)
    
    def test_extract_domain(self):
        """Test domain extraction from URLs."""
        # Test various URL formats
        assert _extract_domain("https://www.decathlon.com.hk/product") == "decathlon.com.hk"
        assert _extract_domain("http://example.com/path") == "example.com"
        assert _extract_domain("https://subdomain.example.com") == "subdomain.example.com"
        assert _extract_domain("www.test.com") == "test.com"
        assert _extract_domain("invalid-url") == "invalid-url"
    
    def test_calculate_confidence(self):
        """Test confidence level calculation."""
        assert _calculate_confidence(0) == "low"
        assert _calculate_confidence(1) == "low"
        assert _calculate_confidence(2) == "medium"
        assert _calculate_confidence(3) == "high"
        assert _calculate_confidence(5) == "high"
    
    @pytest.mark.asyncio
    async def test_callback_no_candidates(self):
        """Test callback handles responses without candidates."""
        callback = create_grounding_callback(verbose=False)
        
        # Mock callback context and response without candidates
        callback_context = Mock()
        callback_context.state = {}
        llm_response = Mock()
        llm_response.candidates = []
        
        # Should not raise error and return None
        result = await callback(callback_context, llm_response)
        assert result is None
    
    @pytest.mark.asyncio
    async def test_callback_with_metadata(self):
        """Test callback extracts grounding metadata from response."""
        callback = create_grounding_callback(verbose=False)
        
        # Mock callback context
        callback_context = Mock()
        callback_context.state = {}
        
        # Mock grounding chunks
        chunk1 = Mock()
        chunk1.web = Mock()
        chunk1.web.title = "Decathlon - Brooks Divide 5"
        chunk1.web.uri = "https://www.decathlon.com.hk/brooks-divide-5"
        
        chunk2 = Mock()
        chunk2.web = Mock()
        chunk2.web.title = "AllTricks - Running Shoes"
        chunk2.web.uri = "https://www.alltricks.com/running-shoes"
        
        # Mock grounding supports
        support1 = Mock()
        support1.segment = Mock()
        support1.segment.text = "Brooks Divide 5 costs €95"
        support1.segment.start_index = 0
        support1.segment.end_index = 26
        support1.grounding_chunk_indices = [0, 1]
        
        # Set up candidate with metadata
        candidate = Mock()
        candidate.grounding_metadata = Mock()
        candidate.grounding_metadata.grounding_chunks = [chunk1, chunk2]
        candidate.grounding_metadata.grounding_supports = [support1]
        
        # Mock response
        llm_response = Mock()
        llm_response.candidates = [candidate]
        
        # Process response
        result = await callback(callback_context, llm_response)
        
        # Verify return value
        assert result is None
        
        # Verify state was updated
        assert "temp:_grounding_sources" in callback_context.state
        assert "temp:_grounding_metadata" in callback_context.state
        
        # Verify sources
        sources = callback_context.state["temp:_grounding_sources"]
        assert len(sources) == 2
        assert sources[0]["title"] == "Decathlon - Brooks Divide 5"
        assert sources[0]["domain"] == "decathlon.com.hk"
        
        # Verify metadata
        metadata = callback_context.state["temp:_grounding_metadata"]
        assert metadata["total_sources"] == 2
        assert len(metadata["supports"]) == 1
        assert metadata["supports"][0]["confidence"] == "medium"  # 2 sources


class TestToolTypes:
    """Test TypedDict definitions work correctly."""
    
    def test_tool_result_success(self):
        """Test ToolResult for successful operation."""
        result: ToolResult = {
            "status": "success",
            "report": "Operation completed",
            "data": {"value": 42}
        }
        
        assert result["status"] == "success"
        assert result["report"] == "Operation completed"
        assert result["data"]["value"] == 42
    
    def test_tool_result_error(self):
        """Test ToolResult for error case."""
        result: ToolResult = {
            "status": "error",
            "report": "Operation failed",
            "error": "ValueError: Invalid input"
        }
        
        assert result["status"] == "error"
        assert "error" in result
    
    def test_user_preferences_structure(self):
        """Test UserPreferences structure."""
        prefs: UserPreferences = {
            "sport": "running",
            "budget_max": 100,
            "experience_level": "beginner"
        }
        
        assert prefs["sport"] == "running"
        assert prefs["budget_max"] == 100
        assert prefs["experience_level"] == "beginner"
    
    def test_grounding_source_structure(self):
        """Test GroundingSource structure."""
        source: GroundingSource = {
            "title": "Product Page",
            "uri": "https://example.com/product",
            "domain": "example.com"
        }
        
        assert source["title"] == "Product Page"
        assert source["uri"] == "https://example.com/product"
        assert source["domain"] == "example.com"
    
    def test_grounding_support_structure(self):
        """Test GroundingSupport structure."""
        support: GroundingSupport = {
            "text": "Product costs €95",
            "start_index": 0,
            "end_index": 18,
            "source_indices": [0, 1],
            "confidence": "high"
        }
        
        assert support["text"] == "Product costs €95"
        assert len(support["source_indices"]) == 2
        assert support["confidence"] == "high"
    
    def test_grounding_metadata_structure(self):
        """Test complete GroundingMetadata structure."""
        metadata: GroundingMetadata = {
            "sources": [
                {
                    "title": "Source 1",
                    "uri": "https://example.com/1",
                    "domain": "example.com"
                }
            ],
            "supports": [
                {
                    "text": "Sample text",
                    "start_index": 0,
                    "end_index": 11,
                    "source_indices": [0],
                    "confidence": "low"
                }
            ],
            "search_suggestions": ["related search"],
            "total_sources": 1
        }
        
        assert len(metadata["sources"]) == 1
        assert len(metadata["supports"]) == 1
        assert metadata["total_sources"] == 1


class TestPreferencesWithTypes:
    """Test that preference tools return ToolResult-compatible dicts."""
    
    def test_save_preferences_return_type(self):
        """Test save_preferences returns dict matching ToolResult structure."""
        # Mock tool context - ADK v1.17+ uses tool_context.state directly
        tool_context = Mock()
        tool_context.state = {}
        
        # Call function
        result = save_preferences(
            sport="running",
            budget_max=100,
            experience_level="beginner",
            tool_context=tool_context
        )
        
        # Verify return type structure
        assert "status" in result
        assert "report" in result
        assert result["status"] == "success"
        assert "data" in result
        
        # Verify state was updated
        assert tool_context.state["user:pref_sport"] == "running"
        assert tool_context.state["user:pref_budget"] == 100
        assert tool_context.state["user:pref_experience"] == "beginner"
    
    def test_get_preferences_return_type(self):
        """Test get_preferences returns dict matching ToolResult structure."""
        # Mock tool context with existing preferences - ADK v1.17+ uses tool_context.state
        tool_context = Mock()
        tool_context.state = {
            "user:pref_sport": "cycling",
            "user:pref_budget": 200,
            "user:pref_experience": "intermediate"
        }
        
        # Call function
        result = get_preferences(tool_context=tool_context)
        
        # Verify return type structure
        assert "status" in result
        assert "report" in result
        assert result["status"] == "success"
        assert "data" in result
        
        # Verify data
        assert result["data"]["sport"] == "cycling"
        assert result["data"]["budget_max"] == 200
        assert result["data"]["experience_level"] == "intermediate"
    
    def test_get_preferences_empty_state(self):
        """Test get_preferences with no saved preferences."""
        # Mock tool context with empty state - ADK v1.17+ uses tool_context.state
        tool_context = Mock()
        tool_context.state = {}
        
        # Call function
        result = get_preferences(tool_context=tool_context)
        
        # Verify returns success with empty data
        assert result["status"] == "success"
        assert result["data"] == {}
        assert "No preferences" in result["report"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
