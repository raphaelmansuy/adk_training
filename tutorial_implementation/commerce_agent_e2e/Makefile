# Commerce Agent E2E - End-to-End Implementation Tutorial
# Production-ready multi-user commerce assistant with session persistence

.PHONY: help setup dev test demo clean check-env

# Default target
help:
	@echo "🛍️  Commerce Agent E2E - End-to-End Implementation"
	@echo ""
	@echo "Quick Start Commands:"
	@echo "  make setup      - Install dependencies and setup package"
	@echo "  make test       - Run comprehensive test suite (unit, integration, e2e)"
	@echo "  make dev        - Start development UI (adk web)"
	@echo "  make demo       - Display demo scenarios"
	@echo ""
	@echo "Advanced Commands:"
	@echo "  make clean      - Clean up generated files"
	@echo ""
	@echo "💡 First time? Run: make setup && make test && make dev"

# Install dependencies
setup: check-env
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	pip install -e .
	@echo ""
	@echo "Initializing database..."
	python3 -c "from commerce_agent import init_database; init_database(); print('✅ Database initialized')"
	@echo ""
	@echo "✅ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Run tests: make test"
	@echo "  2. Start agent: make dev"
	@echo "  3. Open browser: http://localhost:8000"

# Run all tests
test: check-env
	@echo "🧪 Running comprehensive test suite..."
	@echo ""
	pytest tests/ -v \
		--tb=short \
		--cov=commerce_agent \
		--cov-report=html \
		--cov-report=term
	@echo ""
	@echo "✅ Tests complete! Coverage report: htmlcov/index.html"

# Start development UI
dev: check-env
	@echo "🤖 Starting Commerce Agent..."
	@echo ""
	@echo "📱 Open http://localhost:8000 in your browser"
	@echo "🎯 Select 'commerce_agent' from the agent dropdown"
	@echo ""
	@echo "Test scenarios:"
	@echo "  • User 'alice', Sport: 'running' → Find running shoes"
	@echo "  • User 'bob', Sport: 'cycling' → Recommend cycling gear"
	@echo "  • Expensive item test → Try products over €100"
	@echo ""
	adk web

# Display demo scenarios
demo:
	@echo ""
	@echo "📋 Commerce Agent E2E Demo Scenarios"
	@echo ""
	@echo "Run these after starting with: make dev"
	@echo ""
	@echo "------- SCENARIO 1: New User Setup -------"
	@echo "User ID: athlete_1"
	@echo "Session ID: session_1"
	@echo ""
	@echo "1. Type: 'My favorite sport is running'"
	@echo "   → Agent learns your preference"
	@echo ""
	@echo "2. Type: 'Find running shoes under €100'"
	@echo "   → Agent searches Decathlon"
	@echo ""
	@echo "3. Type: 'Add the Kalenji shoes to my favorites'"
	@echo "   → Agent saves to your profile"
	@echo ""
	@echo "------- SCENARIO 2: Returning Customer -------"
	@echo "User ID: athlete_1 (same user)"
	@echo "Session ID: session_2 (new session, same user)"
	@echo ""
	@echo "1. Type: 'What do you know about me?'"
	@echo "   → Agent recalls preferences (running)"
	@echo ""
	@echo "2. Type: 'Recommend something based on my history'"
	@echo "   → Agent suggests running-related products"
	@echo ""
	@echo "------- SCENARIO 3: Multi-User Isolation -------"
	@echo "User ID: cyclist_1"
	@echo "Session ID: session_1"
	@echo ""
	@echo "1. Type: 'I'm into cycling'"
	@echo "2. Type: 'Find cycling gear'"
	@echo ""
	@echo "Then switch:"
	@echo "User ID: athlete_1 (back to runner)"
	@echo ""
	@echo "3. Type: 'What are my preferences?'"
	@echo "   → Agent shows RUNNING (cycling hidden)"
	@echo ""
	@echo "------- SCENARIO 4: Expensive Item Confirmation -------"
	@echo "Type: 'Find high-end running shoes over €200'"
	@echo "   → Agent should ask for confirmation"
	@echo ""
	@echo "✅ All scenarios demonstrate key features!"
	@echo ""

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type d -name ".coverage" -delete
	find . -type d -name "htmlcov" -delete
	find . -type d -name "*.egg-info" -delete
	rm -f .coverage
	rm -f commerce_agent_sessions.db
	@echo "✅ Cleanup complete!"

# Check environment (internal use)
check-env:
	@if [ -z "$$GOOGLE_API_KEY" ] && [ -z "$$GOOGLE_APPLICATION_CREDENTIALS" ]; then \
		echo "❌ Error: Authentication not configured"; \
		echo ""; \
		echo "Choose one of the following authentication methods:"; \
		echo ""; \
		echo "🔑 Method 1 - API Key (Gemini API):"; \
		echo "   export GOOGLE_API_KEY=your_api_key_here"; \
		echo "   Get a free key at: https://aistudio.google.com/app/apikey"; \
		echo ""; \
		echo "🔐 Method 2 - Service Account (VertexAI):"; \
		echo "   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json"; \
		echo "   export GOOGLE_CLOUD_PROJECT=your_project_id"; \
		echo ""; \
		exit 1; \
	fi
