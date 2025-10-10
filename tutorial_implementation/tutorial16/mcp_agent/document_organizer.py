"""
Document Organizer using MCP Filesystem Server
Automatically organizes documents by type, date, and content.

This demonstrates creating a specialized agent with MCP filesystem tools.
"""

import os
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from mcp.client.stdio import StdioServerParameters
from google.genai import types


def create_document_organizer_agent(base_directory: str) -> Agent:
    """
    Create an agent specialized for document organization.

    Args:
        base_directory: Root directory to organize

    Returns:
        Agent configured for document organization with MCP filesystem tools
    """
    # Validate directory
    if not os.path.exists(base_directory):
        raise ValueError(f"Directory does not exist: {base_directory}")

    # Create MCP toolset for filesystem access
    server_params = StdioServerParameters(
        command='npx',
        args=[
            '-y',
            '@modelcontextprotocol/server-filesystem',
            base_directory
        ]
    )

    mcp_tools = McpToolset(
        connection_params=StdioConnectionParams(
            server_params=server_params
        )
    )

    # Create organizer agent
    agent = Agent(
        model='gemini-2.0-flash-exp',
        name='document_organizer',
        description='Intelligent document organization agent with filesystem access',
        instruction="""
You are a document organization expert with filesystem access via MCP.

Your responsibilities:
1. Analyze files by name, type, and content
2. Create logical folder structures
3. Move files to appropriate locations
4. Rename files for clarity
5. Generate organization reports

Guidelines:
- Create folders by category (e.g., Documents, Images, Code, Archives)
- Use subcategories when helpful (e.g., Documents/2024/, Documents/Work/)
- Preserve original filenames unless unclear
- Never delete files
- Report all changes made
- Always explain what you're doing

You have access to filesystem tools:
- read_file: Read file contents
- write_file: Create files
- list_directory: List directory contents
- create_directory: Create folders
- move_file: Move/rename files
- search_files: Search by pattern
- get_file_info: Get file metadata

Provide clear, structured reports of all changes made.
        """.strip(),
        tools=[mcp_tools],
        generate_content_config=types.GenerateContentConfig(
            temperature=0.2,  # Deterministic for file operations
            max_output_tokens=2048
        )
    )

    return agent
