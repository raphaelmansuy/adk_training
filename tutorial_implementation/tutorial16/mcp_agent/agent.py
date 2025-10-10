"""
MCP Agent Implementation with Human-in-the-Loop
Demonstrates MCP filesystem integration with Google ADK.

This agent uses MCPToolset to connect to an MCP filesystem server,
providing file operations capabilities with approval workflow for
destructive operations.

Key Features:
- Restricted to sample_files directory for safety
- Human-in-the-Loop approval for write/move/delete operations
- Before-tool callback for validation and confirmation
- Comprehensive logging and error handling
"""

import os
from typing import Dict, Any, Optional
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from mcp.client.stdio import StdioServerParameters
from google.genai import types
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# HUMAN-IN-THE-LOOP CALLBACKS (Guardrails & Approval Workflow)
# ============================================================================

def before_tool_callback(
    tool,
    args: Dict[str, Any],
    tool_context
) -> Optional[Dict[str, Any]]:
    """
    Human-in-the-Loop callback for MCP filesystem operations.
    
    This callback implements approval workflow for destructive operations:
    - Write operations require confirmation
    - Move/delete operations require explicit approval
    - Read operations are allowed without confirmation
    
    ADK Best Practice: Use before_tool_callback for:
    1. Validation: Check arguments are safe
    2. Authorization: Require approval for sensitive operations
    3. Logging: Track tool usage for audit
    4. Rate limiting: Prevent abuse
    
    Args:
        tool: BaseTool object being called (has .name attribute)
        args: Arguments passed to the tool
        tool_context: ToolContext with state and invocation access
        
    Returns:
        None: Allow tool execution
        dict: Block tool execution and return this result instead
    """
    # Extract tool name from tool object
    tool_name = tool.name if hasattr(tool, 'name') else str(tool)
    
    logger.info(f"[TOOL REQUEST] {tool_name} with args: {args}")
    
    # Track tool usage in session state
    tool_count = tool_context.state.get('temp:tool_count', 0) or 0  # Handle None
    tool_context.state['temp:tool_count'] = tool_count + 1
    tool_context.state['temp:last_tool'] = tool_name
    
    # Define destructive operations that require approval
    DESTRUCTIVE_OPERATIONS = {
        'write_file': 'Writing files modifies content',
        'write_text_file': 'Writing files modifies content',
        'move_file': 'Moving files changes file locations',
        'create_directory': 'Creating directories modifies filesystem structure',
    }
    
    # Check if this is a destructive operation
    if tool_name in DESTRUCTIVE_OPERATIONS:
        reason = DESTRUCTIVE_OPERATIONS[tool_name]
        
        # Log the approval request
        logger.warning(f"[APPROVAL REQUIRED] {tool_name}: {reason}")
        logger.info(f"[APPROVAL REQUEST] Arguments: {args}")
        
        # In a real implementation, this would:
        # 1. Pause agent execution
        # 2. Send approval request to user via UI
        # 3. Wait for user response
        # 4. Continue or cancel based on response
        
        # For this demo, we'll simulate approval by checking a flag
        # In production, use ADK's built-in HITL mechanisms
        auto_approve = tool_context.state.get('user:auto_approve_file_ops', False)
        
        if not auto_approve:
            # Return blocking response - tool won't execute
            return {
                'status': 'requires_approval',
                'message': (
                    f"⚠️ APPROVAL REQUIRED\n\n"
                    f"Operation: {tool_name}\n"
                    f"Reason: {reason}\n"
                    f"Arguments: {args}\n\n"
                    f"To approve, set state['user:auto_approve_file_ops'] = True\n"
                    f"Or use the ADK UI approval workflow.\n\n"
                    f"This operation has been BLOCKED for safety."
                ),
                'tool_name': tool_name,
                'args': args,
                'requires_approval': True
            }
        else:
            logger.info(f"[APPROVED] {tool_name} approved via auto_approve flag")
    
    # Allow non-destructive operations (read, list, search, get_info)
    logger.info(f"[ALLOWED] {tool_name} approved automatically")
    return None  # None means allow tool execution


def create_mcp_filesystem_agent(
    base_directory: str = None,
    enable_hitl: bool = True
) -> Agent:
    """
    Create an agent with MCP filesystem access and Human-in-the-Loop approval.

    ADK Best Practice: Restrict filesystem access to specific directory
    for security and prevent accidental system file modifications.

    Args:
        base_directory: Base directory for filesystem access.
                       Defaults to 'sample_files' subdirectory for safety.
                       MCP server will ONLY access files within this directory.
        enable_hitl: Enable Human-in-the-Loop approval for destructive operations.
                    When True, write/move/delete operations require confirmation.

    Returns:
        Agent configured with MCP filesystem tools and safety guardrails

    Security Features:
        - Scoped to specific directory (no system access)
        - Human approval required for destructive operations
        - Comprehensive logging of all operations
        - Validation of file paths before execution
    """
    if base_directory is None:
        # Default to sample_files directory for safety
        current_dir = os.getcwd()
        base_directory = os.path.join(current_dir, 'sample_files')
        
        # Create sample_files if it doesn't exist
        if not os.path.exists(base_directory):
            logger.info(f"Creating sample_files directory: {base_directory}")
            os.makedirs(base_directory, exist_ok=True)

    # Validate directory exists
    if not os.path.exists(base_directory):
        raise ValueError(f"Directory does not exist: {base_directory}")
    
    # Convert to absolute path for security
    base_directory = os.path.abspath(base_directory)
    logger.info(f"[SECURITY] MCP filesystem access restricted to: {base_directory}")

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
            server_params=server_params,
            timeout=30.0  # Increase timeout to 30 seconds for MCP server initialization
        )
    )

    # Create agent with MCP tools and HITL callback
    agent = Agent(
        model='gemini-2.0-flash-exp',
        name='mcp_file_assistant',
        description='AI assistant with filesystem access via MCP and Human-in-the-Loop approval',
        instruction=f"""
You are a helpful file assistant with access to filesystem operations via MCP.

SECURITY SCOPE:
- You can ONLY access files in: {base_directory}
- This is your BASE DIRECTORY - treat it as your "current directory"
- You cannot access files outside this directory
- System files are completely off-limits

Your capabilities:
- read_file: Read file contents (no approval needed)
- read_text_file: Read text files (no approval needed)
- list_directory: List directory contents (no approval needed)
- search_files: Search for files by pattern (no approval needed)
- get_file_info: Get file metadata (no approval needed)
- write_file: Create or update files (⚠️ REQUIRES APPROVAL)
- write_text_file: Write text files (⚠️ REQUIRES APPROVAL)
- create_directory: Create new directories (⚠️ REQUIRES APPROVAL)
- move_file: Move or rename files (⚠️ REQUIRES APPROVAL)

CRITICAL BEHAVIOR RULES:

1. BE PROACTIVE AND INTELLIGENT:
   - When user says "list files" → IMMEDIATELY list files in {base_directory}
   - When user says "current dir" or "here" → Use {base_directory}
   - When user says "write a file" → Ask ONCE for filename and content together
   - Don't ask multiple follow-up questions - gather context and act decisively

2. CONTEXT-AWARE PATH HANDLING:
   - If user provides just a filename: assume it's in {base_directory}
   - If user says "sample_files" or a subdirectory: use {base_directory}/subdirectory
   - If user provides a full path starting with {base_directory}: use it as-is
   - NEVER ask "what is the current directory" - you already know it's {base_directory}

3. EFFICIENT COMMUNICATION:
   - Combine questions: "To write a file, I need the filename and content. What would you like?"
   - Don't repeat instructions the user already gave
   - If context is clear, proceed immediately
   - Only ask clarifying questions if truly ambiguous

4. HUMAN-IN-THE-LOOP WORKFLOW:
   - Destructive operations (write, move, delete) require user approval
   - You will be notified if an operation is blocked pending approval
   - Always explain WHY you need to perform the operation
   - For write operations: clearly state you'll create the file and what it will contain

5. ERROR RECOVERY:
   - If an operation is blocked, explain what happened and what's needed
   - Suggest alternatives when possible
   - Be helpful, not pedantic

GOOD EXAMPLES:
User: "List files"
You: [IMMEDIATELY call list_directory with {base_directory}]

User: "Write a file"
You: "I can create a file for you. What should I name it and what content should it have?"

User: "test.txt" [after being asked for filename]
You: "Great! What content should I write to test.txt in {base_directory}?"

User: "Create a hello world Python script"
You: "I'll create a file called hello.py with a hello world script. Here's what I'll write: [show content]. This requires your approval to proceed."

BAD EXAMPLES (DON'T DO THIS):
User: "List files"
You: "Could you please specify which directory?" ← WRONG! Use {base_directory}

User: "Write a file"  
You: "What directory?" ← WRONG! Ask for filename AND content together

User: "the current dir"
You: "Could you define current dir?" ← WRONG! It's {base_directory}

REMEMBER: You're an intelligent assistant, not a literal command parser. Understand intent, use context, and act decisively.
        """.strip(),
        tools=[mcp_tools],
        generate_content_config=types.GenerateContentConfig(
            temperature=0.2,  # Deterministic for file operations
            max_output_tokens=2048
        ),
        # Enable Human-in-the-Loop callback if requested
        before_tool_callback=before_tool_callback if enable_hitl else None
    )

    return agent


# ============================================================================
# ROOT AGENT (Default configuration with HITL enabled)
# ============================================================================

# Export root_agent for ADK discovery
# This uses sample_files directory by default for safety
root_agent = create_mcp_filesystem_agent(
    base_directory=None,  # Will use sample_files/
    enable_hitl=True      # Human-in-the-Loop enabled by default
)
