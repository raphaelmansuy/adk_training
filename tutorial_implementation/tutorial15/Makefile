# Tutorial 15: Live API and Audio - Real-Time Voice Interactions
# Makefile for development, testing, and voice assistant demos

.PHONY: help setup dev test demo clean
.PHONY: basic_demo advanced_demo multi_demo all_demos
.PHONY: lint format validate
.PHONY: live_env_check audio_deps_check live_smoke live_models_doc live_access_help direct_audio_demo

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
	@echo "  make demo     # Run text-based demo (API key or Vertex AI)"
	@echo "  make basic_demo # Live API streaming demo (requires Vertex AI)"
	@echo ""
	@echo "🎯 DEVELOPMENT COMMANDS:"
	@echo "  make setup    # Install dependencies and package"
	@echo "  make dev      # Start ADK web interface (requires GOOGLE_API_KEY)"
	@echo "  make test     # Run comprehensive test suite"
	@echo ""
🎪 DEMO COMMANDS:"
	@echo "  make demo              # Text-based conversation demo (no mic needed)"
	@echo "  make basic_demo_text   # Live API: TEXT input → TEXT output"
	@echo "  make basic_demo_audio  # Live API: TEXT input → AUDIO output (✅ WORKS)"
	@echo "  make direct_audio_demo # Direct API: AUDIO input → AUDIO output (bypasses ADK)"
	@echo "  make advanced_demo     # Advanced features (proactivity, affective dialog)"
	@echo "  make multi_demo        # Multi-agent voice coordination"
	@echo "  make check_audio       # Check audio device availability"
	@echo "  make live_smoke        # Quick Vertex Live connectivity smoke test"
	@echo "  make live_models_doc   # Show docs for supported Live API models"
	@echo "  make live_access_help  # Steps to request Gemini Live API activation"
	@echo "  make all_demos         # Run all demos sequentially"
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
	@echo "      Override GOOGLE_CLOUD_LOCATION if your project uses a different region"
	@echo "      Set VOICE_ASSISTANT_LIVE_MODEL to one of the supported Live API models"
	@echo "      Docs: https://ai.google.dev/gemini-api/docs/live#before_you_begin_building"
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
		echo "   ✅ Using Vertex AI (project: $$GOOGLE_CLOUD_PROJECT, region: $${GOOGLE_CLOUD_LOCATION:-us-central1})"; \
		if [ -z "$$GOOGLE_CLOUD_PROJECT" ]; then \
			echo "   ⚠️  GOOGLE_CLOUD_PROJECT not set - Vertex AI may fail"; \
		fi; \
		if [ -z "$$GOOGLE_CLOUD_LOCATION" ]; then \
			echo "   ℹ️  Defaulting region to us-central1; set GOOGLE_CLOUD_LOCATION to override"; \
		fi; \
	elif [ -n "$$GOOGLE_API_KEY" ] || [ -n "$$GEMINI_API_KEY" ]; then \
		echo "   ✅ Using API Key"; \
		echo "   ⚠️  Live API may have limitations with API keys"; \
		echo "   ℹ️  Falling back to Responses API (text-only demo)"; \
		echo "   🔁 Fallback model: $${VOICE_ASSISTANT_TEXT_MODEL:-gemini-2.5-flash}"; \
	else \
		echo "   ⚠️  No authentication found - demo will likely fail"; \
		echo "   💡 Set GOOGLE_API_KEY or configure Vertex AI"; \
	fi
	@echo "📝 Sends pre-written messages and shows responses"
	@echo "🚀 Starting demo script..."
	python -m voice_assistant.demo
	@echo "✅ Demo script finished!"

# Environment helpers for Live API demos
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

# Check audio device availability
check_audio:
	@echo "🔍 Checking audio devices..."
	@python -m voice_assistant.audio_utils

# Basic demo with TEXT modality (fallback mode)
basic_demo_text: live_env_check
	@echo "🎯 Running Basic Live API Demo (TEXT MODE)..."
	@echo "   Demonstrates fundamental bidirectional streaming with LiveRequestQueue"
	@echo "   ⚠️  Requires Vertex AI authentication (not API keys)"
	@echo "   🌎 Default region: us-central1; export GOOGLE_CLOUD_LOCATION to change"
	@echo "   🔄 Sends one message and shows real-time text response"
	@echo "   📡 Uses Live API for low-latency conversation"
	python -m voice_assistant.basic_demo --text

# Basic demo with AUDIO modality (requires PyAudio)
basic_demo_audio: live_env_check audio_deps_check
	@echo "🎯 Running Basic Live API Demo (AUDIO MODE)..."
	@echo "   Demonstrates bidirectional streaming with audio playback"
	@echo "   ⚠️  Requires: Vertex AI + PyAudio + Speakers"
	@echo "   🌎 Default region: us-central1"
	@echo "   🔄 Sends text message, receives and plays audio response"
	@echo "   🔊 Audio output will play through your speakers"
	@echo "   📡 Uses native audio Live API model"
	python -m voice_assistant.basic_demo --audio

# Alias for backward compatibility (defaults to text mode)
basic_demo: basic_demo_text

# Direct Live API demo (bypasses ADK Runner - true audio input/output)
direct_audio_demo: live_env_check audio_deps_check
	@echo "🎙️  Running Direct Live API Audio Demo..."
	@echo "   TRUE bidirectional audio using google.genai.Client"
	@echo "   ⚠️  Requires: Vertex AI + PyAudio + Microphone + Speakers"
	@echo "   🎙️  Microphone input → Agent → Speaker output"
	@echo "   ⚡ Bypasses ADK Runner (no agent tools/state)"
	@echo "   📡 Uses direct Live API WebSocket connection"
	@echo ""
	@echo "💡 This is the only way to get true audio input with current ADK"
	@echo "   ADK Runner.run_live() only supports text input + audio output"
	@echo ""
	python -m voice_assistant.direct_live_audio

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

# Individual demo commands
basic_demo: live_env_check
	@echo "🎯 Running Basic Live API Demo..."
	@echo "   Demonstrates fundamental bidirectional streaming with LiveRequestQueue"
	@echo "   ⚠️  Requires Vertex AI authentication (not API keys)"
	@echo "   🌎 Default region: $${GOOGLE_CLOUD_LOCATION:-us-central1}; export GOOGLE_CLOUD_LOCATION to change"
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

interactive_demo: live_env_check audio_deps_check
	@echo "🎤 Running Interactive Voice Demo..."
	@echo "⚠️  This requires a microphone and PyAudio!"
	@echo "💡 Install PyAudio: pip install pyaudio"
	@echo "   (May require system audio libraries on some platforms)"
	python -m voice_assistant.interactive
	@echo "✅ Interactive demo completed!"

live_audio_demo: interactive_demo
	@:

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
