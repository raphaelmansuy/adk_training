# Tutorial 25: Best Practices - Production-Ready Agent
# Demonstrating production patterns, security, and optimization

.PHONY: help setup dev test test-cov clean demo

# Default target - show help
help:
	@echo "🚀 Tutorial 25: Best Practices - Production-Ready Agent"
	@echo ""
	@echo "Quick Start Commands:"
	@echo "  make setup     - Install dependencies"
	@echo "  make dev       - Start the best practices agent"
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
	@echo "🤖 Starting Best Practices Agent..."
	@echo "📱 Open http://localhost:8000 in your browser"
	@echo "🎯 Select 'best_practices_agent' from the dropdown"
	@echo ""
	@echo "💡 Try these production scenarios:"
	@echo "   • 'Validate this email: user@example.com'"
	@echo "   • 'Process order with retry logic: ORD-123'"
	@echo "   • 'Show me the system health metrics'"
	@echo "   • 'Demonstrate circuit breaker with failing service'"
	@echo "   • 'Batch process these items: A, B, C'"
	@echo ""
	adk web

# Run all tests
test: check-env
	@echo "🧪 Running tests..."
	pytest tests/ -v --tb=short

# Run tests with coverage
test-cov: check-env
	@echo "📊 Running tests with coverage..."
	pytest tests/ --cov=best_practices_agent --cov-report=html --cov-report=term
	@echo "📈 Coverage report generated in htmlcov/"

# Show demo prompts
demo:
	@echo "🎯 Best Practices Agent Demo"
	@echo ""
	@echo "Production Pattern Demonstrations:"
	@echo ""
	@echo "1. Input Validation:"
	@echo "   'Validate this email: user@example.com'"
	@echo "   'Validate this email: invalid-email'"
	@echo ""
	@echo "2. Error Handling & Retry:"
	@echo "   'Process order with retry: ORD-123'"
	@echo "   'Handle failing service call gracefully'"
	@echo ""
	@echo "3. Circuit Breaker:"
	@echo "   'Call external service with circuit breaker'"
	@echo "   'Check circuit breaker status'"
	@echo ""
	@echo "4. Performance Optimization:"
	@echo "   'Cache this data: user preferences'"
	@echo "   'Batch process: item1, item2, item3'"
	@echo ""
	@echo "5. Monitoring & Health:"
	@echo "   'Show system health metrics'"
	@echo "   'Display performance statistics'"
	@echo ""
	@echo "💡 Run: make dev"

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
