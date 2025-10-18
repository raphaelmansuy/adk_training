# Advanced Data Visualization with ADK Code Execution

**Difficulty**: Advanced | **Time**: 30 minutes | **Status**: Production Ready ✅

This sample demonstrates **Advanced Data Visualization** using Google ADK's Code Execution capabilities. Instead of using pre-built visualization functions, the agent generates and executes Python code dynamically to create visualizations.

---

## Quick Start

### 1. Setup

```bash
# Clone and navigate
cd tutorial32_advanced

# Install dependencies
make setup

# Configure API key
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### 2. Run

```bash
# Start the interactive agent
make dev
```

### 3. Try Commands

```
📊 You: Create a bar chart showing sales by region
📊 You: Generate a sine wave plot
📊 You: Make a scatter plot with random points
📊 You: Show a histogram of normal distribution
```

---

## Architecture

### How It Works

```
User Request
    ↓
LLM Agent with Code Executor
    ↓
Agent generates Python code for visualization
    ↓
Code Executor runs code in sandbox
    ↓
Matplotlib generates visualization
    ↓
Code execution result returned
    ↓
Agent explains what was generated
```

### Key Components

**1. Agent with Code Execution**
```python
from google.adk.agents import LlmAgent
from google.adk.code_executors import BuiltInCodeExecutor

agent = LlmAgent(
    name="data_viz_agent",
    code_executor=BuiltInCodeExecutor(),  # Enable code execution
)
```

**2. Agent Reasoning About Visualization**
- Agent understands what visualization to create
- Agent generates appropriate Python code
- Agent can optimize based on data type

**3. Code Execution Sandbox**
- Code runs safely in isolated environment
- No access to file system (by default in prod)
- Results captured and returned

---

## Code Execution Flow

### Step 1: Agent Analyzes Request

Agent receives: `"Create a bar chart showing sales by region"`

Agent reasons:
- Need matplotlib for visualization
- Use bar chart for categorical data
- Should include labels, title, legend

### Step 2: Agent Generates Code

Agent creates:
```python
import matplotlib.pyplot as plt
import numpy as np

regions = ['North', 'South', 'East', 'West']
sales = [150000, 120000, 180000, 140000]

plt.figure(figsize=(10, 6))
plt.bar(regions, sales, color='steelblue')
plt.title('Sales by Region')
plt.xlabel('Region')
plt.ylabel('Sales ($)')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('sales_chart.png', dpi=150)
print("Chart saved successfully")
```

### Step 3: Code Executes

- ADK runs code in `BuiltInCodeExecutor` sandbox
- Matplotlib generates chart
- Output captured in stdout

### Step 4: Agent Responds

Agent returns:
- Generated code (for transparency)
- Execution status (success/error)
- Stdout output
- Explanation of visualization

---

## Features

### ✅ What It Can Do

- **Dynamic Visualization**: Agent decides chart type based on request
- **Code Generation**: Automatic Python code creation
- **Error Handling**: Graceful handling of code execution errors
- **Explanations**: Agent explains what visualization shows
- **Flexibility**: Any matplotlib visualization possible

### ⚠️ Limitations

- Only `BuiltInCodeExecutor` in this sample (development mode)
- No file access (production security feature)
- Matplotlib only (no interactive Plotly in sandbox)
- Single agent (can't mix code execution with other tools)

---

## Real Examples

### Example 1: Sine Wave

```
📊 You: Generate a sine wave plot from 0 to 2π

Agent generates code:
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=2)
plt.title('Sine Wave')
plt.grid(True, alpha=0.3)
plt.savefig('sine.png')
```

### Example 2: Distribution Plot

```
📊 You: Show a histogram of normal distribution data

Agent generates code:
import matplotlib.pyplot as plt
import numpy as np

data = np.random.normal(100, 15, 1000)

plt.figure(figsize=(10, 6))
plt.hist(data, bins=30, color='green', alpha=0.7)
plt.title('Normal Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.3)
plt.savefig('distribution.png')
```

### Example 3: Multi-Plot

```
📊 You: Create a 2x2 subplot showing different visualizations

Agent can generate multiple subplots dynamically
```

---

## Production Considerations

### Upgrading to Vertex AI Code Interpreter

For production, use Vertex AI's Code Interpreter:

```python
from google.adk.code_executors import VertexAICodeInterpreter

agent = LlmAgent(
    name="production_viz_agent",
    code_executor=VertexAICodeInterpreter(),  # Production sandbox
)
```

**Advantages**:
- Enhanced security
- Resource limits enforced
- Integrates with Vertex AI
- Enterprise-grade isolation

**Setup Required**:
- Vertex AI API enabled
- Proper IAM permissions
- Cloud project configuration

### GKE Code Executor

For large-scale deployments:

```python
from google.adk.code_executors import GkeCodeExecutor

executor = GkeCodeExecutor(
    namespace="agent-sandbox",
    cpu_limit="500m",
    mem_limit="512Mi"
)

agent = LlmAgent(
    code_executor=executor
)
```

---

## Comparison with Tutorial 32

| Aspect | Tutorial 32 | This Sample |
|--------|------------|-------------|
| **Approach** | Direct Plotly | Code Execution |
| **Speed** | Instant | Slower (code exec) |
| **Complexity** | Simple | Advanced |
| **Agent Reasoning** | Limited | Full control |
| **Flexibility** | Fixed tools | Dynamic code |
| **Best For** | Learning UI | Production AI |
| **User Experience** | Fast UI updates | More intelligent |

---

## Testing

```bash
# Run all tests
make test

# Run specific test
pytest tests/test_agent.py -v

# Run with coverage
pytest tests/ --cov=data_viz_agent
```

Tests include:
- Agent configuration validation
- Code executor availability
- Project structure verification
- Import testing

---

## Troubleshooting

### Issue: API Key Error

```
❌ Error: GOOGLE_API_KEY not set in .env file
```

**Solution**:
```bash
cp .env.example .env
# Edit .env and add your key from https://aistudio.google.com/app/apikeys
```

### Issue: Module Not Found

```
❌ ModuleNotFoundError: No module named 'google.adk'
```

**Solution**:
```bash
make clean
make setup
```

### Issue: Code Execution Fails

- Agent generated invalid Python code
- Check stdout for error details
- Ask agent to fix and retry

---

## Key Concepts

### 1. Built-in Code Executor

Runs Python code in an isolated sandbox:
- Captures stdout/stderr
- Executes safely
- Returns results as events

### 2. Event Streaming

Agent responses stream through three event types:

```python
# 1. Code generation event
event.content.parts[0].executable_code.code

# 2. Execution result event
event.content.parts[0].code_execution_result.outcome
event.content.parts[0].code_execution_result.output

# 3. Final response event
event.content.parts[0].text
```

### 3. Agent Instruction Engineering

The agent instruction tells Gemini:
- What to do (create visualizations)
- How to do it (use matplotlib)
- What to consider (titles, labels, legends)
- Example code structure

---

## Next Steps

### Explore Further

1. **Modify Instructions**: Edit the agent prompt to change behavior
2. **Add Data Processing**: Generate data in code before visualizing
3. **Error Handling**: Add robust error handling for failed code execution
4. **Vertex AI**: Upgrade to production executor
5. **Integration**: Combine with Streamlit like Tutorial 32

### Create Similar Agents

Use this pattern for:
- Data analysis code generation
- Report generation
- Algorithm implementation
- Data processing pipelines

---

## References

- **ADK Code Execution Docs**: https://google.github.io/adk-docs/tools/built-in-tools/#code-execution
- **Official Data Science Sample**: https://github.com/google/adk-samples/tree/main/python/agents/data-science
- **Gemini Models**: https://ai.google.dev/models
- **Matplotlib Docs**: https://matplotlib.org/stable/contents.html

---

## Summary

This sample demonstrates:

✅ **Code Execution**: LLM-generated Python code execution  
✅ **Dynamic Visualization**: Agent decides visualization approach  
✅ **Advanced Architecture**: Agent with code executor pattern  
✅ **Production Patterns**: Enterprise deployment considerations  
✅ **Error Handling**: Graceful failure modes  

Perfect for understanding advanced ADK patterns and agent reasoning about code generation!
