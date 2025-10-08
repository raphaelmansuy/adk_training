# Tutorial 10: Evaluation & Testing - Quality Assurance for Agents

## Overview

Learn how to systematically test and evaluate AI agents using ADK's evaluation framework. This tutorial demonstrates creating test files, running evaluations via pytest/CLI/UI, and measuring agent quality with trajectory metrics.

**What You'll Build**: A complete testing system for a customer support agent:
- **Test files** (`.test.json`) for unit testing
- **Evalsets** (`.evalset.json`) for integration testing
- **Pytest integration** for CI/CD pipelines
- **Trajectory validation** (tool call sequences)
- **Response quality metrics** (ROUGE scores)
- **Web UI evaluation** workflow

**Why It Matters**: Production agents need systematic testing. The evaluation framework enables automated quality assurance, regression detection, and confidence in agent behavior.

---

## Prerequisites

- Python 3.9+
- `google-adk` and `pytest` installed
- Google API key
- Completed Tutorials 01-02 (basics)
- Understanding of test-driven development (helpful)

---

## Core Concepts

### Why Evaluate Agents?

Traditional software:
```python
assert calculate(2 + 2) == 4  # Deterministic
```

AI Agents:
```python
# Non-deterministic! Could return:
# "The answer is 4"
# "Four"
# "2 + 2 equals 4"
# Need qualitative evaluation
```

**Challenge**: LLM responses are probabilistic, so we need to evaluate:
1. **Trajectory**: Did the agent call the right tools in the right order?
2. **Response Quality**: Is the final answer correct and well-formed?

### What to Evaluate

**1. Trajectory (Tool Usage)**:
- Did the agent call the expected tools?
- In the correct order?
- With valid arguments?

**Metrics**:
- Exact match (perfect trajectory)
- In-order match (correct tools, correct order, extra OK)
- Any-order match (correct tools, any order, extra OK)
- Precision (% of calls that were correct)
- Recall (% of expected calls that were made)

**2. Response Quality (Final Output)**:
- Is the answer accurate?
- Is it well-formatted?
- Does it match expected content?

**Metrics**:
- tool_trajectory_avg_score (0-1): Average tool call correctness
- response_match_score (0-1): ROUGE similarity to expected response

### Evaluation Approaches

**Approach 1: Test Files** (Unit Testing):
- Single `.test.json` file = single session
- Simple interactions
- Fast execution
- Use during active development
- Run with pytest or adk eval

**Approach 2: Evalsets** (Integration Testing):
- Single `.evalset.json` file = multiple sessions
- Complex multi-turn conversations
- Slower execution
- Use for comprehensive testing
- Run with adk eval or Web UI

---

## Use Case: Customer Support Agent Testing

**Scenario**: Build a support agent that:
- Searches knowledge base for answers
- Creates tickets for issues
- Checks ticket status
- Needs systematic testing to ensure quality

**What to Test**:
1. Knowledge base search works correctly
2. Ticket creation uses proper fields
3. Status checks return accurate info
4. Multi-turn conversations maintain context
5. Error handling is appropriate

---

## Implementation

### Project Structure

```
support_agent/
├── __init__.py                  # Imports agent
├── agent.py                     # Agent definition
├── .env                         # API key
└── tests/
    ├── simple.test.json         # Unit test (single session)
    ├── complex.evalset.json     # Integration test (multiple sessions)
    ├── test_config.json         # Evaluation criteria
    └── test_agent.py            # Pytest test file
```

### Complete Code

**support_agent/__init__.py**:
```python
from .agent import root_agent

__all__ = ['root_agent']
```

**support_agent/agent.py**:
```python
"""
Customer Support Agent - For Evaluation Testing Demonstration

This agent demonstrates testable patterns:
- Clear tool usage (easy to validate trajectory)
- Structured responses (easy to compare)
- Deterministic behavior (where possible)
"""

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from typing import Dict, Any, List

# ============================================================================
# TOOLS
# ============================================================================

def search_knowledge_base(
    query: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Search knowledge base for relevant articles.
    
    Args:
        query: Search query
    """
    # Simulated knowledge base
    kb = {
        'password reset': 'To reset your password, go to Settings > Security > Reset Password.',
        'billing': 'For billing questions, contact billing@example.com or call 1-800-555-0123.',
        'technical support': 'Technical support is available 24/7 via chat or phone.'
    }
    
    # Simple keyword search
    results = []
    for key, article in kb.items():
        if any(word in key for word in query.lower().split()):
            results.append({'title': key.title(), 'content': article})
    
    return {
        'status': 'success',
        'query': query,
        'results_count': len(results),
        'results': results
    }


def create_ticket(
    issue: str,
    priority: str,
    customer_email: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Create a support ticket.
    
    Args:
        issue: Issue description
        priority: low, medium, or high
        customer_email: Customer's email
    """
    # Validate priority
    if priority not in ['low', 'medium', 'high']:
        return {
            'status': 'error',
            'message': f'Invalid priority: {priority}. Must be low, medium, or high.'
        }
    
    # Generate ticket ID
    ticket_id = f'TICK-{hash(issue) % 10000:04d}'
    
    return {
        'status': 'success',
        'ticket_id': ticket_id,
        'issue': issue,
        'priority': priority,
        'customer_email': customer_email,
        'message': f'Created ticket {ticket_id} with {priority} priority'
    }


def check_ticket_status(
    ticket_id: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Check status of existing ticket.
    
    Args:
        ticket_id: Ticket ID (e.g., TICK-1234)
    """
    # Simulated ticket database
    tickets = {
        'TICK-1234': {'status': 'open', 'priority': 'high', 'assigned_to': 'Agent Smith'},
        'TICK-5678': {'status': 'resolved', 'priority': 'low', 'resolved_at': '2024-01-15'}
    }
    
    if ticket_id not in tickets:
        return {
            'status': 'error',
            'message': f'Ticket {ticket_id} not found'
        }
    
    ticket = tickets[ticket_id]
    return {
        'status': 'success',
        'ticket_id': ticket_id,
        **ticket
    }


# ============================================================================
# AGENT DEFINITION
# ============================================================================

root_agent = Agent(
    name="support_agent",
    model="gemini-2.0-flash",
    
    description="""
    Customer support agent that can search knowledge base, create tickets,
    and check ticket status. Designed for systematic testing.
    """,
    
    instruction="""
    You are a helpful customer support agent.
    
    CAPABILITIES:
    - Search knowledge base for answers to common questions
    - Create support tickets for issues
    - Check status of existing tickets
    
    WORKFLOW:
    1. For questions, search the knowledge base FIRST
    2. If KB has answer, provide it directly
    3. If KB doesn't have answer or issue needs follow-up, create a ticket
    4. For ticket status inquiries, use check_ticket_status
    
    RESPONSE FORMAT:
    - Be concise and professional
    - Always confirm actions (e.g., "I've created ticket TICK-1234")
    - Provide clear next steps
    
    IMPORTANT:
    - Call search_knowledge_base before creating tickets
    - Use correct priority levels: low, medium, high
    - Always include customer email when creating tickets
    """,
    
    tools=[
        search_knowledge_base,
        create_ticket,
        check_ticket_status
    ],
    
    output_key="support_response"
)
```

**support_agent/.env**:
```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_api_key_here
```

---

## Creating Test Files

### Test File 1: Simple Knowledge Base Search

**support_agent/tests/simple.test.json**:

```json
{
  "eval_set_id": "support_agent_simple_test",
  "name": "Simple Knowledge Base Search",
  "description": "Test that agent searches KB before creating tickets",
  "eval_cases": [
    {
      "eval_id": "test_kb_search",
      "conversation": [
        {
          "invocation_id": "inv-001",
          "user_content": {
            "parts": [
              {
                "text": "How do I reset my password?"
              }
            ],
            "role": "user"
          },
          "final_response": {
            "parts": [
              {
                "text": "To reset your password, go to Settings > Security > Reset Password."
              }
            ],
            "role": "model"
          },
          "intermediate_data": {
            "tool_uses": [
              {
                "name": "search_knowledge_base",
                "args": {
                  "query": "password reset"
                }
              }
            ],
            "intermediate_responses": []
          }
        }
      ],
      "session_input": {
        "app_name": "support_agent_app",
        "user_id": "test_user",
        "state": {}
      }
    }
  ]
}
```

**What This Tests**:
- Agent calls `search_knowledge_base` (trajectory)
- With query "password reset" (argument validation)
- Returns correct KB article (response quality)
- **Expected**: tool_trajectory_avg_score = 1.0, response_match_score ≥ 0.8

### Test File 2: Ticket Creation

**support_agent/tests/ticket_creation.test.json**:

```json
{
  "eval_set_id": "ticket_creation_test",
  "name": "Ticket Creation Flow",
  "description": "Test that agent creates tickets with correct fields",
  "eval_cases": [
    {
      "eval_id": "test_create_ticket",
      "conversation": [
        {
          "invocation_id": "inv-002",
          "user_content": {
            "parts": [
              {
                "text": "I have a critical bug in the app. My email is user@example.com"
              }
            ],
            "role": "user"
          },
          "final_response": {
            "parts": [
              {
                "text": "I've created a high priority ticket for your bug report. Your ticket ID is TICK-"
              }
            ],
            "role": "model"
          },
          "intermediate_data": {
            "tool_uses": [
              {
                "name": "search_knowledge_base",
                "args": {
                  "query": "bug"
                }
              },
              {
                "name": "create_ticket",
                "args": {
                  "issue": "critical bug in the app",
                  "priority": "high",
                  "customer_email": "user@example.com"
                }
              }
            ],
            "intermediate_responses": []
          }
        }
      ],
      "session_input": {
        "app_name": "support_agent_app",
        "user_id": "test_user",
        "state": {}
      }
    }
  ]
}
```

**What This Tests**:
- Agent searches KB first (good practice)
- Then creates ticket (2-step trajectory)
- Uses correct priority ("high" for critical bug)
- Includes customer email
- **Expected**: tool_trajectory_avg_score = 1.0 (exact match)

### Evalset: Multi-Turn Conversation

**support_agent/tests/complex.evalset.json**:

```json
{
  "eval_set_id": "complex_multi_turn",
  "name": "Multi-Turn Support Conversation",
  "description": "Test multi-turn conversation with ticket creation and status check",
  "eval_cases": [
    {
      "eval_id": "session_multi_turn",
      "conversation": [
        {
          "invocation_id": "inv-003-turn1",
          "user_content": {
            "parts": [{"text": "How do I contact billing?"}],
            "role": "user"
          },
          "final_response": {
            "parts": [{"text": "For billing questions, contact billing@example.com or call 1-800-555-0123."}],
            "role": "model"
          },
          "intermediate_data": {
            "tool_uses": [
              {"name": "search_knowledge_base", "args": {"query": "billing"}}
            ],
            "intermediate_responses": []
          }
        },
        {
          "invocation_id": "inv-003-turn2",
          "user_content": {
            "parts": [{"text": "Actually, I need to report a billing error. My email is alice@example.com"}],
            "role": "user"
          },
          "final_response": {
            "parts": [{"text": "I've created a ticket for your billing error"}],
            "role": "model"
          },
          "intermediate_data": {
            "tool_uses": [
              {
                "name": "create_ticket",
                "args": {
                  "issue": "billing error",
                  "priority": "medium",
                  "customer_email": "alice@example.com"
                }
              }
            ],
            "intermediate_responses": []
          }
        }
      ],
      "session_input": {
        "app_name": "support_agent_app",
        "user_id": "test_user_alice",
        "state": {}
      }
    }
  ]
}
```

**What This Tests**:
- Multi-turn conversation (context maintenance)
- First turn: Knowledge base search
- Second turn: Ticket creation
- **Expected**: Both turns pass trajectory and response checks

### Evaluation Criteria

**support_agent/tests/test_config.json**:

```json
{
  "criteria": {
    "tool_trajectory_avg_score": 1.0,
    "response_match_score": 0.7
  }
}
```

**What This Means**:
- `tool_trajectory_avg_score: 1.0` → Perfect tool call match required
- `response_match_score: 0.7` → 70% ROUGE similarity to expected response

---

## Running Evaluations

### Method 1: Pytest (Automated Testing)

**support_agent/tests/test_agent.py**:

```python
"""
Pytest tests for support agent.

Run with: pytest tests/test_agent.py
"""

from google.adk.evaluation.agent_evaluator import AgentEvaluator
import pytest


@pytest.mark.asyncio
async def test_simple_kb_search():
    """Test simple knowledge base search."""
    await AgentEvaluator.evaluate(
        agent_module="support_agent",
        eval_dataset_file_path_or_dir="tests/simple.test.json"
    )


@pytest.mark.asyncio
async def test_ticket_creation():
    """Test ticket creation flow."""
    await AgentEvaluator.evaluate(
        agent_module="support_agent",
        eval_dataset_file_path_or_dir="tests/ticket_creation.test.json"
    )


@pytest.mark.asyncio
async def test_multi_turn_conversation():
    """Test complex multi-turn conversation."""
    await AgentEvaluator.evaluate(
        agent_module="support_agent",
        eval_dataset_file_path_or_dir="tests/complex.evalset.json",
        config_file_path="tests/test_config.json"
    )


@pytest.mark.asyncio
async def test_all_in_directory():
    """Run all tests in tests/ directory."""
    await AgentEvaluator.evaluate(
        agent_module="support_agent",
        eval_dataset_file_path_or_dir="tests/"
    )
```

**Run Tests**:

```bash
# Install pytest if needed
pip install pytest pytest-asyncio

# Run all tests
pytest tests/test_agent.py -v

# Run specific test
pytest tests/test_agent.py::test_simple_kb_search -v

# Run with detailed output
pytest tests/test_agent.py -v -s
```

**Expected Output**:

```
tests/test_agent.py::test_simple_kb_search PASSED [25%]
tests/test_agent.py::test_ticket_creation PASSED [50%]
tests/test_agent.py::test_multi_turn_conversation PASSED [75%]
tests/test_agent.py::test_all_in_directory PASSED [100%]

=============== 4 passed in 12.34s ===============
```

### Method 2: CLI (Command Line)

```bash
# Run single test file
adk eval support_agent tests/simple.test.json

# Run with config
adk eval support_agent tests/complex.evalset.json \
    --config_file_path=tests/test_config.json

# Run specific eval from evalset
adk eval support_agent tests/complex.evalset.json:session_multi_turn

# Run with detailed results
adk eval support_agent tests/ --print_detailed_results
```

**CLI Output Example**:

```
Running evaluations for: support_agent
Eval Set: support_agent_simple_test
  ✓ test_kb_search PASSED
    - tool_trajectory_avg_score: 1.0 (threshold: 1.0)
    - response_match_score: 0.85 (threshold: 0.7)

Total: 1/1 passed (100%)
```

### Method 3: Web UI (Interactive)

```bash
adk web support_agent
```

**Workflow**:

1. **Create Session**:
   - Chat with agent: "How do I reset my password?"
   - Agent responds with KB article

2. **Save as Eval Case**:
   - Click "Eval" tab (right side)
   - Click "Create new eval set" or select existing
   - Click "Add current session"
   - Name it: "test_password_reset"

3. **Edit Eval Case**:
   - Click eval case ID to view
   - Click pencil icon to edit
   - Modify expected tool calls:
     ```json
     "tool_uses": [
       {
         "name": "search_knowledge_base",
         "args": {"query": "password reset"}
       }
     ]
     ```
   - Modify expected response
   - Save changes

4. **Run Evaluation**:
   - Select eval case(s)
   - Click "Run Evaluation"
   - Set thresholds:
     - Tool trajectory: 1.0
     - Response match: 0.7
   - Click "Start"

5. **Analyze Results**:
   - View Pass/Fail for each eval
   - Click "Fail" to see:
     - Expected vs Actual tool calls (side-by-side)
     - Expected vs Actual response
     - Scores that caused failure
   - Use Trace tab for detailed execution flow

**Web UI Benefits**:
- Visual comparison of expected vs actual
- Easy to capture real sessions as tests
- Interactive editing of test cases
- Detailed trace view for debugging

---

## Understanding Evaluation Metrics

### Tool Trajectory Score

**How It Works**:
```python
expected_tools = ["search_knowledge_base", "create_ticket"]
actual_tools = ["search_knowledge_base", "create_ticket"]

# Each match = 1.0, each mismatch = 0.0
# Score = average of all comparisons
score = 2/2 = 1.0  # Perfect!
```

**Examples**:

**Example 1: Perfect Match**:
```
Expected: [search_knowledge_base, create_ticket]
Actual:   [search_knowledge_base, create_ticket]
Score: 1.0 (2/2 matches)
```

**Example 2: Partial Match**:
```
Expected: [search_knowledge_base, create_ticket]
Actual:   [create_ticket]
Score: 0.5 (1/2 matches)
```

**Example 3: Extra Calls OK (In-Order Match)**:
```
Expected: [search_knowledge_base, create_ticket]
Actual:   [search_knowledge_base, check_ticket_status, create_ticket]
Score: 1.0 with any-order metric, 0.67 with exact match
```

### Response Match Score (ROUGE)

**What is ROUGE?**
Recall-Oriented Understudy for Gisting Evaluation - measures n-gram overlap between expected and actual text.

**Example**:

```
Expected: "To reset your password, go to Settings > Security > Reset Password."
Actual:   "You can reset your password in Settings under Security, then Reset Password."

ROUGE-1 (unigrams): ~0.7 (70% word overlap)
ROUGE-2 (bigrams): ~0.5 (50% phrase overlap)
```

**Score Interpretation**:
- 1.0 = Perfect match (identical)
- 0.8-0.9 = Very similar (minor rewording)
- 0.6-0.7 = Similar (same info, different wording)
- 0.4-0.5 = Somewhat similar
- < 0.4 = Different content

**Threshold Selection**:
- 1.0 = Exact wording required (too strict!)
- 0.8 = High similarity (good for specific responses)
- 0.7 = Moderate similarity (good default)
- 0.5 = Loose similarity (too lenient)

---

## How It Works: Evaluation Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Load Test File (simple.test.json)                       │
│    - Parse eval_cases                                       │
│    - Load session_input (app_name, user_id, initial state) │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. For Each Conversation Turn:                             │
│    a. Create session with initial state                     │
│    b. Send user_content to agent                            │
│    c. Agent runs (calls tools, generates response)          │
│    d. Capture actual behavior:                              │
│       - Tool calls (name, args)                             │
│       - Final response text                                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Compare Expected vs Actual:                             │
│    ┌───────────────────────────────────────────────────┐   │
│    │ Trajectory Comparison                             │   │
│    │ Expected: [search_kb, create_ticket]             │   │
│    │ Actual:   [search_kb, create_ticket]             │   │
│    │ Result: 2/2 matches → score = 1.0                │   │
│    └───────────────────────────────────────────────────┘   │
│    ┌───────────────────────────────────────────────────┐   │
│    │ Response Comparison (ROUGE)                       │   │
│    │ Expected: "To reset your password..."            │   │
│    │ Actual:   "You can reset your password..."       │   │
│    │ ROUGE score: 0.75                                 │   │
│    └───────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Apply Thresholds (from test_config.json):               │
│    - tool_trajectory_avg_score ≥ 1.0? ✓ PASS               │
│    - response_match_score ≥ 0.7? ✓ PASS (0.75)             │
│                                                             │
│    Final Result: PASS ✓                                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Report Results:                                          │
│    - Console output (pytest/CLI)                            │
│    - Web UI visualization                                   │
│    - Test framework integration (CI/CD)                     │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Takeaways

1. **Two Dimensions of Quality**:
   - **Trajectory**: Did agent take right steps? (tool calls)
   - **Response**: Is the answer good? (text quality)

2. **Two Testing Approaches**:
   - **Test files**: Unit tests, single sessions, fast
   - **Evalsets**: Integration tests, multiple sessions, comprehensive

3. **Three Execution Methods**:
   - **pytest**: Automated, CI/CD friendly
   - **CLI**: Quick manual testing
   - **Web UI**: Interactive, visual debugging

4. **Flexible Thresholds**:
   - Strict (1.0): Perfect match required
   - Moderate (0.7-0.8): Good balance
   - Loose (0.5): Allow variation

5. **Evaluation is Iterative**:
   - Capture real sessions as tests
   - Run evaluations frequently
   - Adjust thresholds based on needs
   - Refine agent based on failures

---

## Best Practices

### Test Creation

**DO**:
- ✅ Test common user flows (happy paths)
- ✅ Test edge cases (error handling)
- ✅ Test multi-turn conversations
- ✅ Use realistic user inputs
- ✅ Include varied phrasings

**DON'T**:
- ❌ Test only perfect inputs
- ❌ Use overly specific expected responses
- ❌ Forget to test error cases
- ❌ Create tests that are too brittle

### Threshold Selection

**Tool Trajectory**:
- 1.0: Exact match (strict, good for critical flows)
- 0.8-0.9: Allow some flexibility
- < 0.7: Too lenient (agent might skip steps)

**Response Match**:
- 0.9-1.0: Very strict (rarely needed)
- 0.7-0.8: Good default (similar content)
- 0.5-0.6: Loose (useful for creative responses)

### CI/CD Integration

```yaml
# GitHub Actions example
name: Agent Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: pip install google-adk pytest
      - name: Run evaluations
        env:
          GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
        run: pytest tests/test_agent.py -v
```

### Debugging Failed Tests

**Step 1: Reproduce in Web UI**:
```bash
adk web support_agent
# Type the exact user input from failed test
```

**Step 2: Use Trace Tab**:
- See all tool calls (actual trajectory)
- See LLM requests/responses
- Identify where behavior diverged

**Step 3: Check Logs**:
```bash
pytest tests/test_agent.py -v -s  # Show all output
```

**Step 4: Adjust Test or Agent**:
- If agent is wrong → Fix agent logic
- If test is wrong → Update test file

---

## Common Issues & Troubleshooting

### Issue 1: Tool Trajectory Mismatch

**Problem**: Expected `[search_kb, create_ticket]` but got `[create_ticket]`

**Solutions**:
1. Check agent instruction emphasizes search first
2. Add explicit instruction: "Always search KB before creating tickets"
3. Review LLM request in Trace tab (was instruction clear?)
4. Lower threshold if agent's approach is valid but different

### Issue 2: Response Score Too Low

**Problem**: Response is correct but scores 0.5 (below 0.7 threshold)

**Solutions**:
1. Update expected response to match agent's style
2. Lower threshold to 0.5-0.6 if content is correct
3. Check if response includes extra info (might need to strip)
4. Consider if exact wording matters (probably doesn't)

### Issue 3: Evaluation Hangs/Times Out

**Problem**: Evaluation runs for minutes without completing

**Solutions**:
1. Check LLM API key is valid
2. Verify network connectivity
3. Test with single simple eval first
4. Check for infinite loops in agent logic

### Issue 4: Can't Load Test File

**Problem**: `FileNotFoundError: simple.test.json`

**Solutions**:
1. Verify path is correct (relative to agent module)
2. Check file exists: `ls tests/simple.test.json`
3. Ensure JSON is valid (use JSON validator)
4. Check file permissions

---

## Real-World Applications

### 1. Customer Support Agent

**Test Scenarios**:
- Common questions (KB search)
- Ticket creation (various priorities)
- Status inquiries (existing tickets)
- Multi-turn troubleshooting
- Error handling (invalid inputs)

**Metrics**:
- 100% tool trajectory match (critical for compliance)
- 70% response match (allow natural language variation)

### 2. E-commerce Shopping Assistant

**Test Scenarios**:
- Product search (various queries)
- Filtering (price, category, brand)
- Cart operations (add, remove, update)
- Checkout flow (multi-step)
- Order tracking

**Metrics**:
- 90% trajectory match (allow some flexibility)
- 60% response match (product descriptions vary)

### 3. Healthcare Symptom Checker

**Test Scenarios**:
- Symptom assessment (decision trees)
- Emergency detection (must be perfect)
- Appointment scheduling
- Prescription refills
- Medical history queries

**Metrics**:
- 100% trajectory for emergency paths
- 90% trajectory for routine flows
- 80% response match (medical accuracy critical)

### 4. Financial Advisor

**Test Scenarios**:
- Portfolio analysis
- Risk assessment
- Investment recommendations
- Compliance checks
- Transaction execution

**Metrics**:
- 100% trajectory (regulatory compliance)
- 85% response match (specific financial data)

---

## Next Steps

1. **Production Monitoring**: Track live agent performance
2. **Continuous Testing**: Run evals in CI/CD pipelines
3. **A/B Testing**: Compare agent versions with same eval sets
4. **Human Evaluation**: Combine automated metrics with human review

**Exercises**:
1. Add test for invalid priority in ticket creation
2. Create evalset with 5 different conversation flows
3. Integrate pytest tests into GitHub Actions
4. Build dashboard to track eval scores over time

---

## Further Reading

- [Evaluation Documentation](https://google.github.io/adk-docs/evaluate/)
- [EvalSet Schema](https://github.com/google/adk-python/blob/main/src/google/adk/evaluation/eval_set.py)
- [EvalCase Schema](https://github.com/google/adk-python/blob/main/src/google/adk/evaluation/eval_case.py)
- [Pytest Documentation](https://docs.pytest.org/)
- [ROUGE Metric](https://en.wikipedia.org/wiki/ROUGE_(metric))

---

**Congratulations!** You now understand how to systematically test and evaluate AI agents. This enables confidence in agent quality, automated regression detection, and continuous improvement.

---

## Complete Tutorial Series

You've now completed the entire ADK tutorial series:

1. ✅ **Hello World** - Basic agents
2. ✅ **Function Tools** - Custom Python tools
3. ⏳ **OpenAPI Tools** - REST API integration
4. ✅ **Sequential Workflows** - Ordered pipelines
5. ✅ **Parallel Processing** - Concurrent execution
6. ✅ **Multi-Agent Systems** - Agent coordination
7. ✅ **Loop Agents** - Iterative refinement
8. ✅ **State & Memory** - Persistent context
9. ✅ **Callbacks & Guardrails** - Control flow
10. ✅ **Evaluation & Testing** - Quality assurance

**You're now ready to build production-ready AI agents with Google ADK!** 🎉
