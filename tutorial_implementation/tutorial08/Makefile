# Tutorial 08: State & Memory Management
# Personal Learning Tutor with comprehensive state management

.PHONY: help setup dev test clean demo

# Default target - show help
help:
	@echo "🚀 Tutorial 08: State & Memory Management"
	@echo ""
	@echo "Quick Start Commands:"
	@echo "  make setup     - Install dependencies"
	@echo "  make dev       - Start the personal tutor agent"
	@echo "  make demo      - Run a quick demo"
	@echo ""
	@echo "Advanced Commands:"
	@echo "  make test      - Run all tests"
	@echo "  make clean     - Clean up generated files"
	@echo ""
	@echo "💡 First time? Run: make setup && make dev"

# Install dependencies
setup:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Setup complete! Run 'make dev' to start the agent."

# Start the personal tutor agent
dev: check-env
	@echo "🤖 Starting Personal Learning Tutor..."
	@echo "📱 Open http://localhost:8000 in your browser"
	@echo "🎯 Select 'personal_tutor' from the dropdown"
	@echo ""
	@echo "💡 Try these prompts:"
	@echo "   • 'Set my language to Spanish and difficulty to intermediate'"
	@echo "   • 'Start learning Python classes'"
	@echo "   • 'I got 8 out of 10 on my quiz'"
	@echo "   • 'Show me my progress'"
	@echo "   • 'What have I learned about Python?'"
	adk web

# Run a quick demo
demo: check-env
	@echo "🎓 Running Personal Tutor Demo..."
	@echo ""
	@echo "💬 Try these conversation flows in the ADK web UI:"
	@echo ""
	@echo "1️⃣  Set preferences:"
	@echo "   'Set my language to English and difficulty to beginner'"
	@echo ""
	@echo "2️⃣  Start learning:"
	@echo "   'Start learning Python basics'"
	@echo ""
	@echo "3️⃣  Complete a quiz:"
	@echo "   'I scored 9 out of 10 on my Python quiz'"
	@echo ""
	@echo "4️⃣  Check progress:"
	@echo "   'Show me my learning progress'"
	@echo ""
	@echo "5️⃣  Search memory:"
	@echo "   'What have I learned about Python?'"
	@echo ""
	@echo "✅ Demo ready! Open http://localhost:8000"

# Run tests
test: check-env
	@echo "🧪 Running comprehensive test suite..."
	pytest tests/ -v --tb=short

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
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
		echo "   Create credentials at: https://console.cloud.google.com/iam-admin/serviceaccounts"; \
		echo ""; \
		exit 1; \
	fi