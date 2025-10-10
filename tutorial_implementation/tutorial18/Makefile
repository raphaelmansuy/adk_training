.PHONY: setup dev test demo clean coverage help

help:
	@echo "Tutorial 18: Events and Observability"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup    - Install dependencies"
	@echo "  make dev      - Run agent with ADK web interface"
	@echo "  make test     - Run all tests"
	@echo "  make demo     - Run demo scenarios"
	@echo "  make coverage - Run tests with coverage report"
	@echo "  make clean    - Remove cache files and artifacts"
	@echo ""
	@echo "Prerequisites:"
	@echo "  - Python 3.10+"
	@echo "  - GOOGLE_API_KEY environment variable set"
	@echo ""
	@echo "Quick start:"
	@echo "  1. make setup"
	@echo "  2. export GOOGLE_API_KEY=your_key"
	@echo "  3. make dev"

setup:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	pip install -e .
	@echo ""
	@echo "✅ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Set GOOGLE_API_KEY: export GOOGLE_API_KEY=your_key"
	@echo "  2. Run tests: make test"
	@echo "  3. Start agent: make dev"

dev:
	@echo "Starting ADK web interface..."
	@echo ""
	@echo "📊 Event Tracking Capabilities:"
	@echo ""
	@echo "1. Order Status Tracking"
	@echo "   Try: 'What is the status of my order ORD-001?'"
	@echo "   - Tracks customer queries"
	@echo "   - Logs tool calls (check_order_status)"
	@echo "   - Records agent responses"
	@echo ""
	@echo "2. Refund Processing (Auto-Approved)"
	@echo "   Try: 'I want a refund of \$$50 for order ORD-002'"
	@echo "   - Events: query → tool_call → response"
	@echo "   - No escalation (amount < \$$100)"
	@echo ""
	@echo "3. Refund Processing (Escalation)"
	@echo "   Try: 'I need a refund of \$$150 for order ORD-003'"
	@echo "   - Events: query → tool_call → escalation → response"
	@echo "   - Escalation triggered (amount > \$$100)"
	@echo ""
	@echo "4. Inventory Checks"
	@echo "   Try: 'Is product PROD-B in stock?'"
	@echo "   - Product availability tracking"
	@echo "   - Inventory level reporting"
	@echo ""
	@echo "5. Event Reporting"
	@echo "   Try: 'Show me a summary of all interactions'"
	@echo "   - Event statistics"
	@echo "   - Tool usage analysis"
	@echo "   - Escalation tracking"
	@echo ""
	@echo "🔍 Observability Features:"
	@echo "  - Event timeline tracking"
	@echo "  - Tool call logging with arguments"
	@echo "  - Escalation detection and logging"
	@echo "  - Metrics collection (latency, errors)"
	@echo "  - Real-time alerting patterns"
	@echo ""
	@echo "Opening http://localhost:8000..."
	@echo "Select 'observability_agent' from the dropdown"
	@echo ""
	adk web

test:
	@echo "Running tests..."
	pytest tests/ -v

demo:
	@echo "Running observability demo..."
	@echo ""
	@echo "This demo will:"
	@echo "  1. Process 4 customer service scenarios"
	@echo "  2. Track all events (queries, tool calls, responses)"
	@echo "  3. Detect and log escalations"
	@echo "  4. Generate comprehensive reports"
	@echo ""
	@echo "Scenarios:"
	@echo "  - Order status inquiry (ORD-001)"
	@echo "  - Small refund request (\$$50 - approved)"
	@echo "  - Large refund request (\$$150 - escalated)"
	@echo "  - Inventory check (PROD-B)"
	@echo ""
	@echo "Starting demo..."
	@echo ""
	python -m observability_agent.agent

coverage:
	@echo "Running tests with coverage..."
	pytest tests/ --cov=observability_agent --cov-report=html --cov-report=term

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete!"
