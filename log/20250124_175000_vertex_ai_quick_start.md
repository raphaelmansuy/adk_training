# Quick Start: Vertex AI Setup for Commerce Agent

**Goal:** Get commerce_agent running with Vertex AI on adk web in < 10 minutes

---

## ✅ Quick Setup (5 Minutes)

### Step 1: Create Service Account Key

```bash
# If you already have a Google Cloud project and service account key:
# Skip to Step 2

# If not, use this quick setup:
export PROJECT_ID="my-commerce-project"

# Login to Google Cloud
gcloud auth login

# Create project
gcloud projects create $PROJECT_ID

# Set as default
gcloud config set project $PROJECT_ID

# Enable APIs
gcloud services enable aiplatform.googleapis.com

# Create service account
gcloud iam service-accounts create commerce-agent \
  --display-name="Commerce Agent"

# Get service account email
SA_EMAIL=$(gcloud iam service-accounts list --filter="displayName:Commerce Agent" --format="value(email)")

# Grant permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/aiplatform.user"

# Create and download key
mkdir -p ~/.gcp
gcloud iam service-accounts keys create ~/.gcp/commerce-agent.json \
  --iam-account=$SA_EMAIL

echo "✅ Service account key created at: ~/.gcp/commerce-agent.json"
echo "✅ Project ID: $PROJECT_ID"
```

---

### Step 2: Set Environment Variables

```bash
# Get your project ID
PROJECT_ID=$(gcloud config get-value project)
echo "Using project: $PROJECT_ID"

# Set environment variables for this session
export GOOGLE_CLOUD_PROJECT=$PROJECT_ID
export GOOGLE_APPLICATION_CREDENTIALS=$HOME/.gcp/commerce-agent.json

# Make permanent (add to ~/.zshrc)
cat >> ~/.zshrc << EOF

# Commerce Agent Vertex AI
export GOOGLE_CLOUD_PROJECT="$PROJECT_ID"
export GOOGLE_APPLICATION_CREDENTIALS="\$HOME/.gcp/commerce-agent.json"
EOF

# Reload shell
source ~/.zshrc

# Verify
echo "Project: $GOOGLE_CLOUD_PROJECT"
echo "Credentials: $GOOGLE_APPLICATION_CREDENTIALS"
ls $GOOGLE_APPLICATION_CREDENTIALS && echo "✅ File exists" || echo "❌ File not found"
```

---

### Step 3: Configure Commerce Agent

```bash
# Navigate to project
cd /Users/raphaelmansuy/Github/03-working/adk_training/tutorial_implementation/commerce_agent_e2e

# Copy .env.example to .env
cp .env.example .env

# Edit .env with your values
nano .env
```

**Update .env to:**

```dotenv
# Google Cloud Configuration (Vertex AI)
GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID
GOOGLE_APPLICATION_CREDENTIALS=$HOME/.gcp/commerce-agent.json

# Database Configuration
DATABASE_URL=sqlite:///./commerce_agent_sessions.db

# Agent Configuration
ADK_LOG_LEVEL=INFO
```

Replace `YOUR_PROJECT_ID` with your actual project ID from Step 2.

---

### Step 4: Install and Run

```bash
# Install dependencies
make setup

# Verify environment
make check-env

# Run tests (optional, but recommended)
make test

# Start ADK web
make dev
```

**Expected output:**
```
🤖 Starting Commerce Agent...

📱 Open http://localhost:8000 in your browser
🎯 Select 'commerce_agent' from the agent dropdown
```

---

## 🌐 Access the Agent

1. Open browser: `http://localhost:8000`
2. In the agent dropdown, select: `commerce_agent`
3. Try: `"I want running shoes and minimal shorts"`

---

## 🐛 Troubleshooting

### "No credentials found"

```bash
# Verify environment
echo $GOOGLE_CLOUD_PROJECT
echo $GOOGLE_APPLICATION_CREDENTIALS

# If empty:
export GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project)
export GOOGLE_APPLICATION_CREDENTIALS=$HOME/.gcp/commerce-agent.json
```

---

### "Permission denied"

```bash
# Grant admin permissions
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
  --member="serviceAccount:commerce-agent@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com" \
  --role="roles/aiplatform.admin"
```

---

### "API not enabled"

```bash
# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com

# Wait 30 seconds
sleep 30

# Try again
make dev
```

---

### "Agent not in dropdown"

```bash
# Reinstall package
cd tutorial_implementation/commerce_agent_e2e
pip install -e .

# Restart adk web (Ctrl+C and run again)
make dev
```

---

## 📚 Full Guide

For detailed setup instructions, see:
- `log/20250124_173000_vertex_ai_setup_guide.md`

---

## ✨ What's Working Now

✅ commerce_agent uses Vertex AI  
✅ Google Search tool works with site: operators  
✅ Multi-user session management  
✅ Database persistence  
✅ adk web UI working  

---

## 🎯 Next Steps

1. **Test the agent:** Try "Find running shoes under €100"
2. **Review improvements:** See `log/20250124_165000_commerce_agent_improvement_analysis.md`
3. **Implement fixes:** Product database, direct links, simplified preferences

---

**Setup Time:** ~5 minutes  
**Status:** ✅ Ready to Use  
**Contact:** See log files for troubleshooting details
