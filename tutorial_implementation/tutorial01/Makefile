# Tutorial 01: Hello World Agent
# Simple Makefile for getting started quickly

.PHONY: help setup dev test clean demo

# Default target - show help
help:
	@echo "🚀 Tutorial 01: Hello World Agent"
	@echo ""
	@echo "Quick Start Commands:"
	@echo "  make setup     - Install dependencies"
	@echo "  make dev       - Start the hello agent"
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

# Start the hello agent
dev: check-env
	@echo "🤖 Starting Hello World Agent..."
	@echo "📱 Open http://localhost:8000 in your browser"
	@echo "🎯 Select 'hello_agent' from the dropdown"
	adk web

# Run a quick demo
demo: check-env
	@echo "� Running Hello World Demo..."
	@echo ""
	@echo "💬 Try these prompts in the ADK web UI:"
	@echo "   • 'Hello! Who are you?'"
	@echo "   • 'What can you do?'"
	@echo "   • 'Tell me a fun fact'"
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