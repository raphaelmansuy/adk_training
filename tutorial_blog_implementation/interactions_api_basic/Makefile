.PHONY: help setup clean test demo dev

help:
	@echo "Interactions API Basic - Available Commands"
	@echo "============================================"
	@echo ""
	@echo "make setup       Install dependencies and prepare environment"
	@echo "make test        Run unit tests"
	@echo "make demo        Run interactive demonstration"
	@echo "make clean       Remove cache files and artifacts"
	@echo ""

setup:
	pip install -r requirements.txt
	pip install -e .
	cp interactions_basic_agent/.env.example interactions_basic_agent/.env 2>/dev/null || true
	@echo ""
	@echo "✅ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Add your GOOGLE_API_KEY to interactions_basic_agent/.env"
	@echo "   Or set: export GOOGLE_API_KEY='your-key-here'"
	@echo "2. Run 'make test' to validate the implementation"
	@echo "3. Run 'make demo' to see Interactions API in action"
	@echo ""

test:
	@echo ""
	@echo "🧪 Running Interactions API Tests..."
	@echo ""
	@pytest tests/ -v --tb=short
	@echo ""
	@echo "✅ Tests validate:"
	@echo "   • API client configuration"
	@echo "   • Tool definitions"
	@echo "   • Import paths"
	@echo ""

demo:
	@echo ""
	@echo "🚀 Running Interactions API Demo..."
	@echo ""
	@echo "This demo shows:"
	@echo "  1. Basic text interaction"
	@echo "  2. Stateful conversation with previous_interaction_id"
	@echo "  3. Streaming responses"
	@echo "  4. Function calling"
	@echo ""
	python -m interactions_basic_agent.demo
	@echo ""

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .coverage htmlcov build dist *.egg-info
	@echo "✅ Cleaned up cache files"
