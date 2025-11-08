# Quick Fix: make dev Command

**Issue**: `make dev` failed with error "Invalid value for '[AGENTS_DIR]': Directory 'policy_navigator.agent' does not exist."

**Root Cause**: The Makefile's `dev` target was passing `policy_navigator.agent` as an argument to `adk web`, but:
- `adk web` expects a directory path or no argument (to scan current dir)
- `policy_navigator.agent` is not a valid directory
- The agent is already packaged and installed via `pip install -e .`

**Solution Applied**:
Changed Makefile line from:
```makefile
adk web policy_navigator.agent
```

To:
```makefile
adk web
```

**Why This Works**:
1. `adk web` without arguments automatically discovers agents in the current environment
2. The package is installed via `pip install -e .` in the `install` target
3. The `root_agent` is properly exported from `policy_navigator/__init__.py`
4. ADK automatically finds and displays agents in the web UI dropdown

**Verification**:
- ✅ `make dev` now starts successfully
- ✅ ADK web server starts on http://127.0.0.1:8000
- ✅ All 22 tests still passing
- ✅ No breaking changes to other commands

**Testing Results**:
```
✓ ADK Web Server started
✓ For local testing, access at http://127.0.0.1:8000
✓ Application startup complete
✓ All tests passing: 22/22
```

**Usage**:
```bash
make dev      # Now works! Starts web interface at http://localhost:8000
```
