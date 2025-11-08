.PHONY: help setup install dev test clean demo docs

help:
	@echo "Policy Navigator - Tutorial 37 Commands"
	@echo "========================================"
	@echo ""
	@echo "setup        - Install dependencies and setup environment"
	@echo "install      - Install package in development mode"
	@echo "dev          - Start ADK web interface for interactive testing"
	@echo "test         - Run all tests with coverage"
	@echo "test-unit    - Run unit tests only"
	@echo "test-int     - Run integration tests only"
	@echo "clean        - Remove cache files and artifacts"
	@echo "demo         - Run demo scripts"
	@echo "demo-upload  - Demo uploading policies to File Search"
	@echo "demo-search  - Demo searching policies"
	@echo "demo-workflow - Demo complete workflow"
	@echo "lint         - Run code quality checks"
	@echo "format       - Format code with black"
	@echo "docs         - View documentation"
	@echo ""

setup: install
	@echo "✓ Environment setup complete"
	@echo ""
	@echo "Next steps:"
	@echo "1. Copy .env.example to .env"
	@echo "2. Add your GOOGLE_API_KEY to .env"
	@echo "3. Run 'make dev' to start interactive testing"

install:
	pip install -e .
	pip install -r requirements.txt

dev:
	@echo "Starting ADK web interface..."
	@echo "Open http://localhost:8000 in your browser"
	@echo ""
	adk web policy_navigator.agent

test:
	pytest tests/ -v --cov=policy_navigator --cov-report=html
	@echo ""
	@echo "Coverage report generated in htmlcov/index.html"

test-unit:
	pytest tests/ -v -k "not integration" --cov=policy_navigator

test-int:
	pytest tests/ -v -k "integration" --cov=policy_navigator

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete
	@echo "✓ Cleanup complete"

demo: demo-upload demo-search

demo-upload:
	@echo "Running demo: Upload Policies"
	@echo "=============================="
	python demos/demo_upload.py
	@echo ""

demo-search:
	@echo "Running demo: Search Policies"
	@echo "=============================="
	python demos/demo_search.py
	@echo ""

demo-workflow:
	@echo "Running demo: Complete Workflow"
	@echo "==============================="
	python demos/demo_full_workflow.py
	@echo ""

lint:
	ruff check policy_navigator tests
	black --check policy_navigator tests
	mypy policy_navigator --ignore-missing-imports

format:
	black policy_navigator tests
	ruff check --fix policy_navigator tests

docs:
	@echo "Opening documentation..."
	@echo ""
	@echo "Available documentation:"
	@echo "- README.md - Project overview"
	@echo "- docs/architecture.md - System design"
	@echo "- docs/roi_calculator.md - ROI analysis"
	@echo "- docs/deployment_guide.md - Production deployment"
	@echo ""
	open README.md || xdg-open README.md

.DEFAULT_GOAL := help
