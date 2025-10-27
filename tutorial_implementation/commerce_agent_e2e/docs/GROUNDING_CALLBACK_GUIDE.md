# Grounding Metadata Callback - Usage Guide

This guide shows how to use the `create_grounding_callback` function to extract and monitor Google Search grounding metadata.

## Overview

The `create_grounding_callback` function creates an ADK after_model callback that extracts source attribution information from Google Search results, providing:
- ✅ Source URLs and titles from grounding chunks
- ✅ Segment-level attribution (which sources support which claims)
- ✅ Confidence scores based on multi-source agreement
- ✅ Domain extraction for retailer identification
- ✅ Console logging for debugging

## Quick Start

### Basic Usage

```python
from commerce_agent import root_agent, create_grounding_callback
from google.adk.agents import Agent

# Create agent with grounding callback
agent_with_callback = Agent(
    name=root_agent.name,
    model=root_agent.model,
    description=root_agent.description,
    instruction=root_agent.instruction,
    tools=root_agent.tools,
    after_model=create_grounding_callback(verbose=True)  # Enable grounding metadata extraction
)

# Or use Runner with the callback
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name="commerce_agent",
    session_service=session_service,
    after_model_callbacks=[create_grounding_callback(verbose=True)]
)

# Run agent
session = await session_service.create_session(
    app_name="commerce_agent",
    user_id="user123",
    session_id="session456"
)

result = await runner.run_async(
    user_id="user123",
    session_id="session456",
    new_message={"role": "user", "parts": [{"text": "Show me trail running shoes under €100"}]}
)
```

### Silent Mode (No Console Output)

```python
# Disable verbose logging
agent_with_callback = Agent(
    name="commerce_agent",
    model="gemini-2.5-flash",
    tools=[...],
    after_model=create_grounding_callback(verbose=False)
)
```

## What Gets Extracted

### 1. Grounding Sources

Each source includes:
```python
{
    "title": "Brooks Divide 5 - Trail Running Shoes",
    "uri": "https://www.decathlon.com.hk/brooks-divide-5",
    "domain": "decathlon.com.hk"
}
```

### 2. Grounding Supports (Segment Attribution)

Each segment shows which sources support specific claims:
```python
{
    "text": "Brooks Divide 5 costs €95 and is ideal for beginners",
    "start_index": 45,
    "end_index": 98,
    "source_indices": [0, 2],  # Supported by sources at index 0 and 2
    "confidence": "high"  # 2+ sources = high confidence
}
```

### 3. Complete Metadata Structure

```python
{
    "sources": [...],  # List of GroundingSource
    "supports": [...],  # List of GroundingSupport
    "search_suggestions": [...],  # Optional search suggestions
    "total_sources": 5  # Total unique sources
}
```

## Accessing Extracted Data

The callback stores data in the event state:

```python
async for event in runner.run_async(...):
    if event.is_final_response():
        # Get sources list
        sources = event.state.get("temp:_grounding_sources", [])
        
        # Get complete metadata
        metadata = event.state.get("temp:_grounding_metadata", {})
        
        print(f"Found {len(sources)} sources")
        for source in sources:
            print(f"  - [{source['domain']}] {source['title']}")
```

## Example Console Output

When `verbose=True` (default), the callback prints:

```
============================================================
✓ GROUNDING METADATA EXTRACTED
============================================================
Total Sources: 5

Sources:
  1. [decathlon.com.hk] Brooks Divide 5 - Trail Running Shoes
  2. [alltricks.com] Brooks Divide 5 Review
  3. [runningwarehouse.com] Brooks Divide 5 - Men's Trail Running Shoes
  4. [sportsdirect.com] Brooks Running Shoes Collection
  5. [nike.com] Trail Running Shoes Guide

Grounding Supports: 12 segments
  1. [high] "Brooks Divide 5 costs €95 and is ideal for beginners" (3 sources)
  2. [medium] "Comfortable cushioning for mixed terrain" (2 sources)
  3. [low] "Available in 4 color options" (1 sources)
  ... and 9 more
============================================================
```

## Confidence Levels

The callback calculates confidence based on source agreement:

| Sources | Confidence | Meaning |
|---------|-----------|----------|
| 3+ | **high** | Multiple sources confirm this claim |
| 2 | **medium** | Two sources agree |
| 1 | **low** | Single source only |

## Use Cases

### 1. Debugging Search Quality

Check which sources are being used:
```python
callback = GroundingMetadataCallback(verbose=True)
# See console output showing all sources
```

### 2. UI Display of Citations

Show users where information comes from:
```python
sources = event.state.get("temp:_grounding_sources", [])
for source in sources:
    print(f"Source: {source['title']}")
    print(f"URL: {source['uri']}")
```

### 3. URL Verification

Prevent URL hallucination by checking actual sources:
```python
metadata = event.state.get("temp:_grounding_metadata", {})
valid_domains = {s['domain'] for s in metadata['sources']}

# Verify any URLs mentioned in response are from real sources
if "decathlon.com" in valid_domains:
    print("✓ Decathlon links are verified")
```

### 4. Quality Monitoring

Track grounding quality over time:
```python
metadata = event.state.get("temp:_grounding_metadata", {})

# Calculate quality score
high_conf_segments = [s for s in metadata['supports'] if s.get('confidence') == 'high']
quality_score = len(high_conf_segments) / len(metadata['supports'])

print(f"Quality Score: {quality_score:.1%}")
```

## Integration with Tests

```python
import pytest
from commerce_agent import root_agent, GroundingMetadataCallback

@pytest.mark.asyncio
async def test_grounding_metadata_extraction():
    """Test that grounding metadata is properly extracted."""
    runner = Runner(
        agent=root_agent,
        callbacks=[GroundingMetadataCallback(verbose=False)]
    )
    
    # Run query
    async for event in runner.run_async(...):
        if event.is_final_response():
            # Verify metadata was extracted
            sources = event.state.get("temp:_grounding_sources", [])
            assert len(sources) > 0, "Should extract grounding sources"
            
            # Verify source structure
            for source in sources:
                assert "title" in source
                assert "uri" in source
                assert "domain" in source
```

## Type Safety

All callback types are defined with TypedDict:

```python
from commerce_agent.types import (
    GroundingMetadata,
    GroundingSource,
    GroundingSupport
)

# Full type safety with IDE autocomplete
def process_sources(sources: list[GroundingSource]) -> None:
    for source in sources:
        print(source["title"])  # IDE knows this exists
        print(source["uri"])    # Autocomplete works
        print(source["domain"]) # Type-checked
```

## Best Practices

1. **Always use verbose=True during development** for debugging
2. **Set verbose=False in production** to avoid log spam
3. **Access metadata immediately in final response** (temp: scope)
4. **Validate URLs against grounding sources** to prevent hallucination
5. **Monitor quality scores** to track search result quality over time
6. **Display sources to users** for transparency and trust

## Troubleshooting

### No metadata extracted
- Ensure agent uses `GoogleSearchTool(bypass_multi_tools_limit=True)`
- Check that model is Gemini 2.0+
- Verify query triggers Google Search

### Missing domains
- Some URLs may not parse correctly
- Fallback domain is "unknown"
- Check console output for parsing issues

### Empty supports list
- Some responses may not have segment-level attribution
- This is normal for certain types of search results
- Sources list should still be populated

## Next Steps

- Review the TypedDict definitions in `commerce_agent/types.py`
- Check the callback implementation in `commerce_agent/callbacks.py`
- Run tests with `make test` to see callback in action
- Try different queries to see varying grounding patterns
