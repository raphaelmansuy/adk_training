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
	@echo "  make demo      - Run interactive multi-LLM demos"
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
	@echo "  - Optional: Ollama installed for local Granite 4 model (see https://ollama.com)"

# Install dependencies
setup:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Setup complete! Run 'make dev' to start the agent."

# Start the multi-LLM agent
dev: check-env
	@echo "🤖 Starting Multi-LLM Agent Demo..."
	@echo "📱 Open http://localhost:8000 in your browser"
	@echo "🎯 Select 'multi_llm_agent' from the dropdown"
	@echo ""
	@echo "🎬 What this demo does:"
	@echo "   • Tests 4 different AI models: OpenAI GPT-4o-mini, Claude 3.7 Sonnet,"
	@echo "     Ollama Granite 4 (local), and another GPT-4o-mini config"
	@echo "   • All agents use the same tools: math calculator, weather info, sentiment analysis"
	@echo "   • Compare responses from different models on identical prompts"
	@echo ""
	@echo "💬 Example questions to try:"
	@echo "   • 'What is the square of 15?' (uses calculate_square tool)"
	@echo "   • 'What's the weather like in San Francisco?' (uses get_weather tool)"
	@echo "   • 'Analyze this text: I love this amazing new technology!' (sentiment analysis)"
	@echo "   • 'Explain quantum computing in simple terms' (general reasoning)"
	@echo "   • 'Compare OpenAI vs Claude vs local models' (meta discussion)"
	@echo ""
	@echo "🔄 Switch between agents to see different model responses!"
	adk web

# Run example demos
demo:
	@echo "🎬 Running Multi-LLM Demos..."
	@echo ""
	@echo "🤖 This demo will test different LLMs with sample queries"
	@echo "💡 Make sure your API keys are set for the models you want to test"
	@echo ""
	python -m multi_llm_agent.examples.demo

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
