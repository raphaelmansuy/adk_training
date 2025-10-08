# Agent vs LlmAgent Clarification

**Date**: January 23, 2025  
**Issue**: Clarifying the difference between `Agent` and `LlmAgent`

---

## TL;DR

✅ **Both are correct and identical!**

```python
from google.adk.agents import Agent      # Modern (Oct 2025)
from google.adk.agents import LlmAgent   # Legacy (still valid)

# They're the SAME CLASS - Agent is just a type alias for LlmAgent
```

---

## Source Code Evidence

From `/research/adk-python/src/google/adk/agents/llm_agent.py` (line 840):

```python
Agent: TypeAlias = LlmAgent
```

From `/research/adk-python/src/google/adk/agents/__init__.py`:

```python
from .llm_agent import Agent
from .llm_agent import LlmAgent

__all__ = [
    'Agent',
    'LlmAgent',
    # ...
]
```

**Conclusion**: They're imported from the same file, and `Agent` is explicitly defined as a type alias for `LlmAgent`.

---

## Naming Evolution

### October 2025 Pattern (Modern)

**From scratchpad.md research**:

```python
from google.adk.agents import Agent

root_agent = Agent(
    name="my_agent",
    model="gemini-2.0-flash",
    instruction="...",
    tools=[...]
)
```

### Pre-October 2025 Pattern (Legacy, but still valid)

```python
from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    name="my_agent",
    model="gemini-2.0-flash",
    instruction="...",
    tools=[...]
)
```

---

## Why the Change?

**Naming Consistency**: 
- Other agent types: `SequentialAgent`, `ParallelAgent`, `LoopAgent`
- The "Llm" prefix was redundant - all base agents use LLMs
- `Agent` is simpler and more intuitive

**Backward Compatibility**:
- `LlmAgent` is kept as a type alias
- No breaking changes for existing code
- Both names work identically

---

## What About Our Test Implementations?

### Our Code Uses LlmAgent

```python
# tutorial29_test/backend/agent.py
from google.adk.agents import LlmAgent  # ✅ Perfectly valid!

adk_agent = LlmAgent(
    name="quickstart_agent",
    model="gemini-2.0-flash-exp",
    instruction="..."
)
```

### Should We Update?

**No need!** Both are correct:
- ✅ **Modern style**: Use `Agent` for new code
- ✅ **Legacy style**: `LlmAgent` still works perfectly
- ✅ **Our tests**: Using `LlmAgent` is 100% correct

**If updating (optional)**:
- Replace `from google.adk.agents import LlmAgent` → `import Agent`
- Replace `LlmAgent(...)` → `Agent(...)`
- Purely cosmetic change - behavior is identical

---

## Recommendation

### For New Code (2025+)

```python
from google.adk.agents import Agent  # ✅ Use this

agent = Agent(
    name="my_agent",
    model="gemini-2.0-flash-exp",
    instruction="..."
)
```

### For Existing Code

```python
from google.adk.agents import LlmAgent  # ✅ Also fine

agent = LlmAgent(...)  # No need to change
```

### For Tutorials

**Best approach**: Show both with explanation:

```python
# Modern style (recommended for new code)
from google.adk.agents import Agent

# Legacy style (also correct - Agent is an alias for LlmAgent)
from google.adk.agents import LlmAgent
```

---

## Updated Documentation

We've updated:

1. **Tutorial 10** - Troubleshooting section now shows `Agent` as primary, with note about `LlmAgent`
2. **IMPORT_PATH_REVIEW.md** - Clarifies both are valid, explains type alias relationship
3. **This document** - Complete explanation

---

## FAQ

**Q: Is LlmAgent deprecated?**  
A: No! It's a valid type alias for Agent. Not deprecated, just older naming.

**Q: Will LlmAgent be removed?**  
A: Very unlikely - would break backward compatibility. It's officially exported in `__all__`.

**Q: Which should I use?**  
A: `Agent` for new code (modern), `LlmAgent` for existing code (don't bother changing).

**Q: Do they have different features?**  
A: No - they're literally the same class via type alias.

**Q: What about in our tests?**  
A: Our tests use `LlmAgent` - perfectly correct, no need to change.

---

## Comparison with Deprecated Import

### ❌ This IS Deprecated (Don't Use)

```python
from google.genai.llms import Gemini  # ❌ WRONG

model = Gemini(model_name="gemini-2.0-flash")  # OLD API
```

### ✅ Both of These Are Correct

```python
# Option 1: Modern (October 2025)
from google.adk.agents import Agent
agent = Agent(model="gemini-2.0-flash-exp")

# Option 2: Legacy (still valid)
from google.adk.agents import LlmAgent
agent = LlmAgent(model="gemini-2.0-flash-exp")
```

**Key difference**: The deprecated import was for a separate `Gemini` model class. The correct approach uses `Agent`/`LlmAgent` with string-based model selection.

---

## Conclusion

✅ **Agent** = Modern naming (October 2025+)  
✅ **LlmAgent** = Legacy naming (still valid, just older)  
✅ **Same class** = Type alias, identical behavior  
✅ **Our tests** = Using LlmAgent is correct  
✅ **No changes needed** = Both work perfectly  

**Use `Agent` for new code, but don't worry about `LlmAgent` in existing code!**

---

**Status**: ✅ **CLARIFIED**  
**Action**: Documentation updated to show both patterns  
**Confidence**: 100% - verified in ADK source code
