# ADK Training Hub - Quick Start Makefile
# User-friendly commands for the entire project

.PHONY: help setup docs dev test clean format-md tutorials format-md build-docs build-docs-safe build-docs-verify recover-terminal optimize-images check-images

# Default target - show help
help:
	@echo "🚀 ADK Training Hub - Master Google Agent Development Kit"
	@echo ""
	@echo "Quick Start (recommended order):"
	@echo "  make setup          - Install all dependencies"
	@echo "  make docs           - Build and serve documentation"
	@echo "  make dev            - Start ADK web interface"
	@echo "  make tutorials      - List available tutorials"
	@echo ""
	@echo "Documentation Building (SAFE METHODS):"
	@echo "  make build-docs-safe    - Build docs with PTY protection (use external terminal!)"
	@echo "  make build-docs-verify  - Build docs & verify all links"
	@echo "  make recover-terminal   - Recover from PTY disconnect crashes"
	@echo ""
	@echo "Blog Image Optimization:"
	@echo "  make check-images       - Check which images exceed 5MB LinkedIn limit"
	@echo "  make optimize-images    - Optimize all oversized blog images to <5MB"
	@echo ""
	@echo "Development Commands:"
	@echo "  make test           - Run all tests across tutorials"
	@echo "  make format-md      - Format all markdown files"
	@echo "  make clean          - Clean up all generated files and caches"
	@echo ""
	@echo "⚠️  IMPORTANT: Always use 'make build-docs-safe' from external terminal (NOT VSCode terminal)"
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

# Build docs SAFELY with PTY protection (recommended)
build-docs-safe:
	@echo "🔒 Building documentation safely (with PTY protection)..."
	@echo ""
	@echo "⚠️  IMPORTANT: Please run this from an EXTERNAL terminal, not VSCode!"
	@echo "   Use: Terminal.app (macOS) or iTerm2, NOT the VSCode integrated terminal"
	@echo ""
	bash scripts/build-docs-safe.sh

# Build docs and verify all links
build-docs-verify:
	@echo "🔒 Building documentation safely and verifying links..."
	bash scripts/build-docs-safe.sh
	@echo ""
	@echo "🔍 Verifying all links..."
	python3 scripts/verify_links.py --skip-external
	@echo ""
	@echo "✅ Build and verification complete!"

# Recover from terminal crashes
recover-terminal:
	@echo "🆘 Recovering from PTY terminal disconnect..."
	bash scripts/recover-terminal.sh

# Start ADK web interface (requires GOOGLE_API_KEY)
dev: check-env
	@echo "🤖 Starting ADK Web Interface..."
	@echo "📱 Open http://localhost:8000 in your browser"
	@echo "🎯 Select an agent from the dropdown menu"
	@echo ""
	@echo "💡 Example queries to try with code_calculator:"
	@echo "   • 'Calculate the factorial of 50'"
	@echo "   • 'What's the compound interest on $10,000 at 7% for 30 years?'"
	@echo "   • 'Analyze this data: [10, 20, 30, 40, 50] - calculate mean and standard deviation'"
	@echo "   • 'Implement binary search to find 42 in [1, 5, 12, 23, 42, 67, 89, 99]'"
	@echo "   • 'Calculate the monthly payment for a $300,000 mortgage at 6.5% for 30 years'"
	@echo ""
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

# Format all markdown files
format-md:
	@echo "📝 Formatting all markdown files..."
	@if command -v npx >/dev/null 2>&1; then \
		find . -name "*.md" -not -path "./node_modules/*" -not -path "./.git/*" | xargs npx prettier --write --parser markdown; \
		echo "✅ All markdown files formatted!"; \
	else \
		echo "❌ Error: npx not found. Please install Node.js and run 'make setup' first."; \
		exit 1; \
	fi

# Check blog image sizes (LinkedIn 5MB limit)
check-images:
	@echo "🖼️  Checking blog image sizes..."
	cd docs && npm run check-images

# Optimize blog images to under 5MB
optimize-images:
	@echo "🎨 Optimizing blog images for social media..."
	cd docs && npm run optimize-images

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