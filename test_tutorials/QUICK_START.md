# Tutorial Testing - Quick Start Guide

**Fast track to running the ADK tutorial tests**

---

## ⚡ Quick Start (Under 5 Minutes)

### 1. Prerequisites

```bash
# Check Python version (need 3.10+)
python --version

# Install pytest
pip install pytest httpx
```

### 2. Run All Tests

```bash
cd test_tutorials
python run_all_tests.py
```

That's it! The test runner will:
- ✅ Find all tutorial tests automatically
- ✅ Run pytest for each tutorial
- ✅ Generate colorful terminal report
- ✅ Save JSON report to `test_report.json`

---

## 📁 What's Available

### ✅ Fully Tested Tutorials

| Tutorial | What It Tests | Tests | Status |
|----------|--------------|-------|---------|
| **Tutorial 29** | Quickstart agent with AG-UI | 8 tests | ✅ Ready |
| **Tutorial 30** | Customer support agent (3 tools) | 40+ tests | ✅ Ready |

### ⏳ Coming Soon

- Tutorial 31: Vite + Pandas (data analysis)
- Tutorial 32: Streamlit (direct integration)
- Tutorial 33: Slack bot
- Tutorial 34: Pub/Sub (event-driven)
- Tutorial 35: Advanced AG-UI (research agent)

---

## 🧪 Run Individual Tutorial Tests

### Tutorial 29 - Quickstart

```bash
cd tutorial29_test/backend

# Setup (first time only)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run tests
pytest test_agent.py -v
```

### Tutorial 30 - Customer Support

```bash
cd tutorial30_test/backend

# Setup (first time only)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add: GOOGLE_API_KEY=your_key

# Run all tests
pytest test_agent.py -v

# Run specific test class
pytest test_agent.py::TestKnowledgeBaseSearch -v
pytest test_agent.py::TestOrderStatusLookup -v
```

---

## 🎯 What Gets Tested

### Tutorial 29 (8 tests)
- ✅ FastAPI server & endpoints
- ✅ CORS configuration
- ✅ CopilotKit endpoint registration
- ✅ Agent initialization
- ✅ Health checks

### Tutorial 30 (40+ tests)
- ✅ **Knowledge Base Search** (5 tests)
  - Refund policy, shipping, warranty, account
  - Fallback handling
  
- ✅ **Order Lookup** (5 tests)
  - 3 test orders with different statuses
  - Case-insensitive search
  - Error handling

- ✅ **Support Tickets** (4 tests)
  - Priority handling
  - Unique ID generation
  - Ticket creation workflow

- ✅ **API & Integration** (26+ tests)
  - FastAPI configuration
  - CORS for multiple origins
  - Agent configuration
  - All tools working together

---

## 🐛 Troubleshooting

### Error: `ModuleNotFoundError: No module named 'ag_ui_adk'`

**Solution**:
```bash
pip install ag_ui_adk
```

⚠️ **NOT** `adk-middleware` (that package doesn't exist!)

### Error: `ImportError: cannot import name 'LlmAgent'`

**Solution**:
```bash
pip install --upgrade google-genai>=1.15.0
```

### Tests pass but agent doesn't respond

**Cause**: Missing or invalid Google API key

**Solution**:
```bash
export GOOGLE_API_KEY="your_actual_api_key_here"
```

Get your key at: https://aistudio.google.com/

### CORS errors in browser

**Check**:
- Backend runs on port 8000: `python agent.py`
- Frontend runs on port 3000 (Next.js) or 5173 (Vite)
- CORS origins match in `agent.py`

---

## 📊 Expected Output

### Successful Test Run

```
================================================================================
                       ADK Tutorial Test Runner                                
================================================================================

Checking Prerequisites
----------------------
✅ Python 3.10.0 found
✅ pytest 7.4.0 found

Found 2 Tutorial Test(s)
------------------------
ℹ️  Tutorial 29: tutorial29_test
ℹ️  Tutorial 30: tutorial30_test

Running Tests for Tutorial 29
------------------------------
✅ Tutorial 29 tests passed

Running Tests for Tutorial 30
------------------------------
✅ Tutorial 30 tests passed

================================================================================
                          Test Results Summary                                 
================================================================================

Overall Summary:
  Total Tutorials: 2
  Successful:      2
  Failed:          0

Test Statistics:
  Tests Passed:    48
  Tests Failed:    0
  Total Duration:  5.23s

✅ Report saved to test_report.json
```

---

## 📚 Documentation

Each tutorial test has detailed documentation:

- `tutorial29_test/backend/README.md` - Tutorial 29 guide
- `tutorial30_test/backend/README.md` - Tutorial 30 guide
- `test_tutorials/README.md` - Master documentation
- `test_tutorials/TESTING_SUMMARY.md` - Comprehensive summary

---

## 🚀 Next Steps

### To Run the Actual Agent

After tests pass, run the agent server:

```bash
cd tutorial30_test/backend
python agent.py
```

Server starts at `http://localhost:8000`

Test it:
```bash
curl http://localhost:8000/health
```

### To Test with Frontend

See Tutorial 30 for full Next.js integration:
```bash
npx create-next-app@latest frontend --typescript --tailwind --app
cd frontend
npm install @copilotkit/react-core @copilotkit/react-ui
# Update app/page.tsx with code from Tutorial 30
npm run dev
```

---

## ✅ Success Criteria

Your tests are working correctly if you see:

- ✅ All green checkmarks (✅)
- ✅ No red X marks (❌)
- ✅ Tests complete in < 10 seconds
- ✅ "Report saved to test_report.json"

---

## 💡 Tips

1. **Run tests frequently** - Catch issues early
2. **Read test output** - Errors are usually clear
3. **Check READMEs** - Each tutorial has specific docs
4. **Use virtual environments** - Keeps dependencies isolated
5. **Keep API key safe** - Never commit to git

---

## 📞 Get Help

1. Check individual tutorial READMEs
2. Review `TESTING_SUMMARY.md` for details
3. Look at `ERRATA.md` for known corrections
4. Check test output for specific error messages

---

**Created**: January 2025  
**Status**: ✅ 2 tutorials fully tested, 5 coming soon  
**Total Tests**: 48+ passing tests  
**Quick Start Time**: < 5 minutes
