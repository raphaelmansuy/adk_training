"""
Data Analysis Assistant with Streamlit + ADK
Pure Python integration - interactive data analysis application
"""

import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai.types import Content, Part, GenerateContentConfig

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Data Analysis Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize Gemini client
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


client = get_client()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "dataframe" not in st.session_state:
    st.session_state.dataframe = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None


# Header
st.title("📊 Data Analysis Assistant")
st.markdown("Upload a CSV file and ask me to analyze it! I'll help you explore your data.")

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

# Chat input
if prompt := st.chat_input(
    "Ask me about your data..." if st.session_state.dataframe is not None 
    else "📁 Please upload a CSV file first",
    disabled=st.session_state.dataframe is None,
):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Prepare context about dataset
    context = ""
    if st.session_state.dataframe is not None:
        df = st.session_state.dataframe
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(exclude=['number']).columns.tolist()
        
        context = f"""
**Dataset Information:**
- File: {st.session_state.file_name}
- Shape: {df.shape[0]} rows × {df.shape[1]} columns
- Columns: {', '.join(df.columns.tolist())}
- Numeric columns: {', '.join(numeric_cols) if numeric_cols else 'None'}
- Categorical columns: {', '.join(categorical_cols) if categorical_cols else 'None'}
- Data types: {df.dtypes.to_dict()}
- Missing values: {df.isnull().sum().to_dict()}

**First few rows:**
{df.head(5).to_string()}

**Summary statistics:**
{df.describe().to_string()}
"""
    else:
        context = "No dataset uploaded yet. Please ask the user to upload a CSV file first."
    
    # Build system instruction
    system_instruction = f"""You are an expert data analyst assistant helping users understand their datasets.

{context}

Your responsibilities:
- Help users understand their data thoroughly
- Perform analysis based on the dataset context
- Provide clear, actionable insights
- Suggest interesting patterns and correlations
- Be concise but informative
- Use markdown formatting for better readability
- Reference actual column names and statistics from the dataset

Analysis Guidelines:
- Reference specific columns and values from the data
- Provide statistical context when relevant
- Suggest next analysis steps
- Be friendly and encouraging
- For quantitative questions, provide numbers
- For patterns, explain what you observe

Always base your responses on the actual data provided. If a column name is mentioned
that doesn't exist, politely correct and suggest the actual available columns."""
    
    # Generate response with streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
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
        
        # Add assistant message to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.caption("📚 Powered by Google Gemini 2.0 Flash")

with col2:
    st.caption("🐼 Data Analysis with Pandas")

with col3:
    st.caption("💬 Interactive Chat Interface")

# Display helpful tips in expander
with st.expander("💡 Tips & Tricks"):
    st.markdown("""
    **Getting Started:**
    1. Upload a CSV file using the sidebar
    2. Review the data preview and statistics
    3. Ask questions about your data
    
    **Example Questions:**
    - "What are the key insights from this data?"
    - "Show me the correlation between sales and profit"
    - "What are the top 5 values in the revenue column?"
    - "Are there any unusual patterns or outliers?"
    - "Summarize the main characteristics of this dataset"
    
    **Data Requirements:**
    - CSV format files
    - Reasonable file size (< 200MB)
    - Headers in the first row
    - Consistent data types within columns
    """)
