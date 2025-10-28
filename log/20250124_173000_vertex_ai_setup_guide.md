# Vertex AI Setup Guide for Commerce Agent with ADK Web

**Date:** 2025-01-24  
**Objective:** Configure commerce_agent to use Vertex AI instead of Gemini API  
**Status:** Step-by-step guide

---

## 🎯 Why Vertex AI?

**For the Commerce Agent, Vertex AI is better because:**

1. **Search Tool Works Better**
   - `site:decathlon.fr` operator works reliably on Vertex AI
   - Gemini API doesn't respect site: operators
   - This fixes the critical search issue identified in the analysis

2. **exclude_domains Parameter**
   - Vertex AI supports GoogleSearch with exclude_domains
   - Can explicitly exclude: amazon.com, ebay.com, etc.
   - Guarantees Decathlon-only results (Option 3)

3. **Enterprise Features**
   - Better rate limiting
   - Improved monitoring
   - Production-ready infrastructure
   - Multi-region support

4. **Performance**
   - Lower latency
   - Better caching
   - Optimized for production workloads

---

## 📋 Prerequisites

### Required:
- [ ] Google Cloud Project (free tier works)
- [ ] Vertex AI API enabled
- [ ] Service account with Vertex AI permissions
- [ ] Service account key JSON file

### Optional:
- [ ] gcloud CLI (for easier setup)

---

## ⚙️ Setup Steps

### Step 1: Create Google Cloud Project

```bash
# Option A: Using gcloud CLI
gcloud projects create commerce-agent-project
gcloud config set project commerce-agent-project

# Option B: Using Google Cloud Console
# Visit: https://console.cloud.google.com
# Click "Create Project"
# Name: "commerce-agent-project"
```

**Get your Project ID:**
```bash
gcloud config get-value project
# Output: commerce-agent-project
```

---

### Step 2: Enable Required APIs

```bash
# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com

# Enable Cloud Resource Manager API
gcloud services enable cloudresourcemanager.googleapis.com

# Enable IAM API
gcloud services enable iam.googleapis.com

# Verify they're enabled
gcloud services list --enabled | grep -E "aiplatform|cloudresourcemanager|iam"
```

---

### Step 3: Create Service Account

```bash
# Set your project
PROJECT_ID="commerce-agent-project"

# Create service account
gcloud iam service-accounts create commerce-agent-sa \
    --display-name="Commerce Agent Service Account" \
    --project=$PROJECT_ID

# Get the email
SA_EMAIL="commerce-agent-sa@${PROJECT_ID}.iam.gserviceaccount.com"
echo "Service Account: $SA_EMAIL"
```

---

### Step 4: Grant Required Permissions

```bash
# Set variables
PROJECT_ID="commerce-agent-project"
SA_EMAIL="commerce-agent-sa@${PROJECT_ID}.iam.gserviceaccount.com"

# Grant Vertex AI User role (needed for model access)
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/aiplatform.user"

# Grant Generative AI Admin role (recommended)
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/aiplatform.admin"

# Verify permissions
gcloud projects get-iam-policy $PROJECT_ID \
    --flatten="bindings[].members" \
    --filter="bindings.members:serviceAccount:$SA_EMAIL"
```

---

### Step 5: Create and Download Service Account Key

```bash
# Set variables
PROJECT_ID="commerce-agent-project"
SA_EMAIL="commerce-agent-sa@${PROJECT_ID}.iam.gserviceaccount.com"

# Create key
gcloud iam service-accounts keys create \
    ~/.gcp/commerce-agent-key.json \
    --iam-account=$SA_EMAIL

# Verify the file
ls -la ~/.gcp/commerce-agent-key.json

# Display the path (you'll need this)
echo "Service account key saved to: $HOME/.gcp/commerce-agent-key.json"
```

---

### Step 6: Configure Environment Variables

**Option A: Temporary (for current session)**

```bash
export GOOGLE_CLOUD_PROJECT="commerce-agent-project"
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.gcp/commerce-agent-key.json"

# Verify
echo "Project: $GOOGLE_CLOUD_PROJECT"
echo "Credentials: $GOOGLE_APPLICATION_CREDENTIALS"
ls $GOOGLE_APPLICATION_CREDENTIALS
```

**Option B: Permanent (add to ~/.zshrc or ~/.bashrc)**

```bash
# Add to ~/.zshrc
cat >> ~/.zshrc << 'EOF'

# Commerce Agent - Vertex AI Configuration
export GOOGLE_CLOUD_PROJECT="commerce-agent-project"
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.gcp/commerce-agent-key.json"
EOF

# Reload shell
source ~/.zshrc
```

---

### Step 7: Update .env File

**Navigate to commerce_agent_e2e:**

```bash
cd /Users/raphaelmansuy/Github/03-working/adk_training/tutorial_implementation/commerce_agent_e2e
```

**Copy .env.example to .env:**

```bash
cp .env.example .env
```

**Edit .env with your Vertex AI credentials:**

```bash
# Use your favorite editor
nano .env
```

**Update the content:**

```dotenv
# Google Cloud Configuration (Vertex AI)
GOOGLE_CLOUD_PROJECT=commerce-agent-project
GOOGLE_APPLICATION_CREDENTIALS=/Users/YOUR_USERNAME/.gcp/commerce-agent-key.json

# Database Configuration
DATABASE_URL=sqlite:///./commerce_agent_sessions.db

# Agent Configuration
ADK_LOG_LEVEL=INFO
```

**Replace `YOUR_USERNAME` with your actual username:**

```bash
# Get your username
whoami
# Output: raphaelmansuy

# So the path becomes:
# GOOGLE_APPLICATION_CREDENTIALS=/Users/raphaelmansuy/.gcp/commerce-agent-key.json
```

---

### Step 8: Update config.py for Vertex AI

**File:** `/commerce_agent/config.py`

**Add Vertex AI model name:**

```python
# Current (Gemini API)
MODEL_NAME = "gemini-2.5-flash"

# Change to (Vertex AI)
MODEL_NAME = "gemini-2.5-flash"  # Same model, but accessed via Vertex AI
```

**Note:** The model name stays the same. ADK automatically uses Vertex AI when `GOOGLE_APPLICATION_CREDENTIALS` is set.

---

### Step 9: Update agent.py for Vertex AI-Specific Features

**File:** `/commerce_agent/agent.py`

**Update to use exclude_domains parameter (if available in your ADK version):**

```python
from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.genai.types import GoogleSearch

# When creating the search tool with Vertex AI, optionally configure:
search_tool = google_search
# Note: exclude_domains only works with Vertex AI backend:
# google_search_config = GoogleSearch(exclude_domains=["amazon.com", "ebay.com"])
```

---

## ✅ Verification Steps

### Test 1: Verify Environment Variables

```bash
cd /Users/raphaelmansuy/Github/03-working/adk_training/tutorial_implementation/commerce_agent_e2e

# Check if environment is set
echo "Project: $GOOGLE_CLOUD_PROJECT"
echo "Credentials File: $GOOGLE_APPLICATION_CREDENTIALS"

# Check if file exists
test -f $GOOGLE_APPLICATION_CREDENTIALS && echo "✅ Credentials file exists" || echo "❌ Credentials file NOT found"
```

### Test 2: Verify GCP Access

```bash
# Authenticate with service account
gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS

# Set project
gcloud config set project $GOOGLE_CLOUD_PROJECT

# Test Vertex AI API access
gcloud ai models list --project=$GOOGLE_CLOUD_PROJECT
```

### Test 3: Test with Python

```bash
python3 << 'PYTHON_TEST'
import os
from google.auth import default
from google.auth.transport.requests import Request

# Check environment
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

print(f"Project ID: {project_id}")
print(f"Credentials Path: {creds_path}")

# Verify credentials file exists
if os.path.exists(creds_path):
    print("✅ Credentials file found")
else:
    print("❌ Credentials file NOT found")

# Try to authenticate
try:
    credentials, project = default()
    print(f"✅ Authentication successful with project: {project}")
except Exception as e:
    print(f"❌ Authentication failed: {e}")
PYTHON_TEST
```

---

## 🚀 Running with Vertex AI

### Setup

```bash
cd /Users/raphaelmansuy/Github/03-working/adk_training/tutorial_implementation/commerce_agent_e2e

# Install dependencies
make setup

# Run tests to verify everything works
make test
```

### Run ADK Web

```bash
# Start the development interface
make dev

# Expected output:
# 🤖 Starting Commerce Agent...
# 📱 Open http://localhost:8000 in your browser
# 🎯 Select 'commerce_agent' from the agent dropdown
```

### Access in Browser

```
URL: http://localhost:8000
Select Agent: "commerce_agent"
Test with: "I want running shoes and minimal shorts"
```

---

## 🔍 Troubleshooting

### Issue 1: "No credentials found"

**Error:**
```
google.auth.exceptions.DefaultCredentialsError: Could not automatically 
determine credentials
```

**Solution:**
```bash
# Verify environment variables
echo $GOOGLE_CLOUD_PROJECT
echo $GOOGLE_APPLICATION_CREDENTIALS

# If empty, export them
export GOOGLE_CLOUD_PROJECT="commerce-agent-project"
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.gcp/commerce-agent-key.json"

# Verify the file exists
ls -la $GOOGLE_APPLICATION_CREDENTIALS
```

---

### Issue 2: "Permission denied"

**Error:**
```
google.api_core.exceptions.PermissionDenied: 403 User does not have 
permission to access Vertex AI
```

**Solution:**
```bash
# Grant admin role to service account
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="serviceAccount:$SA_EMAIL" \
    --role="roles/aiplatform.admin"
```

---

### Issue 3: "API not enabled"

**Error:**
```
google.api_core.exceptions.NotFound: 403 The Project does not have 
aiplatform.googleapis.com enabled
```

**Solution:**
```bash
# Enable the API
gcloud services enable aiplatform.googleapis.com

# Wait a moment, then try again
sleep 30
```

---

### Issue 4: "adk web not recognizing agent"

**Error:**
```
Agent "commerce_agent" not found in dropdown
```

**Solution:**
```bash
# Make sure package is installed in editable mode
cd /Users/raphaelmansuy/Github/03-working/adk_training/tutorial_implementation/commerce_agent_e2e
pip install -e .

# If still not showing, restart adk web
# Kill the current process (Ctrl+C) and run again:
make dev
```

---

## 📊 Comparing Gemini API vs Vertex AI

| Feature | Gemini API | Vertex AI |
|---------|-----------|----------|
| **Authentication** | API Key | Service Account |
| **Model Access** | Limited | Full suite |
| **Search Tool** | `site:` operator doesn't work | Works reliably |
| **exclude_domains** | Not available | Available |
| **Rate Limiting** | Standard | Enterprise |
| **Monitoring** | Limited | Full dashboards |
| **Cost** | Free tier available | Pay-as-you-go |
| **Production Ready** | ⚠️ Limited | ✅ Recommended |

---

## 🎯 Next Steps After Setup

### 1. Verify Search Works Better

```bash
# Run the agent and test:
# "Find running shoes"
# Should now return Decathlon-only results with site: operator working
```

### 2. Test New Features

```python
# Can now use exclude_domains in search (if supported):
search_tool = GoogleSearch(exclude_domains=["amazon.com", "ebay.com"])
```

### 3. Monitor Performance

```bash
# View Vertex AI API usage
gcloud ai-platform endpoints list --region=us-central1

# View API quotas and usage
# https://console.cloud.google.com/apis/dashboard
```

---

## 📚 Additional Resources

- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Google AI SDK for Python](https://github.com/googleapis/google-ai-python-sdk)
- [Service Account Setup Guide](https://cloud.google.com/docs/authentication/getting-started)
- [ADK Documentation](https://google.github.io/adk-docs/)

---

## 💾 Quick Reference

**Environment Variables:**
```bash
export GOOGLE_CLOUD_PROJECT="commerce-agent-project"
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.gcp/commerce-agent-key.json"
```

**Start Development:**
```bash
cd tutorial_implementation/commerce_agent_e2e
make setup
make dev
```

**Check Status:**
```bash
echo "Project: $GOOGLE_CLOUD_PROJECT"
ls $GOOGLE_APPLICATION_CREDENTIALS
gcloud auth application-default print-access-token
```

---

**Setup Date:** 2025-01-24  
**Status:** Ready for Implementation  
**Expected Outcome:** Search tool works correctly, exclude_domains available, production-ready configuration
