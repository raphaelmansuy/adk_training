# Tool Use Quality Evaluation - TIL Implementation

Quick-start implementation for **Rubric Based Tool Use Quality Metric** from ADK 1.16.

## What is Tool Use Quality?

Tool Use Quality evaluates **HOW** agents use their tools, separate from **WHAT** they accomplish.

### Example

Your agent might:
- ✅ Get the RIGHT ANSWER (final response quality is high)
- ❌ Use tools OUT OF ORDER (tool use quality is low)

**Tool Use Quality catches this!**

## This Implementation

Demonstrates a **data analysis workflow** with proper tool sequencing:

```
Good Sequence:
Analyze Data → Extract Features → Validate Quality → Apply Model
(Each step depends on previous output)

Bad Sequence:
Apply Model → Analyze Data → Extract Features
(Wrong order, prerequisites not met)
```

## Quick Start

### Setup

```bash
make setup
export GOOGLE_API_KEY=your_key_here
make test
```

### Run Real Evaluation ⭐

```bash
make evaluate
```

This **actually calls the ADK evaluation framework** to evaluate tool sequencing:

```
📝 TEST CASES
- good_sequence_complete_pipeline: All 4 tools in correct order
- bad_sequence_skipped_validation: Missing validation step
- good_sequence_proper_analysis: Partial but correct pipeline

🔍 RUNNING EVALUATION
- Creates 3 test cases with expected tool sequences
- LLM judge evaluates against 4 custom rubrics
- Reports scores vs threshold (0.7 required)
- Shows expected vs actual tool calls (side-by-side)

RESULTS
- Score: 0.25 (below 0.7 threshold = FAILED)
- Reason: Test agent didn't match expected tool sequences
```

**What `make evaluate` does:**

```python
# 1. Creates evaluation config with rubric-based tool use quality metric
config = {
    "criteria": {
        "rubric_based_tool_use_quality_v1": {
            "threshold": 0.7,
            "judge_model": "gemini-2.5-flash",
            "rubrics": [
                "proper_tool_order",      # analyze before extract
                "complete_pipeline",      # all 4 tools included
                "validation_before_model", # quality check before apply
                "no_tool_failures"        # all calls succeed
            ]
        }
    }
}

# 2. Creates test cases with good/bad tool sequences
evalset = {
    "eval_cases": [
        {
            "eval_id": "good_sequence",
            "tool_uses": [
                {"name": "analyze_data", ...},
                {"name": "extract_features", ...},
                {"name": "validate_quality", ...},
                {"name": "apply_model", ...}
            ]
        },
        {
            "eval_id": "bad_sequence",
            "tool_uses": [
                {"name": "extract_features", ...},
                {"name": "apply_model", ...}
                # Missing: analyze_data and validate_quality!
            ]
        }
    ]
}

# 3. Runs evaluation
results = await AgentEvaluator.evaluate(
    agent_module="tool_use_evaluator",
    eval_dataset_file_path_or_dir="tool_use_quality.evalset.json",
)

# 4. LLM judge evaluates tool sequences
# - For each test case, judge checks against 4 rubrics
# - Produces per-rubric scores (1.0 = pass, 0.0 = fail)
# - Calculates overall score (average of rubric scores)
# - Returns detailed comparison of expected vs actual calls

# 5. Reports results
# Expected threshold: 0.7, actual: 0.25 → FAILED
# (Agent didn't use tools in expected sequence)
```

### Launch Web UI

```bash
make dev
```

Then open `http://localhost:8000` and select `tool_use_evaluator`.

### Test Prompts

**Good Tool Usage** (demonstrates proper sequencing):
```
"Analyze customer_data, extract features, validate quality, then apply random_forest model"
```

**Bad Tool Usage** (demonstrates wrong sequencing):
```
"Apply the model first, then analyze the data, then extract features"
```

## Files Structure

```
til_rubric_based_tool_use_quality_20250121/
├── tool_use_evaluator/          # Agent implementation
│   ├── __init__.py              # Package init
│   ├── agent.py                 # Main agent with 4 tools
│   └── .env.example             # Environment template
├── tests/
│   ├── test_agent.py            # Agent & tool tests
│   ├── test_imports.py          # Import & structure tests
│   └── test_structure.py        # App configuration tests
├── app.py                       # ADK app configuration
├── Makefile                     # Development commands
├── requirements.txt             # Dependencies
├── pyproject.toml              # Python project config
└── README.md                   # This file
```

## The Agent

### Agent Configuration

```python
root_agent = Agent(
    name="tool_use_evaluator",
    model="gemini-2.0-flash",
    description="Agent for demonstrating tool use quality evaluation",
    instruction="""
When asked to analyze data:
1. FIRST: Analyze the dataset
2. THEN: Extract features
3. THEN: Validate quality
4. FINALLY: Apply model

This sequence demonstrates proper tool ordering.
""",
    tools=[
        analyze_data,
        extract_features,
        validate_quality,
        apply_model,
    ],
)
```

### Tools Included

1. **analyze_data(dataset: str)**
   - Analyzes a dataset
   - Prerequisite for feature extraction
   - Returns analysis metadata

2. **extract_features(data: dict)**
   - Extracts features from analysis
   - Depends on analyze_data output
   - Prerequisite for validation

3. **validate_quality(features: dict)**
   - Validates feature quality
   - Depends on extract_features output
   - Should be called before applying model

4. **apply_model(features: dict, model: str)**
   - Applies ML model to features
   - Depends on validated features
   - Final step in pipeline

## Testing

### Run All Tests

```bash
make test
```

### Test Results

Expected output:
```
test_agent.py::TestAgentConfiguration::test_agent_name PASSED
test_agent.py::TestAgentConfiguration::test_agent_has_tools PASSED
test_agent.py::TestToolFunctionality::test_analyze_data_success PASSED
test_agent.py::TestToolFunctionality::test_extract_features_success PASSED
...

20 passed in 0.42s
```

### Test Coverage

```bash
pytest tests/ --cov=tool_use_evaluator --cov-report=html
# Open htmlcov/index.html to see coverage
```

## Evaluation Concepts

### What the Real Evaluation Does

The `make evaluate` command uses ADK's `AgentEvaluator` to:

1. **Load your agent** - Imports the tool_use_evaluator module
2. **Create test cases** - Generates evalset.json with expected tool sequences
3. **Define rubrics** - 4 evaluation criteria for tool quality
4. **Run evaluation** - Calls Gemini model as LLM judge
5. **Score results** - Produces 0.0-1.0 score for tool use quality
6. **Report differences** - Shows expected vs actual tool calls

### Tool Use Quality vs Final Response Quality

| Aspect | Tool Use | Final Response |
|--------|----------|-----------------|
| **Evaluates** | HOW tools are used | IF answer is correct |
| **Focuses on** | Tool sequence, dependencies | Answer accuracy, completeness |
| **Catches** | Wrong tool order, missing steps | Wrong final answer |
| **Threshold** | Usually 0.7-0.8 | Usually 0.7-0.85 |
| **Score Meaning** | 0.9 = perfect sequence | 0.9 = very accurate answer |

**Example:**

```
Agent produces CORRECT report but:
- Calls tools out of order (backwards sequencing)
- Skips validation step
- Uses inefficient data source

Final Response Score: ✅ HIGH (correct answer)
Tool Use Quality Score: ❌ LOW (poor tool sequencing)

Typical Case (only checking final answer):
  ✅ Tests pass - agent got correct answer

With Tool Use Quality:
  ❌ Tests fail - agent used tools poorly
  (Even though answer was right!)
```

### Rubric Scoring

Score: 0.0 - 1.0

- **1.0**: Perfect tool usage (right tools, right order)
- **0.8**: Very good (minor inefficiency)
- **0.5**: Adequate (right answer, poor tool choices)
- **0.0**: Failed (wrong tools, wrong order)

## Integration with Your Own Agent

To evaluate your agent's tool use quality using the same framework:

### Step 1: Define Your Rubrics

```python
# What "good tool use" looks like for your workflows
rubrics = [
    {
        "rubric_id": "proper_order",
        "rubric_content": {
            "text_property": "Tools are called in logical order"
        }
    },
    {
        "rubric_id": "complete_workflow",
        "rubric_content": {
            "text_property": "All necessary tools are included"
        }
    }
]
```

### Step 2: Create Test Cases (evalset.json)

```python
evalset = {
    "eval_cases": [
        {
            "eval_id": "good_sequence",
            "conversation": [{
                "user_content": {...},
                "intermediate_data": {
                    "tool_uses": [
                        {"name": "tool1", ...},
                        {"name": "tool2", ...}
                    ]
                }
            }]
        }
    ]
}
```

### Step 3: Run Evaluation

```python
from google.adk.evaluation.agent_evaluator import AgentEvaluator

results = await AgentEvaluator.evaluate(
    agent_module="your_agent",
    eval_dataset_file_path_or_dir="evalset.json",
)
```

### Real-World Example (Complete Flow)

```python
# This is what `make evaluate` actually does internally:

import asyncio
from google.adk.evaluation.agent_evaluator import AgentEvaluator

async def evaluate_tool_use():
    # 1. Create evalset with test cases
    evalset = create_test_cases()  # Good/bad sequences
    
    # 2. Create evaluation config with rubric-based metric
    config = {
        "criteria": {
            "rubric_based_tool_use_quality_v1": {
                "threshold": 0.7,
                "judge_model_options": {
                    "judge_model": "gemini-2.5-flash",
                    "num_samples": 3
                },
                "rubrics": [
                    {"rubric_id": "proper_tool_order", ...},
                    {"rubric_id": "complete_pipeline", ...},
                    ...
                ]
            }
        }
    }
    
    # 3. Run evaluation
    results = await AgentEvaluator.evaluate(
        agent_module="tool_use_evaluator",
        eval_dataset_file_path_or_dir="tool_use_quality.evalset.json",
    )
    
    # 4. Interpret results
    # - Score: 0.0-1.0
    # - Shows expected vs actual tool calls
    # - Per-rubric scores
    # - Pass/fail vs threshold
    
    print(f"Score: {results.score}")
    print(f"Status: {'PASS' if results.score >= 0.7 else 'FAIL'}")
    return results

asyncio.run(evaluate_tool_use())
```

## Environment Variables

Create `tool_use_evaluator/.env` from `.env.example`:

```bash
GOOGLE_API_KEY=your_google_api_key_here
```

Optional for Vertex AI:
```
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=your-project-id
```

## Commands

```bash
make setup       # Install and configure
make test        # Run unit tests (validates configuration)
make evaluate    # Show RUBRIC_BASED_TOOL_USE_QUALITY_V1 evaluation ⭐
make dev         # Launch ADK web interface to test tool use
make demo        # Quick validation without web interface
make clean       # Remove cache files and artifacts
make help        # Show all commands
```

### The `make evaluate` Command (NEW - Real Evaluation!)

Unlike `make demo` which shows static examples, `make evaluate` runs **actual evaluation**:

```bash
$ make evaluate

📝 TEST CASES SUMMARY
Test Case 1: good_sequence_complete_pipeline
  Expected Score: 0.95-1.0 (excellent)
  Why: All steps in correct order, all rubrics satisfied

Test Case 2: bad_sequence_skipped_validation
  Expected Score: 0.25-0.4 (poor)
  Why: Skips critical steps, violates rubrics

Test Case 3: good_sequence_proper_analysis
  Expected Score: 0.8-0.9 (good)
  Why: Proper order but doesn't apply model

📁 Creating test evalset file...
   ✓ Created: tool_use_quality.evalset.json

================================================================================
REAL EVALUATION: RUBRIC BASED TOOL USE QUALITY V1
================================================================================

📋 EVALUATION CONFIGURATION
Threshold: 0.7
Judge Model: gemini-2.5-flash
Rubrics: 4
  • proper_tool_order: Agent calls analyze_data BEFORE extract_features...
  • complete_pipeline: All 4 tools in sequence...
  • validation_before_model: Quality validated before modeling...
  • no_tool_failures: All calls succeed with proper parameters...

🔍 RUNNING EVALUATION
[LLM judge evaluates each test case against 4 rubrics...]

Summary: `EvalStatus.FAILED` for Metric: `rubric_based_tool_use_quality_v1`.
Expected threshold: `0.7`, actual value: `0.25`.

[Detailed table showing:]
- eval_status: FAILED/PASSED
- score: 0.25 (below threshold)
- expected_tool_calls: analyze_data → extract_features → validate_quality
- actual_tool_calls: [comparison of what agent actually called]

⚠️  Evaluation ran but test cases failed scoring threshold:
   This means the evaluation framework is working correctly!
   The test agent didn't match expected tool sequences.

In a real scenario, you would:
1. Review the expected vs actual tool calls above
2. Adjust agent instructions to match expected behavior
3. Re-run the evaluation to see if scores improve
```

**Key Differences:**

| Command | Purpose | Output | API Calls |
|---------|---------|--------|-----------|
| `make demo` | Show examples | Static demo configuration | None |
| `make dev` | Interactive testing | Web UI with chat | None (until you chat) |
| `make evaluate` | Real assessment | Actual evaluation scores | ✅ LLM judge calls |

**What Makes `make evaluate` Real:**

1. ✅ Creates evalset.json with test cases
2. ✅ Creates test_config.json with evaluation config
3. ✅ Calls `AgentEvaluator.evaluate()` from ADK
4. ✅ Uses Gemini model as LLM judge
5. ✅ Evaluates against 4 custom rubrics
6. ✅ Returns actual scores (0.0-1.0)
7. ✅ Shows expected vs actual tool calls (side-by-side)
8. ✅ Reports pass/fail vs threshold

## Development

### Running Tests Locally

```bash
# Run all tests
pytest tests/ -v

# Run specific test class
pytest tests/test_agent.py::TestAgentConfiguration -v

# Run with coverage
pytest tests/ --cov=tool_use_evaluator -v
```

### Adding New Tools

1. Create tool function in `tool_use_evaluator/agent.py`
2. Add to agent's `tools=[]` list
3. Add tests in `tests/test_agent.py`
4. Run `make test` to verify

### Debugging

```bash
# Run demo to check imports
make demo

# Check agent loads
python -c "from tool_use_evaluator import root_agent; print(root_agent.name)"

# Launch web interface for interactive testing
make dev
```

## Files

**TIL Article**: `/docs/til/til_rubric_based_tool_use_quality_20251021.md`
- ADK Evaluation Docs: https://google.github.io/adk-docs/
- Tool Use Quality Concept: See TIL article

## Common Issues

**Issue**: `GOOGLE_API_KEY not set`
```bash
# Solution:
export GOOGLE_API_KEY=your_key_here
# Or add to tool_use_evaluator/.env
```

**Issue**: `Module not found: tool_use_evaluator`
```bash
# Solution:
make setup
# This installs the package in development mode
```

**Issue**: Tests fail
```bash
# Solution:
make clean
make setup
make test
```

## Next Steps

1. ✅ Understand tool sequencing concepts (read TIL)
2. ✅ Run implementation tests (`make test`)
3. ✅ Test with web UI (`make dev`)
4. ✅ Adapt for your agent's tools
5. ✅ Integrate evaluation into CI/CD pipeline

## Related Resources

- **TIL Article**: Tool Use Quality Metric guide
- **Tutorial 19**: Full evaluation framework
- **ADK Docs**: Evaluation and metrics reference
- **Pause/Resume TIL**: Another ADK 1.16 feature

## License

Part of ADK Training project. See main repo for license.
