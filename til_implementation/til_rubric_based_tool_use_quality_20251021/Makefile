.PHONY: help setup clean test demo dev evaluate

help:
	@echo "Tool Use Quality Evaluation TIL - Available Commands"
	@echo "====================================================="
	@echo ""
	@echo "make setup       Install dependencies and prepare environment"
	@echo "make test        Run unit tests (validates configuration)"
	@echo "make evaluate    Show LlmAsJudge with RUBRIC_BASED_TOOL_USE_QUALITY_V1"
	@echo "make dev         Launch ADK web interface to test tool use"
	@echo "make demo        Quick validation without web interface"
	@echo "make clean       Remove cache files and artifacts"
	@echo ""

setup:
	pip install -r requirements.txt
	pip install -e .
	cp tool_use_evaluator/.env.example tool_use_evaluator/.env
	@echo ""
	@echo "✅ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Add your GOOGLE_API_KEY to tool_use_evaluator/.env"
	@echo "2. Run 'make test' to validate the implementation"
	@echo "3. Run 'make dev' to launch web interface"
	@echo ""

dev:
	@echo ""
	@echo "🚀 Launching ADK web interface..."
	@echo ""
	@echo "📝 How to test Tool Use Quality:"
	@echo "   1. Open http://localhost:8000"
	@echo "   2. Select 'tool_use_evaluator'"
	@echo "   3. Try these prompts:"
	@echo ""
	@echo "   ✅ GOOD TOOL USAGE:"
	@echo "   'Analyze customer_data, extract features, validate quality, then apply random_forest model'"
	@echo ""
	@echo "   ❌ BAD TOOL USAGE (out of order):"
	@echo "   'Apply the model first, then analyze the data, then extract features'"
	@echo ""
	@echo "   ✅ GOOD TOOL SEQUENCE:"
	@echo "   'Analyze sales_data, extract important features, validate them, apply gradient_boosting'"
	@echo ""
	@echo "💡 What to observe:"
	@echo "   • Tool call sequence in Events tab"
	@echo "   • Whether tools are called in logical order"
	@echo "   • Whether prerequisites are met before dependent tools"
	@echo "   • Error handling when tools are misused"
	@echo ""
	@echo "🎯 Evaluation Focus:"
	@echo "   This agent demonstrates tool use quality concepts:"
	@echo "   - Tool sequencing (analyze → extract → validate → apply)"
	@echo "   - Tool dependencies (each step builds on previous)"
	@echo "   - Error handling (proper validation)"
	@echo "   - Efficiency (no skipped or redundant steps)"
	@echo ""
	adk web

test:
	@echo ""
	@echo "🧪 Running Tool Use Quality Evaluation Tests..."
	@echo ""
	@pytest tests/ -v --tb=short
	@echo ""
	@echo "✅ Tests validate:"
	@echo "   • Agent configuration (6 tests)"
	@echo "   • Tool functionality (8 tests)"
	@echo "   • Import paths (3 tests)"
	@echo "   • App structure (3 tests)"
	@echo ""
	@echo "📋 Test Coverage:"
	@echo "   ✓ Agent name, model, description, instruction"
	@echo "   ✓ Agent has all 4 tools: analyze, extract, validate, apply"
	@echo "   ✓ Agent has output_key configured"
	@echo "   ✓ Tool success and error cases"
	@echo "   ✓ Module imports and exports"
	@echo "   ✓ App configuration and initialization"
	@echo ""
	@echo "🔍 What each test verifies:"
	@echo "   Agent Configuration Tests:"
	@echo "     - Agent name: tool_use_evaluator"
	@echo "     - Model: gemini-2.0-flash"
	@echo "     - Instruction emphasizes proper tool sequencing"
	@echo "     - All 4 tools are available"
	@echo ""
	@echo "   Tool Functionality Tests:"
	@echo "     - analyze_data handles success and error cases"
	@echo "     - extract_features validates input"
	@echo "     - validate_quality checks prerequisites"
	@echo "     - apply_model requires both features and model"
	@echo ""
	@echo "   Import & Structure Tests:"
	@echo "     - Agent can be imported from package"
	@echo "     - App configuration is correct"
	@echo "     - Module exports are properly set up"
	@echo ""
	@echo "💡 To run specific test:"
	@echo "   pytest tests/test_agent.py::TestAgentConfiguration -v"
	@echo "   pytest tests/test_agent.py::TestToolFunctionality -v"
	@echo ""
	@echo "📊 To see test coverage:"
	@echo "   pytest tests/ --cov=tool_use_evaluator --cov-report=html"
	@echo ""

demo:
	@echo ""
	@echo "🔍 Quick validation..."
	python -c "from tool_use_evaluator import root_agent; from app import app; print('✅ Agent loaded:', root_agent.name); print('✅ App configured:', app.name); print('✅ Tools count:', len(root_agent.tools)); print('✅ Implementation ready!')"
	@echo ""
	@echo "🎯 Implementation is ready for evaluation!"
	@echo ""

evaluate:
	@echo ""
	@echo "📊 Demonstrating LlmAsJudge with RUBRIC_BASED_TOOL_USE_QUALITY_V1"
	@echo ""
	python evaluate_tool_use.py
	@echo ""

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov build dist *.egg-info
	@echo "✅ Cleaned up cache files"
