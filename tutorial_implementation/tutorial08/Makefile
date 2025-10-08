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
	@if [ -z "$$GOOGLE_API_KEY" ]; then \
		echo "❌ Error: GOOGLE_API_KEY environment variable not set"; \
		echo "   Please set it with: export GOOGLE_API_KEY=your_key_here"; \
		echo "   Get a free key at: https://aistudio.google.com/app/apikey"; \
		exit 1; \
	fi