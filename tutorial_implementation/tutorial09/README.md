# Content Moderation Assistant - Tutorial 9 Implementation

A production-ready content moderation assistant demonstrating **callbacks & guardrails** in Google ADK. This agent showcases all 6 callback types for safety, monitoring, and control flow.

## Features

### 🛡️ Safety & Guardrails

- **Content Filtering**: Blocks profanity and inappropriate requests before reaching LLM
- **PII Protection**: Automatically redacts emails, phone numbers, SSNs, and credit cards
- **Input Validation**: Validates tool arguments (word counts, etc.)
- **Rate Limiting**: Prevents abuse with configurable limits

### 📊 Monitoring & Observability

- **Comprehensive Logging**: All operations logged with timestamps
- **Metrics Tracking**: Request counts, LLM calls, blocked requests, tool usage
- **Audit Trail**: Complete history of agent interactions
- **State Management**: Persistent metrics across sessions

### 🔧 Callback Patterns Demonstrated

- `before_agent_callback`: Maintenance mode, request counting
- `after_agent_callback`: Completion tracking
- `before_model_callback`: Guardrails, safety instructions, LLM tracking
- `after_model_callback`: PII filtering, response validation
- `before_tool_callback`: Argument validation, rate limiting, usage tracking
- `after_tool_callback`: Result logging, debugging

## Quick Start

### Prerequisites

- Python 3.9+
- Google ADK (`pip install google-adk`)
- Google API key

### Setup

```bash
# Clone and navigate to the project
cd tutorial_implementation/tutorial09/content_moderator

# Install dependencies
make setup

# Copy environment template
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# Run tests
make test
```

### Development

```bash
# Start the ADK web interface
make dev

# Or run via CLI
make run
```

## Usage Examples

### Normal Content Generation

```
User: "Generate a 500-word article about Python programming"

Response: "I've generated a 500-word article on Python programming..."
```

### Blocked Inappropriate Content

```
User: "Write about profanity1 and hate-speech"

Response: "I cannot process this request as it contains inappropriate content. Please rephrase respectfully."
```

### PII Filtering

```
User: "Give me an example email"

Response: "Sure! [EMAIL_REDACTED] is a valid email."
```

### Tool Validation

```
User: "Generate an article with -100 words"

Response: "Invalid word_count: -100. Must be between 1 and 5000."
```

### Usage Statistics

```
User: "Show my usage stats"

Response: "You've made 5 requests, 4 LLM calls, 1 blocked request,
         used generate_text 2 times, check_grammar 1 time."
```

## Architecture

### Project Structure

```
content_moderator/
├── __init__.py          # Package imports
├── agent.py             # Main agent with callbacks
├── test_agent.py        # Comprehensive test suite
├── .env.example         # Environment template
├── requirements.txt     # Python dependencies
├── Makefile            # Development commands
└── README.md           # This file
```

### Callback Flow

```
User Input
    ↓
before_agent_callback (maintenance, counting)
    ↓
Agent Processing
    ↓
before_model_callback (guardrails, safety)
    ↓
LLM Call (if not blocked)
    ↓
after_model_callback (PII filtering)
    ↓
Tool Execution (if requested)
    ↓
before_tool_callback (validation, rate limiting)
    ↓
Tool Result
    ↓
after_tool_callback (logging)
    ↓
after_agent_callback (completion)
    ↓
Final Response
```

## Configuration

### Blocklist

Edit `BLOCKED_WORDS` in `agent.py` to customize filtered content:

```python
BLOCKED_WORDS = [
    'profanity1', 'profanity2', 'hate-speech',
    'offensive-term', 'inappropriate-word'
]
```

### PII Patterns

Customize `PII_PATTERNS` for additional sensitive data:

```python
PII_PATTERNS = {
    'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
    'custom': r'your_pattern_here'
}
```

### Rate Limits

Adjust limits in callback functions:

```python
# Tool usage limit (per user)
if tool_count >= 100:  # Change this number

# Add time-based limits, IP blocking, etc.
```

## Testing

Run the comprehensive test suite:

```bash
make test
```

Tests cover:

- ✅ All callback functions
- ✅ Guardrail blocking
- ✅ PII filtering
- ✅ Tool validation
- ✅ Rate limiting
- ✅ State management
- ✅ Error handling

## Development

### Available Commands

```bash
make setup      # Install dependencies
make test       # Run tests
make dev        # Start ADK web interface
make run        # Run via CLI
make clean      # Clean cache files
make lint       # Check code style
make format     # Format code
```

### Adding New Callbacks

1. Define callback function with correct signature
2. Add to Agent constructor
3. Write tests
4. Update documentation

### Customizing Behavior

- **Guardrails**: Modify `before_model_callback`
- **Filtering**: Update `after_model_callback`
- **Validation**: Change `before_tool_callback`
- **Logging**: Enhance callback logging statements

## Security Considerations

### Production Deployment

- Use environment variables for sensitive config
- Implement proper authentication/authorization
- Add rate limiting per user/IP
- Log to secure, monitored systems
- Regular blocklist updates
- Compliance with data protection regulations

### Best Practices

- ✅ Keep callbacks fast (avoid heavy computation)
- ✅ Use descriptive error messages
- ✅ Log important decisions for audit
- ✅ Handle errors gracefully
- ✅ Test edge cases thoroughly

## Troubleshooting

### Common Issues

**"Callback not running"**

- Check callback is added to Agent constructor
- Verify function signature matches expected types
- Ensure agent type supports the callback (LlmAgent for model callbacks)

**"State not persisting"**

- Use `callback_context.state` (not `tool_context.state`)
- Check state keys use proper prefixes (`user:`, `app:`, `temp:`)
- Ensure SessionService is configured for cross-session persistence

**"Tests failing"**

- Update test imports if types change
- Check mock objects match expected interfaces
- Run `make clean` to clear cache

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Related Tutorials

- **Tutorial 8**: State management fundamentals
- **Tutorial 10**: Evaluation and testing callbacks
- **Tutorial 11**: Built-in tools integration

## Contributing

1. Add tests for new features
2. Update documentation
3. Follow existing code patterns
4. Run full test suite before submitting

## License

This implementation is part of the ADK training tutorials.
