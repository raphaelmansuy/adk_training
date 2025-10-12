# Tutorial 15: Live API and Audio - Real-Time Voice Interactions
# Makefile for development, testing, and voice assistant demos

.PHONY: help setup dev test demo clean
.PHONY: basic_demo advanced_demo multi_demo interactive_demo all_demos
.PHONY: lint format validate

# Default target - show help
help:
	@echo "🎙️  Tutorial 15: Live API and Audio - Real-Time Voice Interactions"
	@echo ""
	@echo "📋 QUICK START:"
	@echo "  make setup    # Install dependencies"
	@echo "  make demo     # Run text-based demo (API key or Vertex AI)"
	@echo "  make basic_demo # Live API streaming demo (requires Vertex AI)"
	@echo ""
	@echo "🎯 DEVELOPMENT COMMANDS:"
	@echo "  make setup    # Install dependencies and package"
	@echo "  make dev      # Start ADK web interface (requires GOOGLE_API_KEY)"
	@echo "  make test     # Run comprehensive test suite"
	@echo ""
	@echo "🎪 DEMO COMMANDS:"
	@echo "  make demo           # Text-based conversation demo (no mic needed)"
	@echo "  make basic_demo     # Basic Live API streaming example (Vertex AI)"
	@echo "  make advanced_demo  # Advanced features (proactivity, affective dialog)"
	@echo "  make multi_demo     # Multi-agent voice coordination"
	@echo "  make interactive_demo # Interactive voice mode (requires microphone)"
	@echo "  make all_demos      # Run all demos sequentially"
	@echo ""
	@echo "🧹 MAINTENANCE:"
	@echo "  make clean    # Remove cache files and artifacts"
	@echo "  make lint     # Check code quality"
	@echo "  make format   # Format code with black"
	@echo "  make validate # Run full validation suite"
	@echo ""
	@echo "📖 TUTORIAL: https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial15"

# Setup environment
setup:
	@echo "📦 Setting up Tutorial 15 environment..."
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Setup complete!"
	@echo "💡 Next steps:"
	@echo "   1. Copy .env.example to .env: cp .env.example .env"
	@echo "   2. For text demo (make demo): Add GOOGLE_API_KEY to .env"
	@echo "   3. For Live API (make basic_demo): Set GOOGLE_GENAI_USE_VERTEXAI=1 and GOOGLE_CLOUD_PROJECT"
	@echo "   4. Run 'make demo' for basic text conversation"
	@echo "   5. Run 'make basic_demo' for real-time streaming"
	@echo "   6. For voice features: pip install pyaudio (optional)"

# Start ADK web interface
dev:
	@echo "🌐 Starting ADK web interface..."
	@echo "🔑 Make sure you have GOOGLE_API_KEY set in your environment"
	@echo "🎙️  Select 'voice_assistant' from the agent dropdown"
	@echo "📱 Visit http://localhost:8000 in your browser"
	adk web

# Run tests
test:
	@echo "🧪 Running comprehensive test suite..."
	pytest tests/ -v --cov=voice_assistant --cov-report=term-missing
	@echo "✅ All tests completed!"

# Main demo (text-based, no microphone required)
demo:
	@echo "🎬 Running main voice assistant demo..."
	@echo "💬 This demo shows text-based conversation (no microphone needed)"
	@echo "🤖 Uses VoiceAssistant class with send_text() method"
	@echo "🔑 Checking authentication..."
	@if [ -n "$$GOOGLE_GENAI_USE_VERTEXAI" ]; then \
		echo "   ✅ Using Vertex AI (project: $$GOOGLE_CLOUD_PROJECT)"; \
		if [ -z "$$GOOGLE_CLOUD_PROJECT" ]; then \
			echo "   ⚠️  GOOGLE_CLOUD_PROJECT not set - Vertex AI may fail"; \
		fi; \
	elif [ -n "$$GOOGLE_API_KEY" ] || [ -n "$$GEMINI_API_KEY" ]; then \
		echo "   ✅ Using API Key"; \
		echo "   ⚠️  Live API may have limitations with API keys"; \
	else \
		echo "   ⚠️  No authentication found - demo will likely fail"; \
		echo "   💡 Set GOOGLE_API_KEY or configure Vertex AI"; \
	fi
	@echo "📝 Sends pre-written messages and shows responses"
	@echo "🚀 Starting demo script..."
	python -m voice_assistant.demo
	@echo "✅ Demo script finished!"

# Individual demo commands
basic_demo:
	@echo "🎯 Running Basic Live API Demo..."
	@echo "   Demonstrates fundamental bidirectional streaming with LiveRequestQueue"
	@echo "   ⚠️  Requires Vertex AI authentication (not API keys)"
	@echo "   🔄 Sends one message and shows real-time streaming response"
	@echo "   🎤 Configured for voice output (Puck voice) but shows text responses"
	@echo "   📡 Uses Live API for low-latency conversation"
	python -m voice_assistant.basic_demo
	@echo "✅ Basic demo completed!"

advanced_demo:
	@echo "⚡ Running Advanced Features Demo..."
	@echo "   Shows proactivity, affective dialog, and video streaming concepts"
	python -m voice_assistant.advanced
	@echo "✅ Advanced demo completed!"

multi_demo:
	@echo "👥 Running Multi-Agent Voice Demo..."
	@echo "   Demonstrates coordinated voice agents with sequential workflow"
	python -m voice_assistant.multi_agent
	@echo "✅ Multi-agent demo completed!"

interactive_demo:
	@echo "🎤 Running Interactive Voice Demo..."
	@echo "⚠️  This requires a microphone and PyAudio!"
	@echo "💡 Install PyAudio: pip install pyaudio"
	@echo "   (May require system audio libraries on some platforms)"
	python -m voice_assistant.interactive
	@echo "✅ Interactive demo completed!"

# Run all demos sequentially
all_demos:
	@echo "🎪 Running ALL voice assistant demos..."
	@echo "=========================================="
	$(MAKE) demo
	@echo ""
	$(MAKE) basic_demo
	@echo ""
	$(MAKE) advanced_demo
	@echo ""
	$(MAKE) multi_demo
	@echo ""
	@echo "🎉 All demos completed!"
	@echo "💡 For voice interaction: make interactive_demo (requires microphone)"
	@echo "🔧 Pro tip: Run individual demos with 'make <demo_name>'"

# Code quality
lint:
	@echo "🔍 Running code quality checks..."
	@command -v ruff >/dev/null 2>&1 && ruff check voice_assistant/ tests/ || echo "⚠️  ruff not installed (optional)"
	@command -v mypy >/dev/null 2>&1 && mypy voice_assistant/ || echo "⚠️  mypy not installed (optional)"
	@command -v flake8 >/dev/null 2>&1 && flake8 voice_assistant/ tests/ || echo "⚠️  flake8 not installed (optional)"
	@echo "✅ Lint checks complete!"

format:
	@echo "🎨 Formatting code..."
	@command -v black >/dev/null 2>&1 && black voice_assistant/ tests/ || echo "⚠️  black not installed (optional)"
	@echo "✅ Code formatting complete!"

# Comprehensive validation
validate: lint test
	@echo "✅ Full validation complete!"

# Clean up
clean:
	@echo "🧹 Cleaning up cache files and artifacts..."
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type f -name "coverage.xml" -delete
	@echo "✅ Cleanup completed!"
