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

"""Callbacks for extracting grounding metadata from Google Search results.

This module provides function-based callbacks for observability and source attribution tracking.
ADK uses function-based callbacks following the pattern:
- before_agent, after_agent
- before_model, after_model
- before_tool, after_tool

Example usage:
    from commerce_agent.callbacks import create_grounding_callback
    from google.adk.agents import Agent
    
    agent = Agent(
        name="my_agent",
        model="gemini-2.5-flash",
        after_model=create_grounding_callback(verbose=True)
    )
"""

from .types import GroundingMetadata, GroundingSource, GroundingSupport


def _extract_domain(url: str) -> str:
    """Extract domain name from URL.
    
    Args:
        url: Full URL
        
    Returns:
        Domain name (e.g., "decathlon.com")
    """
    try:
        # Remove protocol
        if "://" in url:
            url = url.split("://", 1)[1]
        
        # Extract domain (before first /)
        domain = url.split("/")[0]
        
        # Remove www. prefix
        if domain.startswith("www."):
            domain = domain[4:]
        
        return domain
    except Exception:
        return "unknown"


def _calculate_confidence(num_sources: int) -> str:
    """Calculate confidence level based on number of sources.
    
    Args:
        num_sources: Number of sources supporting a claim
        
    Returns:
        Confidence level: "high", "medium", or "low"
    """
    if num_sources >= 3:
        return "high"
    elif num_sources >= 2:
        return "medium"
    else:
        return "low"


def create_grounding_callback(verbose: bool = True):
    """Create a grounding metadata extraction callback.
    
    This function returns an after_model callback that extracts grounding metadata
    from Google Search results.
    
    Args:
        verbose: If True, print grounding information to console
        
    Returns:
        Async callback function for use in Agent(after_model=...)
        
    Example:
        agent = Agent(
            name="search_agent",
            model="gemini-2.5-flash",
            tools=[google_search],
            after_model=create_grounding_callback(verbose=True)
        )
    """
    
    async def extract_grounding_metadata(callback_context, llm_response):
        """Extract grounding metadata from LLM response.
        
        Args:
            callback_context: ADK callback context with state
            llm_response: LLM response with potential grounding metadata
        """
        # Check if response has grounding metadata
        if not hasattr(llm_response, 'candidates') or not llm_response.candidates:
            return None
        
        candidate = llm_response.candidates[0]
        if not hasattr(candidate, 'grounding_metadata') or not candidate.grounding_metadata:
            return None
        
        # Extract grounding metadata
        metadata = candidate.grounding_metadata
        
        # Extract source information
        sources: list[GroundingSource] = []
        if hasattr(metadata, 'grounding_chunks') and metadata.grounding_chunks:
            for chunk in metadata.grounding_chunks:
                if hasattr(chunk, 'web') and chunk.web:
                    domain = _extract_domain(chunk.web.uri) if chunk.web.uri else None
                    source: GroundingSource = {
                        "title": chunk.web.title or "Unknown",
                        "uri": chunk.web.uri or "",
                        "domain": domain
                    }
                    sources.append(source)
        
        # Extract grounding supports (segment-level attribution)
        supports: list[GroundingSupport] = []
        if hasattr(metadata, 'grounding_supports') and metadata.grounding_supports:
            for support in metadata.grounding_supports:
                if hasattr(support, 'segment') and support.segment:
                    segment = support.segment
                    
                    # Calculate confidence based on number of supporting sources
                    num_sources = len(support.grounding_chunk_indices) if hasattr(support, 'grounding_chunk_indices') else 0
                    confidence = _calculate_confidence(num_sources)
                    
                    support_item: GroundingSupport = {
                        "text": segment.text if hasattr(segment, 'text') else "",
                        "start_index": segment.start_index if hasattr(segment, 'start_index') else 0,
                        "end_index": segment.end_index if hasattr(segment, 'end_index') else 0,
                        "source_indices": list(support.grounding_chunk_indices) if hasattr(support, 'grounding_chunk_indices') else [],
                        "confidence": confidence
                    }
                    supports.append(support_item)
        
        # Create complete metadata structure
        grounding_data: GroundingMetadata = {
            "sources": sources,
            "supports": supports,
            "search_suggestions": [],  # Could be extracted from search_entry_point
            "total_sources": len(sources)
        }
        
        # Store in session state (temporary scope for current invocation)
        if hasattr(callback_context, 'state'):
            callback_context.state["temp:_grounding_sources"] = sources
            callback_context.state["temp:_grounding_metadata"] = grounding_data
        
        # Log for debugging
        if verbose:
            print(f"\n{'='*60}")
            print("✓ GROUNDING METADATA EXTRACTED")
            print(f"{'='*60}")
            print(f"Total Sources: {len(sources)}")
            
            if sources:
                print("\nSources:")
                for i, source in enumerate(sources, 1):
                    domain = source.get("domain", "unknown")
                    title = source.get("title", "Unknown")
                    print(f"  {i}. [{domain}] {title}")
            
            if supports:
                print(f"\nGrounding Supports: {len(supports)} segments")
                for i, support in enumerate(supports[:3], 1):  # Show first 3
                    text = support["text"][:60] + "..." if len(support["text"]) > 60 else support["text"]
                    confidence = support.get("confidence", "unknown")
                    num_sources = len(support["source_indices"])
                    print(f"  {i}. [{confidence}] \"{text}\" ({num_sources} sources)")
                
                if len(supports) > 3:
                    print(f"  ... and {len(supports) - 3} more")
            
            print(f"{'='*60}\n")
        
        return None  # ADK callbacks return None or ModelContent
    
    return extract_grounding_metadata


__all__ = ["create_grounding_callback"]
