# Tutorial 27: Third-Party Tools Integration
# Demonstrates LangChain and CrewAI tool integration with ADK

.PHONY: help setup dev test clean demo

# Default target - show help
help:
	@echo "🚀 Tutorial 27: Third-Party Tools Integration"
	@echo ""
	@echo "Quick Start Commands:"
	@echo "  make setup     - Install dependencies"
	@echo "  make dev       - Start the agent"
	@echo "  make demo      - Show demo prompts and usage"
	@echo ""
	@echo "Advanced Commands:"
	@echo "  make test      - Run all tests"
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
	@echo "🤖 Starting Third-Party Tools Agent..."
	@echo "📱 Open http://localhost:8000 in your browser"
	@echo "🎯 Select 'third_party_agent' from the dropdown"
	@echo ""
	@echo "💡 Try these research queries:"
	@echo "   • 'What is quantum computing?'"
	@echo "   • 'Tell me about Ada Lovelace'"
	@echo "   • 'Explain the theory of relativity'"
	@echo "   • 'What is machine learning?'"
	@echo ""
	adk web

# Run all tests
test: check-env
	@echo "🧪 Running tests..."
	pytest tests/ -v --tb=short

# Show demo prompts
demo:
	@echo "🎯 Third-Party Tools Integration Demo"
	@echo ""
	@echo "This tutorial demonstrates:"
	@echo "  ✅ LangChain Wikipedia tool integration"
	@echo "  ✅ Proper import paths (google.adk.tools.langchain_tool)"
	@echo "  ✅ Tool wrapping with LangchainTool"
	@echo "  ✅ No API keys required for Wikipedia"
	@echo ""
	@echo "Try these research queries:"
	@echo "1. 'What is quantum computing?'"
	@echo "2. 'Tell me about Ada Lovelace'"
	@echo "3. 'Explain the theory of relativity'"
	@echo "4. 'What is the history of artificial intelligence?'"
	@echo ""
	@echo "💡 Run: make dev"
	@echo "🔬 Run: make test"

# Clean up cache files
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .coverage -exec rm -rf {} + 2>/dev/null || true
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
