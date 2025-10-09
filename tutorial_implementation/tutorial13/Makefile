.PHONY: setup install dev run test test-verbose test-cov demo validate check clean reset help

# ===== Setup Commands =====

setup: ## Install Python dependencies
	@echo "📦 Installing dependencies..."
	@pip install -r requirements.txt
	@pip install -e .
	@echo "✅ Setup complete! Copy code_calculator/.env.example to code_calculator/.env and add your API key."

install: setup  ## Alias for setup

# ===== Development Commands =====

dev: ## Start ADK development server (web interface)
	@echo "🚀 Starting ADK web interface..."
	@echo "📍 Open http://localhost:8000 in your browser"
	@echo "💡 Select 'code_calculator' from the agent dropdown"
	@echo ""
	@adk web

run: dev  ## Alias for dev

# ===== Testing Commands =====

test: ## Run all tests
	@echo "🧪 Running tests..."
	@pytest tests/ -v

test-verbose: ## Run tests with verbose output
	@echo "🧪 Running tests with verbose output..."
	@pytest tests/ -vv -s

test-cov: ## Run tests with coverage report
	@echo "🧪 Running tests with coverage..."
	@pytest tests/ -v --cov=code_calculator --cov-report=term-missing

# ===== Demo Commands =====

demo: ## Show demo prompts and quick validation
	@echo "💡 Financial Calculator Demo Prompts:"
	@echo ""
	@echo "📊 Basic Calculations:"
	@echo "  • 'Calculate the factorial of 50'"
	@echo "  • 'Calculate the standard deviation of [23, 25, 28, 30, 29, 27, 26, 24, 31, 28]'"
	@echo ""
	@echo "💰 Compound Interest:"
	@echo "  • 'If I invest \$$10,000 at 7% annual interest compounded monthly, how much will I have after 30 years?'"
	@echo "  • 'Calculate compound interest: \$$5,000 principal, 6% annual rate, 15 years, quarterly compounding'"
	@echo ""
	@echo "🏠 Loan Calculations:"
	@echo "  • 'Calculate the monthly payment on a \$$300,000 mortgage at 6.5% annual interest for 30 years'"
	@echo "  • 'What's the monthly payment for a \$$25,000 car loan at 4.5% for 5 years?'"
	@echo ""
	@echo "🎯 Retirement Planning:"
	@echo "  • 'I'm 30 years old and want to retire at 65 with \$$2 million. If I can earn 8% annually, how much do I need to save monthly?'"
	@echo "  • 'How much do I need to save monthly to reach \$$1 million in 20 years at 7% annual return?'"
	@echo ""
	@echo "📈 Investment Analysis:"
	@echo "  • 'Compare: A) \$$50,000 initial at 6% for 20 years vs B) \$$30,000 initial + \$$200/month at 8% for 20 years'"
	@echo "  • 'Calculate CAGR for an investment that grew from \$$100,000 to \$$175,000 over 8 years'"
	@echo ""
	@echo "⚖️ Break-even Analysis:"
	@echo "  • 'Fixed costs \$$50,000/month, variable cost \$$25/unit, selling price \$$75/unit. What's break-even?'"
	@echo ""
	@echo "🔬 Algorithm Implementation:"
	@echo "  • 'Implement binary search and find 42 in [1, 5, 12, 23, 42, 67, 89, 99]'"
	@echo "  • 'Write code to find all prime numbers between 1 and 100'"
	@echo ""
	@echo "📊 Data Analysis:"
	@echo "  • 'Analyze sales data: Jan 15000, Feb 18000, Mar 16500, Apr 22000, May 21000, Jun 25000'"
	@echo ""
	@echo "To test: make dev (then use the prompts above in the web interface)"

validate: test ## Run comprehensive validation
	@echo "✅ Validation complete!"

check: test  ## Alias for validate

# ===== Cleanup Commands =====

clean: ## Clean cache files and artifacts
	@echo "🧹 Cleaning cache files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name ".coverage" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete!"

reset: clean  ## Reset to clean state
	@echo "🔄 Resetting to clean state..."
	@echo "✅ Reset complete!"

# ===== Help =====

help: ## Show this help message
	@echo "Tutorial 13: Code Execution - Financial Calculator"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
