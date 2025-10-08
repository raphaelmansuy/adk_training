# Tutorial 03: Chuck Norris OpenAPI Tools Agent
# Simple Makefile for getting started quickly

.PHONY: help setup dev test clean demo

# Default target - show help
help:
	@echo "🤠 Tutorial 03: Chuck Norris OpenAPI Tools Agent"
	@echo ""
	@echo "Quick Start Commands:"
	@echo "  make setup     - Install dependencies"
	@echo "  make dev       - Start the Chuck Norris agent"
	@echo "  make demo      - Run a quick demo"
	@echo ""
	@echo "Advanced Commands:"
	@echo "  make test      - Run all tests"
	@echo "  make clean     - Clean up generated files"
	@echo ""
	@echo "💡 First time? Run: make setup && make dev"

# Install dependencies
setup:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Setup complete! Run 'make dev' to start the agent."

# Start the Chuck Norris agent
dev: check-env
	@echo "🤠 Starting Chuck Norris Agent..."
	@echo "📱 Open http://localhost:8000 in your browser"
	@echo "🎯 Select 'chuck_norris_agent' from the dropdown"
	adk web

# Run a quick demo
demo: check-env
	@echo "🃏 Running Chuck Norris Demo..."
	@echo ""
	@echo "💬 Try these prompts in the ADK web UI:"
	@echo "   • 'Tell me a random Chuck Norris joke'"
	@echo "   • 'Find jokes about programming'"
	@echo "   • 'What categories are available?'"
	@echo "   • 'Give me a random dev joke'"
	@echo ""
	@echo "✅ Demo ready! Open http://localhost:8000"

# Run tests
test: check-env
	@echo "🧪 Running tests..."
	pytest tests/ -v --tb=short

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	@echo "✅ Cleanup complete!"

# Check environment (internal use)
check-env:
	@if [ -z "$$GOOGLE_API_KEY" ]; then \
		echo "❌ Error: GOOGLE_API_KEY environment variable not set"; \
		echo "   Please set it with: export GOOGLE_API_KEY=your_key_here"; \
		echo "   Get a free key at: https://aistudio.google.com/app/apikey"; \
		exit 1; \
	fi