---
mode: beastmode
---

## Your Task:

### Task 1: Implement Tutorial Implementations

- Follow the strict process outlined in `context_engineering/how_to_create_perfect_tutorial.md`.
- Source tutorials from the `docs/tutorial/` directory.
- Create implementations in the `tutorial_implementation/` directory, adhering to the project structure:
  - Each tutorial gets a `tutorial_implementation/tutorialXX/` folder (e.g., `tutorial01_hello_world_agent/`).
  - Include required files: `Makefile`, `requirements.txt`, `agent_name/` (with `__init__.py`, `agent.py` exporting `root_agent`), `.env.example`, and `tests/` (with `test_agent.py`, `test_imports.py`, `test_structure.py`).
  - Use `pyproject.toml` instead of `setup.py` for package installation (e.g., `pip install -e .` for ADK discoverability).
  - Implement agents with proper patterns: export `root_agent`, use appropriate workflows (SequentialAgent, ParallelAgent, LoopAgent), tools with structured returns, and state management.
  - Ensure comprehensive testing with pytest, covering unit, integration, and structure tests.
  - Log changes in `./log/YYYYMMDD_HHMMSS_description.md` (do not modify tutorials or implementations directly in logs).

### Task 2: Update Original Tutorials

- After implementation, update the corresponding tutorial files in `docs/tutorial/` to include a link to the working implementation (e.g., `[View Implementation](./../../tutorial_implementation/tutorialXX)`).
- Resolve any discrepancies found during implementation by updating the tutorial content for accuracy.
- Sequence: Complete Task 1 fully before proceeding to Task 2.

### Tutorials to Create:

- List specific tutorials here, e.g.:
  - tutorial01_hello_world_agent.md
  - tutorial02_simple_tool_agent.md
  - ... (add all 28 as needed)

### Additional Guidelines:

- Use latest Gemini models (e.g., "gemini-2.5-flash").
- Ensure tools return `{'status': 'success/error', 'report': '...', 'data': ...}`.
- Avoid common pitfalls: no hardcoded keys, specific exceptions, max_iterations in loops.
- Test with `make test` and demo with `make demo`.
- For ADK web interface, ensure package installation via `pyproject.toml` for agent discovery.
