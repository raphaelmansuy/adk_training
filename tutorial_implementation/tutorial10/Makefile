.PHONY: setup dev test clean demo

# Setup environment
setup:
	pip install -r requirements.txt

# Start development server
dev:
	adk web support_agent

# Run all tests
test:
	pytest tests/ -v

# Run tests with coverage
test-cov:
	pytest tests/ --cov=support_agent --cov-report=html

# Run evaluation tests
eval:
	adk eval support_agent tests/simple.test.json
	adk eval support_agent tests/ticket_creation.test.json
	adk eval support_agent tests/complex.evalset.json

# Show demo prompts
demo:
	@echo "=== Support Agent Demo ==="
	@echo ""
	@echo "Try these prompts:"
	@echo "1. 'How do I reset my password?'"
	@echo "2. 'My account is locked, help!'"
	@echo "3. 'What's your refund policy?'"
	@echo "4. 'Check status of ticket TICK-12345678'"
	@echo ""
	@echo "Run: make dev"

# Clean up cache files
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .coverage -exec rm -rf {} +