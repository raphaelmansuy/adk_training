# Google ADK Training Project - AI Coding Guidelines

## Project Overview

This is a comprehensive training repository for Google Agent Development Kit (ADK), featuring 28 tutorials, mental models, research, and automated testing. The project teaches agent development from first principles to production deployment.


## Architecture Patterns

### Agent Hierarchy & Composition

- **Root Agent Convention**: Every agent module must export a `root_agent` variable as the main entry point
- **Sequential Workflows**: Use `SequentialAgent` for ordered pipelines where each step depends on the previous
- **Parallel Workflows**: Use `ParallelAgent` for independent tasks that can run simultaneously
- **Loop Workflows**: Use `LoopAgent` for iterative refinement with critic/refiner patterns
- **State Communication**: Agents communicate via `output_key` (saves to session state) and state interpolation `{key_name}`

### Tool Development Patterns

- **Function Tools**: Python functions become callable tools - return structured dicts with `status`, `report`, and data fields
- **OpenAPI Tools**: Use `OpenAPIToolset` for REST API integration with automatic tool generation
- **MCP Tools**: Use `MCPToolset` for standardized protocol tools (filesystem, databases)
- **Return Format**: Tools return `{'status': 'success/error', 'report': 'human readable', ...data}`

### State Management

- **Session State**: `state['key']` for conversation-scoped data
- **User State**: `state['user:key']` for cross-session user data
- **App State**: `state['app:key']` for global application data
- **Temporary State**: `state['temp:key']` for invocation-only data

## Development Workflow

### Project Structure

```
tutorial_implementation/tutorialXX/
├── Makefile              # Standard commands (setup, dev, test, demo)
├── requirements.txt      # Python dependencies
├── agent_name/           # Agent implementation
│   ├── __init__.py
│   ├── agent.py          # Main agent (exports root_agent)
│   └── .env.example      # Environment variables
└── tests/                # Comprehensive test suite
    ├── test_agent.py     # Agent configuration tests
    ├── test_imports.py   # Import validation
    └── test_structure.py # Project structure tests
```

### Testing Patterns

- **Unit Tests**: Mock external dependencies, test agent configuration and tool logic
- **Integration Tests**: Test with real ADK components when GOOGLE_API_KEY available
- **Test Organization**: Group by functionality (TestAgentConfig, TestTools, TestIntegration)
- **Test Runner**: Use `pytest` with `pytest-cov` for coverage reporting

### Common Commands

```bash
# Setup environment
make setup              # Install dependencies
export GOOGLE_API_KEY=your_key

# Development
make dev                # Start ADK web interface (localhost:8000)
make demo               # Show demo prompts and usage

# Testing
make test               # Run all tests
pytest tests/ -v        # Detailed test output

# Cleanup
make clean              # Remove cache files and artifacts
```

## Today I Learn (TIL) - Quick Feature Learning

### TIL Locations

**Documentation**: `/docs/docs/til/`
- `til_index.md` - Index of all available TILs
- `til_context_compaction_20250119.md` - Context Compaction feature
- `til_pause_resume_20251020.md` - Pause and Resume Invocations
- `til_rubric_based_tool_use_quality_20251021.md` - Tool Use Quality evaluation
- `TIL_TEMPLATE.md` - Guidelines for creating new TILs

**Implementations**: `/til_implementation/`
- `til_context_compaction_20250119/` - Full working example with tests
- `til_pause_resume_20251020/` - Full working example with tests
- `til_rubric_based_tool_use_quality_20251021/` - Full working example with tests

### TIL Structure

Each TIL has two components:

1. **Documentation** (`docs/docs/til/til_[feature]_[YYYYMMDD].md`)
   - Docusaurus frontmatter (id, title, sidebar_label, tags, etc.)
   - Quick problem statement (why it matters)
   - 5-10 minute read format
   - Working code examples
   - Key concepts (3-5 main ideas)
   - Use cases and best practices
   - Link to working implementation

2. **Implementation** (`til_implementation/til_[feature]_[YYYYMMDD]/`)
   - Agent module with root_agent export
   - 3-5 tools demonstrating the feature
   - Complete test suite (~19 tests)
   - Makefile (setup, test, dev, demo, clean)
   - README with detailed documentation
   - `.env.example` for configuration

### Creating a New TIL

1. **Create Documentation**
   - Copy `docs/docs/til/TIL_TEMPLATE.md`
   - Add frontmatter with proper metadata
   - Write 5-10 minute focused guide
   - Include working code examples
   - Reference the implementation

2. **Create Implementation**
   - Create `til_implementation/til_[feature]_[YYYYMMDD]/`
   - Use pattern from existing TILs (context compaction or pause/resume)
   - Include agent, tools, tests, Makefile, README
   - Ensure all tests pass

3. **Register in Docusaurus**
   - Add entry to `docs/sidebars.ts` under TIL category
   - Update `docs/docs/til/til_index.md` with new TIL info
   - Set correct `sidebar_position` (incremental)

### TIL Naming Convention

- Files: `til_[feature_name]_[YYYYMMDD].md`
- Directories: `til_[feature_name]_[YYYYMMDD]/`
- IDs: `til_[feature_name]_[YYYYMMDD]`
- Examples:
  - `til_context_compaction_20250119.md`
  - `til_pause_resume_20251020.md`

### TIL Best Practices

- **Quick reads**: Aim for 5-10 minutes (500-800 words in doc)
- **Working examples**: Always include copy-paste ready code
- **One feature focus**: Don't mix multiple features in one TIL
- **Link to implementation**: Reference the working example
- **Test coverage**: Implementation should have ~15-20 tests
- **Dated**: Include publication date for reference tracking

## Integration Points

### UI Frameworks

- **Next.js**: Use CopilotKit for React integration (`/api/copilotkit` endpoint)
- **Vite**: Similar CopilotKit setup with different build configuration
- **Streamlit**: Direct ADK integration without CopilotKit middleware
- **FastAPI Backend**: Standard REST API with CORS configuration for frontend origins

### External Services

- **Google ADK**: Core agent framework with Gemini models
- **CopilotKit**: React component library for AI chat interfaces
- **Google Cloud**: Vertex AI, Cloud Run, Cloud Storage for production deployment
- **Google Search**: Built-in grounding tool for web search capabilities

## Code Conventions

### Agent Definition

```python
# Standard agent pattern
root_agent = Agent(
    name="agent_name",                    # snake_case, descriptive
    model="gemini-2.5-flash",            # Use latest Gemini models
    description="What this agent does",  # Clear, concise description
    instruction="Detailed behavior...",  # Comprehensive prompt
    tools=[tool1, tool2],                # List of tool functions
    output_key="result_key"              # Optional: save to state
)
```

### Tool Functions

```python
def tool_name(param: Type) -> Dict[str, Any]:
    """
    Docstring explaining what the tool does.

    Args:
        param: Description of parameter

    Returns:
        Dict with status, report, and data fields
    """
    try:
        # Tool logic here
        result = {...}
        return {
            'status': 'success',
            'report': 'Human-readable success message',
            'data': result
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': 'Human-readable error message'
        }
```

### Workflow Composition

```python
# Sequential pipeline
sequential_agent = SequentialAgent(
    name="PipelineName",
    sub_agents=[agent1, agent2, agent3],  # Execute in order
    description="What the pipeline does"
)

# Parallel execution
parallel_agent = ParallelAgent(
    name="ParallelName",
    sub_agents=[agent1, agent2, agent3],  # Execute simultaneously
    description="What the parallel tasks do"
)

# Iterative refinement
loop_agent = LoopAgent(
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=5,  # Prevent infinite loops
    description="Iterative improvement process"
)
```

## Key Files & Directories

- `overview.md`: Mental models and architectural concepts
- `docs/tutorial/`: 28 comprehensive tutorials (01_hello_world_agent.md through 34_pubsub_adk_integration.md)
- `tutorial_implementation/`: Executable code for each tutorial
- `research/`: ADK source code analysis and integration examples
- `test_tutorials/`: Automated testing framework with 70+ tests
- `https://github.com/google/adk-python`: Official ADK source code and documentation

## Deployment Options

- **Local Development**: `adk web` for interactive development
- **Cloud Run**: `adk deploy cloud_run` for serverless production
- **Vertex AI Agent Engine**: `adk deploy agent_engine` for managed enterprise deployment
- **GKE**: `adk deploy gke` for custom Kubernetes infrastructure

## Quality Standards

- **Error Handling**: All tools return structured error responses
- **Documentation**: Comprehensive docstrings for all public functions
- **Testing**: 100% test coverage for implemented tutorials
- **State Safety**: Use appropriate state scopes (temp, session, user, app)
- **Performance**: Prefer parallel execution for independent tasks

## Common Patterns to Avoid

- Don't create agents without proper error handling in tools
- Don't use generic Exception catching - be specific
- Don't hardcode API keys - use environment variables
- Don't create infinite loops in LoopAgent - always set max_iterations
- Don't mix state scopes inappropriately (session data in app scope)

## Getting Help

- Read `overview.md` first for mental models and decision frameworks
- Check `docs/tutorial/XX_tutorial_name.md` for detailed implementation guides
- Run `make demo` in any tutorial directory for quick examples
- Use `adk web` for interactive experimentation
- Check `test_tutorials/` for working examples and test patterns

## Tips and lessons learned

- Always pipe your command with cat to avoid issues with certain shells example, to avoid pagination issues in zsh:

```bash
ls -la | cat
```

- If you are not sure seek the truth in ./research where we have the complete source code of ADK and associated projects. You can also check the official documentation of each project and Github repositories.
- Never edit or producte .env files directly in the repository. Always use .env.example as a template and create your own .env file for local development.

### ADK Agent Discovery (Critical for Web Interface)

**Problem**: `adk web agent_name` fails to load agents in the web interface.

**Root Cause**: ADK requires agents to be installed as Python packages to be discoverable.

**Solution**:

1. Create `setup.py` in tutorial root directory:

```python
from setuptools import setup, find_packages

setup(
    name="agent_name",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["google-genai>=1.15.0"],
)
```

2. Update Makefile setup command:

```makefile
setup:
	pip install -r requirements.txt
	pip install -e .  # Installs agent as discoverable package
```

3. Use `adk web` (not `adk web agent_name`) to show agent dropdown in web interface.

**Key Difference from Tutorial 01**: Tutorial 01 uses `pip install -e .` and `adk web` dropdown, while initial Tutorial 10 tried `adk web support_agent` which doesn't work without package installation.

**Learned During**: Tutorial 10 implementation - agent couldn't be selected in ADK web interface until proper package installation was implemented.

## What you must ensure

- If you want to report what you have done, updated or achieve never report that in the tutorial or in the implementation. It must be done in a ./log directory at the root of the project. Make it in consice way.

Use path: ./log/YYYYMMDD_HHMMSS_description_of_your_change.md

- Never commit any file that contains secrets or API keys.

- Prefer a pyproject instead of a setup.py file.


- To avoid pagination in zsh always pipe your command with cat like this:

```bash
cd /Users/raphaelmansuy/Github/03-working/adk_training && python -c "
from mcp.types import SamplingCapability
print('SamplingCapability:', SamplingCapability)
help(SamplingCapability)
" | cat
```

- Always use the latest version of ADK and associated libraries. Check the official documentation and Github repositories for the latest versions.

- When generating multi-line shell commands using heredocs (e.g., << 'EOF' ... EOF), always ensure the closing EOF delimiter starts exactly at column 0 (no leading spaces or tabs). For indented code blocks, use <<- 'EOF' instead, and indent content/delimiter with tabs only (not spaces). Review and unindent the delimiter before suggesting execution.

- VERY Important: Avoid using heredoc (<< 'EOF' ... EOF or similar) in shell commands for writing multi-line files (e.g., cat > file.py << 'EOF'), as it often causes terminal hangs/crashes in VSCode due to indentation issues. Instead, suggest pasting code directly into the editor, using echo 'multi-line code' | sed 's/^/  /' > file.py for simple cases, or tools like printf for escaped multi-line output.


## Recommendation you must follow

- Always read the documentation about how to write good documentation: docs/docs/skills/how_to_write_good_documentation.md and ensure that all your documentations follow the guidelines.

## ⚠️ CRITICAL: Heredoc (EOF) Causes PTY Host Disconnect

**RULE: NEVER use heredoc syntax (`<< 'EOF'` ... `EOF`) in VSCode integrated terminal.**

Heredoc commands trigger immediate PTY host disconnect in VSCode. This is a VSCode terminal limitation with multi-line input handling.

### What NOT to Do (Causes Crash)

```bash
# ❌ DON'T DO THIS - Causes PTY disconnect
cat > file.py << 'EOF'
# Multi-line content here
print("hello")
EOF
```

**Result**: PTY host disconnect error, terminal unusable.

### What TO Do Instead (Safe Alternatives)

**Option 1: Use echo with printf (Recommended)**

```bash
# ✅ DO THIS INSTEAD
printf 'line1\nline2\nline3\n' > file.py
```

**Option 2: Use printf with escape sequences**

```bash
# ✅ Safe multi-line approach
printf 'line1\nline2\nline3\n' > script.sh
chmod +x script.sh
```

**Option 3: Paste directly into editor**

```bash
# ✅ Use VSCode editor
# 1. Open file: code path/to/file.py
# 2. Paste content directly in editor
# 3. Save with Cmd+S
# 4. Done - no PTY issues
```

**Option 4: Use separate file + copy**

```bash
# ✅ Create content outside VSCode, then copy
# 1. Create file in external terminal or editor
# 2. Copy to project: cp ~/Desktop/content.txt ./file.py
# 3. No PTY involvement
```

### If PTY Disconnect Happens

```bash
# 1. Restart VSCode terminal
# Terminal > New Terminal (Cmd+Shift+`)

# 2. Or close and reopen VSCode
Command+Q  # Close VSCode
# Reopen it
```

## Running Expensive Builds (Docusaurus Build)

⚠️ **CRITICAL: NEVER run `npm run build` from VSCode integrated terminal**

This will cause PTY host disconnect. It is an architectural limitation of VSCode's PTY emulation, not a configuration issue.

### ⚠️ FINAL SOLUTION: Close VSCode, Use External Terminal (ONLY 100% Effective Method)

**After extensive testing, the ONLY way to prevent PTY disconnects is:**

```bash
# STEP 1: Close VSCode completely
Command+Q  # OR quit VSCode from menu

# STEP 2: Open external terminal
open -a Terminal  # macOS Terminal
# OR iTerm2

# STEP 3: Run build with proper isolation
export NODE_OPTIONS=--max-old-space-size=4096
cd /Users/raphaelmansuy/Github/03-working/adk_training/docs
nohup npm run build > build.log 2>&1 &

# STEP 4: Monitor build progress
tail -f build.log

# STEP 5: After build completes, reopen VSCode
open -a "Visual Studio Code" /Users/raphaelmansuy/Github/03-working/adk_training
```

**Why closing VSCode is the ONLY solution:**

The PTY disconnect issue is not a build problem—it's a **VSCode terminal architecture limitation**:

1. VSCode integrated terminal uses PTY emulation layer (not native PTY)
2. This emulation layer has resource limits and timeout mechanisms
3. Complex process trees (webpack with 4-8 workers) exceed these limits
4. VSCode times out and sends SIGINT signal
5. Shell process dies → PTY connection orphaned
6. "PTY host disconnect" error occurs
7. **NO VSCode settings or configurations can fix this** (it's architectural)

The ONLY ways to avoid it:

- ✅ **Option A (BEST)**: Close VSCode, run build in external terminal
- ✅ **Option B (ACCEPTABLE)**: Keep VSCode but run build in external terminal (separate processes)
- ❌ **Option C (DOESN'T WORK)**: Run from VSCode tasks/terminal (PTY still involved)
- ❌ **Option D (DOESN'T WORK)**: VSCode settings changes (can't override architecture)
- ❌ **Option E (DOESN'T WORK)**: Different build commands (all use PTY if run from VSCode)

### Typical Build Workflow (SAFE - Prevents All Crashes)

**Complete step-by-step process (only guaranteed safe method):**

**Step 1: Close VSCode**

```bash
# Close VSCode completely from dock or use:
Command+Q
```

**Step 2: Open External Terminal**

```bash
# Press Command+Space and type: Terminal
# Press Enter to open macOS Terminal
# OR use iTerm2, which is more stable
```

**Step 3: Set Node.js Memory**

```bash
# Set Node.js memory allocation
export NODE_OPTIONS=--max-old-space-size=4096

# Verify memory is set
echo $NODE_OPTIONS
```

**Step 4: Run the Build**

```bash
# Navigate to docs directory
cd /Users/raphaelmansuy/Github/03-working/adk_training/docs

# Run build with proper output capture
set -o pipefail; rm -rf build && npm run build 2>&1 | tail -100
BUILD_STATUS=$?

# Check result
echo "Build exit status: $BUILD_STATUS"
```

**Step 5: Verify Build Completed**

```bash
# Check if build succeeded
if [ -d "build" ] && [ -f "build/index.html" ]; then
  echo "✅ Build successful"
  find build -name "*.html" | wc -l  # Should show 225+
else
  echo "❌ Build failed"
  exit 1
fi
```

**Step 6: Verify Links After Build**

```bash
# From project root, verify all internal links
cd ..
python3 scripts/verify_links.py --skip-external

# Expected: Success Rate 99%+
```

**Step 7: Reopen VSCode**

```bash
# Once build complete and verified, reopen VSCode
open -a "Visual Studio Code" /Users/raphaelmansuy/Github/03-working/adk_training

# VSCode will be fresh and responsive
# All build artifacts are cached, next VSCode session is fast
```

**Complete One-Liner (for experienced users):**

```bash
export NODE_OPTIONS=--max-old-space-size=4096 && \
cd /Users/raphaelmansuy/Github/03-working/adk_training/docs && \
set -o pipefail; rm -rf build && npm run build 2>&1 | tail -100 && \
cd .. && \
python3 scripts/verify_links.py --skip-external
```

**Key Success Indicators:**

✅ Build completes with exit status 0
✅ 225 HTML files generated in `docs/build`
✅ Link verification shows 99%+ success rate
✅ No broken links reported
✅ VSCode remains responsive (if open separately)
✅ No terminal hangs or crashes
✅ No "PTY host disconnect" error

**Step 2: Run the Build (with memory and isolation)**

```bash
# Navigate to docs directory and run build
cd /Users/raphaelmansuy/Github/03-working/adk_training/docs

# Option A: Synchronous build (simple, blocks terminal)
set -o pipefail; rm -rf build && npm run build 2>&1 | tail -100
BUILD_STATUS=$?

# Option B: Asynchronous build (advanced, continue working)
set -o pipefail; rm -rf build && npm run build 2>&1 | tail -100 &!
BUILD_PID=$!
```

**Step 3: Monitor Build Progress (if async)**

```bash
# Check if build is still running
ps -p $BUILD_PID

# Wait for completion
wait $BUILD_PID
BUILD_STATUS=$?

# Or check job status
jobs -l
```

**Step 4: Verify Build Success**

```bash
# Check build exit status (0 = success, non-zero = failure)
echo "Build status: $BUILD_STATUS"

# Verify build artifacts exist
ls -lh docs/build/index.html  # Should exist

# Check total HTML files generated
find docs/build -name "*.html" | wc -l  # Should show 225+
```

**Step 5: Validate All Links**

```bash
# Quick check (internal links only, fast)
python3 scripts/verify_links.py --skip-external

# Full check (includes external URLs, slower)
python3 scripts/verify_links.py

# Export report for analysis
python3 scripts/verify_links.py --json-output links_report.json
```

**Step 6: Review Results**

```bash
# View broken links count
grep "Success Rate" <(python3 scripts/verify_links.py --skip-external)

# If JSON was generated, examine it
cat links_report.json | head -50

# Expected: Success Rate: 99.9% or higher
```

**Complete One-Liner (for experienced users):**

```bash
export NODE_OPTIONS=--max-old-space-size=4096 && \
cd /Users/raphaelmansuy/Github/03-working/adk_training/docs && \
rm -rf build && npm run build 2>&1 | tail -100 && \
cd .. && python3 scripts/verify_links.py --skip-external
```

**Key Success Indicators:**

✅ Build completes with exit status 0
✅ 225 HTML files generated in `docs/build`
✅ Link verification shows 99%+ success rate
✅ No broken links reported
✅ VSCode remains responsive (if open)
✅ No terminal hangs or crashes

**If Something Goes Wrong:**

| Problem | Solution |
|---------|----------|
| Build fails (non-zero status) | Check `npm run build` output, look for compilation errors |
| Links verify but show broken | Run full verification with: `python3 scripts/verify_links.py` |
| Memory issues (build slow/hangs) | Increase NODE_OPTIONS: `--max-old-space-size=6144` |
| VSCode crashes during build | Ensure separate terminal used, VSCode not minimized helps |
| File not found errors | Verify docs directory exists: `ls docs/package.json` |
| Links remain broken after build | Check copilot-instructions.md for known issues |

### Link Verification After Build

After a successful Docusaurus build, verify all internal links:

```bash
# Quick internal link check (fast)
python3 scripts/verify_links.py --skip-external

# Full link verification including external URLs (slow, makes network requests)
python3 scripts/verify_links.py

# Export results to JSON for analysis
python3 scripts/verify_links.py --json-output links_report.json
```

See `scripts/verify_links.py` for full documentation and options.