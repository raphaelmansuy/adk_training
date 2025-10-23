.PHONY: setup clean test dev help docker-up docker-down

help:
	@echo ""
	@echo "╔════════════════════════════════════════════════════════════════╗"
	@echo "║  Custom Session Services TIL - Redis Session Storage Demo     ║"
	@echo "╚════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "🎯 QUICK START:"
	@echo "   make setup          Install dependencies"
	@echo "   make dev            Start ADK web with Redis sessions"
	@echo "   make test           Run unit tests"
	@echo ""
	@echo "🐳 DOCKER:"
	@echo "   make docker-up      Start Redis container (port 6379)"
	@echo "   make docker-down    Stop containers"
	@echo ""
	@echo "🧹 CLEANUP:"
	@echo "   make clean          Remove cache files"
	@echo ""
	@echo "📖 FULL GUIDE:"
	@echo "   1. make setup"
	@echo "   2. make docker-up"
	@echo "   3. make dev"
	@echo "   4. Open http://127.0.0.1:8000"
	@echo "   5. Select: custom_session_agent"
	@echo ""
	@echo "✨ Try sending: 'Write me a poem'"
	@echo "   Then refresh the browser to test persistence!"
	@echo ""

setup:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Done!"

docker-up:
	@echo "🐳 Starting Redis..."
	docker-compose up -d redis
	@echo "⏳ Waiting for Redis to be ready..."
	sleep 2
	redis-cli ping 2>/dev/null || sleep 2
	@echo "✅ Redis ready at redis://localhost:6379"

docker-down:
	@echo "🛑 Stopping Redis..."
	docker-compose down
	@echo "✅ Stopped"

dev: docker-up
	@echo ""
	@echo "🚀 Starting ADK web interface..."
	@echo "   Agent: custom_session_agent"
	@echo "   Backend: Redis (redis://localhost:6379)"
	@echo "   URL: http://127.0.0.1:8000"
	@echo ""
	python -m custom_session_agent web --session_service_uri=redis://localhost:6379

test:
	@echo "🧪 Running tests..."
	pytest tests/ -v --tb=short
	@echo "✅ Tests complete!"

clean:
	@echo "🧹 Cleaning..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type d -name "*.egg-info" -delete
	@echo "✅ Clean!"
