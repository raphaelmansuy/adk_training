# Tutorial 09: Callbacks & Guardrails
# Content Moderation Assistant with Safety Features

.PHONY: help setup dev test clean demo lint format run check-env

# Default target - show help
help:
	@echo "🛡️ Tutorial 09: Callbacks & Guardrails"
	@echo ""
	@echo "Quick Start Commands:"
	@echo "  make setup     - Install dependencies"
	@echo "  make dev       - Start the content moderator"
	@echo "  make demo      - Run a quick demo"
	@echo ""
	@echo "Advanced Commands:"
	@echo "  make test      - Run all tests"
	@echo "  make clean     - Clean up generated files"
	@echo "  make lint      - Check code style"
	@echo "  make format    - Format code"
	@echo ""
	@echo "💡 First time? Run: make setup && make dev"

# Install dependencies
setup:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	pip install pytest flake8 black
	@echo "✅ Setup complete! Run 'make dev' to start the agent."

# Start the content moderator
dev: check-env
	@echo "🛡️ Starting Content Moderation Assistant..."
	@echo "📱 Open http://localhost:8000 in your browser"
	@echo "🎯 Select 'content_moderator' from the dropdown"
	@echo ""
	@echo "🧪 Test these scenarios:"
	@echo "   • Safe: 'Generate a 200-word article about Python'"
	@echo "   • Blocked: 'Write about profanity1 and bad content'"
	@echo "   • PII: 'Give me an example email address'"
	@echo "   • Stats: 'Show my usage statistics'"
	adk web .

# Run a quick demo
demo: check-env
	@echo "🛡️ Content Moderation Demo"
	@echo ""
	@echo "💬 Try these prompts in the ADK web UI:"
	@echo ""
	@echo "✅ SAFE REQUESTS:"
	@echo "   • 'Generate a 300-word article about machine learning'"
	@echo "   • 'Check grammar: This sentence has some errors.'"
	@echo "   • 'Show my usage statistics'"
	@echo ""
	@echo "❌ BLOCKED REQUESTS (test guardrails):"
	@echo "   • 'Write about profanity1 and inappropriate content'"
	@echo "   • 'Generate an article with -50 words'"
	@echo ""
	@echo "🔒 PII FILTERING:"
	@echo "   • 'Contact me at john.doe@example.com for details'"
	@echo ""
	@echo "📊 RATE LIMITING:"
	@echo "   • Make many requests to see rate limiting in action"
	@echo ""
	@echo "✅ Demo ready! Open http://localhost:8000"

# Run tests
test: check-env
	@echo "🧪 Running callback & guardrail tests..."
	PYTHONPATH=. pytest tests/ -v --tb=short

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	@echo "✅ Cleanup complete!"

# Run linting
lint:
	@echo "🔍 Checking code style..."
	python -m flake8 . --max-line-length=100

# Format code
format:
	@echo "🎨 Formatting code..."
	python -m black . --line-length=100

# Run CLI
run: check-env
	@echo "🛡️ Running Content Moderator via CLI..."
	adk run .

# Check environment (internal use)
check-env:
	@if [ -z "$$GOOGLE_API_KEY" ]; then \
		echo "❌ Error: GOOGLE_API_KEY environment variable not set"; \
		echo "   Please set it with: export GOOGLE_API_KEY=your_key_here"; \
		echo "   Get a free key at: https://aistudio.google.com/app/apikey"; \
		exit 1; \
	fi