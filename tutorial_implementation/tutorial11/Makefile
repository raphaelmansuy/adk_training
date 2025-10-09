# Tutorial 11: Built-in Tools & Grounding - Grounding Agent
# Demonstrates web grounding with Google Search and built-in ADK tools

.PHONY: help setup dev test test-cov clean demo

# Default target - show help
help:
	@echo "🚀 Tutorial 11: Built-in Tools & Grounding - Grounding Agent"
	@echo ""
	@echo "Quick Start Commands:"
	@echo "  make setup     - Install dependencies"
	@echo "  make dev       - Start the grounding agent"
	@echo "  make demo      - Show demo prompts and usage"
	@echo ""
	@echo "Advanced Commands:"
	@echo "  make test      - Run all tests"
	@echo "  make test-cov  - Run tests with coverage report"
	@echo "  make clean     - Clean up generated files"
	@echo ""
	@echo "💡 First time? Run: make setup && make dev"

# Setup environment
setup:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Setup complete! Run 'make dev' to start the agent."

# Start development server
dev: check-env
	@echo "🔍 Starting Grounding Agent..."
	@echo "📱 Open http://localhost:8000 in your browser"
	@echo "🎯 Select 'research_assistant' from the dropdown"
	@echo ""
	@echo "💡 Try these research scenarios:"
	@echo "   • 'What are the latest developments in AI for 2025?'"
	@echo "   • 'Research quantum computing breakthroughs'"
	@echo "   • 'Find current information about renewable energy'"
	@echo "   • 'Analyze recent developments in space exploration'"
	@echo ""
	adk web

# Run all tests
test: check-env
	@echo "🧪 Running tests..."
	pytest tests/ -v --tb=short

# Run tests with coverage
test-cov: check-env
	@echo "📊 Running tests with coverage..."
	pytest tests/ --cov=grounding_agent --cov-report=html
	@echo "📈 Coverage report generated in htmlcov/"

# Show demo prompts
demo:
	@echo "🔍 Grounding Agent Demo"
	@echo ""
	@echo "Try these research scenarios:"
	@echo "1. 'What are the latest AI developments?'"
	@echo "2. 'Research current trends in electric vehicles'"
	@echo "3. 'Find information about recent space missions'"
	@echo "4. 'Analyze developments in renewable energy'"
	@echo ""
	@echo "💡 Run: make dev"
	@echo "🧪 Run: make test (for automated testing)"

# Clean up cache files
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .coverage -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete!"

# Check environment (internal use)
check-env:
	@if [ -z "$$GOOGLE_API_KEY" ] && [ -z "$$GOOGLE_APPLICATION_CREDENTIALS" ]; then \
		echo "❌ Error: Authentication not configured"; \
		echo ""; \
		echo "Choose one of the following authentication methods:"; \
		echo ""; \
		echo "🔑 Method 1 - API Key (Gemini API):"; \
		echo "   export GOOGLE_API_KEY=your_api_key_here"; \
		echo "   Get a free key at: https://aistudio.google.com/app/apikey"; \
		echo ""; \
		echo "🔐 Method 2 - Service Account (VertexAI):"; \
		echo "   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json"; \
		echo "   export GOOGLE_CLOUD_PROJECT=your_project_id"; \
		echo "   export GOOGLE_CLOUD_LOCATION=us-central1"; \
		echo ""; \
		echo "Note: Maps grounding requires VertexAI (Method 2)"; \
		echo ""; \
		exit 1; \
	fi