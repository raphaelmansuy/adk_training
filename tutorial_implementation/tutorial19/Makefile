# Tutorial 19: Artifacts and File Management
# Document processing agent with artifact storage capabilities

.PHONY: help setup dev test clean demo

# Default target - show help
help:
	@echo "🚀 Tutorial 19: Artifacts & File Management"
	@echo ""
	@echo "Quick Start Commands:"
	@echo "  make setup     - Install dependencies"
	@echo "  make dev       - Start the artifact agent"
	@echo "  make demo      - Run document processing demo"
	@echo ""
	@echo "Advanced Commands:"
	@echo "  make test      - Run all tests"
	@echo "  make clean     - Clean up generated files"
	@echo ""
	@echo "💡 First time? Run: make setup && make dev"

# Install dependencies
setup:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Setup complete! Run 'make dev' to start the agent."

# Start the artifact agent
dev: check-env
	@echo "🤖 Starting Artifact Agent..."
	@echo "📱 Open http://localhost:8000 in your browser"
	@echo "🎯 Select 'artifact_agent' from the dropdown"
	@echo "📄 Try prompts like:"
	@echo "   • 'Process this document: [paste text]'"
	@echo "   • 'Show me all saved artifacts'"
	@echo "   • 'Summarize the document I just saved'"
	adk web

# Run a document processing demo
demo: check-env
	@echo "📄 Running Document Processing Demo..."
	@echo ""
	@echo "💬 Try these prompts in the ADK web UI:"
	@echo "   1. 'Process this document: The quick brown fox jumps over the lazy dog. This is a sample document for testing artifact storage.'"
	@echo "   2. 'List all artifacts'"
	@echo "   3. 'Summarize the extracted text'"
	@echo "   4. 'Translate the summary to Spanish'"
	@echo "   5. 'Create a final report combining all artifacts'"
	@echo ""
	@echo "✅ Demo ready! Open http://localhost:8000"

# Run tests
test: check-env
	@echo "🧪 Running tests..."
	pytest tests/ -v --tb=short --cov=artifact_agent --cov-report=term-missing

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf .coverage
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