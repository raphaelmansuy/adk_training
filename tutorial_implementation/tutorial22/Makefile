# Tutorial 22: Model Selection & Optimization Framework
# Intelligent agent that helps select the best AI model for your use case

.PHONY: help setup dev test test-cov clean demo benchmark compare-models
.PHONY: quick-start full-demo model-info

# Default target - show comprehensive help
help:
	@echo "🚀 Tutorial 22: Model Selection & Optimization Framework"
	@echo "🤖 An intelligent agent that recommends and compares AI models"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🎯 GETTING STARTED (5 minutes)"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  make setup          📦 Install dependencies (2 min)"
	@echo "  make dev            🚀 Start interactive agent (instant)"
	@echo "  make quick-start    ⚡ Setup + start in one command (3 min)"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🧪 TESTING & VALIDATION"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  make test           ✅ Run all tests (30 sec)"
	@echo "  make test-cov       📊 Run tests with coverage report (45 sec)"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🎪 DEMONSTRATIONS & EXAMPLES"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  make demo           🎯 Interactive demo with sample questions"
	@echo "  make benchmark      📈 Run automated model performance tests"
	@echo "  make compare-models 🔄 Compare specific models side-by-side"
	@echo "  make model-info     ℹ️  Show detailed model specifications"
	@echo "  make full-demo      🎉 Complete experience (all demos)"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🧹 MAINTENANCE"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  make clean          🗑️  Remove cache files and build artifacts"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📋 PREREQUISITES"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  • Python 3.9+"
	@echo "  • GOOGLE_API_KEY environment variable"
	@echo "     💡 Get free key: https://aistudio.google.com/app/apikey"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "💡 QUICK START WORKFLOW"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  1️⃣  make setup          # Install everything"
	@echo "  2️⃣  make dev            # Start the agent"
	@echo "  3️⃣  Open http://localhost:8000"
	@echo "  4️⃣  Select 'model_selector_agent' from dropdown"
	@echo "  5️⃣  Ask: 'What model should I use for real-time voice chat?'"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🎯 WHAT THIS TUTORIAL TEACHES"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  • Model selection strategies and trade-offs"
	@echo "  • Performance benchmarking across models"
	@echo "  • Cost optimization for AI workloads"
	@echo "  • Real-world model comparison frameworks"
	@echo "  • Production deployment considerations"

	@echo "  • Production deployment considerations"

# Quick start: setup + dev in one command
quick-start: setup dev

# Setup environment with progress indicators
setup:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📦 SETTING UP TUTORIAL 22 ENVIRONMENT"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "⏳ Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "✅ Python dependencies installed"
	@echo ""
	@echo "⏳ Installing model_selector package..."
	pip install -e .
	@echo "✅ Package installed successfully"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🎉 SETUP COMPLETE!"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "💡 Next steps:"
	@echo "   1. Configure API key: export GOOGLE_API_KEY=your_key"
	@echo "   2. Run: make dev"
	@echo "   3. Open http://localhost:8000 in your browser"
	@echo ""
	@echo "🔑 Don't have an API key?"
	@echo "   Get one free at: https://aistudio.google.com/app/apikey"

# Start development server with guided experience
dev: check-env
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🤖 STARTING MODEL SELECTOR AGENT"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📱 Web Interface: http://localhost:8000"
	@echo "🎯 Agent Name: model_selector_agent"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "� TRY THESE SAMPLE QUESTIONS:"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🎯 Model Recommendations:"
	@echo "  • 'What model should I use for real-time voice chat?'"
	@echo "  • 'Which model is best for complex reasoning tasks?'"
	@echo "  • 'Recommend a model for customer support chatbot'"
	@echo "  • 'What model for code generation and debugging?'"
	@echo ""
	@echo "📊 Model Comparisons:"
	@echo "  • 'Compare gemini-2.5-flash and gemini-2.5-pro'"
	@echo "  • 'How does gemini-2.5-flash-lite differ from flash?'"
	@echo "  • 'Show me the trade-offs between speed and quality'"
	@echo ""
	@echo "💰 Cost Optimization:"
	@echo "  • 'Which model gives best performance per dollar?'"
	@echo "  • 'Help me choose a model for high-volume API calls'"
	@echo "  • 'What's the most cost-effective model for my use case?'"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🎮 HOW TO USE:"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  1. Open http://localhost:8000 in your browser"
	@echo "  2. Select 'model_selector_agent' from the dropdown"
	@echo "  3. Type any question above or describe your use case"
	@echo "  4. Watch the agent analyze and recommend the best model!"
	@echo ""
	@echo "💡 Pro Tips:"
	@echo "  • Be specific about your use case (latency, cost, accuracy needs)"
	@echo "  • Mention your expected usage volume"
	@echo "  • Ask about trade-offs between different models"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🚀 STARTING SERVER..."
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	adk web

# Run all tests with detailed output
test: check-env
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🧪 RUNNING TEST SUITE"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "⏳ Executing all tests..."
	pytest tests/ -v --tb=short
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "✅ TEST SUITE COMPLETE"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "💡 Tests validate:"
	@echo "   • Model selection logic"
	@echo "   • Performance benchmarking"
	@echo "   • Cost optimization algorithms"
	@echo "   • Agent response formatting"

# Run tests with coverage report
test-cov: check-env
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📊 RUNNING TESTS WITH COVERAGE ANALYSIS"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "⏳ Running tests and analyzing code coverage..."
	pytest tests/ --cov=model_selector --cov-report=html --cov-report=term-missing
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📈 COVERAGE REPORT GENERATED"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📁 HTML Report: htmlcov/index.html"
	@echo "💡 Open the HTML file in your browser for detailed coverage analysis"
	@echo ""
	@echo "🎯 Coverage includes:"
	@echo "   • Model selection algorithms"
	@echo "   • Benchmarking functions"
	@echo "   • Cost calculation logic"
	@echo "   • Agent response generation"

# Interactive demo with guided experience
demo: check-env
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🎯 MODEL SELECTION AGENT - INTERACTIVE DEMO"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "🎪 This demo shows the agent's capabilities through guided examples"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📋 DEMO SCENARIOS:"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "1️⃣  🎯 Model Recommendations:"
	@echo "   • Real-time voice applications"
	@echo "   • Complex reasoning tasks"
	@echo "   • Customer support chatbots"
	@echo "   • Code generation & debugging"
	@echo ""
	@echo "2️⃣  📊 Performance Comparisons:"
	@echo "   • Speed vs accuracy trade-offs"
	@echo "   • Cost vs performance analysis"
	@echo "   • Model capability matrices"
	@echo ""
	@echo "3️⃣  💰 Cost Optimization:"
	@echo "   • Best performance per dollar"
	@echo "   • High-volume API optimization"
	@echo "   • Budget-conscious recommendations"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🚀 TO RUN THE DEMO:"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  1. In another terminal, run: make dev"
	@echo "  2. Open http://localhost:8000 in your browser"
	@echo "  3. Select 'model_selector_agent' from dropdown"
	@echo "  4. Try the questions shown during 'make dev'"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "⚡ STANDALONE BENCHMARK MODE:"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "Running automated model comparison..."
	python -m model_selector.agent

# Run automated model performance benchmarks
benchmark: check-env
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📈 MODEL PERFORMANCE BENCHMARK"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "⏳ Running comprehensive model benchmarks..."
	@echo "   This may take several minutes..."
	@echo ""
	python -c "\
from model_selector.agent import benchmark_models; \
print('🏃 Running benchmark suite...'); \
results = benchmark_models(); \
print('✅ Benchmark complete!'); \
print('📊 Results saved to benchmark_results.json'); \
"

# Compare specific models side-by-side
compare-models: check-env
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🔄 MODEL COMPARISON TOOL"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📊 Comparing Gemini models across key dimensions..."
	@echo ""
	python -c 'from model_selector.agent import compare_models_detailed; print("🔍 Analyzing model differences..."); comparison = compare_models_detailed(); print("✅ Comparison complete!"); print("📋 Key findings:"); [print("   • " + finding) for finding in comparison.get("key_findings", [])]'

# Show detailed model specifications
model-info: check-env
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "ℹ️  GEMINI MODEL SPECIFICATIONS"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	python model_specs.py

# Complete experience - run all demos
full-demo: check-env
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🎉 COMPLETE MODEL SELECTION EXPERIENCE"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🎪 This will run all demonstrations and benchmarks"
	@echo "   Estimated time: 5-10 minutes"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "📋 WHAT YOU'LL SEE:"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  1. 🤖 Interactive agent capabilities"
	@echo "  2. 📈 Automated performance benchmarks"
	@echo "  3. 🔄 Detailed model comparisons"
	@echo "  4. ℹ️  Complete model specifications"
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🚀 STARTING COMPLETE DEMO..."
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo ""
	@echo "Step 1/4: Interactive Demo Instructions"
	$(MAKE) demo
	@echo ""
	@echo "Step 2/4: Running Benchmarks..."
	$(MAKE) benchmark
	@echo ""
	@echo "Step 3/4: Model Comparisons..."
	$(MAKE) compare-models
	@echo ""
	@echo "Step 4/4: Model Specifications..."
	$(MAKE) model-info
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🎉 COMPLETE EXPERIENCE FINISHED!"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "💡 What you learned:"
	@echo "   • How to select AI models for different use cases"
	@echo "   • Performance characteristics of Gemini models"
	@echo "   • Cost-benefit analysis for model selection"
	@echo "   • Production deployment considerations"
	@echo ""
	@echo "🚀 Ready to build? Check out the source code in model_selector/"

# Clean up cache files and build artifacts
clean:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🧹 CLEANING UP CACHE FILES AND ARTIFACTS"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "⏳ Removing cache files..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .coverage -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name htmlcov -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type f -name "benchmark_results.json" -delete 2>/dev/null || true
	find . -type f -name "comparison_results.json" -delete 2>/dev/null || true
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "✅ CLEANUP COMPLETE"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🗑️  Removed:"
	@echo "   • Python cache files (__pycache__, *.pyc)"
	@echo "   • Test artifacts (.pytest_cache, .coverage)"
	@echo "   • Build artifacts (*.egg-info)"
	@echo "   • Generated reports (htmlcov/, benchmark_results.json)"
	@echo ""
	@echo "💡 Your source code and configuration files are preserved"

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
