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

---

## 🆕 ADVANCED FEATURES (Production-Ready)

**📋 RESEARCH STATUS: COMPREHENSIVE** - Deep source code research completed. 15+ critical production features documented below.

### Built-in Tools & Grounding

**Purpose**: Gemini 2.0+ models have built-in tools that execute **inside the model** (no local execution). These tools provide web grounding, code execution, and location-based information.

#### Google Search Tool

**Source**: `google/adk/tools/google_search_tool.py`

```python
from google.adk.tools import google_search
from google.adk.agents import Agent

# Simplest usage - model has web grounding
agent = Agent(
    model='gemini-2.0-flash',  # Requires Gemini 2.0+
    tools=[google_search]
)

# Agent can now search the web automatically
# Results integrated directly into model responses
```

**Key Details**:
- **Gemini 2.0+ only** - Raises error for 1.x models
- **No local execution** - All handled by model internally
- **Built-in grounding** - Model can search web for current information
- **GroundingMetadata** - Search results tracked in responses
- Temporarily stored in `temp:_adk_grounding_metadata` during invocation

#### Google Search Agent Tool (Workaround)

**Source**: `google/adk/tools/google_search_agent_tool.py`

```python
from google.adk.tools import GoogleSearchAgentTool, create_google_search_agent

# Workaround for using google_search with other tools
# TODO(b/448114567): Remove once workaround no longer needed
search_tool = GoogleSearchAgentTool()

agent = Agent(
    model='gemini-2.0-flash',
    tools=[search_tool, my_custom_tool]  # Can combine with other tools
)
```

**Why needed**: Built-in tools can't be used with custom tools directly. This wrapper creates a sub-agent with `google_search` and forwards results.

#### Google Maps Grounding Tool

**Source**: `google/adk/tools/google_maps_grounding_tool.py`

```python
from google.adk.tools import google_maps_grounding

agent = Agent(
    model='gemini-2.0-flash',  # Gemini 2.0+ only
    tools=[google_maps_grounding]
)

# Agent can now answer location-based queries
# "What's nearby?", "Directions to...", etc.
```

**Key Details**:
- **VertexAI API only** (not AI Studio)
- **Gemini 2.0+ only**
- Built-in location grounding
- Adds `types.Tool(google_maps=types.GoogleMaps())`

#### Enterprise Web Search Tool

**Source**: `google/adk/tools/enterprise_search_tool.py`

```python
from google.adk.tools import enterprise_web_search

agent = Agent(
    model='gemini-2.0-flash',  # Gemini 2+ only
    tools=[enterprise_web_search]
)

# For enterprise compliance web grounding
```

**Documentation**: https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/web-grounding-enterprise

### Built-in Planners

**Source**: `google/adk/planners/`

ADK provides planners that control how agents think and reason before taking actions.

#### BuiltInPlanner (Extended Thinking)

**Source**: `google/adk/planners/built_in_planner.py`

```python
from google.adk.planners import BuiltInPlanner
from google.genai import types

agent = Agent(
    model='gemini-2.0-flash',  # Requires Gemini 2.0+ with thinking support
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(
            include_thoughts=True  # Show reasoning to user
        )
    )
)

# Agent now does extended reasoning before responding
# Model thinks through problem, shows thought process
```

**Key Details**:
- Uses model's **native thinking capabilities** (Gemini 2.0+)
- `include_thoughts=True`: Shows reasoning in response
- `include_thoughts=False`: Hides reasoning (just final answer)
- Applied via `planner.apply_thinking_config(llm_request)`
- Only works with models supporting built-in thinking

#### PlanReActPlanner (Plan → Reason → Act)

**Source**: `google/adk/planners/plan_re_act_planner.py`

```python
from google.adk.planners import PlanReActPlanner

agent = Agent(
    model='gemini-2.0-flash',
    planner=PlanReActPlanner()
)

# Agent follows structured reasoning:
# 1. Generate PLAN (what steps to take)
# 2. Add REASONING (why these steps)
# 3. Take ACTION (execute tools)
# 4. OBSERVE results
# 5. REPLAN if needed
# 6. Repeat until FINAL_ANSWER
```

**Key Details**:
- Structured planning pattern
- Uses XML-like tags: `<PLANNING>`, `<REASONING>`, `<ACTION>`, `<FINAL_ANSWER>`
- Supports **replanning** - agent can adjust plan based on results
- Explicit reasoning steps injected into instructions
- `REPLANNING_TAG` for mid-execution plan changes

#### BasePlanner (Custom Planners)

**Source**: `google/adk/planners/base_planner.py`

```python
from google.adk.planners import BasePlanner

class MyCustomPlanner(BasePlanner):
    def build_planning_instruction(self, agent, context) -> str:
        """Return planning instructions to inject."""
        return "Custom planning approach..."
    
    def process_planning_response(self, response) -> LlmResponse:
        """Process and modify response based on planning."""
        return response
```

**Key Methods**:
- `build_planning_instruction`: Inject planning guidance
- `process_planning_response`: Post-process responses
- `apply_thinking_config`: Apply ThinkingConfig (BuiltInPlanner)

### Code Execution

**Source**: `google/adk/code_executors/built_in_code_executor.py`

```python
from google.adk.code_executors import BuiltInCodeExecutor

agent = Agent(
    model='gemini-2.0-flash',  # Requires Gemini 2.0+
    code_executor=BuiltInCodeExecutor()
)

# Agent can now:
# - Generate Python code
# - Execute it internally (in the model)
# - Use results in reasoning
```

**Key Details**:
- **Gemini 2.0+ only**
- **No local execution** - Code runs inside model environment
- Adds `types.Tool(code_execution=types.ToolCodeExecution())`
- Model generates + executes Python code
- Useful for: calculations, data processing, analysis
- Raises error for unsupported models

### Streaming (Server-Sent Events)

**Source**: `google/adk/agents/run_config.py`, `google/adk/models/google_llm.py`

```python
from google.adk.agents import RunConfig, StreamingMode, Runner

runner = Runner()

# Enable SSE streaming
run_config = RunConfig(streaming_mode=StreamingMode.SSE)

# Stream events as they arrive
async for event in runner.run_async(
    "Explain quantum computing",
    run_config=run_config
):
    print(event.content.parts[0].text, end='', flush=True)
```

**Key Details**:
- **StreamingMode.SSE** - Server-Sent Events (one-way)
- **StreamingMode.NONE** - Regular non-streaming
- **StreamingMode.BIDI** - Bidirectional (Live API)
- `StreamingResponseAggregator` handles partial/complete events
- Events marked as `partial=True` while streaming
- Final aggregated event sent at completion
- Available for all LLM models

### Live API (Bidirectional Streaming)

**Source**: `google/adk/agents/live_request_queue.py`, `google/adk/models/gemini_llm_connection.py`

**Documentation**: https://google.github.io/adk-docs/get-started/streaming/

```python
from google.adk.agents import LiveRequestQueue, RunConfig, StreamingMode, Runner
from google.genai import types

# Create live request queue
queue = LiveRequestQueue()

# Configure for live streaming
run_config = RunConfig(
    streaming_mode=StreamingMode.BIDI,
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name="Kore"
            )
        )
    ),
    response_modalities=["AUDIO"],  # or ["TEXT"], ["AUDIO", "TEXT"]
    enable_affective_dialog=True,  # Emotion detection
    proactivity=types.ProactivityConfig(
        proactive_response_generation=True
    )
)

agent = Agent(
    model='gemini-2.0-flash-live-preview-04-09',  # For Vertex
    # model='gemini-live-2.5-flash-preview',  # For AI Studio
    name='voice_assistant',
    instruction='You are a helpful voice assistant.'
)

runner = Runner()

# Start live streaming session
async for event in runner.run_live(queue, run_config):
    # Handle incoming events
    if event.content:
        print(event.content.parts[0].text)

# Send realtime audio/video
audio_blob = types.Blob(data=audio_bytes, mime_type='audio/pcm')
queue.send_realtime(blob=audio_blob)
```

**Key Details**:
- **Bidirectional streaming** - Agent and user both send/receive continuously
- **Audio input/output** - Voice conversations
- **Video streaming** - Camera input for visual analysis
- **Models**: 
  - Vertex: `gemini-2.0-flash-live-preview-04-09`
  - AI Studio: `gemini-live-2.5-flash-preview`
- **speech_config** - Voice configuration
- **response_modalities** - Output types (AUDIO, TEXT, or both)
- **enable_affective_dialog** - Emotion detection in voice
- **proactivity** - Agent can proactively respond
- **AudioTranscriptionConfig** - Transcribe audio to text
- **GeminiLlmConnection** - Manages live websocket session
- Multi-agent support - Audio converted to text for sub-agents

**Advanced RunConfig Options**:
```python
RunConfig(
    streaming_mode=StreamingMode.BIDI,
    
    # Audio output configuration
    speech_config=types.SpeechConfig(...),
    response_modalities=["AUDIO", "TEXT"],
    output_audio_transcription=True,  # Transcribe agent audio
    
    # Audio input configuration
    input_audio_transcription=types.AudioTranscriptionConfig(
        model="chirp2",
        language_codes=["en-US"]
    ),
    
    # Realtime input configuration (VAD)
    realtime_input_config=types.RealtimeInputConfig(
        automatic_activity_detection=types.AutomaticActivityDetection(
            disabled=False,  # Voice Activity Detection
            sensitivity=types.ActivityDetectionSensitivity.LOW
        )
    ),
    
    # Emotion and proactivity
    enable_affective_dialog=True,
    proactivity=types.ProactivityConfig(
        proactive_response_generation=True
    ),
    
    # Compositional Function Calling
    support_cfc=True
)
```

**Samples**:
- `contributing/samples/live_bidi_streaming_single_agent/`
- `contributing/samples/live_bidi_streaming_multi_agent/`
- `contributing/samples/live_bidi_streaming_tools_agent/`

### MCP (Model Context Protocol)

**Source**: `google/adk/tools/mcp_tool/`

**Documentation**: https://modelcontextprotocol.io/

```python
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams, StdioServerParameters

# Connect to MCP filesystem server
mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        command='npx',
        args=[
            '-y',
            '@modelcontextprotocol/server-filesystem',
            '/path/to/allowed/directory'
        ],
        server_params=StdioServerParameters(
            env={'NODE_ENV': 'production'}
        )
    )
)

agent = Agent(
    model='gemini-2.0-flash',
    tools=[mcp_tools]
)

# Agent now has file system access via MCP
# Can read, write, list files in allowed directory
```

**Key Details**:
- **MCP** - Model Context Protocol for standardized tool integration
- **MCPToolset** - Wrapper for MCP servers
- **StdioConnectionParams** - Connect to stdio-based MCP servers
- **Session pooling** - Reuses MCP sessions efficiently
- **McpTool** - Individual tool from MCP server
- **Authentication** - Supports credentials via headers
- Sample: `contributing/samples/mcp_stdio_server_agent/`

**Available MCP Servers**:
- `@modelcontextprotocol/server-filesystem` - File operations
- `@modelcontextprotocol/server-postgres` - Database access
- `@modelcontextprotocol/server-github` - GitHub API
- Many more at: https://github.com/modelcontextprotocol/servers

### A2A (Agent-to-Agent Communication)

**Source**: `google/adk/agents/remote_a2a_agent.py`

**Documentation**: https://github.com/google/adk-python/blob/main/a2a/README.md

```python
from google.adk.agents import RemoteA2aAgent, Agent
from google.adk.tools import AgentTool

# Define remote agent
remote_agent = RemoteA2aAgent(
    name='youtube_helper',
    base_url='https://youtube-agent.example.com'
)

# Use in local agent
agent = Agent(
    model='gemini-2.0-flash',
    tools=[AgentTool(remote_agent)]
)

# Agent can now call remote agent as a tool
```

**Agent Discovery** (Well-Known Path):
```python
from google.adk.agents import AGENT_CARD_WELL_KNOWN_PATH

# Remote agents publish "agent card" at:
# https://your-agent.com/.well-known/agent.json
print(AGENT_CARD_WELL_KNOWN_PATH)  # ".well-known/agent.json"
```

**Key Details**:
- **RemoteA2aAgent** - Represents remote agent
- **AGENT_CARD_WELL_KNOWN_PATH** - Standard discovery path
- **Authentication** - Supports auth between agents
- **Use cases**: Microservices, distributed agents, specialized services
- Sample: `contributing/samples/a2a_auth/` with YouTube tool
- Deploy with `adk deploy cloud_run --a2a`

### Events System

**Source**: `google/adk/events/event.py`, `google/adk/events/event_actions.py`

```python
from google.adk.events import Event, EventActions
from google.genai import types

# Create event with actions
event = Event(
    invocation_id='inv-123',
    author='my_agent',
    content=types.Content(
        role='model',
        parts=[types.Part.from_text('Processing complete')]
    ),
    actions=EventActions(
        state_delta={'result': 'success', 'count': 42},
        artifact_delta={'output.txt': 1},  # version 1
        transfer_to_agent='next_agent',
        escalate=True,
        skip_summarization=False
    )
)

# Events tracked in session history
# Available for debugging and observability
```

**EventActions Fields**:
- **state_delta** - State changes to apply
- **artifact_delta** - Artifact version changes
- **transfer_to_agent** - Hand off to another agent
- **escalate** - Signal completion (exit loop)
- **skip_summarization** - Don't summarize this event
- **requested_auth_configs** - Authentication requests
- **long_running_tool_ids** - Track async tool execution

**Key Details**:
- **Event** - Extends LlmResponse with metadata
- Used throughout agent execution flow
- Tracked in `session.events`
- Critical for observability and debugging
- Visible in adk web trace view

### Artifacts (File Handling)

**Source**: `google/adk/agents/callback_context.py`, `google/adk/tools/tool_context.py`

```python
from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google.genai import types

async def process_document(input_text: str, tool_context: ToolContext):
    """Process and save document as artifact."""
    
    # Save artifact
    version = await tool_context.save_artifact(
        filename='processed_doc.txt',
        part=types.Part.from_text(input_text.upper())
    )
    
    # Load artifact
    artifact = await tool_context.load_artifact(
        filename='processed_doc.txt',
        version=1  # or None for latest
    )
    
    # List all artifacts
    all_artifacts = await tool_context.list_artifacts()
    
    return f"Saved as version {version}, found {len(all_artifacts)} artifacts"

agent = Agent(
    model='gemini-2.0-flash',
    tools=[process_document]
)
```

**Key Details**:
- **save_artifact** - Save file/binary data with versioning
- **load_artifact** - Retrieve specific version
- **list_artifacts** - Get all artifact filenames
- **Version tracking** - Each save increments version
- **artifact_delta** - Track version changes in events
- Available in: `CallbackContext`, `ToolContext`
- Stored via `ArtifactService`

**Callback Context Usage**:
```python
from google.adk.agents import CallbackContext

async def on_agent_complete(context: CallbackContext):
    """Save results as artifact."""
    result = context.invocation_context.state.get('result')
    
    await context.save_artifact(
        'final_result.json',
        types.Part.from_text(result)
    )
```

### Agent Configuration (YAML)

**Source**: `google/adk/agents/agent_config.py`, `google/adk/agents/llm_agent_config.py`

**Schema**: `google/adk/agents/config_schemas/AgentConfig.json`

```yaml
# root_agent.yaml
# yaml-language-server: $schema=https://raw.githubusercontent.com/google/adk-python/refs/heads/main/src/google/adk/agents/config_schemas/AgentConfig.json

name: research_assistant
description: A helpful research assistant
instruction: |
  You are a research assistant that helps find and analyze information.
  Use search tools when needed.
model: gemini-2.0-flash

tools:
  - name: google_search  # Built-in ADK tool
  - name: my_library.my_tools.custom_search  # User-defined tool
  - name: my_library.my_tools.create_tool  # Factory function
    args:
      api_key: "${SEARCH_API_KEY}"  # From env

sub_agents:
  - name: fact_checker
    description: Verifies factual accuracy
    instruction: Check if claims are accurate using search
    model: gemini-2.0-flash
    tools:
      - name: google_search

flow: sequential  # or parallel, loop, single

generate_content_config:
  temperature: 0.7
  max_output_tokens: 2048
```

**Load Config Agent**:
```python
from google.adk.agents import config_agent_utils

# Load from YAML
root_agent = config_agent_utils.from_config("path/to/root_agent.yaml")

# Use like any agent
runner = Runner()
result = runner.run("Research quantum computing", agent=root_agent)
```

**Create Config Agent**:
```bash
# Create YAML-based agent
adk create --type=config my_agent

# Creates:
# my_agent/
#   __init__.py
#   root_agent.yaml
#   .env
```

**Key Details**:
- **AgentConfig** - YAML schema for agents
- **LlmAgentConfig** - Config for LLM agents
- Alternative to Python code-first approach
- Supports: tools, sub_agents, flows, config
- **Environment variable substitution**: `${VAR_NAME}`
- **Tool naming**:
  - Built-in: `name: google_search`
  - User-defined: `name: my.module.function`
  - Factory: `name: my.module.create` with `args:`
- Deployed via `adk deploy` (auto-detected)

### Image Generation & Multimodal

**Source**: `contributing/samples/generate_image/`, `contributing/samples/static_non_text_content/`

**Image Generation (Vertex AI)**:
```python
from google.genai import Client, types
from google.adk.tools import ToolContext

client = Client()  # Requires Vertex AI

async def generate_image(prompt: str, tool_context: ToolContext):
    """Generate image using Imagen."""
    
    response = client.models.generate_images(
        model='imagen-3.0-generate-001',
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio='1:1',
            safety_filter_level='block_some'
        )
    )
    
    # Save as artifact
    image_part = types.Part(
        inline_data=types.Blob(
            mime_type='image/png',
            data=response.generated_images[0].image.image_bytes
        )
    )
    
    await tool_context.save_artifact('generated.png', image_part)
    
    return "Image generated and saved"
```

**Multimodal Input**:
```python
from google.genai import types

# Image from bytes
image_part = types.Part(
    inline_data=types.Blob(
        mime_type='image/jpeg',
        data=image_bytes
    )
)

# Image from GCS
file_part = types.Part(
    file_data=types.FileData(
        file_uri='gs://bucket/image.jpg',
        mime_type='image/jpeg',
        display_name='Input Image'
    )
)

# Image from HTTPS URL
url_part = types.Part(
    file_data=types.FileData(
        file_uri='https://example.com/image.jpg',
        mime_type='image/jpeg'
    )
)

# Use in agent
agent = Agent(model='gemini-2.0-flash')
runner = Runner()
result = runner.run(
    types.Content(
        role='user',
        parts=[
            types.Part.from_text('Describe this image'),
            image_part
        ]
    ),
    agent=agent
)
```

**Key Details**:
- **Image generation**: Vertex AI only (Imagen models)
- **Multimodal input**: Images, audio, video, PDFs
- **Blob types**: `inline_data` (bytes) or `file_data` (URI)
- **MIME types**: `image/jpeg`, `image/png`, `audio/pcm`, `video/mp4`, `application/pdf`
- **response_modalities**: Control output types (TEXT, AUDIO)
- **Support**: Gemini 1.5+, Gemini 2.0+

### Model Selection Guide

**Source**: `google/adk/models/google_llm.py`, `google/adk/models/base_llm.py`

**Current Models (Oct 2025)**:

| Model | Purpose | Features |
|-------|---------|----------|
| `gemini-2.5-flash` | Default, fast | Latest, balanced speed/quality |
| `gemini-2.0-flash` | Production | Built-in tools, thinking, code exec |
| `gemini-2.0-flash-exp` | Experimental | Latest 2.0 features |
| `gemini-2.0-flash-live-preview-04-09` | Live API (Vertex) | Bidirectional streaming |
| `gemini-live-2.5-flash-preview` | Live API (AI Studio) | Bidirectional streaming |
| `gemini-1.5-flash` | Legacy fast | No built-in tools |
| `gemini-1.5-pro` | Legacy quality | No built-in tools |

**Feature Compatibility**:

| Feature | Requirements |
|---------|--------------|
| google_search | Gemini 2.0+ |
| google_maps_grounding | Gemini 2.0+, VertexAI |
| Code execution | Gemini 2.0+ |
| Thinking config | Gemini 2.0+ with thinking support |
| Live API (BIDI) | `gemini-2.0-flash-live-*` or `gemini-live-2.5-*` |
| Multimodal | Gemini 1.5+, Gemini 2.0+ |

**Model Selection**:
```python
# Fast, modern, all features
Agent(model='gemini-2.0-flash')

# Highest quality
Agent(model='gemini-2.0-pro')  # When available

# Live streaming
Agent(model='gemini-2.0-flash-live-preview-04-09')

# Specific version
Agent(model='gemini-2.0-flash-001')

# Custom LLM
from google.adk.models import Gemini

Agent(model=Gemini(
    model='gemini-2.0-flash',
    retry_options=types.HttpRetryOptions(
        initial_delay=1,
        attempts=2
    )
))
```

### Production Deployment

**Source**: `google/adk/cli/cli_deploy.py`, `google/adk/cli/adk_web_server.py`

**Local FastAPI Server**:
```bash
# Start local API server
adk api_server --port=8000 ./my_agent

# With UI
adk api_server --port=8000 --with_ui ./my_agent

# With services
adk api_server \
  --session_service_uri=postgresql://... \
  --artifact_service_uri=gs://bucket \
  --memory_service_uri=vertexai://project/location \
  --port=8000 \
  ./my_agent
```

**Cloud Run Deployment**:
```bash
# Deploy to Cloud Run
adk deploy cloud_run \
  --project=my-project \
  --region=us-central1 \
  --service_name=my-agent-service \
  --with_ui \
  ./my_agent

# With A2A support
adk deploy cloud_run \
  --project=my-project \
  --region=us-central1 \
  --service_name=my-agent-service \
  --a2a \
  ./my_agent
```

**Vertex AI Agent Engine**:
```bash
# Deploy to Agent Engine
adk deploy agent_engine \
  --project=my-project \
  --region=us-central1 \
  --staging_bucket=gs://my-bucket \
  --display_name="My Agent" \
  ./my_agent

# With custom requirements
adk deploy agent_engine \
  --project=my-project \
  --region=us-central1 \
  --staging_bucket=gs://my-bucket \
  --requirements_file=requirements.txt \
  --env_file=.env \
  ./my_agent
```

**Google Kubernetes Engine (GKE)**:
```bash
# Deploy to GKE
adk deploy gke \
  --project=my-project \
  --region=us-central1 \
  --cluster_name=my-cluster \
  --service_name=my-agent-service \
  --with_ui \
  ./my_agent
```

**Key Details**:
- **adk api_server** - Local development
- **adk deploy cloud_run** - Serverless deployment
- **adk deploy agent_engine** - Managed Vertex AI
- **adk deploy gke** - Kubernetes deployment
- **Dockerfile generation** - Automatic
- **deployment.yaml** - Auto-generated for GKE
- **Environment variables** - `.env` file support
- **Service URIs** - Session, artifact, memory services
- **--with_ui** - Include adk web UI
- **--a2a** - Enable A2A protocol
- **--trace_to_cloud** - Cloud Trace integration

**AdkWebServer (Custom FastAPI)**:
```python
from google.adk.cli.adk_web_server import AdkWebServer
from google.adk.cli.fast_api import get_fast_api_app

# Get FastAPI app
app = get_fast_api_app(agents_dir='./agents')

# Add custom routes
@app.get('/health')
async def health():
    return {'status': 'ok'}

# Run with uvicorn
import uvicorn
uvicorn.run(app, host='0.0.0.0', port=8000)
```

### Observability

**Source**: `google/adk/agents/run_config.py`, adk web UI

**Event Tracking**:
- All agent execution creates **Events**
- Events stored in `session.events`
- Tracks: inputs, outputs, tool calls, state changes
- Available in callbacks and trace view

**ADK Web Trace View**:
```bash
# Start with web UI
adk web ./my_agent

# Navigate to trace view after running agent
# 4 tabs available:
# - Event: Timeline of all events
# - Request: Full LLM requests
# - Response: Full LLM responses
# - Graph: Agent execution graph
```

**Cloud Trace Integration**:
```python
from vertexai.preview.reasoning_engines import AdkApp

adk_app = AdkApp(
    agent=root_agent,
    enable_tracing=True  # Enable Cloud Trace
)

# Or via CLI
adk deploy cloud_run --trace_to_cloud ./my_agent
```

**Plugin System**:
```python
# Custom observability plugin
from google.adk.plugins import BasePlugin

class MyMonitoringPlugin(BasePlugin):
    async def on_agent_start(self, context):
        # Log agent start
        pass
    
    async def on_agent_complete(self, context):
        # Log agent completion
        pass

# Use plugin
adk api_server --extra_plugins=my_module.MyMonitoringPlugin ./agents
```

**Key Details**:
- **Events** - Complete execution history
- **Trace View** - Visual debugging (4 tabs)
- **Cloud Trace** - Production monitoring
- **Plugins** - Extensible monitoring
- **State tracking** - State prefix visibility
- **Performance metrics** - Token usage, latency

---

## Version & Compatibility Notes

**Latest Research Date**: October 2025

**ADK Version**: 1.0+ (weekly releases)

**Installation**:
```bash
# Stable (recommended)
pip install google-adk

# Development (latest features)
pip install git+https://github.com/google/adk-python.git@main
```

**Source Code**: `research/adk-python/` (local copy for research)

**Official Documentation**: https://google.github.io/adk-docs/

**Feature Compatibility**:
- **Gemini 2.0+**: All advanced features (grounding, thinking, code exec, live API)
- **Gemini 1.5**: Basic features only (no built-in tools, no thinking)
- **VertexAI vs AI Studio**: Some features VertexAI-only (maps grounding, agent engine)
- **MCP**: Requires MCP-compatible servers
- **A2A**: Requires HTTP-accessible remote agents

**Experimental Features** (may change):
- YAML config agents (marked `@experimental`)
- Some Live API parameters
- New model versions

---

## 🔥 PHASE 3: NEW CRITICAL GAPS RESEARCH (2025-01-26)

### Research Summary (8 Concepts)

User identified 8 additional critical capabilities not yet covered in tutorials 01-25. Deep source code research completed across research/adk-python and research/ag-ui directories.

### 1. Multiple Tool Calling ✅ FOUND

**Status**: Fully implemented, native ADK feature

**Source**: `google/adk/flows/llm_flows/functions.py`

**Key Finding**: ADK executes multiple tool calls in PARALLEL automatically via `asyncio.gather()`

```python
# Internal ADK implementation
async def handle_function_call_list_async(
    invocation_context: InvocationContext,
    function_calls: list[types.FunctionCall],
    tools_dict: dict[str, BaseTool],
) -> Optional[Event]:
    """Calls multiple functions in parallel."""
    # Create tasks for ALL function calls
    tasks = [...]
    
    # Execute ALL simultaneously
    function_response_events = await asyncio.gather(*tasks)
    
    # Merge results
    merged_event = merge_parallel_function_response_events(
        function_response_events
    )
    return merged_event
```

**How It Works**:
1. Model generates multiple `FunctionCall` objects in single LLM response
2. ADK detects list of function calls
3. Creates async task for each call
4. Executes ALL simultaneously via `asyncio.gather()`
5. Waits for all to complete
6. Merges results into single event
7. Returns merged response to model

**User-Facing Pattern**:
```python
# Tools are called in parallel automatically
agent = Agent(
    model='gemini-2.0-flash',
    instruction="""
Use multiple tools simultaneously for faster responses.
For example, if asked about weather AND currency,
call both tools at once.
    """,
    tools=[get_weather, get_currency_rate, get_population]
)

# Query: "Weather in SF, EUR/USD rate, and Tokyo population"
# → All 3 tools called in parallel (~2s total, not ~6s sequential)
```

**Evidence**:
- `tests/unittests/tools/test_base_toolset.py`: Test multiple tools maintain correct declarations
- `contributing/samples/parallel_functions/agent.py`: Full working example with timing proof
- `research/ag-ui/typescript-sdk/.../agent-concurrent.test.ts`: Concurrent tool call tests

**Key Points**:
- ✅ No configuration needed - automatic
- ✅ Model decides when to make multiple calls
- ✅ Works with async tools only (`async def`)
- ✅ Error handling per tool (one failure doesn't stop others)
- ✅ Usage metadata tracked per tool
- ⚠️ Tools must be thread-safe if sharing state
- ⚠️ GIL-aware: Use `await asyncio.sleep()` not `time.sleep()`

**Tutorial Status**: Needs documentation (maybe extend Tutorial 02 or create advanced patterns tutorial)

---

### 2. Gemini 2.5 Flash/Pro Models ✅ FOUND

**Status**: Supported (DEFAULT MODEL!), needs documentation

**Source**: `google/adk/models/google_llm.py`

**Shocking Discovery**:
```python
class Gemini(BaseLlm):
    """Integration for Gemini models."""
    
    model: str = 'gemini-2.5-flash'  # <-- DEFAULT MODEL IN ADK!
```

**ADK already defaults to gemini-2.5-flash** but this is not documented anywhere in our tutorials!

**Evidence from Tests**:
```python
# tests/unittests/utils/test_model_name_utils.py
def test_is_gemini_2_model():
    assert is_gemini_2_model('gemini-2.5-pro') is True
    assert is_gemini_2_model('gemini-2.5-flash') is True
    
# tests/unittests/models/test_models.py  
'gemini-2.5-pro-preview'  # Listed as supported

# src/google/adk/cli/cli_create.py
def _prompt_for_model():
    """CLI defaults to gemini-2.5-flash"""
    ...
    return "gemini-2.5-flash"
```

**Model Detection**:
```python
def is_gemini_2_model(model_string: Optional[str]) -> bool:
    """Detects Gemini 2.x models (includes 2.0, 2.5, 2.9, etc.)"""
    model_name = extract_model_name(model_string)
    return re.match(r'^gemini-2\.\d+', model_name) is not None
```

**Usage Patterns**:
```python
# Simple (uses default 2.5-flash)
agent = Agent(model='gemini-2.5-flash')

# Via Gemini class (explicit)
from google.adk.models import Gemini
agent = Agent(model=Gemini(model='gemini-2.5-pro'))

# Via LiteLLM (Google AI Studio)
from google.adk.models import LiteLlm
agent = Agent(model=LiteLlm(model='gemini/gemini-2.5-pro'))

# Via LiteLLM (Vertex AI)
agent = Agent(model=LiteLlm(model='vertex_ai/gemini-2.5-flash'))
```

**Documentation Gap**:
- Tutorial 22 (Model Selection) only documents 2.0 and 1.5 models
- No mention of 2.5 capabilities, differences, or availability
- Need official Google AI documentation for 2.5 features

**Action Items**:
- [ ] Web search for official Gemini 2.5 documentation
- [ ] Update Tutorial 22 with 2.5 models section
- [ ] Document 2.5 vs 2.0 differences (if any)
- [ ] Update model comparison matrix
- [ ] Clarify availability (preview vs GA)

---

### 3. AG-UI Protocol ✅ FOUND

**Status**: Full protocol implementation in research/ag-ui/, official ADK partnership

**Source**: `research/ag-ui/` directory (complete TypeScript and Python SDK)

**What is AG-UI?**
> "An open, lightweight, event-based protocol that standardizes how AI agents connect to user-facing applications."

From `research/ag-ui/README.md`:
- Event-based protocol (~16 standard event types)
- Works with ANY event transport (SSE, WebSockets, webhooks)
- Flexible middleware for compatibility
- Official partnerships: LangGraph, CrewAI, **Google ADK**

**The Agent Protocol Stack**:
```
┌─────────────────────────────────────────┐
│  AG-UI Protocol                         │  ← Agent ↔ User Interface
│  (Brings agents to applications)       │
├─────────────────────────────────────────┤
│  A2A Protocol                           │  ← Agent ↔ Agent
│  (Covered in Tutorial 17)              │
├─────────────────────────────────────────┤
│  MCP Protocol                           │  ← Agent ↔ Tools
│  (Covered in Tutorial 16)              │
└─────────────────────────────────────────┘
```

**Key AG-UI Features**:
1. 💬 Real-time agentic chat with streaming
2. 🔄 Bi-directional state synchronization
3. 🧩 Generative UI and structured messages
4. 🧠 Real-time context enrichment
5. 🛠️ Frontend tool integration
6. 🧑‍💻 Human-in-the-loop collaboration

**Core AG-UI Events**:
- `RUN_STARTED` - Agent execution begins
- `TEXT_MESSAGE_CONTENT` - Streaming text (delta)
- `TOOL_CALL_START` - Tool invocation begins
- `TOOL_CALL_ARGS` - Tool arguments (streaming)
- `TOOL_CALL_END` - Tool execution complete
- `RUN_FINISHED` - Agent execution ends
- ~10 more event types

**ADK Integration**:
```
Location: research/ag-ui/typescript-sdk/integrations/adk-middleware/
Status: ✅ Officially supported (Partnership)
Documentation: https://docs.copilotkit.ai/adk (redirects to docs.ag-ui.com)
Demos: https://dojo.ag-ui.com/adk-middleware
```

**Python ADK Middleware** (from research/ag-ui):
```python
# ADK agent emits AG-UI compatible events
async for event in adk_agent.run(user_input):
    # Events: RUN_STARTED, TOOL_CALL_START, TEXT_MESSAGE_CONTENT, etc.
    yield event
```

**Why AG-UI Matters for ADK**:
- Standardizes ADK agent ↔ UI communication
- Works with React, Vue, Svelte, vanilla JS frontends
- Enables rich UI interactions (progress bars, forms, generative UI)
- Human-in-the-loop patterns built-in
- Interoperability with LangGraph, CrewAI agents

**GitHub**: https://github.com/ag-ui-protocol/ag-ui
**Issue #103**: https://github.com/ag-ui-protocol/ag-ui/issues/103 (user requested research)

**Action Items**:
- [ ] Read AG-UI docs in research/ag-ui/docs/
- [ ] Review ADK middleware code
- [ ] Test AG-UI demos
- [ ] Create Tutorial 26: AG-UI Protocol Integration
- [ ] Document event types and usage patterns

---

### 4. MCP OAuth Authentication ✅ FOUND

**Status**: Fully implemented and tested, needs tutorial documentation

**Source**: `google/adk/tools/mcp_tool/mcp_tool.py`, `tests/unittests/tools/mcp_tool/test_mcp_tool.py`

**Key Finding**: MCP tools support OAuth2, HTTP Bearer, Basic Auth, API Keys

**McpTool Implementation**:
```python
class McpTool(BaseAuthenticatedTool):
    """MCP tool with authentication support."""
    
    def __init__(
        self,
        *,
        mcp_tool: McpBaseTool,
        mcp_session_manager: MCPSessionManager,
        auth_scheme: Optional[AuthScheme] = None,
        auth_credential: Optional[AuthCredential] = None,
    ):
        # Supports OAuth2, API Key, HTTP auth
        ...
    
    async def _get_headers(
        self, tool_context: ToolContext, credential: AuthCredential
    ) -> Optional[dict[str, str]]:
        """Generate authentication headers for MCP session."""
        
        if credential.oauth2:
            # OAuth2 Bearer token
            return {"Authorization": f"Bearer {credential.oauth2.access_token}"}
        
        elif credential.http:
            if credential.http.scheme.lower() == "bearer":
                # HTTP Bearer
                return {"Authorization": f"Bearer {credential.http.credentials.token}"}
            elif credential.http.scheme.lower() == "basic":
                # HTTP Basic Auth
                credentials = f"{username}:{password}"
                encoded = base64.b64encode(credentials.encode()).decode()
                return {"Authorization": f"Basic {encoded}"}
        
        elif credential.api_key:
            # API Key (header-based only)
            return {auth_scheme.name: credential.api_key}
        
        return None
```

**Supported Auth Methods**:
1. ✅ **OAuth2** - Access tokens
2. ✅ **HTTP Bearer** - Bearer tokens
3. ✅ **HTTP Basic** - Username/password
4. ✅ **API Key** - Header-based only (not query/cookie)

**OAuth2 Example**:
```python
from google.adk.tools.mcp_tool import MCPToolset, StdioConnectionParams
from google.adk.auth import AuthCredential, AuthCredentialTypes, OAuth2Auth
from fastapi.openapi.models import OAuth2

# Define OAuth2 scheme
auth_scheme = OAuth2(flows={
    'clientCredentials': {
        'tokenUrl': 'https://api.example.com/token',
        'scopes': {'read': 'Read access'}
    }
})

# Provide access token
auth_credential = AuthCredential(
    auth_type=AuthCredentialTypes.OAUTH2,
    oauth2=OAuth2Auth(access_token="ya29.a0AfH6...")
)

# Create authenticated MCP toolset
github_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        command='npx',
        args=['-y', '@modelcontextprotocol/server-github']
    ),
    auth_scheme=auth_scheme,
    auth_credential=auth_credential
)

agent = Agent(
    model='gemini-2.0-flash',
    tools=[github_tools]  # Authenticated MCP tools
)
```

**OAuth Flows Supported** (from samples):
```
contributing/samples/oauth2_client_credentials/oauth2_test_server.py:
- ✅ Client Credentials flow
- ✅ Authorization Code flow  
- ✅ Token refresh
- ✅ OIDC discovery (/.well-known/openid_configuration)
- ✅ Token validation
```

**Test Coverage**:
```python
# tests/unittests/tools/mcp_tool/test_mcp_tool.py
def test_init_with_auth():
    """Test MCP tool initialization with OAuth2."""
    
def test_run_async_impl_with_oauth2():
    """Test running tool with OAuth2 authentication."""
    
def test_get_headers_oauth2():
    """Test header generation for OAuth2 credentials."""
    
def test_get_headers_http_bearer():
    """Test header generation for HTTP Bearer."""
    
def test_run_async_impl_with_api_key_header_auth():
    """Test API key header authentication end-to-end."""
```

**Current Documentation**:
- Tutorial 16 covers basic MCP (no authentication)
- OAuth implementation exists in samples but not explained

**Action Items**:
- [ ] Extend Tutorial 16 with "MCP Authentication" section
- [ ] Document OAuth2 client credentials flow
- [ ] Document OAuth2 authorization code flow
- [ ] Add examples for Bearer tokens, API keys
- [ ] Troubleshooting: common OAuth errors

---

### 5. AgentSpace ✅ FOUND - GOOGLE CLOUD PLATFORM

**Status**: NOT an ADK feature - separate Google Cloud product for enterprise AI agent management

**Source**: https://cloud.google.com/products/agentspace?hl=en

**What is Google AgentSpace?**
> "Google Agentspace provides a single, secure platform to build, manage, and adopt AI agents at scale and unlock the potential of individuals, teams, and entire enterprises."

**Key Clarification**: 
- ❌ AgentSpace is NOT a class/module in ADK source code
- ✅ AgentSpace is a Google Cloud PLATFORM for managing AI agents
- 🔗 Relationship: ADK builds agents → AgentSpace manages/governs/deploys agents

**Pricing**: Enterprise editions start at $25 USD per seat per month

**Core Capabilities**:

1. **Pre-built Google Agents** (Ready-to-use experts):
   - **Idea Generation**: Uses hundreds of AI agents to generate and refine innovative ideas with comprehensive reports
   - **Deep Research**: Performs hundreds of searches across web and enterprise data, generates comprehensive research reports
   - **NotebookLM Enterprise**: Document synthesis and insights with enhanced security/privacy for work

2. **Agent Designer** (Low-code builder):
   - Empowers functional teams to be "agent builders"
   - Turn domain knowledge into automated workflows
   - Build custom agents without coding

3. **Agent Gallery** (Discovery & sharing):
   - Marketplace for agent assets
   - Discover pre-built agents
   - Share custom agents across organization

4. **Agent Orchestration & Governance**:
   - Centralized agent management
   - Enterprise-level security and compliance
   - Agent threat management
   - Secure-by-design infrastructure

5. **Data Connectors** (Out-of-box integrations):
   - SharePoint, Google Drive, OneDrive
   - HubSpot, Adobe Experience Manager (AEM)
   - CMS, custom data sources
   - Seamless access to enterprise data

**AgentSpace + ADK Integration Pattern**:
```
┌─────────────────────────────────────────────────┐
│              GOOGLE AGENTSPACE                  │
│         (Enterprise Management Platform)        │
│                                                 │
│  ┌─────────────┐  ┌────────────┐  ┌──────────┐│
│  │ Pre-built   │  │ Custom ADK │  │ 3rd-party││
│  │ Google      │  │ Agents     │  │ Agents   ││
│  │ Agents      │  │ (Built w/  │  │          ││
│  │             │  │ ADK SDK)   │  │          ││
│  └─────────────┘  └────────────┘  └──────────┘│
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ Governance, Security, Orchestration      │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
         ↓                    ↑
    Deploy ADK           Manage agents
    agents here          at enterprise scale
```

**Use Cases by Team**:

**Marketing**:
- Generate blogs and social posts in brand voice
- Summarize industry/competitor news into audio
- Analyze customer feedback for content needs
- Connect to: SharePoint, Google Drive, CMS, HubSpot

**Sales**:
- Create personalized messages and offers
- Product recommendations based on customer data
- Access CRM and sales tools

**Engineering**:
- Technical research assistance
- Documentation generation
- Code analysis support

**HR**:
- Employee assistance agents
- Policy query handling
- Onboarding automation

**How ADK Agents Fit In**:
```python
# 1. Build agent with ADK
from google.adk import Agent

custom_agent = Agent(
    name="sales_assistant",
    model="gemini-2.0-flash",
    instruction="Help sales team with customer research...",
    tools=[crm_tool, email_tool, calendar_tool]
)

# 2. Deploy to AgentSpace
# - Via Agent Engine
# - With governance policies
# - Available in Agent Gallery
# - Managed centrally with security

# 3. Team uses agent
# - Discovered in Agent Gallery
# - Governed by enterprise policies
# - Integrated with existing tools
# - Monitored and audited
```

**Key Benefits of AgentSpace**:
- ✅ Secure by design (Google Cloud infrastructure)
- ✅ Enterprise governance and compliance
- ✅ Agent discovery and sharing
- ✅ Out-of-box and custom connectors
- ✅ Works with ADK and other frameworks
- ✅ Centralized management at scale

**Documentation Resources**:
- Main: https://cloud.google.com/products/agentspace
- FAQ: https://cloud.google.com/products/agentspace/faq
- Enterprise Docs: https://cloud.google.com/agentspace/agentspace-enterprise/docs/

**Action Items**:
- [ ] Create Tutorial 26: Google AgentSpace
- [ ] Document ADK → AgentSpace deployment pattern
- [ ] Explain governance and enterprise features
- [ ] Cover Agent Designer for non-developers
- [ ] Highlight pre-built Google agents

**ACTION REQUIRED**: **Ask user for clarification** - What is "AgentSpace"? Can they provide:
- What feature they're referring to?
- Where they saw this term?
- What functionality they expect?

---

### 6. ADK Builtin Tools (Comprehensive) ✅ COMPLETE LIST

**Status**: All builtin tools identified and categorized

**Source**: `google/adk/tools/__init__.py`, tool files

**COMPLETE INVENTORY (30+ tools)**:

#### Category A: Grounding Tools (Model Built-ins)
```python
from google.adk.tools import (
    google_search,              # Web search grounding (Gemini 2.0+)
    google_maps_grounding,      # Location grounding (Gemini 2.0+, VertexAI)
    enterprise_web_search,      # Enterprise compliance search (Gemini 2.0+)
)
```
**Requirements**: Gemini 2.0+, maps requires VertexAI

#### Category B: Memory & Artifacts
```python
from google.adk.tools import (
    load_memory,      # Load conversation history into context
    preload_memory,   # Preload memory at agent initialization
    load_artifacts,   # Retrieve saved artifacts by ID
)
```

#### Category C: Workflow Control
```python
from google.adk.tools import (
    exit_loop,              # Exit LoopAgent early with result
    get_user_choice,        # Present options, get user choice
    transfer_to_agent,      # Hand off conversation to another agent
)
```

#### Category D: Context Enrichment
```python
from google.adk.tools import (
    url_context,  # Fetch and process web page content
)
```

#### Category E: Enterprise Search
```python
from google.adk.tools import (
    VertexAiSearchTool,         # Vertex AI Search datastore integration
    DiscoveryEngineSearchTool,  # Legacy discovery engine (deprecated)
)
```
**Usage**:
```python
search = VertexAiSearchTool(
    data_store_id='projects/.../dataStores/my-store'
)
agent = Agent(tools=[search])
```

#### Category F: Integration Wrappers
```python
from google.adk.tools import (
    GoogleSearchAgentTool,  # Wrapper for google_search as regular tool
                            # (allows mixing with custom tools)
)
```

#### Category G: Tool Classes
```python
from google.adk.tools import (
    FunctionTool,            # Wrap Python function as tool
    AgentTool,               # Wrap agent as tool (sub-agent pattern)
    LongRunningFunctionTool, # Tools requiring user interaction/approval
    ExampleTool,             # Few-shot examples for tool usage
    BaseTool,                # Base class for custom tools
)
```

#### Category H: Toolsets (Collections)
```python
from google.adk.tools import (
    MCPToolset,       # Model Context Protocol servers
    OpenAPIToolset,   # REST APIs from OpenAPI/Swagger spec
    APIHubToolset,    # Google API Hub integrations
    ToolboxToolset,   # Google Cloud Toolbox
)
```

#### Category I: Framework Integrations
```python
from google.adk.tools import (
    CrewaiTool,  # Wrap CrewAI tools for ADK
)
```

#### Category J: Specialized
```python
from google.adk.tools import (
    SetModelResponseTool,  # Structured output validation tool
    ToolContext,           # Execution context for tools
)
```

**Tutorial 11 Current Coverage**:
- ✅ google_search
- ✅ google_maps_grounding
- ✅ enterprise_web_search
- ❌ Memory tools (load_memory, preload_memory, load_artifacts)
- ❌ Workflow tools (exit_loop, get_user_choice, transfer_to_agent)
- ❌ VertexAiSearchTool
- ❌ url_context
- ❌ GoogleSearchAgentTool patterns

**Action Items**:
- [ ] Extend Tutorial 11 with all tool categories
- [ ] Add examples for each tool type
- [ ] Document use cases and constraints
- [ ] Create quick reference table

---

### 7. Framework Integrations ✅ FOUND

**Status**: Integrations via AG-UI Protocol + Native CrewAI wrapper

**Key Finding**: ADK integrates with frameworks through **TWO approaches**:

#### Approach 1: AG-UI Protocol (Primary Integration Layer)

**Architecture**:
```
┌──────────────────────────────────────────────┐
│  Frontend (React, Vue, Svelte, vanilla JS)  │
├──────────────────────────────────────────────┤
│  AG-UI Protocol (Event Stream)              │  ← Standardized events
├────────────┬─────────────┬──────────────────┤
│  ADK Agent │ LangGraph   │  CrewAI Flow     │  ← Any framework
└────────────┴─────────────┴──────────────────┘
```

AG-UI acts as the **interoperability layer** - all frameworks emit AG-UI events that frontends understand.

**LangGraph Integration** (Official Partnership):
```typescript
// research/ag-ui/typescript-sdk/integrations/langgraph/
import { LangGraphAgent } from '@ag-ui/langgraph'

const agent = new LangGraphAgent({
  deploymentUrl: 'http://localhost:8000',
  graphId: 'my_graph'
})

// Emits AG-UI events compatible with ADK frontends
await agent.run({ messages: [...] })
```

**CrewAI Integration** (Official Partnership):
```python
# research/ag-ui/typescript-sdk/integrations/crewai/python/
from ag_ui_crewai import Flow, CopilotKitState

class MyFlow(Flow[CopilotKitState]):
    @start()
    async def chat(self):
        # CrewAI flow emits AG-UI events
        response = await copilotkit_stream(
            completion(
                model="openai/gpt-4o",
                messages=self.state.messages,
                tools=self.state.copilotkit.actions,
            )
        )
```

**LangChain** (Via AG-UI):
- Examples exist in AG-UI repository
- Uses LangChain LLMs/chains
- Wraps with AG-UI event emission

#### Approach 2: Native Tool Wrapping

**CrewaiTool** (ADK Direct):
```python
from google.adk.tools import CrewaiTool
from crewai_tools import SomeTool as CrewaiBaseTool

# Wrap CrewAI tool for ADK agent
adk_tool = CrewaiTool(
    tool=CrewaiBaseTool(),
    name='crewai_search',
    description='Search using CrewAI tool'
)

agent = Agent(
    model='gemini-2.0-flash',
    tools=[adk_tool]  # CrewAI tool usable in ADK
)
```

**Integration Status**:
- ✅ **LangGraph**: Official support via AG-UI
- ✅ **CrewAI**: Official support via AG-UI + native tool wrapper
- 🔄 **LangChain**: Community integration via AG-UI
- ✅ **Mastra**: Supported via AG-UI
- ✅ **Pydantic AI**: Supported via AG-UI
- ✅ **LlamaIndex**: Supported via AG-UI
- ✅ **AG2** (formerly AutoGen): Supported via AG-UI

**Key Insight**: ADK doesn't directly integrate with LangGraph/CrewAI. Instead:
1. All frameworks adopt AG-UI protocol
2. Emit standardized events
3. Work with any AG-UI-compatible frontend
4. ADK agents can call LangGraph/CrewAI via RemoteA2aAgent if exposed via HTTP

**Action Items**:
- [ ] Document AG-UI as integration layer
- [ ] Show ADK ↔ LangGraph via AG-UI
- [ ] Show ADK ↔ CrewAI via AG-UI
- [ ] Explain event standardization
- [ ] Create Tutorial 27: Framework Integrations

---

### 8. Using Other LLMs via LiteLLM ✅ COMPLETE SUPPORT

**Status**: Full support for ANY LLM via LiteLLM, samples exist

**Source**: `google/adk/models/lite_llm.py`, samples in `contributing/samples/`

**Key Finding**: ADK supports **any LiteLLM provider** - OpenAI, Anthropic, Azure, Ollama, AWS Bedrock, etc.

**LiteLlm Class**:
```python
class LiteLlm(BaseLlm):
    """Wrapper around litellm library.
    
    Supports ANY model from litellm.
    Environment variables for authentication must be set.
    """
    
    model: str  # LiteLLM model string (e.g., 'openai/gpt-4o')
    llm_client: LiteLLMClient = Field(default_factory=LiteLLMClient)
    
    async def generate_content_async(self, llm_request, stream=False):
        # Delegates to litellm.acompletion()
        return await self.llm_client.acompletion(
            model=self.model,
            messages=messages,
            tools=tools,
            **self._additional_args
        )
```

**Supported Providers**:

#### A. OpenAI
```python
from google.adk.models import LiteLlm

agent = Agent(
    model=LiteLlm(model='openai/gpt-4o'),
    tools=[...]
)
```
**Requires**: `OPENAI_API_KEY` environment variable

#### B. Anthropic Claude
```python
agent = Agent(
    model=LiteLlm(model='anthropic/claude-3-sonnet-20240229'),
    tools=[...]
)
```
**Requires**: `ANTHROPIC_API_KEY`

#### C. Claude via Vertex AI
```python
agent = Agent(
    model=LiteLlm(model='vertex_ai/claude-3-7-sonnet@20250219'),
    tools=[...]
)
```
**Requires**: `VERTEXAI_PROJECT`, `VERTEXAI_LOCATION`

#### D. Ollama (Local Models)
```python
agent = Agent(
    model=LiteLlm(model='ollama_chat/mistral-small3.1'),
    tools=[...]
)
```
**Requires**: `OLLAMA_API_BASE=http://localhost:11434`
⚠️ **CRITICAL**: Use `ollama_chat` provider (not `ollama`) to avoid infinite tool call loops

#### E. Azure OpenAI
```python
agent = Agent(
    model=LiteLlm(model='azure/gpt-4'),
    tools=[...]
)
```
**Requires**: `AZURE_API_KEY`, `AZURE_API_BASE`, `AZURE_API_VERSION`

**Working Examples**:
```
contributing/samples/hello_world_litellm/agent.py:
- OpenAI GPT-4o
- Anthropic Claude
- Vertex AI Claude

contributing/samples/hello_world_ollama/agent.py:
- Ollama local models
- Proper provider usage (ollama_chat)
```

**Important Notes**:
- ⚠️ **Gemini via LiteLLM discouraged** - Use native `Gemini` class for better integration
- ⚠️ **Ollama provider**: Always use `ollama_chat` (not `ollama`) to avoid issues
- ⚠️ **Environment variables**: Must be set BEFORE creating agent
- ✅ Tool calling works across all providers
- ✅ Streaming supported for all providers
- ✅ Function calling translated automatically

**LiteLLM Warning** (from code):
```python
def _warn_gemini_via_litellm(model_string: str):
    """Warn users to use native Gemini class instead of LiteLLM."""
    if _is_litellm_gemini_model(model_string):
        warnings.warn(
            f"Using Gemini model '{model_string}' via LiteLLM. "
            "Consider using google.adk.models.Gemini for better integration.",
            UserWarning
        )
```

**Tutorial 22 Gap**:
- Only covers Gemini family models
- No mention of LiteLLM or other providers
- Missing OpenAI, Claude, Ollama documentation

**Action Items**:
- [ ] Create Tutorial 28: Using Other LLMs with ADK
- [ ] Document OpenAI integration (GPT-4, GPT-3.5)
- [ ] Document Ollama for local models
- [ ] Document Azure OpenAI setup
- [ ] Document Anthropic Claude
- [ ] Document AWS Bedrock (if supported via LiteLLM)
- [ ] Provider-specific troubleshooting
- [ ] Environment variable reference

---

### 9. Third-Party Framework Tools ✅ OFFICIAL DOCUMENTATION FOUND

**Status**: Native support via LangchainTool and CrewaiTool wrappers

**Source**: https://google.github.io/adk-docs/tools/third-party-tools/

**Key Finding**: ADK provides official wrappers to integrate tools from LangChain and CrewAI ecosystems directly into ADK agents

#### LangChain Tools Integration

**Source**: `google/adk/tools/langchain_tool.py`

**Pattern**:
```python
from google.adk.tools.langchain_tool import LangchainTool
from langchain_community.tools import TavilySearchResults

# 1. Instantiate LangChain tool
tavily_tool = TavilySearchResults(
    max_results=5,
    search_depth="advanced",
    include_answer=True,
    include_raw_content=True,
    include_images=True,
)

# 2. Wrap with LangchainTool
adk_tavily_tool = LangchainTool(tool=tavily_tool)

# 3. Add to ADK agent
my_agent = Agent(
    name="langchain_tool_agent",
    model="gemini-2.0-flash",
    description="Agent to answer questions using TavilySearch.",
    instruction="I can answer your questions by searching the internet.",
    tools=[adk_tavily_tool]  # LangChain tool now usable in ADK!
)
```

**Installation**:
```bash
pip install langchain_community tavily-python
export TAVILY_API_KEY=your_api_key
```

**How it works**:
- `LangchainTool` wraps any LangChain tool
- Converts LangChain tool schema to ADK tool schema
- Handles tool execution and result marshaling
- Supports all LangChain tool features (async, streaming, etc.)

**Available LangChain Tools**: 100+ tools including:
- TavilySearchResults (web search)
- DuckDuckGoSearchRun (search)
- WikipediaQueryRun (Wikipedia)
- ArxivQueryRun (academic papers)
- PubmedQueryRun (medical research)
- GoogleSerperRun (Google search via Serper API)
- BraveSearchRun (Brave search)
- And many more...

#### CrewAI Tools Integration

**Source**: `google/adk/tools/crewai_tool.py`

**Pattern**:
```python
from google.adk.tools.crewai_tool import CrewaiTool
from crewai_tools import SerperDevTool

# 1. Instantiate CrewAI tool
serper_tool = SerperDevTool(
    n_results=10,
    save_file=False,
    search_type="news",
)

# 2. Wrap with CrewaiTool (MUST provide name and description!)
adk_serper_tool = CrewaiTool(
    name="InternetNewsSearch",
    description="Searches the internet specifically for recent news articles using Serper.",
    tool=serper_tool
)

# 3. Add to ADK agent
my_agent = Agent(
    name="crewai_search_agent",
    model="gemini-2.0-flash",
    description="Agent to find recent news using the Serper search tool.",
    instruction="I can find the latest news for you. What topic are you interested in?",
    tools=[adk_serper_tool]  # CrewAI tool now usable in ADK!
)
```

**Installation**:
```bash
pip install crewai-tools
export SERPER_API_KEY=your_api_key
```

**CRITICAL**: Must provide `name` and `description` to CrewaiTool wrapper (ADK needs these for tool selection)

**Available CrewAI Tools**:
- SerperDevTool (Google search via Serper)
- FileReadTool (read files)
- DirectoryReadTool (read directories)
- CodeInterpreterTool (execute code)
- WebsiteSearchTool (search websites)
- ScrapeWebsiteTool (scrape web content)
- And many more...

#### Integration Approach Comparison

**Option 1: Native Tool Wrappers** (LangchainTool, CrewaiTool)
```
✅ Direct tool integration in ADK agent
✅ Simple Python code
✅ Best for: Single tools, development, testing
❌ Limited to tool-level integration
```

**Option 2: AG-UI Protocol** (Framework-level integration)
```
✅ Full framework interoperability
✅ Event-based communication
✅ Best for: Frontend integration, multi-framework systems
✅ Production-ready for complex UIs
```

#### When to Use What

**Use LangchainTool/CrewaiTool when**:
- Need specific tools from these ecosystems
- Building pure Python ADK agents
- Want direct tool access without extra infrastructure
- Testing/development phase

**Use AG-UI Protocol when**:
- Building frontend applications
- Need framework interoperability
- Want event-based architecture
- Production deployment with rich UIs

**Combine Both when**:
```python
# Use LangChain tools in ADK agent
from google.adk.tools.langchain_tool import LangchainTool

# Deploy ADK agent with AG-UI for frontend
# Emit AG-UI events for UI updates
# Get best of both worlds
```

**Official Documentation**: https://google.github.io/adk-docs/tools/third-party-tools/

**Action Items**:
- [ ] Create Tutorial 27: Third-Party Framework Tools
- [ ] Document LangchainTool with working examples
- [ ] Document CrewaiTool with working examples
- [ ] Compare tool-level vs framework-level integration
- [ ] Show combined approach (tools + AG-UI)
- [ ] List popular tools from each ecosystem
- [ ] Environment setup guide
- [ ] Troubleshooting common issues

---

## Phase 3 Summary

**RESEARCH COMPLETE**: 8/8 concepts (100%)
**IMPLEMENTATION IN PROGRESS**: 5/12 tasks complete (42%)

### Status Matrix

| Concept | Status | Location | Tutorial Action | Completed |
|---------|--------|----------|-----------------|-----------|
| 1. Multiple Tool Calling | ✅ FOUND | `google/adk/flows/llm_flows/functions.py` | Tutorial 02 - Parallel Section | ✅ DONE |
| 2. Gemini 2.5 Models | ✅ FOUND (DEFAULT!) | `google/adk/models/google_llm.py` | Tutorial 22 - Gemini 2.5 Section | ✅ DONE |
| 3. AG-UI Protocol | ✅ FOUND | `research/ag-ui/` | Tutorial 27 (New) | ⏳ Pending |
| 4. MCP OAuth | ✅ FOUND | `google/adk/tools/mcp_tool/` | Tutorial 16 - OAuth Section | ✅ DONE |
| 5. AgentSpace | ✅ FOUND (Google Cloud) | https://cloud.google.com/products/agentspace | Tutorial 26 (New) | ⏳ Pending |
| 6. Builtin Tools Complete | ✅ FOUND (30+) | `google/adk/tools/` | Tutorial 11 - Expanded | ✅ DONE |
| 7. Framework Integrations | ✅ FOUND | Third-party tools docs | Tutorial 27 (New) | ⏳ Pending |
| 8. LiteLLM/Other LLMs | ✅ FOUND | `google/adk/models/lite_llm.py` | Tutorial 22 + 28 (New) | Tutorial 22 ✅, Tutorial 28 ⏳ |

### Implementation Progress (Latest)

**Completed (4/7 tutorial changes)**:
1. ✅ Tutorial 02 - Added ~200 lines on parallel tool calling with asyncio.gather()
2. ✅ Tutorial 11 - Added ~400 lines on Memory/Workflow/Context/Enterprise tools (30+ total)
3. ✅ Tutorial 16 - Added ~320 lines on MCP OAuth2 authentication (OAuth2/Bearer/Basic/API Key)
4. ✅ Tutorial 22 - Added ~500 lines on Gemini 2.5 (2.5-flash, 2.5-pro, 2.5-flash-lite) + LiteLLM integration

**Total New Content**: ~1,420 lines across 4 existing tutorials ✅ ALL UPDATES COMPLETE

**Completed (7/7 tutorial changes)** ✅ ALL DONE:
5. ✅ Tutorial 26 - Google AgentSpace (new file, ~920 lines) ✅ COMPLETE
6. ✅ Tutorial 27 - Third-Party Framework Tools (new file, ~820 lines) ✅ COMPLETE
7. ✅ Tutorial 28 - Using Other LLMs (new file, ~950 lines) ✅ COMPLETE

**Total New Content**: ~4,110 lines across 7 tutorial files ✅ TARGET EXCEEDED
6. ⏳ Tutorial 27 - Third-Party Framework Tools (new file, ~800 lines)
7. ⏳ Tutorial 28 - Using Other LLMs (new file, ~900 lines)

### Tutorial Strategy Options

**Option A: Update Existing Tutorials**
- Extend Tutorial 02 with parallel tool calling section
- Extend Tutorial 11 with all builtin tools (memory, workflow, etc.)
- Extend Tutorial 16 with MCP OAuth section
- Extend Tutorial 22 with Gemini 2.5 and LiteLLM section

**Pros**: Keeps content consolidated
**Cons**: Makes existing tutorials very long

**Option B: Create New Specialized Tutorials**
- Tutorial 26: AG-UI Protocol & Frontend Integration
- Tutorial 27: Framework Integrations (LangGraph, CrewAI, via AG-UI)
- Tutorial 28: Using Other LLMs (OpenAI, Claude, Ollama, Azure)
- Tutorial 29: Advanced Tool Patterns (Parallel calling, OAuth auth)

**Pros**: Focused deep-dives, easier navigation
**Cons**: More files to maintain

**Option C: Hybrid Approach**
- Update existing: Tutorial 11 (all tools), Tutorial 16 (OAuth), Tutorial 22 (2.5 models)
- Create new: Tutorial 26 (AG-UI), Tutorial 27 (Other LLMs)

### Next Steps

1. **IMMEDIATE**: Ask user about "AgentSpace" - what is it?
2. **Web Research**: Find official Gemini 2.5 documentation from Google AI
3. **Decide Strategy**: Confirm with user - update existing or create new tutorials?
4. **Update thought.md**: Document execution plan
5. **Begin Implementation**: Start with highest priority gap

### Critical Findings

1. **Gemini 2.5 is already the default** - This is HUGE and completely undocumented
2. **Parallel tool calling is automatic** - No configuration needed, works out of the box
3. **AG-UI is the integration layer** - Not direct ADK ↔ LangGraph, but via events
4. **MCP OAuth is production-ready** - Fully tested, just needs documentation
5. **LiteLLM support is comprehensive** - Any model, any provider, working samples exist

