# Tutorial 01: Hello World Agent - Makefile
# A user-friendly build system for the Hello World ADK agent

.PHONY: help setup dev test test-unit test-integration clean lint format check-env

# Default target
help: ## Show this help message
	@echo "Tutorial 01: Hello World Agent"
	@echo "==============================="
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

# Setup and installation
setup: ## Install dependencies and setup environment
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"
	@echo ""
	@echo "🔑 Next steps:"
	@echo "  1. Copy environment template: cp hello_agent/.env.example hello_agent/.env"
	@echo "  2. Add your GOOGLE_API_KEY to hello_agent/.env"
	@echo "  3. Run 'make dev' to start the agent"

# Development server
dev: check-env ## Start ADK development server
	@echo "🚀 Starting ADK development server..."
	@echo "📱 Open http://localhost:8000 in your browser"
	@echo "🎯 Select 'hello_agent' from the dropdown"
	@echo ""
	adk web

# Testing
test: ## Run all tests
	@echo "🧪 Running comprehensive test suite..."
	pytest tests/ -v --tb=short

test-unit: ## Run unit tests only
	@echo "🧪 Running unit tests..."
	pytest tests/test_agent.py tests/test_imports.py tests/test_structure.py -v

test-integration: ## Run integration tests (requires API key)
	@echo "🔗 Running integration tests..."
	@if [ -f hello_agent/.env ] && grep -q "GOOGLE_API_KEY=." hello_agent/.env; then \
		pytest tests/ -k "integration" -v; \
	else \
		echo "❌ Integration tests require GOOGLE_API_KEY in hello_agent/.env"; \
		echo "   Run 'cp hello_agent/.env.example hello_agent/.env' and add your key"; \
		exit 1; \
	fi

# Code quality
lint: ## Check code style and linting
	@echo "🔍 Running linters..."
	flake8 hello_agent/ tests/ --max-line-length=100 --extend-ignore=E203,W503
	black --check hello_agent/ tests/
	isort --check-only hello_agent/ tests/

format: ## Format code with black and isort
	@echo "🎨 Formatting code..."
	black hello_agent/ tests/
	isort hello_agent/ tests/

# Environment checks
check-env: ## Check if environment is properly configured
	@echo "🔍 Checking environment setup..."
	@if [ ! -f hello_agent/.env ]; then \
		echo "❌ hello_agent/.env not found"; \
		echo "   Run: cp hello_agent/.env.example hello_agent/.env"; \
		exit 1; \
	fi
	@if ! grep -q "GOOGLE_API_KEY=." hello_agent/.env; then \
		echo "❌ GOOGLE_API_KEY not set in hello_agent/.env"; \
		echo "   Add your API key from: https://aistudio.google.com/app/apikey"; \
		exit 1; \
	fi
	@if ! grep -q "GOOGLE_GENAI_USE_VERTEXAI=FALSE" hello_agent/.env; then \
		echo "⚠️  GOOGLE_GENAI_USE_VERTEXAI should be FALSE for Google AI Studio"; \
	fi
	@echo "✅ Environment looks good!"

# CLI testing
cli: check-env ## Test agent via command line
	@echo "💻 Testing agent via CLI..."
	@echo "Type your messages below (Ctrl+C to exit):"
	@echo ""
	adk run hello_agent

# Cleanup
clean: ## Remove generated files and caches
	@echo "🧹 Cleaning up..."
	rm -rf __pycache__ */__pycache__ *.pyc */*.pyc .pytest_cache
	rm -rf .coverage coverage.xml htmlcov/
	@echo "✅ Cleanup complete"

# Advanced targets
coverage: ## Run tests with coverage report
	@echo "📊 Running tests with coverage..."
	pytest tests/ --cov=hello_agent --cov-report=html --cov-report=term
	@echo "📱 Coverage report: htmlcov/index.html"

docs: ## Generate documentation
	@echo "📚 Generating documentation..."
	@echo "This would generate API docs, but for now just check the README.md"

# Development helpers
watch: ## Watch for file changes and run tests
	@echo "👀 Watching for changes..."
	# Requires: pip install watchfiles
	# watchfiles "make test-unit" hello_agent/ tests/

# Docker support (optional)
docker-build: ## Build Docker image
	@echo "🐳 Building Docker image..."
	docker build -t tutorial01-hello-agent .

docker-run: ## Run agent in Docker
	@echo "🐳 Running agent in Docker..."
	docker run -p 8000:8000 tutorial01-hello-agent

# CI/CD simulation
ci: lint test ## Run full CI pipeline (lint + test)
	@echo "✅ CI pipeline passed!"

# Emergency reset
reset: clean ## Reset everything to clean state
	@echo "🔄 Resetting to clean state..."
	rm -f hello_agent/.env
	@echo "✅ Reset complete. Run 'make setup' to start over."