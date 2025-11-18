.PHONY: help setup test demo web jaeger-up jaeger-down clean

# Color output
BOLD := \033[1m
GREEN := \033[32m
BLUE := \033[34m
YELLOW := \033[33m
RESET := \033[0m

help:
	@echo ""
	@echo "$(BOLD)🚀 OpenTelemetry + ADK + Jaeger$(RESET)"
	@echo ""
	@echo "$(BOLD)Quick Start (3 steps):$(RESET)"
	@echo "  1. $(GREEN)make setup$(RESET)      — Install dependencies"
	@echo "  2. $(GREEN)make jaeger-up$(RESET)  — Start Jaeger (observe traces)"
	@echo "  3. $(GREEN)make web$(RESET)        — Launch interactive chat at $(BLUE)http://localhost:8000$(RESET)"
	@echo ""
	@echo "$(BOLD)Then:$(RESET)"
	@echo "  • Ask the agent math questions in the web UI"
	@echo "  • View traces in Jaeger at $(BLUE)http://localhost:16686$(RESET)"
	@echo "  • Stop Jaeger with $(GREEN)make jaeger-down$(RESET)"
	@echo ""
	@echo "$(BOLD)Other Commands:$(RESET)"
	@echo "  $(GREEN)make demo$(RESET)          — Run demo with sample queries"
	@echo "  $(GREEN)make test$(RESET)          — Run 42 unit tests"
	@echo "  $(GREEN)make clean$(RESET)         — Remove cache files"
	@echo ""

setup:
	@echo "$(BOLD)📦 Installing dependencies...$(RESET)"
	pip install -r requirements.txt
	pip install -e .
	@echo "$(GREEN)✅ Done$(RESET)"
	@echo ""

test:
	@echo "$(BOLD)🧪 Running tests...$(RESET)"
	pytest tests/ -v --cov=math_agent --cov-report=term-missing
	@echo ""

demo:
	@echo "$(BOLD)🤖 Running demo...$(RESET)"
	@echo ""
	python -m math_agent.agent
	@echo ""

web:
	@echo "$(BOLD)🌐 Starting web UI at http://localhost:8000$(RESET)"
	@echo ""
	adk web .

jaeger-up:
	@echo "$(BOLD)🚀 Starting Jaeger...$(RESET)"
	docker run -d --name jaeger \
		-e COLLECTOR_OTLP_ENABLED=true \
		-p 16686:16686 -p 4318:4318 \
		jaegertracing/all-in-one:latest > /dev/null 2>&1
	@echo "$(GREEN)✅ Jaeger running at http://localhost:16686$(RESET)"
	@echo ""

jaeger-down:
	@echo "$(BOLD)🛑 Stopping Jaeger...$(RESET)"
	@docker stop jaeger > /dev/null 2>&1 && docker rm jaeger > /dev/null 2>&1 || true
	@echo "$(GREEN)✅ Jaeger stopped$(RESET)"
	@echo ""

clean:
	@echo "$(BOLD)🧹 Cleaning...$(RESET)"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	@echo "$(GREEN)✅ Done$(RESET)"
	@echo ""
