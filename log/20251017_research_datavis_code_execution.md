# Research: Data Visualization with ADK Code Execution

**Date**: October 17, 2025  
**Subject**: Feasibility of implementing data visualization using ADK Code Execution  
**Status**: Research Complete ✅

---

## Executive Summary

**YES, data visualization CAN be implemented using ADK Code Execution**, but with important considerations:

✅ **Officially Supported**: ADK has built-in code execution tools designed for this purpose  
✅ **Production Ready**: Vertex AI Code Interpreter extension provides secure execution  
✅ **Proven Pattern**: Official ADK Data Science sample demonstrates this capability  
⚠️ **Trade-offs**: Requires learning different architecture vs. current Tutorial 32 approach

---

## Official ADK Documentation Findings

### 1. Built-in Code Execution Tool

**Source**: https://google.github.io/adk-docs/tools/built-in-tools/#code-execution

**Key Facts**:
- **Tool Name**: `built_in_code_execution` (Python), `BuiltInCodeExecutor` (class)
- **Models Supported**: Gemini 2.0+ only
- **Execution Model**: Agent writes Python code → ADK executes → captures output
- **Return Format**: Code execution results with `outcome` and `output` fields
- **Code Availability**: Full code output, execution results, and stdout/stderr

**Example from Official Docs**:
```python
from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.agents import LlmAgent

code_agent = LlmAgent(
    name="calculator_agent",
    model="gemini-2.0-flash",
    code_executor=BuiltInCodeExecutor(),  # Enable code execution
    instruction="Write Python code to perform calculations"
)
```

### 2. Code Execution Output Handling

The agent receives execution results with:
- `part.executable_code.code` - The Python code generated
- `part.code_execution_result.outcome` - Success/failure status
- `part.code_execution_result.output` - stdout from execution

### 3. GKE Code Executor (Production)

**Source**: https://google.github.io/adk-docs/tools/built-in-tools/#gke-code-executor

For production environments with enhanced security:
- Sandboxed execution in gVisor-enabled Kubernetes Pods
- Resource limits and timeouts configurable
- Ephemeral environments (no state transfer between executions)
- Used by Google Cloud's production systems

---

## Real-World Implementation: ADK Data Science Agent

**Source**: https://github.com/google/adk-samples/tree/main/python/agents/data-science

### Official Sample Architecture

The ADK samples repository contains a **Data Science Multi-Agent System** that demonstrates data visualization with code execution:

#### Key Components

1. **Data Science Sub-Agent**
   - Purpose: Performs data analysis and visualization using Python
   - Method: Executes Python code via Vertex AI Code Interpreter
   - Capabilities: Generates plots, graphs, and statistical analysis

2. **Code Interpreter Integration**
   - Uses: Vertex AI Code Interpreter extension
   - Function: Executes LLM-generated Python code in sandbox
   - Output: Returns plots, statistics, and analysis results

3. **Agent Interaction Example**

   ```
   User: "Please generate a plot with total sales per country."
   
   Agent Response:
   1. Database Agent retrieves: SELECT SUM(sales) FROM table GROUP BY country
   2. Data Science Agent receives: [country, sales] data
   3. Generates Python code:
      import matplotlib.pyplot as plt
      plt.bar(countries, sales)
      plt.savefig('plot.png')
   4. Code Executor: Runs code, captures plot
   5. Returns: Plot visualization + explanation
   ```

### Confirmed Capabilities

From the official README:
- ✅ "The agent can generate text response as well as visuals, including plots and graphs for data analysis"
- ✅ "Supports the use of a Code Interpreter extension in Vertex AI for executing Python code"
- ✅ "Features a Data Science Agent that performs data analysis and visualization using Python"
- ✅ "enables complex data analysis and manipulation"

---

## Supported Visualization Libraries

Code execution supports any Python package available. Common options:

### 1. **Matplotlib** (Recommended for code execution)
- File-based: `plt.savefig('plot.png')`
- Works in sandboxed environments
- No display server needed
- Example: Bar charts, line plots, histograms

### 2. **Plotly** (Interactive)
- Generates HTML/JSON output
- Can be captured and displayed
- Example: Interactive scatter plots, dashboards

### 3. **Seaborn** (Statistical)
- Built on Matplotlib
- Better defaults for statistical plots
- Example: Heatmaps, distribution plots

### 4. **Pandas Plotting**
- Direct from DataFrame: `df.plot()`
- Matplotlib backend
- Simple and clean

---

## Implementation Approaches

### Approach 1: BuiltInCodeExecutor (Development/Local)

**When to use**: Local development, quick prototyping

```python
from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.agents import LlmAgent

visualization_agent = LlmAgent(
    name="data_visualizer",
    model="gemini-2.0-flash",
    code_executor=BuiltInCodeExecutor(),
    instruction="""You are a data visualization expert.
    When asked to create visualizations:
    1. Write Python code using matplotlib/plotly
    2. Use base64 encoding to embed plots in responses
    3. Provide clear explanations
    """
)
```

**Pros**:
- Easiest to set up
- Works locally
- Good for development

**Cons**:
- Limited security
- No resource isolation
- Not recommended for production

### Approach 2: Vertex AI Code Interpreter (Production)

**When to use**: Production deployments, enhanced security needed

```python
from google.adk.code_executors import VertexAICodeInterpreter
from google.adk.agents import LlmAgent

viz_agent = LlmAgent(
    name="viz_agent_prod",
    model="gemini-2.0-flash",
    code_executor=VertexAICodeInterpreter(),
    instruction="Create data visualizations..."
)
```

**Pros**:
- Sandbox execution environment
- Resource limits enforced
- Production-ready
- Google Cloud integration

**Cons**:
- Requires Vertex AI setup
- Higher latency
- Costs associated with execution

### Approach 3: GKE Code Executor (Enterprise)

**When to use**: Large-scale deployments, custom requirements

```python
from google.adk.code_executors import GkeCodeExecutor

gke_executor = GkeCodeExecutor(
    namespace="agent-sandbox",
    timeout_seconds=600,
    cpu_limit="1000m",
    mem_limit="1Gi"
)

agent = LlmAgent(
    name="enterprise_agent",
    model="gemini-2.0-flash",
    code_executor=gke_executor
)
```

**Pros**:
- Maximum security
- Enterprise-grade isolation
- Kubernetes native
- Scales easily

**Cons**:
- Requires GKE cluster
- Complex setup
- Highest operational overhead

---

## Comparison: Code Execution vs. Current Tutorial 32

### Current Tutorial 32 Approach (Direct Plotly)

```
User Request
    ↓
Streamlit App
    ↓
Direct Python (Plotly in-process)
    ↓
Display in UI
```

**Characteristics**:
- ✅ Fast (zero latency)
- ✅ Simple to implement
- ✅ Full control over visualization
- ❌ Agent doesn't "understand" visualizations
- ❌ Limited LLM guidance on what to plot

### Code Execution Approach

```
User Request
    ↓
Agent with Code Executor
    ↓
Agent Generates Python Code
    ↓
Code Executor Runs Code
    ↓
Returns Plot + Explanation
    ↓
Display in UI
```

**Characteristics**:
- ✅ Agent has reasoning about visualizations
- ✅ Dynamic code generation
- ✅ Flexible visualization types
- ✅ Agent can explain what it's showing
- ❌ Higher latency (code execution time)
- ❌ More complex error handling
- ❌ Requires sandboxed execution

---

## Architectural Patterns

### Pattern 1: Agent-Driven Visualization (Recommended for ADK)

```
┌─────────────────────────────────────────────┐
│         User Query                          │
│  "Show me sales by region as a chart"      │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│    LLM Agent with Code Executor             │
│  Reasons: "Need matplotlib for this"        │
│  Generates: Python plotting code            │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│    Code Executor (Sandboxed)                │
│  Executes: matplotlib.pyplot code           │
│  Returns: Image binary + stdout             │
└──────────────────┬──────────────────────────┘
                   ↓
┌─────────────────────────────────────────────┐
│    Parse & Display                          │
│  Show: Encoded image + explanation          │
└─────────────────────────────────────────────┘
```

### Pattern 2: Hybrid (Recommended for Streamlit)

```
┌──────────────────────────────────────────────┐
│         User Query                           │
│  "Analyze sales data"                       │
└───────────────┬────────────────────────────┬─┘
                ↓                            ↓
        ┌──────────────┐          ┌─────────────────┐
        │ Data Retrieval│         │ Visualization   │
        │ (DB Agent)    │         │ (Direct Python) │
        │ Returns: Data │         │ Returns: Plot   │
        └──────────────┘          └─────────────────┘
                │                            │
                └──────────────┬─────────────┘
                               ↓
                    Combine Results in UI
```

---

## Limitations & Important Notes

### From Official ADK Documentation

**Current Limitation**: 
> "Currently, for each root agent or single agent, only one built-in tool is supported. No other tools of any type can be used in the same agent."

This means:
- ❌ Can't use Code Execution + Custom Tools in same agent
- ❌ Can't use Code Execution + Google Search in same agent
- ✅ Workaround: Use sub-agents with AgentTool

### Solution: Multi-Agent Architecture

```python
# Sub-agent for code execution
visualization_agent = Agent(
    name="visualizer",
    code_executor=BuiltInCodeExecutor(),
)

# Sub-agent for data tools
analysis_agent = Agent(
    name="analyzer",
    tools=[custom_analysis_tool]
)

# Root agent coordinates both
root_agent = Agent(
    name="data_science_root",
    sub_agents=[
        AgentTool(agent=visualization_agent),
        AgentTool(agent=analysis_agent)
    ]
)
```

---

## Handling Visualization Output

### File-Based Output (Recommended)

```python
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Generate plot
plt.figure(figsize=(10, 6))
plt.plot(x, y)

# Save to bytes
buffer = BytesIO()
plt.savefig(buffer, format='png')
buffer.seek(0)

# Encode for display
b64_image = base64.b64encode(buffer.getvalue()).decode()
print(f"data:image/png;base64,{b64_image}")
```

### Interactive Output (For Plotly/JSON)

```python
import plotly.express as px
import json

fig = px.bar(data, x='region', y='sales')
json_output = fig.to_json()
print(json_output)  # Send to UI for rendering
```

### Capture in Agent Response

The agent can include visualizations in its response:
```
Explanation: Here are your sales by region
[BASE64_ENCODED_IMAGE or JSON_DATA]
Insight: Region X has highest sales
```

---

## Pros and Cons Summary

### Advantages of Code Execution for Data Viz

| Pro | Details |
|-----|---------|
| **Agent Reasoning** | Agent understands and explains visualizations |
| **Dynamic Generation** | Any visualization type possible |
| **Self-Documenting** | Code shows exactly what was done |
| **Flexibility** | Can modify code on-the-fly based on feedback |
| **Production Ready** | With Vertex AI/GKE executors, fully secure |
| **Scalability** | Scales with ADK deployment infrastructure |

### Disadvantages

| Con | Details |
|-----|---------|
| **Latency** | Code execution takes time (vs. direct plotting) |
| **Complexity** | More moving parts, error handling needed |
| **Learning Curve** | Agents generate code, need robust parsing |
| **Tool Limitation** | Can't combine with other tools in same agent |
| **Cost** | Vertex AI/GKE execution has associated costs |
| **Error Handling** | Code generation errors need graceful handling |

---

## Recommendation for Tutorial 32

### Option A: Keep Current Approach (Recommended for Streamlit Tutorial)

**Why**: 
- Tutorial 32 focuses on **Streamlit + ADK integration**
- Direct visualization is simpler and faster
- Better user experience (lower latency)
- Demonstrates Streamlit's strengths

**Current Implementation**: ✅ Solid
- Direct Plotly integration
- Tools provide data, Streamlit displays charts
- Clear separation of concerns

### Option B: Create New Tutorial for Code Execution

**Suggested**: "Tutorial 33: Advanced Data Visualization with ADK Code Execution"

**Content Would Include**:
- Code Execution capabilities
- Multi-agent architecture for visualization
- Vertex AI Code Interpreter setup
- Error handling patterns
- Performance considerations

---

## Implementation Recommendations

### For Tutorial 32 (Current)
Keep the direct Streamlit/Plotly approach - it's:
- Cleaner for Streamlit focus
- Better performance
- Simpler to understand

### For Advanced Users
Consider Code Execution when:
- ✅ Want agent to reason about visualizations
- ✅ Need dynamic chart type selection
- ✅ Building enterprise applications
- ✅ Deploying to Vertex AI Agent Engine

### Best Practice Pattern

Use **Hybrid Approach**:
```
1. Agent: Uses tools to retrieve/analyze data (provides insights)
2. Streamlit: Direct visualization (for performance)
3. Agent: Explains what the visualization means
```

This combines:
- Agent intelligence (reasoning about data)
- Streamlit performance (direct plotting)
- Best user experience (fast + smart)

---

## References

### Official Documentation
- **ADK Code Execution**: https://google.github.io/adk-docs/tools/built-in-tools/#code-execution
- **GKE Code Executor**: https://google.github.io/adk-docs/tools/built-in-tools/#gke-code-executor
- **Built-in Tools**: https://google.github.io/adk-docs/tools/built-in-tools/

### Sample Implementation
- **ADK Data Science Sample**: https://github.com/google/adk-samples/tree/main/python/agents/data-science
- **Video Walkthrough**: https://www.youtube.com/watch?v=efcUXoMX818

### Code Examples
- **Calculator Agent Example**: Official ADK docs (BuiltInCodeExecutor)
- **Data Science Agent**: Real-world multi-agent data visualization

---

## Conclusion

**✅ Data visualization CAN be implemented using ADK Code Execution**

**Key Takeaways**:

1. **Official Support**: ADK has mature code execution tools designed for this
2. **Proven Pattern**: Official samples demonstrate this in production
3. **Multiple Options**: BuiltInCodeExecutor, VertexAI, GKE options
4. **Trade-offs**: Flexibility vs. simplicity vs. latency
5. **Current Tutorial 32**: Already optimal for Streamlit use case
6. **Future Expansion**: Code execution ideal for advanced features/new tutorials

**Best Recommendation**: 
- Keep Tutorial 32 as-is (Streamlit focus, direct visualization)
- Consider Tutorial 33+ for ADK Code Execution patterns
- Use hybrid approach for production systems

---

**Research completed by**: AI Assistant  
**Date**: October 17, 2025  
**Status**: Ready for implementation discussion

