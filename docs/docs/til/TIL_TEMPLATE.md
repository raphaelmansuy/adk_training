---
id: til_template
title: "TIL Template - How to Write a TIL"
description: "Template and guidelines for creating 'Today I Learn' articles focused on specific ADK features"
sidebar_label: "TIL Template"
sidebar_position: 1
tags: ["template", "guidelines", "til"]
status: "template"
difficulty: "reference"
---

import Comments from '@site/src/components/Comments';

# Today I Learn (TIL) Format Guide

## What is a TIL?

**Today I Learn (TIL)** articles are **short, focused learning pieces** that highlight a specific feature, pattern, or capability in Google ADK. Unlike comprehensive tutorials, TILs are:

- ✅ **Focused**: One feature, one pattern, one solution
- ✅ **Quick**: Readable in 5-10 minutes
- ✅ **Practical**: Working code examples with full implementation
- ✅ **Dated**: Published with a specific date for reference
- ✅ **Standalone**: Complete on their own, but linked to related content

## TIL File Structure

Each TIL should follow this naming convention:

```
til_[feature_name]_[YYYYMMDD].md

Examples:
- til_context_compaction_20250119.md
- til_streaming_responses_20250120.md
- til_error_handling_patterns_20250121.md
```

## TIL Markdown Template

```markdown
---
id: til_feature_name
title: "TIL: [Feature Name] in Google ADK [Version]"
description: "Quick guide to [feature]: what it is, why you need it, and how to use it"
sidebar_label: "TIL: [Feature Name]"
sidebar_position: [number]
tags: ["til", "quick-learn", "[feature-keyword]", "adk-[version]"]
keywords: ["adk", "[feature-keyword]", "short-tutorial", "learning"]
status: "completed"
difficulty: "beginner"
estimated_time: "5-10 minutes"
publication_date: "2025-01-19"
adk_version_minimum: "1.16"
implementation_link: "https://github.com/raphaelmansuy/adk_training/tree/main/til_implementation/til_feature_name_20250119"
---

import Comments from '@site/src/components/Comments';

## [Feature Name] - [Subtitle]

### What is [Feature]?

**In one sentence**: [Clear, concise explanation of what this feature does]

Example: "Context Compaction is a new ADK 1.16 feature that automatically
summarizes old conversation history to reduce token usage and costs."

## Why Should You Care?

**Problem it solves**:
- [Problem 1]
- [Problem 2]
- [Problem 3]

**Benefits**:
- ✅ [Benefit 1]
- ✅ [Benefit 2]
- ✅ [Benefit 3]

## Quick Example

Here's the simplest way to use [feature]:

\`\`\`python
# Quick example - just the essentials
code_example_here()
\`\`\`

## How It Works (3 Key Points)

### Point 1: [Concept]
[2-3 sentences explaining first concept]

### Point 2: [Concept]
[2-3 sentences explaining second concept]

### Point 3: [Concept]
[2-3 sentences explaining third concept]

## Common Use Cases

1. **Scenario A**: [When to use it]
   - Example application
   - Expected outcome

2. **Scenario B**: [When to use it]
   - Example application
   - Expected outcome

## Complete Working Code

See the full implementation with tests and configuration:

```bash
cd til_implementation/til_feature_name_20250119/
make setup
make test  # Run tests
make dev   # Launch development UI
```

**Files included**:

- `agent.py` - Complete working implementation
- `tests/` - Comprehensive test suite
- `Makefile` - Standard development commands
- `requirements.txt` - Dependencies
- `.env.example` - Configuration template

## Configuration Reference

Key parameters for [feature]:

| Parameter | Type | Default | Purpose |
|-----------|------|---------|---------|
| param1 | Type | value | What it does |
| param2 | Type | value | What it does |
| param3 | Type | value | What it does |

## Pro Tips

💡 **Tip 1**: [Practical tip for using this feature effectively]

💡 **Tip 2**: [Common gotcha and how to avoid it]

💡 **Tip 3**: [Performance or optimization consideration]

## When NOT to Use It

⚠️ **Avoid when**: [Scenario where this feature isn't appropriate]

⚠️ **Consider alternatives**: [Other patterns that might be better]

## Related Resources

- **Tutorial XX**: [Full tutorial on related topic]
- **Official Docs**: [Link to official documentation]
- **GitHub Examples**: [Link to example code]
- **Previous TIL**: [Link to related TIL]

## Testing It Out

Quick validation that everything works:

```bash
# From til_implementation/til_feature_name_20250119/
make test
```

You should see all tests passing ✅

## Next Steps

- 🚀 **Try the implementation** - Copy and modify for your use case
- 📖 **Read related tutorial** - Deep dive into [related topic]
- 💬 **Share feedback** - Comments below

## Key Takeaway

[One-paragraph summary of why this matters and how to remember it]

---

<Comments />
```

## TIL Directory Structure

Each TIL should have a corresponding implementation:

```
til_implementation/
├── til_feature_name_20250119/
│   ├── Makefile              # Standard commands (setup, dev, test, demo)
│   ├── requirements.txt      # Dependencies
│   ├── README.md             # Implementation guide
│   ├── agent_name/           # Agent implementation
│   │   ├── __init__.py
│   │   ├── agent.py          # Main agent (exports root_agent)
│   │   └── .env.example      # Environment variables template
│   └── tests/                # Comprehensive test suite
│       ├── test_agent.py     # Agent configuration tests
│       ├── test_imports.py   # Import validation
│       └── test_structure.py # Project structure tests
```

## TIL Best Practices

### DO ✅

- **Keep it focused** - One feature or pattern per TIL
- **Start with the "what"** - Clear problem statement
- **Show real code** - Copy-paste examples that actually work
- **Include tests** - Validate the implementation
- **Link to full impl** - Point readers to working code
- **Use active voice** - "You can use..." not "It is used..."
- **Include a one-liner** - Perfect for social sharing

### DON'T ❌

- **Don't explain history** - Focus on how to use it NOW
- **Don't duplicate tutorials** - TIL is different from Tutorial
- **Don't go too deep** - Save details for tutorials
- **Don't forget tests** - Validate everything works
- **Don't create multiple TILs** - One per feature is cleaner
- **Don't use jargon without explanation** - Assume some readers are new
- **Don't forget the implementation link** - That's the value add!

## TIL vs Tutorial

| Aspect | TIL | Tutorial |
|--------|-----|----------|
| **Length** | 500-1000 words | 1500-5000 words |
| **Time** | 5-10 minutes | 30-90 minutes |
| **Depth** | Surface-level | Comprehensive |
| **Code** | Simple example | Full project |
| **Focus** | One feature | Multiple concepts |
| **Purpose** | "Learn this TODAY" | "Master this topic" |
| **Update cadence** | Weekly | Monthly |

## Implementation Checklist

When creating a new TIL implementation:

- [ ] Create TIL markdown file following this template
- [ ] Create `til_implementation/til_[feature]_[date]/` directory
- [ ] Implement working `agent.py` with `root_agent` export
- [ ] Create `Makefile` with `setup`, `test`, `demo`, `dev` commands
- [ ] Add comprehensive tests in `tests/`
- [ ] Create `requirements.txt` with minimal dependencies
- [ ] Create `.env.example` with required variables
- [ ] Create `README.md` for the implementation
- [ ] Update `docs/sidebars.ts` to include TIL
- [ ] Create git commit with date-based log entry
- [ ] Update main README.md with TIL section

## Publishing a TIL

1. Create markdown file in `docs/til/`
2. Create implementation in `til_implementation/`
3. Update `docs/sidebars.ts`
4. Run tests: `make test` from implementation directory
5. Test locally: `adk web` from implementation directory
6. Commit with log entry: `./log/YYYYMMDD_HHMMSS_til_feature_name.md`
7. Push to GitHub

## Example: Minimal TIL

For reference, here's the shortest possible valid TIL:

```markdown
---
id: til_minimal_example
title: "TIL: Minimal Example"
description: "Minimal TIL structure"
sidebar_label: "TIL: Minimal Example"
tags: ["til"]
estimated_time: "5 minutes"
implementation_link: "https://github.com/raphaelmansuy/adk_training/tree/main/til_implementation/til_minimal"
---

# TIL: [Feature]

## What?
[One sentence]

## Code
\`\`\`python
# Minimal working example
\`\`\`

## Why?
[2-3 sentences on benefits]

## Full Implementation
See: [link to implementation]
```

---

**Need help creating a TIL?** Reference this template and check existing TIL examples!

<Comments />
