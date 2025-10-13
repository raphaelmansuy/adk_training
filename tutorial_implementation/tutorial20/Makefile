# Tutorial 20: YAML Configuration - Declarative Agent Setup
# Makefile for YAML-based agent configuration

.PHONY: help setup dev test clean demo validate-config

# Default target - show help
help:
	@echo "🚀 Tutorial 20: YAML Configuration"
	@echo ""
	@echo "Quick Start Commands:"
	@echo "  make setup          - Install dependencies"
	@echo "  make validate-config - Validate YAML configuration"
	@echo "  make dev            - Start the YAML-configured agent"
	@echo "  make demo           - Run a quick demo"
	@echo ""
	@echo "Advanced Commands:"
	@echo "  make test           - Run all tests"
	@echo "  make clean          - Clean up generated files"
	@echo ""
	@echo "💡 First time? Run: make setup && make validate-config && make dev"

# Install dependencies
setup:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Setup complete! Run 'make validate-config' to check YAML."

# Validate YAML configuration
validate-config:
	@echo "🔍 Validating YAML configuration..."
	python -c "import yaml; from google.adk.agents import config_agent_utils; agent = config_agent_utils.from_config('customer_support/root_agent.yaml'); print(f'✅ Configuration valid: {agent.name}'); print(f'   Sub-agents: {len(agent.sub_agents) if hasattr(agent, \"sub_agents\") else 0}'); print(f'   Tools: {len(agent.tools) if hasattr(agent, \"tools\") else 0}')"

# Start the YAML-configured agent
dev: check-env validate-config
	@echo "🤖 Starting YAML-Configured Customer Support Agent..."
	@echo "📱 Open http://localhost:8000 in your browser"
	@echo "🎯 Select 'customer_support' from the dropdown"
	adk web

# Run a quick demo
demo: check-env validate-config
	@echo "🎯 Running Customer Support Demo..."
	@echo ""
	@echo "💬 Try these prompts in the ADK web UI:"
	@echo "   • 'I'm customer CUST-001 and I want to check my order ORD-001'"
	@echo "   • 'I need help with a login error'"
	@echo "   • 'I'd like a refund of \$75 for order ORD-002'"
	@echo ""
	@echo "✅ Demo ready! Open http://localhost:8000"

# Run tests
test: check-env validate-config
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