"""
Data Visualization Agent with Code Execution

This agent demonstrates ADK's code execution capabilities for dynamic data
visualization. Instead of using pre-built plotting tools, the agent generates
and executes Python code to create visualizations.
"""

from google.adk.agents import LlmAgent
from google.adk.code_executors import BuiltInCodeExecutor


# Create agent with code execution capability
root_agent = LlmAgent(
    name="data_viz_agent",
    model="gemini-2.0-flash",
    description="Data visualization agent using code execution",
    code_executor=BuiltInCodeExecutor(),
    instruction="""You are an expert data visualization agent.

When a user asks you to visualize data or create charts:

1. Analyze the request to understand what visualization is needed
2. Write Python code to create the visualization using matplotlib
3. The code will be automatically executed in a sandbox environment
4. Your output will include both the code and any generated visualizations

Important guidelines:
- Use matplotlib for all visualizations (it works in sandbox environments)
- Always use plt.savefig() to save plots to files
- Provide clear titles, labels, and legends
- Use base64 encoding to embed images in responses if needed
- Explain what the visualization shows

Example code structure:
```python
import matplotlib.pyplot as plt
import numpy as np

# Generate data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create plot
plt.figure(figsize=(10, 6))
plt.plot(x, y)
plt.title('Sample Visualization')
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.grid(True)

# Save to file
plt.savefig('plot.png', dpi=150, bbox_inches='tight')
print("Plot saved successfully")
```

You can also analyze the code execution results and provide insights
about the data visualization."""
)


__all__ = ["root_agent"]
