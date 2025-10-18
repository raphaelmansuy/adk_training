# Tutorial 34: Google Cloud Pub/Sub + Event-Driven Agents
# Makefile for development, testing, and GCP infrastructure management
#
# Key Features:
#   • Idempotent commands (safe to run multiple times)
#   • Excellent UX with progress indicators
#   • Local and Cloud infrastructure support
#   • Comprehensive cleanup

.PHONY: help setup test demo clean dev-env check-deps gcp-setup gcp-destroy gcp-status web test-cov

# Color codes for UX
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m  # No Color

# Default target - show help
help:
	@echo "$(BLUE)🚀 Tutorial 34: Google Cloud Pub/Sub + Event-Driven Agents$(NC)"
	@echo ""
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo "$(GREEN)QUICK START - Local Development$(NC)"
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo "  $(YELLOW)make setup$(NC)        Install dependencies (idempotent)"
	@echo "  $(YELLOW)make test$(NC)         Run all tests locally"
	@echo "  $(YELLOW)make web$(NC)          Launch ADK web UI for local testing"
	@echo "  $(YELLOW)make demo$(NC)         Show example usage"
	@echo ""
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo "$(GREEN)DEVELOPMENT & MAINTENANCE$(NC)"
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo "  $(YELLOW)make test-cov$(NC)     Run tests with coverage report"
	@echo "  $(YELLOW)make dev-env$(NC)      Show environment info"
	@echo "  $(YELLOW)make check-deps$(NC)   Verify all dependencies"
	@echo "  $(YELLOW)make clean$(NC)        Clean cache and build artifacts"
	@echo ""
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo "$(GREEN)GOOGLE CLOUD DEPLOYMENT (Optional)$(NC)"
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo "  $(YELLOW)make gcp-setup$(NC)    Create GCP Pub/Sub resources"
	@echo "  $(YELLOW)make gcp-status$(NC)   Check GCP resource status"
	@echo "  $(YELLOW)make gcp-destroy$(NC)  Remove all GCP resources"
	@echo ""
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo "$(GREEN)Quick Links$(NC)"
	@echo "  📚 Tutorial: docs/tutorial/34_pubsub_adk_integration.md"
	@echo "  💡 First time? Run: $(YELLOW)make setup && make test$(NC)"
	@echo "$(BLUE)━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"

# ============================================================================
# LOCAL DEVELOPMENT TARGETS
# ============================================================================

# Install dependencies (idempotent - safe to run multiple times)
setup: check-python
	@echo "$(BLUE)📦 Setting up development environment...$(NC)"
	@echo ""
	@echo "$(YELLOW)Step 1/3: Installing Python dependencies$(NC)"
	@pip install -r requirements.txt > /dev/null 2>&1 && \
		echo "  $(GREEN)✓$(NC) Python packages installed" || \
		(echo "  $(RED)✗$(NC) Failed to install packages"; exit 1)
	@echo ""
	@echo "$(YELLOW)Step 2/3: Installing package in editable mode$(NC)"
	@pip install -e . > /dev/null 2>&1 && \
		echo "  $(GREEN)✓$(NC) Package installed (editable)" || \
		(echo "  $(RED)✗$(NC) Failed to install package"; exit 1)
	@echo ""
	@echo "$(YELLOW)Step 3/3: Verifying installation$(NC)"
	@python -c "from pubsub_agent.agent import root_agent; print('  $(GREEN)✓$(NC) Agent imports successfully')" || \
		(echo "  $(RED)✗$(NC) Agent import failed"; exit 1)
	@echo ""
	@echo "$(GREEN)✅ Setup complete!$(NC)"
	@echo "  Next steps:"
	@echo "    • Run tests: $(YELLOW)make test$(NC)"
	@echo "    • View demo: $(YELLOW)make demo$(NC)"
	@echo ""

# Show development environment info
dev-env:
	@echo "$(BLUE)📋 Development Environment$(NC)"
	@echo ""
	@python3 --version
	@echo ""
	@echo "$(YELLOW)Python packages:$(NC)"
	@pip list | grep -E "google|pytest|adk" || echo "  (No matching packages found)"
	@echo ""
	@echo "$(YELLOW)Project structure:$(NC)"
	@find . -maxdepth 1 -type f \( -name "*.py" -o -name "*.toml" -o -name "Makefile" \) | sort | sed 's|^\./|  • |'
	@echo ""

# Check Python dependencies
check-deps:
	@echo "$(BLUE)🔍 Checking dependencies$(NC)"
	@echo ""
	@python3 -c "import google.adk; print('  $(GREEN)✓$(NC) google-adk installed')" 2>/dev/null || \
		(echo "  $(RED)✗$(NC) google-adk not installed"; echo "  Run: make setup"; exit 1)
	@python3 -c "import google.cloud.pubsub_v1; print('  $(GREEN)✓$(NC) google-cloud-pubsub installed')" 2>/dev/null || \
		(echo "  $(RED)✗$(NC) google-cloud-pubsub not installed"; echo "  Run: make setup"; exit 1)
	@python3 -c "import pytest; print('  $(GREEN)✓$(NC) pytest installed')" 2>/dev/null || \
		(echo "  $(RED)✗$(NC) pytest not installed"; echo "  Run: make setup"; exit 1)
	@echo ""
	@echo "$(GREEN)✅ All dependencies verified$(NC)"
	@echo ""

# Run tests
test: check-python
	@echo "$(BLUE)🧪 Running test suite$(NC)"
	@echo ""
	@pytest tests/ -v --tb=short 2>&1 | tail -20
	@echo ""

# Run tests with coverage
test-cov: check-python
	@echo "$(BLUE)📊 Running tests with coverage report$(NC)"
	@echo ""
	@pytest tests/ -v --cov=pubsub_agent --cov-report=term-missing 2>&1 | tail -30
	@echo ""

# Run a quick demo
demo:
	@echo "$(BLUE)🎯 Tutorial 34 Demo: Event-Driven Document Processing$(NC)"
	@echo ""
	@echo "$(YELLOW)📋 Architecture Overview:$(NC)"
	@echo "   1. Publisher → Sends documents to Pub/Sub topic"
	@echo "   2. Agent     → Processes documents (summarize, extract entities)"
	@echo "   3. Subscriber → Receives results"
	@echo ""
	@echo "$(YELLOW)🔧 Components in this tutorial:$(NC)"
	@echo "   • pubsub_agent/    - Main ADK agent for processing"
	@echo "   • publisher.py     - Example publisher script"
	@echo "   • subscriber.py    - Example subscriber script"
	@echo ""
	@echo "$(YELLOW)📝 Testing locally (without GCP):$(NC)"
	@echo "   $$ make test"
	@echo ""
	@echo "$(YELLOW)☁️  Deploying to GCP:$(NC)"
	@echo "   $$ make gcp-setup        # Create resources"
	@echo "   $$ python publisher.py   # Publish documents"
	@echo "   $$ python subscriber.py  # Process documents"
	@echo "   $$ make gcp-destroy      # Clean up"
	@echo ""
	@echo "$(GREEN)✅ Ready! See tutorial for detailed instructions.$(NC)"
	@echo ""

# Launch ADK web UI for local testing and development
web: check-python setup
	@echo "$(BLUE)🌐 Launching ADK Development UI$(NC)"
	@echo ""
	@echo "$(GREEN)Starting ADK web server...$(NC)"
	@echo "$(YELLOW)📍 Open your browser at: http://localhost:8000$(NC)"
	@echo ""
	@echo "$(YELLOW)Features available:$(NC)"
	@echo "  • Test agent with custom prompts"
	@echo "  • View agent configuration"
	@echo "  • Inspect structured outputs"
	@echo "  • Debug agent behavior"
	@echo ""
	@echo "$(YELLOW)Press Ctrl+C to stop the server$(NC)"
	@echo ""
	@adk web

# ============================================================================
# GCP INFRASTRUCTURE TARGETS (IDEMPOTENT)
# ============================================================================

# Setup GCP Pub/Sub resources (idempotent)
gcp-setup: check-gcloud check-project
	@echo "$(BLUE)☁️  Setting up Google Cloud Pub/Sub resources$(NC)"
	@echo ""
	@PROJECT=$$(gcloud config get-value project 2>/dev/null); \
	echo "$(YELLOW)Target project: $$PROJECT$(NC)"; \
	echo ""
	@echo "$(YELLOW)Step 1/4: Creating Pub/Sub topic$(NC)"
	@gcloud pubsub topics create document-uploads \
		--quiet --project=$$(gcloud config get-value project) 2>/dev/null && \
		echo "  $(GREEN)✓$(NC) Topic 'document-uploads' created" || \
		echo "  $(GREEN)✓$(NC) Topic 'document-uploads' already exists"
	@echo ""
	@echo "$(YELLOW)Step 2/4: Creating processor subscription$(NC)"
	@gcloud pubsub subscriptions create document-processor \
		--topic=document-uploads \
		--ack-deadline=600 \
		--quiet --project=$$(gcloud config get-value project) 2>/dev/null && \
		echo "  $(GREEN)✓$(NC) Subscription 'document-processor' created" || \
		echo "  $(GREEN)✓$(NC) Subscription 'document-processor' already exists"
	@echo ""
	@echo "$(YELLOW)Step 3/4: Creating results topic$(NC)"
	@gcloud pubsub topics create document-results \
		--quiet --project=$$(gcloud config get-value project) 2>/dev/null && \
		echo "  $(GREEN)✓$(NC) Topic 'document-results' created" || \
		echo "  $(GREEN)✓$(NC) Topic 'document-results' already exists"
	@echo ""
	@echo "$(YELLOW)Step 4/4: Creating DLQ topic$(NC)"
	@gcloud pubsub topics create document-dlq \
		--quiet --project=$$(gcloud config get-value project) 2>/dev/null && \
		echo "  $(GREEN)✓$(NC) Topic 'document-dlq' created" || \
		echo "  $(GREEN)✓$(NC) Topic 'document-dlq' already exists"
	@echo ""
	@echo "$(GREEN)✅ GCP resources ready!$(NC)"
	@echo "  Next steps:"
	@echo "    • Check status: $(YELLOW)make gcp-status$(NC)"
	@echo "    • Run publisher: $(YELLOW)python publisher.py$(NC)"
	@echo "    • Clean up: $(YELLOW)make gcp-destroy$(NC)"
	@echo ""

# Show GCP resource status (idempotent)
gcp-status: check-gcloud check-project
	@echo "$(BLUE)☁️  Google Cloud Pub/Sub Resources$(NC)"
	@echo ""
	@PROJECT=$$(gcloud config get-value project 2>/dev/null); \
	echo "$(YELLOW)Project: $$PROJECT$(NC)"; \
	echo ""
	@echo "$(YELLOW)Topics:$(NC)"
	@gcloud pubsub topics list --project=$$(gcloud config get-value project) \
		--filter="name:document*" --format="table(name)" 2>/dev/null | \
		sed 's|projects/.*/topics/|  • |' || echo "  (No topics found)"
	@echo ""
	@echo "$(YELLOW)Subscriptions:$(NC)"
	@gcloud pubsub subscriptions list --project=$$(gcloud config get-value project) \
		--filter="name:document*" --format="table(name)" 2>/dev/null | \
		sed 's|projects/.*/subscriptions/|  • |' || echo "  (No subscriptions found)"
	@echo ""
	@echo "$(YELLOW)Message Stats:$(NC)"
	@gcloud pubsub subscriptions describe document-processor \
		--project=$$(gcloud config get-value project) \
		--format="table(messageRetentionDuration, expirationPolicy)" 2>/dev/null || \
		echo "  (Subscription not found - run 'make gcp-setup' first)"
	@echo ""

# Destroy GCP resources (idempotent with confirmation)
gcp-destroy: check-gcloud check-project
	@echo "$(RED)⚠️  WARNING: This will delete GCP Pub/Sub resources$(NC)"
	@echo ""
	@echo "$(YELLOW)Resources to be deleted:$(NC)"
	@echo "  • Subscriptions: document-processor"
	@echo "  • Topics: document-uploads, document-results, document-dlq"
	@echo ""
	@read -p "$(YELLOW)Continue? (yes/no): $(NC)" CONFIRM; \
	if [ "$$CONFIRM" = "yes" ]; then \
		echo ""; \
		echo "$(YELLOW)Deleting subscriptions...$(NC)"; \
		gcloud pubsub subscriptions delete document-processor \
			--quiet --project=$$(gcloud config get-value project) 2>/dev/null && \
			echo "  $(GREEN)✓$(NC) Subscription deleted" || \
			echo "  $(GREEN)✓$(NC) Subscription already deleted"; \
		echo ""; \
		echo "$(YELLOW)Deleting topics...$(NC)"; \
		gcloud pubsub topics delete document-uploads \
			--quiet --project=$$(gcloud config get-value project) 2>/dev/null && \
			echo "  $(GREEN)✓$(NC) Topic 'document-uploads' deleted" || \
			echo "  $(GREEN)✓$(NC) Already deleted"; \
		gcloud pubsub topics delete document-results \
			--quiet --project=$$(gcloud config get-value project) 2>/dev/null && \
			echo "  $(GREEN)✓$(NC) Topic 'document-results' deleted" || \
			echo "  $(GREEN)✓$(NC) Already deleted"; \
		gcloud pubsub topics delete document-dlq \
			--quiet --project=$$(gcloud config get-value project) 2>/dev/null && \
			echo "  $(GREEN)✓$(NC) Topic 'document-dlq' deleted" || \
			echo "  $(GREEN)✓$(NC) Already deleted"; \
		echo ""; \
		echo "$(GREEN)✅ Cleanup complete!$(NC)"; \
	else \
		echo "$(YELLOW)Cancelled.$(NC)"; \
	fi
	@echo ""

# ============================================================================
# MAINTENANCE TARGETS
# ============================================================================

# Clean up local files
clean:
	@echo "$(BLUE)🧹 Cleaning up local build artifacts$(NC)"
	@echo ""
	@echo "$(YELLOW)Removing Python cache files...$(NC)"
	@find . -type f -name "*.pyc" -delete && \
		echo "  $(GREEN)✓$(NC) Removed .pyc files"
	@find . -type d -name "__pycache__" -delete && \
		echo "  $(GREEN)✓$(NC) Removed __pycache__ directories"
	@echo ""
	@echo "$(YELLOW)Removing pytest cache...$(NC)"
	@rm -rf .pytest_cache/ && \
		echo "  $(GREEN)✓$(NC) Removed .pytest_cache"
	@echo ""
	@echo "$(YELLOW)Removing coverage data...$(NC)"
	@rm -rf .coverage htmlcov/ && \
		echo "  $(GREEN)✓$(NC) Removed coverage files"
	@echo ""
	@echo "$(GREEN)✅ Cleanup complete!$(NC)"
	@echo ""

# ============================================================================
# HELPER TARGETS (Internal use)
# ============================================================================

# Check Python availability
check-python:
	@python3 --version > /dev/null 2>&1 || \
		(echo "$(RED)Error: Python 3 not found$(NC)"; exit 1)

# Check gcloud availability
check-gcloud:
	@command -v gcloud > /dev/null 2>&1 || \
		(echo "$(RED)❌ Error: gcloud CLI not installed$(NC)"; \
		echo "$(YELLOW)Install from: https://cloud.google.com/sdk/docs/install$(NC)"; exit 1)

# Check GCP project is set
check-project:
	@PROJECT=$$(gcloud config get-value project 2>/dev/null); \
	if [ -z "$$PROJECT" ]; then \
		echo "$(RED)❌ Error: No GCP project selected$(NC)"; \
		echo "$(YELLOW)Set project with: gcloud config set project YOUR_PROJECT_ID$(NC)"; \
		exit 1; \
	fi
