# Tutorial 06: Multi-Agent Systems - Content Publishing System
# Makefile for development, testing, and deployment

.PHONY: help setup dev test clean demo

# Default target
help:
	@echo "Tutorial 06: Multi-Agent Systems - Content Publishing System"
	@echo ""
	@echo "Available commands:"
	@echo "  setup    Install dependencies and set up development environment"
	@echo "  dev      Start development server (ADK web interface)"
	@echo "  test     Run comprehensive test suite"
	@echo "  demo     Run a quick demo of the content publishing system"
	@echo "  clean    Clean up temporary files and caches"
	@echo "  help     Show this help message"

# Setup development environment
setup:
	@echo "Setting up Tutorial 06 development environment..."
	pip install -r requirements.txt
	@echo "Setup complete! Copy content_publisher/.env.example to content_publisher/.env and add your API key."

# Start development server
dev:
	@echo "Starting ADK development server..."
	@echo "Open http://localhost:8000 in your browser"
	@echo "Select 'content_publisher' from the agent list"
	@echo ""
	@echo "Example prompts to try:"
	@echo "  - 'Write an article about artificial intelligence in healthcare'"
	@echo "  - 'Create an article about renewable energy adoption'"
	@echo "  - 'Write about the future of remote work'"
	@echo "  - 'Create an article explaining quantum computing breakthroughs'"
	@echo ""
	adk web

# Run tests
test:
	@echo "Running comprehensive test suite..."
	pytest tests/ -v --tb=short

# Quick demo
demo:
	@echo "Running content publishing system demo..."
	@echo "This will test the basic functionality"
	@python -c "from content_publisher.agent import root_agent; print('✅ Content publishing system loaded successfully!'); print(f'Agent name: {root_agent.name}'); print(f'Number of pipeline stages: {len(root_agent.sub_agents)}'); print('Phase 1 (parallel research) has', len(root_agent.sub_agents[0].sub_agents), 'concurrent pipelines'); print('✅ Demo complete!')"

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