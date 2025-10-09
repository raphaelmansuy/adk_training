# ADK Training Hub - Quick Start Makefile
# User-friendly commands for the entire project

.PHONY: help setup docs dev test clean tutorials

# Default target - show help
help:
	@echo "🚀 ADK Training Hub - Master Google Agent Development Kit"
	@echo ""
	@echo "Quick Start (recommended order):"
	@echo "  make setup     - Install all dependencies"
	@echo "  make docs      - Build and serve documentation"
	@echo "  make dev       - Start ADK web interface"
	@echo "  make tutorials - List available tutorials"
	@echo ""
	@echo "Development Commands:"
	@echo "  make test      - Run all tests across tutorials"
	@echo "  make clean     - Clean up all generated files"
	@echo ""
	@echo "📚 Documentation: https://raphaelmansuy.github.io/adk_training/"
	@echo "💡 First time? Run: make setup && make docs"

# Install all dependencies
setup:
	@echo "📦 Setting up ADK Training environment..."
	@echo ""
	@echo "🔧 Installing Python dependencies..."
	pip install -r requirements.txt
	@echo ""
	@echo "📖 Setting up documentation..."
	cd docs && npm install
	@echo ""
	@echo "✅ Setup complete! Run 'make docs' to start exploring."

# Build and serve documentation
docs:
	@echo "📖 Starting documentation server..."
	@echo "🌐 Open http://localhost:3000 in your browser"
	cd docs && npm start

# Start ADK web interface (requires GOOGLE_API_KEY)
dev: check-env
	@echo "🤖 Starting ADK Web Interface..."
	@echo "📱 Open http://localhost:8000 in your browser"
	@echo "🎯 Select an agent from the dropdown menu"
	adk web

# Run tests across all tutorials
test: check-env
	@echo "🧪 Running all tutorial tests..."
	@for dir in tutorial_implementation/tutorial*; do \
		if [ -d "$$dir" ] && [ -f "$$dir/Makefile" ]; then \
			echo ""; \
			echo "🧪 Testing $$(basename $$dir)..."; \
			cd $$dir && make test && cd ../..; \
		fi; \
	done
	@echo ""
	@echo "✅ All tests completed!"

# List available tutorials
tutorials:
	@echo "📚 Available ADK Tutorials:"
	@echo ""
	@for dir in tutorial_implementation/tutorial*; do \
		if [ -d "$$dir" ]; then \
			tutorial=$$(basename $$dir); \
			if [ -f "$$dir/README.md" ]; then \
				title=$$(head -1 $$dir/README.md | sed 's/^# //'); \
				echo "  📖 $$tutorial - $$title"; \
			else \
				echo "  📖 $$tutorial"; \
			fi; \
		fi; \
	done
	@echo ""
	@echo "💡 To work on a tutorial:"
	@echo "   cd tutorial_implementation/tutorial01"
	@echo "   make setup && make dev"

# Clean up all generated files
clean:
	@echo "🧹 Cleaning up project files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	@echo "✅ Cleanup complete!"

# Check environment (internal use)
check-env:
	@if [ -z "$$GOOGLE_API_KEY" ] && [ -z "$$GOOGLE_APPLICATION_CREDENTIALS" ]; then \
		echo "❌ Error: Google AI authentication not configured"; \
		echo ""; \
		echo "Choose one authentication method:"; \
		echo ""; \
		echo "🔑 Method 1 - Gemini API Key (Free):"; \
		echo "   export GOOGLE_API_KEY=your_api_key_here"; \
		echo "   🔗 Get key: https://aistudio.google.com/app/apikey"; \
		echo ""; \
		echo "🔐 Method 2 - Vertex AI (Cloud Project):"; \
		echo "   export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json"; \
		echo "   export GOOGLE_CLOUD_PROJECT=your_project_id"; \
		echo "   🔗 Setup: https://console.cloud.google.com/iam-admin/serviceaccounts"; \
		echo ""; \
		exit 1; \
	fi