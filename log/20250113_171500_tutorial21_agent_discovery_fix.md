# Tutorial 21 - Agent Discovery Fix

**Date**: 2025-01-13 17:15
**Issue**: ADK agent discovery conflict
**Status**: ✅ Resolved

## Problem

When running `adk web`, ADK was attempting to discover `sample_images` directory as an agent, causing errors:

```
ValueError: No root_agent found for 'sample_images'. Searched in 'sample_images.agent.root_agent', 'sample_images.root_agent' and 'sample_images/root_agent.yaml'.
```

## Root Cause

ADK automatically scans all directories in the project root for potential agents. The `sample_images/` directory was being incorrectly identified as a potential agent package.

## Solution

Renamed `sample_images/` to `_sample_images/`. ADK automatically ignores directories that start with:
- `_` (underscore)
- `.` (dot)

This is ADK's built-in convention for excluding utility/data directories from agent discovery.

## Files Updated

1. **vision_catalog_agent/agent.py**
   - Updated sample directory path reference

2. **demo.py**
   - Updated sample directory path reference

3. **Makefile**
   - Updated demo examples with new path

4. **tests/test_structure.py**
   - Updated test expectations for directory name

5. **.adkignore**
   - Added documentation about underscore prefix convention

## Verification

```bash
# Tests pass
pytest tests/ --tb=no -q
# Result: 63 passed in 4.76s

# Agent imports correctly
python -c "from vision_catalog_agent import root_agent; print(root_agent.name)"
# Result: vision_catalog_coordinator

# ADK web now works correctly
# Only vision_catalog_agent appears in dropdown
```

## Key Learnings

1. **Directory Naming Convention**: Use `_` or `.` prefix for non-agent directories
2. **ADK Discovery**: ADK recursively scans for agent packages
3. **Best Practice**: Organize utility directories with underscore prefix

## Impact

- ✅ ADK web interface works correctly
- ✅ Only `vision_catalog_agent` appears in agent selector
- ✅ All 63 tests pass
- ✅ No breaking changes to agent functionality
