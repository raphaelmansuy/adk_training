"""
Third-Party Tools Integration Agent - Tutorial 27

This agent demonstrates how to integrate third-party framework tools into ADK.
It uses LangChain's Wikipedia tool as the main example (no API key required).

Key Concepts:
- LangchainTool wrapper for integrating LangChain tools
- Proper import paths (google.adk.tools.langchain_tool)
- Tool wrapping and agent configuration
- Error handling for third-party tools
"""

from google.adk.agents import Agent
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from crewai_tools import DirectoryReadTool, FileReadTool


def create_wikipedia_tool():
    """
    Create a Wikipedia search tool using LangChain.
    
    This tool allows the agent to search Wikipedia for factual information.
    No API key required - uses public Wikipedia API.
    
    Returns:
        LangchainTool: Wrapped Wikipedia tool ready for ADK agent
    """
    # Create Wikipedia tool with LangChain
    wikipedia = WikipediaQueryRun(
        api_wrapper=WikipediaAPIWrapper(
            top_k_results=3,
            doc_content_chars_max=4000
        )
    )
    
    # Wrap for ADK using LangchainTool
    wiki_tool = LangchainTool(tool=wikipedia)
    
    return wiki_tool


def create_web_search_tool():
    """
    Create a web search tool using DuckDuckGo via LangChain.
    
    This tool allows the agent to search the web for current information.
    No API key required - uses DuckDuckGo's public search.
    
    Returns:
        LangchainTool: Wrapped web search tool ready for ADK agent
    """
    # Create web search tool with LangChain
    web_search = DuckDuckGoSearchRun()
    
    # Wrap for ADK using LangchainTool
    search_tool = LangchainTool(tool=web_search)
    
    return search_tool


def create_directory_read_tool():
    """
    Create a directory reading tool using CrewAI.
    
    This tool allows the agent to explore directory structures.
    Useful for understanding project layouts and file organization.
    
    Returns:
        function: ADK-compatible tool function
    """
    tool = DirectoryReadTool()
    
    def directory_read(directory_path: str) -> dict:
        """
        Read the contents of a directory.
        
        Args:
            directory_path: Path to the directory to read
            
        Returns:
            Dict with status, report, and directory contents
        """
        try:
            result = tool.run(directory_path=directory_path)
            return {
                'status': 'success',
                'report': f'Successfully read directory: {directory_path}',
                'data': result
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'report': f'Failed to read directory: {directory_path}'
            }
    
    return directory_read


def create_file_read_tool():
    """
    Create a file reading tool using CrewAI.
    
    This tool allows the agent to read file contents.
    Useful for analyzing code, documents, and configuration files.
    
    Returns:
        function: ADK-compatible tool function
    """
    tool = FileReadTool()
    
    def file_read(file_path: str) -> dict:
        """
        Read the contents of a file.
        
        Args:
            file_path: Path to the file to read
            
        Returns:
            Dict with status, report, and file contents
        """
        try:
            result = tool.run(file_path=file_path)
            return {
                'status': 'success',
                'report': f'Successfully read file: {file_path}',
                'data': result
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'report': f'Failed to read file: {file_path}'
            }
    
    return file_read


# Create the root agent with multiple third-party tools
root_agent = Agent(
    name="third_party_agent",
    model="gemini-2.0-flash",
    description="""
    A comprehensive research and file analysis assistant with access to Wikipedia, web search, and file system tools.
    Demonstrates integration of multiple third-party tools (LangChain and CrewAI) into ADK agents.
    
    Key features:
    - LangChain Wikipedia tool for encyclopedia knowledge
    - LangChain DuckDuckGo web search for current information
    - CrewAI DirectoryReadTool for exploring file structures
    - CrewAI FileReadTool for analyzing file contents
    - No API keys required for any tool
    - Access to both historical facts, recent developments, and local files
    - Structured, factual responses from multiple sources
    """,
    instruction="""
You are a knowledgeable research and file analysis assistant with access to multiple tools.

When users ask questions:
1. Use Wikipedia for historical facts, biographies, and established knowledge
2. Use web search for current events, recent developments, and breaking news
3. Use directory reading to explore project structures and file organization
4. Use file reading to analyze specific files, code, or documents
5. Cross-reference information when possible for comprehensive answers
6. Provide factual, well-sourced answers with source attribution
7. If information conflicts, note the discrepancy and suggest verification
8. Be honest about limitations of each tool

Always be:
- Accurate and factual
- Clear and concise
- Helpful in directing users to more information

Example queries you can help with:
- "What is quantum computing?" (Wikipedia)
- "Latest AI developments this year" (Web search)
- "Tell me about Ada Lovelace" (Wikipedia)
- "Current news about space exploration" (Web search)
- "Show me the project structure" (Directory read)
- "Read the README file" (File read)
    """.strip(),
    tools=[
        create_wikipedia_tool(),
        create_web_search_tool(),
        create_directory_read_tool(),
        create_file_read_tool()
    ],
    output_key="research_response"
)


if __name__ == "__main__":
    # Demonstrate that the agent can be imported and created successfully
    print("Third-Party Tools Integration Agent")
    print("=" * 50)
    print(f"Agent Name: {root_agent.name}")
    print(f"Model: {root_agent.model}")
    print(f"Tools: {len(root_agent.tools)} tool(s) registered")
    print("\nAgent created successfully!")
    print("\nTry queries like:")
    print("  - 'What is quantum computing?' (Wikipedia)")
    print("  - 'Latest AI developments this year' (Web search)")
    print("  - 'Tell me about Ada Lovelace' (Wikipedia)")
    print("  - 'Current news about space exploration' (Web search)")
    print("  - 'Show me the project structure' (Directory read)")
    print("  - 'Read the README file' (File read)")
    print("\nRun 'make dev' to start the agent in web interface")
