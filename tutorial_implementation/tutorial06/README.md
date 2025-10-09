# Tutorial 06: Multi-Agent Systems - Content Publishing System

This implementation demonstrates sophisticated multi-agent orchestration by combining Sequential and Parallel agents in nested workflows. The content publishing system runs parallel research pipelines (news, social, expert) then creates content through sequential refinement (write, edit, format).

## Overview

The content publishing system showcases:

- **Nested Agent Orchestration**: Sequential agents inside Parallel agents
- **Multi-Phase Workflows**: Parallel research → Sequential content creation
- **State Management**: Complex data flow between nested agent layers
- **Production-Ready Architecture**: Real-world content generation pipeline

## Architecture

```
User Query: "Write article about AI in healthcare"
    ↓
┌─────────────────────────────────────────────────────────┐
│  PHASE 1: Parallel Research (3 Sequential Pipelines)    │
├─────────────────────────────────────────────────────────┤
│  News Pipeline:    fetch → summarize → news_summary     │
│  Social Pipeline:  monitor → analyze → social_insights  │ ← ALL RUN
│  Expert Pipeline:  find → extract → expert_quotes       │   AT ONCE!
└─────────────────────────────────────────────────────────┘
    ↓ (waits for ALL 3 to complete)
┌─────────────────────────────────────────────────────────┐
│  PHASE 2: Sequential Content Creation                   │
├─────────────────────────────────────────────────────────┤
│  Writer:    combines all research → draft_article       │
│  Editor:    reviews draft → edited_article              │ ← ONE AT
│  Formatter: adds markdown → published_article           │   A TIME
└─────────────────────────────────────────────────────────┘
    ↓
Final Output: Publication-ready article!
```

## Quick Start

1. **Install dependencies:**
   ```bash
   make setup
   ```

2. **Configure API key:**
   ```bash
   cp content_publisher/.env.example content_publisher/.env
   # Edit content_publisher/.env and add your Google AI API key
   ```

3. **Start development server:**
   ```bash
   make dev
   ```

4. **Open [http://localhost:8000](http://localhost:8000)** and select "content_publisher"

## Example Prompts

Try these prompts to see multi-agent orchestration in action:

- `"Write an article about artificial intelligence in healthcare"`
- `"Create an article about renewable energy adoption"`
- `"Write about the future of remote work"`
- `"Create an article explaining quantum computing breakthroughs"`

## How It Works

### Phase 1: Parallel Research
The system runs three research pipelines simultaneously:
- **News Pipeline**: Fetches current articles → Summarizes key points
- **Social Pipeline**: Monitors trends → Analyzes sentiment
- **Expert Pipeline**: Finds opinions → Extracts quotes

### Phase 2: Sequential Content Creation
After all research completes, content is created through sequential refinement:
- **Writer**: Synthesizes all research into a draft article
- **Editor**: Improves clarity, flow, and impact
- **Formatter**: Adds publication formatting and structure

### Performance Benefits
- **Without orchestration**: ~90 seconds (9 agents sequentially)
- **With multi-agent orchestration**: ~35 seconds (6 research agents parallel + 3 creation sequential)
- **Speedup**: ~2.6x faster with sophisticated parallel processing

## Implementation Details

### Agent Structure

```python
# Research pipelines (Sequential agents)
news_pipeline = SequentialAgent(
    name="NewsPipeline",
    sub_agents=[news_fetcher, news_summarizer]
)

social_pipeline = SequentialAgent(
    name="SocialPipeline",
    sub_agents=[social_monitor, sentiment_analyzer]
)

expert_pipeline = SequentialAgent(
    name="ExpertPipeline",
    sub_agents=[expert_finder, quote_extractor]
)

# Parallel research phase
parallel_research = ParallelAgent(
    name="ParallelResearch",
    sub_agents=[news_pipeline, social_pipeline, expert_pipeline]
)

# Sequential content creation
content_publishing_system = SequentialAgent(
    name="ContentPublishingSystem",
    sub_agents=[
        parallel_research,  # Phase 1: Research
        article_writer,     # Phase 2: Write
        article_editor,     # Phase 3: Edit
        article_formatter   # Phase 4: Format
    ]
)
```

### State Flow

1. **Parallel Research** saves to state:
   - `news_summary` (from news pipeline)
   - `social_insights` (from social pipeline)
   - `expert_quotes` (from expert pipeline)

2. **Sequential Creation** reads from state:
   - Writer: `{news_summary}`, `{social_insights}`, `{expert_quotes}`
   - Editor: `{draft_article}`
   - Formatter: `{edited_article}`

## Testing

Run the comprehensive test suite:

```bash
make test
```

Tests cover:
- ✅ Individual agent configurations (9 agents)
- ✅ Sequential pipeline structures (3 pipelines)
- ✅ Parallel research orchestration
- ✅ Complete system integration
- ✅ State management and data flow
- ✅ Import validation and module structure
- ✅ Project file organization

## Development

### Project Structure

```
tutorial06/
├── content_publisher/           # Agent implementation
│   ├── __init__.py             # Package initialization
│   ├── agent.py                # Multi-agent system definition
│   └── .env.example            # Environment template
├── tests/                      # Comprehensive test suite
│   ├── __init__.py
│   ├── test_agent.py           # Agent and pipeline tests (57 tests)
│   ├── test_imports.py         # Import validation tests
│   └── test_structure.py       # Project structure tests
├── requirements.txt            # Python dependencies
├── Makefile                   # Development commands
└── README.md                  # This documentation
```

### Key Files

- **`content_publisher/agent.py`**: Complete multi-agent orchestration
- **`tests/test_agent.py`**: 57 comprehensive tests
- **`Makefile`**: `make setup`, `make test`, `make dev`, `make demo` commands

## Learning Outcomes

After completing this tutorial, you'll understand:

- ✅ **Nested Agent Orchestration**: Sequential inside Parallel agents
- ✅ **Multi-Phase Workflows**: Parallel research + sequential creation
- ✅ **Complex State Management**: Data flow in nested architectures
- ✅ **Production Architectures**: Real-world content generation patterns
- ✅ **Performance Optimization**: Strategic parallelization for speed

## Real-World Applications

This multi-agent pattern is perfect for:

- **Content Platforms**: Research → Write → Edit → Publish
- **Data Analysis**: Gather data (parallel) → Process → Synthesize → Report
- **E-Commerce**: Product research + pricing + reviews (parallel) → Compare → Recommend
- **Customer Support**: Classify → Research solutions → Draft → Review → Respond
- **Financial Analysis**: Market data + news + sentiment (parallel) → Analyze → Report
- **Code Generation**: Design + Implement + Test + Document + Review

## Troubleshooting

### Common Issues

**"Agents in parallel phase seem sequential"**
- Check Events tab for actual start times
- May be rate-limited by API

**"Writer missing research data"**
- Verify pipeline agents have `output_key` set
- Check `{key}` syntax in writer instruction

**"Complex to debug nested agents"**
- Test each pipeline individually first
- Use Events tab to trace execution flow
- Add descriptive agent names

### Debug Mode

Enable detailed logging:

```bash
ADK_LOG_LEVEL=DEBUG make dev
```

## Next Steps

- **Tutorial 07**: Loop Agents - Iterative refinement for quality
- **Advanced Patterns**: Error handling, conditional routing, dynamic pipelines
- **Production Deployment**: Scaling multi-agent systems for high-throughput applications

## Contributing

This implementation follows the established tutorial pattern:

1. **Working Code First**: Complete implementation before documentation
2. **Comprehensive Testing**: 57+ tests covering all functionality
3. **User-Friendly Setup**: Simple `make setup && make dev` workflow
4. **Clear Documentation**: Step-by-step guides and architecture explanations

## Links

- **Tutorial**: [Tutorial 06: Multi-Agent Systems](../../docs/tutorial/06_multi_agent_systems.md)
- **ADK Documentation**: google.github.io/adk-docs/
- **Previous Tutorial**: [Tutorial 05 Implementation](../tutorial05/)

---

*Built with ❤️ for the ADK community*