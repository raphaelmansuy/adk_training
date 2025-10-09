# Tutorial 05: Parallel Processing - Travel Planning System

This implementation demonstrates the **ParallelAgent** pattern and **fan-out/gather** technique for concurrent execution in ADK. The travel planner searches for flights, hotels, and activities in parallel, then merges the results into a complete itinerary.

## Overview

The travel planning system showcases:

- **ParallelAgent**: Concurrent execution of multiple agents
- **Fan-out/Gather Pattern**: Parallel data gathering + sequential synthesis
- **State Management**: Data flow between parallel and sequential agents
- **Real-world Performance**: 3x faster than sequential execution

## Architecture

```
text
User Query → ParallelAgent (3 concurrent searches)
               ├─ Flight Finder → state['flight_options']
               ├─ Hotel Finder → state['hotel_options']
               └─ Activity Finder → state['activity_options']
               ↓
          SequentialAgent (merge results)
               ↓
          Itinerary Builder → Final Travel Itinerary
```

## Quick Start

1. **Install dependencies:**

   ```bash
   make setup
   ```

2. **Configure API key:**

   ```bash
   cp travel_planner/.env.example travel_planner/.env
   # Edit travel_planner/.env and add your Google AI API key
   ```

3. **Start development server:**

   ```bash
   make dev
   ```

4. **Open [http://localhost:8000](http://localhost:8000)** and select "travel_planner"

## Example Prompts

Try these prompts to see parallel processing in action:

- `"Plan a 3-day trip to Paris"`
- `"Weekend getaway to New York with cultural activities"`
- `"5-day Tokyo trip for 2 people, budget-friendly"`
- `"Relaxing week in Bali with beach activities"`

## How It Works

### Parallel Execution

The system uses `ParallelAgent` to run three searches simultaneously:

- **Flight Finder**: Searches for available flights
- **Hotel Finder**: Finds suitable accommodations
- **Activity Finder**: Recommends local attractions

### Sequential Synthesis

After all parallel searches complete, `SequentialAgent` runs the:

- **Itinerary Builder**: Merges all results into a complete travel plan

### Performance Benefits

- **Sequential**: ~30 seconds (3 agents × 10 seconds each)
- **Parallel**: ~10 seconds (all 3 run concurrently)
- **Result**: 3x faster execution for I/O-bound tasks

## Implementation Details

### Agent Structure

```python
# Parallel search agents
flight_finder = Agent(name="flight_finder", output_key="flight_options")
hotel_finder = Agent(name="hotel_finder", output_key="hotel_options")
activity_finder = Agent(name="activity_finder", output_key="activity_options")

# Parallel execution
parallel_search = ParallelAgent(
    name="ParallelSearch",
    sub_agents=[flight_finder, hotel_finder, activity_finder]
)

# Sequential merge
itinerary_builder = Agent(
    name="itinerary_builder",
    instruction="...{flight_options}...{hotel_options}...{activity_options}..."
)

# Complete pipeline
travel_planning_system = SequentialAgent(
    sub_agents=[parallel_search, itinerary_builder]
)
```

### State Flow

1. Parallel agents save results to state with `output_key`
2. Itinerary builder reads from state using `{key}` syntax
3. Data flows: Parallel → State → Sequential → Output

## Testing

Run the comprehensive test suite:

```bash
make test
```

Tests cover:

- ✅ Agent configurations and instructions
- ✅ ParallelAgent structure and sub-agents
- ✅ SequentialAgent pipeline flow
- ✅ State management and data injection
- ✅ Import and module structure
- ✅ Project file organization

## Development

### Project Structure

```
text
tutorial05/
├── travel_planner/           # Agent implementation
│   ├── __init__.py          # Package initialization
│   ├── agent.py             # Agent definitions and pipeline
│   └── .env.example         # Environment template
├── tests/                   # Comprehensive test suite
│   ├── __init__.py
│   ├── test_agent.py        # Agent and pipeline tests
│   ├── test_imports.py      # Import validation tests
│   └── test_structure.py    # Project structure tests
├── requirements.txt         # Python dependencies
├── Makefile                # Development commands
└── README.md               # This documentation
```

### Key Files

- **`travel_planner/agent.py`**: Complete agent implementation
- **`tests/test_agent.py`**: 50+ comprehensive tests
- **`Makefile`**: User-friendly development commands

## Learning Outcomes

After completing this tutorial, you'll understand:

- ✅ **ParallelAgent** for concurrent execution
- ✅ **Fan-out/gather pattern** for real-world workflows
- ✅ **Performance optimization** through parallelism
- ✅ **State management** between parallel and sequential agents
- ✅ **Pipeline design** combining different agent types

## Real-World Applications

This pattern is perfect for:

- **Data Gathering**: Search multiple APIs simultaneously
- **Content Generation**: Create variations concurrently
- **Analysis Tasks**: Run different analyses on same data
- **Validation**: Check multiple conditions simultaneously
- **Research**: Gather information from diverse sources

## Troubleshooting

### Common Issues

**"Agents seem to run sequentially"**

- Check Events tab - they should start simultaneously
- May be limited by API rate limits

**"Itinerary builder missing data"**

- Verify parallel agents have `output_key` defined
- Check `{key}` syntax in itinerary instruction

**"Performance not improved"**

- Parallel speedup depends on task type
- I/O-bound tasks benefit most from parallelism

### Debug Mode

Enable detailed logging:

```bash
ADK_LOG_LEVEL=DEBUG make dev
```

## Next Steps

- **Tutorial 06**: Multi-Agent Systems - Combine Sequential and Parallel patterns
- **Advanced Patterns**: Error handling, conditional flows, nested parallelism
- **Production Deployment**: Scaling parallel agents for high-throughput applications

## Contributing

This implementation follows the established tutorial pattern:

1. **Working Code First**: Complete implementation before documentation
2. **Comprehensive Testing**: 50+ tests covering all functionality
3. **User-Friendly Setup**: Simple `make setup && make dev` workflow
4. **Clear Documentation**: Step-by-step guides and examples

## Links

- **Tutorial**: [Tutorial 05: Parallel Processing](../../docs/tutorial/05_parallel_processing.md)
- **ADK Documentation**: google.github.io/adk-docs/
- **Previous Tutorial**: [Tutorial 04 Implementation](../tutorial04/)

---

_Built with ❤️ for the ADK community_
