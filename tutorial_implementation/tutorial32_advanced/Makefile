.PHONY: setup dev test clean lint format help

help:
	@echo "Data Visualization Agent with ADK Code Execution"
	@echo "=================================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make setup     - Install dependencies"
	@echo "  make dev       - Run the agent in CLI mode"
	@echo "  make test      - Run tests"
	@echo "  make lint      - Run linting checks"
	@echo "  make format    - Format code with black and isort"
	@echo "  make clean     - Remove cache and build files"
	@echo "  make help      - Show this help message"

setup:
	pip install -r requirements.txt
	pip install -e .

dev:
	python main.py

test:
	pytest tests/ -v

lint:
	flake8 data_viz_agent/ main.py
	black --check data_viz_agent/ main.py
	isort --check-only data_viz_agent/ main.py

format:
	black data_viz_agent/ main.py
	isort data_viz_agent/ main.py

clean:
	rm -rf __pycache__ .pytest_cache build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

.DEFAULT_GOAL := help
