# Tutorial 24: Advanced Observability & Monitoring
# Production monitoring agent with custom plugins

.PHONY: help setup dev test clean demo

# Default target - show help
help:
	@echo "🚀 Tutorial 24: Advanced Observability & Monitoring"
	@echo ""
	@echo "Quick Start Commands:"
	@echo "  make setup     - Install dependencies"
	@echo "  make dev       - Start the observability agent"
	@echo "  make demo      - Show demo prompts and usage"
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

# Start the observability agent
dev: check-env
	@echo "🤖 Starting Observability Agent..."
	@echo "📱 Open http://localhost:8000 in your browser"
	@echo "🎯 Select 'observability_agent' from the dropdown"
	@echo "📊 Try prompts like:"
	@echo "   • 'What is artificial intelligence?'"
	@echo "   • 'Explain machine learning'"
	@echo "   • 'What are neural networks?'"
	@echo "💡 Check console for real-time metrics and monitoring data"
	adk web

# Run a monitoring demo
demo: check-env
	@echo "📊 Advanced Observability Demo"
	@echo ""
	@echo "💬 Try these prompts in the ADK web UI:"
	@echo "   1. 'What is artificial intelligence?'"
	@echo "   2. 'Explain machine learning in simple terms'"
	@echo "   3. 'What are the applications of AI?'"
	@echo "   4. 'How does deep learning work?'"
	@echo "   5. 'What is the future of AI?'"
	@echo ""
	@echo "📈 Features demonstrated:"
	@echo "   • SaveFilesAsArtifactsPlugin - automatic file saving"
	@echo "   • MetricsCollectorPlugin - request/response metrics"
	@echo "   • AlertingPlugin - error detection and alerts"
	@echo "   • PerformanceProfilerPlugin - detailed profiling"
	@echo ""
	@echo "🔍 Observe the console output for:"
	@echo "   • Request start/completion events"
	@echo "   • Latency measurements"
	@echo "   • Token counts"
	@echo "   • Success/error tracking"
	@echo ""
	@echo "✅ Demo ready! Open http://localhost:8000"

# Run tests
test: check-env
	@echo "🧪 Running tests..."
	pytest tests/ -v --tb=short --cov=observability_agent --cov-report=term-missing

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf *.egg-info/
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
