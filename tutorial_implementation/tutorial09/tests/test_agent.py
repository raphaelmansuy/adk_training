import pytest
from unittest.mock import Mock
from content_moderator.agent import (
    root_agent,
    generate_text,
    check_grammar,
    get_usage_stats,
    before_agent_callback,
    after_agent_callback,
    before_model_callback,
    after_model_callback,
    before_tool_callback,
    after_tool_callback
)
from google.genai import types
from google.adk.models.llm_response import LlmResponse

class MockCallbackContext:
    def __init__(self):
        self.invocation_id = 'test_invocation_123'
        self.state = {}


def test_before_agent_blocks_maintenance():
    ctx = MockCallbackContext()
    ctx.state['app:maintenance_mode'] = True
    result = before_agent_callback(ctx)
    assert result is not None
    assert "maintenance" in result.parts[0].text.lower()


def test_before_agent_increments_request_count():
    ctx = MockCallbackContext()
    ctx.state['user:request_count'] = 2
    result = before_agent_callback(ctx)
    assert result is None
    assert ctx.state['user:request_count'] == 3


def test_before_model_blocks_profanity():
    ctx = MockCallbackContext()
    req = types._GenerateContentParameters(
        contents=[types.Content(parts=[types.Part(text="This contains profanity1")], role="user")]
    )
    result = before_model_callback(ctx, req)
    assert result is not None
    assert "inappropriate content" in result.candidates[0].content.parts[0].text.lower()
    assert ctx.state['user:blocked_requests'] == 1


def test_before_model_adds_safety_instruction():
    ctx = MockCallbackContext()
    req = types._GenerateContentParameters(
        contents=[types.Content(parts=[types.Part(text="Safe text")], role="user")],
        config=types.GenerateContentConfig(system_instruction="Base instruction.")
    )
    result = before_model_callback(ctx, req)
    assert result is None
    assert "IMPORTANT" in req.config.system_instruction
    assert ctx.state['user:llm_calls'] == 1


def test_after_model_filters_pii():
    ctx = MockCallbackContext()
    content = types.Content(
        parts=[types.Part(text="Contact me at john.doe@example.com")], 
        role="model"
    )
    resp = LlmResponse(content=content)
    result = after_model_callback(ctx, resp)
    assert result is not None
    assert "[EMAIL_REDACTED]" in result.content.parts[0].text


def test_before_tool_validates_word_count():
    ctx = MockCallbackContext()
    args = {'topic': 'Test', 'word_count': -5}
    result = before_tool_callback(ctx, 'generate_text', args)
    assert result['status'] == 'error'
    assert "invalid word_count" in result['message'].lower()


def test_before_tool_rate_limits():
    ctx = MockCallbackContext()
    ctx.state['user:tool_generate_text_count'] = 100
    args = {'topic': 'Test', 'word_count': 10}
    result = before_tool_callback(ctx, 'generate_text', args)
    assert result['status'] == 'error'
    assert "rate limit" in result['message'].lower()


def test_after_tool_logs_result():
    ctx = MockCallbackContext()
    tool_response = {'status': 'success'}
    result = after_tool_callback(ctx, 'generate_text', tool_response)
    assert result is None
    assert 'success' in ctx.state['temp:last_tool_result']


def test_generate_text_tool():
    mock_context = Mock()
    mock_context.state = {}
    result = generate_text("Python", 100, mock_context)
    assert result['status'] == 'success'
    assert result['word_count'] == 100
    assert "Python" in result['message']


def test_check_grammar_tool():
    mock_context = Mock()
    mock_context.state = {}
    result = check_grammar("This is a test sentence with some errors.", mock_context)
    assert result['status'] == 'success'
    assert 'issues_found' in result


def test_get_usage_stats_tool():
    mock_context = Mock()
    mock_context.state = {
        'user:request_count': 5,
        'user:llm_calls': 3,
        'user:blocked_requests': 1,
        'user:tool_generate_text_count': 2,
        'user:tool_check_grammar_count': 1
    }
    result = get_usage_stats(mock_context)
    assert result['status'] == 'success'
    assert result['request_count'] == 5
    assert result['llm_calls'] == 3
    assert result['blocked_requests'] == 1
    assert result['tool_generate_text_count'] == 2
    assert result['tool_check_grammar_count'] == 1
