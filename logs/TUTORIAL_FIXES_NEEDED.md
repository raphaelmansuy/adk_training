# Tutorial Fixes Needed - Package Name Corrections

## Critical Issue Discovered

The tutorials use incorrect package name `adk-middleware` which does not exist on PyPI.

**Correct package**: `ag_ui_adk`

## Root Cause

The research phase identified CopilotKit's AG-UI Protocol but incorrectly assumed a package called `adk-middleware` existed. The actual package is `ag_ui_adk`.

Additionally, the tutorials use the OLD ADK API (`genai.Client().agentic.create_agent()`) but the `ag_ui_adk` integration requires the NEW ADK API (`google.adk.agents.LlmAgent`).

## Affected Tutorials

- ✅ **Tutorial 29** - FIXED
- ⏳ **Tutorial 30** - IN PROGRESS (complex fixes needed)
- ⏳ **Tutorial 31** - NOT STARTED
- ✅ **Tutorial 32** - NO CHANGES NEEDED (uses direct ADK, no CopilotKit)
- ✅ **Tutorial 33** - NO CHANGES NEEDED (uses direct ADK, no CopilotKit)  
- ✅ **Tutorial 34** - NO CHANGES NEEDED (uses direct ADK, no CopilotKit)
- ⏳ **Tutorial 35** - NOT STARTED

## Changes Required

### Tutorial 29 ✅ (COMPLETE)

**Status**: Fixed
**Changes**:
- ✅ `pip install adk-middleware` → `pip install ag_ui_adk`
- ✅ `from adk_middleware import` → `from ag_ui_adk import`  
- ✅ Updated agent structure to use `google.adk.agents.LlmAgent`
- ✅ Updated architecture diagram
- ✅ Updated comparison table

### Tutorial 30 ⏳ (IN PROGRESS)

**Status**: Needs major rewrite
**Changes needed**:
1. Replace `pip install adk-middleware` with `pip install ag_ui_adk`
2. Replace `adk-middleware>=0.1.0` in requirements.txt with `ag_ui_adk>=0.1.0`
3. Replace ALL agent code:
   - Remove `genai.Client().agentic.create_agent()`
   - Use `google.adk.agents.LlmAgent` instead
   - Change tool definition from `Tool(function_declarations=[...])` to direct Python functions
   - Remove `create_copilotkit_runtime()` (doesn't exist)
   - Use `ADKAgent` wrapper + `add_adk_fastapi_endpoint()`
4. Update architecture diagram
5. Update all text references to `adk-middleware`

**Critical**: Tools defined with ADK's old API need conversion:
- OLD: `Tool(function_declarations=[FunctionDeclaration(...)])`
- NEW: Just pass Python functions directly to `tools=[func1, func2]`

### Tutorial 31 ⏳ (NOT STARTED)

**Status**: Not started
**Changes needed**:
- Same as Tutorial 30
- Replace `adk-middleware` with `ag_ui_adk`
- Rewrite agent code to use `LlmAgent`
- Update all imports

### Tutorial 35 ⏳ (NOT STARTED)

**Status**: Not started
**Changes needed**:
- Same as Tutorial 30
- Replace `adk-middleware` with `ag_ui_adk`
- Rewrite agent code to use `LlmAgent`
- Update all imports
- Special attention to advanced patterns (HITL, Generative UI, Shared State)

## Correct Code Pattern

### Agent Creation

```python
from fastapi import FastAPI
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from google.adk.agents import LlmAgent

# Define tools as regular Python functions
def my_tool(param: str) -> str:
    """Tool description for the LLM."""
    return f"Result for {param}"

# Create ADK agent using LlmAgent
adk_agent = LlmAgent(
    name="agent_name",
    model="gemini-2.5-flash",  # or gemini-2.0-flash-exp
    instruction="System instructions here",
    tools=[my_tool]  # List of Python functions
)

# Wrap with AG-UI middleware
agent = ADKAgent(
    adk_agent=adk_agent,
    app_name="my_app",
    user_id="user_id",
    session_timeout_seconds=3600,
    use_in_memory_services=True
)

# Create FastAPI app
app = FastAPI()

# Add ADK endpoint
add_adk_fastapi_endpoint(app, agent, path="/api/copilotkit")

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Dependencies

**requirements.txt**:
```
google-genai>=1.15.0
fastapi>=0.115.0
uvicorn>=0.30.0
ag_ui_adk>=0.1.0
python-dotenv>=1.0.0
```

**pip install**:
```bash
pip install google-genai fastapi uvicorn ag_ui_adk python-dotenv
```

## Testing Strategy

After fixes:
1. Test Tutorial 29 quickstart (<10 min setup)
2. Test Tutorial 30 CLI method (`npx copilotkit@latest create -f adk`)
3. Test Tutorial 30 manual setup (verify all dependencies install)
4. Test Tutorial 31 setup
5. Test Tutorial 35 advanced features

## References

- CopilotKit ADK Documentation: https://docs.copilotkit.ai/adk
- CopilotKit GitHub Examples: https://github.com/CopilotKit/CopilotKit/tree/main/examples
- Google ADK Documentation: https://google.github.io/adk-docs/
- ag_ui_adk Package: https://pypi.org/project/ag_ui_adk/ (verify)

## Estimated Time

- Tutorial 30 fixes: 2-3 hours (major rewrite)
- Tutorial 31 fixes: 2-3 hours (major rewrite)
- Tutorial 35 fixes: 3-4 hours (advanced features, major rewrite)
- Testing: 4-6 hours
- **Total**: 11-16 hours

## Priority

**HIGH** - Users cannot use tutorials without these fixes. The package name error will cause immediate failure on `pip install`.

## Next Steps

1. Complete Tutorial 30 fixes
2. Complete Tutorial 31 fixes
3. Complete Tutorial 35 fixes
4. Test all corrected tutorials
5. Update TABLE_OF_CONTENTS.md
6. Create ERRATA.md documenting the issue for users who started with old versions
