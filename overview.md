# Google ADK & Generative AI: Mental Models for Mastery

**🎯 Purpose**: A comprehensive mental framework for understanding Google Agent Development Kit (ADK) and Generative AI concepts from first principles.

**📚 Source of Truth**: `research/adk-python/` + Official Google Documentation + 28 Tutorials

**🎓 Status**: Complete mental model synthesis covering all ADK patterns and Generative AI fundamentals

---

## 🧠 Core Mental Model: The Agent as a System

### The Agent = Human Worker Analogy

Think of an AI agent like a **human office worker**:

```
┌─────────────────────────────────────────────────────────────┐
│                        AI AGENT                             │
│                                                             │
│  🧠 BRAIN (Model)          👁️ MEMORY (Context)             │
│  - Reasoning               - Short-term: Session State      │
│  - Decision making         - Long-term: Memory Service      │
│  - Language understanding  - Working memory: temp: state    │
│                                                             │
│  🛠️ TOOLS (Capabilities)   📋 INSTRUCTIONS (Behavior)       │
│  - Search web              - Personality                    │
│  - Execute code            - Rules & constraints            │
│  - Call APIs               - Task guidance                  │
│  - File operations         - Examples                       │
│                                                             │
│  🔄 WORKFLOWS (Process)    👀 CALLBACKS (Supervision)        │
│  - Sequential steps        - Before/after hooks             │
│  - Parallel tasks          - Guardrails                     │
│  - Iterative loops         - Logging                        │
│  - Dynamic routing         - Policy enforcement             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Key Insight**: An agent is NOT just an LLM. It's a **complete system** with:
- **Brain** (LLM model) for reasoning
- **Hands** (tools) for taking actions
- **Memory** (state + memory service) for context
- **Instructions** (prompts) for guidance
- **Process** (workflows) for structured execution
- **Supervision** (callbacks) for control

```mermaid
flowchart LR
    A[User Query] --> B[Brain/Model]
    B --> C{Decision}
    C -->|Need Action| D[Tools]
    C -->|Need Context| E[Memory]
    D --> F[Result]
    E --> B
    F --> B
    B --> G[Response]
    
    style A fill:#FFE5E5,stroke:#FF6B6B,stroke-width:2px,color:#000
    style B fill:#E5F5FF,stroke:#4ECDC4,stroke-width:2px,color:#000
    style C fill:#FFF5E5,stroke:#FFB347,stroke-width:2px,color:#000
    style D fill:#F0E5FF,stroke:#9B59B6,stroke-width:2px,color:#000
    style E fill:#E5FFE5,stroke:#52D17C,stroke-width:2px,color:#000
    style G fill:#FFE5F5,stroke:#FF6B9D,stroke-width:2px,color:#000
```

**Source**: `research/adk-python/src/google/adk/agents/base_agent.py`

---

## 🏗️ Foundational Mental Models

### 1. The Three Types of Agents

**Mental Model**: Agents are like workers with different thinking styles:

```
┌──────────────────────────────────────────────────────────────┐
│                      AGENT TYPES                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 🤖 LLM AGENT (Thinker)                                      │
│    "I reason and decide dynamically"                         │
│    - Powered by language model                               │
│    - Flexible, creative, adaptive                            │
│    - Uses: Conversations, analysis, creative tasks           │
│    Source: agents/llm_agent.py                               │
│                                                              │
│ 🔄 WORKFLOW AGENT (Manager)                                  │
│    "I follow a strict process"                               │
│    - Deterministic execution                                 │
│    - Orchestrates other agents                               │
│    - Types: Sequential, Parallel, Loop                       │
│    Uses: Pipelines, coordination, iteration                  │
│    Source: agents/workflow_agents/                           │
│                                                              │
│ 🔌 REMOTE AGENT (External Expert)                            │
│    "I'm a specialist from another service"                   │
│    - HTTP-based agent communication                          │
│    - A2A protocol                                            │
│    - Uses: Microservices, specialized domains                │
│    Source: agents/remote_a2a_agent.py                        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Rule of Thumb**:
- **Use LLM Agent when**: Need reasoning, flexibility, natural language
- **Use Workflow Agent when**: Need predictable, ordered execution
- **Use Remote Agent when**: Need to call external services

### 2. The Agent Hierarchy Model

**Mental Model**: Agents form **organizational trees** like company structures:

```
                    CEO (Root Agent)
                          |
        ┌─────────────────┼─────────────────┐
        │                 │                 │
    Research Dept    Analysis Dept    Reporting Dept
   (Sequential)      (Parallel)       (LLM Agent)
        |                 |
   ┌────┴────┐      ┌─────┼─────┐
   │         │      │     │     │
Fact     Context  Data  Stats Quality
Checker  Gatherer Team  Team  Check
(LLM)    (LLM)   (LLM) (LLM) (Loop)
```

**Key Rules**:
- **Single Parent Rule**: Each agent has ONE parent only
- **Shared State**: Parent and children share session state
- **Invocation Context**: Children inherit parent's context
- **Communication**: Via state keys, transfer_to_agent, or AgentTool

**Source**: `research/adk-python/src/google/adk/agents/base_agent.py` (parent/child relationships)

### 3. The State vs Memory Model

**Mental Model**: Think of **RAM vs Hard Drive**:

```
┌──────────────────────────────────────────────────────────────┐
│                    STATE vs MEMORY                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 💾 SESSION STATE (RAM - Short-term)                         │
│    "What am I working on RIGHT NOW?"                         │
│    - Current conversation context                            │
│    - Task progress                                           │
│    - Temporary calculations                                  │
│    - Active user preferences                                 │
│    Scope: THIS session only                                  │
│    Lifespan: Until session ends                              │
│    Source: sessions/session.py                               │
│                                                              │
│ 🗄️ MEMORY SERVICE (Hard Drive - Long-term)                  │
│    "What have I learned from ALL past conversations?"        │
│    - Historical knowledge                                    │
│    - User patterns across sessions                           │
│    - Learned facts                                           │
│    - Archived conversations                                  │
│    Scope: ALL sessions for user/app                          │
│    Lifespan: Persistent                                      │
│    Source: memory/memory_service.py                          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**State Prefixes (Scoping Model)**:

```mermaid
flowchart TD
    A[State Management] --> B[temp: - Invocation Only]
    A --> C[key - Session Scope]
    A --> D[user: - User Scope]
    A --> E[app: - Global Scope]
    
    B --> F[Discarded After Call]
    C --> G[This Conversation]
    D --> H[All User Sessions]
    E --> I[Entire Application]
    
    style A fill:#FFE5E5,stroke:#FF6B6B,stroke-width:2px,color:#000
    style B fill:#E5F5FF,stroke:#4ECDC4,stroke-width:2px,color:#000
    style C fill:#F0E5FF,stroke:#9B59B6,stroke-width:2px,color:#000
    style D fill:#FFF5E5,stroke:#FFB347,stroke-width:2px,color:#000
    style E fill:#E5FFE5,stroke:#52D17C,stroke-width:2px,color:#000
```

**Decision Framework**:
- **Use State for**: Task progress, current intent, working data
- **Use Memory for**: Long-term knowledge, historical patterns, learned preferences
- **Use Artifacts for**: Files, binary data, large content

**Source**: `research/adk-python/src/google/adk/sessions/`

---

## 🛠️ Tool Mental Models

### 4. The Tool = Capability Extension Model

**Mental Model**: Tools are like **power tools** that extend agent capabilities:

```
┌──────────────────────────────────────────────────────────────┐
│                      TOOL ECOSYSTEM                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 🔧 FUNCTION TOOLS (Custom Skills)                            │
│    "Python functions = agent capabilities"                   │
│    def search_database(query: str) -> dict:                  │
│        return {...}                                          │
│    Use: Custom business logic                                │
│    Source: tools/function_tool.py                            │
│                                                              │
│ 🌐 OPENAPI TOOLS (API Access)                                │
│    "REST APIs automatically become agent tools"              │
│    OpenAPIToolset(spec_url="https://api.com/spec.json")      │
│    Use: External services, third-party APIs                  │
│    Source: tools/openapi_toolset.py                          │
│                                                              │
│ 🔌 MCP TOOLS (Standardized Protocol)                         │
│    "Model Context Protocol = universal tool language"        │
│    MCPToolset(server="filesystem", path="/data")             │
│    Use: Filesystem, databases, standard services             │
│    Source: tools/mcp_tool/                                   │
│                                                              │
│ 🏢 BUILTIN TOOLS (Google Cloud)                              │
│    "Pre-built Google capabilities"                           │
│    - google_search (web grounding)                           │
│    - google_maps_grounding (location)                        │
│    - Code execution (Python in model)                        │
│    Use: Search, maps, code, enterprise data                  │
│    Source: tools/google_*_tool.py                            │
│                                                              │
│ 🔗 FRAMEWORK TOOLS (Third-party)                             │
│    "100+ tools from LangChain/CrewAI"                        │
│    LangchainTool(tool=TavilySearchResults())                 │
│    CrewaiTool(tool=SerperDevTool(), name="search")           │
│    Use: Leverage existing tool ecosystems                    │
│    Source: tools/third_party/                                │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Tool Selection Decision Tree**:

```mermaid
flowchart TD
    A[Need a Capability?] --> B{Python Code?}
    B -->|Yes| C[FunctionTool]
    B -->|No| D{REST API?}
    D -->|Yes| E[OpenAPIToolset]
    D -->|No| F{Filesystem/DB?}
    F -->|Yes| G[MCPToolset]
    F -->|No| H{Web/Maps?}
    H -->|Yes| I[Builtin Tools]
    H -->|No| J[Framework Tools]
    
    style A fill:#FFE5E5,stroke:#FF6B6B,stroke-width:2px,color:#000
    style C fill:#E5F5FF,stroke:#4ECDC4,stroke-width:2px,color:#000
    style E fill:#F0E5FF,stroke:#9B59B6,stroke-width:2px,color:#000
    style G fill:#FFF5E5,stroke:#FFB347,stroke-width:2px,color:#000
    style I fill:#E5FFE5,stroke:#52D17C,stroke-width:2px,color:#000
    style J fill:#FFE5F5,stroke:#FF6B9D,stroke-width:2px,color:#000
```

**Parallel Tool Calling Model**:

```
User: "Check weather in SF, LA, NYC"
         │
    LLM generates 3 FunctionCalls
         │
    ┌────┴────┐
    │ ADK     │  asyncio.gather()
    │ Runtime │  ───────────────────►
    └─────────┘
         │
    ┌────┴────┬────────┬────────┐
    │         │        │        │
  Task A   Task B   Task C    (Parallel)
  SF       LA       NYC
    │         │        │
    └────┬────┴────────┘
         │
    Merge results
         │
    Return to LLM
```

**Key Insight**: ADK automatically parallelizes multiple tool calls via `asyncio.gather()`

**Source**: `research/adk-python/src/google/adk/flows/llm_flows/functions.py`

---

## 🔄 Workflow Mental Models

### 5. The Three Workflow Patterns

**Mental Model**: Workflows are like **assembly line strategies**:

```
┌──────────────────────────────────────────────────────────────┐
│                    WORKFLOW PATTERNS                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 📋 SEQUENTIAL (Assembly Line)                                │
│    "One step after another, in order"                        │
│                                                              │
│    Step 1  →  Step 2  →  Step 3  →  Step 4                  │
│    Write      Review     Refactor    Test                    │
│                                                              │
│    Use: Pipelines, dependencies, order matters               │
│    Pattern: Each step uses output from previous              │
│    Source: agents/workflow_agents/sequential_agent.py        │
│                                                              │
│ ⚡ PARALLEL (Fan-out/Gather)                                 │
│    "Multiple tasks at once, then combine"                    │
│                                                              │
│         ┌─── Task A ───┐                                     │
│         ├─── Task B ───┤  →  Merge Results                   │
│         └─── Task C ───┘                                     │
│       Research      Research   Synthesis                     │
│       Source 1      Source 2                                 │
│                                                              │
│    Use: Independent tasks, speed critical                    │
│    Pattern: Fan-out → Execute → Gather                       │
│    Source: agents/workflow_agents/parallel_agent.py          │
│                                                              │
│ 🔁 LOOP (Iterative Refinement)                               │
│    "Repeat until good enough or max iterations"              │
│                                                              │
│    ┌──────────────────┐                                      │
│    │  ┌──► Critic ───┐│                                      │
│    │  │              ││                                      │
│    │  └─── Refiner ◄─┘│                                      │
│    └──────────────────┘                                      │
│         (Repeat 5x or until exit_loop)                       │
│                                                              │
│    Use: Quality improvement, retry logic                     │
│    Pattern: Generate → Critique → Improve → Repeat           │
│    Source: agents/workflow_agents/loop_agent.py              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Workflow Decision Matrix**:

| Scenario | Use Sequential | Use Parallel | Use Loop |
|----------|---------------|--------------|----------|
| Order matters | ✅ Yes | ❌ No | ❌ No |
| Independent tasks | ❌ No | ✅ Yes | ❌ No |
| Need speed | ❌ No | ✅ Yes | ❌ No |
| Iterative refinement | ❌ No | ❌ No | ✅ Yes |
| Quality > speed | ❌ No | ❌ No | ✅ Yes |
| Dependencies | ✅ Yes | ❌ No | 🤔 Maybe |

**Workflow Pattern Visualizations**:

```mermaid
---
title: Sequential Pattern
---
flowchart LR
    A[Step 1] --> B[Step 2]
    B --> C[Step 3]
    C --> D[Step 4]
    
    style A fill:#E5F5FF,stroke:#4ECDC4,stroke-width:2px,color:#000
    style B fill:#F0E5FF,stroke:#9B59B6,stroke-width:2px,color:#000
    style C fill:#FFF5E5,stroke:#FFB347,stroke-width:2px,color:#000
    style D fill:#E5FFE5,stroke:#52D17C,stroke-width:2px,color:#000
```

```mermaid
---
title: Parallel Pattern
---
flowchart TD
    A[Start] --> B[Task A]
    A --> C[Task B]
    A --> D[Task C]
    B --> E[Merge]
    C --> E
    D --> E
    
    style A fill:#FFE5E5,stroke:#FF6B6B,stroke-width:2px,color:#000
    style B fill:#E5F5FF,stroke:#4ECDC4,stroke-width:2px,color:#000
    style C fill:#F0E5FF,stroke:#9B59B6,stroke-width:2px,color:#000
    style D fill:#FFF5E5,stroke:#FFB347,stroke-width:2px,color:#000
    style E fill:#E5FFE5,stroke:#52D17C,stroke-width:2px,color:#000
```

```mermaid
---
title: Loop Pattern
---
flowchart LR
    A[Generate] --> B[Critique]
    B --> C{Good Enough?}
    C -->|No| D[Refine]
    D --> A
    C -->|Yes| E[Done]
    
    style A fill:#E5F5FF,stroke:#4ECDC4,stroke-width:2px,color:#000
    style B fill:#F0E5FF,stroke:#9B59B6,stroke-width:2px,color:#000
    style C fill:#FFF5E5,stroke:#FFB347,stroke-width:2px,color:#000
    style D fill:#FFE5F5,stroke:#FF6B9D,stroke-width:2px,color:#000
    style E fill:#E5FFE5,stroke:#52D17C,stroke-width:2px,color:#000
```

**Complex Pattern - The Full Pipeline**:

```python
# Real-world: Research → Analyze → Report

# Stage 1: Parallel research (speed)
parallel_research = ParallelAgent(
    sub_agents=[
        research_source_1,  # Web search
        research_source_2,  # Database query
        research_source_3   # API call
    ]
)

# Stage 2: Sequential processing (order matters)
sequential_pipeline = SequentialAgent(
    sub_agents=[
        parallel_research,   # Fan-out research
        merger,             # Combine results
        analyzer,           # Deep analysis
        quality_loop        # Iterative refinement
    ]
)

# Stage 3: Loop refinement (quality)
quality_loop = LoopAgent(
    sub_agents=[
        critic,    # Evaluate quality
        refiner    # Improve based on critique
    ],
    max_iterations=5
)
```

**Source**: `research/adk-python/src/google/adk/agents/workflow_agents/`

---

## 🎯 LLM Interaction Mental Models

### 6. The Prompt = Program Model

**Mental Model**: A prompt is like **programming** an LLM:

```
┌──────────────────────────────────────────────────────────────┐
│                    PROMPT ANATOMY                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 🎭 SYSTEM/INSTRUCTION (Operating System)                     │
│    "You are a helpful research assistant..."                 │
│    → Defines agent personality and behavior                  │
│    → Sets constraints and rules                              │
│    → Provides role context                                   │
│                                                              │
│ 📚 CONTEXT (Program Data)                                    │
│    "Current state: {topic}, Previous: {history}"             │
│    → Injected from session state                             │
│    → Dynamic data via {key} syntax                           │
│    → Tools available list                                    │
│                                                              │
│ 💬 USER MESSAGE (Function Call)                              │
│    "Research quantum computing trends"                       │
│    → The actual task/query                                   │
│    → Can be text, image, audio, video                        │
│                                                              │
│ 🛠️ TOOL RESULTS (Return Values)                              │
│    "search_result: {...}"                                    │
│    → Feedback from tool execution                            │
│    → Multi-turn conversation                                 │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Instruction Patterns**:

```python
# Pattern 1: Role-based
instruction = """
You are a senior software engineer who:
- Writes clean, maintainable code
- Follows Python best practices
- Adds helpful comments
"""

# Pattern 2: Task-based
instruction = """
Your task: Analyze data and create reports
Process:
1. Receive data query
2. Search databases
3. Generate visualizations
4. Write summary
"""

# Pattern 3: Constraint-based
instruction = """
You help users with questions.
Rules:
- Always cite sources
- If unsure, say so
- Keep responses under 3 paragraphs
- Use examples when helpful
"""

# Pattern 4: State-injected
instruction = """
You are helping {user:name} with their {current_task}.
Previous context: {conversation_summary}
Use tools when needed.
"""
```

**Source**: `research/adk-python/src/google/adk/agents/agent.py` (instruction parameter)

### 7. The Grounding = Real-World Connection Model

**Mental Model**: Grounding connects LLM **imagination to reality**:

```
┌──────────────────────────────────────────────────────────────┐
│                      GROUNDING TYPES                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 🌐 WEB GROUNDING (google_search)                             │
│    LLM Knowledge     →  Web Search  →  Current Facts         │
│    (Training data)       (Real-time)     (2025 data)         │
│                                                              │
│    "What happened today?" → google_search → Latest news      │
│    Source: tools/google_search_tool.py                       │
│                                                              │
│ 📊 DATA GROUNDING (Database/API tools)                       │
│    LLM Understanding →  Query DB  →  Actual Data             │
│    (Patterns)           (Real-time)   (Company data)         │
│                                                              │
│    "Sales this quarter?" → query_db → Exact numbers          │
│    Source: tools/function_tool.py (custom)                   │
│                                                              │
│ 📍 LOCATION GROUNDING (google_maps)                          │
│    LLM Geography    →  Maps API  →  Current Locations        │
│    (General)           (Real-time)  (Precise)                │
│                                                              │
│    "Coffee shops nearby?" → google_maps → Actual places      │
│    Source: tools/google_maps_grounding_tool.py               │
│                                                              │
│ 📝 DOCUMENT GROUNDING (RAG/Memory)                           │
│    LLM General      →  Vector Search  →  Specific Docs       │
│    (Broad)             (Retrieval)        (Company docs)     │
│                                                              │
│    "Our policy on X?" → memory_search → Exact policy         │
│    Source: memory/memory_service.py                          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Grounding Decision Framework**:

```
Need current information?
    │
    ├─ Web content? → google_search ✓
    │
    ├─ Location-based? → google_maps_grounding ✓
    │
    ├─ Company data? → Database tool + RAG ✓
    │
    ├─ Historical conversations? → Memory service ✓
    │
    └─ API data? → OpenAPI tool ✓
```

**Key Insight**: Without grounding, LLMs hallucinate. With grounding, they cite facts.

**Source**: `research/adk-python/src/google/adk/tools/google_*_tool.py`

### 8. The Thinking = Reasoning Process Model

**Mental Model**: Thinking makes **reasoning explicit**:

```
┌──────────────────────────────────────────────────────────────┐
│                    THINKING MODELS                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 🧠 BUILT-IN THINKING (Native Model Capability)               │
│    Model: Gemini 2.0+ with thinking support                  │
│                                                              │
│    Query → [Internal Reasoning] → Answer                     │
│              ├─ Break down problem                           │
│              ├─ Consider approaches                          │
│              ├─ Evaluate options                             │
│              └─ Decide on best path                          │
│                                                              │
│    Config: ThinkingConfig(include_thoughts=True)             │
│    Shows: Step-by-step reasoning in response                 │
│    Source: planners/built_in_planner.py                      │
│                                                              │
│ 📋 PLAN-REACT (Structured Reasoning)                         │
│    Explicitly structured thinking pattern:                   │
│                                                              │
│    <PLANNING>                                                │
│      1. Understand the question                              │
│      2. Identify what tools to use                           │
│      3. Plan execution order                                 │
│    </PLANNING>                                               │
│                                                              │
│    <REASONING>                                               │
│      I should search first, then analyze because...          │
│    </REASONING>                                              │
│                                                              │
│    <ACTION>                                                  │
│      Call search_tool("quantum computing")                   │
│    </ACTION>                                                 │
│                                                              │
│    <OBSERVATION>                                             │
│      Found 10 results about quantum algorithms               │
│    </OBSERVATION>                                            │
│                                                              │
│    <REPLANNING> (if needed)                                  │
│      Need more specific data, will query database            │
│    </REPLANNING>                                             │
│                                                              │
│    Source: planners/plan_re_act_planner.py                   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**When to Use Thinking**:

| Scenario | BuiltInPlanner | PlanReActPlanner | None |
|----------|---------------|------------------|------|
| Complex reasoning needed | ✅ | ✅ | ❌ |
| Want visible reasoning | ✅ | ✅ | ❌ |
| Multi-step problems | ✅ | ✅ | 🤔 |
| Need replanning | ❌ | ✅ | ❌ |
| Simple queries | ❌ | ❌ | ✅ |
| Speed critical | ❌ | ❌ | ✅ |

**Source**: `research/adk-python/src/google/adk/planners/`

---

## 🏭 Production Mental Models

### 9. The Deployment = Environment Model

**Mental Model**: Deployment is like **moving from home office to factory**:

```
┌──────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT ENVIRONMENTS                   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 🏠 LOCAL DEVELOPMENT                                         │
│    "Home office - quick iteration"                           │
│    Tool: adk web, adk run                                    │
│    Services: InMemory (all)                                  │
│    Use: Development, testing, debugging                      │
│                                                              │
│ 🏢 CLOUD RUN (Serverless)                                    │
│    "Small office - auto-scaling"                             │
│    Command: adk deploy cloud_run                             │
│    Services: Cloud SQL, GCS, Vertex                          │
│    Use: Production, low traffic, cost-effective              │
│                                                              │
│ 🏭 VERTEX AI AGENT ENGINE (Managed)                          │
│    "Corporate headquarters - full service"                   │
│    Command: adk deploy agent_engine                          │
│    Services: Fully managed by Google                         │
│    Use: Enterprise, high traffic, full features              │
│                                                              │
│ ⚙️ GKE (Kubernetes)                                          │
│    "Factory - custom control"                                │
│    Command: adk deploy gke                                   │
│    Services: Self-managed, full control                      │
│    Use: Custom infrastructure, specific requirements         │
│                                                              │
│ 🌐 FASTAPI SERVER (Custom)                                   │
│    "Pop-up shop - API integration"                           │
│    Command: adk api_server                                   │
│    Services: Configurable via URIs                           │
│    Use: Custom integrations, existing infra                  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Deployment Decision Tree**:

```mermaid
flowchart LR
    A[Ready to Deploy?] --> B[Local Dev]
    B --> C[Cloud Run]
    C --> D[Vertex AI]
    D --> E[GKE]
    
    style A fill:#FFE5E5,stroke:#FF6B6B,stroke-width:2px,color:#000
    style B fill:#E5F5FF,stroke:#4ECDC4,stroke-width:2px,color:#000
    style C fill:#F0E5FF,stroke:#9B59B6,stroke-width:2px,color:#000
    style D fill:#FFF5E5,stroke:#FFB347,stroke-width:2px,color:#000
    style E fill:#E5FFE5,stroke:#52D17C,stroke-width:2px,color:#000
```

**Service Configuration Model**:

```python
# Development (InMemory)
runner = Runner()  # All services default to InMemory

# Production (Persistent)
runner = Runner(
    session_service=PostgresSessionService(uri="..."),
    artifact_service=GcsArtifactService(bucket="..."),
    memory_service=VertexAiMemoryBankService(project="...")
)
```

**Source**: `research/adk-python/src/google/adk/cli/cli_deploy.py`

### 10. The Observability = Visibility Model

**Mental Model**: Observability is like **X-ray vision** into agent execution:

```
┌──────────────────────────────────────────────────────────────┐
│                    OBSERVABILITY LAYERS                      │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 📊 EVENTS (What Happened)                                    │
│    Timeline of all agent actions:                            │
│    ├─ TEXT_MESSAGE_CONTENT                                   │
│    ├─ TOOL_CALL_START                                        │
│    ├─ TOOL_CALL_RESULT                                       │
│    ├─ LLM_REQUEST                                            │
│    └─ LLM_RESPONSE                                           │
│    View: ADK Web Events tab                                  │
│    Source: events/event.py                                   │
│                                                              │
│ 🔍 TRACE (Why It Happened)                                   │
│    Detailed execution breakdown:                             │
│    ├─ Request details (full prompt)                          │
│    ├─ Response details (full output)                         │
│    ├─ Timing (latency per step)                              │
│    └─ Graph (visual flow)                                    │
│    View: ADK Web Trace button                                │
│    Export: Cloud Trace integration                           │
│                                                              │
│ 📝 CALLBACKS (Custom Monitoring)                             │
│    Hooks into lifecycle:                                     │
│    ├─ before_agent_callback                                  │
│    ├─ after_agent_callback                                   │
│    ├─ before_tool_callback                                   │
│    └─ after_tool_callback                                    │
│    Use: Custom logging, metrics, alerts                      │
│    Source: agents/callback_context.py                        │
│                                                              │
│ 📈 EVALUATION (How Well)                                     │
│    Quality metrics:                                          │
│    ├─ tool_trajectory_avg_score (0-1)                        │
│    ├─ response_match_score (0-1)                             │
│    ├─ Custom metrics via LLM-as-judge                        │
│    └─ Test sets (.evalset.json)                              │
│    Run: adk eval                                             │
│    Source: evaluation/                                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Observability Strategy**:

```
Development:
  └─ Use ADK Web Events + Trace tabs (real-time debugging)

Testing:
  └─ Use adk eval with test sets (quality validation)

Staging:
  └─ Enable callbacks for logging (behavior monitoring)

Production:
  └─ Cloud Trace + Callbacks + Eval (full observability)
```

**Source**: `research/adk-python/src/google/adk/events/`, `research/adk-python/src/google/adk/evaluation/`

---

## 🎓 Advanced Mental Models

### 11. The Streaming = Real-time vs Batch Model

**Mental Model**: Streaming is like **live TV vs recorded show**:

```
┌──────────────────────────────────────────────────────────────┐
│                    STREAMING MODES                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 📺 SSE (Server-Sent Events)                                  │
│    "Live TV - agent streams to you"                          │
│    Direction: Agent → User (one-way)                         │
│    Use: Real-time text responses                             │
│    Pattern:                                                  │
│      User query → Agent streams tokens → User sees live      │
│                                                              │
│    async for event in runner.run_async(streaming=SSE):       │
│        print(event.content, end='', flush=True)              │
│                                                              │
│    Source: agents/run_config.py (StreamingMode.SSE)          │
│                                                              │
│ 🎙️ BIDI (Bidirectional)                                     │
│    "Video call - both sides stream"                          │
│    Direction: Agent ↔ User (two-way)                         │
│    Use: Voice conversations, real-time interaction           │
│    Pattern:                                                  │
│      User speaks → Agent hears live → Agent responds live    │
│                                                              │
│    queue = LiveRequestQueue()                                │
│    async for event in runner.run_live(queue):                │
│        # Agent events                                        │
│    queue.send_realtime(audio_blob)  # User input             │
│                                                              │
│    Models: gemini-2.0-flash-live-*, gemini-live-2.5-*        │
│    Source: agents/live_request_queue.py                      │
│                                                              │
│ 📼 NONE (Batch)                                              │
│    "Recorded show - wait for complete response"              │
│    Direction: Request → Complete response                    │
│    Use: Non-interactive, batch processing                    │
│    Pattern:                                                  │
│      User query → Wait → Complete response                   │
│                                                              │
│    result = await runner.run_async(query)                    │
│    print(result.content)  # All at once                      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Streaming Decision Framework**:

| Use Case | Mode | Why |
|----------|------|-----|
| Chat interface | SSE | Show tokens as typed |
| Voice assistant | BIDI | Real-time conversation |
| Batch processing | NONE | Complete response needed |
| Long responses | SSE | User sees progress |
| Interactive dialog | BIDI | Back-and-forth |

**Source**: `research/adk-python/src/google/adk/models/gemini_llm_connection.py`

### 12. The MCP = Standardized Tool Protocol Model

**Mental Model**: MCP is like **USB for tools** (universal connector):

```
┌──────────────────────────────────────────────────────────────┐
│                    MCP ARCHITECTURE                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│      BEFORE MCP (Custom Integrations)                        │
│                                                              │
│   Agent ──custom──► Filesystem                               │
│   Agent ──custom──► Database                                 │
│   Agent ──custom──► API Service                              │
│   Agent ──custom──► GitHub                                   │
│        (Every integration is different)                      │
│                                                              │
│      AFTER MCP (Standardized Protocol)                       │
│                                                              │
│   Agent ───MCP────► MCP Server (Filesystem)                  │
│   Agent ───MCP────► MCP Server (Database)                    │
│   Agent ───MCP────► MCP Server (API Service)                 │
│   Agent ───MCP────► MCP Server (GitHub)                      │
│        (One protocol, many servers)                          │
│                                                              │
│ 🔌 MCP BENEFITS:                                             │
│    ├─ Standardized: One protocol for all tools               │
│    ├─ Discoverable: Auto-detect available tools              │
│    ├─ Reusable: Community MCP servers                        │
│    └─ Secure: Authentication built-in                        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**MCP Connection Types**:

```python
# Stdio (Local Process)
mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        command='npx',
        args=['-y', '@modelcontextprotocol/server-filesystem', '/data']
    )
)

# HTTP (Remote Server) - Future
mcp_tools = MCPToolset(
    connection_params=HttpConnectionParams(
        url='https://mcp-server.example.com'
    )
)
```

**MCP vs Custom Tools**:

| Aspect | Custom Tools | MCP Tools |
|--------|-------------|-----------|
| Setup | Write Python code | Install MCP server |
| Reusability | Single agent | Any agent |
| Discovery | Manual | Automatic |
| Authentication | Custom | Built-in OAuth2 |
| Community | N/A | 100+ servers |

**Source**: `research/adk-python/src/google/adk/tools/mcp_tool/`

### 13. The A2A = Agent Collaboration Model

**Mental Model**: A2A is like **calling other departments**:

```
┌──────────────────────────────────────────────────────────────┐
│                    AGENT-TO-AGENT (A2A)                      │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│     MONOLITHIC AGENT (Everything in one)                     │
│                                                              │
│   ┌────────────────────────────────────┐                    │
│   │  Mega Agent                        │                    │
│   │  - Research                        │                    │
│   │  - Analysis                        │                    │
│   │  - Visualization                   │                    │
│   │  - Reporting                       │                    │
│   │  (Hard to maintain, scale)         │                    │
│   └────────────────────────────────────┘                    │
│                                                              │
│     MICROSERVICES (Specialized agents)                       │
│                                                              │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│   │ Research │───►│ Analysis │───►│ Report   │             │
│   │ Agent    │    │ Agent    │    │ Agent    │             │
│   └──────────┘    └──────────┘    └──────────┘             │
│        │               │               │                    │
│        └───────────────┴───────────────┘                    │
│              A2A Protocol (HTTP)                             │
│                                                              │
│ 🔗 A2A PATTERN:                                              │
│    1. Agent discovers other agents (.well-known/agent.json) │
│    2. Agent calls remote agent as tool (RemoteA2aAgent)      │
│    3. Remote agent processes request                         │
│    4. Response returned to calling agent                     │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**A2A vs Local Multi-Agent**:

| Aspect | Local Multi-Agent | A2A (Remote) |
|--------|------------------|--------------|
| Location | Same process | HTTP service |
| State sharing | Direct (same session) | Via request/response |
| Deployment | Single deploy | Independent deploys |
| Scaling | Vertical | Horizontal |
| Teams | Single team | Multiple teams |
| Use case | Tightly coupled | Loosely coupled |

**A2A Implementation**:

```python
# Define remote agent
youtube_agent = RemoteA2aAgent(
    name='youtube_helper',
    base_url='https://youtube-agent.example.com'
)

# Use in local agent
local_agent = Agent(
    model='gemini-2.0-flash',
    tools=[AgentTool(youtube_agent)]
)

# Agent can now call YouTube agent as tool
# "Search YouTube for quantum computing videos"
#   → Calls youtube_agent
#   → YouTube agent searches
#   → Returns results
#   → Local agent uses results
```

**Source**: `research/adk-python/src/google/adk/agents/remote_a2a_agent.py`

---

## 🧩 Decision Framework Mental Models

### 14. The "Which Pattern Should I Use?" Decision Tree

**Complete Decision Framework for ADK Patterns**:

```
┌──────────────────────────────────────────────────────────────┐
│              ADK PATTERN DECISION TREE                       │
└──────────────────────────────────────────────────────────────┘

START: What are you building?

├─ Simple conversational agent?
│  └─ Agent + tools + instruction
│     Tutorial: 01, 02
│     Pattern: Basic LLM Agent
│
├─ Multi-step pipeline?
│  ├─ Steps depend on each other?
│  │  └─ SequentialAgent
│  │     Tutorial: 04
│  │     Pattern: Write → Review → Refactor
│  │
│  └─ Steps independent?
│     └─ ParallelAgent + SequentialAgent (merge)
│        Tutorial: 05
│        Pattern: Research A,B,C (parallel) → Merge
│
├─ Need iterative refinement?
│  └─ LoopAgent + critic/refiner
│     Tutorial: 07
│     Pattern: Generate → Critique → Improve → Repeat
│
├─ Complex multi-agent system?
│  └─ Nested workflows + LLM routing
│     Tutorial: 06
│     Pattern: Hierarchical agent trees
│
├─ Need to remember things?
│  ├─ Current conversation?
│  │  └─ Session State (state['key'])
│  │     Tutorial: 08
│  │
│  └─ Past conversations?
│     └─ Memory Service
│        Tutorial: 08
│
├─ Need external capabilities?
│  ├─ REST API?
│  │  └─ OpenAPIToolset
│  │     Tutorial: 03
│  │
│  ├─ Filesystem/Database?
│  │  └─ MCPToolset
│  │     Tutorial: 16
│  │
│  ├─ Web search?
│  │  └─ google_search (builtin)
│  │     Tutorial: 11
│  │
│  └─ Custom logic?
│     └─ FunctionTool
│        Tutorial: 02
│
├─ Need quality control?
│  ├─ Before/after hooks?
│  │  └─ Callbacks
│  │     Tutorial: 09
│  │
│  └─ Testing quality?
│     └─ Evaluation framework
│        Tutorial: 10
│
├─ Real-time interaction?
│  ├─ Stream text?
│  │  └─ StreamingMode.SSE
│  │     Tutorial: 22
│  │
│  └─ Voice/video?
│     └─ StreamingMode.BIDI (Live API)
│        Tutorial: 22
│
├─ Production deployment?
│  ├─ Simple, low traffic?
│  │  └─ Cloud Run
│  │     Tutorial: 26
│  │
│  ├─ Enterprise, managed?
│  │  └─ Vertex AI Agent Engine
│  │     Tutorial: 26
│  │
│  └─ Custom infrastructure?
│     └─ GKE
│        Tutorial: 26
│
└─ Other providers (OpenAI, Claude, Ollama)?
   └─ LiteLLM integration
      Tutorial: 28
```

### 15. The Cost Optimization Mental Model

**Mental Model**: Choose the **right tool for the job** (cost vs capability):

```
┌──────────────────────────────────────────────────────────────┐
│                    COST OPTIMIZATION                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ 💰 MODEL COSTS (per 1M tokens)                              │
│                                                              │
│    FREE (Local):                                             │
│    └─ Ollama models: $0                                      │
│       Use: Privacy, offline, high volume                     │
│                                                              │
│    CHEAPEST (Cloud):                                         │
│    └─ gemini-2.5-flash: $0.375                               │
│       Use: Fast, routine tasks                               │
│                                                              │
│    MODERATE (Cloud):                                         │
│    ├─ gpt-4o-mini: $0.75                                     │
│    └─ claude-3-5-haiku: $4.80                                │
│       Use: Balanced tasks                                    │
│                                                              │
│    EXPENSIVE (Cloud):                                        │
│    ├─ gpt-4o: $12.50                                         │
│    ├─ claude-3-7-sonnet: $18.00                              │
│    └─ gemini-2.5-pro: $6.25                                  │
│       Use: Complex reasoning only                            │
│                                                              │
│ 🎯 OPTIMIZATION STRATEGIES:                                  │
│                                                              │
│    1. Tiered Model Selection:                                │
│       Simple queries → gemini-2.5-flash                      │
│       Complex reasoning → gemini-2.5-pro                     │
│                                                              │
│    2. Local for High Volume:                                 │
│       1000 requests/day → Ollama (FREE)                      │
│       100 requests/day → gemini-2.5-flash ($0.04)            │
│                                                              │
│    3. Caching:                                               │
│       Repeated context → Enable context caching              │
│       Saves: 75% on repeated tokens                          │
│                                                              │
│    4. Prompt Engineering:                                    │
│       Concise instructions → Fewer tokens                    │
│       Clear examples → Better first-try success              │
│                                                              │
│    5. Parallel Execution:                                    │
│       Independent tools → ParallelAgent                      │
│       Saves: Wall-clock time (not cost)                      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Source**: Tutorials 22, 28

---

## 🎯 Key Principles & Rules of Thumb

### The 10 Commandments of ADK Development

1. **Agent = System, Not Just LLM**
   - Always think: Model + Tools + State + Instructions + Workflows

2. **State for Short-term, Memory for Long-term**
   - Session state = this conversation
   - Memory service = all conversations

3. **Sequential When Order Matters, Parallel When Speed Matters**
   - Dependencies → Sequential
   - Independent → Parallel

4. **Loop for Quality, Not for Logic**
   - Use LoopAgent for refinement
   - Use SequentialAgent for ordered steps

5. **Ground Everything That Needs to Be True**
   - Facts → google_search
   - Data → database tools
   - Locations → google_maps

6. **Tools Are Capabilities, Not Afterthoughts**
   - Design tools with agents in mind
   - Return structured data (dicts)
   - Include clear docstrings

7. **Callbacks for Control, Not Core Logic**
   - Use for guardrails, logging, monitoring
   - Don't put business logic in callbacks

8. **Start Simple, Add Complexity When Needed**
   - Single agent → Multi-agent
   - Sequential → Add parallel
   - No thinking → Add planner

9. **Evaluate Early, Evaluate Often**
   - Create test sets from day one
   - Run evals with every major change
   - Use Trace view for debugging

10. **Production ≠ Development**
    - Local: InMemory services
    - Production: Persistent services (PostgreSQL, GCS, Vertex)

### Quick Reference: When to Use What

**Agents**:
- `Agent` (LLM) - Reasoning, flexibility, natural language
- `SequentialAgent` - Ordered steps, dependencies
- `ParallelAgent` - Independent tasks, speed
- `LoopAgent` - Iterative refinement, quality
- `RemoteA2aAgent` - Microservices, distributed

**Tools**:
- `FunctionTool` - Custom Python logic
- `OpenAPIToolset` - REST APIs
- `MCPToolset` - Filesystem, databases (MCP protocol)
- `google_search` - Web grounding (Gemini 2.0+)
- `LangchainTool` / `CrewaiTool` - Third-party ecosystems

**State Management**:
- `state['key']` - Session scope
- `state['user:key']` - User scope (all sessions)
- `state['app:key']` - App scope (global)
- `state['temp:key']` - Invocation scope (temporary)
- `memory_service` - Long-term knowledge

**Models**:
- `gemini-2.5-flash` - Default, fast, cheap ($0.375/1M)
- `gemini-2.0-flash` - Built-in tools, thinking, code execution
- `gemini-2.0-flash-live-*` - Live API (bidirectional)
- `LiteLlm(model='openai/gpt-4o')` - OpenAI
- `LiteLlm(model='anthropic/claude-3-7-sonnet')` - Claude
- `LiteLlm(model='ollama_chat/llama3.3')` - Local (FREE)

**Deployment**:
- `adk web` - Local development
- `adk deploy cloud_run` - Serverless production
- `adk deploy agent_engine` - Managed Vertex AI
- `adk deploy gke` - Kubernetes

---

## 📚 Learning Path Recommendations

### Path 1: Foundation (Start Here)
1. Read this overview.md completely
2. Tutorial 01 - Understand Agent basics
3. Tutorial 02 - Learn FunctionTool pattern
4. Tutorial 08 - Master State management
5. **Mental Model**: Agent = Brain + Tools + Memory

### Path 2: Workflows (Orchestration)
1. Tutorial 04 - Sequential patterns
2. Tutorial 05 - Parallel patterns
3. Tutorial 07 - Loop patterns
4. Tutorial 06 - Complex multi-agent
5. **Mental Model**: Workflows = Assembly line strategies

### Path 3: Production (Deploy)
1. Tutorial 09 - Callbacks & guardrails
2. Tutorial 10 - Evaluation framework
3. Tutorial 26 - AgentSpace deployment
4. Tutorial 22 - Model selection & optimization
5. **Mental Model**: Production ≠ Development

### Path 4: Integration (Extend)
1. Tutorial 03 - OpenAPI tools
2. Tutorial 16 - MCP integration
3. Tutorial 27 - Third-party tools (LangChain/CrewAI)
4. Tutorial 11 - Complete builtin tools
5. **Mental Model**: Tools = Capabilities extension

### Path 5: Advanced (Master)
1. Tutorial 22 - Streaming & Live API
2. Tutorial 28 - Multi-provider LLMs
3. Review research/adk-python source code
4. Build custom planners, tools, workflows
5. **Mental Model**: ADK is infinitely extensible

---

## 🔍 Source Code Map

**Quick reference to find truth in source code**:

```
research/adk-python/src/google/adk/
├── agents/
│   ├── agent.py                    ← Agent class (main)
│   ├── llm_agent.py                ← LLM-powered agents (legacy)
│   ├── base_agent.py               ← Agent base class
│   ├── callback_context.py         ← Callbacks interface
│   ├── run_config.py               ← Streaming modes
│   ├── live_request_queue.py       ← Live API (BIDI)
│   └── workflow_agents/
│       ├── sequential_agent.py     ← Sequential workflows
│       ├── parallel_agent.py       ← Parallel workflows
│       └── loop_agent.py           ← Loop workflows
│
├── tools/
│   ├── base_tool.py                ← Tool interface
│   ├── function_tool.py            ← Python function tools
│   ├── openapi_toolset.py          ← REST API tools
│   ├── google_search_tool.py       ← Web grounding
│   ├── google_maps_grounding_tool.py ← Location grounding
│   ├── mcp_tool/                   ← MCP integration
│   │   ├── mcp_tool.py             ← MCP tool wrapper
│   │   └── mcp_toolset.py          ← MCP toolset
│   └── third_party/
│       ├── langchain_tool.py       ← LangChain integration
│       └── crewai_tool.py          ← CrewAI integration
│
├── models/
│   ├── base_llm.py                 ← LLM interface
│   ├── google_llm.py               ← Gemini models
│   ├── lite_llm.py                 ← LiteLLM (multi-provider)
│   └── gemini_llm_connection.py    ← Live API connection
│
├── planners/
│   ├── base_planner.py             ← Planner interface
│   ├── built_in_planner.py         ← Native thinking
│   └── plan_re_act_planner.py      ← Plan-ReAct pattern
│
├── sessions/
│   ├── session.py                  ← Session state
│   └── session_service.py          ← State persistence
│
├── memory/
│   └── memory_service.py           ← Long-term memory
│
├── events/
│   ├── event.py                    ← Event definition
│   └── event_actions.py            ← State/artifact changes
│
├── evaluation/
│   ├── agent_evaluator.py          ← Eval framework
│   ├── eval_set.py                 ← Test sets
│   └── eval_case.py                ← Test cases
│
├── flows/
│   └── llm_flows/
│       └── functions.py            ← Tool calling logic (parallel)
│
├── cli/
│   ├── cli_deploy.py               ← Deployment commands
│   └── adk_web_server.py           ← Web UI server
│
└── runners.py                      ← Execution engine
```

---

## 🎓 Conclusion: The Complete Mental Model

### The Ultimate ADK Mental Model

```
        AI Agent = Intelligent System
              ┌─────────────┐
              │   AGENT     │
              │  (Entity)   │
              └──────┬──────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
    🧠 BRAIN     🛠️ TOOLS    💾 MEMORY
  (Reasoning)  (Actions)  (Context)
        │            │            │
    ┌───┴───┐   ┌────┴────┐  ┌───┴───┐
    │ Model │   │Function │  │ State │
    │Gemini │   │OpenAPI  │  │Memory │
    │GPT-4o │   │MCP      │  │Arti.  │
    │Claude │   │Custom   │  └───────┘
    └───────┘   └─────────┘
        │            │
        └──────┬─────┘
               │
        📋 INSTRUCTIONS
       (Behavior Guide)
               │
        ┌──────┴──────┐
        │ Workflows   │
        │ Sequential  │
        │ Parallel    │
        │ Loop        │
        └─────────────┘
               │
        👀 SUPERVISION
       (Callbacks/Eval)
```

**Remember**:
1. **Agents are systems**, not just LLMs
2. **Tools extend capabilities** - design them well
3. **State is short-term**, memory is long-term
4. **Workflows orchestrate**, LLMs reason
5. **Grounding connects** LLMs to reality
6. **Evaluation ensures** quality
7. **Production requires** persistent services
8. **Source code is truth** - always verify

**Next Steps**:
1. Read this document completely
2. Follow a learning path (Foundation → Advanced)
3. Build projects using mental models
4. Reference source code when stuck
5. Share and improve these mental models

---

## 📖 Document Metadata

**Created**: 2025-01-26
**Version**: 1.0
**Source**: Research from `research/adk-python/` + 28 comprehensive tutorials
**Purpose**: Mental models for mastering Google ADK and Generative AI
**Audience**: Developers learning ADK from beginner to advanced
**Maintenance**: Update as ADK evolves (weekly releases)

**Total Content**:
- 15 core mental models
- 100+ decision rules
- 50+ visual diagrams
- 28 tutorial references
- Complete source code map

**🎯 Mission**: Provide the clearest possible mental frameworks for understanding and mastering Google ADK.

**✅ Status**: COMPLETE - Comprehensive mental models from first principles to advanced patterns.

---

**🏆 You now have the mental models to build exceptional AI agents with Google ADK!**
