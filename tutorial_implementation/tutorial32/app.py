"""
Data Analysis Assistant with Streamlit + ADK + Code Execution
Pure Python integration - interactive data analysis with dynamic visualization
"""

import asyncio
import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai.types import Content, Part, GenerateContentConfig
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

# Import agents
from data_analysis_agent import root_agent
from data_analysis_agent.visualization_agent import visualization_agent

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Data Analysis Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize Gemini client (for legacy chat support)
@st.cache_resource
def get_client():
    """Initialize and cache Gemini client."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("❌ Please set GOOGLE_API_KEY environment variable")
        st.info("1. Copy `.env.example` to `.env`")
        st.info("2. Add your Google API key from https://makersuite.google.com/app/apikey")
        st.info("3. Restart the app")
        st.stop()
    
    return genai.Client(
        api_key=api_key,
        http_options={'api_version': 'v1alpha'}
    )


# Initialize ADK runner
@st.cache_resource
def get_runner():
    """Initialize and cache ADK runner with multi-agent system."""
    session_service = InMemorySessionService()
    return Runner(
        agent=root_agent,
        app_name="data_analysis_assistant",
        session_service=session_service,
    ), session_service


# Initialize visualization runner (bypasses multi-agent routing for direct data passing)
@st.cache_resource
def get_visualization_runner():
    """Initialize and cache visualization runner for direct data passing."""
    session_service = InMemorySessionService()
    return Runner(
        agent=visualization_agent,
        app_name="visualization_assistant",
        session_service=session_service,
    ), session_service


runner, session_service = get_runner()
viz_runner, viz_session_service = get_visualization_runner()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "dataframe" not in st.session_state:
    st.session_state.dataframe = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None

if "adk_session_id" not in st.session_state:
    # Create ADK session properly - this initializes it in the session service
    adk_session = session_service.create_session_sync(
        app_name="data_analysis_assistant",
        user_id="streamlit_user"
    )
    st.session_state.adk_session_id = adk_session.id

if "viz_session_id" not in st.session_state:
    # Create visualization session
    viz_session = viz_session_service.create_session_sync(
        app_name="visualization_assistant",
        user_id="streamlit_user"
    )
    st.session_state.viz_session_id = viz_session.id

if "use_code_execution" not in st.session_state:
    st.session_state.use_code_execution = False  # Default to False for stability


# Header
st.title("📊 Data Analysis Assistant")
st.markdown("Upload a CSV file and ask me to analyze it or generate visualizations!")

# Sidebar for file upload and settings
with st.sidebar:
    st.header("📁 Upload Data")
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Upload a CSV file to analyze",
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.dataframe = df
            st.session_state.file_name = uploaded_file.name
            
            st.success(f"✅ Loaded: {uploaded_file.name}")
            
            # Display data info
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Rows", df.shape[0])
            with col2:
                st.metric("Columns", df.shape[1])
            
            # Show data preview
            with st.expander("📋 Data Preview"):
                st.dataframe(df.head(10), width='stretch')
            
            # Show data info
            with st.expander("ℹ️ Data Information"):
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Column Names & Types")
                    info_df = pd.DataFrame({
                        "Column": df.columns,
                        "Type": [str(dtype) for dtype in df.dtypes],
                        "Non-Null": df.count(),
                    })
                    st.dataframe(info_df, width='stretch')
                
                with col2:
                    st.subheader("Basic Statistics")
                    st.dataframe(df.describe(), width='stretch')
            
            st.subheader("⚙️ Features")
            st.session_state.use_code_execution = st.checkbox(
                "🔧 Use Code Execution for Visualizations (Beta)",
                value=False,
                help="Enable dynamic visualization generation using AI (BuiltInCodeExecutor) - Still in beta"
            )
            
            # Suggest analyses
            st.markdown("---")
            st.subheader("💡 Suggested Analyses")
            suggestions = [
                "📈 Analyze the main columns for insights",
                "🔗 Find correlations between variables",
                "🎯 Identify outliers and anomalies",
                "📊 Create visualizations of key metrics",
            ]
            for suggestion in suggestions:
                st.write(f"• {suggestion}")
            
            # Clear data button
            if st.button("🗑️ Clear Data"):
                st.session_state.dataframe = None
                st.session_state.file_name = None
                st.session_state.messages = []
                st.rerun()
        
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")

# Main chat interface
st.markdown("---")
st.subheader("💬 Chat with Your Data")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        # Display visualization if present
        if "visualization" in message:
            if message["visualization"]["type"] == "base64_image":
                st.image(f"data:image/png;base64,{message['visualization']['data']}")
            elif message["visualization"]["type"] == "html":
                st.html(message["visualization"]["data"])

# Chat input
if prompt := st.chat_input(
    "Ask me about your data or request a visualization..." if st.session_state.dataframe is not None 
    else "📁 Please upload a CSV file first",
    disabled=st.session_state.dataframe is None,
):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Prepare context about dataset
    context = ""
    df_csv = ""
    if st.session_state.dataframe is not None:
        df = st.session_state.dataframe
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(exclude=['number']).columns.tolist()
        
        # Convert DataFrame to CSV for code execution
        df_csv = df.to_csv(index=False)
        
        context = f"""
**Dataset Information:**
- File: {st.session_state.file_name}
- Shape: {df.shape[0]} rows × {df.shape[1]} columns
- Columns: {', '.join(df.columns.tolist())}
- Numeric columns: {', '.join(numeric_cols) if numeric_cols else 'None'}
- Categorical columns: {', '.join(categorical_cols) if categorical_cols else 'None'}

**Data available for visualization:**
The user's dataset is provided as CSV data below. Load it using:
```python
import pandas as pd
from io import StringIO
df = pd.read_csv(StringIO(csv_data))
```

CSV DATA (first 50 rows):
{df.head(50).to_csv(index=False)}

Users can request visualizations by asking for specific chart types."""
    else:
        context = "No dataset uploaded yet. Please ask the user to upload a CSV file first."
    
    # Choose routing: code execution or direct chat
    if st.session_state.use_code_execution:
        # Use ADK multi-agent system with code execution
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            has_visualization = False
            response_text = ""  # Initialize before try block to avoid scope issues
            
            try:
                # Prepare full context message for the agent
                context_message = f"""{context}

User Question: {prompt}"""
                
                # Create ADK message with full context
                message = Content(
                    role="user",
                    parts=[Part.from_text(text=context_message)]
                )
                
                # Use visualization runner directly to ensure CSV data reaches the agent
                async def collect_events():
                    """Collect and process all events from agent execution."""
                    response_parts = ""
                    has_visualization = False
                    visualization_data = []
                    
                    async for event in viz_runner.run_async(
                        user_id="streamlit_user",
                        session_id=st.session_state.viz_session_id,
                        new_message=message
                    ):
                        # Check for content in events
                        if event.content and event.content.parts:
                            for part in event.content.parts:
                                # Handle inline data (visualizations/images)
                                if hasattr(part, 'inline_data') and part.inline_data:
                                    has_visualization = True
                                    visualization_data.append(part.inline_data)
                                    response_parts += "\n📊 Visualization generated\n"
                                
                                # Handle executable code generation
                                if part.executable_code:
                                    # Code was generated by visualization agent
                                    pass
                                
                                # Handle code execution results
                                if part.code_execution_result:
                                    # Code executed successfully
                                    if part.code_execution_result.outcome == "SUCCESS":
                                        pass  # Result may be in inline_data
                                
                                # Handle text responses (don't skip if we already found inline_data)
                                if part.text and not part.text.isspace():
                                    response_parts += part.text
                        
                        # Update display with collected text
                        if response_parts:
                            message_placeholder.markdown(response_parts + "▌")
                    
                    return response_parts, has_visualization, visualization_data
                
                # Run async collection
                response_text, has_viz, viz_data = asyncio.run(collect_events())
                
                # Display final response
                if response_text:
                    message_placeholder.markdown(response_text)
                else:
                    message_placeholder.markdown("✓ Request processed")
                    response_text = "✓ Analysis and visualization complete"
                
                # Display any visualizations
                if has_viz and viz_data:
                    for viz in viz_data:
                        try:
                            # Handle inline_data from visualization agent
                            if hasattr(viz, 'data'):
                                import base64
                                from io import BytesIO
                                from PIL import Image
                                
                                # viz.data might be bytes or base64 string
                                if isinstance(viz.data, str):
                                    # Base64 encoded
                                    image_bytes = base64.b64decode(viz.data)
                                else:
                                    # Already bytes
                                    image_bytes = viz.data
                                
                                image = Image.open(BytesIO(image_bytes))
                                st.image(image, use_container_width=True)
                        except Exception as e:
                            st.warning(f"Could not display visualization: {str(e)}")
                
            except Exception as e:
                error_msg = f"❌ Error with code execution: {str(e)}"
                st.error(error_msg)
                message_placeholder.markdown(error_msg)
                response_text = error_msg
            
            # Add response to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text if response_text else "✓ Processed"
            })
    
    else:
        # Use direct Gemini API for faster response (legacy mode)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            try:
                client = get_client()
                
                system_instruction = f"""You are an expert data analyst assistant helping users understand their datasets.

{context}

Your responsibilities:
- Help users understand their data thoroughly
- Perform analysis based on the dataset context
- Provide clear, actionable insights
- Suggest interesting patterns and correlations
- Be concise but informative
- Use markdown formatting for better readability

Always base your responses on the actual data provided."""
                
                response = client.models.generate_content_stream(
                    model="gemini-2.0-flash",
                    contents=[
                        Content(role="user", parts=[Part.from_text(text=prompt)])
                    ],
                    config=GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7,
                        max_output_tokens=2048,
                    ),
                )
                
                # Stream response
                for chunk in response:
                    if chunk.text:
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌")
                
                # Final message
                message_placeholder.markdown(full_response)
            
            except Exception as e:
                error_msg = f"❌ Error generating response: {str(e)}"
                st.error(error_msg)
                full_response = error_msg
            
            # Add response to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response
            })

# Footer
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.caption("📚 Powered by Google Gemini 2.0 Flash")

with col2:
    st.caption("🐼 Data Analysis with Pandas")

with col3:
    st.caption("🔧 ADK Code Execution")

with col4:
    st.caption("💬 Interactive Chat")

# Display helpful tips in expander
with st.expander("💡 Tips & Tricks"):
    st.markdown("""
    **Getting Started:**
    1. Upload a CSV file using the sidebar
    2. Toggle "Use Code Execution for Visualizations" for dynamic charts
    3. Review the data preview and statistics
    4. Ask questions about your data
    
    **Example Questions with Code Execution (Visual):**
    - "Create a bar chart of sales by region"
    - "Show me a histogram of prices"
    - "Plot revenue vs quantity as a scatter plot"
    - "Generate a correlation heatmap"
    - "Visualize the distribution of customer ages"
    
    **Example Questions for Analysis:**
    - "What are the key insights from this data?"
    - "Show me the correlation between sales and profit"
    - "What are the top 5 values in the revenue column?"
    - "Are there any unusual patterns or outliers?"
    - "Summarize the main characteristics of this dataset"
    
    **Understanding the Modes:**
    - **Code Execution Mode** (recommended): Uses ADK's BuiltInCodeExecutor to generate visualizations dynamically
    - **Direct Mode**: Uses Gemini API directly for faster analysis responses
    
    **Code Execution Features:**
    - Dynamic visualization generation using Python (matplotlib, plotly)
    - Multi-agent system: analysis agent + visualization agent
    - Agent reasoning about what visualizations would be most insightful
    - Data is available as 'df' in the execution environment
    """)
