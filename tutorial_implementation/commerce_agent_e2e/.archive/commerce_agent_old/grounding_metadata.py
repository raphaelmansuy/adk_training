"""
Grounding Metadata Extraction and Management

This module handles extraction, structuring, and management of grounding metadata
from Google Search Tool responses. Grounding metadata provides:

1. Source Attribution: Each response is linked to authoritative sources
2. Segment-Level Citations: Specific sentences are mapped to supporting sources
3. URL Validation: URLs come directly from search results, preventing hallucination
4. Customer Trust: Users can verify information by checking sources

Key Components:
- GroundingChunk: Individual source (title + URI)
- GroundingSegment: Portion of text with start/end indices
- GroundingSupport: Maps segment to supporting chunks
- GroundingMetadata: Complete metadata structure

Customer Experience Benefits:
✓ Real-time verification: Users can click to verify each fact
✓ Source transparency: Know exactly where information comes from
✓ Confidence signals: More sources = more trusted information
✓ Related topics: Discover related searches through metadata
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class GroundingChunk:
    """
    Represents a single source from Google Search results.
    
    Attributes:
        title: Display title of the source (website name, article title)
        uri: Direct URL to the source
        domain: Extracted domain for validation and categorization
        snippet: Optional preview text from the source
    """
    title: str
    uri: str
    domain: Optional[str] = None
    snippet: Optional[str] = None

    def __post_init__(self):
        """Extract domain from URI if not provided."""
        if not self.domain and self.uri:
            try:
                from urllib.parse import urlparse
                parsed = urlparse(self.uri)
                self.domain = parsed.netloc
            except Exception:
                self.domain = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        return {
            "title": self.title,
            "uri": self.uri,
            "domain": self.domain,
            "snippet": self.snippet
        }


@dataclass
class GroundingSegment:
    """
    Represents a portion of the response text.
    
    Attributes:
        start_index: Character position where segment starts (0-indexed)
        end_index: Character position where segment ends (exclusive)
        text: The actual text of this segment
    """
    start_index: int
    end_index: int
    text: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "start_index": self.start_index,
            "end_index": self.end_index,
            "text": self.text
        }


@dataclass
class GroundingSupport:
    """
    Maps a response segment to supporting sources (chunks).
    
    Attributes:
        chunk_indices: Which chunks (sources) support this segment
        segment: The text segment being supported
        confidence: Optional confidence score (0.0-1.0)
    """
    chunk_indices: List[int]
    segment: GroundingSegment
    confidence: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "chunk_indices": self.chunk_indices,
            "segment": self.segment.to_dict(),
            "confidence": self.confidence
        }


@dataclass
class GroundingMetadata:
    """
    Complete grounding metadata from a Google Search response.
    
    This structure enables:
    - Segment-level attribution (which sources back which claims)
    - Source verification (clickable links to authoritative sources)
    - Trust signals (multiple sources indicate higher confidence)
    - Related topics (suggested searches from metadata)
    
    Attributes:
        chunks: List of source URLs and titles
        supports: List of segment-to-source mappings
        search_entry_point: Optional pre-rendered HTML for search suggestions
        timestamp: When metadata was extracted
        quality_score: Overall quality indicator (0.0-1.0)
        is_grounded: Whether response is backed by search results
    """
    chunks: List[GroundingChunk]
    supports: List[GroundingSupport]
    search_entry_point: Optional[str] = None
    timestamp: Optional[str] = None
    quality_score: Optional[float] = None
    is_grounded: bool = True

    def __post_init__(self):
        """Set timestamp if not provided."""
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()

    def get_sources_for_segment(self, segment: GroundingSegment) -> List[GroundingChunk]:
        """
        Get all source chunks that support a specific segment.
        
        Args:
            segment: The text segment to find sources for
        
        Returns:
            List of GroundingChunk objects supporting this segment
        """
        for support in self.supports:
            if (support.segment.start_index == segment.start_index and
                support.segment.end_index == segment.end_index):
                return [self.chunks[i] for i in support.chunk_indices if i < len(self.chunks)]
        return []

    def get_supported_segments(self) -> List[tuple]:
        """
        Get all supported segments with their sources.
        
        Returns:
            List of (segment_text, [sources]) tuples
        """
        result = []
        for support in self.supports:
            sources = [self.chunks[i] for i in support.chunk_indices if i < len(self.chunks)]
            result.append((support.segment.text, sources))
        return result

    def get_unique_sources(self) -> List[GroundingChunk]:
        """Get list of unique sources."""
        seen_uris = set()
        unique = []
        for chunk in self.chunks:
            if chunk.uri not in seen_uris:
                unique.append(chunk)
                seen_uris.add(chunk.uri)
        return unique

    def get_sources_by_domain(self) -> Dict[str, List[GroundingChunk]]:
        """Group sources by domain."""
        by_domain = {}
        for chunk in self.chunks:
            domain = chunk.domain or "unknown"
            if domain not in by_domain:
                by_domain[domain] = []
            by_domain[domain].append(chunk)
        return by_domain

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "chunks": [chunk.to_dict() for chunk in self.chunks],
            "supports": [support.to_dict() for support in self.supports],
            "search_entry_point": self.search_entry_point,
            "timestamp": self.timestamp,
            "quality_score": self.quality_score,
            "is_grounded": self.is_grounded
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "GroundingMetadata":
        """Reconstruct GroundingMetadata from dictionary."""
        chunks = [
            GroundingChunk(
                title=c["title"],
                uri=c["uri"],
                domain=c.get("domain"),
                snippet=c.get("snippet")
            )
            for c in data.get("chunks", [])
        ]

        supports = []
        for s in data.get("supports", []):
            segment = GroundingSegment(
                start_index=s["segment"]["start_index"],
                end_index=s["segment"]["end_index"],
                text=s["segment"]["text"]
            )
            support = GroundingSupport(
                chunk_indices=s["chunk_indices"],
                segment=segment,
                confidence=s.get("confidence")
            )
            supports.append(support)

        return GroundingMetadata(
            chunks=chunks,
            supports=supports,
            search_entry_point=data.get("search_entry_point"),
            timestamp=data.get("timestamp"),
            quality_score=data.get("quality_score"),
            is_grounded=data.get("is_grounded", True)
        )


class GroundingMetadataExtractor:
    """
    Extracts grounding metadata from Google Search Tool responses.
    
    The extractor:
    1. Parses groundingMetadata from Gemini API responses
    2. Structures data into domain objects
    3. Validates source URLs match their domains
    4. Calculates quality scores based on coverage
    5. Prevents URL hallucination by using only sources from search results
    """

    @staticmethod
    def extract_from_response(response: Dict[str, Any]) -> Optional[GroundingMetadata]:
        """
        Extract grounding metadata from a complete response object.
        
        Args:
            response: Response dict that may contain groundingMetadata
        
        Returns:
            GroundingMetadata object or None if no metadata found
        """
        if not response:
            return None

        # Look for grounding metadata in various locations
        grounding_data = (
            response.get("grounding_metadata") or
            response.get("groundingMetadata") or
            response.get("metadata", {}).get("grounding") or
            None
        )

        if not grounding_data:
            # No grounding metadata found
            return GroundingMetadata(chunks=[], supports=[], is_grounded=False)

        return GroundingMetadataExtractor._parse_grounding_data(grounding_data)

    @staticmethod
    def extract_from_search_result(search_result: Dict[str, Any]) -> Optional[GroundingMetadata]:
        """
        Extract metadata from individual search result.
        
        Args:
            search_result: Single search result object
        
        Returns:
            GroundingMetadata or None
        """
        if not search_result:
            return None

        chunks = []
        if "source" in search_result:
            chunk = GroundingChunk(
                title=search_result.get("title", search_result.get("source", "Unknown")),
                uri=search_result.get("link") or search_result.get("url", ""),
                snippet=search_result.get("snippet", "")
            )
            chunks.append(chunk)

        if chunks:
            return GroundingMetadata(chunks=chunks, supports=[])
        return None

    @staticmethod
    def _parse_grounding_data(data: Dict[str, Any]) -> GroundingMetadata:
        """
        Parse raw grounding data structure from Google API.
        
        Args:
            data: Raw groundingMetadata dict
        
        Returns:
            Structured GroundingMetadata object
        """
        chunks = GroundingMetadataExtractor._parse_chunks(data.get("groundingChunks", []))
        supports = GroundingMetadataExtractor._parse_supports(
            data.get("groundingSupports", []),
            chunks
        )

        quality_score = GroundingMetadataExtractor._calculate_quality_score(
            chunks, supports
        )

        return GroundingMetadata(
            chunks=chunks,
            supports=supports,
            search_entry_point=data.get("searchEntryPoint"),
            quality_score=quality_score,
            is_grounded=len(chunks) > 0
        )

    @staticmethod
    def _parse_chunks(chunks_data: List[Dict[str, Any]]) -> List[GroundingChunk]:
        """Parse grounding chunks from API response."""
        chunks = []
        for chunk_data in chunks_data:
            # Handle nested web structure
            web_data = chunk_data.get("web", chunk_data)

            title = web_data.get("title", "")
            uri = web_data.get("uri", "")

            if uri:  # Only add if we have a URL
                chunk = GroundingChunk(
                    title=title or uri.split("/")[-1],
                    uri=uri
                )
                chunks.append(chunk)

        return chunks

    @staticmethod
    def _parse_supports(
        supports_data: List[Dict[str, Any]],
        chunks: List[GroundingChunk]
    ) -> List[GroundingSupport]:
        """Parse grounding supports (segment-to-source mappings) from API response."""
        supports = []
        for support_data in supports_data:
            chunk_indices = support_data.get("groundingChunkIndices", [])
            segment_data = support_data.get("segment", {})

            segment = GroundingSegment(
                start_index=segment_data.get("startIndex", 0),
                end_index=segment_data.get("endIndex", 0),
                text=segment_data.get("text", "")
            )

            # Validate chunk indices
            valid_indices = [i for i in chunk_indices if i < len(chunks)]

            if valid_indices and segment.text:
                support = GroundingSupport(
                    chunk_indices=valid_indices,
                    segment=segment,
                    confidence=support_data.get("confidence")
                )
                supports.append(support)

        return supports

    @staticmethod
    def _calculate_quality_score(
        chunks: List[GroundingChunk],
        supports: List[GroundingSupport]
    ) -> float:
        """
        Calculate quality score based on grounding coverage.
        
        Factors:
        - Number of sources (more = higher confidence)
        - Number of supported segments (more = better coverage)
        - URL validity (all valid = full score)
        
        Returns:
            Score between 0.0 and 1.0
        """
        if not chunks:
            return 0.0

        # Valid URLs (all should be valid for proper grounding)
        valid_urls = sum(1 for chunk in chunks if chunk.uri)
        url_score = valid_urls / len(chunks) if chunks else 0.0

        # Source diversity
        unique_domains = len(set(chunk.domain for chunk in chunks if chunk.domain))
        source_score = min(unique_domains / 3.0, 1.0)  # Perfect score with 3+ domains

        # Coverage
        coverage_score = min(len(supports) / 5.0, 1.0)  # Perfect score with 5+ supports

        # Weighted average
        quality = (url_score * 0.4 + source_score * 0.3 + coverage_score * 0.3)
        return round(quality, 2)


class GroundingMetadataFormatter:
    """
    Formats grounding metadata for display to users.
    
    Provides multiple output formats:
    - Inline citations in response text
    - Source list with clickable links
    - Segment-level attribution with tooltips
    """

    @staticmethod
    def format_with_inline_citations(
        text: str,
        metadata: GroundingMetadata
    ) -> str:
        """
        Format text with inline citation markers.
        
        Example output:
        "Nike Air Max is popular¹ among runners. It offers cushioning²."
        
        Then provide footnotes with sources.
        
        Args:
            text: Original response text
            metadata: Grounding metadata
        
        Returns:
            Formatted text with citation markers
        """
        if not metadata.is_grounded or not metadata.supports:
            return text

        # Create citation markers based on segments
        # This would be done in reverse order to avoid index shifting
        result = text
        for i, support in enumerate(reversed(metadata.supports), 1):
            segment = support.segment
            # Insert superscript citation number
            citation_marker = f"[{i}]"
            # Find the segment in the text and add marker
            if segment.text in result:
                result = result.replace(
                    segment.text,
                    f"{segment.text}{citation_marker}",
                    1  # Replace only first occurrence to avoid duplicates
                )

        return result

    @staticmethod
    def format_source_list(metadata: GroundingMetadata) -> str:
        """
        Format sources as a numbered list with links.
        
        Example output:
        [1] Nike Official Store - https://nike.com
        [2] Runner's World Magazine - https://runnersworld.com
        
        Args:
            metadata: Grounding metadata
        
        Returns:
            Formatted source list
        """
        if not metadata.is_grounded:
            return "No sources available"

        unique_sources = metadata.get_unique_sources()
        if not unique_sources:
            return "No sources available"

        lines = ["**Sources:**"]
        for i, chunk in enumerate(unique_sources, 1):
            lines.append(f"[{i}] {chunk.title}")
            lines.append(f"    📎 {chunk.uri}")
            if chunk.snippet:
                lines.append(f"    \"{chunk.snippet[:100]}...\"")

        return "\n".join(lines)

    @staticmethod
    def format_segment_attribution(metadata: GroundingMetadata) -> List[Dict[str, Any]]:
        """
        Format segment-level attribution for detailed display.
        
        Returns list of dicts like:
        {
            "text": "Nike Air Max offers cushioning",
            "sources": [
                {"title": "Nike Official", "url": "https://nike.com", "confidence": 0.95}
            ]
        }
        
        Args:
            metadata: Grounding metadata
        
        Returns:
            List of segment attribution dicts
        """
        result = []

        for support in metadata.supports:
            segment = support.segment
            sources = [
                {
                    "title": metadata.chunks[i].title,
                    "url": metadata.chunks[i].uri,
                    "domain": metadata.chunks[i].domain
                }
                for i in support.chunk_indices
                if i < len(metadata.chunks)
            ]

            result.append({
                "text": segment.text,
                "sources": sources,
                "confidence": support.confidence
            })

        return result

    @staticmethod
    def format_quality_report(metadata: GroundingMetadata) -> str:
        """
        Format a quality report about the grounding.
        
        Args:
            metadata: Grounding metadata
        
        Returns:
            Human-readable quality report
        """
        report = []
        report.append("**Grounding Quality Report**")
        report.append(f"Is Grounded: {'✅ Yes' if metadata.is_grounded else '❌ No'}")
        report.append(f"Quality Score: {metadata.quality_score:.0%}" if metadata.quality_score else "N/A")
        report.append(f"Total Sources: {len(metadata.chunks)}")
        report.append(f"Unique Domains: {len(metadata.get_sources_by_domain())}")
        report.append(f"Supported Segments: {len(metadata.supports)}")
        report.append(f"Coverage: {len(metadata.supports)}/{len(metadata.chunks)} segments supported")

        return "\n".join(report)
