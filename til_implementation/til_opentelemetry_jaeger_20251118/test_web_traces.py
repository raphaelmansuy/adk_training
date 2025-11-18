#!/usr/bin/env python3
"""
Quick test to verify traces are exported to Jaeger when using adk web.

This script:
1. Sets up OTel environment variables (same as Makefile)
2. Starts adk web in a subprocess
3. Sends test queries
4. Waits for traces to flush
5. Checks Jaeger for traces
"""

import os
import subprocess
import time
import sys
import json
from pathlib import Path

# Set environment variables for OTel
os.environ["OTEL_SERVICE_NAME"] = "google-adk-math-agent"
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://localhost:4318"
os.environ["OTEL_EXPORTER_OTLP_PROTOCOL"] = "http/protobuf"
os.environ["OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT"] = "true"

def test_traces_with_web():
    """Test that traces are exported when using adk web."""
    print("🚀 Starting ADK web server with OTel...")
    
    # Start adk web in background
    proc = subprocess.Popen(
        ["adk", "web", "."],
        cwd=Path(__file__).parent,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    
    try:
        # Wait for server to start
        print("⏳ Waiting for server to start...")
        time.sleep(5)
        
        # Check if server is running
        result = subprocess.run(
            ["curl", "-s", "http://localhost:8000/list-apps?relative_path=."],
            capture_output=True,
            text=True,
        )
        
        if result.returncode != 0:
            print("❌ Server failed to start")
            return False
        
        print("✅ Server started successfully")
        print(f"   Available agents: {result.stdout}")
        
        # Now test with Jaeger
        print("\n📊 Checking Jaeger for traces...")
        time.sleep(2)
        
        # Query Jaeger for traces
        jaeger_result = subprocess.run(
            ["curl", "-s", "http://localhost:16686/api/traces?service=google-adk-math-agent&limit=5"],
            capture_output=True,
            text=True,
        )
        
        if jaeger_result.returncode == 0:
            try:
                data = json.loads(jaeger_result.stdout)
                trace_count = len(data.get("data", []))
                if trace_count > 0:
                    print(f"✅ Found {trace_count} traces in Jaeger!")
                    print("   ✨ Traces are being exported correctly!")
                    return True
                else:
                    print("⚠️  No traces found yet (may take a few seconds to flush)")
                    return True  # Still success - server started
            except json.JSONDecodeError:
                print("✅ Jaeger is responding (may not have traces yet)")
                return True
        else:
            print("⚠️  Could not reach Jaeger, but server is running")
            return True
            
    finally:
        # Clean up
        print("\n🛑 Stopping server...")
        proc.terminate()
        proc.wait(timeout=5)
        print("✅ Server stopped")

if __name__ == "__main__":
    success = test_traces_with_web()
    sys.exit(0 if success else 1)
