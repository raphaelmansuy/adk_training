# Tutorial 10: Evaluation & Testing - Support Agent
# Comprehensive evaluation framework for ADK agents

.PHONY: help setup dev test test-cov eval clean demo

# Default target - show help
help:
	@echo "🚀 Tutorial 10: Evaluation & Testing - Support Agent"
	@echo ""
	@echo "Quick Start Commands:"
	@echo "  make setup     - Install dependencies"
	@echo "  make dev       - Start the support agent"
	@echo "  make demo      - Show demo prompts and usage"
	@echo ""
	@echo "Advanced Commands:"
	@echo "  make test      - Run all tests"
	@echo "  make test-cov  - Run tests with coverage report"
	@echo "  make eval      - Run evaluation tests"
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
	@echo "🤖 Starting Support Agent..."
	@echo "📱 Open http://localhost:8000 in your browser"
	@echo "🎯 Select 'support_agent' from the dropdown"
	@echo ""
	@echo "💡 Try these support scenarios:"
	@echo "   • 'How do I reset my password?'"
	@echo "   • 'My account is locked, help!'"
	@echo "   • 'What's your refund policy?'"
	@echo "   • 'Check status of ticket TICK-12345678'"
	@echo ""
	adk web

# Run all tests
test: check-env
	@echo "🧪 Running tests..."
	pytest tests/ -v --tb=short

# Run tests with coverage
test-cov: check-env
	@echo "📊 Running tests with coverage..."
	pytest tests/ --cov=support_agent --cov-report=html
	@echo "📈 Coverage report generated in htmlcov/"

# Run evaluation tests
eval: check-env
	@echo "🔍 Running evaluation tests..."
	@echo "📋 Testing simple scenarios..."
	adk eval support_agent tests/simple.test.json
	@echo "🎫 Testing ticket creation..."
	adk eval support_agent tests/ticket_creation.test.json
	@echo "🏗️  Testing complex scenarios..."
	adk eval support_agent tests/complex.evalset.json
	@echo "✅ All evaluations complete!"

# Show demo prompts
demo:
	@echo "🎯 Support Agent Demo"
	@echo ""
	@echo "Try these support scenarios:"
	@echo "1. 'How do I reset my password?'"
	@echo "2. 'My account is locked, help!'"
	@echo "3. 'What's your refund policy?'"
	@echo "4. 'Check status of ticket TICK-12345678'"
	@echo ""
	@echo "💡 Run: make dev"
	@echo "🔬 Run: make eval  (for automated testing)"

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