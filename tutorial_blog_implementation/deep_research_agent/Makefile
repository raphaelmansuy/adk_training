.PHONY: help setup clean test demo research

help:
	@echo "Deep Research Agent - Available Commands"
	@echo "========================================="
	@echo ""
	@echo "make setup       Install dependencies and prepare environment"
	@echo "make test        Run unit tests"
	@echo "make demo        Run quick demonstration (mock mode)"
	@echo "make research    Run actual research task (requires API key)"
	@echo "make clean       Remove cache files and artifacts"
	@echo ""

setup:
	pip install -r requirements.txt
	pip install -e .
	cp research_agent/.env.example research_agent/.env 2>/dev/null || true
	@echo ""
	@echo "✅ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Add your GOOGLE_API_KEY to research_agent/.env"
	@echo "   Or set: export GOOGLE_API_KEY='your-key-here'"
	@echo "2. Run 'make test' to validate the implementation"
	@echo "3. Run 'make demo' to see a mock demonstration"
	@echo "4. Run 'make research' to run actual research (costs tokens!)"
	@echo ""

test:
	@echo ""
	@echo "🧪 Running Deep Research Agent Tests..."
	@echo ""
	@pytest tests/ -v --tb=short
	@echo ""
	@echo "✅ Tests validate:"
	@echo "   • Agent configuration"
	@echo "   • Research task creation"
	@echo "   • Streaming utilities"
	@echo "   • Error handling"
	@echo ""

demo:
	@echo ""
	@echo "🔬 Deep Research Agent Demo (Mock Mode)"
	@echo "========================================"
	@echo ""
	@echo "This shows the structure of Deep Research without API calls."
	@echo "Use 'make research' for actual research."
	@echo ""
	python -m research_agent.demo --mock
	@echo ""

research:
	@echo ""
	@echo "🔬 Running Deep Research Task"
	@echo "=============================="
	@echo ""
	@echo "⚠️  This will make actual API calls and consume tokens!"
	@echo ""
	python -m research_agent.demo
	@echo ""

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov build dist *.egg-info
	@echo "✅ Cleaned up cache files"
