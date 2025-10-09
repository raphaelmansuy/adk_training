# Strategic Problem Solver - Tutorial 12: Planners & Thinking Configuration
# Makefile for development, testing, and deployment

.PHONY: help setup dev test demo examples clean lint format

# Default target
help:
	@echo "Strategic Problem Solver - Tutorial 12"
	@echo ""
	@echo "Available commands:"
	@echo "  setup     Install dependencies and package in development mode"
	@echo "  dev       Start ADK web interface (http://localhost:8000)"
	@echo "  test      Run comprehensive test suite (60+ tests)"
	@echo "  demo      Run automated strategic problem-solving examples"
	@echo "  examples  Show example queries you can test with the agents"
	@echo "  clean     Remove cache files and artifacts"
	@echo "  lint      Check code style with flake8"
	@echo "  format    Format code with black"

# Setup environment
setup:
	pip install -r requirements.txt
	pip install -e .[dev]

# Start development server
dev:
	@echo "Starting ADK web interface..."
	@echo "Open http://localhost:8000 in your browser"
	@echo "Select 'strategic_solver' from the agent dropdown"
	adk web

# Run tests
test:
	pytest tests/ -v --cov=strategic_solver --cov-report=term-missing

# Run demo examples
demo:
	@echo "Running strategic problem-solving examples..."
	@echo "This will demonstrate all three planner types (BuiltInPlanner, PlanReActPlanner, StrategicPlanner)"
	@echo "with different business scenarios."
	@echo ""
	python -c "import asyncio; from strategic_solver.agent import demo_strategic_planning; asyncio.run(demo_strategic_planning())"

# Show example queries to test
examples:
	@echo "Strategic Problem Solver - Example Queries to Test"
	@echo "=================================================="
	@echo ""
	@echo "Try these queries in the ADK web interface (make dev) or with the agents:"
	@echo ""
	@echo "📊 MARKET ANALYSIS QUERIES:"
	@echo "  • Should we expand into the Asian healthcare market?"
	@echo "  • Is the European fintech sector worth entering?"
	@echo "  • Analyze market opportunity for AI consulting services"
	@echo ""
	@echo "💰 FINANCIAL ANALYSIS QUERIES:"
	@echo '  • Should we invest $$2M in renewable energy startup?'
	@echo '  • Is this $$500K investment in AI technology worth the risk?'
	@echo "  • Calculate ROI for a 3-year investment with 15% annual return"
	@echo ""
	@echo "⚠️  RISK ASSESSMENT QUERIES:"
	@echo "  • How should we mitigate cybersecurity threats in our fintech startup?"
	@echo "  • What are the risks of entering the European market?"
	@echo "  • Assess business risks for a new product launch"
	@echo ""
	@echo "🎯 STRATEGIC PLANNING QUERIES:"
	@echo '  • We have $$1M to invest - should we expand current business or enter new market?'
	@echo "  • Design a 5-year growth strategy for our SaaS company"
	@echo "  • How should we respond to increasing market competition?"
	@echo ""
	@echo "🤖 PLANNER COMPARISON:"
	@echo "  Each agent uses different planning approaches:"
	@echo "  • BuiltInPlanner: Shows transparent thinking process"
	@echo "  • PlanReActPlanner: Uses structured Plan→Reason→Act→Observe→Replan"
	@echo "  • StrategicPlanner: Domain-specific business strategy workflow"
	@echo ""
	@echo "💡 TIPS:"
	@echo "  • Complex queries work better with planners than simple ones"
	@echo "  • BuiltInPlanner shows its reasoning - great for learning"
	@echo "  • PlanReActPlanner is systematic and thorough"
	@echo "  • StrategicPlanner follows business consulting methodology"

# Clean up
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

# Code quality
lint:
	flake8 strategic_solver/ tests/
	black --check strategic_solver/ tests/

format:
	black strategic_solver/ tests/