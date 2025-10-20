---
id: til_index
title: "Today I Learn - Quick Daily Insights"
description: "Short, focused articles on specific Google ADK features and patterns. 5-10 minute reads with working code examples."
sidebar_label: "📚 TIL Index"
sidebar_position: 1
tags: ["til", "index", "quick-learn"]
---

import Comments from '@site/src/components/Comments';

# Today I Learn (TIL) - Quick Daily Learning

Welcome to **Today I Learn** (TIL) - a collection of short, focused learning articles on specific Google ADK features and patterns.

## What are TILs?

TILs are **quick, practical guides** designed for busy developers who want to:
- ✅ Learn one specific feature or pattern
- ✅ Get working code examples
- ✅ Understand when to use it
- ✅ Move on (5-10 minute read)

Perfect for staying current with ADK features and integrating them into your projects.

## Available TILs

### Pause and Resume Invocations (October 20, 2025)

**📖 [TIL: Pause and Resume Invocations with Google ADK 1.16](/docs/til/til_pause_resume_20251020)**

Checkpoint agent state and resume execution later for long-running workflows,
human-in-the-loop interactions, and fault tolerance.

**Key Points:**

- �️ Fault tolerance - System failures don't cause work loss; resume from
  checkpoint
- 👤 Human-in-the-loop - Agent pauses to request feedback, then continues
- ⏱️ Long-running tasks - Complex workflows can pause at natural break points
- 🔄 Multi-agent handoff - State is preserved when handing off between agents
- 💾 State persistence - Complete execution context is saved automatically

**In 10 minutes you'll learn:**

1. Why pause/resume invocations matter
2. How state checkpointing works
3. State restoration on resumption
4. Configuration with ResumabilityConfig
5. Real-world use cases (data processing, approvals, fault tolerance)
6. Working implementation with tests

**ADK Version:** 1.16+  
**Complexity:** Intermediate  
**Time:** ~10 minutes

---

### Context Compaction (October 19, 2025)

**📖 [TIL: Context Compaction with Google ADK 1.16](/docs/til/til_context_compaction_20250119)**

Automatically summarize conversation history to reduce token usage in long-running agent conversations.

**Key Points:**
- � Save 70-90% on tokens in long conversations
- ⚡ Faster responses with smaller context
- 🧠 Intelligent summarization preserves key information
- 🔄 Perfect for 24-hour support agents and research assistants
- ⏰ Completely automatic and transparent

**In 8 minutes you'll learn:**
1. Why context compaction matters
2. How sliding window compaction works
3. LLM-based summarization approach
4. Configuration options
5. Real-world cost savings
6. Working implementation with tests

**ADK Version:** 1.16+  
**Complexity:** Intermediate  
**Time:** ~8 minutes

---

## Why TILs Instead of Full Tutorials?

| Aspect | TIL | Full Tutorial |
|--------|-----|--------------|
| **Scope** | One feature or pattern | Complete topic |
| **Time** | 5-10 minutes | 30-90 minutes |
| **Code** | Quick example | Full project |
| **Depth** | Surface-level | Comprehensive |
| **Use Case** | "Learn this TODAY" | "Master this topic" |

---

## Upcoming TILs

**Coming Soon:**

- **Context Caching** - Cache conversation prefixes to reduce API calls
- **Streaming Responses** - Real-time output for better UX
- **Error Recovery Patterns** - Handling and recovering from agent errors
- **Tool Composition** - Combining multiple tools effectively
- **Performance Tuning** - Optimizing agents for production

---

## How to Use TILs

### For Learning

1. Pick a TIL based on what you need today
2. Read through (5-10 minutes)
3. Run the working code example
4. Integrate into your project
5. Check related tutorials for deeper learning

### For Teaching

- Share specific TILs with your team when they need to learn a feature
- Link in code reviews: "See TIL: [Feature Name]"
- Combine multiple TILs to teach a workflow

### For Contributing

Want to create a TIL? See the [TIL Template & Guidelines](
/docs/til/til_template) for:

- Structure and format
- Best practices
- Submission process

---

## TIL Guidelines

Every TIL includes:

✅ **Clear problem statement** - What is the problem this solves?  
✅ **One-sentence explanation** - Understand it instantly  
✅ **Why it matters** - Concrete benefits  
✅ **Quick example** - Copy-paste ready code  
✅ **Key concepts** - 3-5 main ideas explained  
✅ **Use cases** - When to apply it  
✅ **Working implementation** - Full code with tests  
✅ **Configuration reference** - All options documented  
✅ **Pro tips** - Real-world advice  
✅ **When NOT to use it** - Important caveats  

---

## TIL vs Tutorials vs Blog Posts

**TIL:**

- Specific feature or pattern
- 5-10 minutes
- Working code example
- Published weekly
- Dated for reference

**Tutorial:**

- Broader topic or workflow
- 30-90 minutes
- Full project structure
- Comprehensive curriculum
- Timeless reference

**Blog Post:**

- Opinion, experience, or analysis
- Variable length
- Personal insights
- Published as needed
- Narrative-driven

---

## Related Reading

### Blog Posts on Related Topics

Explore deeper insights and narrative discussions about patterns and features:

- 📖 **[The Multi-Agent Pattern: Managing Complexity](/blog/multi-agent-pattern-complexity-management)**
  - Understanding complex system structure (relates to pause/resume workflows)
- 📖 **[Deploy AI Agents: Production Strategies](/blog/deploy-ai-agents)**
  - Deployment with fault tolerance and state management
- 📖 **[Multi-Agent Pattern Analysis](/blog/multi-agent-pattern-complexity-management)**
  - Cognitive load management in agent systems

**Recommended Learning Path:**

1. 📚 Read the relevant TIL (5-10 minutes)
2. 📖 Explore related blog post for deeper context (15-30 minutes)
3. 🧪 Run the TIL working implementation (10-20 minutes)
4. 📘 Dive into full tutorial for comprehensive mastery (1-2 hours)

---

## Stay Updated

### RSS Feed

Subscribe to the [ADK Training RSS Feed](/adk_training/blog/rss.xml)
to get notified when new TILs are published.

### Social

Follow for TIL announcements:

- 🐦 [@raphaelmansuy on Twitter/X](https://twitter.com/raphaelmansuy)
- 🐙 [GitHub Discussions](https://github.com/raphaelmansuy/adk_training/discussions)

### Weekly Schedule

New TILs are typically published:

- **Tuesdays** - Core ADK features
- **Fridays** - Integration patterns and tips

---

## TIL Template & Guidelines

Want to create a TIL for a feature you've learned about?

**[📋 See TIL Template & Guidelines](/docs/til/til_template)**

The template includes:

- Complete structure
- Best practices
- DO's and DON'Ts
- Publishing checklist

---

## Quick Navigation

- **[📚 All Tutorials](/docs/hello_world_agent)** - Comprehensive courses
- **[🧠 Mental Models](/docs/overview)** - Architecture and design
- **[📖 Blog](/blog)** - Articles and insights
- **[🐙 GitHub](https://github.com/raphaelmansuy/adk_training)** - Source code

---

## Questions?

- 💬 Comment below
- 🐛 [Report an issue](https://github.com/raphaelmansuy/adk_training/issues)
- 💡 [Suggest a TIL topic](https://github.com/raphaelmansuy/adk_training/discussions)

---

<Comments />
