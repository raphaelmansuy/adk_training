# Streamlit Integration Research

**Research Date**: 2025-10-08  
**Sources**:

- ADK Python source code
- Google Cloud documentation
- Streamlit official docs

---

## Overview

Streamlit is a popular Python framework for building data apps and ML dashboards. Integrating ADK agents with Streamlit creates interactive AI-powered data applications.

### Key Finding: No Official AG-UI Support

❌ **No official Streamlit SDK** from AG-UI/CopilotKit (TypeScript-focused)  
✅ **Native ADK API integration** is straightforward (both Python)  
✅ **Streamlit's built-in session state** maps well to ADK sessions

---

## Integration Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Streamlit App (Pure Python)                             │
│  ┌───────────────────────────────────────────────────┐  │
│  │  streamlit library                                 │  │
│  │  - st.chat_message()                               │  │
│  │  - st.chat_input()                                 │  │
│  │  - st.session_state                                │  │
│  └───────────────┬───────────────────────────────────┘  │
└──────────────────┼─────────────────────────────────────┘
                   │ Direct Python API
                   ▼
┌─────────────────────────────────────────────────────────┐
│  Google ADK (In-Process)                                 │
│  ┌───────────────────────────────────────────────────┐  │
│  │  from google.adk.agents import Agent, Runner      │  │
│  │  - No FastAPI/HTTP overhead                        │  │
│  │  - Direct Python function calls                    │  │
│  └─────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

### Key Advantage: In-Process Integration

Unlike Next.js/React which require a separate backend server, Streamlit runs Python, allowing **direct import** of ADK agents without HTTP/WebSocket overhead.

---

## Implementation Patterns

### Pattern 1: Direct In-Process (Recommended)

**Project Structure**:

```
my-streamlit-adk-app/
├── app.py                    # Streamlit app
├── agents/
│   ├── __init__.py
│   └── assistant.py          # ADK agent definition
├── requirements.txt
└── .env                      # GOOGLE_API_KEY
```

**agents/assistant.py**:

```python
from google.adk.agents import LlmAgent
from google.adk.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get current weather for a location."""
    return f"Weather in {location}: Sunny, 72°F"

def create_agent():
    """Factory function to create agent."""
    return LlmAgent(
        name="assistant",
        model="gemini-2.0-flash",
        instruction="You are a helpful assistant.",
        tools=[get_weather]
    )
```

**app.py**:

```python
import streamlit as st
from google.adk.agents import Runner, Session
from agents.assistant import create_agent

# Page config
st.set_page_config(page_title="ADK Chat", page_icon="🤖")
st.title("🤖 ADK Assistant")

# Initialize session state
if "agent" not in st.session_state:
    st.session_state.agent = create_agent()
    st.session_state.runner = Runner()
    st.session_state.adk_session = Session()
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = st.session_state.runner.run(
                prompt,
                agent=st.session_state.agent,
                session=st.session_state.adk_session
            )
            response = result.content.parts[0].text
            st.markdown(response)
    
    # Add assistant message to chat
    st.session_state.messages.append({"role": "assistant", "content": response})
```

**requirements.txt**:

```txt
streamlit
google-adk
python-dotenv
```

**Run**:

```bash
export GOOGLE_API_KEY='your-key-here'
streamlit run app.py
```

---

### Pattern 2: Streaming Responses

Streamlit supports streaming text output with `st.write_stream()`:

**app.py** (streaming version):

```python
import streamlit as st
from google.adk.agents import Runner, Session, types
from agents.assistant import create_agent

st.set_page_config(page_title="ADK Chat (Streaming)", page_icon="🤖")
st.title("🤖 ADK Assistant (Streaming)")

# Initialize
if "agent" not in st.session_state:
    st.session_state.agent = create_agent()
    st.session_state.runner = Runner()
    st.session_state.adk_session = Session()
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Stream response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # Generate content with streaming
        for chunk in st.session_state.runner.run_stream(
            prompt,
            agent=st.session_state.agent,
            session=st.session_state.adk_session
        ):
            if chunk.content and chunk.content.parts:
                text = chunk.content.parts[0].text
                full_response += text
                response_placeholder.markdown(full_response + "▌")
        
        response_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
```

---

### Pattern 3: With Remote Backend (Optional)

If you need to separate the ADK backend (e.g., for Cloud Run deployment):

**Backend** (backend/main.py):

```python
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app

app = get_fast_api_app(
    agent_dir="./agents",
    web=True,
    allow_origins=["*"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Streamlit** (app.py):

```python
import streamlit as st
import httpx
import json

st.title("🤖 ADK Assistant (Remote)")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.session_id = "streamlit_session_123"

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Call remote ADK API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            with httpx.Client() as client:
                response = client.post(
                    "http://localhost:8000/run",
                    json={
                        "app_name": "assistant",
                        "user_id": "streamlit_user",
                        "session_id": st.session_state.session_id,
                        "new_message": {
                            "role": "user",
                            "parts": [{"text": prompt}]
                        },
                        "streaming": False
                    },
                    timeout=60.0
                )
                events = response.json()
                assistant_text = events[-1]["content"]["parts"][0]["text"]
                st.markdown(assistant_text)
    
    st.session_state.messages.append({"role": "assistant", "content": assistant_text})
```

---

## Advanced Features

### 1. Session Management with State

**app.py** (with persistent state):

```python
import streamlit as st
from google.adk.agents import Runner, Session

st.title("📊 Data Analysis Assistant")

# Initialize with custom state
if "adk_session" not in st.session_state:
    st.session_state.adk_session = Session()
    st.session_state.adk_session.state["analysis_history"] = []
    st.session_state.adk_session.state["current_dataset"] = None

# Sidebar for state display
with st.sidebar:
    st.subheader("Session State")
    st.json(st.session_state.adk_session.state)

# File uploader
uploaded_file = st.file_uploader("Upload CSV", type="csv")
if uploaded_file:
    import pandas as pd
    df = pd.read_csv(uploaded_file)
    st.session_state.adk_session.state["current_dataset"] = uploaded_file.name
    st.dataframe(df.head())

# Chat interface
if prompt := st.chat_input("Ask about your data..."):
    result = st.session_state.runner.run(
        prompt,
        agent=st.session_state.agent,
        session=st.session_state.adk_session
    )
    response = result.content.parts[0].text
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Update analysis history
    st.session_state.adk_session.state["analysis_history"].append({
        "query": prompt,
        "response": response
    })
```

### 2. Tool Output Rendering

**agents/data_tools.py**:

```python
from google.adk.tools import tool
import pandas as pd
import plotly.express as px

@tool
def create_chart(data: list[dict], chart_type: str, x_col: str, y_col: str) -> dict:
    """Create a data visualization."""
    df = pd.DataFrame(data)
    
    if chart_type == "bar":
        fig = px.bar(df, x=x_col, y=y_col)
    elif chart_type == "line":
        fig = px.line(df, x=x_col, y=y_col)
    else:
        fig = px.scatter(df, x=x_col, y=y_col)
    
    return {
        "chart_type": chart_type,
        "data": data,
        "config": {"x": x_col, "y": y_col}
    }
```

**app.py** (rendering tool output):

```python
import streamlit as st
import plotly.express as px
import pandas as pd

# After agent execution
for event in result.events:
    if event.type == "tool_execution":
        tool_name = event.tool_name
        tool_output = event.output
        
        if tool_name == "create_chart":
            # Render chart in Streamlit
            df = pd.DataFrame(tool_output["data"])
            if tool_output["chart_type"] == "bar":
                st.bar_chart(df.set_index(tool_output["config"]["x"]))
            elif tool_output["chart_type"] == "line":
                st.line_chart(df.set_index(tool_output["config"]["x"]))
```

### 3. Multi-Agent Dashboard

**app.py** (multi-agent):

```python
import streamlit as st
from google.adk.agents import LlmAgent, Runner, Session

st.title("🎯 Multi-Agent Dashboard")

# Initialize agents
if "agents" not in st.session_state:
    st.session_state.agents = {
        "researcher": LlmAgent(name="researcher", model="gemini-2.0-flash", 
                              instruction="You research topics in depth."),
        "writer": LlmAgent(name="writer", model="gemini-2.0-flash",
                          instruction="You write clear, concise summaries."),
        "critic": LlmAgent(name="critic", model="gemini-2.0-flash",
                          instruction="You critique and improve content.")
    }
    st.session_state.runner = Runner()
    st.session_state.session = Session()

# Agent selection
agent_choice = st.selectbox("Select Agent", list(st.session_state.agents.keys()))

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["Chat", "Session State", "History"])

with tab1:
    if prompt := st.chat_input(f"Ask {agent_choice}..."):
        result = st.session_state.runner.run(
            prompt,
            agent=st.session_state.agents[agent_choice],
            session=st.session_state.session
        )
        response = result.content.parts[0].text
        with st.chat_message("assistant"):
            st.markdown(response)

with tab2:
    st.json(st.session_state.session.state)

with tab3:
    st.write("Event history:")
    for event in st.session_state.session.events:
        st.write(f"- {event.type}: {event.content}")
```

---

## Real-World Example: Data Analysis App

**Complete Implementation**:

**app.py**:

```python
import streamlit as st
import pandas as pd
from google.adk.agents import LlmAgent, Runner, Session
from google.adk.tools import tool

# Page config
st.set_page_config(page_title="Data Analysis Assistant", layout="wide")
st.title("📊 Data Analysis Assistant")

# Define tools
@tool
def analyze_dataframe(df_json: str, analysis_type: str) -> dict:
    """Analyze a pandas dataframe.
    
    Args:
        df_json: JSON string representation of dataframe
        analysis_type: Type of analysis (summary, correlation, etc.)
    """
    import json
    df = pd.read_json(json.loads(df_json))
    
    if analysis_type == "summary":
        return {"result": df.describe().to_dict()}
    elif analysis_type == "correlation":
        return {"result": df.corr().to_dict()}
    else:
        return {"result": "Unknown analysis type"}

# Initialize
if "agent" not in st.session_state:
    st.session_state.agent = LlmAgent(
        name="data_analyst",
        model="gemini-2.0-flash",
        instruction="""You are a data analysis expert. 
        Help users understand their datasets through analysis and visualization.
        Use the analyze_dataframe tool when appropriate.""",
        tools=[analyze_dataframe]
    )
    st.session_state.runner = Runner()
    st.session_state.session = Session()
    st.session_state.messages = []
    st.session_state.df = None

# Layout: Sidebar + Main
with st.sidebar:
    st.subheader("📁 Data Upload")
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    
    if uploaded_file:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.success(f"Loaded: {uploaded_file.name}")
        st.dataframe(st.session_state.df.head())
        
        # Store in session state for agent access
        st.session_state.session.state["dataset_name"] = uploaded_file.name
        st.session_state.session.state["dataset_shape"] = st.session_state.df.shape
    
    st.subheader("📈 Quick Actions")
    if st.button("Get Summary"):
        if st.session_state.df is not None:
            st.write(st.session_state.df.describe())

# Main chat area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Chat with Data")
    
    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about your data..."):
        if st.session_state.df is None:
            st.warning("Please upload a dataset first!")
        else:
            # Add context about dataset
            enhanced_prompt = f"""
            Dataset: {st.session_state.session.state.get('dataset_name', 'unknown')}
            Shape: {st.session_state.session.state.get('dataset_shape', 'unknown')}
            
            User question: {prompt}
            """
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    result = st.session_state.runner.run(
                        enhanced_prompt,
                        agent=st.session_state.agent,
                        session=st.session_state.session
                    )
                    response = result.content.parts[0].text
                    st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})

with col2:
    st.subheader("🔍 Session Info")
    st.json({
        "session_id": st.session_state.session.id,
        "state": st.session_state.session.state,
        "message_count": len(st.session_state.messages)
    })
```

**Run**:

```bash
pip install streamlit google-adk pandas
export GOOGLE_API_KEY='your-key-here'
streamlit run app.py
```

---

## Deployment

### Option 1: Streamlit Cloud (Recommended)

**requirements.txt**:

```txt
streamlit>=1.30.0
google-adk>=1.0.0
pandas>=2.0.0
plotly>=5.0.0
```

**secrets.toml** (Streamlit Cloud Secrets):

```toml
GOOGLE_API_KEY = "your-api-key-here"
```

**Deploy**:

1. Push to GitHub
2. Connect to Streamlit Cloud
3. Add secrets via dashboard
4. Deploy!

### Option 2: Google Cloud Run

**Dockerfile**:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
```

**Deploy**:

```bash
gcloud run deploy streamlit-adk-app \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=your-key
```

---

## Comparison: Streamlit vs React/Next.js

| Aspect | Streamlit | React/Next.js (AG-UI) |
|--------|-----------|----------------------|
| **Language** | Pure Python | TypeScript + Python backend |
| **Setup Complexity** | Very Low | Medium |
| **UI Components** | Built-in (st.chat_message) | Custom (CopilotChat) |
| **Integration** | Direct in-process | HTTP/SSE |
| **Performance** | Good (single-threaded) | Better (async) |
| **Streaming** | Basic | Advanced (real-time) |
| **State Management** | st.session_state | React state + AG-UI |
| **Deployment** | Streamlit Cloud, Cloud Run | Vercel, Cloud Run |
| **Best For** | Data apps, internal tools | Production SaaS, customer-facing |

---

## Limitations & Considerations

### ⚠️ Streamlit Limitations

1. **Single-threaded**: Streamlit reruns entire script on interaction
2. **No WebSocket**: Limited real-time capabilities compared to Next.js
3. **Session state**: Stored in memory, not persistent by default
4. **Concurrency**: Limited concurrent users per instance
5. **UI Flexibility**: Less control than React

### ✅ Streamlit Advantages

1. **Pure Python**: No JavaScript/TypeScript needed
2. **Rapid development**: Minimal boilerplate
3. **Data visualization**: Excellent built-in support
4. **ML/Data workflows**: Natural fit for data scientists

---

## Best Practices

### 1. Cache Agent Initialization

```python
@st.cache_resource
def get_agent():
    """Cache agent to avoid re-initialization on every rerun."""
    return LlmAgent(
        name="assistant",
        model="gemini-2.0-flash",
        instruction="You are helpful."
    )

agent = get_agent()
```

### 2. Use Session State for Everything

```python
# Initialize all state upfront
if "adk_session" not in st.session_state:
    st.session_state.adk_session = Session()
    st.session_state.runner = Runner()
    st.session_state.messages = []
```

### 3. Handle Errors Gracefully

```python
try:
    result = runner.run(prompt, agent=agent, session=session)
    response = result.content.parts[0].text
except Exception as e:
    st.error(f"Error: {str(e)}")
    response = "Sorry, I encountered an error."
```

### 4. Clear Session on Reset

```python
if st.sidebar.button("Reset Conversation"):
    st.session_state.adk_session = Session()
    st.session_state.messages = []
    st.rerun()
```

---

## Key Findings

### ✅ High Confidence for Tutorial

1. **Simple Integration**: Direct Python imports, no HTTP overhead
2. **Built-in Chat UI**: `st.chat_message()` and `st.chat_input()`
3. **Session Management**: `st.session_state` + ADK `Session`
4. **Real Examples**: Working patterns documented
5. **Deployment Options**: Streamlit Cloud, Cloud Run

### ⚠️ Considerations

1. **No AG-UI SDK**: Custom client implementation required
2. **Limited Real-time**: No WebSocket support
3. **Performance**: Single-threaded execution model
4. **Scaling**: Limited concurrent users per instance

### 🎯 Recommendations

**Use Streamlit When**:

- Building internal data tools
- Rapid prototyping
- ML/data science workflows
- Python-only team

**Use Next.js/AG-UI When**:

- Customer-facing applications
- Need real-time features
- Large-scale deployments
- Production SaaS products

---

## Next Steps

1. ✅ **Completed**: Streamlit integration research
2. ⏳ **Next**: Research Slack Bolt integration
3. ⏳ **Next**: Research Google Cloud Pub/Sub patterns
4. ⏳ **Next**: Verify version compatibility

---

## Resources

- **Streamlit Docs**: https://docs.streamlit.io/
- **ADK Python API**: https://google.github.io/adk-docs/api-reference/python/
- **Streamlit Chat**: https://docs.streamlit.io/develop/api-reference/chat
- **Streamlit Cloud**: https://streamlit.io/cloud
