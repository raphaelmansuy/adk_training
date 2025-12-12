.PHONY: help setup clean test demo dev

help:
	@echo "ADK Interactions Integration - Available Commands"
	@echo "=================================================="
	@echo ""
	@echo "make setup       Install dependencies and prepare environment"
	@echo "make test        Run unit tests"
	@echo "make dev         Launch ADK web interface"
	@echo "make demo        Run demonstration"
	@echo "make clean       Remove cache files and artifacts"
	@echo ""

setup:
	pip install -r requirements.txt
	pip install -e .
	cp adk_interactions_agent/.env.example adk_interactions_agent/.env 2>/dev/null || true
	@echo ""
	@echo "✅ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Add your GOOGLE_API_KEY to adk_interactions_agent/.env"
	@echo "   Or set: export GOOGLE_API_KEY='your-key-here'"
	@echo "2. Run 'make test' to validate the implementation"
	@echo "3. Run 'make dev' to launch ADK web interface"
	@echo ""

dev:
	@echo ""
	@echo "🚀 Launching ADK Web Interface..."
	@echo ""
	@echo "📝 This agent demonstrates:"
	@echo "   • ADK with Interactions API backend"
	@echo "   • Server-side state management"
	@echo "   • Tool orchestration"
	@echo ""
	@echo "Open http://localhost:8000 and select 'adk_interactions_agent'"
	@echo ""
	adk web

test:
	@echo ""
	@echo "🧪 Running ADK Interactions Integration Tests..."
	@echo ""
	@pytest tests/ -v --tb=short
	@echo ""
	@echo "✅ Tests validate:"
	@echo "   • Agent configuration"
	@echo "   • Tool definitions"
	@echo "   • ADK integration patterns"
	@echo ""

demo:
	@echo ""
	@echo "🔬 ADK Interactions Integration Demo"
	@echo "====================================="
	@echo ""
	python -m adk_interactions_agent.demo
	@echo ""

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov build dist *.egg-info
	@echo "✅ Cleaned up cache files"
