.PHONY: help setup setup-agent setup-frontend dev dev-agent dev-frontend test demo clean

help:
	@echo "Data Analysis Dashboard - Available Commands:"
	@echo ""
	@echo "Setup Commands:"
	@echo "  make setup          - Install all dependencies (agent + frontend)"
	@echo "  make setup-agent    - Install agent dependencies only"
	@echo "  make setup-frontend - Install frontend dependencies only"
	@echo ""
	@echo "Development Commands:"
	@echo "  make dev            - Run both agent and frontend simultaneously"
	@echo "  make dev-agent      - Run agent backend server (port 8000)"
	@echo "  make dev-frontend   - Run frontend dev server (port 5173)"
	@echo ""
	@echo "Testing Commands:"
	@echo "  make test           - Run all tests with coverage"
	@echo ""
	@echo "Demo Commands:"
	@echo "  make demo           - Show demo prompts and usage examples"
	@echo ""
	@echo "Cleanup Commands:"
	@echo "  make clean          - Remove cache files and build artifacts"
	@echo ""
	@echo "Full Workflow:"
	@echo "  1. make setup       - Install dependencies"
	@echo "  2. Configure .env   - Add your GOOGLE_API_KEY"
	@echo "  3. make dev         - Start both backend and frontend"
	@echo "  4. Open http://localhost:5173 in browser"

setup: setup-agent setup-frontend
	@echo "✅ Full setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Copy agent/.env.example to agent/.env"
	@echo "  2. Add your GOOGLE_API_KEY to agent/.env"
	@echo "  3. Run 'make dev-agent' in one terminal"
	@echo "  4. Run 'make dev-frontend' in another terminal"

setup-agent:
	@echo "📦 Installing agent dependencies..."
	cd agent && python -m venv venv || true
	cd agent && . venv/bin/activate && pip install --upgrade pip
	cd agent && . venv/bin/activate && pip install -r requirements.txt
	pip install -e .
	@echo "✅ Agent setup complete!"

setup-frontend:
	@echo "📦 Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✅ Frontend setup complete!"

dev:
	@echo "🚀 Starting both agent backend and frontend servers..."
	@echo ""
	@echo "This will start:"
	@echo "  Backend: http://localhost:8000 (ADK agent)"
	@echo "  Frontend: http://localhost:5173 (Data Analysis Dashboard)"
	@echo ""
	@echo "Press Ctrl+C to stop both servers"
	@echo ""
	@$(MAKE) dev-parallel

dev-agent:
	@echo "🚀 Starting agent backend server..."
	@echo "Backend will be available at: http://localhost:8000"
	@echo "Health check: http://localhost:8000/health"
	@echo ""
	cd agent && . venv/bin/activate && python agent.py

dev-frontend:
	@echo "🚀 Starting frontend dev server..."
	@echo "Frontend will be available at: http://localhost:5173"
	@echo ""
	cd frontend && npm run dev

# Start both backend and frontend in parallel (internal use)
dev-parallel:
	@trap 'kill 0' EXIT; \
	(cd agent && . venv/bin/activate && python agent.py) & \
	(cd frontend && npm run dev) & \
	wait

test:
	@echo "🧪 Running tests with coverage..."
	. agent/venv/bin/activate && pytest tests/ -v --cov=agent --cov-report=term-missing --cov-report=html
	@echo ""
	@echo "✅ Tests complete! Coverage report generated in htmlcov/"

demo:
	@echo "📊 Data Analysis Dashboard - Demo Guide"
	@echo "========================================"
	@echo ""
	@echo "Prerequisites:"
	@echo "  - Backend running on http://localhost:8000"
	@echo "  - Frontend running on http://localhost:5173"
	@echo ""
	@echo "Example Workflow:"
	@echo "  1. Open http://localhost:5173 in your browser"
	@echo "  2. Upload a CSV file (sales data, customer data, etc.)"
	@echo "  3. Try these prompts:"
	@echo ""
	@echo "Sample Prompts:"
	@echo "  • 'Summarize the data for me'"
	@echo "  • 'What are the key statistics?'"
	@echo "  • 'Show me a line chart of sales over time'"
	@echo "  • 'Create a bar chart comparing products'"
	@echo "  • 'What correlations exist in the data?'"
	@echo "  • 'Analyze trends in the dataset'"
	@echo ""
	@echo "Sample CSV Data:"
	@echo "  month,sales,expenses"
	@echo "  Jan,10000,7000"
	@echo "  Feb,12000,7500"
	@echo "  Mar,11500,7200"
	@echo "  Apr,13000,7800"
	@echo ""
	@echo "Features:"
	@echo "  ✓ CSV data loading and parsing"
	@echo "  ✓ Statistical analysis (summary, correlation, trends)"
	@echo "  ✓ Interactive chart generation (line, bar, scatter)"
	@echo "  ✓ Natural language queries"
	@echo "  ✓ Real-time agent responses"

clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	cd frontend && rm -rf dist node_modules 2>/dev/null || true
	@echo "✅ Cleanup complete!"
