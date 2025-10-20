# Content Cross-References Map

**Purpose**: This document maps relationships between TILs, Blog Posts, and
Tutorials to help readers navigate the learning ecosystem.

**Last Updated**: October 20, 2025

---

## Quick Navigation

- [TIL Cross-References](#til-cross-references)
- [Blog Post Cross-References](#blog-post-cross-references)
- [Tutorial Relationships](#tutorial-relationships)
- [Learning Paths](#learning-paths-by-content-type)
- [Content Type Comparison](#content-type-comparison)

---

## TIL Cross-References

### TIL: Pause and Resume Invocations (Oct 20, 2025)

**Links To:**

- **Related TILs**:
  - [TIL: Context Compaction](/docs/til/til_context_compaction_20250119)
    - Use together for complete state management

- **Related Blog Posts**:
  - [Deploy AI Agents: Production Strategies](/blog/deploy-ai-agents)
    - Fault tolerance in production
  - [The Multi-Agent Pattern: Managing Complexity](/blog/multi-agent-pattern-complexity-management)
    - State management across handoffs

- **Related Tutorials**:
  - [Tutorial 08: State & Memory](/docs/state_memory)
    - Broader state management patterns
  - [Tutorial 17: Agent-to-Agent Communication](/docs/agent_to_agent)
    - State preservation in distributed systems
  - [Tutorial 18: Events & Observability](/docs/events_observability)
    - Understanding checkpoint events

- **Working Implementation**:
  - `til_implementation/til_pause_resume_20251020/`

**Use Case**: "I need to save agent state and resume later"

---

### TIL: Context Compaction (Oct 19, 2025)

**Links To:**

- **Related TILs**:
  - [TIL: Pause and Resume Invocations](/docs/til/til_pause_resume_20251020)
    - Combine for complete memory management

- **Related Blog Posts**:
  - [Deploy AI Agents: Production Strategies](/blog/deploy-ai-agents)
    - Cost optimization in production
  - [Tutorial Progress Update](/blog/tutorial-progress-october-2025)
    - Memory optimization patterns

- **Related Tutorials**:
  - [Tutorial 08: State & Memory](/docs/state_memory)
    - Broader memory patterns
  - [Tutorial 14: Streaming & SSE](/docs/streaming_sse)
    - Real-time memory-efficient responses
  - [Tutorial 18: Events & Observability](/docs/events_observability)
    - Monitoring compaction events

- **Working Implementation**:
  - `til_implementation/til_context_compaction_20250119/`

**Use Case**: "I need to reduce token costs in long conversations"

---

## Blog Post Cross-References

### Blog: The Multi-Agent Pattern: Managing Complexity (Oct 14, 2025)

**Links To:**

- **Related TILs**:
  - [TIL: Pause & Resume Invocations](/docs/til/til_pause_resume_20251020)
    - Implement state management in multi-agent handoffs
  - [TIL: Context Compaction](/docs/til/til_context_compaction_20250119)
    - Manage token costs across orchestrator + sub-agent
      communication

- **Related Tutorials**:
  - [Tutorial 04: Sequential Workflows](/docs/sequential_workflows)
    - Ordered agent pipelines
  - [Tutorial 05: Parallel Processing](/docs/parallel_processing)
    - Concurrent agent execution
  - [Tutorial 06: Multi-Agent Systems](/docs/multi_agent_systems)
    - Complex agent hierarchies
  - [Tutorial 07: Loop Agents](/docs/loop_agents)
    - Iterative refinement patterns

**Content Type**: Narrative analysis of multi-agent complexity patterns

**Audience**: Architects and experienced developers

---

### Blog: Deploy AI Agents: Production Strategies (Oct 17, 2025)

**Links To:**

- **Related TILs**:
  - [TIL: Pause & Resume Invocations](/docs/til/til_pause_resume_20251020)
    - Build resilient, fault-tolerant workflows
  - [TIL: Context Compaction](/docs/til/til_context_compaction_20250119)
    - Reduce costs in long-running production agents

- **Related Tutorials**:
  - [Tutorial 23: Production Deployment Strategies](/docs/production_deployment)
    - Comprehensive deployment guide
  - [Tutorial 22: Advanced Observability](/docs/advanced_observability)
    - Production monitoring

- **Related Blog Posts**:
  - [Tutorial Progress Update](/blog/tutorial-progress-october-2025)
    - Learning paths to production

**Content Type**: Practical deployment decision framework

**Audience**: Developers ready for production deployment

---

### Blog: Tutorial Progress Update (Oct 14, 2025)

**Links To:**

- **Related TILs**:
  - [TIL: Pause & Resume Invocations](/docs/til/til_pause_resume_20251020)
    - State management for Tutorials 08+
  - [TIL: Context Compaction](/docs/til/til_context_compaction_20250119)
    - Memory optimization for Tutorials 08+

- **All Tutorials** (See blog post for complete list)

- **Learning Paths Section**:
  - Beginner Path: Tutorials 1, 2, 8, 10
  - Intermediate Path: Tutorials 4-6, 11, 14
  - Advanced Path: Tutorials 15-21, 30

**Content Type**: Progress update with learning path recommendations

**Audience**: All developers seeking learning paths

---

### Blog: Welcome to ADK Training Hub (Oct 9, 2025)

**Links To:**

- **All Tutorials and Documentation**
- **Tutorial 01: Hello World Agent** - Starting point

**Content Type**: Project introduction

**Audience**: New visitors to the project

---

## Tutorial Relationships

### Foundation Tutorials (1-3)

- **Tutorial 01: Hello World Agent**
  - Related TILs: [TIL Index](/docs/til/til_index) (overview)
  - Related Blog: [Welcome to ADK Training Hub](/blog/welcome-to-adk-training-hub)
  - Next: Tutorial 02

- **Tutorial 02: Function Tools**
  - Prerequisite: Tutorial 01
  - Related TILs: None specific (foundational)
  - Next: Tutorial 03

- **Tutorial 03: OpenAPI Tools**
  - Prerequisite: Tutorials 01-02
  - Related TILs: None specific (foundational)
  - Next: Tutorial 04

### Workflow Orchestration (4-7)

- **Tutorial 04: Sequential Workflows**
  - Prerequisite: Tutorial 03
  - Related TILs: [TIL: Pause & Resume](/docs/til/til_pause_resume_20251020)
    - Checkpointing in pipelines
  - Related Blog: [Multi-Agent Pattern](/blog/multi-agent-pattern-complexity-management)
  - Next: Tutorial 05

- **Tutorial 05: Parallel Processing**
  - Prerequisite: Tutorial 04
  - Related Blog: [Multi-Agent Pattern](/blog/multi-agent-pattern-complexity-management)
  - Next: Tutorial 06

- **Tutorial 06: Multi-Agent Systems**
  - Prerequisite: Tutorials 04-05
  - Related TILs:
    - [TIL: Pause & Resume](/docs/til/til_pause_resume_20251020)
      - State in handoffs
    - [TIL: Context Compaction](/docs/til/til_context_compaction_20250119)
      - Orchestrator efficiency
  - Related Blog: [Multi-Agent Pattern](/blog/multi-agent-pattern-complexity-management)
  - Next: Tutorial 07

- **Tutorial 07: Loop Agents**
  - Prerequisite: Tutorial 06
  - Related Blog: [Multi-Agent Pattern](/blog/multi-agent-pattern-complexity-management)
  - Next: Tutorial 08

### Production Foundations (8-12)

- **Tutorial 08: State & Memory Management**
  - Prerequisite: Tutorial 07
  - Related TILs:
    - [TIL: Pause & Resume](/docs/til/til_pause_resume_20251020)
      - Checkpoint state
    - [TIL: Context Compaction](/docs/til/til_context_compaction_20250119)
      - Memory efficiency
  - Related Blog: [Deploy AI Agents](/blog/deploy-ai-agents)
    - State in production
  - Next: Tutorial 09

- **Tutorial 09: Callbacks & Guardrails**
  - Related TILs: None specific
  - Next: Tutorial 10

- **Tutorial 10: Evaluation & Testing**
  - Related TILs: None specific
  - Next: Tutorial 11

- **Tutorial 11: Built-in Tools & Grounding**
  - Related TILs: None specific
  - Next: Tutorial 12

- **Tutorial 12: Planners & Advanced Thinking**
  - Related TILs: None specific
  - Next: Tutorial 13

### Advanced Capabilities (13-21)

- **Tutorial 14: Streaming & SSE**
  - Related TILs: [TIL: Context Compaction](/docs/til/til_context_compaction_20250119)
    - Efficiency with streaming

- **Tutorial 15: Live API Audio**
  - Related TILs: None specific

- **Tutorial 16: MCP Integration**
  - Related TILs: None specific

- **Tutorial 17: Agent-to-Agent Communication**
  - Related TILs: [TIL: Pause & Resume](/docs/til/til_pause_resume_20251020)
    - State preservation in distributed systems

- **Tutorial 18: Events & Observability**
  - Related TILs:
    - [TIL: Pause & Resume](/docs/til/til_pause_resume_20251020)
      - Checkpoint events
    - [TIL: Context Compaction](/docs/til/til_context_compaction_20250119)
      - Compaction events

### UI Integration (29-30)

- **Tutorial 30: Next.js & CopilotKit Integration**
  - Related TILs: [TIL: Context Compaction](/docs/til/til_context_compaction_20250119)
    - Frontend efficiency
  - Related Blog: [Deploy AI Agents](/blog/deploy-ai-agents)
    - Full-stack deployment

---

## Learning Paths by Content Type

### Path 1: Fastest Way to Production (6 hours)

1. **Read**: [Blog: Deploy AI Agents](/blog/deploy-ai-agents) (15 min)
2. **Do**: [Tutorial 01: Hello World Agent](/docs/hello_world_agent) (30 min)
3. **Read**: [TIL: Pause & Resume](/docs/til/til_pause_resume_20251020) (10 min)
4. **Do**: [Tutorial 08: State & Memory](/docs/state_memory) (2 hours)
5. **Read**: [TIL: Context Compaction](/docs/til/til_context_compaction_20250119)
   (10 min)
6. **Do**: [Tutorial 23: Production Deployment](/docs/production_deployment)
   (3 hours)

**Outcome**: Production-ready agent deployed to cloud

---

### Path 2: Understanding Patterns (8 hours)

1. **Read**: [Blog: Multi-Agent Pattern](/blog/multi-agent-pattern-complexity-management)
   (30 min)
2. **Do**: [Tutorial 04: Sequential Workflows](/docs/sequential_workflows)
   (1.5 hours)
3. **Do**: [Tutorial 05: Parallel Processing](/docs/parallel_processing)
   (1.5 hours)
4. **Do**: [Tutorial 06: Multi-Agent Systems](/docs/multi_agent_systems)
   (2 hours)
5. **Read**: [TIL: Pause & Resume](/docs/til/til_pause_resume_20251020) (10 min)
6. **Do**: [Tutorial 07: Loop Agents](/docs/loop_agents) (1.5 hours)

**Outcome**: Deep understanding of orchestration patterns

---

### Path 3: Full Mastery (30+ hours)

1. Read [Blog: Welcome](/blog/welcome-to-adk-training-hub)
2. Read [Blog: Tutorial Progress Update](/blog/tutorial-progress-october-2025)
   for learning paths
3. Follow Beginner Path (Tutorials 1-2, 8, 10)
4. Follow Intermediate Path (Tutorials 4-6, 11, 14)
5. Follow Advanced Path (Tutorials 15-21, 30)
6. Explore TILs for specific features as needed:
   - [TIL: Pause & Resume](/docs/til/til_pause_resume_20251020)
   - [TIL: Context Compaction](/docs/til/til_context_compaction_20250119)

**Outcome**: Expert-level understanding and production deployment capability

---

## Content Type Comparison

| Aspect | TIL | Blog | Tutorial | Mental Model |
|--------|-----|------|----------|--------------|
| **Scope** | Single feature | Opinion/analysis | Complete topic | Architecture |
| **Time** | 5-10 min | 15-30 min | 1-2 hours | 20-30 min |
| **Format** | Reference | Narrative | Step-by-step | Conceptual |
| **Code** | Quick snippet | Long example | Full project | Diagrams |
| **Update** | Rarely | Occasionally | As needed | Quarterly |
| **Frequency** | Weekly | Monthly | Completed | As needed |

---

## Navigation Tips

### For Developers

**"I want to learn one thing today"**
→ Pick a [TIL](/docs/til/til_index) based on what you need

**"I want to understand why patterns work"**
→ Read a [Blog Post](/blog) for narrative explanation

**"I want to build something real"**
→ Follow a [Tutorial](/docs/hello_world_agent)

**"I want to become an expert"**
→ Combine all three types using the learning paths above

### For Teachers

**Teaching a team about multi-agent systems:**

1. Share [Blog: Multi-Agent Pattern](/blog/multi-agent-pattern-complexity-management)
2. Have them do [Tutorial 06: Multi-Agent Systems](/docs/multi_agent_systems)
3. Reference specific TILs as they implement features

**Teaching about production deployment:**

1. Share [Blog: Deploy AI Agents](/blog/deploy-ai-agents)
2. Point to [TIL: Pause & Resume](/docs/til/til_pause_resume_20251020)
   for state management
3. Direct to [Tutorial 23: Production Deployment](/docs/production_deployment)

---

## Contributing Cross-References

When creating new content:

### For TILs

- Link to related TILs in "See Also" section
- Link to related tutorials
- Link to blog posts covering broader topics

### For Blog Posts

- Link to related TILs in "See Also" section
- Link to detailed tutorials
- Link to other blog posts on related topics

### For Tutorials

- Link to relevant TILs at the end
- Reference blog posts for architectural context
- Link to related tutorials for deeper learning

---

## Content Calendar

| Month | Content | Type |
|-------|---------|------|
| Oct 2025 | Pause & Resume | TIL |
| Oct 2025 | Context Compaction | TIL |
| Oct 2025 | Multi-Agent Pattern | Blog |
| Oct 2025 | Deploy AI Agents | Blog |
| Nov 2025 | Upcoming TILs (5+) | TIL |
| Nov 2025 | Production Deployment | Tutorial |
| Dec 2025 | Best Practices | Blog |

---

## Questions?

See the [TIL Index](/docs/til/til_index) or individual content pages for
comments and discussion.

---

**Last Updated**: October 20, 2025  
**Maintained by**: ADK Training Team
