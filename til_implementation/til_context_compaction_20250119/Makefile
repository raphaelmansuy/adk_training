.PHONY: help setup clean test demo dev

help:
	@echo "Context Compaction TIL - Available Commands"
	@echo "==========================================="
	@echo ""
	@echo "make setup       Install dependencies and prepare environment"
	@echo "make test        Run unit tests (validates configuration)"
	@echo "make dev         Launch ADK web interface to see compaction in action"
	@echo "make demo        Quick validation without web interface"
	@echo "make clean       Remove cache files and artifacts"
	@echo ""

setup:
	pip install -r requirements.txt
	pip install -e .
	cp context_compaction_agent/.env.example context_compaction_agent/.env
	@echo ""
	@echo "✅ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Add your GOOGLE_API_KEY to context_compaction_agent/.env"
	@echo "2. Run 'make test' to validate the implementation"
	@echo "3. Run 'make dev' to launch web interface and test compaction"
	@echo ""

dev:
	@echo ""
	@echo "🚀 Launching ADK web interface..."
	@echo ""
	@echo "📝 How to test Context Compaction:"
	@echo "   1. Open http://localhost:8000"
	@echo "   2. Select 'context_compaction_agent'"
	@echo "   3. Send 5+ messages to trigger compaction"
	@echo "   4. Check each response's token count in the response"
	@echo ""
	@echo "💡 Token Growth Pattern:"
	@echo "   • Without compaction: ~180 tokens per interaction"
	@echo "   • With compaction: ~50-60 tokens per interaction"
	@echo "   • Look for stabilization after 5 interactions ✅"
	@echo ""
	@echo "🎯 Expected token progression:"
	@echo "   Message 1: ~180 | Message 2: ~243 | Message 3: ~295"
	@echo "   Message 4: ~347 | Message 5: ~405 ← Compaction triggers!"
	@echo ""
	adk web

test:
	@echo ""
	@echo "🧪 Running Context Compaction Tests..."
	@echo ""
	@pytest tests/ -v --tb=short
	@echo ""
	@echo "✅ Tests validate:"
	@echo "   • Agent configuration (7 tests)"
	@echo "   • Tool functionality (5 tests)"
	@echo "   • Import paths (3 tests)"
	@echo "   • App & compaction setup (4 tests)"
	@echo ""

demo:
	@echo ""
	@echo "🔍 Quick validation..."
	python -c "from context_compaction_agent import root_agent; from app import app; print('✅ Agent loaded:', root_agent.name); print('✅ App configured:', app.name); print('✅ Compaction enabled:', app.events_compaction_config is not None)"
	@echo ""
	@echo "🎯 Implementation is ready!"
	@echo ""

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov build dist *.egg-info
	@echo "✅ Cleaned up cache files"
