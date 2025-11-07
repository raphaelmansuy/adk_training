# Tutorial: GEPA (Genetic-Pareto Prompt Optimization)

Learn how GEPA automat ically optimizes LLM agent prompts using AI-guided evolution.

## 🚀 Quick Start

```bash
# 1. Install dependencies
make setup

# 2. See GEPA in action (demo)
make demo

# 3. Configure API key (for interactive testing)
export GOOGLE_API_KEY=your_api_key_here

# 4. Start ADK web interface
make dev

# 5. Open http://localhost:8000 and select 'gepa_agent'
```

## 📚 What You'll Learn

This tutorial teaches GEPA concepts through a **simulated customer support agent**
that handles refunds and returns. The agent has known gaps that GEPA can optimize:

### The Problem

The initial agent prompt is intentionally simple:

```
You are a helpful customer support agent.
Be polite and professional.
Use the available tools to help customers.
```

This basic prompt has problems:
- ❌ Doesn't explicitly require identity verification
- ❌ Doesn't mention the 30-day return policy
- ❌ Lacks structure for tool sequencing
- ❌ Can issue refunds without proper checks

### The GEPA Solution

GEPA automatically evolves the prompt through a 5-step loop:

```
┌─────────────────────────────────────────────────────┐
│  Run Agent with Current Prompt                      │
│  (Collect failures and successful interactions)     │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│  LLM Reflection                                     │
│  (Analyze WHY failures happen)                      │
│  → "Agent needs explicit identity verification"    │
│  → "Agent should check 30-day policy"               │
│  → "Agent needs clear explanation structure"        │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│  Generate New Prompt Variants                       │
│  (Genetic operations + insights)                    │
│  → Mutation: Add requirements                       │
│  → Crossover: Combine best features                 │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│  Evaluate New Prompts                               │
│  (Test on validation set)                           │
│  → Variant A: 65% success (+15%)                    │
│  → Variant B: 72% success (+22%)                    │
└──────────────────┬──────────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────────┐
│  Select Best & Diverse Prompts                      │
│  (Pareto frontier for next iteration)               │
└──────────────────┬──────────────────────────────────┘
                   ↓
        [Loop: Repeat until improvement plateaus]
```

### Expected Results

```
Initial prompt:    40-50% task success
After GEPA iter 1: 65% success (+15 points)
After GEPA iter 2: 72% success (+7 points)
After GEPA iter 3: 85% success (+13 points)
...continues until improvement plateaus
Final result:      85-95% success (+35-45 points!)

Optimized Prompt:
  You are an expert customer support agent.
  
  CRITICAL REQUIREMENTS:
  1. ALWAYS verify customer identity FIRST
     - Never process refunds without verification
     - Use verify_customer_identity tool
  
  2. ALWAYS check return policy
     - Validate 30-day return window
     - Explain policy clearly if declining
  
  3. Provide clear explanations
     - Explain all decisions
     - Reference specific order details
  
  Tool Usage Sequence:
  - First: verify_customer_identity
  - Second: check_return_policy
  - Third: process_refund (if eligible)
```

## 🏗️ Architecture

### Agent Structure

```
Customer Support Agent
├── Tool 1: verify_customer_identity
│   └─ Checks order ID + email
│   └─ Returns success/failure
│
├── Tool 2: check_return_policy
│   └─ Validates 30-day return window
│   └─ Returns eligibility
│
└── Tool 3: process_refund
    └─ Issues refund after verification
    └─ Returns transaction details
```

### Evaluation Process

The tutorial agent is evaluated on customer scenarios:

**Success Scenarios:**
- ✓ Customer provides order ID and email
- ✓ Agent verifies identity
- ✓ Order is within 30-day window
- ✓ Agent processes refund
- ✓ Result: Happy customer, refund processed

**Failure Scenarios:**
- ✗ Agent processes refund without verification
- ✗ Agent ignores 30-day policy violation
- ✗ Agent provides unclear explanations
- Result: Policy violations, customer dissatisfaction

GEPA identifies these failure patterns and evolves the prompt to prevent them.

## 📁 Project Structure

```
tutorial_gepa_optimization/
├── gepa_agent/                 # Agent implementation
│   ├── __init__.py            # Package marker
│   ├── agent.py               # ADK agent + tools
│   └── .env.example           # API key template
│
├── tests/                     # Test suite
│   ├── test_agent.py          # Agent tests
│   ├── test_imports.py        # Import tests
│
├── Makefile                   # Build commands
├── README.md                  # This file
├── requirements.txt           # Python dependencies
└── pyproject.toml            # Package configuration
```

## 🔧 Configuration

### Setup Steps

1. **Install dependencies:**
   ```bash
   make setup
   ```

2. **Create environment file:**
   ```bash
   cp gepa_agent/.env.example gepa_agent/.env
   ```

3. **Add your API key:**
   Edit `gepa_agent/.env` and add:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

4. **Start the agent:**
   ```bash
   make dev
   ```

### Get API Key

- **Free (Gemini API)**: https://aistudio.google.com/app/apikey
- **Paid (VertexAI)**: https://console.cloud.google.com/iam-admin/serviceaccounts

## 💬 Using the Agent

### Via ADK Web Interface (Recommended)

```bash
make dev
# Opens http://localhost:8000
# Click 'gepa_agent' to select agent
# Type messages in chat
```

### Try These Prompts

**Test 1: Identity Verification**
```
User: "I want a refund for order ORD-12345"
Expected: Agent asks to verify email
Prompt checks: Does agent verify before proceeding?
```

**Test 2: Policy Adherence**
```
User: "Can I return ORD-12345 from 90 days ago?"
Expected: Agent checks policy and explains why not eligible
Prompt checks: Does agent know about 30-day limit?
```

**Test 3: Clear Explanation**
```
User: "Why was my refund denied?"
Expected: Agent provides detailed, clear explanation
Prompt checks: Does agent explain decisions clearly?
```

## 🧪 Testing

### Run All Tests

```bash
make test
```

### Test Coverage

```bash
make test-coverage
# Generates htmlcov/index.html with coverage report
```

### Test Structure

Tests cover:
- ✓ Agent configuration and initialization
- ✓ Tool declarations and async execution
- ✓ GEPA optimization concepts
- ✓ Project structure validation
- ✓ Import correctness

## 🎓 Learning Objectives

After completing this tutorial, you'll understand:

1. **What is GEPA?**
   - Genetic algorithms for prompt evolution
   - Pareto frontier for solution diversity
   - LLM reflection for guided improvement

2. **Why GEPA Works**
   - Learns from failures, not just rewards
   - Tests many variants efficiently
   - Maintains diversity to avoid local optima

3. **When to Use GEPA**
   - Agent has clear success/failure metrics
   - Evaluation is automated/fast
   - Need 20-40% performance improvement
   - Have 1-3 hours for optimization

4. **How to Apply GEPA**
   - Define evaluation metrics
   - Create evaluation dataset
   - Run GEPA optimization
   - Deploy optimized prompt

## 🎬 Live GEPA Evolution Demo

Before diving into code, see GEPA in action:

```bash
make demo
```

This runs an interactive demonstration showing:

1. **Seed Prompt** - A weak, generic baseline
2. **Evaluation** - Testing against 5 scenarios (0% success)
3. **Analysis** - Why the seed prompt failed
4. **Evolution** - An improved prompt addressing issues
5. **Validation** - Same scenarios re-tested (100% success!)
6. **Results** - Metrics showing 0% → 100% improvement

**Demo Scenarios:**
- ✅ Valid refund request (quick approval)
- ❌ Invalid email (security block)
- ❌ Outside 30-day window (policy violation)
- ✅ Exactly at 30-day boundary (edge case)
- ❌ Urgent request (requires verification first)

**What You'll See:**
- Clear before/after comparison
- Specific failures identified
- Exact improvements made
- Measurable performance gain

This demo validates that GEPA actually works!

## 📖 Understanding the Code

### The Root Agent

```python
from gepa_agent import root_agent

# This is the entry point for ADK
# It's the agent that runs in the web interface
# Initially uses INITIAL_PROMPT
# Can be evolved using GEPA
```

### Creating Custom Agents

```python
from gepa_agent.agent import create_support_agent

# Use initial prompt
agent = create_support_agent()

# Or with custom prompt (as would be done during GEPA optimization)
optimized_prompt = """..."""
agent = create_support_agent(prompt=optimized_prompt)
```

### Tools

Three tools demonstrate different scenarios:

1. **verify_customer_identity**
   - Simulates identity verification
   - Takes order_id and email
   - Returns success/failure

2. **check_return_policy**
   - Simulates policy validation
   - Checks 30-day return window
   - Returns eligibility status

3. **process_refund**
   - Simulates refund processing
   - Requires all checks passed first
   - Returns transaction details

## 🔬 GEPA Optimization Workflow

### Step 1: Evaluate Initial Prompt

```bash
# Baseline performance measurement
python -c "
from gepa_agent import root_agent
# Run agent on 10 test scenarios
# Measure success rate (e.g., 40-50%)
"
```

### Step 2: Collect Failures

Identify failure scenarios:
- Missing identity verification
- Policy violations
- Unclear explanations

### Step 3: LLM Reflection

Use gemini-2.5-pro to analyze:
- Why refunds processed without verification?
- Why policies were ignored?
- Why explanations were unclear?

### Step 4: Generate Variants

Create improved prompts:
- Mutation: Add explicit requirements
- Crossover: Combine best features
- Refinement: Use insights

### Step 5: Evaluate Variants

Test on validation set:
- Variant A: 65% success
- Variant B: 72% success
- Variant C: 68% success

### Step 6: Select Frontier

Keep best and diverse prompts:
- B (72%) - best overall
- A (65%) - alternative approach
- Maybe C (68%) - different strategy

### Step 7: Iterate

Use frontier prompts for next iteration:
- Collect new failures with B, A, C
- Reflect on new patterns
- Generate next variants
- Evaluate and select

Repeat until improvement plateaus.

## 📊 Expected Evolution

```
Iteration  | Best Score | Improvement | Tools/Prompts
-----------|-----------|-------------|---------------
0 (seed)   | 50%       | baseline    | Initial simple
1          | 65%       | +15%        | 4 variants
2          | 72%       | +7%         | 5 variants
3          | 85%       | +13%        | 5 variants
4          | 88%       | +3%         | 4 variants
5          | 90%       | +2%         | plateau reached
```

## 🐛 Troubleshooting

### Issue: ImportError when importing gepa_agent

```bash
# Solution: Make sure package is installed
pip install -e .
# Reinstall if needed
pip install -e . --force-reinstall
```

### Issue: GOOGLE_API_KEY not set

```bash
# Solution: Configure authentication
export GOOGLE_API_KEY=your_key_here

# Or use .env file
cp gepa_agent/.env.example gepa_agent/.env
# Edit .env and add your key
```

### Issue: Tests fail with async errors

```bash
# Solution: Install pytest-asyncio
pip install pytest-asyncio

# And run tests
make test
```

### Issue: ADK web interface not available

```bash
# Solution: Install ADK CLI
pip install google-adk>=0.1.4

# Then try again
make dev
```

## 🚀 Next Steps

### Learn More About GEPA

**Official Resources:**

- **[GEPA Research Paper](https://arxiv.org/abs/2507.19457)** - Original research from Stanford NLP
  - "GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning"
  - Authors: Lakshya A Agrawal et al.
  - Published: July 2025

- **[DSPy Framework](https://github.com/stanfordnlp/dspy)** - GEPA is part of DSPy
  - Full documentation: [dspy.ai](https://dspy.ai/)
  - GEPA implementation and optimizers
  - Community support: [Discord](https://discord.gg/XCGy2WDCQB)

- **[Tutorial Implementation](../tutorial_gepa_optimization/)** - This working example
  - `gepa_demo.py` - Fully annotated evolution demonstration
  - `gepa_agent/agent.py` - Agent implementation with comments
  - `tests/` - Comprehensive test suite showing GEPA concepts

### Implement Real GEPA Optimization

To run actual GEPA optimization (beyond this conceptual demo):

1. Install DSPy with GEPA support:
   ```bash
   pip install dspy-ai
   ```

2. Create evaluation function that uses this agent

3. Run GEPA optimization loop

4. Deploy optimized prompt

### Explore Related Tutorials

- **Tutorial 01**: Hello World Agent (basic concepts)
- **Tutorial 02**: Function Tools (building blocks)
- **Tutorial 04**: Sequential Workflows (orchestration)
- **Tutorial 30**: Full-stack with Next.js + FastAPI

## 📝 Key Concepts

### Pareto Frontier

Don't keep only the BEST prompt. Keep multiple diverse prompts:
- Best performing
- Alternative approaches
- Different strengths

This diversity enables GEPA to explore better in future iterations.

### LLM Reflection

The key innovation in GEPA:
- Analyze WHY failures happen
- Extract actionable insights
- Guide prompt evolution
- Not just random mutation

### Genetic Algorithms

Proven techniques adapted for prompts:
- Mutation: Modify based on insights
- Crossover: Combine features from multiple prompts
- Selection: Keep best and diverse
- Evolution: Generational improvement

## 🤝 Contributing

Found an issue? Have suggestions?
- Open issue: https://github.com/raphaelmansuy/adk_training/issues
- Submit PR: https://github.com/raphaelmansuy/adk_training/pulls

## 📄 License

Part of ADK Training project. Apache License 2.0.

---

**Built with ❤️ using Google ADK**

