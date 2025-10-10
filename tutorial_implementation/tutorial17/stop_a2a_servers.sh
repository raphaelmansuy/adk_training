#!/bin/bash

# Stop A2A Servers - Official ADK Implementation using to_a2a() function
# This script stops all running uvicorn servers hosting A2A agents

echo "🛑 Stopping ADK A2A servers..."

# Function to gracefully terminate processes on specific ports
stop_server_on_port() {
    local port=$1
    local agent_name=$2
    
    # Find process using the port
    PID=$(lsof -ti :$port 2>/dev/null)
    
    if [ -n "$PID" ]; then
        echo "🔸 Stopping $agent_name (PID: $PID) on port $port..."
        kill $PID 2>/dev/null
        
        # Wait for graceful shutdown
        local attempts=0
        while [ $attempts -lt 10 ] && kill -0 $PID 2>/dev/null; do
            sleep 1
            attempts=$((attempts + 1))
        done
        
        # Force kill if still running
        if kill -0 $PID 2>/dev/null; then
            echo "⚠️  Force killing $agent_name (PID: $PID)..."
            kill -9 $PID 2>/dev/null
        fi
        
        echo "✅ $agent_name stopped"
    else
        echo "💡 No process found on port $port for $agent_name"
    fi
}

# Stop all known A2A servers
stop_server_on_port 8001 "Research Agent"
stop_server_on_port 8002 "Analysis Agent"
stop_server_on_port 8003 "Content Agent"

# Additional cleanup: kill any remaining uvicorn processes for our agents
echo "🧹 Cleaning up any remaining uvicorn processes..."
pkill -f "uvicorn.*research_agent\|uvicorn.*analysis_agent\|uvicorn.*content_agent" 2>/dev/null && echo "✅ Cleaned up remaining uvicorn processes" || echo "💡 No additional uvicorn processes found"

# Verify all processes are stopped
echo ""
echo "🔍 Verifying servers are stopped..."

all_stopped=true
for port in 8001 8002 8003; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "⚠️  Port $port is still in use"
        all_stopped=false
    fi
done

if [ "$all_stopped" = true ]; then
    echo "✅ All A2A servers have been stopped successfully!"
    echo ""
    echo "🚀 To restart servers, run: ./start_a2a_servers.sh"
else
    echo "❌ Some ports are still in use. You may need to manually kill processes:"
    echo "   lsof -ti :8001,8002,8003 | xargs kill -9"
fi

echo ""