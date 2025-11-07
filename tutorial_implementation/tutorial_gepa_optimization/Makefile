# Tutorial: GEPA (Genetic-Pareto Prompt Optimization)
# Makefile for managing the tutorial

.PHONY: help setup dev test demo real-demo clean check

# Default target - show help
help:
	@echo "🧬 GEPA Optimization Tutorial"
	@echo ""
	@echo "Quick Start Commands:"
	@echo "  make setup          - Install dependencies"
	@echo "  make dev            - Start ADK web interface"
	@echo "  make demo           - Show simulated GEPA demo (2 minutes)"
	@echo "  make real-demo      - Run REAL GEPA with LLM reflection"
	@echo ""
	@echo "Development Commands:"
	@echo "  make test           - Run tests"
	@echo "  make check          - Run code quality checks"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          - Remove generated files"
	@echo ""
	@echo "💡 First time? Run: make setup && make demo"
	@echo "🚀 For real optimization? Run: make real-demo"

# Install dependencies
setup:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Configure API key: cp gepa_agent/.env.example gepa_agent/.env"
	@echo "  2. Edit gepa_agent/.env and add your GOOGLE_API_KEY"
	@echo "  3. Run: make dev"

# Start ADK web interface
dev: check-env
	@echo "🚀 Starting ADK web interface..."
	@echo "📱 Open http://localhost:8000 and select 'gepa_agent'"
	@echo "Press Ctrl+C to stop"
	@echo ""
	adk web

# Run tests
test:
	@echo "🧪 Running tests..."
	pytest tests/ -v --tb=short -x

# Run tests with coverage
test-coverage:
	@echo "📊 Running tests with coverage..."
	pytest tests/ -v --cov=gepa_agent --cov-report=html --cov-report=term
	@echo ""
	@echo "📈 Coverage report generated in htmlcov/index.html"

# Show demo prompts and GEPA evolution
demo:
	@echo "🧬 Running GEPA Evolution Demo..."
	@echo ""
	python gepa_demo.py

# Run REAL GEPA with actual LLM reflection and evolution
real-demo: check-env
	@echo "🧬 Running REAL GEPA Evolution Demo..."
	@echo ""
	@echo "This demo uses actual LLM calls for reflection and evolution."
	@echo "You will be charged for API calls (typically $0.05-$0.10 per run)."
	@echo ""
	python gepa_real_demo.py

# Run code quality checks
check:
	@echo "🔍 Running code quality checks..."
	@echo ""
	@echo "Running ruff..."
	ruff check gepa_agent tests
	@echo "✓ ruff passed"
	@echo ""
	@echo "Running black..."
	black --check gepa_agent tests
	@echo "✓ black passed"
	@echo ""
	@echo "Running mypy..."
	mypy gepa_agent
	@echo "✓ mypy passed"
	@echo ""
	@echo "✅ All checks passed!"

# Format code
format:
	@echo "🎨 Formatting code..."
	black gepa_agent tests
	ruff check --fix gepa_agent tests
	@echo "✅ Formatting complete!"

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	@echo "✅ Cleanup complete!"

# Check environment
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
		echo ""; \
		exit 1; \
	fi

