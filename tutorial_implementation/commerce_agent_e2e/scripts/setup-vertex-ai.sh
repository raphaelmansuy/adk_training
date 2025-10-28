#!/bin/bash
# ============================================================================
# setup-vertex-ai.sh
# 
# Configures the commerce agent to use Vertex AI authentication exclusively
# Unsets any conflicting Gemini API keys
# ============================================================================

set -e

echo "🔐 Vertex AI Authentication Setup"
echo "================================="
echo ""

# Check if credentials file exists
if [ ! -f "./credentials/commerce-agent-key.json" ]; then
    echo "❌ Error: Service account key not found at ./credentials/commerce-agent-key.json"
    echo ""
    echo "To set up a service account key, run:"
    echo "  See: log/20250124_173000_vertex_ai_setup_guide.md"
    exit 1
fi

echo "✅ Service account key found"
echo ""

# Get project ID from credentials file
PROJECT_ID=$(jq -r '.project_id' ./credentials/commerce-agent-key.json)
if [ -z "$PROJECT_ID" ] || [ "$PROJECT_ID" = "null" ]; then
    echo "❌ Error: Could not read project_id from credentials file"
    exit 1
fi

echo "✅ Project ID: $PROJECT_ID"
echo ""

# Unset Gemini API key if it exists
if [ ! -z "$GOOGLE_API_KEY" ]; then
    echo "⚠️  Unsetting GOOGLE_API_KEY to avoid conflicts..."
    unset GOOGLE_API_KEY
    echo "✅ GOOGLE_API_KEY unset"
    echo ""
fi

if [ ! -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  Unsetting GEMINI_API_KEY to avoid conflicts..."
    unset GEMINI_API_KEY
    echo "✅ GEMINI_API_KEY unset"
    echo ""
fi

# Set Vertex AI credentials
export GOOGLE_CLOUD_PROJECT="$PROJECT_ID"
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credentials/commerce-agent-key.json"

echo "✅ Environment variables set for Vertex AI:"
echo "   GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT"
echo "   GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS"
echo ""

# Verify credentials work
echo "🔍 Verifying credentials..."
python3 << 'VERIFY_CREDS'
import os
import json
import sys

project = os.getenv('GOOGLE_CLOUD_PROJECT')
creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

if not project or not creds_path:
    print("❌ Environment variables not set")
    sys.exit(1)

if not os.path.exists(creds_path):
    print(f"❌ Credentials file not found: {creds_path}")
    sys.exit(1)

try:
    with open(creds_path, 'r') as f:
        creds = json.load(f)
    
    if creds.get('project_id') != project:
        print(f"⚠️  Project ID mismatch: {project} vs {creds.get('project_id')}")
    
    print(f"✅ Credentials verified:")
    print(f"   Service Account: {creds.get('client_email')}")
    print(f"   Type: {creds.get('type')}")
    print(f"   Project: {creds.get('project_id')}")
    
except Exception as e:
    print(f"❌ Error reading credentials: {e}")
    sys.exit(1)
VERIFY_CREDS

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Credential verification failed"
    exit 1
fi

echo ""
echo "✅ Vertex AI Setup Complete!"
echo ""
echo "To make these settings permanent, add to your ~/.zshrc:"
echo ""
echo "  export GOOGLE_CLOUD_PROJECT=\"$PROJECT_ID\""
echo "  export GOOGLE_APPLICATION_CREDENTIALS=\"$(pwd)/credentials/commerce-agent-key.json\""
echo ""
echo "Then run: source ~/.zshrc"
echo ""
echo "Ready to start the agent:"
echo "  make dev"
echo ""
