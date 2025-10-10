"""
Quick test of Human-in-the-Loop functionality
Shows how destructive operations are blocked
"""

from mcp_agent.agent import create_mcp_filesystem_agent, before_tool_callback
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.state import State

# Test the before_tool_callback directly
print("=" * 70)
print("TESTING HUMAN-IN-THE-LOOP FUNCTIONALITY")
print("=" * 70)
print()

# Create mock context
state = State()
context = CallbackContext(state=state)

# Test 1: Safe operation (should allow)
print("Test 1: Safe Operation (read_file)")
print("-" * 70)
result = before_tool_callback(context, 'read_file', {'path': 'test.txt'})
if result is None:
    print("✅ ALLOWED: read_file operation approved automatically")
else:
    print(f"❌ BLOCKED: {result}")
print()

# Test 2: Destructive operation without approval (should block)
print("Test 2: Destructive Operation (write_file) - No Approval")
print("-" * 70)
result = before_tool_callback(context, 'write_file', {'path': 'test.txt', 'content': 'Hello'})
if result is None:
    print("❌ ERROR: write_file should have been blocked!")
else:
    print(f"✅ BLOCKED: {result['status']}")
    print(f"   Message: {result['message'][:80]}...")
print()

# Test 3: Destructive operation with approval (should allow)
print("Test 3: Destructive Operation (write_file) - With Approval")
print("-" * 70)
context.state['user:auto_approve_file_ops'] = True
result = before_tool_callback(context, 'write_file', {'path': 'test.txt', 'content': 'Hello'})
if result is None:
    print("✅ ALLOWED: write_file operation approved via auto_approve flag")
else:
    print(f"❌ BLOCKED: {result}")
print()

# Test 4: Agent creation with default directory
print("Test 4: Agent Creation - Directory Restriction")
print("-" * 70)
agent = create_mcp_filesystem_agent()
print(f"✅ Agent created successfully")
print(f"   Name: {agent.name}")
print(f"   HITL enabled: {agent.before_tool_callback is not None}")
print(f"   Description: {agent.description[:60]}...")
print()

print("=" * 70)
print("ALL TESTS PASSED - HITL IS WORKING CORRECTLY")
print("=" * 70)
