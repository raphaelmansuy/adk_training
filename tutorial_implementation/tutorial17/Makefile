# Tutorial 17: Agent-to-Agent Communication - Official ADK Implementation
# Makefile for setup, development, testing, and demo
# Updated to use official Google ADK patterns and adk api_server commands

.PHONY: help setup dev test demo clean lint format start-agents stop-agents check-agents

# Default target
help:
	@printf "\n🚀 Tutorial 17: Agent-to-Agent Communication (Official ADK)\n\n"
	@printf "Available commands:\n"
	@printf "  %-15s %s\n" "setup" "Install dependencies and setup environment"
	@printf "  %-15s %s\n" "start-agents" "Start all remote A2A agents (official ADK)"
	@printf "  %-15s %s\n" "stop-agents" "Stop all running agents (clean)"
	@printf "  %-15s %s\n" "check-agents" "Check agent status and availability"
	@printf "  %-15s %s\n" "dev" "Start ADK web interface"
	@printf "  %-15s %s\n" "test" "Run all tests"
	@printf "  %-15s %s\n" "demo" "Show tutorial overview and examples"
	@printf "  %-15s %s\n" "clean" "Clean cache files and artifacts"
	@printf "  %-15s %s\n" "lint" "Run linting checks"
	@printf "  %-15s %s\n" "format" "Format code with black and isort"
	@printf "\n"

# Setup environment
setup:
	@printf "📦 Setting up Tutorial 17 environment...\n"
	@pip install -r requirements.txt || { printf "❌ Failed to install requirements\n"; exit 1; }
	@pip install -e . || { printf "❌ Failed to install main package\n"; exit 1; }
	@printf "✅ Setup complete!\n"
	@printf "📋 Google ADK Version: $(shell pip show google-adk | grep Version | cut -d' ' -f2)\n"
	@printf "💡 Copy a2a_orchestrator/.env.example to .env and add your API keys.\n"

# Development mode - start ADK web interface
dev:
	@printf "🌐 Starting ADK web interface...\n"
	@printf "   Open: http://localhost:8000\n"
	@printf "   Select: 'a2a_orchestrator' from agent dropdown\n\n"
	@adk web

# Run tests
test:
	@printf "🧪 Running tests...\n"
	@pytest tests/ -v --tb=short

# Demo - show example usage
demo:
	@printf "\n🎯 Tutorial 17: Agent-to-Agent Communication (Official ADK)\n\n"
	@printf "This tutorial demonstrates distributed agent orchestration using official Google ADK.\n\n"
	@printf "🔧 Key Features:\n"
	@printf "  • Official RemoteA2aAgent for A2A communication\n"
	@printf "  • Agent discovery via .well-known/agent-card.json\n"
	@printf "  • Sub-agent pattern with automatic delegation\n"
	@printf "  • Three specialized remote agents with official ADK patterns\n\n"
	@printf "🤖 Remote Agents:\n"
	@printf "  📚 Research: http://localhost:8001 (web search, fact-checking)\n"
	@printf "  📊 Analysis: http://localhost:8002 (data analysis, insights)\n"
	@printf "  ✍️  Content:  http://localhost:8003 (content creation, formatting)\n\n"
	@printf "💡 Example Queries:\n"
	@printf "  • 'Research quantum computing developments and create summary'\n"
	@printf "  • 'Analyze electric vehicle market trends'\n"
	@printf "  • 'Create technical documentation for our AI platform'\n\n"
	@printf "🚀 Quick Start:\n"
	@printf "  1. make setup\n"
	@printf "  2. Copy .env.example to .env + add GOOGLE_API_KEY\n"
	@printf "  3. make start-agents  (starts official ADK A2A servers)\n"
	@printf "  4. make check-agents  (verify communication works)\n"
	@printf "  5. make dev          (start ADK web interface)\n\n"
	@printf "🔧 Management Commands:\n"
	@printf "  • make check-agents  (verify all agents are running)\n"
	@printf "  • make stop-agents   (clean shutdown)\n"
	@printf "  • ./start_a2a_servers.sh  (direct script usage)\n"
	@printf "  • ./stop_a2a_servers.sh   (direct cleanup)\n\n"
	@printf "✨ Official ADK Implementation:\n"
	@printf "  • Uses RemoteA2aAgent class from google.adk.agents\n"
	@printf "  • Official to_a2a() function for exposing agents\n"
	@printf "  • Auto-generated .well-known/agent-card.json\n"
	@printf "  • uvicorn + to_a2a() pattern for A2A servers\n\n"

# Clean up
clean:
	@printf "🧹 Cleaning up...\n"
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type f -name ".coverage" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".adk_cache" -exec rm -rf {} + 2>/dev/null || true
	@rm -f .agent_pids 2>/dev/null || true
	@printf "✅ Cleanup complete.\n"

# Linting
lint:
	@printf "🔍 Running linting checks...\n"
	@flake8 a2a_orchestrator tests --max-line-length=100 || { printf "❌ Linting failed\n"; exit 1; }
	@printf "✅ Linting checks passed (formatting may need attention).\n"

# Code formatting
format:
	@printf "🎨 Formatting code...\n"
	@isort a2a_orchestrator tests || { printf "❌ Import sorting failed\n"; exit 1; }
	@black a2a_orchestrator tests || { printf "❌ Black formatting failed\n"; exit 1; }
	@printf "✅ Code formatting complete.\n"

# Start remote A2A agents using official ADK command
start-agents:
	@printf "🚀 Starting remote A2A agents with official ADK servers...\n"
	@./start_a2a_servers.sh

# Stop remote agents using official ADK cleanup
stop-agents:
	@printf "🛑 Stopping remote A2A agents with clean shutdown...\n"
	@./stop_a2a_servers.sh

# Check agent status and availability
check-agents:
	@printf "🔍 Checking A2A agent status...\n\n"
	@printf " Research Agent (8001): "
	@curl -s http://localhost:8001/.well-known/agent-card.json | jq -r '.name' 2>/dev/null || printf "❌ Not responding\n"
	@printf "📊 Analysis Agent (8002): "
	@curl -s http://localhost:8002/.well-known/agent-card.json | jq -r '.name' 2>/dev/null || printf "❌ Not responding\n"
	@printf "✍️  Content Agent (8003):  "
	@curl -s http://localhost:8003/.well-known/agent-card.json | jq -r '.name' 2>/dev/null || printf "❌ Not responding\n"
	@printf "\n💡 If agents are not responding, run 'make start-agents'\n"