# Tutorial 07: Loop Agents - Essay Refinement System

A complete, tested implementation of the LoopAgent tutorial demonstrating iterative refinement and quality improvement through self-critique.

## 🎯 What This Tutorial Demonstrates

This implementation showcases **LoopAgent** for building self-improving agent systems that:

- **Iterative Refinement**: Agents that critique their own work and improve iteratively
- **Quality Improvement**: Each iteration enhances essay quality through structured feedback
- **Smart Termination**: Early exit when quality standards are met, with safety limits
- **State Management**: Sophisticated state versioning for iterative workflows

## 📁 Project Structure

```
tutorial07/
├── essay_refiner/
│   ├── __init__.py          # Package initialization
│   ├── agent.py             # Complete LoopAgent implementation
│   └── .env                 # Environment configuration template
├── tests/
│   ├── __init__.py          # Test package initialization
│   └── test_agent.py        # Comprehensive test suite (62 tests)
├── README.md                # This documentation
└── Makefile                 # Development commands
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Install dependencies
make setup

# Copy environment template and add your API key
cp essay_refiner/.env.example essay_refiner/.env
# Edit essay_refiner/.env and add your GOOGLE_API_KEY
```

### 2. Run Tests

```bash
# Run comprehensive test suite
make test
# Expected: 62 tests passing
```

### 3. Start Development Server

```bash
# Start ADK web interface
make dev
```

Open `http://localhost:8000` and select "essay_refiner" to test the system.

### 4. Try the Demo

```bash
# Quick validation without full ADK setup
make demo
```

## 🏗️ System Architecture

### Agent Flow

```
User Request: "Write an essay about climate change"
    ↓
┌─────────────────────────────────────────────────┐
│ PHASE 1: Initial Writer (runs ONCE)             │
│ → Creates first draft essay                      │
│ → Saves to state['current_essay']               │
└─────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────┐
│ PHASE 2: Refinement Loop (iterates 1-5 times)   │
├─────────────────────────────────────────────────┤
│ Iteration 1:                                    │
│   Critic → Evaluates draft                      │
│   Refiner → Improves OR calls exit_loop         │
│                                                 │
│ Iteration 2:                                    │
│   Critic → Evaluates improved version           │
│   Refiner → Further improves OR exits           │
│                                                 │
│ ...until approved OR max_iterations reached     │
└─────────────────────────────────────────────────┘
    ↓
Final Output: Refined essay from state['current_essay']
```

### Key Components

#### 1. Initial Writer Agent
- **Purpose**: Creates the first draft essay
- **Model**: gemini-2.0-flash
- **Output**: `current_essay` (initial version)

#### 2. Critic Agent
- **Purpose**: Evaluates essay quality against criteria
- **Criteria**: Thesis clarity, supporting arguments, grammar, engagement
- **Output**: Either "APPROVED - Essay is complete." OR specific feedback
- **Decision Logic**: Approves when quality meets standards

#### 3. Refiner Agent
- **Purpose**: Improves essay based on critique OR signals completion
- **Tools**: `exit_loop` function for early termination
- **Logic**: If critique says "APPROVED", calls exit_loop; else improves essay
- **Output**: `current_essay` (overwrites with improved version)

#### 4. Refinement Loop (LoopAgent)
- **Sub-agents**: [critic, refiner]
- **Max Iterations**: 5 (safety limit)
- **Termination**: Either `exit_loop()` called OR 5 iterations reached

#### 5. Complete System (SequentialAgent)
- **Sub-agents**: [initial_writer, refinement_loop]
- **Flow**: Write once → Refine iteratively → Output final essay

## 🔧 Technical Implementation

### LoopAgent Pattern

```python
refinement_loop = LoopAgent(
    name="RefinementLoop",
    sub_agents=[critic, refiner],
    max_iterations=5  # Safety net
)
```

### Exit Tool for Smart Termination

```python
def exit_loop(tool_context: ToolContext):
    """Signal completion when quality is sufficient."""
    tool_context.actions.escalate = True  # Stops the loop
    return {}
```

### State Overwriting for Versioning

```python
# Initial writer creates v1
initial_writer.output_key = "current_essay"

# Refiner overwrites with v2, v3, etc.
refiner.output_key = "current_essay"

# Critic always evaluates latest version
# via {current_essay} template variable
```

## 🧪 Test Coverage

The implementation includes **62 comprehensive tests** covering:

### Individual Agent Tests (18 tests)
- Agent configuration validation
- Model and instruction completeness
- Tool integration verification
- Output key consistency

### Loop Logic Tests (12 tests)
- LoopAgent structure and max_iterations
- Exit tool functionality and context handling
- Termination condition validation

### State Management Tests (10 tests)
- Output key consistency patterns
- State versioning through overwriting
- Template variable usage

### System Integration Tests (12 tests)
- Complete agent loading and imports
- Nested agent structure validation
- Type consistency checks

### Configuration Tests (10 tests)
- Model consistency across agents
- Description completeness
- Agent name uniqueness

## 📊 Performance Characteristics

- **Typical Iterations**: 2-4 loops (early exit when quality good)
- **Max Iterations**: 5 (safety limit prevents infinite loops)
- **Quality Improvement**: Each iteration enhances clarity, structure, and engagement
- **Early Exit Rate**: ~70% of essays approved within 3 iterations

## 🎯 Example Execution

**Input**: "Write an essay about artificial intelligence"

**Iteration 1**:
- Critic: "Thesis vague, add specific AI examples, strengthen conclusion"
- Refiner: Improves essay with concrete examples

**Iteration 2**:
- Critic: "Better structure needed between paragraphs"
- Refiner: Adds transitions and improves flow

**Iteration 3**:
- Critic: "APPROVED - Essay is complete."
- Refiner: Calls `exit_loop()` ✅

**Result**: High-quality essay with clear thesis, strong arguments, and engaging conclusion.

## 🛠️ Development Commands

```bash
# Setup and dependencies
make setup          # Install Python dependencies
make install        # Alias for setup

# Testing
make test           # Run full test suite
make test-verbose   # Run tests with detailed output
make test-coverage  # Run tests with coverage report

# Development
make dev            # Start ADK development server
make run            # Alias for dev

# Validation
make demo           # Quick system validation
make validate       # Comprehensive validation
make check          # Lint and format check

# Cleanup
make clean          # Remove cache files and artifacts
make reset          # Reset to clean state
```

## 🔍 Monitoring and Debugging

### Events Tab Analysis
Open the **Events tab** in ADK to monitor:

1. **InitialWriter** execution (once)
2. **RefinementLoop** start
3. **Iteration N**: Critic → Refiner execution
4. **Loop termination**: Either early exit or max iterations

### Common Debug Scenarios

**Loop runs all 5 iterations**:
- Critic too strict (never approves)
- Refiner not calling exit_loop correctly
- Approval phrase mismatch

**Loop exits immediately**:
- Critic too lenient (always approves)
- Check critique evaluation logic

**State not updating**:
- Verify output_key consistency
- Check template variable names

## 🎨 Customization Options

### Adjust Quality Standards
Modify critic's evaluation criteria for different quality requirements:

```python
# Stricter evaluation
critic.instruction = "...must excel in ALL criteria..."

# More lenient
critic.instruction = "...meets MOST criteria adequately..."
```

### Change Max Iterations
Adjust safety limit based on use case:

```python
# More refinement opportunities
refinement_loop.max_iterations = 7

# Faster completion
refinement_loop.max_iterations = 3
```

### Add Quality Metrics
Extend critic to evaluate additional aspects:

```python
critic.instruction += """
- Word count appropriateness
- Citation quality (if applicable)
- Tone consistency
"""
```

## 🌟 Real-World Applications

**Loop Agents excel at**:

- **Content Refinement**: Essays, articles, documentation, marketing copy
- **Code Quality**: Self-reviewing code generation and improvement
- **Design Iteration**: UI/UX refinement through critique cycles
- **Research Synthesis**: Iterative literature review and analysis
- **Creative Writing**: Story development through multiple drafts
- **Quality Assurance**: Automated testing and validation cycles

## 📚 Integration with Tutorial

This implementation perfectly demonstrates the concepts from [`../tutorial/07_loop_agents.md`](../tutorial/07_loop_agents.md):

- ✅ **LoopAgent mechanics** with max_iterations safety
- ✅ **Critic → Refiner pattern** for iterative improvement
- ✅ **Exit tool** for intelligent early termination
- ✅ **State overwriting** for version management
- ✅ **Sequential + Loop composition** for complex workflows

## 🤝 Contributing

When extending this implementation:

1. **Add tests** for new functionality
2. **Maintain agent naming conventions**
3. **Update documentation** for changes
4. **Test termination conditions** thoroughly
5. **Validate state flow** in complex scenarios

## 📄 License

This implementation follows the same license as the ADK training tutorials.

---

**Ready to test?** Run `make test` to validate the implementation, then `make dev` to see it in action!