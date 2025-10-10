"""
Test import functionality
"""

import pytest


class TestImports:
    """Test that all required imports work correctly"""

    def test_import_agent_module(self):
        """Test importing agent module"""
        from mcp_agent import agent
        assert agent is not None

    def test_import_root_agent(self):
        """Test importing root_agent"""
        from mcp_agent import root_agent
        assert root_agent is not None

    def test_import_create_function(self):
        """Test importing create function"""
        from mcp_agent.agent import create_mcp_filesystem_agent
        assert create_mcp_filesystem_agent is not None

    def test_import_document_organizer(self):
        """Test importing document organizer"""
        from mcp_agent.document_organizer import create_document_organizer_agent
        assert create_document_organizer_agent is not None

    def test_import_adk_core(self):
        """Test importing ADK core modules"""
        from google.adk.agents import Agent
        from google.adk import Runner
        assert Agent is not None
        assert Runner is not None

    def test_import_mcp_tools(self):
        """Test importing MCP tools"""
        from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams
        assert MCPToolset is not None
        assert StdioConnectionParams is not None

    def test_import_mcp_connection_types(self):
        """Test importing MCP connection types (ADK 1.16.0+)"""
        from google.adk.tools.mcp_tool import (
            SseConnectionParams,
            StreamableHTTPConnectionParams
        )
        assert SseConnectionParams is not None
        assert StreamableHTTPConnectionParams is not None

    def test_import_auth_credential(self):
        """Test importing auth credential classes (ADK 1.16.0+)"""
        try:
            from google.adk.auth.auth_credential import (
                AuthCredential,
                AuthCredentialTypes
            )
            assert AuthCredential is not None
            assert AuthCredentialTypes is not None
        except ImportError:
            pytest.skip("Auth credential classes not available in this ADK version")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
