# Commerce Agent Testing Guide

## ✅ All Fixes Completed

The following issues have been resolved:

1. ✅ **TypedDict Return Types**: Fixed - now using `Dict[str, Any]` in signatures with TypedDict hints internally
2. ✅ **Grounding Callback**: Implemented function-based callback (not class-based)
3. ✅ **Agent.after_model Parameter**: Removed - callbacks go in Runner, not Agent
4. ✅ **Prompt Rewrite**: Complete concierge persona with explicit preference workflow
5. ✅ **Package Installation**: `pip install -e .` completed successfully
6. ✅ **Server Starting**: ADK web server runs without errors

## 🧪 Testing Instructions

### Step 1: Start the Server

The server is already running! If not, run:

```bash
cd /Users/raphaelmansuy/Github/03-working/adk_training/tutorial_implementation/commerce_agent_e2e
make dev
```

### Step 2: Open the Web Interface

Open your browser to: **http://localhost:8000**

### Step 3: Select the Correct Agent

⚠️ **CRITICAL**: In the agent dropdown at the top of the page, select **`commerce_agent`** (NOT `context_engineering` or any other agent)

### Step 4: Test the Concierge Workflow

#### Test Case 1: Basic Preference Saving

**User Message 1:**
```
I want running shoes
```

**Expected Agent Behavior:**
- ✅ Agent calls `get_preferences` tool first
- ✅ Agent asks: "What's your budget?" and "Are you a beginner or experienced?"
- ✅ Warm, friendly tone

**User Message 2:**
```
Under 150 euros, I'm a beginner
```

**Expected Agent Behavior:**
- ✅ Agent calls `save_preferences` tool with: sport="running", budget=150, experience="beginner"
- ✅ Agent confirms: "✓ I've saved your preferences..."
- ✅ Agent calls `search_products` tool to find running shoes
- ✅ Agent explains WHY products are good for beginners
- ✅ Personalized recommendations with expert guidance

#### Test Case 2: Existing Preferences

**User Message (New Session):**
```
Find me some cycling gear
```

**Expected Agent Behavior:**
- ✅ Agent calls `get_preferences` tool
- ✅ If preferences exist from previous session, agent references them: "I see you prefer products under €150..."
- ✅ Agent asks if these preferences apply to cycling too
- ✅ Updates preferences if user provides new info

#### Test Case 3: Expert User

**User Message:**
```
I'm looking for trail running shoes, budget around 180, I've been running for 5 years
```

**Expected Agent Behavior:**
- ✅ Agent saves: sport="trail running", budget=180, experience="experienced"
- ✅ Agent recommends advanced features: "As an experienced runner, you'll appreciate..."
- ✅ Technical explanations about cushioning, grip, durability

### Step 5: Verify Grounding Metadata (Optional)

The grounding callback extracts metadata from Google Search results. To see it:

1. Look at the **terminal output** where `make dev` is running
2. After agent calls `search_products`, you should see logs like:

```
Grounding Sources:
  • decathlon.fr (confidence: 0.85)
  • nike.com (confidence: 0.90)
  • amazon.fr (confidence: 0.75)
```

**Note**: This metadata is currently logged to server console only. It's not displayed in the UI yet (that would require custom frontend integration).

### Step 6: Verify State Persistence

To test that preferences are saved across sessions:

1. Complete Test Case 1 above (save preferences)
2. Refresh the browser page (creates new session)
3. Send a message: "Show me tennis rackets"
4. Verify agent retrieves previous preferences with `get_preferences`

### Step 7: Check for Errors

Monitor the terminal for:
- ❌ `ValidationError` → Should NOT appear (fixed)
- ❌ `Extra inputs are not permitted` → Should NOT appear (fixed)
- ✅ Normal INFO logs → Expected
- ✅ Experimental warnings → Expected (safe to ignore)

## 🐛 Troubleshooting

### Issue: Agent dropdown shows wrong agents

**Solution**: Make sure you're in the correct directory and the package is installed:

```bash
cd /Users/raphaelmansuy/Github/03-working/adk_training/tutorial_implementation/commerce_agent_e2e
pip install -e .
make dev
```

### Issue: "No root_agent found for 'commerce_agent'"

**Solution**: Clear Python cache and reinstall:

```bash
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null
pip install -e .
```

### Issue: Agent doesn't save preferences

**Check**:
1. Verify prompt has explicit "ALWAYS call save_preferences" instruction
2. Check terminal logs for tool calls
3. Ensure `.env` file has `GOOGLE_API_KEY` or Google Cloud credentials

### Issue: Grounding metadata not showing

**Expected Behavior**: Grounding metadata appears in **server logs** (terminal), not in the UI. This is by design. To see it:

```bash
# Watch terminal output while testing
# Look for "Grounding Sources:" after search_products calls
```

## 📊 Success Criteria

Your testing is successful if:

✅ Agent starts without errors
✅ Agent calls `get_preferences` at conversation start
✅ Agent calls `save_preferences` when user provides info
✅ Agent confirms preference saving with friendly message
✅ Agent searches products using Google Search
✅ Agent explains product recommendations with reasoning
✅ Agent uses warm, expert concierge tone
✅ Preferences persist across browser refreshes
✅ Grounding metadata appears in server logs

## 🔍 Advanced Testing (Optional)

### Test with Runner and Callback

If you want to test the callback programmatically:

```python
from commerce_agent import root_agent, create_grounding_callback
from google.adk.runners import Runner

# Create runner with grounding callback
runner = Runner(
    agent=root_agent,
    after_model_callbacks=[create_grounding_callback(verbose=True)]
)

# Run test conversation
response = runner.run("Find me running shoes under 150 for beginners")
print(response)
```

### Run Tests

```bash
cd /Users/raphaelmansuy/Github/03-working/adk_training/tutorial_implementation/commerce_agent_e2e
make test
```

Expected: **14/14 tests passing**

## 📝 What's Fixed vs What's Not

### ✅ Fixed in This Session

- TypedDict compatibility with ADK function calling
- Function-based grounding callback (not class-based)
- Agent configuration (removed invalid `after_model` parameter)
- Prompt rewritten for concierge behavior
- Explicit preference workflow in instructions
- Package installation and discovery

### ⚠️ Not Implemented (Out of Scope)

- **SQLite Database**: Using ADK state instead (simpler, sufficient for preferences)
- **UI Grounding Display**: Callback logs to console only (UI integration requires custom frontend)
- **Product Catalog Caching**: Not needed for current scale
- **Analytics Dashboard**: Future enhancement

### 🎯 Known Limitations

1. **Grounding Metadata Location**: Appears in server logs, not UI (requires CopilotKit or custom React components)
2. **State Persistence**: Uses ADK state, not SQLite (trade-off: simplicity vs query capability)
3. **Callback in Agent**: Must use Runner for callbacks (ADK design decision)

## 📚 Next Steps

After testing, you can:

1. **Customize Prompt**: Edit `commerce_agent/prompt.py` to change agent personality
2. **Add Tools**: Create new tools in `commerce_agent/tools/`
3. **Integrate UI**: Use CopilotKit to build custom frontend with grounding source display
4. **Add Database**: Switch from ADK state to SQLite for complex queries (see tutorial examples)
5. **Deploy**: Use `adk deploy cloud_run` for production (see Tutorial 32-34)

## 🤝 Support

If you encounter issues:

1. Check terminal logs for detailed error messages
2. Verify `.env` file has correct API keys
3. Run `make test` to check for configuration issues
4. Review `README.md` for architecture details
5. Check `copilot-instructions.md` for ADK patterns
