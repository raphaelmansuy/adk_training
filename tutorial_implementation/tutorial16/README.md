# Tutorial 16: MCP Integration

**Learn Model Context Protocol (MCP) integration with Google ADK for standardized tool access.**

## Overview

This implementation demonstrates how to:
- Connect agents to MCP servers using `MCPToolset`
- **Implement Human-in-the-Loop (HITL) approval workflow** ✨ NEW
- **Restrict filesystem access to safe directories** 🔒 SECURITY
- Use stdio, SSE, and HTTP connection types
- Implement filesystem operations via MCP
- Build document organization systems
- Handle OAuth2 authentication for production deployments

## 🔒 Security Features

- **Directory Scoping**: MCP server restricted to `sample_files/` directory only
- **Human-in-the-Loop**: Destructive operations require user approval
- **Operation Logging**: All file operations are logged for audit
- **Before-tool Callbacks**: Validation and authorization before execution

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js and npx (for MCP servers)
- Google API Key

### Installation

```bash
# 1. Install dependencies
make setup

# 2. Configure environment
cp mcp_agent/.env.example mcp_agent/.env
# Edit mcp_agent/.env and add your GOOGLE_API_KEY

# 3. Start development server
make dev

# 4. Open http://localhost:8000 in your browser
```

### Verify Installation

```bash
# Check Node.js is installed
make check-node

# Run tests
make test
```

### Quick Demo

```bash
# See what the agent can do
make about

# Create sample files to experiment with
make create-sample-files

# Start the agent and try organizing files
make dev
# Then ask: "Organize the sample_files/mixed_content folder by file type"

# View example prompts
make demo

# Clean up sample files when done
make clean-samples
```

## Project Structure

```
tutorial16/
├── mcp_agent/              # Agent implementation
│   ├── __init__.py         # Package exports
│   ├── agent.py            # Root agent with MCP filesystem
│   ├── document_organizer.py  # Document organization example
│   └── .env.example        # Environment template
├── tests/                  # Test suite
│   ├── test_agent.py       # Agent configuration tests
│   ├── test_imports.py     # Import validation
│   └── test_structure.py   # Project structure tests
├── Makefile                # Development commands
├── requirements.txt        # Dependencies
├── pyproject.toml          # Package configuration
└── README.md               # This file
```

## Features

### 1. Human-in-the-Loop (HITL) Workflow

**What is Human-in-the-Loop?**

HITL is a safety pattern where the agent requests human approval before performing sensitive operations. This prevents accidental data loss and gives users control over destructive actions.

**Implementation in this agent:**

```python
# Destructive operations require approval
DESTRUCTIVE_OPERATIONS = {
    'write_file': 'Writing files modifies content',
    'write_text_file': 'Writing files modifies content',
    'move_file': 'Moving files changes file locations',
    'create_directory': 'Creating directories modifies filesystem structure',
}

# Read operations are allowed automatically
SAFE_OPERATIONS = [
    'read_file',
    'list_directory',
    'search_files',
    'get_file_info'
]
```

**How it works:**

1. **Before Tool Callback**: Intercepts every tool call before execution
2. **Operation Classification**: Checks if operation is destructive
3. **Approval Request**: Pauses execution and requests user confirmation
4. **Logging**: Records all operations for audit trail

**Try it yourself:**

```bash
# Start the agent
make dev

# Try a safe operation (works immediately)
"List all files in sample_files"

# Try a destructive operation (requires approval)
"Create a new file called test.txt with content: Hello World"
# Agent response: "⚠️ APPROVAL REQUIRED - This operation has been BLOCKED for safety"

# To approve operations, set the approval flag in ADK state
# state['user:auto_approve_file_ops'] = True
```

**ADK Best Practice:**

Use `before_tool_callback` for:
- ✅ Input validation and sanitization
- ✅ Authorization checks and permissions
- ✅ Rate limiting and quota management
- ✅ Audit logging for compliance
- ✅ Human approval for sensitive operations

### 2. Restricted Filesystem Access

**Security by Design:**

The agent is **restricted to `sample_files/` directory only**. This prevents:
- ❌ Accessing system files
- ❌ Modifying important project files
- ❌ Reading sensitive configuration
- ❌ Deleting critical data

**Implementation:**

```python
# MCP server is scoped to specific directory
server_params = StdioServerParameters(
    command='npx',
    args=[
        '-y',
        '@modelcontextprotocol/server-filesystem',
        '/path/to/sample_files'  # Only this directory is accessible
    ]
)
```

**Why this matters:**

In production, you can:
- Give agents access to specific customer data folders
- Prevent cross-customer data leakage
- Implement per-user directory isolation
- Audit all file operations within scope

### 3. MCP Filesystem Agent

The core agent provides filesystem access via MCP:

```python
from mcp_agent import root_agent
from google.adk.agents import Runner

runner = Runner()
result = runner.run(
    "List all files in the current directory",
    agent=root_agent
)
```

**Available Operations:**
- `read_file` - Read file contents
- `write_file` - Create/update files
- `list_directory` - List directory contents
- `create_directory` - Create folders
- `move_file` - Move/rename files
- `search_files` - Search by pattern
- `get_file_info` - Get file metadata

### 2. Document Organizer

Automated document organization system:

```python
from mcp_agent.document_organizer import DocumentOrganizer
import asyncio

async def main():
    organizer = DocumentOrganizer('/path/to/documents')
    await organizer.organize()
    await organizer.search_documents('budget reports')
    await organizer.summarize_directory()

asyncio.run(main())
```

### 3. Connection Types (ADK 1.16.0+)

**Stdio Connection** (Local):
```python
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams

mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        command='npx',
        args=['-y', '@modelcontextprotocol/server-filesystem', '/path']
    )
)
```

**SSE Connection** (Remote):
```python
from google.adk.tools.mcp_tool import SseConnectionParams

mcp_tools = MCPToolset(
    connection_params=SseConnectionParams(
        url='https://api.example.com/mcp/sse',
        timeout=30.0,
        sse_read_timeout=300.0
    )
)
```

**HTTP Streaming** (Remote):
```python
from google.adk.tools.mcp_tool import StreamableHTTPConnectionParams

mcp_tools = MCPToolset(
    connection_params=StreamableHTTPConnectionParams(
        url='https://api.example.com/mcp/stream',
        timeout=30.0
    )
)
```

### 4. OAuth2 Authentication

Secure MCP server access:

```python
from google.adk.auth.auth_credential import (
    AuthCredential, AuthCredentialTypes, OAuth2Auth
)

oauth2_credential = AuthCredential(
    auth_type=AuthCredentialTypes.OAUTH2,
    oauth2=OAuth2Auth(
        client_id='your-client-id',
        client_secret='your-client-secret',
        auth_uri='https://auth.example.com/authorize',
        token_uri='https://auth.example.com/token',
        scopes=['read', 'write']
    )
)

mcp_tools = MCPToolset(
    connection_params=SseConnectionParams(url='...'),
    auth_credential=oauth2_credential
)
```

## Demo Prompts

### Using Sample Files

Create a playground with diverse file types to test the agent:

```bash
# Create sample files for testing
make create-sample-files

# This creates:
#   - Text documents (document1.txt, notes.txt, meeting_notes.txt)
#   - Code files (script.py, app.js, main.go)
#   - Config files (package.json, config.toml, settings.yaml)
#   - Documentation (README.md, TODO.md)
#   - Data files (data.csv, users.json)
#   - Mixed unsorted files in mixed_content/

# Now start the agent
make dev

# Clean up when done
make clean-samples
```

Try these in the ADK UI (<http://localhost:8000>):

### Basic Operations

1. **List Files:**

   ```text
   List all files in the sample_files directory
   ```

2. **Read File:**

   ```text
   Read the contents of sample_files/README.md
   ```

3. **Create File:**

   ```text
   Create a new file called test.txt with content: Hello MCP!
   ```

4. **Search Files:**

   ```text
   Find all Python files in sample_files
   ```

5. **File Info:**

   ```text
   What is the size and last modified date of requirements.txt?
   ```

### Advanced Operations

1. **Directory Organization:**

   ```text
   Organize the sample_files/mixed_content folder by file type
   ```

2. **File Analysis:**

   ```text
   Analyze all code files in sample_files and list their main functions
   ```

3. **Batch Operations:**

   ```text
   Create folders named 'code', 'docs', and 'config', then move files accordingly
   ```

4. **Content Summary:**

   ```text
   Read all markdown files in sample_files and create a combined summary
   ```

8. **Batch Operations:**
   ```
   Find all image files and move them to an Images folder
   ```

## Testing

Run the comprehensive test suite:

```bash
# All tests
make test

# Specific test file
pytest tests/test_agent.py -v

# With coverage
pytest tests/ --cov=mcp_agent --cov-report=html
```

**Test Coverage:**
- Agent configuration and creation
- MCP toolset initialization
- Connection parameter validation
- Import verification
- Project structure validation
- ADK 1.16.0+ feature compatibility

## Environment Configuration

The `.env.example` file contains all available options:

```bash
# Required
GOOGLE_API_KEY=your_api_key_here

# Optional: Vertex AI
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1

# Optional: MCP Configuration
MCP_BASE_DIRECTORY=/path/to/your/directory

# Optional: OAuth2
OAUTH_CLIENT_ID=your-client-id
OAUTH_CLIENT_SECRET=your-client-secret
OAUTH_TOKEN_URL=https://auth.example.com/token

# Optional: SSE/HTTP
MCP_SSE_URL=https://api.example.com/sse
MCP_HTTP_URL=https://api.example.com/stream
```

## Common Issues

### "npx command not found"

**Problem:** Node.js not installed

**Solution:**
```bash
# macOS
brew install node

# Ubuntu
sudo apt install nodejs npm

# Verify
npx --version
```

### "MCP server connection failed"

**Problem:** Server not starting or wrong path

**Solution:**
1. Test server manually:
   ```bash
   npx -y @modelcontextprotocol/server-filesystem /path/to/dir
   ```

2. Verify directory exists:
   ```python
   import os
   print(os.path.exists('/path/to/dir'))
   ```

3. Check logs for errors

### "Import errors"

**Problem:** Missing dependencies

**Solution:**
```bash
pip install -r requirements.txt
pip install -e .
```

## Key Learnings

### MCP Benefits

- ✅ Standardized protocol for tool integration
- ✅ Community ecosystem of 100+ servers
- ✅ Multiple connection types (stdio, SSE, HTTP)
- ✅ Secure authentication support
- ✅ Production-ready patterns

### Best Practices

- ✅ Validate directory paths before MCP connection
- ✅ Use OAuth2 for production deployments
- ✅ Provide clear instructions to agents
- ✅ Handle connection errors gracefully
- ✅ Test with actual MCP servers
- ✅ Monitor MCP server health

### Production Checklist

- [ ] Node.js/npx installed
- [ ] Directory paths validated
- [ ] Authentication configured
- [ ] Credentials stored securely
- [ ] Error handling implemented
- [ ] Tests passing
- [ ] Monitoring in place

## Resources

- **Tutorial Documentation:** [docs/tutorial/16_mcp_integration.md](../../docs/tutorial/16_mcp_integration.md)
- **MCP Specification:** https://spec.modelcontextprotocol.io/
- **Official MCP Servers:** https://github.com/modelcontextprotocol/servers
- **ADK Documentation:** https://google.github.io/adk-docs/

## Next Steps

After mastering MCP integration:

1. **Tutorial 17:** Agent-to-Agent (A2A) Communication
2. **Tutorial 18:** Events & Observability
3. **Tutorial 19:** Artifacts & File Management

## License

Part of the ADK Training repository - Educational purposes.

---

**Need Help?** Check the tutorial documentation or open an issue in the repository.
