## Google GenAI Agent ADK: Core Concepts & Architecture

**📋 RESEARCH STATUS: COMPLETE** - All ADK patterns documented. 10 comprehensive tutorials created (6,435 lines of content).

### What is ADK?
Agent Development Kit (ADK) is a flexible, modular framework for building, evaluating, and deploying AI agents. While optimized for Gemini and Google Cloud, it is model-agnostic and can integrate with other frameworks and LLMs.

### Key Features
- **Rich Tool Ecosystem:** Pre-built tools, custom functions, OpenAPI, 3rd-party integrations.
- **Code-First Development:** Define agents, tools, and workflows directly in Python.
- **Modular Multi-Agent Systems:** Compose specialized agents into scalable, hierarchical systems.
- **Flexible Orchestration:** Use workflow agents (Sequential, Parallel, Loop) or LLM-driven routing for dynamic behavior.
- **Deployment Ready:** Run locally, on Vertex AI Agent Engine, Cloud Run, or custom infra.
- **Built-in Evaluation:** Assess agent performance and execution steps.
- **Safety & Security:** Patterns and best practices for trustworthy agents.

### Main Components
- **Agents:** Core logic units (LLM agents, workflow agents, custom agents, multi-agent systems).
- **Tools:** Extend agent capabilities (search, code exec, custom functions, APIs, etc.).
- **Workflows:** Orchestrate tasks (sequential, parallel, loop, dynamic routing).
- **Deployment:** Containerize and deploy anywhere; supports cloud and local.
- **Sessions & Memory:** Manage state, memory, and context for agents.
- **Callbacks & Observability:** Logging, tracing, evaluation, and monitoring.

### Ecosystem & Model-Agnosticism
- Optimized for Gemini, but supports other LLMs (GPT, Claude, etc.) and frameworks (LangChain, CrewAI).
- Integrates with Google Cloud, but can run standalone or in other environments.

### Loop Agents (Iterative Refinement)

**Source**: https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/

### Purpose
`LoopAgent` is a workflow agent that **executes sub-agents iteratively** (in a loop) for refinement, retry, or quality improvement scenarios.

### When to Use Loop Agents

Use `LoopAgent` when:
- Need iterative refinement (improve quality over iterations)
- Want retry logic (keep trying until success)
- Building self-improving systems (critique → refine → repeat)
- Quality matters more than first-draft speed

### Key Characteristics

- **Not LLM-powered**: Deterministic execution loop
- **Runs sub-agents repeatedly**: Each iteration goes through all sub-agents
- **Must have termination**: YOU must prevent infinite loops
- **max_iterations**: Hard limit on loop count
- **Escalation pattern**: Sub-agent signals "done" via tool

### Termination Strategies

**Strategy 1: Max Iterations (Simple)**
```python
loop_agent = LoopAgent(
    sub_agents=[critic, refiner],
    max_iterations=5  # Stops after 5 iterations
)
```

**Strategy 2: Exit Tool (Smart)**
```python
def exit_loop(tool_context: ToolContext):
    """Signal loop completion."""
    tool_context.actions.escalate = True
    return {}

# Agent calls this tool when done
refiner = Agent(
    tools=[exit_loop],
    instruction="If critique says 'No issues', call exit_loop."
)
```

**Strategy 3: Combination (Best)**
Use both max_iterations (safety) + exit tool (early termination)

### Common Pattern: Critic → Refiner Loop

```python
# Step 1: Critic evaluates quality
critic = Agent(
    name="critic",
    model="gemini-2.0-flash",
    instruction=(
        "Review the document: {current_doc}\n"
        "If good quality: output 'APPROVED'\n"
        "Else: list specific improvements needed"
    ),
    output_key="critique"
)

# Step 2: Refiner improves OR exits
refiner = Agent(
    name="refiner",
    model="gemini-2.0-flash",
    tools=[exit_loop],
    instruction=(
        "Read critique: {critique}\n"
        "If critique says 'APPROVED': call exit_loop\n"
        "Else: improve document based on critique"
    ),
    output_key="current_doc"  # Overwrites for next iteration
)

# Loop: critic → refiner → critic → refiner → ...
loop = LoopAgent(
    sub_agents=[critic, refiner],
    max_iterations=5  # Safety limit
)
```

### How It Works (Execution Flow)

1. **Iteration 1**:
   - Run critic → saves to state['critique']
   - Run refiner → reads critique, improves doc
2. **Iteration 2**:
   - Run critic again → evaluates improved doc
   - Run refiner again → improves more OR calls exit_loop
3. **Continue** until:
   - exit_loop called (tool_context.actions.escalate = True)
   - OR max_iterations reached

### State Management in Loops

**Key Pattern**: Use same `output_key` to overwrite state each iteration

```python
writer = Agent(
    output_key="document"  # Iteration 1: writes doc
)

refiner = Agent(
    instruction="Improve: {document}",
    output_key="document"  # Iteration 2: OVERWRITES same key!
)
```

Each iteration, the refiner reads the latest version and overwrites it.

### Complete Example Pattern

```python
from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.tools.tool_context import ToolContext

# Exit tool
def exit_loop(tool_context: ToolContext):
    tool_context.actions.escalate = True
    return {}

# Initial creation (outside loop)
initial_writer = Agent(
    name="initial_writer",
    instruction="Write first draft about: {topic}",
    output_key="current_doc"
)

# Critic (inside loop)
critic = Agent(
    name="critic",
    instruction=(
        "Review: {current_doc}\n"
        "If excellent: output 'APPROVED'\n"
        "Else: list improvements"
    ),
    output_key="critique"
)

# Refiner with exit (inside loop)
refiner = Agent(
    name="refiner",
    tools=[exit_loop],
    instruction=(
        "Critique: {critique}\n"
        "Doc: {current_doc}\n"
        "If APPROVED: call exit_loop\n"
        "Else: apply improvements"
    ),
    output_key="current_doc"  # Overwrites each iteration
)

# Assemble pipeline
refinement_loop = LoopAgent(
    sub_agents=[critic, refiner],
    max_iterations=5
)

root_agent = SequentialAgent(
    sub_agents=[
        initial_writer,    # Run once
        refinement_loop    # Loop until approved or max iterations
    ]
)
```

### Best Practices

**DO:**
- Always set `max_iterations` (safety!)
- Use exit tool for early termination
- Overwrite state keys for iteration
- Keep loop agents focused (2-3 sub-agents max)
- Test termination conditions

**DON'T:**
- Forget max_iterations (infinite loop risk!)
- Put too many agents in loop (slow)
- Assume loop will always exit early
- Use loops when sequential would work

### Real-World Use Cases

- **Quality Improvement**: Essay editing, code refactoring, image generation
- **Retry Logic**: API calls with validation, data fetch with error handling
- **Consensus Building**: Multi-reviewer systems, voting mechanisms
- **Self-Correction**: Math problem solving with verification

## State & Memory (Session Management)

**Source**: https://google.github.io/adk-docs/sessions/state/, https://google.github.io/adk-docs/sessions/memory/

### Session State (`session.state`)

Session state is the agent's **scratchpad** - a key-value dictionary for tracking conversation-level data.

**Key Characteristics**:
- **Structure**: `key: value` pairs where keys are strings
- **Values**: Must be serializable (strings, numbers, booleans, lists, dicts)
- **Mutability**: Changes during conversation
- **Persistence**: Depends on SessionService (InMemory = lost on restart, Database/VertexAI = persistent)

### State Prefixes (Scoping)

**No Prefix (Session State)**:
- Scope: Current session only
- Example: `state['current_intent'] = 'book_flight'`
- Use: Task progress, temporary flags

**`user:` Prefix (User State)**:
- Scope: All sessions for that user (shared across sessions)
- Example: `state['user:preferred_language'] = 'fr'`
- Use: User preferences, profile details

**`app:` Prefix (App State)**:
- Scope: All users and sessions for the app
- Example: `state['app:global_discount_code'] = 'SAVE10'`
- Use: Global settings, shared templates

**`temp:` Prefix (Temporary Invocation State)**:
- Scope: Current invocation only (discarded after)
- Example: `state['temp:raw_api_response'] = {...}`
- Use: Intermediate calculations, flags within single invocation
- **Important**: Shared across all sub-agents in same invocation!

### Accessing State in Instructions

**Direct Injection with `{key}` Syntax**:
```python
agent = Agent(
    instruction="Write a story about {topic}."  # Replaced with state['topic']
)
```

**Optional Keys**: `{topic?}` - won't error if missing

**Escaping**: Use `InstructionProvider` function for literal `{{}}` braces

### How State is Updated

**Method 1: `output_key` (Easiest)**:
```python
agent = Agent(
    output_key="last_greeting"  # Auto-saves response to state
)
```

**Method 2: `EventActions.state_delta` (Manual)**:
```python
state_changes = {
    "task_status": "active",
    "user:login_count": count + 1
}
actions = EventActions(state_delta=state_changes)
await session_service.append_event(session, Event(..., actions=actions))
```

**Method 3: Via `CallbackContext` or `ToolContext` (Recommended)**:
```python
def my_callback(context: CallbackContext):
    context.state["user_action_count"] = count + 1
    # Changes auto-tracked in EventActions!
```

### ⚠️ Critical Warning

**DON'T** directly modify `session.state` from `SessionService.get_session()`:
```python
# BAD! Bypasses event tracking, won't persist
session = await session_service.get_session(...)
session.state['key'] = value  # WRONG!
```

**DO** use context objects or EventActions - they track changes properly!

### Memory Service (`MemoryService`)

Memory provides **long-term knowledge** beyond current session - like a searchable archive.

**Two Implementations**:

1. **InMemoryMemoryService** (Dev/Testing):
   - No persistence (data lost on restart)
   - Basic keyword matching
   - No setup required
   
2. **VertexAiMemoryBankService** (Production):
   - Persistent with Vertex AI Agent Engine
   - Semantic search powered by LLM
   - Extracts and consolidates memories from conversations
   - Requires: GCP Project, Agent Engine, authentication

### Using Memory

**Configuration**:
```bash
adk web path/to/agent --memory_service_uri="agentengine://1234567890"
```

**Or programmatically**:
```python
memory_service = VertexAiMemoryBankService(
    project="PROJECT_ID",
    location="LOCATION",
    agent_engine_id=agent_engine_id
)
runner = Runner(..., memory_service=memory_service)
```

**Retrieval Tools**:
- `PreloadMemoryTool()`: Always retrieves memory at start of each turn
- `LoadMemoryTool()`: Retrieves when agent decides it's helpful

**Saving to Memory**:
```python
await memory_service.add_session_to_memory(session)
```

### Memory Workflow

1. User interacts with agent (session managed by SessionService)
2. After session, call `add_session_to_memory(session)` to ingest
3. Later, agent uses memory tool to search: `search_memory(app_name, user_id, query)`
4. Memory service returns relevant snippets from past sessions
5. Agent uses retrieved context to answer user

## Callbacks (Control Flow & Monitoring)

**Source**: https://google.github.io/adk-docs/callbacks/

### What are Callbacks?

Callbacks are **functions you define** that ADK automatically calls at specific execution points. They let you observe, customize, and control agent behavior without modifying ADK core.

### Callback Types

**Agent Lifecycle**:
- `before_agent_callback`: Before agent's main logic starts
- `after_agent_callback`: After agent finishes, before result returned

**LLM Interaction** (LlmAgent only):
- `before_model_callback`: Before LLM API call
- `after_model_callback`: After LLM response received

**Tool Execution** (LlmAgent only):
- `before_tool_callback`: Before tool function runs
- `after_tool_callback`: After tool function completes

### Control Flow Pattern

**Return `None`** → Allow default behavior (proceed normally)

**Return Specific Object** → Override/skip default behavior:
- `before_agent_callback` → `Content`: Skip agent execution
- `before_model_callback` → `LlmResponse`: Skip LLM call
- `before_tool_callback` → `dict`: Skip tool execution
- `after_agent_callback` → `Content`: Replace agent output
- `after_model_callback` → `LlmResponse`: Replace LLM response
- `after_tool_callback` → `dict`: Replace tool result

### Common Patterns

**1. Guardrails & Policy Enforcement**:
```python
def check_request(callback_context: CallbackContext, llm_request):
    if has_forbidden_content(llm_request.contents):
        return LlmResponse(...)  # Block LLM call
    return None  # Allow
```

**2. Dynamic State Management**:
```python
def save_transaction(tool_context: ToolContext, tool_response):
    tool_context.state['last_transaction_id'] = tool_response['id']
    return None  # Use original response
```

**3. Logging and Monitoring**:
```python
def log_tool_call(callback_context, tool_name, args):
    logger.info(f"Tool: {tool_name}, Args: {args}")
    return None
```

**4. Caching**:
```python
def check_cache(callback_context, llm_request):
    cache_key = hash(llm_request.contents)
    if cache_key in callback_context.state:
        return callback_context.state[cache_key]  # Return cached
    return None  # Allow LLM call
```

**5. Request/Response Modification**:
```python
def add_language_hint(callback_context, llm_request):
    if callback_context.state.get('lang') == 'es':
        llm_request.config.system_instruction += "\nRespond in Spanish."
    return None
```

**6. Conditional Skipping**:
```python
def check_quota(tool_context, tool_name, args):
    if tool_context.state.get('api_quota_exceeded'):
        return {'error': 'Quota exceeded'}  # Skip tool
    return None
```

**7. Tool-Specific Actions**:
```python
def handle_auth(tool_context, tool_name, args):
    # Authentication
    if not tool_context.get_auth_response():
        tool_context.request_credential(auth_config)
    # Summarization control
    tool_context.actions.skip_summarization = True
    return None
```

**8. Artifact Handling**:
```python
async def save_report(tool_context, tool_response):
    await tool_context.save_artifact("report.pdf", report_data)
    return None
```

### Best Practices

**Design**:
- Keep focused (single purpose per callback)
- Avoid long-running operations (callbacks are synchronous)

**Error Handling**:
- Use try/except blocks
- Log errors appropriately
- Decide: halt or recover?

**State Management**:
- Be deliberate about state changes
- Use specific keys, not broad modifications
- Consider prefixes (`user:`, `app:`, `temp:`)

**Testing**:
- Unit test with mock context objects
- Integration test in full agent flow
- Document purpose and side effects

## Evaluation Framework

**Source**: https://google.github.io/adk-docs/evaluate/

### Why Evaluate Agents?

Traditional testing (unit/integration) gives pass/fail signals. **LLM agents need qualitative evaluation** due to probabilistic nature.

Evaluate:
1. **Trajectory**: Steps agent took (tool calls, reasoning process)
2. **Final Response**: Quality, relevance, correctness of output

### What to Evaluate

**Trajectory Metrics** (Ground-truth based):
- **Exact match**: Perfect match to ideal trajectory
- **In-order match**: Correct actions in order (extra actions OK)
- **Any-order match**: Correct actions in any order
- **Precision**: Relevance of predicted actions
- **Recall**: How many essential actions captured
- **Single-tool use**: Check for specific action

**Response Metrics**:
- **tool_trajectory_avg_score**: Average match of tool usage (0-1)
- **response_match_score**: ROUGE similarity to expected response (0-1)

### Evaluation Approaches

**Approach 1: Test Files** (Unit Testing):
- Single `.test.json` file per session
- Simple interactions for rapid testing
- Best for active development
- Schema: [EvalSet](https://github.com/google/adk-python/blob/main/src/google/adk/evaluation/eval_set.py), [EvalCase](https://github.com/google/adk-python/blob/main/src/google/adk/evaluation/eval_case.py)

**Approach 2: Evalset Files** (Integration Testing):
- Multiple sessions in one `.evalset.json` file
- Complex multi-turn conversations
- Run less frequently (more extensive)
- Use UI tools to capture and convert sessions

### Test File Structure

```json
{
  "eval_set_id": "test_set_id",
  "eval_cases": [
    {
      "eval_id": "case_1",
      "conversation": [
        {
          "invocation_id": "uuid",
          "user_content": {...},           // User query
          "final_response": {...},         // Expected response
          "intermediate_data": {
            "tool_uses": [...],            // Expected tool trajectory
            "intermediate_responses": []   // Sub-agent responses
          }
        }
      ],
      "session_input": {
        "app_name": "my_app",
        "user_id": "user_1",
        "state": {}
      }
    }
  ]
}
```

### Evaluation Criteria

**Default**:
- `tool_trajectory_avg_score`: 1.0 (100% match required)
- `response_match_score`: 0.8 (small margin allowed)

**Custom** (`test_config.json`):
```json
{
  "criteria": {
    "tool_trajectory_avg_score": 1.0,
    "response_match_score": 0.8
  }
}
```

### Running Evaluations

**Method 1: Web UI** (`adk web`):
1. Interact with agent to create session
2. Navigate to Eval tab
3. Click "Add current session" to save as eval case
4. Configure metrics with sliders
5. Click "Run Evaluation"
6. Analyze results (Pass/Fail, side-by-side comparison)
7. Use Trace tab for detailed debugging

**Method 2: pytest** (Programmatic):
```python
@pytest.mark.asyncio
async def test_agent():
    await AgentEvaluator.evaluate(
        agent_module="my_agent",
        eval_dataset_file_path_or_dir="tests/simple_test.test.json"
    )
```

**Method 3: CLI** (`adk eval`):
```bash
adk eval \
    path/to/agent \
    path/to/evalset.json \
    [--config_file_path=test_config.json] \
    [--print_detailed_results]
```

### Trace View (Debugging)

The Trace tab provides:
- Grouped traces by user message
- Interactive rows (hover highlights chat, click opens detail)
- Four detail tabs: Event, Request, Response, Graph
- Blue rows = event generated
- Visual representation of tool calls and agent flow

### Best Practices

**Before Evaluation**:
- Define success criteria
- Identify critical tasks
- Choose relevant metrics

**During Development**:
- Use test files for unit testing
- Run frequently during active development
- Use Trace tab to understand behavior

**For Production**:
- Use evalsets for integration testing
- Automate in CI/CD with pytest or CLI
- Track metrics over time
- Iterate based on failures

## References & URLs

All research notes above are based on official Google ADK documentation as of December 2024 / January 2025:

- Main Docs: https://google.github.io/adk-docs/
- Quickstart: https://google.github.io/adk-docs/get-started/quickstart/
- Function Tools: https://google.github.io/adk-docs/tools/function-tools/
- OpenAPI Tools: https://google.github.io/adk-docs/tools/openapi-tools/
- Sequential Agents: https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/
- Parallel Agents: https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/
- Loop Agents: https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/
- Session State: https://google.github.io/adk-docs/sessions/state/
- Memory Service: https://google.github.io/adk-docs/sessions/memory/
- Callbacks: https://google.github.io/adk-docs/callbacks/
- Callback Types: https://google.github.io/adk-docs/callbacks/types-of-callbacks/
- Callback Patterns: https://google.github.io/adk-docs/callbacks/design-patterns-and-best-practices/
- Evaluation: https://google.github.io/adk-docs/evaluate/
# Scratchpad

Notes from exploring Google ADK documentation and examples.

## ADK Overview

- **Google Agent Development Kit (ADK)**: Open-source Python framework for building, evaluating, and deploying AI agents
- **Modular Architecture**: Separates agents, tools, models, persistence, and orchestration layers
- **Key Components**:
  - Agents: BaseAgent subclasses (LlmAgent, SequentialAgent, ParallelAgent, LoopAgent)
  - Models: BaseLlm interface with Gemini (Google models) and LiteLLM (100+ providers)
  - Tools: BaseTool for extensions (OpenAPI, MCP, function tools)
  - Persistence: SessionService, ArtifactService, MemoryService
  - Orchestration: Runner class for execution

## Agent Types

- **LlmAgent**: LLM-powered agent for conversational interactions
- **SequentialAgent**: Executes tasks in sequence
- **ParallelAgent**: Runs tasks concurrently
- **LoopAgent**: Iterative execution with conditions
- **Multi-agent composition**: Combine multiple agents for complex workflows

## Tools Ecosystem

- **BaseTool**: Abstract base class for all tools
- **OpenAPI Tools**: Auto-generated from OpenAPI specifications
- **MCP Tools**: Model Context Protocol integration
- **Function Tools**: Python callable functions
- **Built-in Tools**: BigQuery, Spanner, and other Google Cloud services

## Model Integration

- **Gemini**: Native Google models with context caching
- **LiteLLM**: Support for 100+ LLM providers
- **Streaming**: Real-time response streaming
- **Context Caching**: Efficient token usage for repeated interactions

## Persistence & State Management

- **SessionService**: Conversation history and state
- **ArtifactService**: File and data handling
- **MemoryService**: RAG capabilities for knowledge retrieval
- **Pluggable Services**: Custom persistence implementations

## Orchestration & Execution

- **Runner Class**: Main execution engine
- **Invocation Contexts**: Runtime environment management
- **CLI Interface**: Command-line tools for development
- **Web UI**: Browser-based interface
- **FastAPI Server**: REST API for agent interactions

## Evaluation Framework

- **Metrics**: Performance measurement
- **LLM-as-judge**: Automated evaluation using LLMs
- **Test Sets**: Structured evaluation datasets
- **Quality Assurance**: Automated testing pipelines

## Deployment Options

- **Cloud Run**: Serverless deployment
- **Vertex AI Agent Engine**: Managed agent platform
- **GKE**: Kubernetes orchestration
- **Workflow**: Local testing → evaluation → production deployment

## Wiki Structure (13 Topics)

1. Overview - Introduction and getting started
2. Getting Started - Installation and basic setup
3. Agent System - Agent types and architecture
4. Tools - Tool ecosystem and integration
5. Models - LLM integration and configuration
6. Persistence - State management and storage
7. Orchestration - Workflow execution and coordination
8. Evaluation - Testing and quality assurance
9. Deployment - Production deployment options
10. Advanced Features - Streaming, telemetry, plugins
11. Configuration - Settings and environment management
12. Troubleshooting - Common issues and solutions
13. Contributing - Development and contribution guidelines

## Key Example Patterns

From GitHub repo exploration:

### Multi-Agent Example (hello_world_ma)

```python
# Agent with multiple tools
agent = LlmAgent(
    model=Gemini(model_name="gemini-1.5-flash"),
    instruction="You are a helpful assistant that can roll dice and check prime numbers.",
    tools=[roll_die_tool, check_prime_tool]
)

# Tool functions
def roll_die(sides: int) -> int:
    return random.randint(1, sides)

def check_prime(nums: list[int]) -> str:
    # Implementation for prime checking
```

### Workflow Examples

- **Sequential**: Step-by-step task execution
- **Parallel**: Concurrent tool calls
- **Loop**: Conditional iterative processing
- **Triage**: Agent routing and decision making

### Tool Integration

- **Function Tools**: Direct Python function calls
- **OpenAPI Tools**: REST API integration
- **MCP Tools**: Standardized tool protocol
- **Example Tools**: Few-shot learning demonstrations

### Caching & Performance

- Context caching for repeated interactions
- Memory services for knowledge persistence
- Artifact handling for file operations

## Practical Use Cases

- Conversational assistants with tool integration
- Data analysis and querying (BigQuery, Spanner)
- Workflow automation and orchestration
- Multi-agent collaborative systems
- Real-time streaming applications
- Knowledge retrieval and RAG systems

## Development Workflow

1. Define agent with instructions and tools
2. Test locally using CLI/Web UI
3. Evaluate performance with test sets
4. Deploy to production (Cloud Run/Vertex AI/GKE)
5. Monitor and iterate based on telemetry

## Key Insights

- ADK emphasizes modularity and separation of concerns
- Strong focus on evaluation and quality assurance
- Extensive tool ecosystem for real-world integrations
- Flexible deployment options from local to cloud
- Built-in support for advanced features like streaming and caching

## Advanced ADK Patterns & Concepts (from in-depth docs)

### Multi-Agent Orchestration & Hierarchy
- Agents can be composed hierarchically using the `sub_agents` argument; parent/child relationships are automatically managed.
- Single parent rule: an agent can only be a sub-agent of one parent.
- Hierarchies enable complex workflows and targeted delegation.

### Workflow Agents
- **SequentialAgent**: Runs sub-agents in strict order, passing shared state. Use for pipelines.
- **ParallelAgent**: Runs sub-agents concurrently, each with its own context branch but shared state. Use for fan-out/gather and speed.
- **LoopAgent**: Runs sub-agents in a loop until a condition is met or max iterations reached. Use for iterative refinement.
- Workflow agents are deterministic and do not use LLMs for orchestration logic.

### Communication Patterns
- **Shared Session State**: Agents communicate by writing/reading keys in `context.state`. `output_key` on LlmAgent auto-saves output.
- **LLM-Driven Delegation**: LlmAgent can dynamically transfer execution to another agent using `transfer_to_agent` function call.
- **Explicit Invocation (AgentTool)**: Wrap an agent as a tool and invoke it synchronously from another agent.

### Common Multi-Agent Patterns
- **Coordinator/Dispatcher**: Central LlmAgent routes requests to specialist sub-agents.
- **Sequential Pipeline**: SequentialAgent chains agents, passing state.
- **Parallel Fan-Out/Gather**: ParallelAgent runs tasks in parallel, then a gather agent combines results.
- **Hierarchical Task Decomposition**: Multi-level agent trees for breaking down complex tasks.
- **Generator-Critic (Review/Critique)**: SequentialAgent with generator and reviewer agents.
- **Iterative Refinement**: LoopAgent with agents that refine and check results until a stop condition.
- **Human-in-the-Loop**: Integrate human approval via custom tools or agent delegation.

### Artifacts
- Artifacts are versioned, named binary blobs (files, images, etc.) managed by an ArtifactService.
- Use `save_artifact` and `load_artifact` on context objects to persist and retrieve artifacts.
- Two main implementations: InMemoryArtifactService (dev/test) and GcsArtifactService (production/persistent).
- Artifacts are not stored in session state; they are referenced by filename and version.
- Namespacing: `user:` prefix for user-wide artifacts, otherwise session-scoped.

### Callback Design Patterns
- **Guardrails**: Use before/after callbacks to enforce policies, block requests, or validate data.
- **Dynamic State Management**: Read/write session state in callbacks for context-aware behavior.
- **Logging/Monitoring**: Add logs at key lifecycle points for observability.
- **Caching**: Serve cached results in before callbacks, store new results in after callbacks.
- **Request/Response Modification**: Alter LLM/tool requests or responses in callbacks.
- **Conditional Skipping**: Return a value from before callbacks to skip agent/LLM/tool execution.
- **Artifact Handling**: Save/load artifacts in callbacks for file/data workflows.

### Best Practices
- Use workflow agents for deterministic control flow; use LlmAgent for dynamic, LLM-driven logic.
- Prefer shared state for simple data passing; use artifacts for large/binary data.
- Always configure ArtifactService in Runner for artifact workflows.
- Design callbacks for single, focused purposes; handle errors gracefully.
- Test callbacks and agent flows thoroughly.

---

## ADDITIONAL FINDINGS (Oct 2025 Documentation)

### Modern ADK Pattern (2025)
- **Primary Class**: Use `Agent` (not `LlmAgent`) for modern code
- **Required Variable Name**: Must be `root_agent` in agent.py
- **Project Structure**: Canonical structure required for CLI tooling
  ```
  my_agent/
    ├── __init__.py      # Must contain: from . import agent
    ├── agent.py         # Must define: root_agent = Agent(...)
    └── .env             # Authentication credentials
  ```

### Modern Agent Definition
```python
from google.adk.agents import Agent

root_agent = Agent(
    name="agent_name",
    model="gemini-2.0-flash",  # Current recommended model
    description="Brief description",
    instruction="Detailed behavioral instructions",
    tools=[tool_func1, tool_func2]
)
```

### Tool Return Pattern (Best Practice)
```python
def tool_function(param: str) -> dict:
    """Clear docstring explaining the tool's purpose.
    
    Args:
        param: Description of parameter
        
    Returns:
        dict: Dictionary with 'status' and 'report' or 'error_message'
    """
    if success:
        return {"status": "success", "report": "result data"}
    else:
        return {"status": "error", "error_message": "what went wrong"}
```

### Running Agents (Modern Approach - NO Runner class needed)
1. **Dev UI**: `adk web` - Launch interactive browser interface
2. **CLI**: `adk run <agent_dir>` - Quick terminal interaction  
3. **API Server**: `adk api_server` - FastAPI production server

Note: The `Runner` class is now internal - use CLI commands instead!

### Authentication Setup
**For Google AI Studio (recommended for learning):**
```bash
# In .env file:
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_api_key_here
```

**For Vertex AI:**
```bash
# In .env file:
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_LOCATION=us-central1

# Then authenticate:
gcloud auth application-default login
```

### Current Model Recommendations
- **Standard**: `gemini-2.0-flash` or `gemini-2.5-flash`
- **Live/Streaming**: `gemini-2.0-flash-live-001`

### Evaluation Framework
- Test sets stored as JSON files (`.evalset.json`)
- Run with: `adk eval <agent_dir> <evalset_file>`
- Key metrics:
  - `tool_trajectory_avg_score`: Did agent use tools correctly?
  - `response_match_score`: Is final answer correct?

### Dev UI Features (Critical for Development)
- **Chat Tab**: Interactive conversation with agent
- **Events Tab**: Detailed execution trace showing:
  - All LLM prompts and responses
  - Tool calls and their results
  - Timing information
- **Trace Button**: Latency analysis for each operation
- **Audio Input**: Can enable microphone for voice interaction (with Live models)

### Key Differences from Older Examples
❌ OLD: `LlmAgent`, `Runner(agent).run()`, various model names
✅ NEW: `Agent`, `adk web/run/api_server`, `gemini-2.0-flash`

### FastAPI Integration Pattern
```python
from google.adk.cli.fast_api import get_fast_api_app

app = get_fast_api_app(agent_dir="./agents")

# Can add custom endpoints:
@app.get("/health")
async def health():
    return {"status": "ok"}
```

### CLI Commands Summary
- `adk web` - Dev UI (with auto-reload)
- `adk web --no-reload` - Dev UI without auto-reload (Windows)
- `adk run <agent_dir>` - Terminal interaction
- `adk api_server` - Start FastAPI server
- `adk eval <agent> <evalset>` - Run evaluations
- `adk deploy` - Deploy to cloud

### Important Conventions
- 2-space indentation (Google Python style)
- Always include: `from __future__ import annotations`
- Use relative imports in source code
- Use absolute imports in tests
- Tool functions should have comprehensive docstrings
- Return structured dicts from tools for consistency

---

## WORKFLOW AGENTS DEEP DIVE (Oct 2025 - Official Docs)

### SequentialAgent
**Source**: https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/
**Location**: `google.adk.agents.SequentialAgent`

**Purpose**: Execute sub-agents in strict, deterministic order
**Use Case**: When tasks MUST happen in sequence (write → review → refactor)

**Key Features**:
- NOT powered by LLM (deterministic execution)
- All sub-agents share same `InvocationContext`
- Shared session state (including `temp:` namespace)
- Data passing via `output_key` in agent definition

**Pattern**:
```python
from google.adk.agents import Agent, SequentialAgent

# Define agents with output_key for state passing
agent1 = Agent(
    name="step1",
    model="gemini-2.0-flash",
    instruction="Do X. Output: {format}",
    output_key="step1_result"  # Saves to state['step1_result']
)

agent2 = Agent(
    name="step2",
    model="gemini-2.0-flash",
    instruction="Process {step1_result}",  # Reads from state
    output_key="step2_result"
)

# Orchestrate
pipeline = SequentialAgent(
    name="Pipeline",
    sub_agents=[agent1, agent2]  # Strict order
)

root_agent = pipeline
```

**State Injection in Instructions**:
- Use `{state_key}` in instruction strings
- ADK automatically injects values from state
- Example: `{generated_code}` becomes value from `state['generated_code']`

**Best Practices**:
- Use for pipelines where order matters
- Each agent saves output with `output_key`
- Next agent reads from state using `{previous_key}`
- Deterministic, predictable execution

### ParallelAgent
**Source**: https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/
**Location**: `google.adk.agents.ParallelAgent`

**Purpose**: Execute sub-agents concurrently for speed
**Use Case**: Independent tasks that don't depend on each other (multi-source data gathering)

**Key Features**:
- All sub-agents start simultaneously
- Each runs in independent execution branch
- No automatic state sharing DURING execution
- Results collected after all complete
- Result order may not be deterministic

**Pattern**:
```python
from google.adk.agents import Agent, ParallelAgent, SequentialAgent

# Define independent research agents
researcher1 = Agent(
    name="topic1_researcher",
    model="gemini-2.0-flash",
    instruction="Research topic 1",
    tools=[google_search],
    output_key="topic1_result"
)

researcher2 = Agent(
    name="topic2_researcher", 
    model="gemini-2.0-flash",
    instruction="Research topic 2",
    tools=[google_search],
    output_key="topic2_result"
)

# Run in parallel
parallel_research = ParallelAgent(
    name="ParallelResearch",
    sub_agents=[researcher1, researcher2]
)

# Merge results sequentially
merger = Agent(
    name="merger",
    model="gemini-2.0-flash",
    instruction="Combine {topic1_result} and {topic2_result}",
)

# Combine parallel + sequential
pipeline = SequentialAgent(
    name="ResearchPipeline",
    sub_agents=[parallel_research, merger]  # Parallel first, then merge
)

root_agent = pipeline
```

**State Management**:
- Sub-agents CAN write to shared state via `output_key`
- But no coordination DURING execution
- Use merger agent AFTER to combine results

**Best Practices**:
- Use for independent, time-consuming tasks
- Combine with SequentialAgent for fan-out/gather pattern
- Each parallel agent should have `output_key`
- Add merger agent to synthesize results

**Common Pattern - Fan-Out/Gather**:
```
Sequential [
    Parallel [agent1, agent2, agent3],  # Fan-out
    MergerAgent                          # Gather
]
```

### Key Differences: Sequential vs Parallel

| Aspect | SequentialAgent | ParallelAgent |
|--------|----------------|---------------|
| **Execution** | One at a time, strict order | All at once, concurrent |
| **Use Case** | Order matters (pipeline) | Independent tasks (speed) |
| **State Sharing** | Automatic via shared context | Write only, merge after |
| **Speed** | Slower (sequential) | Faster (parallel) |
| **Determinism** | Fully deterministic order | Non-deterministic result order |

### Combining Workflow Agents

**Nested Composition**:
```python
# Parallel inside Sequential
SequentialAgent(
    sub_agents=[
        prep_agent,
        ParallelAgent(sub_agents=[task1, task2, task3]),
        merger_agent
    ]
)

# Sequential inside Parallel  
ParallelAgent(
    sub_agents=[
        SequentialAgent(sub_agents=[fetch, process]),
        SequentialAgent(sub_agents=[fetch2, process2])
    ]
)
```

### output_key Best Practice

**Define output_key on agents**:
```python
agent = Agent(
    name="processor",
    model="gemini-2.0-flash",
    instruction="Process data",
    output_key="processed_data"  # IMPORTANT: saves to state
)
```

**Access in next agent**:
```python
next_agent = Agent(
    name="reviewer",
    model="gemini-2.0-flash",
    instruction="Review: {processed_data}"  # IMPORTANT: reads from state
)
```

### Real-World Patterns

**Code Pipeline** (Sequential):
- Write → Review → Refactor → Test

**Research Pipeline** (Parallel + Sequential):
- Research A, B, C (parallel) → Merge Results (sequential)

**Data Processing** (Sequential):
- Extract → Transform → Load

**Multi-Source Lookup** (Parallel):
- Check DB1, DB2, DB3 simultaneously → Combine results

### Version Notes
- As of Oct 2025: Both SequentialAgent and ParallelAgent are stable
- Part of core `google.adk.agents` module
- Available in Python ADK v1.0+
- Documented at: https://google.github.io/adk-docs/agents/workflow-agents/
