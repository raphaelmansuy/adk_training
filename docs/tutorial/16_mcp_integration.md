---
id: mcp_integration
title: "Tutorial 16: Model Context Protocol (MCP) Integration - Standardized Tool Protocols"
description: "Integrate MCP servers for standardized tool access including filesystem, databases, and external services using the Model Context Protocol."
sidebar_label: "16. MCP Integration"
sidebar_position: 16
tags: ["advanced", "mcp", "protocol", "tools", "standardization"]
keywords:
  [
    "model context protocol",
    "mcp servers",
    "standardized tools",
    "filesystem",
    "databases",
    "tool protocols",
  ]
status: "draft"
difficulty: "advanced"
estimated_time: "2 hours"
prerequisites:
  [
    "Tutorial 01: Hello World Agent",
    "Tutorial 02: Function Tools",
    "MCP server setup",
  ]
learning_objectives:
  - "Use MCPToolset for standardized tool access"
  - "Configure and connect to MCP servers"
  - "Build agents with filesystem and database access"
  - "Understand MCP protocol specifications"
implementation_link: "https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial16"
---

:::danger UNDER CONSTRUCTION

**This tutorial is currently under construction and may contain errors, incomplete information, or outdated code examples.**

Please check back later for the completed version. If you encounter issues, refer to the working implementation in the [tutorial repository](https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial16).

:::
---

# Tutorial 16: Model Context Protocol (MCP) Integration

**Goal**: Integrate external tools and services into your agents using the Model Context Protocol (MCP), expanding your agent's capabilities with community-built tool servers.

**Prerequisites**:

- Tutorial 01 (Hello World Agent)
- Tutorial 02 (Function Tools)
- Node.js installed (for MCP servers)
- Basic understanding of protocols and APIs

**What You'll Learn**:

- Understanding Model Context Protocol (MCP)
- Using `MCPToolset` to connect to MCP servers
- Configuring stdio-based MCP connections
- Building agents with filesystem access
- Creating custom MCP server integrations
- Session pooling and resource management
- Best practices for production MCP deployments

**Time to Complete**: 50-65 minutes

---

## Why MCP Matters

**Problem**: Building custom tools for every external service is time-consuming and repetitive.

**Solution**: **Model Context Protocol (MCP)** is an open standard for connecting AI agents to external tools and data sources. Instead of writing custom integrations, use **pre-built MCP servers** from the community.

**Benefits**:

- 🔌 **Plug-and-Play**: Connect to existing MCP servers instantly
- 🌐 **Community Ecosystem**: Leverage community-built tools
- [TOOLS] **Standardized Interface**: Consistent API across all tools
- 📦 **Rich Capabilities**: Filesystem, databases, APIs, and more
- [FLOW] **Reusable**: Same server works with multiple agents
- 🚀 **Extensible**: Build custom servers when needed

**MCP Ecosystem**:

- Official MCP servers: filesystem, GitHub, Slack, database, etc.
- Community servers: 100+ available
- Custom servers: Build your own for proprietary systems

---

## 1. MCP Basics

### What is Model Context Protocol?

**MCP** defines a standard way for AI models to discover and use external tools. An **MCP server** exposes:

- **Tools**: Functions the agent can call
- **Resources**: Data the agent can access
- **Prompts**: Predefined instruction templates

**Architecture**:

```
Agent (ADK)
    ↓
MCPToolset (ADK wrapper)
    ↓
MCP Client
    ↓
MCP Server (stdio/HTTP)
    ↓
External Service (filesystem, API, database, etc.)
```

**Source**: `google/adk/tools/mcp_tool/mcp_tool.py`, `mcp_toolset.py`

### MCP Connection Types

**Stdio** (Standard Input/Output):

```python
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams

# Connect via stdio (most common)
mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        command='npx',  # Node package executor
        args=['-y', '@modelcontextprotocol/server-filesystem', '/path/to/directory']
    )
)
```

**HTTP** (coming soon):

```python
# Future: HTTP-based connections
# mcp_tools = MCPToolset(
#     connection_params=HttpConnectionParams(
#         url='http://localhost:3000'
#     )
# )
```

---

## 2. Using MCP Filesystem Server

The most common MCP server is the **filesystem server**, which gives agents controlled file access.

### Basic Setup

```python
from google.adk.agents import Agent, Runner
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams

# Create MCP toolset for filesystem access
mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        command='npx',
        args=[
            '-y',  # Auto-install if needed
            '@modelcontextprotocol/server-filesystem',
            '/Users/username/documents'  # Directory to access
        ]
    )
)

# Create agent with MCP tools
agent = Agent(
    model='gemini-2.0-flash',
    name='file_assistant',
    instruction='You can read and write files in the documents directory.',
    tools=[mcp_tools]
)

runner = Runner()
result = runner.run(
    "List all text files in the directory",
    agent=agent
)

print(result.content.parts[0].text)
```

### Available Filesystem Operations

The filesystem MCP server provides these tools:

```python
# Tools automatically available through MCPToolset:

# 1. read_file - Read file contents
"Read the contents of report.txt"

# 2. write_file - Write to file
"Create a new file called notes.md with content: Hello World"

# 3. list_directory - List directory contents
"Show me all files in the current directory"

# 4. create_directory - Create new directory
"Create a folder called 'projects'"

# 5. move_file - Move or rename file
"Rename old_report.txt to archived_report.txt"

# 6. search_files - Search for files
"Find all Python files containing 'TODO'"

# 7. get_file_info - Get file metadata
"What's the size and modification date of config.json?"
```

---

## 3. Real-World Example: Document Organizer

Let's build an agent that organizes documents using MCP filesystem access.

### Complete Implementation

```python
"""
Document Organizer using MCP Filesystem Server
Automatically organizes documents by type, date, and content.
"""

import asyncio
import os
from google.adk.agents import Agent, Runner, Session
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams
from google.genai import types

# Environment setup
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = '1'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'your-project-id'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'


class DocumentOrganizer:
    """Intelligent document organizer using MCP."""

    def __init__(self, base_directory: str):
        """
        Initialize document organizer.

        Args:
            base_directory: Root directory to organize
        """

        self.base_directory = base_directory

        # Create MCP toolset for filesystem access
        self.mcp_tools = MCPToolset(
            connection_params=StdioConnectionParams(
                command='npx',
                args=[
                    '-y',
                    '@modelcontextprotocol/server-filesystem',
                    base_directory
                ]
            ),
            retry_on_closed_resource=True  # Auto-retry on connection issues
        )

        # Create organizer agent
        self.agent = Agent(
            model='gemini-2.0-flash',
            name='document_organizer',
            description='Intelligent document organization agent',
            instruction="""
You are a document organization expert with filesystem access.

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

You have access to filesystem tools:
- read_file: Read file contents
- write_file: Create files
- list_directory: List directory contents
- create_directory: Create folders
- move_file: Move/rename files
- search_files: Search by pattern
- get_file_info: Get file metadata
            """.strip(),
            tools=[self.mcp_tools],
            generate_content_config=types.GenerateContentConfig(
                temperature=0.2,  # Deterministic for file operations
                max_output_tokens=2048
            )
        )

        self.runner = Runner()
        self.session = Session()

    async def organize(self):
        """Organize documents in base directory."""

        print(f"{'='*70}")
        print(f"ORGANIZING: {self.base_directory}")
        print(f"{'='*70}\n")

        result = await self.runner.run_async(
            """
Organize all files in the directory:

1. List all files and analyze their types
2. Create appropriate folder structure
3. Move files to their logical locations
4. Generate a summary report of changes

Start by listing the directory contents.
            """.strip(),
            agent=self.agent,
            session=self.session
        )

        print("\n📊 ORGANIZATION REPORT:\n")
        print(result.content.parts[0].text)
        print(f"\n{'='*70}\n")

    async def search_documents(self, query: str):
        """
        Search documents by content.

        Args:
            query: Search query
        """

        print(f"\n🔍 SEARCHING FOR: {query}\n")

        result = await self.runner.run_async(
            f"Search all files for content related to: {query}",
            agent=self.agent,
            session=self.session
        )

        print("RESULTS:\n")
        print(result.content.parts[0].text)
        print()

    async def summarize_directory(self):
        """Generate directory summary."""

        print("\n📁 DIRECTORY SUMMARY:\n")

        result = await self.runner.run_async(
            """
Generate a comprehensive directory summary:
1. Total number of files
2. Files by type (documents, images, code, etc.)
3. Total size
4. Largest files
5. Recommendations for further organization
            """.strip(),
            agent=self.agent,
            session=self.session
        )

        print(result.content.parts[0].text)
        print()


async def main():
    """Main entry point."""

    # Set base directory
    base_dir = '/Users/username/Documents/ToOrganize'

    # Create organizer
    organizer = DocumentOrganizer(base_dir)

    # Organize documents
    await organizer.organize()

    # Search for specific content
    await organizer.search_documents('budget reports')

    # Get summary
    await organizer.summarize_directory()


if __name__ == '__main__':
    asyncio.run(main())
```

### Expected Output

```
======================================================================
ORGANIZING: /Users/username/Documents/ToOrganize
======================================================================

📊 ORGANIZATION REPORT:

**Initial Analysis:**
Found 25 files in directory:
- 8 PDF documents
- 6 Word documents (.docx)
- 5 Images (.jpg, .png)
- 3 Spreadsheets (.xlsx)
- 2 Python scripts (.py)
- 1 Text file (.txt)

**Actions Taken:**

1. **Created Folder Structure:**
   - Documents/
     - 2024/
     - Work/
     - Personal/
   - Images/
   - Code/
   - Spreadsheets/

2. **File Movements:**
   - Moved 8 PDFs to Documents/ (3 to Work/, 5 to Personal/)
   - Moved 6 DOCX files to Documents/2024/
   - Moved 5 images to Images/
   - Moved 3 spreadsheets to Spreadsheets/
   - Moved 2 Python scripts to Code/

3. **Files Renamed:**
   - IMG_1234.jpg → vacation_photo_2024.jpg
   - document.docx → project_proposal_draft.docx
   - script.py → data_processor.py

**Summary:**
✅ Organized 25 files into 6 folders
✅ Renamed 3 files for clarity
✅ Created logical structure for future files
✅ All files preserved (no deletions)

======================================================================

🔍 SEARCHING FOR: budget reports

RESULTS:

Found 3 files matching "budget reports":

1. **Documents/Work/Q3_Budget_Report.pdf**
   - Contains: Q3 financial summary, expense breakdown
   - Size: 2.4 MB
   - Modified: 2024-09-15

2. **Spreadsheets/Budget_2024.xlsx**
   - Contains: Annual budget with quarterly projections
   - Size: 156 KB
   - Modified: 2024-10-01

3. **Documents/Work/Budget_Meeting_Notes.docx**
   - Contains: Meeting notes from budget review
   - Size: 45 KB
   - Modified: 2024-09-20

📁 DIRECTORY SUMMARY:

**Directory Statistics:**
- Total Files: 25
- Total Size: 47.3 MB
- Folders: 6

**Files by Type:**
- Documents (PDF/DOCX): 14 files (35.2 MB)
- Images (JPG/PNG): 5 files (8.1 MB)
- Spreadsheets (XLSX): 3 files (2.8 MB)
- Code (PY): 2 files (18 KB)
- Other: 1 file (1.2 MB)

**Largest Files:**
1. Documents/Personal/Family_Photos_Archive.pdf (12.5 MB)
2. Images/high_res_photo.jpg (3.8 MB)
3. Spreadsheets/Annual_Data.xlsx (2.8 MB)

**Recommendations:**
- Consider archiving files older than 1 year
- Large images could be compressed
- Create additional subfolder for monthly reports in Documents/Work/
```

---

## 4. Advanced MCP Features

### Session Pooling

MCPToolset maintains a pool of connections for efficiency:

```python
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams

mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        command='npx',
        args=['-y', '@modelcontextprotocol/server-filesystem', '/path']
    ),

    # Session pooling configuration
    retry_on_closed_resource=True,  # Auto-retry on connection loss

    # Pool automatically manages:
    # - Connection reuse
    # - Resource cleanup
    # - Error recovery
)
```

### Multiple MCP Servers

Use multiple MCP servers simultaneously:

```python
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams

# Filesystem server
filesystem_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        command='npx',
        args=['-y', '@modelcontextprotocol/server-filesystem', '/documents']
    )
)

# GitHub server (hypothetical)
github_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        command='npx',
        args=['-y', '@modelcontextprotocol/server-github', '--token', 'YOUR_TOKEN']
    )
)

# Agent with multiple MCP toolsets
agent = Agent(
    model='gemini-2.0-flash',
    name='multi_tool_agent',
    instruction='You have access to both filesystem and GitHub operations.',
    tools=[filesystem_tools, github_tools]
)
```

### Resource Access

MCP servers can expose **resources** (read-only data):

```python
# Resources are automatically discovered
# Agent can access them like:
# "Read the README resource from the GitHub server"

# Resources appear as:
# - resource://server/path/to/resource
# - Automatically listed when agent queries available resources
```

---

## 5. Building Custom MCP Servers

### Simple MCP Server (Node.js)

```javascript
// custom-mcp-server.js
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

// Create server
const server = new Server(
  {
    name: "custom-calculator-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  },
);

// Register tool
server.setRequestHandler("tools/list", async () => {
  return {
    tools: [
      {
        name: "calculate",
        description: "Perform mathematical calculations",
        inputSchema: {
          type: "object",
          properties: {
            expression: {
              type: "string",
              description: "Mathematical expression to evaluate",
            },
          },
          required: ["expression"],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "calculate") {
    const expression = request.params.arguments.expression;
    try {
      const result = eval(expression); // In production, use safe math parser
      return {
        content: [
          {
            type: "text",
            text: `Result: ${result}`,
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: "text",
            text: `Error: ${error.message}`,
          },
        ],
        isError: true,
      };
    }
  }
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Using Custom MCP Server

```python
from google.adk.agents import Agent, Runner
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams

# Connect to custom server
custom_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        command='node',
        args=['custom-mcp-server.js']
    )
)

# Use in agent
agent = Agent(
    model='gemini-2.0-flash',
    name='calculator_agent',
    tools=[custom_tools]
)

runner = Runner()
result = runner.run("Calculate 25 * 4 + 10", agent=agent)

print(result.content.parts[0].text)
# Output: "The result is 110"
```

---

## 6. Popular MCP Servers

### Official MCP Servers

```python
# 1. Filesystem Server
filesystem = MCPToolset(
    connection_params=StdioConnectionParams(
        command='npx',
        args=['-y', '@modelcontextprotocol/server-filesystem', '/path']
    )
)

# 2. GitHub Server
github = MCPToolset(
    connection_params=StdioConnectionParams(
        command='npx',
        args=[
            '-y',
            '@modelcontextprotocol/server-github',
            '--token', 'YOUR_GITHUB_TOKEN'
        ]
    )
)

# 3. Slack Server
slack = MCPToolset(
    connection_params=StdioConnectionParams(
        command='npx',
        args=[
            '-y',
            '@modelcontextprotocol/server-slack',
            '--token', 'YOUR_SLACK_TOKEN'
        ]
    )
)

# 4. Postgres Server
postgres = MCPToolset(
    connection_params=StdioConnectionParams(
        command='npx',
        args=[
            '-y',
            '@modelcontextprotocol/server-postgres',
            'postgresql://user:pass@localhost:5432/dbname'
        ]
    )
)
```

### Community MCP Servers

Browse 100+ community servers at:

- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)

---

## 7. Best Practices

### ✅ DO: Use Retry on Closed Resource

```python
# ✅ Good - Auto-retry on connection loss
mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(...),
    retry_on_closed_resource=True
)

# ❌ Bad - No retry (fails on connection loss)
mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(...)
)
```

### ✅ DO: Validate Directory Paths

```python
import os

# ✅ Good - Validate path exists
directory = '/Users/username/documents'

if not os.path.exists(directory):
    raise ValueError(f"Directory does not exist: {directory}")

mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        command='npx',
        args=['-y', '@modelcontextprotocol/server-filesystem', directory]
    )
)

# ❌ Bad - No validation
mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        command='npx',
        args=['-y', '@modelcontextprotocol/server-filesystem', '/nonexistent']
    )
)
```

### ✅ DO: Provide Clear Instructions

```python
# ✅ Good - Clear tool guidance
agent = Agent(
    model='gemini-2.0-flash',
    instruction="""
You have filesystem access via MCP tools:
- read_file: Read file contents
- write_file: Create/update files
- list_directory: List directory contents
- move_file: Move/rename files

Always explain what you're doing before file operations.
    """,
    tools=[mcp_tools]
)

# ❌ Bad - No guidance
agent = Agent(
    model='gemini-2.0-flash',
    instruction="You can access files",
    tools=[mcp_tools]
)
```

### ✅ DO: Handle MCP Errors

```python
# ✅ Good - Error handling
try:
    mcp_tools = MCPToolset(
        connection_params=StdioConnectionParams(
            command='npx',
            args=['-y', '@modelcontextprotocol/server-filesystem', directory]
        )
    )

    result = runner.run(query, agent=agent)

except Exception as e:
    print(f"MCP Error: {e}")
    # Fallback behavior

# ❌ Bad - No error handling
mcp_tools = MCPToolset(...)  # May fail silently
```

---

## 8. Troubleshooting

### Error: "npx command not found"

**Problem**: Node.js not installed

**Solution**:

```bash
# Install Node.js
# macOS:
brew install node

# Ubuntu:
sudo apt install nodejs npm

# Verify
npx --version
```

### Error: "MCP server connection failed"

**Problem**: Server not starting or wrong command

**Solutions**:

1. **Test server manually**:

```bash
# Run server directly to see errors
npx -y @modelcontextprotocol/server-filesystem /path/to/dir
```

2. **Check path**:

```python
import os

directory = '/Users/username/documents'
print(f"Path exists: {os.path.exists(directory)}")
print(f"Absolute path: {os.path.abspath(directory)}")
```

3. **Use correct command**:

```python
# ✅ Correct
StdioConnectionParams(
    command='npx',  # Not 'npm' or 'node'
    args=['-y', '@modelcontextprotocol/server-filesystem', directory]
)
```

### Issue: "Tools not appearing"

**Problem**: MCP server not exposing tools correctly

**Solution**: Check server logs and tool discovery:

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# ADK will log MCP tool discovery
mcp_tools = MCPToolset(...)
```

---

## 9. Testing MCP Integrations

### Unit Tests

```python
import pytest
import os
import tempfile
from google.adk.agents import Agent, Runner
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams

@pytest.mark.asyncio
async def test_mcp_filesystem_read():
    """Test reading file via MCP."""

    # Create temp directory and file
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, 'test.txt')

        with open(test_file, 'w') as f:
            f.write('Hello MCP')

        # Create MCP toolset
        mcp_tools = MCPToolset(
            connection_params=StdioConnectionParams(
                command='npx',
                args=['-y', '@modelcontextprotocol/server-filesystem', tmpdir]
            )
        )

        # Create agent
        agent = Agent(
            model='gemini-2.0-flash',
            tools=[mcp_tools]
        )

        runner = Runner()
        result = await runner.run_async(
            "Read the contents of test.txt",
            agent=agent
        )

        # Verify
        text = result.content.parts[0].text
        assert 'Hello MCP' in text


@pytest.mark.asyncio
async def test_mcp_filesystem_write():
    """Test writing file via MCP."""

    with tempfile.TemporaryDirectory() as tmpdir:
        mcp_tools = MCPToolset(
            connection_params=StdioConnectionParams(
                command='npx',
                args=['-y', '@modelcontextprotocol/server-filesystem', tmpdir]
            )
        )

        agent = Agent(
            model='gemini-2.0-flash',
            tools=[mcp_tools]
        )

        runner = Runner()
        result = await runner.run_async(
            "Create a file called output.txt with content: Test content",
            agent=agent
        )

        # Verify file created
        output_file = os.path.join(tmpdir, 'output.txt')
        assert os.path.exists(output_file)

        with open(output_file) as f:
            content = f.read()
            assert 'Test content' in content
```

---

## 7. MCP OAuth Authentication

**Source**: `google/adk/tools/mcp_tool/mcp_tool.py`, `contributing/samples/oauth2_client_credentials/`

MCP supports **multiple authentication methods** for securing access to MCP servers. This is critical for production deployments where MCP servers access sensitive resources.

### Supported Authentication Methods

ADK's MCP implementation supports:

1. **OAuth2** (Client Credentials flow)
2. **HTTP Bearer Token**
3. **HTTP Basic Authentication**
4. **API Key**

### OAuth2 Authentication (Most Secure)

OAuth2 is the **recommended authentication method** for production MCP servers.

**Use Case**: Accessing protected APIs, enterprise data sources, cloud services.

**Implementation**:

```python
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams
from google.adk.agents import Agent, Runner

# OAuth2 Client Credentials configuration
mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        command='npx',
        args=['-y', '@mycompany/secure-mcp-server']
    ),
    credential={
        'type': 'oauth2',
        'token_url': 'https://auth.example.com/oauth/token',
        'client_id': 'your-client-id',
        'client_secret': 'your-client-secret',
        'scopes': ['read', 'write']  # Optional
    }
)

agent = Agent(
    model='gemini-2.5-flash',
    name='secure_agent',
    instruction='You have authenticated access to secure resources.',
    tools=[mcp_tools]
)
```

**How It Works**:

1. ADK automatically requests access token from `token_url`
2. Token included in all MCP server requests
3. Token refreshed automatically when expired
4. Secure credential handling throughout

### HTTP Bearer Token (Simple)

For MCP servers that use bearer tokens.

```python
mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        command='npx',
        args=['-y', '@mycompany/api-server']
    ),
    credential={
        'type': 'bearer',
        'token': 'your-bearer-token-here'
    }
)
```

**When to use**: APIs with static bearer tokens, internal services.

### HTTP Basic Authentication

For MCP servers using username/password.

```python
mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        command='npx',
        args=['-y', '@mycompany/legacy-server']
    ),
    credential={
        'type': 'basic',
        'username': 'admin',
        'password': 'secure-password'
    }
)
```

**When to use**: Legacy systems, simple internal tools.

### API Key Authentication

For MCP servers using API key headers.

```python
mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        command='npx',
        args=['-y', '@mycompany/api-gateway']
    ),
    credential={
        'type': 'api_key',
        'key': 'your-api-key',
        'header': 'X-API-Key'  # Optional, default: 'Authorization'
    }
)
```

**When to use**: Cloud services, third-party APIs.

### Complete OAuth2 Example: Secure Document Server

```python
"""
OAuth2-secured MCP server integration.
Source: contributing/samples/oauth2_client_credentials/oauth2_test_server.py
"""

import asyncio
import os
from google.adk.agents import Agent, Runner
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams

# Environment setup
os.environ['GOOGLE_GENAI_USE_VERTEXAI'] = '1'
os.environ['GOOGLE_CLOUD_PROJECT'] = 'your-project'
os.environ['GOOGLE_CLOUD_LOCATION'] = 'us-central1'


async def main():
    """Demonstrate OAuth2-secured MCP integration."""

    # OAuth2 configuration
    oauth2_credential = {
        'type': 'oauth2',
        'token_url': 'https://auth.company.com/oauth/token',
        'client_id': os.environ.get('OAUTH_CLIENT_ID'),
        'client_secret': os.environ.get('OAUTH_CLIENT_SECRET'),
        'scopes': ['documents.read', 'documents.write']
    }

    # Create MCP toolset with OAuth2
    secure_mcp_tools = MCPToolset(
        connection_params=StdioConnectionParams(
            command='npx',
            args=[
                '-y',
                '@company/secure-document-server',
                '--environment', 'production'
            ]
        ),
        credential=oauth2_credential,
        retry_on_closed_resource=True
    )

    # Create agent with authenticated MCP access
    agent = Agent(
        model='gemini-2.5-flash',
        name='secure_document_agent',
        description='Agent with OAuth2-secured document access',
        instruction="""
You have authenticated access to the company document server.
You can:
- Read confidential documents
- Create new documents with proper permissions
- Search across authorized document repositories
- Respect access control policies

Always handle sensitive information appropriately.
        """.strip(),
        tools=[secure_mcp_tools]
    )

    # Run queries with authentication
    runner = Runner()

    print("\n" + "="*60)
    print("SECURE MCP SERVER WITH OAUTH2")
    print("="*60 + "\n")

    # Query 1: Read secure document
    result1 = await runner.run_async(
        "Read the Q4 financial report from the secure archive.",
        agent=agent
    )
    print("📄 Q4 Report:\n")
    print(result1.content.parts[0].text)

    await asyncio.sleep(1)

    # Query 2: Create document
    result2 = await runner.run_async(
        "Create a summary document of key findings from the Q4 report.",
        agent=agent
    )
    print("\n\n📝 Summary Created:\n")
    print(result2.content.parts[0].text)

    print("\n" + "="*60 + "\n")


if __name__ == '__main__':
    asyncio.run(main())
```

### How Authentication Works Internally

**Source**: `google/adk/tools/mcp_tool/mcp_tool.py` (simplified):

```python
class McpTool:
    """Individual MCP tool with authentication."""

    def _get_headers(self, credential: dict) -> dict:
        """Generate authentication headers based on credential type."""

        if credential['type'] == 'oauth2':
            # Fetch OAuth2 access token
            token = self._fetch_oauth2_token(
                token_url=credential['token_url'],
                client_id=credential['client_id'],
                client_secret=credential['client_secret'],
                scopes=credential.get('scopes', [])
            )
            return {'Authorization': f'Bearer {token}'}

        elif credential['type'] == 'bearer':
            return {'Authorization': f"Bearer {credential['token']}"}

        elif credential['type'] == 'basic':
            # Base64 encode username:password
            import base64
            creds = f"{credential['username']}:{credential['password']}"
            encoded = base64.b64encode(creds.encode()).decode()
            return {'Authorization': f'Basic {encoded}'}

        elif credential['type'] == 'api_key':
            header_name = credential.get('header', 'Authorization')
            return {header_name: credential['key']}

        return {}
```

### Best Practices for Authentication

**DO**:

- ✅ Use OAuth2 for production systems
- ✅ Store credentials in environment variables (not hardcoded!)
- ✅ Use least-privilege scopes (only necessary permissions)
- ✅ Rotate credentials regularly
- ✅ Monitor authentication failures
- ✅ Test with expired tokens

**DON'T**:

- ❌ Commit credentials to version control
- ❌ Use same credentials across environments (dev/prod)
- ❌ Share credentials between agents
- ❌ Ignore token expiration
- ❌ Use Basic auth for internet-facing services

### Credential Management

**Environment Variables** (Recommended):

```python
import os

# Load from environment
oauth2_credential = {
    'type': 'oauth2',
    'token_url': os.environ['OAUTH_TOKEN_URL'],
    'client_id': os.environ['OAUTH_CLIENT_ID'],
    'client_secret': os.environ['OAUTH_CLIENT_SECRET'],
    'scopes': os.environ.get('OAUTH_SCOPES', '').split(',')
}

mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(...),
    credential=oauth2_credential
)
```

**Secret Manager** (Production):

```python
from google.cloud import secretmanager

def get_oauth_credentials():
    """Fetch OAuth2 credentials from Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()

    # Fetch secrets
    client_id = client.access_secret_version(
        name="projects/PROJECT/secrets/oauth-client-id/versions/latest"
    ).payload.data.decode()

    client_secret = client.access_secret_version(
        name="projects/PROJECT/secrets/oauth-client-secret/versions/latest"
    ).payload.data.decode()

    return {
        'type': 'oauth2',
        'token_url': 'https://auth.company.com/oauth/token',
        'client_id': client_id,
        'client_secret': client_secret
    }

mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(...),
    credential=get_oauth_credentials()
)
```

### Testing Authentication

```python
import pytest
from unittest.mock import Mock, patch

@pytest.mark.asyncio
async def test_mcp_oauth2_authentication():
    """Test MCP with OAuth2 authentication."""

    # Mock OAuth2 token endpoint
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {
            'access_token': 'test-token-123',
            'token_type': 'Bearer',
            'expires_in': 3600
        }

        # Create MCP toolset with OAuth2
        mcp_tools = MCPToolset(
            connection_params=StdioConnectionParams(
                command='npx',
                args=['-y', '@test/secure-server']
            ),
            credential={
                'type': 'oauth2',
                'token_url': 'https://auth.test.com/token',
                'client_id': 'test-client',
                'client_secret': 'test-secret'
            }
        )

        # Verify token was fetched
        mock_post.assert_called_once()

        # Test agent with authenticated MCP
        agent = Agent(
            model='gemini-2.5-flash',
            tools=[mcp_tools]
        )

        runner = Runner()
        result = await runner.run_async(
            "Test authenticated query",
            agent=agent
        )

        # Verify authentication worked
        assert result is not None


@pytest.mark.asyncio
async def test_mcp_bearer_token():
    """Test MCP with bearer token."""

    mcp_tools = MCPToolset(
        connection_params=StdioConnectionParams(
            command='npx',
            args=['-y', '@test/api-server']
        ),
        credential={
            'type': 'bearer',
            'token': 'test-bearer-token'
        }
    )

    agent = Agent(
        model='gemini-2.5-flash',
        tools=[mcp_tools]
    )

    runner = Runner()
    result = await runner.run_async("Test query", agent=agent)

    assert result is not None
```

### Troubleshooting Authentication

**Error: "401 Unauthorized"**

- Check credential type matches server expectation
- Verify client_id and client_secret are correct
- Check token hasn't expired
- Verify scopes include necessary permissions

**Error: "403 Forbidden"**

- Check user has required permissions
- Verify scopes are sufficient
- Check rate limits not exceeded

**Error: "Token refresh failed"**

- Verify token_url is accessible
- Check network connectivity
- Verify OAuth2 server is operational

**Error: "Invalid credentials"**

- Double-check credential dictionary structure
- Verify credential type ('oauth2', 'bearer', 'basic', 'api_key')
- Check for typos in credential fields

---

## Summary

You've mastered MCP integration and authentication for extended agent capabilities:

**Key Takeaways**:

- ✅ MCP provides standardized protocol for external tools
- ✅ `MCPToolset` connects agents to MCP servers
- ✅ `StdioConnectionParams` for stdio-based servers
- ✅ Filesystem server most common (file operations)
- ✅ Session pooling for efficiency
- ✅ `retry_on_closed_resource=True` for reliability
- ✅ **OAuth2 authentication** for secure production deployments
- ✅ Multiple auth methods supported (OAuth2, Bearer, Basic, API Key)
- ✅ Credential management via environment variables or Secret Manager
- ✅ 100+ community MCP servers available
- ✅ Can build custom MCP servers in Node.js

**Production Checklist**:

- [ ] Node.js/npx installed
- [ ] Directory paths validated
- [ ] `retry_on_closed_resource=True` enabled
- [ ] **Authentication configured** (OAuth2 for production)
- [ ] **Credentials stored securely** (environment variables or Secret Manager)
- [ ] **OAuth2 scopes** set to least-privilege
- [ ] Clear instructions for MCP tools
- [ ] Error handling for connection failures
- [ ] **Authentication error handling** (401, 403)
- [ ] Testing with actual MCP servers
- [ ] **Testing with expired tokens**
- [ ] Monitoring MCP server health
- [ ] Appropriate permissions for file access

**Next Steps**:

- **Tutorial 17**: Learn Agent-to-Agent (A2A) communication
- **Tutorial 18**: Master Events & Observability
- **Tutorial 19**: Implement Artifacts & File Management

**Resources**:

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Official MCP Servers](https://github.com/modelcontextprotocol/servers)
- [Sample: mcp_stdio_server_agent](https://github.com/google/adk-python/tree/main/contributing/samples/mcp_stdio_server_agent/)

---

**🎉 Tutorial 16 Complete!** You now know how to extend your agents with MCP tool servers. Continue to Tutorial 17 to learn about agent-to-agent communication.
