.PHONY: help setup install dev test clean demo docs lint format
.PHONY: test-unit test-int clean-stores demo-upload demo-search demo-workflow

# Colors for output
BOLD := \033[1m
BLUE := \033[34m
GREEN := \033[32m
YELLOW := \033[33m
RESET := \033[0m

help:
	@printf "\n$(BOLD)$(BLUE)Policy Navigator - Tutorial 37$(RESET)\n"
	@printf "$(BOLD)File Search Store Management System$(RESET)\n\n"
	
	@printf "$(BOLD)🚀 Getting Started$(RESET)\n"
	@printf "  $(GREEN)setup$(RESET)              Install dependencies & setup environment\n"
	@printf "  $(GREEN)dev$(RESET)                Start interactive ADK web interface\n\n"
	
	@printf "$(BOLD)📦 Development$(RESET)\n"
	@printf "  $(GREEN)install$(RESET)            Install package in development mode\n"
	@printf "  $(GREEN)lint$(RESET)               Run code quality checks (ruff + black + mypy)\n"
	@printf "  $(GREEN)format$(RESET)             Auto-format code with black and ruff\n"
	@printf "  $(GREEN)test$(RESET)               Run all tests with coverage\n"
	@printf "  $(GREEN)test-unit$(RESET)          Run unit tests only\n"
	@printf "  $(GREEN)test-int$(RESET)           Run integration tests only\n\n"
	
	@printf "$(BOLD)🎯 Demos$(RESET)\n"
	@printf "  $(GREEN)demo$(RESET)               Run all demos (upload → search)\n"
	@printf "  $(GREEN)demo-upload$(RESET)        Demo: Upload policies to File Search stores\n"
	@printf "  $(GREEN)demo-search$(RESET)        Demo: Search and retrieve policies\n"
	@printf "  $(GREEN)demo-workflow$(RESET)      Demo: Complete end-to-end workflow\n\n"
	
	@printf "$(BOLD)🧹 Cleanup$(RESET)\n"
	@printf "  $(GREEN)clean$(RESET)              Remove cache, __pycache__, coverage reports\n"
	@printf "  $(GREEN)clean-stores$(RESET)       Delete ALL File Search stores (⚠️  fresh start)\n\n"
	
	@printf "$(BOLD)📚 Reference$(RESET)\n"
	@printf "  $(GREEN)docs$(RESET)               View documentation\n"
	@printf "  $(GREEN)help$(RESET)               Show this help message\n\n"

setup: install
	@printf "\n$(GREEN)✓ Environment setup complete$(RESET)\n\n"
	@printf "$(BOLD)Next steps:$(RESET)\n"
	@printf "  1. Copy .env.example to .env\n"
	@printf "       $(BLUE)cp .env.example .env$(RESET)\n\n"
	@printf "  2. Add your GOOGLE_API_KEY to .env\n\n"
	@printf "  3. Run the interactive web interface\n"
	@printf "       $(BLUE)make dev$(RESET)\n\n"
	@printf "$(BOLD)First time setup?$(RESET)\n"
	@printf "  Run the upload demo to create and populate File Search stores:\n"
	@printf "       $(BLUE)make demo-upload$(RESET)\n\n"

install:
	@printf "$(BOLD)Installing dependencies...$(RESET)\n"
	pip install -e . > /dev/null 2>&1
	pip install -r requirements.txt > /dev/null 2>&1
	@printf "$(GREEN)✓ Installation complete$(RESET)\n"

dev:
	@printf "\n$(BOLD)🚀 Starting ADK Web Interface...$(RESET)\n\n"
	@printf "$(BLUE)http://localhost:8000$(RESET)\n\n"
	@printf "The interface will open in your browser shortly.\n"
	@printf "Press Ctrl+C to stop the server.\n\n"
	adk web

test:
	@printf "\n$(BOLD)Running tests with coverage...$(RESET)\n\n"
	pytest tests/ -v --cov=policy_navigator --cov-report=html
	@printf "\n$(GREEN)✓ All tests passed!$(RESET)\n"
	@printf "$(BLUE)Coverage report: htmlcov/index.html$(RESET)\n\n"

test-unit:
	@printf "$(BOLD)Running unit tests...$(RESET)\n\n"
	pytest tests/ -v -k "not integration" --cov=policy_navigator
	@printf "\n$(GREEN)✓ Unit tests complete$(RESET)\n\n"

test-int:
	@printf "$(BOLD)Running integration tests...$(RESET)\n\n"
	pytest tests/ -v -k "integration" --cov=policy_navigator
	@printf "\n$(GREEN)✓ Integration tests complete$(RESET)\n\n"

clean:
	@printf "$(BOLD)Cleaning up artifacts...$(RESET)\n"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	@printf "$(GREEN)✓ Cleanup complete$(RESET)\n"
	@printf "  Removed: __pycache__, *.pyc, .egg-info, .pytest_cache, coverage reports\n\n"

clean-stores:
	@printf "\n$(BOLD)$(YELLOW)⚠️  WARNING: Deleting ALL File Search stores...$(RESET)\n"
	@printf "This will start you from a completely fresh state.\n\n"
	@read -p "Are you sure? (type 'yes' to confirm): " confirm; \
	if [ "$$confirm" = "yes" ]; then \
		printf "$(YELLOW)Deleting File Search stores...$(RESET)\n"; \
		python scripts/cleanup_stores.py; \
		printf "$(GREEN)✓ Cleanup complete$(RESET)\n\n"; \
	else \
		printf "$(BLUE)Cancelled$(RESET)\n\n"; \
	fi

demo: demo-upload demo-search
	@printf "$(GREEN)✓ All demos complete!$(RESET)\n"
	@printf "Next: Try $(BLUE)make demo-workflow$(RESET) for the complete end-to-end workflow\n\n"

demo-upload:
	@printf "\n$(BOLD)📤 Demo: Upload Policies to File Search$(RESET)\n"
	@printf "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)\n\n"
	python demos/demo_upload.py
	@printf "\n$(GREEN)✓ Upload demo complete$(RESET)\n\n"

demo-search:
	@printf "\n$(BOLD)🔍 Demo: Search and Retrieve Policies$(RESET)\n"
	@printf "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)\n\n"
	python demos/demo_search.py
	@printf "\n$(GREEN)✓ Search demo complete$(RESET)\n\n"

demo-workflow:
	@printf "\n$(BOLD)🔄 Demo: Complete End-to-End Workflow$(RESET)\n"
	@printf "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(RESET)\n\n"
	python demos/demo_full_workflow.py
	@printf "\n$(GREEN)✓ Workflow demo complete$(RESET)\n\n"

lint:
	@printf "$(BOLD)Running code quality checks...$(RESET)\n\n"
	@printf "$(YELLOW)Checking with ruff...$(RESET)\n"
	ruff check policy_navigator tests
	@printf "$(GREEN)✓ Ruff passed$(RESET)\n\n"
	@printf "$(YELLOW)Checking format with black...$(RESET)\n"
	black --check policy_navigator tests
	@printf "$(GREEN)✓ Black check passed$(RESET)\n\n"
	@printf "$(YELLOW)Type checking with mypy...$(RESET)\n"
	mypy policy_navigator --ignore-missing-imports
	@printf "$(GREEN)✓ MyPy passed$(RESET)\n\n"
	@printf "$(GREEN)✓ All quality checks passed!$(RESET)\n\n"

format:
	@printf "$(BOLD)Auto-formatting code...$(RESET)\n\n"
	black policy_navigator tests
	ruff check --fix policy_navigator tests
	@printf "$(GREEN)✓ Formatting complete$(RESET)\n\n"

docs:
	@printf "\n$(BOLD)📚 Documentation$(RESET)\n\n"
	@printf "$(YELLOW)Available docs:$(RESET)\n"
	@printf "  • $(BLUE)README.md$(RESET) - Project overview & quickstart\n"
	@printf "  • $(BLUE)docs/architecture.md$(RESET) - System design & components\n"
	@printf "  • $(BLUE)docs/roi_calculator.md$(RESET) - ROI analysis for enterprises\n"
	@printf "  • $(BLUE)docs/deployment_guide.md$(RESET) - Production deployment\n\n"
	@printf "$(YELLOW)Opening README.md...$(RESET)\n\n"
	open README.md || xdg-open README.md

.DEFAULT_GOAL := help
