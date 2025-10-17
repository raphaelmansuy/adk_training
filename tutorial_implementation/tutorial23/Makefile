# Tutorial 23: Production Deployment Implementation
# Makefile for development, testing, and deployment guidance

.PHONY: help setup dev test demo clean check-env server server-docs
.PHONY: demo-info demo-scenarios demo-deployment

# Default target - show help
help:
	@echo "🚀 Tutorial 23: Production Deployment Implementation"
	@echo ""
	@echo "📋 QUICK START:"
	@echo "  make setup    # Install dependencies"
	@echo "  make demo     # Show deployment strategies"
	@echo ""
	@echo "🎯 DEVELOPMENT COMMANDS:"
	@echo "  make setup    # Install dependencies and package"
	@echo "  make dev      # Start ADK web interface (requires GOOGLE_API_KEY)"
	@echo "  make test     # Run comprehensive test suite"
	@echo ""
	@echo "🎪 DEMO COMMANDS:"
	@echo "  make demo               # Show all deployment info (default)"
	@echo "  make demo-info          # Deployment concepts and best practices"
	@echo "  make demo-scenarios     # Real-world deployment scenarios"
	@echo "  make demo-deployment    # Deployment commands reference"
	@echo ""
	@echo "🌐 SERVER COMMANDS:"
	@echo "  make server             # Start custom FastAPI server"
	@echo "  make server-docs        # Show FastAPI documentation info"
	@echo ""
	@echo "🧹 MAINTENANCE:"
	@echo "  make clean    # Remove cache files and artifacts"
	@echo ""
	@echo "📖 LEARN MORE: https://github.com/raphaelmansuy/adk_training/tree/main/docs/tutorial/23_production_deployment.md"

# Setup environment
setup:
	@echo "📦 Setting up Tutorial 23 environment..."
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Setup complete!"
	@echo ""
	@echo "💡 Next steps:"
	@echo "   1. Set your API key: export GOOGLE_API_KEY=your_api_key"
	@echo "   2. Try the demo:     make demo"
	@echo "   3. Run tests:        make test"
	@echo "   4. Start dev:        make dev"
	@echo ""
	@echo "🔑 Get a free API key at: https://aistudio.google.com/app/apikey"

# Start ADK web interface
dev: check-env
	@echo "🤖 Starting Production Deployment Agent..."
	@echo "🌐 Open http://localhost:8000 in your browser"
	@echo "🎯 Select 'production_deployment_agent' from the dropdown"
	@echo ""
	@echo "💬 Try these prompts:"
	@echo "   • 'What deployment options are available?'"
	@echo "   • 'How do I deploy to Cloud Run?'"
	@echo "   • 'What are best practices for production?'"
	@echo "   • 'Show me health check configuration'"
	@echo ""
	adk web

# Run tests
test: check-env
	@echo "🧪 Running comprehensive test suite..."
	pytest tests/ -v --cov=production_agent --cov-report=term-missing
	@echo ""
	@echo "✅ All tests completed!"

# Main demo - show all deployment information
demo: demo-info demo-deployment demo-scenarios

# Demo: Deployment concepts and best practices
demo-info:
	@echo ""
	@echo "═══════════════════════════════════════════════════════════════"
	@echo "📚 PRODUCTION DEPLOYMENT CONCEPTS"
	@echo "═══════════════════════════════════════════════════════════════"
	@echo ""
	@echo "🎯 DEPLOYMENT STRATEGIES:"
	@echo "   • Local Development: Quick testing and iteration"
	@echo "   • API Server: Expose agent as REST endpoints"
	@echo "   • Cloud Run: Serverless container deployment"
	@echo "   • Agent Engine: Managed enterprise deployment"
	@echo "   • GKE: Kubernetes for scalable deployments"
	@echo ""
	@echo "🔒 BEST PRACTICES:"
	@echo "   • Security: Use service accounts, not API keys"
	@echo "   • Monitoring: Track metrics and errors"
	@echo "   • Health Checks: Implement liveness probes"
	@echo "   • Scalability: Use auto-scaling for load"
	@echo "   • Reliability: Implement retries and timeouts"
	@echo ""
	@echo "📊 KEY METRICS:"
	@echo "   • Request latency and throughput"
	@echo "   • Error rates and types"
	@echo "   • Resource usage (CPU, memory, network)"
	@echo "   • Uptime and availability"
	@echo ""

# Demo: Real-world deployment scenarios
demo-scenarios:
	@echo "═══════════════════════════════════════════════════════════════"
	@echo "🎬 DEPLOYMENT SCENARIOS"
	@echo "═══════════════════════════════════════════════════════════════"
	@echo ""
	@echo "📝 Scenario 1: Initial Development"
	@echo "   Goal: Quickly iterate on agent logic"
	@echo "   Command: make dev"
	@echo "   Tools: ADK Web UI for testing"
	@echo ""
	@echo "📝 Scenario 2: Local Testing"
	@echo "   Goal: Test agent as REST API"
	@echo "   Command: make server"
	@echo "   Endpoint: http://localhost:8000/invoke"
	@echo ""
	@echo "📝 Scenario 3: Production on Cloud Run"
	@echo "   Goal: Deploy to serverless environment"
	@echo "   Steps:"
	@echo "      1. Create Docker image"
	@echo "      2. Push to Google Container Registry"
	@echo "      3. Deploy with: adk deploy cloud_run"
	@echo ""
	@echo "📝 Scenario 4: Enterprise Deployment"
	@echo "   Goal: Use Google's managed Agent Engine"
	@echo "   Command: adk deploy agent_engine"
	@echo "   Features: Full monitoring, scaling, security"
	@echo ""

# Demo: Deployment commands reference
demo-deployment:
	@echo "═══════════════════════════════════════════════════════════════"
	@echo "⚙️  DEPLOYMENT COMMANDS REFERENCE"
	@echo "═══════════════════════════════════════════════════════════════"
	@echo ""
	@echo "🏠 Local Development:"
	@echo "   adk web                           # Start ADK web UI"
	@echo "   adk api_server                    # Start API server locally"
	@echo ""
	@echo "☁️  Cloud Deployment:"
	@echo "   adk deploy cloud_run --project PROJECT --region REGION"
	@echo "      Deploy to Google Cloud Run (serverless)"
	@echo ""
	@echo "🤖 Managed Deployment:"
	@echo "   adk deploy agent_engine --project PROJECT --region REGION"
	@echo "      Deploy to Google's managed Agent Engine"
	@echo ""
	@echo "🐳 Kubernetes Deployment:"
	@echo "   adk deploy gke                    # Deploy to GKE cluster"
	@echo ""
	@echo "💡 Example: Deploy to Cloud Run in us-central1"
	@echo "   adk deploy cloud_run --project my-project --region us-central1"
	@echo ""

# Start custom FastAPI server
server: check-env
	@echo "🚀 Starting Production Deployment FastAPI Server..."
	@echo ""
	@echo "📍 Server Details:"
	@echo "   • URL: http://localhost:8000"
	@echo "   • Docs: http://localhost:8000/docs"
	@echo "   • Health: http://localhost:8000/health"
	@echo ""
	@echo "🎯 Example Requests:"
	@echo "   # Health check"
	@echo "   curl http://localhost:8000/health"
	@echo ""
	@echo "   # Invoke agent"
	@echo "   curl -X POST http://localhost:8000/invoke \\  "
	@echo "     -H 'Content-Type: application/json' \\"
	@echo "     -d '{\"query\": \"What are deployment options?\"}'"
	@echo ""
	@echo "Press Ctrl+C to stop the server"
	@echo ""
	python -m uvicorn production_agent.server:app --reload

# Show FastAPI documentation info
server-docs:
	@echo ""
	@echo "═══════════════════════════════════════════════════════════════"
	@echo "📚 FASTAPI SERVER DOCUMENTATION"
	@echo "═══════════════════════════════════════════════════════════════"
	@echo ""
	@echo "🚀 Start the server:"
	@echo "   make server"
	@echo ""
	@echo "📖 Access Documentation:"
	@echo "   • Swagger UI: http://localhost:8000/docs"
	@echo "   • ReDoc: http://localhost:8000/redoc"
	@echo ""
	@echo "🔌 API Endpoints:"
	@echo ""
	@echo "   GET /health"
	@echo "      Check server health and uptime"
	@echo "      Returns: uptime (seconds), request_count, status"
	@echo ""
	@echo "   POST /invoke"
	@echo "      Invoke the production deployment agent"
	@echo "      Body: { \"query\": \"your prompt here\" }"
	@echo "      Returns: { \"response\": \"...\", \"status\": \"success\" }"
	@echo ""
	@echo "   GET /"
	@echo "      API root information"
	@echo ""
	@echo "💡 Python Example:"
	@echo "   import requests"
	@echo "   response = requests.post("
	@echo "       'http://localhost:8000/invoke',"
	@echo "       json={'query': 'What deployment options are available?'}"
	@echo "   )"
	@echo "   print(response.json()['response'])"
	@echo ""

# Clean up cache files
clean:
	@echo "🧹 Cleaning up cache files and artifacts..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.pyd" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .coverage -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name .coverage -delete 2>/dev/null || true
	find . -type f -name coverage.xml -delete 2>/dev/null || true
	@echo "✅ Cleanup completed!"

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
