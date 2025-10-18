# Implementation Guide: ADK Code Execution for Data Visualization

## Overview

This sample implements data visualization using **ADK Code Execution**, where the agent generates and executes Python code dynamically instead of using pre-built functions.

---

## Architecture

### Component 1: Agent with Code Executor

**File**: `data_viz_agent/agent.py`

```python
from google.adk.agents import LlmAgent
from google.adk.code_executors import BuiltInCodeExecutor

root_agent = LlmAgent(
    name="data_viz_agent",
    model="gemini-2.0-flash",
    code_executor=BuiltInCodeExecutor(),
    instruction="You are a visualization expert..."
)
```

**Key Features**:
- Uses `LlmAgent` with code execution enabled
- Gemini 2.0 Flash model for reasoning
- Comprehensive instruction for visualization tasks
- BuiltInCodeExecutor for development/demo

### Component 2: CLI Runner

**File**: `main.py`

Implements:
- Async event handling for streaming responses
- Code execution event detection
- User-friendly output formatting
- Interactive loop for continuous interaction

**Flow**:
```python
async for event in runner.run_async(...):
    if event.content.parts[0].executable_code:
        # Handle code generation
    elif event.content.parts[0].code_execution_result:
        # Handle execution result
    elif event.content.parts[0].text:
        # Handle text response
```

---

## How It Works

### Step 1: User Request

```
User: "Create a bar chart showing sales by region"
```

### Step 2: Agent Reasoning

Agent analyzes:
- Request intent (create visualization)
- Data structure (categorical - regions & values)
- Appropriate chart type (bar chart)
- Required elements (title, labels, legend)

### Step 3: Code Generation

Agent generates Python code:
```python
import matplotlib.pyplot as plt

regions = ['North', 'South', 'East', 'West']
sales = [150000, 120000, 180000, 140000]

plt.figure(figsize=(10, 6))
plt.bar(regions, sales)
plt.title('Sales by Region')
plt.xlabel('Region')
plt.ylabel('Sales ($)')
plt.savefig('chart.png')
```

### Step 4: Code Execution

- ADK's BuiltInCodeExecutor runs the code
- Matplotlib generates the visualization
- Stdout captured (e.g., "Plot saved successfully")

### Step 5: Response

Agent returns:
- Generated code (for transparency)
- Execution outcome (success/failure)
- Stdout output
- Explanation of visualization

---

## Key Implementation Details

### 1. Agent Configuration

**Name**: Identifies agent in logs  
**Model**: "gemini-2.0-flash" for reasoning capability  
**Code Executor**: BuiltInCodeExecutor() enables code execution  
**Instruction**: Tells agent how to handle visualization requests

### 2. Instruction Engineering

The instruction includes:
- **Role**: "You are an expert data visualization agent"
- **Task**: "When asked to visualize data or create charts..."
- **Guidelines**: Specific requirements (use matplotlib, save files)
- **Example**: Code template showing expected patterns

### 3. Event Streaming

Three types of events to handle:

```python
# 1. Code Generation
event.content.parts[0].executable_code.code

# 2. Execution Result
part.code_execution_result.outcome      # "SUCCESS" or "ERROR"
part.code_execution_result.output       # stdout from code

# 3. Final Response
event.content.parts[0].text
```

### 4. Async Execution

```python
async for event in runner.run_async(
    user_id="user123",
    session_id=session.id,
    new_message=message
):
    # Process streaming events
```

---

## Comparing with Tutorial 32

### Tutorial 32: Direct Integration

```
User Request
  ↓
Tool (analyze_column, filter_data, etc.)
  ↓
Streamlit displays Plotly chart directly
  ↓
Fast, simple, predictable
```

**Characteristics**:
- Pre-built tools for visualization
- Streamlit directly renders charts
- No code generation
- Optimal user experience (fast rendering)

### This Sample: Code Execution

```
User Request
  ↓
Agent generates Python code
  ↓
Code executor runs matplotlib
  ↓
Result returned to agent
  ↓
Agent explains visualization
  ↓
More intelligent, flexible, but slower
```

**Characteristics**:
- Dynamic code generation
- Agent reasoning about visualizations
- Flexible (any matplotlib chart possible)
- Slower (code execution overhead)

---

## Production Upgrade Path

### Current: BuiltInCodeExecutor

**Suitable for**: Development, demos, local testing

```python
code_executor=BuiltInCodeExecutor()
```

**Limitations**:
- No security isolation (development only)
- No resource limits
- Single-machine deployment

### Production: Vertex AI Code Interpreter

**Suitable for**: Production deployments

```python
from google.adk.code_executors import VertexAICodeInterpreter

code_executor = VertexAICodeInterpreter()
```

**Advantages**:
- Google-managed sandbox
- Resource limits enforced
- Enterprise security
- Scales with Vertex AI

**Setup**:
```bash
# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com

# Update requirements
google-adk[vertex-ai]>=1.16.0
```

### Enterprise: GKE Code Executor

**Suitable for**: Large-scale deployments

```python
from google.adk.code_executors import GkeCodeExecutor

executor = GkeCodeExecutor(
    namespace="agent-sandbox",
    cpu_limit="500m",
    mem_limit="512Mi",
    timeout_seconds=300
)
```

**Benefits**:
- Kubernetes-native deployment
- Custom resource limits
- gVisor sandbox isolation
- Enterprise-grade control

---

## Error Handling Patterns

### Code Generation Errors

**Issue**: Agent generates invalid Python code

**Handling**:
```python
if event.content.parts[0].code_execution_result.outcome == "ERROR":
    error_output = part.code_execution_result.output
    print(f"Code execution failed: {error_output}")
```

### Missing Dependencies

**Issue**: Code references unavailable library

**Solution**: 
- Ensure matplotlib in requirements.txt
- NumPy included for numerical operations
- Restrict to standard libraries

### Request Ambiguity

**Issue**: User request doesn't specify chart type

**Solution**:
- Agent instruction includes decision logic
- Agent can ask for clarification
- Example code in instruction guides agent

---

## Testing Strategy

### Unit Tests

```python
# tests/test_agent.py
def test_agent_has_code_executor():
    from google.adk.code_executors import BuiltInCodeExecutor
    assert isinstance(root_agent.code_executor, BuiltInCodeExecutor)
```

### Integration Tests (Manual)

```bash
make dev
# Interactively test visualization requests
```

### Example Scripts

```bash
python examples.py
# Runs predefined visualization examples
```

---

## Performance Considerations

### Latency

**BuiltInCodeExecutor**: ~2-5 seconds per request
- Code generation: ~1s
- Code execution: ~1-2s
- Response streaming: ~0.5s

**Vertex AI Code Interpreter**: ~5-10 seconds per request
- Network latency
- Queue time on Vertex AI
- Security scanning

### Optimization Tips

1. **Batch Requests**: Multiple charts in one request
2. **Caching**: Pre-generated templates for common charts
3. **Prompt Optimization**: Clear instructions reduce iterations
4. **Code Quality**: Well-structured code executes faster

---

## Extending the Sample

### Add New Capabilities

1. **Data Processing**:
   - Agent generates data transformation code
   - Pandas operations before visualization

2. **Statistical Analysis**:
   - Agent calculates statistics
   - Includes in visualization explanations

3. **Multiple Plots**:
   - Agent creates subplots
   - Compares multiple datasets

4. **Interactivity**:
   - Generate Plotly code (in string form)
   - Combine with Streamlit for interactive UI

### Integrate with Streamlit

```python
# Hybrid approach: Use both patterns

# Agent reasons about visualizations
agent_recommendation = await get_agent_insight(data)

# Streamlit directly renders performance charts
st.plotly_chart(create_interactive_chart(data))
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'google.adk'"

**Solution**:
```bash
make clean
make setup
```

### Issue: Code execution times out

**Solution**:
- Simplify code generation
- Use smaller datasets in examples
- Adjust timeout in production executor

### Issue: Agent generates incomplete code

**Solution**:
- Enhance instruction with more examples
- Add error handling guidance
- Test with different models

---

## Best Practices

### 1. Instruction Engineering

✅ **Good**:
```
Use matplotlib for all visualizations
Always include titles and labels
Use plt.savefig() to save plots
Provide clear legends
```

❌ **Avoid**:
```
Make nice charts
Create visualizations
Generate plots
```

### 2. Error Handling

✅ **Good**:
```python
if outcome == "ERROR":
    print(f"Code execution failed: {output}")
    # Retry or user notification
```

❌ **Avoid**:
```python
# Silently ignore errors
if outcome != "SUCCESS":
    pass
```

### 3. Code Quality

✅ **Good**:
- Clear variable names
- Comments explaining logic
- Proper imports
- Clean output formatting

❌ **Avoid**:
- Cryptic variable names
- Missing error handling
- No comments
- Messy output

---

## Summary

This implementation demonstrates:

✅ **Code Execution**: LLM generates and executes Python  
✅ **Agent Reasoning**: Agent decides visualization approach  
✅ **Dynamic Code**: Flexible, adaptable visualizations  
✅ **Production Patterns**: Upgrade paths for scaling  
✅ **Best Practices**: Error handling, testing, performance  

Perfect for understanding advanced ADK patterns and intelligent code generation!

---

## References

- **Official ADK Code Execution**: https://google.github.io/adk-docs/tools/built-in-tools/#code-execution
- **ADK Data Science Sample**: https://github.com/google/adk-samples/tree/main/python/agents/data-science
- **Gemini Documentation**: https://ai.google.dev/
- **Matplotlib Guide**: https://matplotlib.org/stable/contents.html
