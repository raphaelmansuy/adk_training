"""
Test agent configuration and functionality
"""

import pytest
import os
import tempfile
from mcp_agent.agent import create_mcp_filesystem_agent, root_agent


class TestAgentConfig:
    """Test agent configuration"""

    def test_root_agent_exists(self):
        """Test root_agent variable exists"""
        assert root_agent is not None

    def test_agent_has_correct_model(self):
        """Test agent uses correct model"""
        assert root_agent.model == 'gemini-2.0-flash-exp'

    def test_agent_has_name(self):
        """Test agent has correct name"""
        assert root_agent.name == 'mcp_file_assistant'

    def test_agent_has_description(self):
        """Test agent has description"""
        assert root_agent.description is not None
        assert len(root_agent.description) > 0

    def test_agent_has_instruction(self):
        """Test agent has instruction"""
        assert root_agent.instruction is not None
        assert 'filesystem' in root_agent.instruction.lower()

    def test_agent_has_tools(self):
        """Test agent has tools configured"""
        assert root_agent.tools is not None
        assert len(root_agent.tools) > 0


class TestAgentCreation:
    """Test agent creation functions"""

    def test_create_agent_with_default_directory(self):
        """Test creating agent with default directory"""
        agent = create_mcp_filesystem_agent()
        assert agent is not None
        assert agent.name == 'mcp_file_assistant'

    def test_create_agent_with_custom_directory(self):
        """Test creating agent with custom directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            agent = create_mcp_filesystem_agent(tmpdir)
            assert agent is not None

    def test_create_agent_with_invalid_directory(self):
        """Test creating agent with non-existent directory raises error"""
        with pytest.raises(ValueError, match="Directory does not exist"):
            create_mcp_filesystem_agent("/nonexistent/directory/path")


class TestMCPToolset:
    """Test MCP toolset configuration"""

    def test_mcp_imports_available(self):
        """Test MCP imports are available"""
        from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
        assert McpToolset is not None
        assert StdioConnectionParams is not None

    def test_stdio_connection_params(self):
        """Test StdioConnectionParams can be created"""
        from google.adk.tools.mcp_tool import StdioConnectionParams
        from mcp.client.stdio import StdioServerParameters

        server_params = StdioServerParameters(
            command='npx',
            args=['-y', '@modelcontextprotocol/server-filesystem', '/tmp']
        )
        params = StdioConnectionParams(server_params=server_params)
        assert params is not None
        assert params.server_params.command == 'npx'

    @pytest.mark.skipif(
        os.environ.get('SKIP_MCP_INTEGRATION') == 'true',
        reason="MCP integration tests skipped (requires Node.js and npx)"
    )
    def test_mcp_toolset_creation(self):
        """Test MCPToolset can be created with StdioConnectionParams"""
        from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
        from mcp.client.stdio import StdioServerParameters

        with tempfile.TemporaryDirectory() as tmpdir:
            server_params = StdioServerParameters(
                command='npx',
                args=[
                    '-y',
                    '@modelcontextprotocol/server-filesystem',
                    tmpdir
                ]
            )
            mcp_tools = McpToolset(
                connection_params=StdioConnectionParams(
                    server_params=server_params
                )
            )
            assert mcp_tools is not None


class TestADKVersion:
    """Test ADK version compatibility"""

    def test_adk_1_16_features(self):
        """Test ADK 1.16.0+ features are available"""
        # Test SSE connection params
        from google.adk.tools.mcp_tool import SseConnectionParams
        assert SseConnectionParams is not None

        # Test HTTP connection params
        from google.adk.tools.mcp_tool import StreamableHTTPConnectionParams
        assert StreamableHTTPConnectionParams is not None

    def test_sse_connection_params(self):
        """Test SseConnectionParams can be created"""
        from google.adk.tools.mcp_tool import SseConnectionParams

        params = SseConnectionParams(
            url='https://api.example.com/sse',
            timeout=30.0,
            sse_read_timeout=300.0
        )
        assert params is not None
        assert params.url == 'https://api.example.com/sse'

    def test_http_connection_params(self):
        """Test StreamableHTTPConnectionParams can be created"""
        from google.adk.tools.mcp_tool import StreamableHTTPConnectionParams

        params = StreamableHTTPConnectionParams(
            url='https://api.example.com/http',
            timeout=30.0,
            sse_read_timeout=300.0
        )
        assert params is not None
        assert params.url == 'https://api.example.com/http'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
