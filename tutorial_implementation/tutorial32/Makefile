.PHONY: help setup dev demo test clean lint format

help:
	@echo "Data Analysis Agent with Streamlit - Available Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup              Install dependencies and package"
	@echo ""
	@echo "Development:"
	@echo "  make dev                Run Streamlit app (localhost:8501)"
	@echo "  make demo               Show demo prompts and usage examples"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test               Run all tests with coverage"
	@echo "  make lint               Check code quality"
	@echo "  make format             Format code with black and isort"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean              Remove cache and generated files"

setup:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Setup complete! Next steps:"
	@echo "   1. Copy .env.example to .env"
	@echo "   2. Add your GOOGLE_API_KEY to .env"
	@echo "   3. Run: make dev"

dev:
	@if [ ! -f .env ]; then \
		echo "❌ .env file not found!"; \
		echo "Please create .env from .env.example and add your GOOGLE_API_KEY"; \
		exit 1; \
	fi
	streamlit run app.py

demo:
	@echo "📊 Data Analysis Agent Demo"
	@echo ""
	@echo "This tutorial demonstrates:"
	@echo "  • Streamlit UI for interactive data analysis"
	@echo "  • Direct ADK agent integration (no HTTP overhead)"
	@echo "  • CSV file upload and data exploration"
	@echo "  • Real-time chat with Gemini 2.0 Flash"
	@echo ""
	@echo "📁 Sample Data:"
	@echo "  Create a simple CSV like this:"
	@echo "    name,age,salary,department"
	@echo "    Alice,30,75000,Engineering"
	@echo "    Bob,28,68000,Engineering"
	@echo "    Carol,35,82000,Sales"
	@echo ""
	@echo "💬 Try these questions:"
	@echo "  1. 'What are the main insights from this data?'"
	@echo "  2. 'What is the average salary by department?'"
	@echo "  3. 'Show me summary statistics for the data'"
	@echo "  4. 'Are there any patterns or trends?'"
	@echo ""
	@echo "🚀 To get started:"
	@echo "  1. Run: make dev"
	@echo "  2. Upload a CSV file"
	@echo "  3. Ask questions about your data"

test:
	pytest tests/ -v --tb=short --cov=data_analysis_agent --cov-report=term-missing | cat

lint:
	flake8 data_analysis_agent/ app.py tests/ --max-line-length=100 --count --statistics | cat

format:
	black data_analysis_agent/ app.py tests/
	isort data_analysis_agent/ app.py tests/ --profile black

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .coverage -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage*" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .cache/ .pytest_cache/ htmlcov/ .tox/ *.egg-info/
	@echo "✅ Cleaned up cache and generated files"
