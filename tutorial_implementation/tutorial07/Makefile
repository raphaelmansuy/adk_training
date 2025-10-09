# Tutorial 07: Loop Agents - Essay Refinement System
# Makefile for development, testing, and deployment

.PHONY: help setup install test test-verbose test-coverage dev run demo validate check clean reset

# Default target
help:
	@echo "Tutorial 07: Loop Agents - Essay Refinement System"
	@echo ""
	@echo "Development Commands:"
	@echo "  make setup         Install Python dependencies"
	@echo "  make test          Run full test suite (62 tests)"
	@echo "  make dev           Start ADK development server"
	@echo "  make demo          Quick system validation"
	@echo "  make validate      Comprehensive validation"
	@echo ""
	@echo "Testing Commands:"
	@echo "  make test-verbose  Run tests with detailed output"
	@echo "  make test-coverage Run tests with coverage report"
	@echo "  make check         Lint and format check"
	@echo ""
	@echo "Cleanup Commands:"
	@echo "  make clean         Remove cache files and artifacts"
	@echo "  make reset         Reset to clean state"

# Setup and Dependencies
setup: install
install:
	@echo "📦 Installing dependencies..."
	pip install google-adk pytest pytest-cov black flake8
	pip install -e .

# Testing
test:
	@echo "🧪 Running test suite..."
	cd tests && python -m pytest test_agent.py -v --tb=short
	@echo "✅ Test suite completed"

test-verbose:
	@echo "🧪 Running tests with verbose output..."
	cd tests && python -m pytest test_agent.py -v -s

test-coverage:
	@echo "🧪 Running tests with coverage..."
	cd tests && python -m pytest test_agent.py --cov=../essay_refiner --cov-report=html --cov-report=term-missing

# Development
dev: run
run: check-env
	@echo "🚀 Starting ADK development server..."
	@echo "Open http://localhost:8000 and select 'essay_refiner'"
	adk web

# Validation and Demo
demo:
	@echo "🎯 Running quick system validation..."
	python -c "from essay_refiner.agent import root_agent; print(f'✅ Root agent loaded: {root_agent.name}'); print(f'✅ Has {len(root_agent.sub_agents)} phases'); print(f'✅ Refinement loop has {root_agent.sub_agents[1].max_iterations} max iterations'); print('✅ Essay refinement system ready!')"

validate:
	@echo "🔍 Running comprehensive validation..."
	@echo "1. Testing imports..."
	python -c "from essay_refiner.agent import root_agent, essay_refinement_system, refinement_loop, initial_writer, critic, refiner, exit_loop; print('✅ All imports successful')"
	@echo "2. Testing agent configurations..."
	python -c "from essay_refiner.agent import root_agent; assert root_agent.name == 'EssayRefinementSystem'; assert len(root_agent.sub_agents) == 2; print('✅ Agent configurations valid')"
	@echo "3. Testing loop structure..."
	python -c "from essay_refiner.agent import refinement_loop; assert refinement_loop.max_iterations == 5; assert len(refinement_loop.sub_agents) == 2; print('✅ Loop structure valid')"
	@echo "4. Testing tool integration..."
	python -c "from essay_refiner.agent import refiner, exit_loop; assert len(refiner.tools) == 1; assert refiner.tools[0] == exit_loop; print('✅ Tool integration valid')"
	@echo "5. Running test suite..."
	make test
	@echo "🎉 All validations passed!"

check:
	@echo "🔍 Running lint and format checks..."
	flake8 essay_refiner tests --max-line-length=100 --ignore=E203,W503
	black --check essay_refiner tests

# Cleanup
clean:
	@echo "🧹 Cleaning up cache files and artifacts..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .coverage -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete

reset: clean
	@echo "🔄 Resetting to clean state..."
	@echo "Note: This removes all generated files but keeps source code"
	# Add any additional reset logic here if needed

# Check environment (internal use)
check-env:
	@if [ -z "$$GOOGLE_API_KEY" ]; then \
		echo "❌ Error: GOOGLE_API_KEY environment variable not set"; \
		echo "   Please set it with: export GOOGLE_API_KEY=your_key_here"; \
		echo "   Get a free key at: https://aistudio.google.com/app/apikey"; \
		exit 1; \
	fi