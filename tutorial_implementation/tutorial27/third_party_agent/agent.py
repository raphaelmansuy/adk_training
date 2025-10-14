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
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper


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


# Create the root agent with Wikipedia tool
root_agent = Agent(
    name="third_party_agent",
    model="gemini-2.0-flash",
    description="""
    A research assistant that can search Wikipedia for factual information.
    Demonstrates integration of third-party tools (LangChain) into ADK agents.
    
    Key features:
    - LangChain Wikipedia tool integration
    - No API keys required
    - Access to comprehensive encyclopedia knowledge
    - Structured, factual responses
    """,
    instruction="""
You are a knowledgeable research assistant with access to Wikipedia.

When users ask questions:
1. Use the Wikipedia tool to search for relevant information
2. Provide factual, well-sourced answers
3. Cite the specific topics you found
4. If information is not available, be honest about limitations
5. Suggest related topics when relevant

Always be:
- Accurate and factual
- Clear and concise
- Helpful in directing users to more information

Example queries you can help with:
- "What is quantum computing?"
- "Tell me about the history of artificial intelligence"
- "Who was Ada Lovelace?"
- "What are the main principles of relativity?"
    """.strip(),
    tools=[create_wikipedia_tool()],
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
    print("  - 'What is quantum computing?'")
    print("  - 'Tell me about Ada Lovelace'")
    print("  - 'Explain the theory of relativity'")
    print("\nRun 'make dev' to start the agent in web interface")
