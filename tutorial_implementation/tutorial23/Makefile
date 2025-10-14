.PHONY: setup dev test demo clean help

help:
	@echo "Available commands:"
	@echo "  make setup    - Install dependencies and package"
	@echo "  make dev      - Start ADK web interface (requires GOOGLE_API_KEY)"
	@echo "  make test     - Run all tests with coverage"
	@echo "  make demo     - Show demo prompts and usage"
	@echo "  make clean    - Remove cache and generated files"

setup:
	pip install -r requirements.txt
	pip install -e .

dev:
	@if [ -z "$$GOOGLE_API_KEY" ]; then \
		echo "Error: GOOGLE_API_KEY not set"; \
		echo "Run: export GOOGLE_API_KEY=your_key"; \
		exit 1; \
	fi
	adk web

test:
	pytest tests/ -v --cov=production_agent --cov-report=term-missing

demo:
	@echo "=== Tutorial 23: Production Deployment Agent ==="
	@echo ""
	@echo "This agent demonstrates production deployment strategies for ADK agents."
	@echo ""
	@echo "Available deployment options:"
	@echo "  1. Local API Server:    adk api_server"
	@echo "  2. Cloud Run:          adk deploy cloud_run --project YOUR_PROJECT --region us-central1"
	@echo "  3. Agent Engine:       adk deploy agent_engine --project YOUR_PROJECT --region us-central1"
	@echo "  4. GKE:                adk deploy gke"
	@echo ""
	@echo "Example prompts to try:"
	@echo ""
	@echo "  'What deployment options are available?'"
	@echo "  'How do I deploy to Cloud Run?'"
	@echo "  'What are the best practices for production deployment?'"
	@echo "  'Show me how to set up health checks'"
	@echo "  'How do I configure auto-scaling?'"
	@echo ""
	@echo "Start the agent:"
	@echo "  1. Set API key: export GOOGLE_API_KEY=your_key"
	@echo "  2. Run: make dev"
	@echo "  3. Open: http://localhost:8000"
	@echo ""
	@echo "Or use custom FastAPI server:"
	@echo "  python -m uvicorn production_agent.server:app --reload"
	@echo "  Then visit: http://localhost:8000/docs"

clean:
	rm -rf __pycache__ .pytest_cache .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
