# Tutorial 24: Advanced Observability & Monitoring
# Production monitoring agent with custom plugins

.PHONY: help setup dev test clean demo deploy auth

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
	@echo "  make deploy    - Deploy to Cloud Run with tracing"
	@echo "  make auth      - Authenticate with Google Cloud"
	@echo "  make clean     - Clean up generated files"
	@echo ""
	@echo "💡 First time? Run: make setup && make auth && make dev"

# Install dependencies
setup:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Setup complete! Run 'make dev' to start the agent."

# Start the observability agent
dev: check-env
	@echo "🤖 Starting Observability Agent with Cloud Tracing..."
	@echo "📱 Open http://localhost:8000 in your browser"
	@echo "🎯 Select 'observability_agent' from the dropdown"
	@echo "📊 Try prompts like:"
	@echo "   • 'What is artificial intelligence?'"
	@echo "   • 'Explain machine learning'"
	@echo "   • 'What are neural networks?'"
	@echo "💡 Check console for real-time metrics and monitoring data"
	@echo ""
	@echo "🔍 View traces in Google Cloud Console:"
	@echo "   https://console.cloud.google.com/traces?project=saas-app-001"
	@echo ""
	@echo "📋 View logs in Google Cloud Console:"
	@echo "   https://console.cloud.google.com/logs/query?project=saas-app-001"
	@echo "   Filter by: resource.type=\"cloud_run_revision\" OR resource.type=\"agent_engine\""
	adk web --trace_to_cloud

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

# Authenticate with Google Cloud
auth:
	@echo "🔐 Authenticating with Google Cloud..."
	@echo "📋 This will open a browser for authentication"
	@echo "🔑 Select your Google account and grant permissions"
	@echo ""
	gcloud auth application-default login
	@echo ""
	@echo "✅ Authentication complete!"
	@echo "💡 Next steps:"
	@echo "   1. Set your project: export GOOGLE_CLOUD_PROJECT=your-project-id"
	@echo "   2. Set your region: export GOOGLE_CLOUD_LOCATION=us-central1"
	@echo "   3. Run: make deploy"

# Deploy to Cloud Run with tracing
deploy: check-env
	@echo "🚀 Deploying Observability Agent to Cloud Run with tracing..."
	@echo "🔍 Traces will be available at:"
	@echo "   https://console.cloud.google.com/traces?project=saas-app-001"
	@echo ""
	@echo "📋 Logs will be available at:"
	@echo "   https://console.cloud.google.com/logs/query?project=saas-app-001"
	@echo "   Filter by: resource.type=\"cloud_run_revision\""
	adk deploy cloud_run --project saas-app-001 --region us-central1 --trace_to_cloud observability_agent

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
	@if [ -z "$$GOOGLE_API_KEY" ] && [ -z "$$GOOGLE_APPLICATION_CREDENTIALS" ] && [ -z "$$GOOGLE_CLOUD_PROJECT" ]; then \
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
		echo "   export GOOGLE_CLOUD_LOCATION=us-central1"; \
		echo "   Create credentials at: https://console.cloud.google.com/iam-admin/serviceaccounts"; \
		echo ""; \
		echo "🔑 Method 3 - Application Default Credentials (VertexAI):"; \
		echo "   gcloud auth application-default login"; \
		echo "   export GOOGLE_CLOUD_PROJECT=your_project_id"; \
		echo "   export GOOGLE_CLOUD_LOCATION=us-central1"; \
		echo ""; \
		exit 1; \
	fi
