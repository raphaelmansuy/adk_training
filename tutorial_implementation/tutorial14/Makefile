# Tutorial 14: Streaming Agent with Server-Sent Events (SSE)
# Makefile for development, testing, and demo commands

.PHONY: setup dev test demo clean help
.PHONY: basic_demo modes_demo chat_demo advanced_demo aggregator_demo
.PHONY: fastapi_demo client_demo all_demos

# Default target - show help
help:
	@echo "🚀 Tutorial 14: Streaming Agent with Server-Sent Events (SSE)"
	@echo ""
	@echo "📋 QUICK START:"
	@echo "  make setup    # Install dependencies"
	@echo "  make demo     # Run the main demo"
	@echo ""
	@echo "🎯 DEVELOPMENT COMMANDS:"
	@echo "  make setup    # Install dependencies and package"
	@echo "  make dev      # Start ADK web interface (requires GOOGLE_API_KEY)"
	@echo "  make test     # Run comprehensive test suite"
	@echo ""
	@echo "🎪 DEMO COMMANDS:"
	@echo "  make demo           # Run main streaming demo"
	@echo "  make basic_demo     # Basic streaming implementation"
	@echo "  make modes_demo     # StreamingMode configurations"
	@echo "  make chat_demo      # Interactive chat application"
	@echo "  make advanced_demo  # Advanced streaming patterns"
	@echo "  make aggregator_demo # Response aggregation demo"
	@echo "  make fastapi_demo   # FastAPI SSE server info"
	@echo "  make client_demo    # SSE client demo info"
	@echo "  make all_demos      # Run all demos sequentially"
	@echo ""
	@echo "🧹 MAINTENANCE:"
	@echo "  make clean    # Remove cache files and artifacts"
	@echo ""
	@echo "📖 TUTORIAL: https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial14"

# Setup environment
setup:
	@echo "📦 Setting up Tutorial 14 environment..."
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Setup complete!"
	@echo "💡 Next steps:"
	@echo "   1. Copy streaming_agent/.env.example to .env"
	@echo "   2. Add your GOOGLE_API_KEY to .env"
	@echo "   3. Run 'make demo' to see streaming in action!"

# Start ADK web interface
dev:
	@echo "🌐 Starting ADK web interface..."
	@echo "🔑 Make sure you have GOOGLE_API_KEY set in your environment"
	@echo "📱 Visit http://localhost:8000 in your browser"
	adk web streaming_agent

# Run tests
test:
	@echo "🧪 Running comprehensive test suite..."
	pytest tests/ -v --cov=streaming_agent --cov-report=term-missing
	@echo "✅ All tests completed!"

# Main demo (basic streaming)
demo:
	@echo "🎬 Running main streaming demo..."
	python demos/basic_streaming_demo.py
	@echo "✅ Demo completed!"

# Individual demo commands
basic_demo:
	@echo "🎯 Running Basic Streaming Demo..."
	@echo "   Demonstrates fundamental streaming with Runner.run_async()"
	python demos/basic_streaming_demo.py
	@echo "✅ Basic demo completed!"

modes_demo:
	@echo "🔄 Running Streaming Modes Demo..."
	@echo "   Shows different StreamingMode configurations (SSE, NONE)"
	python demos/streaming_modes_demo.py
	@echo "✅ Modes demo completed!"

chat_demo:
	@echo "💬 Running Streaming Chat Application..."
	@echo "   Interactive chat with real-time streaming responses"
	@echo "   Press Ctrl+C to exit"
	python demos/streaming_chat_app.py
	@echo "✅ Chat demo completed!"

advanced_demo:
	@echo "⚡ Running Advanced Streaming Patterns Demo..."
	@echo "   Demonstrates: aggregation, progress indicators, multiple outputs, timeout"
	python demos/advanced_patterns_demo.py
	@echo "✅ Advanced demo completed!"

aggregator_demo:
	@echo "📊 Running Streaming Aggregator Demo..."
	@echo "   Shows response aggregation and chunk analysis"
	python demos/streaming_aggregator_demo.py
	@echo "✅ Aggregator demo completed!"

fastapi_demo:
	@echo "🚀 FastAPI SSE Demo Setup Instructions"
	@echo "======================================"
	@echo "This demo shows how to build web APIs with streaming SSE."
	@echo ""
	@echo "📦 Install additional dependencies:"
	@echo "   pip install fastapi uvicorn"
	@echo ""
	@echo "🚀 Start the FastAPI server:"
	@echo "   python -m uvicorn demos.fastapi_sse_demo:app --reload --host 0.0.0.0 --port 8000"
	@echo ""
	@echo "🌐 Open in browser:"
	@echo "   http://localhost:8000/docs     - Interactive API documentation"
	@echo "   http://localhost:8000/client   - Built-in test client"
	@echo ""
	@echo "🧪 Test the streaming endpoint:"
	@echo "   curl \"http://localhost:8000/chat/stream?query=Hello%20world\""
	@echo ""
	@echo "💡 The server includes:"
	@echo "   • RESTful chat endpoints"
	@echo "   • Server-Sent Events streaming"
	@echo "   • Built-in HTML test client"
	@echo "   • CORS headers for web apps"

client_demo:
	@echo "🌐 SSE Client Demo Setup Instructions"
	@echo "===================================="
	@echo "This demo shows client-side JavaScript for SSE connections."
	@echo ""
	@echo "📋 Requirements:"
	@echo "   • FastAPI server running (see 'make fastapi_demo')"
	@echo "   • Modern web browser"
	@echo ""
	@echo "🚀 Start local web server:"
	@echo "   python -m http.server 8080"
	@echo ""
	@echo "🌐 Open in browser:"
	@echo "   http://localhost:8080/demos/sse_client.html"
	@echo ""
	@echo "💡 Features:"
	@echo "   • Real-time SSE connection"
	@echo "   • Progressive message display"
	@echo "   • Error handling and reconnection"
	@echo "   • Clean, responsive UI"
	@echo "   • Typing indicators"

# Run all demos sequentially
all_demos:
	@echo "🎪 Running ALL streaming demos..."
	@echo "=================================="
	$(MAKE) basic_demo
	@echo ""
	$(MAKE) modes_demo
	@echo ""
	$(MAKE) advanced_demo
	@echo ""
	$(MAKE) aggregator_demo
	@echo ""
	$(MAKE) fastapi_demo
	@echo ""
	$(MAKE) client_demo
	@echo ""
	@echo "🎉 All demos completed!"
	@echo "💡 Pro tip: Run individual demos with 'make <demo_name>'"

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
	find . -type f -name "streaming_output.txt" -delete
	@echo "✅ Cleanup completed!"