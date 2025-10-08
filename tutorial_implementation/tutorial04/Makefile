# Tutorial 04: Sequential Workflows - Blog Creation Pipeline
# Makefile for development, testing, and deployment

.PHONY: help setup dev test clean demo

# Default target
help:
	@echo "Tutorial 04: Sequential Workflows - Blog Creation Pipeline"
	@echo ""
	@echo "Available commands:"
	@echo "  setup    Install dependencies"
	@echo "  dev      Start development server"
	@echo "  test     Run test suite"
	@echo "  demo     Show demo commands"
	@echo "  clean    Clean up generated files"
	@echo "  help     Show this help message"

# Setup dependencies
setup:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Setup complete!"

# Start development server
dev:
	@echo "🚀 Starting ADK development server..."
	@echo "Open http://localhost:8000 in your browser"
	@echo "Select 'blog_pipeline' from the agent list"
	@echo ""
	@echo "Try these prompts:"
	@echo "  • 'Write a blog post about artificial intelligence'"
	@echo "  • 'Create a blog post explaining how solar panels work'"
	@echo "  • 'Write about the history of the Internet'"
	@echo ""
	adk web

# Run tests
test:
	@echo "🧪 Running tests..."
	pytest tests/ -v --tb=short
	@echo "✅ Tests complete!"

# Show demo commands
demo:
	@echo "💬 Blog Creation Pipeline Demo"
	@echo ""
	@echo "The pipeline consists of 4 agents that run in sequence:"
	@echo "1. Research Agent - Gathers facts about the topic"
	@echo "2. Writer Agent - Creates a blog post draft"
	@echo "3. Editor Agent - Reviews and suggests improvements"
	@echo "4. Formatter Agent - Applies edits and formats as markdown"
	@echo ""
	@echo "Try these prompts in the ADK web UI:"
	@echo "   • 'Write a blog post about quantum computing'"
	@echo "   • 'Create a blog post about electric vehicles'"
	@echo "   • 'Blog post explaining machine learning'"
	@echo ""
	@echo "Watch the Events tab to see each agent run in sequence!"
	@echo ""
	@echo "Run 'make dev' to start the development server"

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	@echo "✅ Cleanup complete!"