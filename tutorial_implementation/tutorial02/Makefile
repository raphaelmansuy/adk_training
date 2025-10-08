# Tutorial 02: Function Tools - Finance Assistant Agent
# Simple Makefile for getting started quickly

.PHONY: help setup dev parallel-demo test clean demo

# Default target - show help
help:
	@echo "🚀 Tutorial 02: Function Tools - Finance Assistant Agent"
	@echo ""
	@echo "Quick Start Commands:"
	@echo "  make setup     - Install dependencies"
	@echo "  make dev       - Start the finance assistant agent"
	@echo "  make demo      - Run a quick demo of calculations"
	@echo ""
	@echo "Advanced Commands:"
	@echo "  make parallel-demo  - Start parallel execution demo"
	@echo "  make test           - Run all tests"
	@echo "  make clean          - Clean up generated files"
	@echo ""
	@echo "💡 First time? Run: make setup && make dev"

# Install dependencies
setup:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Setup complete! Run 'make dev' to start the agent."

# Start the main finance assistant
dev: check-env
	@echo "🤖 Starting Finance Assistant..."
	@echo "Available agents: finance_assistant, parallel_finance_assistant"
	@echo "Open http://localhost:8000 in your browser"
	adk web

# Start the parallel execution demo
parallel-demo: check-env
	@echo "⚡ Starting Parallel Execution Demo..."
	@echo "This demo shows how ADK runs multiple tools simultaneously"
	@echo "Open http://localhost:8000 in your browser"
	adk web

# Run a quick demo
demo: check-env
	@echo "🧮 Running Financial Calculation Demo..."
	@echo ""
	@echo "💰 Compound Interest: $$10,000 at 6% for 5 years"
	@python -c "from finance_assistant.agent import calculate_compound_interest; result = calculate_compound_interest(10000, 0.06, 5); print(result['report'])"
	@echo ""
	@echo "🏠 Loan Payment: $$300,000 at 4.5% for 30 years"
	@python -c "from finance_assistant.agent import calculate_loan_payment; result = calculate_loan_payment(300000, 0.045, 30); print(result['report'])"
	@echo ""
	@echo "🎯 Monthly Savings: $$50,000 in 3 years at 5%"
	@python -c "from finance_assistant.agent import calculate_monthly_savings; result = calculate_monthly_savings(50000, 3, 0.05); print(result['report'])"
	@echo ""
	@echo "✅ Demo complete! Now try: make dev"

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
	@echo "✅ Cleanup complete!"

# Check environment (internal use)
check-env:
	@if [ -z "$$GOOGLE_API_KEY" ]; then \
		echo "❌ Error: GOOGLE_API_KEY environment variable not set"; \
		echo "   Please set it with: export GOOGLE_API_KEY=your_key_here"; \
		echo "   Get a free key at: https://aistudio.google.com/app/apikey"; \
		exit 1; \
	fi