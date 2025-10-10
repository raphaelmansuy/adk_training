"""
Tests for Human-in-the-Loop (HITL) callback functionality.

This module tests the before_tool_callback implementation for:
- Tool name extraction from tool objects
- Destructive operation detection
- Approval workflow logic
- State management
- Logging behavior
"""

import pytest
from unittest.mock import Mock
from mcp_agent.agent import before_tool_callback


class TestToolNameExtraction:
    """Test that tool names are correctly extracted from tool objects."""
    
    def test_extract_name_from_tool_with_name_attribute(self):
        """Tool with .name attribute should use that name."""
        # Create a mock tool object with name attribute
        mock_tool = Mock()
        mock_tool.name = "write_file"
        
        # Create mock tool_context with state
        mock_context = Mock()
        mock_context.state = {}
        
        # Call callback
        before_tool_callback(
            tool=mock_tool,
            args={'path': '/test/file.txt', 'content': 'test'},
            tool_context=mock_context
        )
        
        # Should track tool name in state
        assert mock_context.state.get('temp:last_tool') == 'write_file'
    
    def test_extract_name_from_tool_without_name_attribute(self):
        """Tool without .name attribute should use string representation."""
        # Create a mock tool object without name attribute
        mock_tool = Mock(spec=[])  # No attributes
        
        # Create mock tool_context with state
        mock_context = Mock()
        mock_context.state = {}
        
        # Call callback
        before_tool_callback(
            tool=mock_tool,
            args={'path': '/test/file.txt'},
            tool_context=mock_context
        )
        
        # Should use string representation
        assert 'temp:last_tool' in mock_context.state
        assert isinstance(mock_context.state['temp:last_tool'], str)


class TestDestructiveOperationDetection:
    """Test detection of operations requiring approval."""
    
    @pytest.mark.parametrize("operation_name", [
        "write_file",
        "write_text_file",
        "move_file",
        "create_directory"
    ])
    def test_destructive_operations_require_approval(self, operation_name):
        """All destructive operations should require approval when not auto-approved."""
        mock_tool = Mock()
        mock_tool.name = operation_name
        
        mock_context = Mock()
        mock_context.state = {}  # No auto_approve flag
        
        result = before_tool_callback(
            tool=mock_tool,
            args={'path': '/test/file.txt'},
            tool_context=mock_context
        )
        
        # Should return approval required message
        assert result is not None
        assert result['status'] == 'requires_approval'
        assert 'APPROVAL REQUIRED' in result['message']
        assert result['tool_name'] == operation_name
        assert result['requires_approval'] is True
    
    @pytest.mark.parametrize("operation_name", [
        "read_file",
        "list_directory",
        "search_files",
        "get_file_info"
    ])
    def test_safe_operations_allowed_without_approval(self, operation_name):
        """Safe read operations should be allowed without approval."""
        mock_tool = Mock()
        mock_tool.name = operation_name
        
        mock_context = Mock()
        mock_context.state = {}
        
        result = before_tool_callback(
            tool=mock_tool,
            args={'path': '/test/file.txt'},
            tool_context=mock_context
        )
        
        # Should return None to allow execution
        assert result is None


class TestApprovalWorkflow:
    """Test the approval workflow logic."""
    
    def test_auto_approve_flag_bypasses_approval(self):
        """When auto_approve is True, destructive operations should be allowed."""
        mock_tool = Mock()
        mock_tool.name = "write_file"
        
        mock_context = Mock()
        mock_context.state = {
            'user:auto_approve_file_ops': True
        }
        
        result = before_tool_callback(
            tool=mock_tool,
            args={'path': '/test/file.txt', 'content': 'test'},
            tool_context=mock_context
        )
        
        # Should return None to allow execution
        assert result is None
    
    def test_missing_auto_approve_flag_blocks_destructive_ops(self):
        """When auto_approve flag is missing, destructive operations should be blocked."""
        mock_tool = Mock()
        mock_tool.name = "write_file"
        
        mock_context = Mock()
        mock_context.state = {}  # No auto_approve flag
        
        result = before_tool_callback(
            tool=mock_tool,
            args={'path': '/test/file.txt', 'content': 'test'},
            tool_context=mock_context
        )
        
        # Should return blocking response
        assert result is not None
        assert result['status'] == 'requires_approval'
    
    def test_false_auto_approve_flag_blocks_destructive_ops(self):
        """When auto_approve is explicitly False, destructive operations should be blocked."""
        mock_tool = Mock()
        mock_tool.name = "write_file"
        
        mock_context = Mock()
        mock_context.state = {
            'user:auto_approve_file_ops': False
        }
        
        result = before_tool_callback(
            tool=mock_tool,
            args={'path': '/test/file.txt', 'content': 'test'},
            tool_context=mock_context
        )
        
        # Should return blocking response
        assert result is not None
        assert result['status'] == 'requires_approval'


class TestStateManagement:
    """Test state tracking in the callback."""
    
    def test_tool_count_increments(self):
        """Tool count should increment with each call."""
        mock_tool = Mock()
        mock_tool.name = "read_file"
        
        mock_context = Mock()
        mock_context.state = {}
        
        # First call
        before_tool_callback(
            tool=mock_tool,
            args={'path': '/test/file1.txt'},
            tool_context=mock_context
        )
        assert mock_context.state['temp:tool_count'] == 1
        
        # Second call
        before_tool_callback(
            tool=mock_tool,
            args={'path': '/test/file2.txt'},
            tool_context=mock_context
        )
        assert mock_context.state['temp:tool_count'] == 2
        
        # Third call
        before_tool_callback(
            tool=mock_tool,
            args={'path': '/test/file3.txt'},
            tool_context=mock_context
        )
        assert mock_context.state['temp:tool_count'] == 3
    
    def test_last_tool_tracked(self):
        """Last tool name should be tracked in state."""
        mock_context = Mock()
        mock_context.state = {}
        
        # Call with first tool
        mock_tool1 = Mock()
        mock_tool1.name = "read_file"
        before_tool_callback(
            tool=mock_tool1,
            args={'path': '/test/file.txt'},
            tool_context=mock_context
        )
        assert mock_context.state['temp:last_tool'] == 'read_file'
        
        # Call with second tool
        mock_tool2 = Mock()
        mock_tool2.name = "list_directory"
        before_tool_callback(
            tool=mock_tool2,
            args={'path': '/test/'},
            tool_context=mock_context
        )
        assert mock_context.state['temp:last_tool'] == 'list_directory'
    
    def test_state_persists_across_calls(self):
        """State should persist across multiple callback invocations."""
        mock_context = Mock()
        mock_context.state = {
            'user:custom_data': 'preserved',
            'temp:previous_value': 42
        }
        
        mock_tool = Mock()
        mock_tool.name = "read_file"
        
        before_tool_callback(
            tool=mock_tool,
            args={'path': '/test/file.txt'},
            tool_context=mock_context
        )
        
        # Original state should be preserved
        assert mock_context.state['user:custom_data'] == 'preserved'
        assert mock_context.state['temp:previous_value'] == 42
        # New state should be added
        assert 'temp:tool_count' in mock_context.state
        assert 'temp:last_tool' in mock_context.state


class TestApprovalMessageContent:
    """Test the content of approval messages."""
    
    def test_approval_message_includes_operation_name(self):
        """Approval message should include the operation name."""
        mock_tool = Mock()
        mock_tool.name = "write_file"
        
        mock_context = Mock()
        mock_context.state = {}
        
        result = before_tool_callback(
            tool=mock_tool,
            args={'path': '/test/file.txt', 'content': 'test'},
            tool_context=mock_context
        )
        
        assert 'write_file' in result['message']
        assert result['tool_name'] == 'write_file'
    
    def test_approval_message_includes_reason(self):
        """Approval message should include reason for blocking."""
        mock_tool = Mock()
        mock_tool.name = "write_file"
        
        mock_context = Mock()
        mock_context.state = {}
        
        result = before_tool_callback(
            tool=mock_tool,
            args={'path': '/test/file.txt', 'content': 'test'},
            tool_context=mock_context
        )
        
        assert 'Reason:' in result['message']
        assert 'modifies' in result['message'].lower()
    
    def test_approval_message_includes_arguments(self):
        """Approval message should include the arguments passed to the tool."""
        mock_tool = Mock()
        mock_tool.name = "move_file"
        
        mock_context = Mock()
        mock_context.state = {}
        
        args = {'source': '/test/old.txt', 'destination': '/test/new.txt'}
        result = before_tool_callback(
            tool=mock_tool,
            args=args,
            tool_context=mock_context
        )
        
        assert 'Arguments:' in result['message']
        assert 'args' in result
        assert result['args'] == args
    
    def test_approval_message_includes_instructions(self):
        """Approval message should include instructions on how to approve."""
        mock_tool = Mock()
        mock_tool.name = "create_directory"
        
        mock_context = Mock()
        mock_context.state = {}
        
        result = before_tool_callback(
            tool=mock_tool,
            args={'path': '/test/new_dir'},
            tool_context=mock_context
        )
        
        assert 'auto_approve_file_ops' in result['message']
        assert 'BLOCKED' in result['message']


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_args(self):
        """Callback should handle empty args dictionary."""
        mock_tool = Mock()
        mock_tool.name = "list_directory"
        
        mock_context = Mock()
        mock_context.state = {}
        
        # Should not raise exception
        result = before_tool_callback(
            tool=mock_tool,
            args={},
            tool_context=mock_context
        )
        
        assert result is None  # Safe operation
    
    def test_none_state_values(self):
        """Callback should handle None values in state."""
        mock_tool = Mock()
        mock_tool.name = "read_file"
        
        mock_context = Mock()
        mock_context.state = {
            'temp:tool_count': None,
            'user:auto_approve_file_ops': None
        }
        
        # Should handle None gracefully
        result = before_tool_callback(
            tool=mock_tool,
            args={'path': '/test/file.txt'},
            tool_context=mock_context
        )
        
        # Should start count at 1 (None treated as 0)
        assert mock_context.state['temp:tool_count'] == 1
    
    def test_unknown_tool_name_allowed(self):
        """Unknown tool names (not in destructive list) should be allowed."""
        mock_tool = Mock()
        mock_tool.name = "custom_unknown_operation"
        
        mock_context = Mock()
        mock_context.state = {}
        
        result = before_tool_callback(
            tool=mock_tool,
            args={'param': 'value'},
            tool_context=mock_context
        )
        
        # Should allow unknown operations (safe by default)
        assert result is None


class TestIntegrationScenarios:
    """Test realistic integration scenarios."""
    
    def test_workflow_read_then_write(self):
        """Test a workflow that reads a file then writes it."""
        mock_context = Mock()
        mock_context.state = {}
        
        # Step 1: Read file (should be allowed)
        read_tool = Mock()
        read_tool.name = "read_file"
        result1 = before_tool_callback(
            tool=read_tool,
            args={'path': '/test/config.json'},
            tool_context=mock_context
        )
        assert result1 is None
        assert mock_context.state['temp:tool_count'] == 1
        
        # Step 2: Write file (should be blocked without approval)
        write_tool = Mock()
        write_tool.name = "write_file"
        result2 = before_tool_callback(
            tool=write_tool,
            args={'path': '/test/config.json', 'content': 'updated'},
            tool_context=mock_context
        )
        assert result2 is not None
        assert result2['status'] == 'requires_approval'
        assert mock_context.state['temp:tool_count'] == 2
        
        # Step 3: Enable auto-approve
        mock_context.state['user:auto_approve_file_ops'] = True
        
        # Step 4: Write file again (should be allowed now)
        result3 = before_tool_callback(
            tool=write_tool,
            args={'path': '/test/config.json', 'content': 'updated'},
            tool_context=mock_context
        )
        assert result3 is None
        assert mock_context.state['temp:tool_count'] == 3
    
    def test_multiple_destructive_operations_blocked(self):
        """Test that multiple destructive operations are all blocked."""
        mock_context = Mock()
        mock_context.state = {}
        
        destructive_ops = [
            ('write_file', {'path': '/test/file1.txt', 'content': 'test1'}),
            ('write_text_file', {'path': '/test/file2.txt', 'content': 'test2'}),
            ('move_file', {'source': '/test/old.txt', 'dest': '/test/new.txt'}),
            ('create_directory', {'path': '/test/new_dir'}),
        ]
        
        for op_name, args in destructive_ops:
            mock_tool = Mock()
            mock_tool.name = op_name
            
            blocked_result = before_tool_callback(
                tool=mock_tool,
                args=args,
                tool_context=mock_context
            )
            
            # All should be blocked
            assert blocked_result is not None
            assert blocked_result['status'] == 'requires_approval'
            assert blocked_result['tool_name'] == op_name


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
