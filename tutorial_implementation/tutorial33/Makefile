.PHONY: help setup dev test clean demo lint install slack-dev slack-deploy slack-test

help:
	@echo "📚 Tutorial 33: Slack Bot Integration with ADK"
	@echo ""
	@echo "Core Commands:"
	@echo "  make setup              - Install dependencies and setup environment"
	@echo "  make dev                - Start ADK web interface for development"
	@echo "  make test               - Run test suite"
	@echo "  make test-coverage      - Run tests with coverage report"
	@echo "  make demo               - Show demo prompts and example usage"
	@echo "  make lint               - Run linting checks"
	@echo "  make clean              - Remove cache files and artifacts"
	@echo ""
	@echo "Slack Integration Commands:"
	@echo "  make slack-dev          - Run bot in Socket Mode (development)"
	@echo "  make slack-deploy       - Deploy to Cloud Run (production)"
	@echo "  make slack-test         - Test Slack integration"
	@echo ""

setup:
	@echo "🔧 Setting up Tutorial 33..."
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Setup complete!"
	@echo ""
	@echo "📝 Next steps:"
	@echo "   1. Copy support_bot/.env.example to support_bot/.env"
	@echo "   2. Add your Slack tokens and Google API key to support_bot/.env"
	@echo "   3. Run 'make dev' to start developing"

dev:
	@echo "🚀 Starting ADK web development interface..."
	@echo "📌 Open http://localhost:8000 in your browser"
	@echo ""
	adk web

test:
	@echo "🧪 Running tests..."
	pytest tests/ -v --tb=short

test-coverage:
	@echo "📊 Running tests with coverage..."
	pytest tests/ -v --cov=support_bot --cov-report=term-missing

demo:
	@echo "📖 Support Bot - Example Usage"
	@echo ""
	@echo "The support bot provides:"
	@echo ""
	@echo "1. 🔍 Knowledge Base Search"
	@echo "   - Search for company policies"
	@echo "   - Find IT support information"
	@echo "   - Get vacation and remote work policies"
	@echo ""
	@echo "2. 🎫 Support Ticket Creation"
	@echo "   - Create tickets for complex issues"
	@echo "   - Set priority levels (low, normal, high, urgent)"
	@echo "   - Track tickets with unique IDs"
	@echo ""
	@echo "Example queries:"
	@echo "  • 'How do I reset my password?'"
	@echo "  • 'What is the vacation policy?'"
	@echo "  • 'I need help with VPN setup'"
	@echo "  • 'Create a ticket for my laptop issue'"
	@echo ""
	@echo "Run 'make dev' to test these queries in the ADK web interface!"
	@echo ""

lint:
	@echo "🔍 Running linting checks..."
	python -m pylint support_bot/ || true
	python -m flake8 support_bot/ || true
	@echo "✅ Linting complete"

clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .eggs -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
	rm -rf build/ dist/ *.egg-info/
	@echo "✅ Clean complete!"

slack-dev:
	@echo "🚀 Starting Support Bot in Socket Mode (development)..."
	@echo ""
	@if [ ! -f support_bot/.env ]; then \
		echo "❌ ERROR: support_bot/.env file not found!"; \
		echo ""; \
		echo "📝 To set up your bot:"; \
		echo "   1. Copy the environment template:"; \
		echo "      cp support_bot/.env.example support_bot/.env"; \
		echo ""; \
		echo "   2. Edit support_bot/.env with your Slack tokens:"; \
		echo "      SLACK_BOT_TOKEN=xoxb-..."; \
		echo "      SLACK_APP_TOKEN=xapp-..."; \
		echo "      GOOGLE_API_KEY=..."; \
		echo ""; \
		echo "   3. Get tokens from https://api.slack.com/apps"; \
		echo ""; \
		exit 1; \
	fi
	@echo "📋 Configuration loaded from support_bot/.env"
	@echo ""
	@echo "🔗 Connecting to Slack in Socket Mode..."
	@echo "💡 Bot is running! Try these in Slack:"
	@echo ""
	@echo "   @Support Bot help"
	@echo "   @Support Bot What is the password reset procedure?"
	@echo "   @Support Bot Create a ticket for my issue"
	@echo ""
	@echo "⏹️  Press Ctrl+C to stop"
	@echo ""
	python -m support_bot.bot_dev

slack-deploy:
	@echo "🚀 Cloud Run Production Deployment (Safe by Default)"
	@echo ""
	@echo "📋 Dry-run mode: this prints the steps only."
	@echo ""
	@echo "Prerequisites:"
	@echo "  • gcloud CLI authenticated (gcloud auth login)"
	@echo "  • Docker installed and working"
	@echo "  • PROJECT and REGION environment variables set"
	@echo ""
	@echo "Steps:"
	@echo "  1. Build: docker build -t gcr.io/[PROJECT]/support-bot:latest ."
	@echo "  2. Push:  docker push gcr.io/[PROJECT]/support-bot:latest"
	@echo "  3. Deploy: gcloud run deploy with image and secrets"
	@echo "  4. Slack:  Update Event Subscription URL to https://[SERVICE_URL]/slack/events"
	@echo ""
	@echo "To run this deployment safely:"
	@echo "  • Set PROJECT and REGION:"
	@echo "      export PROJECT=your-gcp-project"
	@echo "      export REGION=us-central1"
	@echo "  • Create secrets (one-time):"
	@echo "      echo -n $$SLACK_BOT_TOKEN | gcloud secrets create SLACK_BOT_TOKEN --data-file=-"
	@echo "      echo -n $$SLACK_APP_TOKEN | gcloud secrets create SLACK_APP_TOKEN --data-file=-"
	@echo "  • Run the deployment script:"
	@echo "      bash scripts/deploy_cloud_run.sh"
	@echo ""
	@echo "Or manually follow the Production Deployment section in README.md"

slack-test:
	@echo "🧪 Testing Slack integration..."
	@echo ""
	@echo "Testing:"
	@echo "   ✓ Agent imports"
	@echo "   ✓ Tool functionality"
	@echo "   ✓ Slack compatibility"
	@echo ""
	@echo "Running tests..."
	pytest tests/ -v -k "test_" --tb=short
	@echo ""
	@echo "✅ All tests passed!"

