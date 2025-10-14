# Tutorial 29: UI Integration Quick Start
# Makefile for managing backend and frontend

.PHONY: help setup setup-backend setup-frontend dev dev-backend dev-frontend test clean demo

# Default target - show help
help:
	@echo "🚀 Tutorial 29: UI Integration Quick Start"
	@echo ""
	@echo "Quick Start Commands:"
	@echo "  make setup          - Install all dependencies (backend + frontend)"
	@echo "  make dev            - Start both backend and frontend servers"
	@echo "  make dev-backend    - Start only the backend server"
	@echo "  make dev-frontend   - Start only the frontend server"
	@echo "  make demo           - Show demo prompts and usage"
	@echo ""
	@echo "Advanced Commands:"
	@echo "  make test           - Run all tests"
	@echo "  make clean          - Clean up generated files"
	@echo ""
	@echo "💡 First time? Run: make setup && make dev"
	@echo ""
	@echo "Architecture:"
	@echo "  Backend:  Python FastAPI + ADK agent (port 8000)"
	@echo "  Frontend: React + Vite + CopilotKit (port 5173)"

# Install all dependencies
setup: setup-backend setup-frontend
	@echo "✅ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Configure API key: cp agent/.env.example agent/.env"
	@echo "  2. Edit agent/.env and add your GOOGLE_API_KEY"
	@echo "  3. Run: make dev"

# Install backend dependencies
setup-backend:
	@echo "📦 Installing backend dependencies..."
	pip install -r requirements.txt
	pip install -e .
	@echo "✅ Backend setup complete!"

# Install frontend dependencies
setup-frontend:
	@echo "📦 Installing frontend dependencies..."
	@if [ ! -d "frontend/node_modules" ]; then \
		cd frontend && npm install; \
	else \
		echo "Frontend dependencies already installed. Run 'make clean' to reinstall."; \
	fi
	@echo "✅ Frontend setup complete!"

# Start both backend and frontend
dev:
	@echo "🚀 Starting backend and frontend servers..."
	@echo ""
	@echo "This will open two terminals:"
	@echo "  Terminal 1: Backend (http://localhost:8000)"
	@echo "  Terminal 2: Frontend (http://localhost:5173)"
	@echo ""
	@echo "Press Ctrl+C to stop both servers"
	@echo ""
	@$(MAKE) dev-parallel

# Start backend and frontend in parallel (internal use)
dev-parallel: check-env
	@trap 'kill 0' EXIT; \
	(cd agent && python agent.py) & \
	(cd frontend && npm run dev) & \
	wait

# Start only backend server
dev-backend: check-env
	@echo "🤖 Starting Backend Server..."
	@echo "📱 Server: http://localhost:8000"
	@echo "📚 API Docs: http://localhost:8000/docs"
	@echo "💬 CopilotKit endpoint: http://localhost:8000/api/copilotkit"
	@echo ""
	cd agent && python agent.py

# Start only frontend server
dev-frontend:
	@echo "🌐 Starting Frontend Server..."
	@echo "📱 Open http://localhost:5173 in your browser"
	@echo ""
	@echo "⚠️  Make sure backend is running on port 8000"
	@echo "    Run in another terminal: make dev-backend"
	@echo ""
	cd frontend && npm run dev

# Run tests
test: check-env
	@echo "🧪 Running tests..."
	pytest tests/ -v --tb=short

# Run demo
demo: check-env
	@echo "💬 Demo: Tutorial 29 - UI Integration Quick Start"
	@echo ""
	@echo "=================================="
	@echo "Try These Prompts in the Chat UI:"
	@echo "=================================="
	@echo ""
	@echo "🤖 General Questions:"
	@echo "  • 'What is Google ADK?'"
	@echo "  • 'How does the AG-UI Protocol work?'"
	@echo "  • 'Explain the benefits of UI integration'"
	@echo "  • 'What can you help me with?'"
	@echo ""
	@echo "📚 Learning:"
	@echo "  • 'Tell me about different UI integration approaches'"
	@echo "  • 'When should I use CopilotKit vs native API?'"
	@echo "  • 'How do I deploy an ADK agent?'"
	@echo ""
	@echo "=================================="
	@echo ""
	@echo "Usage Instructions:"
	@echo "  1. Start servers: make dev"
	@echo "  2. Open http://localhost:5173"
	@echo "  3. Type any of the prompts above"
	@echo "  4. The agent responds using Gemini!"
	@echo ""
	@echo "Architecture:"
	@echo "  User → React/Vite (port 5173) → FastAPI (port 8000) → ADK Agent → Gemini"

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache/
	cd frontend && rm -rf dist/ node_modules/.cache/ || true
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
