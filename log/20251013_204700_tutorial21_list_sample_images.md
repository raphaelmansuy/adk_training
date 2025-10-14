# Tutorial 21: Added list_sample_images Tool

**Date**: 2025-10-13 20:47:00
**Status**: ✅ Complete
**Enhancement**: Added tool to list available sample images

## What Was Added

Created a new `list_sample_images()` tool that allows users to discover what
sample product images are available in the `_sample_images/` directory.

## Motivation

Users need an easy way to:
1. Discover what sample images are available
2. See image details (size, dimensions, format)
3. Get guidance on how to use sample images

## Implementation

### New Tool: list_sample_images()

**Function**: `async def list_sample_images(tool_context: ToolContext)`

**Returns**:
```python
{
    'status': 'success',
    'report': 'Found 3 sample image(s) in _sample_images/',
    'available_images': [
        {
            'filename': 'laptop.jpg',
            'path': '/path/to/_sample_images/laptop.jpg',
            'size': '38.5 KB',
            'dimensions': '800x533',
            'format': 'JPG'
        },
        # ... more images
    ],
    'directory': '/path/to/_sample_images',
    'usage_hint': 'Use analyze_product_image(product_id, image_path) to analyze...'
}
```

**Features**:
- Scans `_sample_images/` directory for image files
- Supports: .jpg, .jpeg, .png, .webp, .heic
- Extracts file size and dimensions (if PIL available)
- Returns structured data for each image
- Handles missing directory gracefully

### Updated Root Agent

**Added to instruction**:
- Mentions sample images directory
- Guides users to use `list_sample_images()` tool
- Suggests sample images when users explore capabilities
- Lists sample image names (laptop, headphones, smartwatch)

**New tool added**: `FunctionTool(list_sample_images)` (now 4 tools total)

## Test Coverage

### New Tests

**tests/test_multimodal.py** - TestListSampleImages class:
- `test_list_sample_images_with_images`: Verifies tool works with real images
- `test_list_sample_images_structure`: Validates return structure

**tests/test_agent.py**:
- Updated tool count: `>= 4` (was `>= 3`)
- Updated expected tools: added `'list_sample_images'`

**tests/test_imports.py**:
- Added import validation for `list_sample_images`

## Test Results

```bash
68 passed in 4.58s (was 66)
Coverage: 73%
```

## User Experience

**Before**:
```
User: What images are available?
Agent: I'm not sure. You can check the _sample_images directory.
```

**After**:
```
User: What images are available?
Agent: [calls list_sample_images tool]

I found 3 sample images:

1. **laptop.jpg** (38.5 KB, 800x533px)
   - Path: tutorial_implementation/tutorial21/_sample_images/laptop.jpg
   
2. **headphones.jpg** (41.1 KB, 800x533px)
   - Path: tutorial_implementation/tutorial21/_sample_images/headphones.jpg
   
3. **smartwatch.jpg** (53.3 KB, 800x533px)
   - Path: tutorial_implementation/tutorial21/_sample_images/smartwatch.jpg

You can analyze any of these using:
analyze_product_image("PROD_ID", "path/to/image.jpg")
```

## Example Usage

### In ADK Web Interface

1. User: "What sample images do you have?"
2. Agent calls `list_sample_images()`
3. Agent presents formatted list with details
4. User can then request analysis of specific images

### Programmatic Usage

```python
from vision_catalog_agent import root_agent
from google.adk.agents import Runner

runner = Runner()
result = await runner.run_async(
    "List available sample images",
    agent=root_agent
)
print(result.content.parts[0].text)
```

## Files Modified

1. `vision_catalog_agent/agent.py`:
   - Added `list_sample_images()` function (~70 lines)
   - Updated root_agent instruction (~45 lines)
   - Added FunctionTool(list_sample_images) to root_agent

2. `tests/test_agent.py`:
   - Updated tool count assertion
   - Updated expected tool names

3. `tests/test_imports.py`:
   - Added list_sample_images import test

4. `tests/test_multimodal.py`:
   - Added TestListSampleImages class with 2 tests

5. `log/20251013_204700_tutorial21_list_sample_images.md` - This log

## Benefits

1. **Discovery**: Users can easily find available samples
2. **Guidance**: Tool provides usage hints
3. **Details**: Shows image specs (size, dimensions, format)
4. **Onboarding**: New users can explore capabilities
5. **Transparency**: Clear visibility into what's available

## Technical Details

- Uses `Path.iterdir()` to scan directory
- Filters by extension: `.jpg`, `.jpeg`, `.png`, `.webp`, `.heic`
- Gets file stats with `stat().st_size`
- Optionally reads dimensions with PIL
- Handles missing directory gracefully (returns info status)
- Sorts results alphabetically by filename

## Integration

The tool integrates seamlessly with existing workflow:

1. User discovers images with `list_sample_images()`
2. User selects an image to analyze
3. Agent uses `analyze_product_image(id, path)` for analysis
4. Catalog entry is generated and saved

## Summary

Added `list_sample_images()` tool to Tutorial 21, making it easy for users to
discover and explore available sample product images. The tool provides detailed
information about each image and guides users on how to use them. All 68 tests
passing with 73% coverage.
