# Tutorial 22: Model Selection & Optimization
# Framework for selecting and comparing AI models

.PHONY: help setup dev test test-cov clean demo

# Default target - show help
help:
	@echo "🚀 Tutorial 22: Model Selection & Optimization"
	@echo ""
	@echo "Quick Start Commands:"
	@echo "  make setup     - Install dependencies"
	@echo "  make dev       - Start the model selector agent"
	@echo "  make demo      - Show demo prompts and run standalone comparison"
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
	@echo "🤖 Starting Model Selector Agent..."
	@echo "📱 Open http://localhost:8000 in your browser"
	@echo "🎯 Select 'model_selector_agent' from the dropdown"
	@echo ""
	@echo "💡 Try these questions:"
	@echo "   • 'What model should I use for real-time voice chat?'"
	@echo "   • 'Compare gemini-2.5-flash and gemini-2.5-pro'"
	@echo "   • 'Tell me about gemini-2.5-flash-lite'"
	@echo "   • 'Which model is best for complex reasoning tasks?'"
	@echo ""
	adk web

# Run all tests
test: check-env
	@echo "🧪 Running tests..."
	pytest tests/ -v --tb=short

# Run tests with coverage
test-cov: check-env
	@echo "📊 Running tests with coverage..."
	pytest tests/ --cov=model_selector --cov-report=html
	@echo "📈 Coverage report generated in htmlcov/"

# Show demo prompts and run standalone comparison
demo: check-env
	@echo "🎯 Model Selection Demo"
	@echo ""
	@echo "=== Interactive Agent Mode ==="
	@echo "Run: make dev"
	@echo ""
	@echo "Try these questions in the web interface:"
	@echo "1. 'What model should I use for real-time voice chat?'"
	@echo "2. 'Compare gemini-2.5-flash and gemini-2.5-pro'"
	@echo "3. 'Tell me about gemini-2.5-flash-lite'"
	@echo "4. 'Which model is best for complex reasoning tasks?'"
	@echo ""
	@echo "=== Standalone Benchmark Mode ==="
	@echo "Running automated model comparison..."
	@echo ""
	python -m model_selector.agent

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
		echo "   Create credentials at: https://console.cloud.google.com/iam-admin/serviceaccounts"; \
		echo ""; \
		exit 1; \
	fi
