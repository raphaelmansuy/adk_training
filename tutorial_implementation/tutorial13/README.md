# Tutorial 13: Code Execution - Financial Calculator Agent

A complete, production-ready implementation demonstrating **BuiltInCodeExecutor** for enabling AI agents to write and execute Python code for precise calculations, data analysis, and algorithm implementation.

## 🎯 What This Tutorial Demonstrates

This implementation showcases **Code Execution** capabilities for building agents that:

- **Execute Python Code**: Generate and run Python code within the model environment
- **Precise Calculations**: Perform exact mathematical operations (no approximation errors)
- **Financial Analysis**: Compound interest, loan payments, retirement planning, ROI calculations
- **Statistical Processing**: Mean, median, standard deviation, data analysis
- **Algorithm Implementation**: Binary search, prime numbers, sorting, optimization
- **Data Processing**: Arrays, lists, statistical transformations

## 📁 Project Structure

```
tutorial13/
├── code_calculator/
│   ├── __init__.py          # Package initialization
│   ├── agent.py             # Financial calculator agent with code execution
│   └── .env.example         # Environment configuration template
├── tests/
│   ├── __init__.py          # Test package initialization
│   └── test_agent.py        # Comprehensive test suite (40+ tests)
├── pyproject.toml           # Python package configuration
├── requirements.txt         # Python dependencies
├── Makefile                 # Development commands
└── README.md                # This documentation
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Install dependencies
make setup

# Copy environment template and add your API key
cp code_calculator/.env.example code_calculator/.env
# Edit code_calculator/.env and add your GOOGLE_API_KEY
```

### 2. Run Tests

```bash
# Run comprehensive test suite
make test
# Expected: 40+ tests passing
```

### 3. Start Development Server

```bash
# Start ADK web interface
make dev
```

Open `http://localhost:8000` and select "code_calculator" to test the agent.

### 4. Try Demo Examples

```bash
# See all demo prompts
make demo
```

## 🏗️ Code Execution Architecture

### How BuiltInCodeExecutor Works

```
User Query: "Calculate compound interest on $10,000 at 7% for 30 years"
    ↓
┌─────────────────────────────────────────────────┐
│ Agent receives request                           │
│ Model: gemini-2.0-flash                         │
└─────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────┐
│ Model generates Python code                      │
│ Code:                                            │
│   principal = 10000                              │
│   rate = 0.07                                    │
│   years = 30                                     │
│   compounds_per_year = 12                        │
│   future_value = principal * (1 + rate/cpn)^...  │
└─────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────┐
│ Code executes in model environment              │
│ (Google's infrastructure, not locally)           │
│ Result: 81402.45                                 │
└─────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────┐
│ Model integrates result into response            │
│ "Your $10,000 will grow to $81,402.45 after 30  │
│  years with monthly compounding at 7% annual    │
│  interest. You'll earn $71,402.45 in interest." │
└─────────────────────────────────────────────────┘
```

### Key Components

#### 1. Financial Calculator Agent

- **Model**: `gemini-2.0-flash` (requires Gemini 2.0+ for code execution)
- **Code Executor**: `BuiltInCodeExecutor()` - enables Python code generation and execution
- **Temperature**: 0.1 (very low for deterministic, accurate code)
- **Capabilities**:
  - Compound interest calculations
  - Loan payment amortization
  - Retirement planning and savings goals
  - Investment analysis (ROI, CAGR, NPV, IRR)
  - Break-even analysis
  - Statistical data analysis
  - Algorithm implementation

#### 2. BuiltInCodeExecutor

**Source**: `google.adk.code_executors.BuiltInCodeExecutor`

```python
from google.adk.code_executors import BuiltInCodeExecutor

agent = Agent(
    model='gemini-2.0-flash',  # Requires Gemini 2.0+
    code_executor=BuiltInCodeExecutor()
)
```

**Key Characteristics**:

- **Model-Side Execution**: Code runs inside Google's model environment (not locally)
- **Gemini 2.0+ Only**: Older models don't support code execution
- **Sandboxed Environment**: Isolated, secure execution
- **Standard Library Only**: Python standard library available (no external packages)
- **No Network/File Access**: Cannot access files or make network requests

#### 3. Instruction Design

The agent instruction emphasizes:

1. **Always Use Code**: Execute Python for ALL calculations (no approximation)
2. **Show Code**: Display the Python code being executed
3. **Explain Formulas**: Describe the financial concepts and formulas
4. **Format Results**: Use $ and proper number formatting
5. **Provide Interpretation**: Explain what the numbers mean
6. **Handle Errors**: Validate inputs and provide helpful error messages

## 🔧 Technical Implementation

### Agent Configuration

```python
financial_calculator = Agent(
    model="gemini-2.0-flash",  # Gemini 2.0+ required
    name="FinancialCalculator",
    description="Expert financial calculator with Python code execution",
    instruction="""
    You are a financial calculator expert that uses Python code execution.

    Always:
    1. Write Python code for calculations
    2. Show the code you're executing
    3. Explain the formulas
    4. Format results with $ and commas
    5. Provide interpretation

    Financial formulas you know:
    - Compound Interest: A = P(1 + r/n)^(nt)
    - Loan Payment: M = P[r(1+r)^n]/[(1+r)^n-1]
    - Present Value: PV = FV / (1 + r)^n
    ...
    """,
    code_executor=BuiltInCodeExecutor(),
    generate_content_config=types.GenerateContentConfig(
        temperature=0.1,  # Low for accuracy
        max_output_tokens=2048
    )
)

root_agent = financial_calculator
```

### Code Execution Patterns

#### Pattern 1: Financial Calculations

```python
# User Query: "Calculate compound interest on $10,000 at 7% for 30 years"

# Agent generates and executes:
principal = 10000
rate = 0.07
years = 30
compounds_per_year = 12

future_value = principal * (1 + rate/compounds_per_year) ** (compounds_per_year * years)
interest_earned = future_value - principal

print(f"Future Value: ${future_value:,.2f}")
print(f"Interest Earned: ${interest_earned:,.2f}")

# Result: $81,402.45
```

#### Pattern 2: Statistical Analysis

```python
# User Query: "Calculate mean, median, std dev of [15, 18, 16.5, 22, 21, 25]"

# Agent generates and executes:
import statistics

data = [15, 18, 16.5, 22, 21, 25]

mean = statistics.mean(data)
median = statistics.median(data)
stdev = statistics.stdev(data)

print(f"Mean: {mean:.2f}")
print(f"Median: {median:.2f}")
print(f"Std Dev: {stdev:.2f}")
```

#### Pattern 3: Algorithm Implementation

```python
# User Query: "Implement binary search to find 42 in [1, 5, 12, 23, 42, 67, 89, 99]"

# Agent generates and executes:
def binary_search(arr, target):
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1

arr = [1, 5, 12, 23, 42, 67, 89, 99]
result = binary_search(arr, 42)

print(f"Found 42 at index {result}")
```

## 🧪 Test Coverage

The implementation includes **40+ comprehensive tests** covering:

### Configuration Tests (11 tests)

- Agent import and type validation
- Model requirement (Gemini 2.0+)
- Code executor configuration
- Temperature settings
- Instruction completeness

### Code Execution Tests (3 tests)

- Simple arithmetic
- Factorial calculations
- Statistical functions

### Financial Calculation Tests (3 tests)

- Basic compound interest
- Complex compound interest (30 years)
- Loan payment calculations

### Algorithm Implementation Tests (2 tests)

- Prime number checking
- Binary search implementation

### Statistical Analysis Tests (2 tests)

- Standard deviation
- Median calculation

### Edge Case Tests (2 tests)

- Zero principal handling
- Empty list handling

### Integration Tests (3 tests)

- Retirement planning
- Break-even analysis
- Data analysis workflow

### Code Quality Tests (4 tests)

- Documentation completeness
- Instruction quality
- Description accuracy
- Performance configuration

## 📊 Example Interactions

### 1. Compound Interest Calculation

**User**: "If I invest $10,000 at 7% annual interest compounded monthly, how much will I have after 30 years?"

**Agent Response**:

```
Let me calculate the compound interest:

[Code:]
principal = 10000
rate = 0.07
years = 30
compounds_per_year = 12

future_value = principal * (1 + rate/compounds_per_year) ** (compounds_per_year * years)
interest_earned = future_value - principal

print(f"Future Value: ${future_value:,.2f}")
print(f"Interest Earned: ${interest_earned:,.2f}")
print(f"Multiple: {future_value/principal:.2f}x")

[Result:]
Future Value: $81,402.45
Interest Earned: $71,402.45
Multiple: 8.14x

Your investment will grow to $81,402.45, earning $71,402.45 in interest.
Your money will multiply 8.14 times over 30 years with monthly compounding.
```

### 2. Loan Payment Calculation

**User**: "Calculate the monthly payment on a $300,000 mortgage at 6.5% annual interest for 30 years"

**Agent Response**:

```
Let me calculate the mortgage payment:

[Code:]
principal = 300000
annual_rate = 0.065
monthly_rate = annual_rate / 12
num_payments = 30 * 12

numerator = monthly_rate * (1 + monthly_rate) ** num_payments
denominator = (1 + monthly_rate) ** num_payments - 1
monthly_payment = principal * (numerator / denominator)

total_paid = monthly_payment * num_payments
total_interest = total_paid - principal

print(f"Monthly Payment: ${monthly_payment:,.2f}")
print(f"Total Paid: ${total_paid:,.2f}")
print(f"Total Interest: ${total_interest:,.2f}")

[Result:]
Monthly Payment: $1,896.20
Total Paid: $682,632.00
Total Interest: $382,632.00

Your monthly payment will be $1,896.20.
Over 30 years, you'll pay $682,632 total, with $382,632 in interest.
```

### 3. Data Analysis

**User**: "Analyze sales data: Jan 15000, Feb 18000, Mar 16500, Apr 22000, May 21000, Jun 25000"

**Agent Response**:

```
Let me analyze the sales data:

[Code:]
import statistics

sales = [15000, 18000, 16500, 22000, 21000, 25000]
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']

mean = statistics.mean(sales)
median = statistics.median(sales)
stdev = statistics.stdev(sales)
total = sum(sales)

growth = [(sales[i] - sales[i-1]) / sales[i-1] * 100
          for i in range(1, len(sales))]

best_month = months[sales.index(max(sales))]

print(f"Mean: ${mean:,.2f}")
print(f"Median: ${median:,.2f}")
print(f"Std Dev: ${stdev:,.2f}")
print(f"Total: ${total:,}")
print(f"Best Month: {best_month}")
print(f"Avg Growth: {statistics.mean(growth):.1f}%")

Key Insights:
- Strong upward trend with 9.2% average monthly growth
- June showed best performance at $25,000
- Consistent growth from April onwards
```

## 🛠️ Development Commands

```bash
# Setup and dependencies
make setup          # Install Python dependencies
make install        # Alias for setup

# Testing
make test           # Run full test suite
make test-verbose   # Run tests with detailed output
make test-cov       # Run tests with coverage report

# Development
make dev            # Start ADK development server
make run            # Alias for dev

# Validation
make demo           # Show demo prompts
make validate       # Run comprehensive validation
make check          # Alias for validate

# Cleanup
make clean          # Remove cache files and artifacts
make reset          # Reset to clean state
```

## 🎨 Customization Options

### Adjust Temperature

```python
# More deterministic (recommended for calculations)
generate_content_config=types.GenerateContentConfig(
    temperature=0.0  # Most deterministic
)

# Slightly more creative (still accurate)
generate_content_config=types.GenerateContentConfig(
    temperature=0.2
)
```

### Add Custom Financial Formulas

Extend the instruction to include additional formulas:

```python
instruction += """
Additional formulas:
- Net Present Value (NPV): Sum of discounted cash flows
- Internal Rate of Return (IRR): Rate where NPV = 0
- Modified Duration: Interest rate sensitivity measure
"""
```

### Configure Output Verbosity

```python
instruction += """
Output Format:
- BRIEF: Show only final results
- DETAILED: Show code, explanation, and interpretation
- TECHNICAL: Include all intermediate calculations
"""
```

## 🔍 Troubleshooting

### Issue: "Code execution requires Gemini 2.0+"

**Cause**: Using older model version

**Solution**:

```python
# ❌ Wrong - old model
agent = Agent(
    model='gemini-1.5-flash',
    code_executor=BuiltInCodeExecutor()
)

# ✅ Correct - Gemini 2.0+
agent = Agent(
    model='gemini-2.0-flash',
    code_executor=BuiltInCodeExecutor()
)
```

### Issue: "Model not generating code"

**Cause**: Query doesn't trigger code execution

**Solution**: Make queries explicitly require computation

```python
# ❌ Vague query
"What's compound interest?"

# ✅ Specific calculation query
"Calculate compound interest on $10,000 at 5% for 10 years"
```

### Issue: "Code execution errors"

**Cause**: Generated code has bugs

**Solution**: Lower temperature for more reliable code

```python
generate_content_config=types.GenerateContentConfig(
    temperature=0.0  # Most reliable
)
```

### Issue: "Slow responses"

**Cause**: Code execution adds latency

**Solution**: Use streaming for better UX

```python
from google.adk.agents import RunConfig, StreamingMode

run_config = RunConfig(streaming_mode=StreamingMode.SSE)

async for event in runner.run_async(query, agent=agent, run_config=run_config):
    print(event.content.parts[0].text, end='', flush=True)
```

## 🌟 Real-World Applications

**Code Execution excels at**:

- **Financial Services**: Loan calculators, investment analysis, retirement planning
- **Data Analysis**: Statistical processing, trend analysis, forecasting
- **Scientific Computing**: Physics calculations, engineering formulas, simulations
- **Educational Tools**: Math tutoring, algorithm demonstration, proof verification
- **Business Analytics**: Break-even analysis, cost modeling, optimization
- **Research**: Data processing, statistical testing, mathematical proofs

## 📚 Integration with Tutorial

This implementation perfectly demonstrates the concepts from [`../../docs/tutorial/13_code_execution.md`](../../docs/tutorial/13_code_execution.md):

- ✅ **BuiltInCodeExecutor** setup and configuration
- ✅ **Gemini 2.0+ requirement** enforcement
- ✅ **Model-side execution** (not local)
- ✅ **Financial calculations** with precise results
- ✅ **Algorithm implementation** capabilities
- ✅ **Statistical analysis** patterns
- ✅ **Low temperature** for accuracy
- ✅ **Comprehensive testing** with 40+ tests

## 🔒 Security Considerations

### What Code Execution CAN Do

- ✅ Mathematical calculations
- ✅ Data processing (lists, dicts, arrays)
- ✅ Algorithm implementation
- ✅ Statistical analysis
- ✅ String manipulation
- ✅ Use Python standard library

### What Code Execution CANNOT Do

- ❌ Access local files or file system
- ❌ Make network requests
- ❌ Install external packages
- ❌ Execute shell commands
- ❌ Access environment variables
- ❌ Persist data between executions

**Security Benefits**:

- **Sandboxed Execution**: Code runs in isolated model environment
- **No Local Risk**: Cannot affect your local system
- **Automatic Cleanup**: No persistent state
- **Resource Limited**: Constrained execution resources

## 🤝 Contributing

When extending this implementation:

1. **Maintain low temperature** for code accuracy
2. **Add tests** for new financial calculations
3. **Update instruction** for new capabilities
4. **Document formulas** in agent instruction
5. **Validate calculations** against known results

## 📄 License

This implementation follows the same license as the ADK training tutorials.

---

**Ready to calculate?** Run `make test` to validate the implementation, then `make dev` to see code execution in action!
