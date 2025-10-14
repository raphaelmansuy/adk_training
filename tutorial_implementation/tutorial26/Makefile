# Tutorial 26: Gemini Enterprise - Enterprise Agent Platform
# Makefile for development, testing, and deployment

.PHONY: help setup dev test clean demo

# Default target
help:
	@echo "Tutorial 26: Gemini Enterprise - Enterprise Agent Platform"
	@echo ""
	@echo "Available commands:"
	@echo "  setup    Install dependencies and set up development environment"
	@echo "  dev      Start development server (ADK web interface)"
	@echo "  test     Run comprehensive test suite"
	@echo "  demo     Run a quick demo of the enterprise lead qualifier"
	@echo "  clean    Clean up temporary files and caches"
	@echo "  help     Show this help message"

# Setup development environment
setup:
	@echo "Setting up Tutorial 26 development environment..."
	pip install -r requirements.txt
	pip install -e .
	@echo "Setup complete! Copy enterprise_agent/.env.example to enterprise_agent/.env and add your API key."

# Start development server
dev: check-env
	@echo "Starting ADK development server..."
	@echo "Open http://localhost:8000 in your browser"
	@echo "Select 'lead_qualifier' from the agent list"
	@echo ""
	@echo "Example prompts to try:"
	@echo "  - 'Qualify TechCorp as a sales lead with enterprise budget'"
	@echo "  - 'Score FinanceGlobal with business budget tier'"
	@echo "  - 'Check if HealthPlus qualifies for our enterprise tier'"
	@echo "  - 'Compare us to CompetitorX for the TechCorp opportunity'"
	@echo ""
	adk web

# Run tests
test:
	@echo "Running comprehensive test suite..."
	pytest tests/ -v --tb=short

# Quick demo
demo:
	@echo "Running enterprise lead qualifier demo..."
	@echo ""
	@python -c "from enterprise_agent.agent import root_agent, check_company_size, score_lead; print('✅ Enterprise agent loaded successfully!'); print(f'Agent name: {root_agent.name}'); print(f'Number of tools: {len(root_agent.tools)}'); print(''); print('Testing qualification workflow:'); result = check_company_size('TechCorp'); print(f'  Company lookup: {result[\"report\"]}'); score = score_lead(250, 'technology', 'enterprise'); print(f'  Lead score: {score[\"report\"]}'); print(''); print('✅ Demo complete!')"

# Clean up
clean:
	@echo "Cleaning up temporary files..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleanup complete!"

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
