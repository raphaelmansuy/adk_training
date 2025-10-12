# Tutorial 15: Live API and Audio - Real-Time Voice Interactions
# Makefile for development, testing, and voice assistant demos

.PHONY: help setup dev test clean
.PHONY: lint format validate
.PHONY: live_env_check live_smoke live_models_doc live_access_help

# Default environment values targeting a region that hosts Gemini Live preview.
# For Vertex AI: gemini-2.0-flash-live-preview-04-09 (from official ADK samples)
export VOICE_ASSISTANT_LIVE_MODEL ?= gemini-2.0-flash-live-preview-04-09
export GOOGLE_CLOUD_PROJECT ?= saas-app-001
export GOOGLE_GENAI_USE_VERTEXAI ?= 1
export GOOGLE_CLOUD_LOCATION ?= us-central1
export GOOGLE_GENAI_VERTEXAI_LOCATION ?= $(GOOGLE_CLOUD_LOCATION)

# Default target - show help
help:
	@echo "🎙️  Tutorial 15: Live API and Audio - Real-Time Voice Interactions"
	@echo ""
	@echo "📋 QUICK START:"
	@echo "  make setup    # Install dependencies"
	@echo "  make dev      # Start ADK web interface (✅ RECOMMENDED for Live API)"
	@echo "  make test     # Run comprehensive test suite"
	@echo ""
	@echo "🔧 DIAGNOSTICS & SETUP:"
	@echo "  make live_env_check    # Verify Vertex AI Live API configuration"
	@echo "  make live_models_list  # List available Live API models in your project"
	@echo "  make check_audio       # Check audio device availability"
	@echo "  make live_smoke        # Quick Vertex Live connectivity smoke test"
	@echo "  make live_models_doc   # Show docs for supported Live API models"
	@echo "  make live_access_help  # Steps to request Gemini Live API activation"
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
	@echo "   2. Configure Vertex AI credentials:"
	@echo "      export GOOGLE_GENAI_USE_VERTEXAI=1"
	@echo "      export GOOGLE_CLOUD_PROJECT=your-project"
	@echo "      export GOOGLE_CLOUD_LOCATION=us-central1"
	@echo "      export VOICE_ASSISTANT_LIVE_MODEL=gemini-2.0-flash-live-preview-04-09"
	@echo "   3. Run 'make dev' to start ADK web interface"
	@echo "   4. Open http://localhost:8000 and select 'voice_assistant'"

# Start ADK web interface (RECOMMENDED for Live API)
dev:
	@echo "🌐 Starting ADK web interface..."
	@echo "✅ This is the WORKING method for Live API bidirectional streaming"
	@echo ""
	@echo "📋 Prerequisites:"
	@echo "   • Vertex AI: Set GOOGLE_GENAI_USE_VERTEXAI=1"
	@echo "   • Project: Set GOOGLE_CLOUD_PROJECT=your-project"
	@echo "   • Region: Set GOOGLE_CLOUD_LOCATION=us-central1"
	@echo "   • Model: Set VOICE_ASSISTANT_LIVE_MODEL=gemini-2.0-flash-live-preview-04-09"
	@echo ""
	@echo "🎯 Usage:"
	@echo "   1. Open http://localhost:8000 in your browser"
	@echo "   2. Select 'voice_assistant' from the dropdown"
	@echo "   3. Click the Audio/Microphone button (🎤)"
	@echo "   4. Start typing or speaking"
	@echo ""
	@echo "🚀 Starting server..."
	adk web

# Run tests
test:
	@echo "🧪 Running comprehensive test suite..."
	pytest tests/ -v --cov=voice_assistant --cov-report=term-missing
	@echo "✅ All tests completed!"

# Environment helpers for Live API diagnostics
live_env_check:
	@echo "🩺 Verifying Vertex Live environment..."
	@if [ -z "$$GOOGLE_GENAI_USE_VERTEXAI" ]; then \
		echo "   ❌ GOOGLE_GENAI_USE_VERTEXAI is not set. Export it (value 1) for Live API."; \
		echo "   👉 Example: export GOOGLE_GENAI_USE_VERTEXAI=1"; \
		exit 1; \
	fi
	@if [ -z "$$GOOGLE_CLOUD_PROJECT" ]; then \
		echo "   ❌ GOOGLE_CLOUD_PROJECT is missing. Set your Vertex project id."; \
		echo "   👉 Example: export GOOGLE_CLOUD_PROJECT=your-project"; \
		exit 1; \
	fi
	@if [ -z "$$GOOGLE_CLOUD_LOCATION" ]; then \
		echo "   ℹ️  GOOGLE_CLOUD_LOCATION not set. Defaulting to us-central1."; \
	fi
	@if [ -z "$$VOICE_ASSISTANT_LIVE_MODEL" ]; then \
		echo "   ❌ VOICE_ASSISTANT_LIVE_MODEL not set. Choose a supported Live API model."; \
		echo "   👉 Docs: https://ai.google.dev/gemini-api/docs/live#before_you_begin_building"; \
		exit 1; \
	fi
	@echo "   • Live model: $$VOICE_ASSISTANT_LIVE_MODEL"
	@python -m scripts.validate_live_model
	@echo "   ✅ Vertex Live prerequisites detected."

audio_deps_check:
	@echo "🎧 Checking local audio dependencies..."
	@python scripts/check_audio_deps.py

live_smoke: live_env_check
	@echo "🧪 Running Vertex Live smoke test (text fallback)..."
	@python scripts/smoke_test.py

live_models_doc:
	@echo "📚 Supported Live API models (official docs):"
	@echo "   Half-cascade: gemini-live-2.5-flash-preview, gemini-2.0-flash-live-001"
	@echo "   Native audio (default): gemini-live-2.5-flash-preview-native-audio,"
	@echo "                gemini-2.5-flash-native-audio-preview-09-2025, gemini-2.5-flash-preview-native-audio-dialog,"
	@echo "                gemini-2.5-flash-exp-native-audio-thinking-dialog"
	@echo "   Docs: https://ai.google.dev/gemini-api/docs/live#before_you_begin_building"
	@echo "   Region availability varies; see https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-flash-live-api"

live_access_help:
	@python -m scripts.live_access_help

live_models_list:
	@echo "📡 Querying Vertex AI for accessible Live API models..."
	@if [ -z "$$GOOGLE_GENAI_USE_VERTEXAI" ]; then \
		echo "   ❌ GOOGLE_GENAI_USE_VERTEXAI is not set. Export it to use Vertex AI."; \
		echo "   👉 Example: export GOOGLE_GENAI_USE_VERTEXAI=1"; \
		exit 1; \
	fi
	@if [ -z "$$GOOGLE_CLOUD_PROJECT" ]; then \
		echo "   ❌ GOOGLE_CLOUD_PROJECT is missing. Set your Vertex project id."; \
		echo "   👉 Example: export GOOGLE_CLOUD_PROJECT=your-project"; \
		exit 1; \
	fi
	@python -m scripts.list_live_models

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
