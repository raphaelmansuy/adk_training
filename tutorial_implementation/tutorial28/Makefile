# Tutorial 28: Using Other LLMs with LiteLLM
# Makefile for managing the multi-LLM agent

.PHONY: help setup dev test clean demo

# Default target - show help
help:
	@echo "🚀 Tutorial 28: Using Other LLMs with LiteLLM"
	@echo ""
	@echo "Quick Start Commands:"
	@echo "  make setup     - Install dependencies"
	@echo "  make dev       - Start the multi-LLM agent"
	@echo "  make demo      - Run example demos"
	@echo ""
	@echo "Advanced Commands:"
	@echo "  make test      - Run all tests"
	@echo "  make clean     - Clean up generated files"
	@echo ""
	@echo "💡 First time? Run: make setup && make dev"
	@echo ""
	@echo "⚠️  Prerequisites:"
	@echo "  - OpenAI API key: export OPENAI_API_KEY='sk-...'"
	@echo "  - Anthropic API key: export ANTHROPIC_API_KEY='sk-ant-...'"
	@echo "  - Optional: Ollama installed for local models (see https://ollama.com)"

# Install dependencies
setup:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Setup complete! Run 'make dev' to start the agent."

# Start the multi-LLM agent
dev: check-env
	@echo "🤖 Starting Multi-LLM Agent..."
	@echo "📱 Open http://localhost:8000 in your browser"
	@echo "🎯 Select 'multi_llm_agent' from the dropdown"
	adk web

# Run example demos
demo:
	@echo "🎬 Running Multi-LLM Demos..."
	@echo ""
	@echo "💬 Examples available:"
	@echo "   1. OpenAI GPT-4o: python -m multi_llm_agent.examples.openai_example"
	@echo "   2. Claude 3.7: python -m multi_llm_agent.examples.claude_example"
	@echo "   3. Ollama Local: python -m multi_llm_agent.examples.ollama_example"
	@echo "   4. Multi-Provider Comparison: python -m multi_llm_agent.examples.comparison"
	@echo ""
	@echo "⚠️  Make sure to set your API keys first!"

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
	rm -rf *.egg-info
	@echo "✅ Cleanup complete!"

# Check environment (internal use)
check-env:
	@if [ -z "$$GOOGLE_API_KEY" ] && [ -z "$$GOOGLE_APPLICATION_CREDENTIALS" ]; then \
		echo "❌ Error: Google authentication not configured"; \
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
	@echo "⚠️  Note: For OpenAI examples, also set OPENAI_API_KEY"
	@echo "⚠️  Note: For Claude examples, also set ANTHROPIC_API_KEY"
