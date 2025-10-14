# Tutorial 21: Multimodal and Image Processing
# Vision-based product catalog analyzer with synthetic image generation

.PHONY: help setup dev test demo clean lint download-images analyze generate coverage

# Default target - show help
help:
	@echo "🚀 Tutorial 21: Multimodal & Image Processing"
	@echo ""
	@echo "Quick Start Commands:"
	@echo "  make setup          - Install dependencies"
	@echo "  make download-images - Get sample product images"
	@echo "  make dev            - Start the vision catalog agent"
	@echo "  make demo           - Show example prompts"
	@echo ""
	@echo "Image Analysis Commands:"
	@echo "  make analyze        - Analyze all sample images (batch)"
	@echo "  make generate       - Generate synthetic product mockups ⭐"
	@echo ""
	@echo "Advanced Commands:"
	@echo "  make test           - Run all tests"
	@echo "  make coverage       - Run tests with coverage report"
	@echo "  make lint           - Run code linters"
	@echo "  make clean          - Clean up generated files"
	@echo ""
	@echo "💡 First time? Run: make setup && make download-images && make dev"

# Install dependencies
setup:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Set your API key: export GOOGLE_API_KEY=your_key"
	@echo "  2. Download samples: make download-images"
	@echo "  3. Start the agent: make dev"

# Download sample product images
download-images:
	@echo "📸 Downloading sample product images from Unsplash..."
	@echo ""
	python3 download_images.py
	@echo ""
	@echo "✅ Sample images downloaded to _sample_images/"
	@echo "   • laptop.jpg"
	@echo "   • headphones.jpg"
	@echo "   • smartwatch.jpg"

# Analyze all sample images
analyze: check-env
	@echo "🔍 Analyzing all sample product images..."
	@echo ""
	@echo "This will:"
	@echo "  • Load each sample image"
	@echo "  • Analyze with vision model"
	@echo "  • Generate professional catalog entries"
	@echo ""
	python3 analyze_samples.py

# Generate synthetic product mockups
generate: check-env
	@echo "🎨 Generating synthetic product mockups..."
	@echo ""
	@echo "This will:"
	@echo "  • Generate 3 synthetic product images"
	@echo "  • Analyze each generated image"
	@echo "  • Create professional catalog entries"
	@echo ""
	@echo "Products: Desk Lamp, Leather Wallet, Gaming Mouse"
	@echo ""
	python3 generate_mockups.py

# Start the vision catalog agent
dev: check-env
	@echo "🤖 Starting Vision Catalog Agent..."
	@echo ""
	@echo "🎯 Agent Capabilities:"
	@echo "   • List available sample images"
	@echo "   • Generate synthetic product mockups ⭐ NEW"
	@echo "   • Analyze uploaded images (drag & drop)"
	@echo "   • Analyze images from file paths"
	@echo "   • Compare multiple product images"
	@echo ""
	@echo "📱 Web Interface: http://localhost:8000"
	@echo "🎯 Agent: Select 'vision_catalog_agent' from dropdown"
	@echo ""
	@echo "💬 Try these example prompts:"
	@echo "   • 'What sample images do you have?'"
	@echo "   • 'Generate a mockup of a minimalist desk lamp'"
	@echo "   • [Upload image] 'Analyze this product'"
	@echo "   • 'Analyze _sample_images/laptop.jpg'"
	@echo "   • 'Compare laptop and headphones images'"
	@echo ""
	@echo "⚡ The server will start below. Press Ctrl+C to stop."
	@echo ""
	adk web

# Run all tests
test: check-env
	@echo "🧪 Running tests..."
	pytest tests/ -v --tb=short

# Run tests with coverage report
coverage: check-env
	@echo "🧪 Running tests with coverage..."
	pytest tests/ --cov=vision_catalog_agent --cov-report=html --cov-report=term
	@echo ""
	@echo "✅ Coverage report generated!"
	@echo "📊 Open htmlcov/index.html to view detailed report"

# Show demo prompts and usage examples
demo:
	@echo "=== Tutorial 21: Multimodal and Image Processing Demo ==="
	@echo ""
	@echo "This tutorial demonstrates:"
	@echo "  • Processing images with Gemini vision models"
	@echo "  • Using types.Part for multimodal content"
	@echo "  • Building vision-based product catalog analyzer"
	@echo "  • Working with multiple image inputs"
	@echo "  • Artifact management for catalog entries"
	@echo ""
	@echo "🎯 RECOMMENDED: Upload Images Directly (ADK Web Interface)"
	@echo ""
	@echo "1. Run: make dev"
	@echo "2. Open: http://localhost:8000"
	@echo "3. Select: 'vision_catalog_agent' from dropdown"
	@echo "4. Drag and drop or paste images into the chat"
	@echo "5. Try these prompts with uploaded images:"
	@echo "   • 'Analyze this product and create a catalog entry'"
	@echo "   • 'Compare these two product images'"
	@echo "   • 'What features does this product have?'"
	@echo ""
	@echo "📁 Alternative: File-Based Image Analysis"
	@echo ""
	@echo "1. Basic Image Analysis:"
	@echo "   'Analyze the sample laptop image and describe what you see'"
	@echo ""
	@echo "2. Product Catalog Entry:"
	@echo "   'Analyze _sample_images/laptop.jpg and create a catalog entry'"
	@echo ""
	@echo "3. Multiple Images:"
	@echo "   'Compare the laptop and headphones images'"
	@echo ""
	@echo "4. Batch Processing:"
	@echo "   'Analyze all images in the _sample_images directory'"
	@echo ""
	@echo "🤖 Automated Analysis: Analyze All Samples Programmatically"
	@echo ""
	@echo "Run 'make analyze' to analyze all three sample images at once"
	@echo "This will generate professional catalog entries for each product"
	@echo ""
	@echo "🎨 Synthetic Image Generation: Create Product Mockups"
	@echo ""
	@echo "Run 'make generate' to create synthetic product images"
	@echo "Perfect for prototyping when you don't have real photos yet!"
	@echo "Examples: desk lamp, leather wallet, gaming mouse, etc."
	@echo ""
	@echo "Run 'make dev' to start the ADK web interface"
	@echo ""

# Run code linters
lint:
	@echo "🔍 Running linters..."
	@echo "Checking agent code..."
	python -m py_compile vision_catalog_agent/*.py
	@echo "Checking test code..."
	python -m py_compile tests/*.py
	@echo "✅ All code passes syntax checks!"

# Clean up generated files
clean:
	@echo "🧹 Cleaning up..."
	rm -rf __pycache__ .pytest_cache .coverage htmlcov
	rm -rf vision_catalog_agent/__pycache__ tests/__pycache__
	rm -rf *.egg-info dist build
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
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
