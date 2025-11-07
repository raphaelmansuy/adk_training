# Fix: BasePlanner Method Signatures in Documentation

**Date**: 2025-11-07
**Issue**: MyCustomPlanner.process_planning_response() takes 2 positional arguments but 3 were given
**Status**: ✅ Resolved

## Problem

The documentation for Tutorial 12 (Planners & Thinking) showed outdated method signatures for `BasePlanner` custom implementations. This would cause runtime errors when users implemented planners following the documentation.

### Old (Incorrect) Signature in Documentation

```python
def build_planning_instruction(self, agent, context) -> str:
    """Inject custom planning instructions."""
    return "..."

def process_planning_response(self, response: LlmResponse) -> LlmResponse:
    """Process response after planning."""
    return response
```

### Actual API Signature (from google-adk 1.18.0)

```python
def build_planning_instruction(
    self,
    readonly_context: ReadonlyContext,
    llm_request: LlmRequest,
) -> Optional[str]:
    """Build planning instruction."""
    return "..."

def process_planning_response(
    self,
    callback_context: CallbackContext,
    response_parts: List[types.Part],
) -> Optional[List[types.Part]]:
    """Process planning response."""
    return response_parts
```

## Root Cause

The documentation in `docs/docs/12_planners_thinking.md` contained outdated API examples that didn't match the current ADK API (1.15.0+). The method signatures for `BasePlanner` abstract methods had changed between versions, but the documentation wasn't updated.

## Impact

Users implementing custom planners by following the documentation would encounter:
- `TypeError: MyCustomPlanner.process_planning_response() takes 2 positional arguments but 3 were given`
- Confusion about the correct implementation pattern
- Failed agent execution at runtime

## Solution

Updated all custom planner examples in the documentation with:

1. **Correct import statements**:
   ```python
   from google.adk.agents.callback_context import CallbackContext
   from google.adk.agents.readonly_context import ReadonlyContext
   from google.adk.models.llm_request import LlmRequest
   from google.genai import types
   from typing import List, Optional
   ```

2. **Correct method signatures** for both abstract methods:
   - `build_planning_instruction(readonly_context, llm_request) -> Optional[str]`
   - `process_planning_response(callback_context, response_parts) -> Optional[List[types.Part]]`

3. **Proper type hints and docstrings** following ADK conventions

## Files Changed

- `docs/docs/12_planners_thinking.md`:
  - Updated `MyCustomPlanner` example (lines 784-855)
  - Updated `DataSciencePlanner` example (lines 860-938)

## Verification

The implementation in `tutorial_implementation/tutorial12/strategic_solver/agent.py` was already correct:
- `StrategicPlanner` class uses correct signatures
- All 60 tests pass (100% for relevant test cases)
- Implementation matches current ADK API (1.18.0)

## Testing

```bash
cd tutorial_implementation/tutorial12
python3 -m pytest tests/test_agents.py::TestStrategicPlanner -v
# Result: All 3 tests passed ✅
```

## Prevention

- Documentation examples should reference actual working implementations
- Consider automated checks for API signature changes in documentation
- Keep documentation synchronized with minimum required ADK version (1.15.0+)

## Related

- Google ADK version: 1.15.0+ (tested with 1.18.0)
- Tutorial 12: Planners & Thinking Configuration
- BasePlanner abstract class in `google.adk.planners`
