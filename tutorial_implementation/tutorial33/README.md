# Tutorial 33 Implementation: Slack Bot Integration with ADK

This is a working implementation of Tutorial 33 from the ADK Training project. It demonstrates building intelligent Slack bots with Google ADK for team support.

## Features

- ✅ **Knowledge Base Search**: Search company policies and procedures
- ✅ **Support Ticket Creation**: Create and track support tickets
- ✅ **ADK Agent**: Root agent with callable tools
- ✅ **Slack Bolt Integration**: Handle mentions, DMs, and slash commands (in bot.py)
- ✅ **Comprehensive Tests**: Unit, integration, and structure tests

## Quick Start

### 1. Setup Environment

```bash
make setup
```

This installs dependencies and sets up the package for ADK discoverability.

### 2. Configure Slack App

Create a `.env` file in the `support_bot/` directory:

```bash
cp support_bot/.env.example support_bot/.env
```

Add your credentials:
```bash
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_APP_TOKEN=xapp-your-token
GOOGLE_API_KEY=your-api-key
```

### 3. Test the Agent

```bash
make test
```

### 4. Run in Development

```bash
make dev
```

This starts the ADK web interface at http://localhost:8000

### 5. View Demo

```bash
make demo
```

## Project Structure

```
tutorial33/
├── support_bot/              # Agent module
│   ├── __init__.py          # Module entry point
│   ├── agent.py             # Root agent with tools
│   └── .env.example         # Environment template
├── tests/                    # Test suite
│   ├── test_agent.py        # Agent and tool tests
│   ├── test_imports.py      # Import tests
│   └── test_structure.py    # Structure tests
├── Makefile                 # Development commands
├── pyproject.toml          # Package configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Tools Implemented

### 1. search_knowledge_base(query: str)

Searches the company knowledge base for information.

**Returns:**
```python
{
    'status': 'success',
    'report': 'Found article: ...',
    'article': {
        'title': '...',
        'content': '...'
    }
}
```

**Example:**
```python
result = search_knowledge_base("password reset")
# Returns password reset procedure
```

### 2. create_support_ticket(subject, description, priority)

Creates a support ticket for complex issues.

**Returns:**
```python
{
    'status': 'success',
    'report': 'Support ticket created: TKT-ABC123...',
    'ticket': {
        'id': 'TKT-ABC123',
        'subject': '...',
        'priority': 'normal',
        'created_at': '2025-10-18T...'
    }
}
```

**Example:**
```python
result = create_support_ticket(
    subject="VPN Issue",
    description="Cannot connect to company VPN",
    priority="high"
)
```

## Test Coverage

The implementation includes comprehensive tests:

- **test_imports.py**: Tests agent and tools can be imported
- **test_structure.py**: Tests project structure and file layout
- **test_agent.py**: 40+ tests covering:
  - Agent configuration
  - Tool functionality
  - Knowledge base search
  - Ticket creation
  - Return format validation
  - Error handling

Run tests with:

```bash
make test              # Run all tests
make test-coverage    # Run with coverage report
```

## Deploy to Slack

### Getting Started

To deploy this agent to Slack, follow these 8 steps:

#### 1. Create Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click the green **"Create New App"** button
3. Select **"From scratch"**
4. Fill in the details:
   - **App Name**: `Support Bot`
   - **Workspace**: Select your workspace
5. Click **"Create App"**

#### 2. Configure Bot Scopes (OAuth Permissions)

This gives your bot permission to read messages, send replies, and access user info.

1. In the left sidebar, click **"OAuth & Permissions"**
2. Scroll to **"Bot Token Scopes"**
3. Click **"Add an OAuth Scope"** and add these scopes:
   - `app_mentions:read` (respond to @mentions)
   - `chat:write` (send messages)
   - `channels:history` (read channel messages)
   - `channels:read` (access public channels)
   - `groups:history` (read private messages)
   - `groups:read` (access private channels)
   - `im:history` (read direct messages)
   - `im:read` (access DMs)
   - `users:read` (look up user information)

#### 3. Get Your Bot Token

This is the token your bot will use to authenticate with Slack.

1. After adding scopes, scroll up to **"OAuth Tokens for Your Workspace"**
2. Click the green **"Install to Workspace"** button
3. Review permissions and click **"Allow"**
4. You'll see **"Bot User OAuth Token"** (starts with `xoxb-`)
5. Click **"Copy"** to copy it

**Your token should look like:**

```bash
xoxb-<workspace-id>-<bot-id>-<secret>
```

⚠️ **IMPORTANT**: Keep this token secret! Never share it or commit it to git.

#### 4. Enable Socket Mode

Socket Mode lets your bot receive real-time events without needing a public webhook.

1. In the left sidebar, click **"Socket Mode"**
2. Toggle the switch to **"Enable Socket Mode"**
3. Click **"Generate App-Level Token"**
4. Fill in:
   - **Token Name**: `socket_token`
   - **Scope**: Check `connections:write`
5. Click **"Generate"**
6. Copy the token (starts with `xapp-`)

**Your token should look like:**

```bash
xapp-1-<app-id>-<token-id>-<secret>
```

#### 5. Subscribe to Bot Events

1. In the left sidebar, click **"Event Subscriptions"**
2. Toggle **"Enable Events"** to ON
3. Scroll to **"Subscribe to bot events"**
4. Click **"Add Bot User Event"** and add these 4 events:
   - `app_mention` (bot is mentioned)
   - `message.channels` (message in public channels)
   - `message.groups` (message in private channels)
   - `message.im` (direct messages)
5. Click **"Save Changes"**

#### 6. Install App to Your Workspace

1. In the left sidebar, click **"Install App"**
2. Click **"Install to Workspace"**
3. Review the permissions
4. Click **"Allow"** to authorize

#### 7. Configure Your Environment File

Now add your tokens to the project:

```bash
cd /path/to/tutorial33
cp support_bot/.env.example support_bot/.env
```

Edit `support_bot/.env` and add your three tokens:

```bash
# From Step 3: Bot Token (starts with xoxb-)
SLACK_BOT_TOKEN=xoxb-<workspace-id>-<bot-id>-<secret>

# From Step 4: App Token (starts with xapp-)
SLACK_APP_TOKEN=xapp-1-<app-id>-<token-id>-<secret>

# From https://ai.google.dev (Google Gemini API key)
GOOGLE_API_KEY=AIzaSyD_your_actual_key_here
```

**File Structure After Setup:**

```
support_bot/
├── __init__.py
├── agent.py          (ADK agent with tools)
├── .env              (← Your tokens go here)
└── .env.example      (template, don't modify)
```

#### 8. Run Your Slack Bot

**For Development (Socket Mode):**

```bash
make slack-dev
```

This command will:

- Check that your tokens are configured
- Connect to Slack via Socket Mode
- Listen for mentions and messages
- Print any errors to the terminal

**For Production (Cloud Run):**

```bash
make slack-deploy
```

This command will:

- Build a Docker container
- Deploy to Google Cloud Run
- Convert Socket Mode to HTTP webhooks
- Run 24/7 without your computer

#### 9. Test Your Bot in Slack

1. Go to your Slack workspace
2. Find the **#general** channel (or any channel)
3. Type a message mentioning your bot:

```text
@Support Bot What is the password reset procedure?
```

**Try these test commands:**

```bash
@Support Bot help
@Support Bot What is the vacation policy?
@Support Bot Create a ticket for my laptop is slow
@Support Bot Show me the remote work policy
```

**Expected Results:**

```bash
User: @Support Bot What is the password reset procedure?

Support Bot:
Found article: Password Reset
Procedure:
1. Go to account.company.com
2. Click "Forgot Password"
3. Follow the email link
4. Create new password
```

### Integration Flow

```
User Message in Slack
        ↓
   Slack Bolt SDK
        ↓
   Parse Event & Context
        ↓
   ADK Agent (root_agent)
        ↓
  ┌─────────────────────┐
  │  Available Tools:   │
  │  • search_kb        │
  │  • create_ticket    │
  └─────────────────────┘
        ↓
   Format Response
        ↓
   Send to Slack Channel
```

### Available Commands

```bash
make slack-dev         # Run bot in Socket Mode (development)
make slack-deploy      # Deploy to Cloud Run (production)
make slack-test        # Test Slack integration
```

See the Makefile for full details.

### Production Deployment

Deploy to Google Cloud Run:

```bash
make slack-deploy
```

This will:

- Build Docker image
- Deploy to Cloud Run
- Configure HTTP webhook in Slack
- Set `PORT=8080` for Cloud Run

Detailed Production Deployment (Cloud Run)

Follow these steps to deploy the Slack bot to Google Cloud Run. This is written as an explicit, repeatable process you can run from your workstation.

1. Prerequisites

- Install and authenticate the Google Cloud CLI (gcloud):

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

- Enable required APIs:

```bash
gcloud services enable run.googleapis.com iam.googleapis.com artifactregistry.googleapis.com
```

- Install Docker and ensure you can build and push images.

2. Build the container image

Replace `[REGION]`, `[PROJECT]` and `[REPOSITORY]` with your values. Use Artifact Registry or Container Registry. Example using the default GCR naming:

```bash
IMAGE=gcr.io/[PROJECT]/support-bot:latest
docker build -t "$IMAGE" .
```

3. Push the image

```bash
docker push "$IMAGE"
```

If you use Artifact Registry with a custom repository, tag accordingly and push:

```bash
IMAGE=[REGION]-docker.pkg.dev/[PROJECT]/[REPOSITORY]/support-bot:latest
docker build -t "$IMAGE" .
docker push "$IMAGE"
```

4. Deploy to Cloud Run (managed)

This deploys the container as a service. Replace `[REGION]` as appropriate.

```bash
gcloud run deploy support-bot \
    --image "$IMAGE" \
    --region [REGION] \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars ENVIRONMENT=production,PORT=8080
```

Notes:
- For secrets (Slack tokens, API keys) prefer using Secret Manager and reference them with `--set-secrets` or set them in the Cloud Run service after deployment.
- Use `--no-allow-unauthenticated` if you want to restrict access behind IAP or a load balancer.

5. Configure Slack (HTTP webhook)

After deployment you'll get a service URL such as `https://support-bot-xxxxx-uc.a.run.app`.

1. In Slack App settings → Event Subscriptions or Interactivity, set the Request URL to:

```text
https://[CLOUD_RUN_URL]/slack/events
```

2. Verify Slack can reach the URL (Cloud Run must allow unauthenticated requests or you must configure verification via a signed header).

6. Use Secret Manager (recommended)

Store secrets securely and avoid injecting tokens directly into environment variables when possible. Example creating a secret (one-liner):

```bash
echo -n "$SLACK_BOT_TOKEN" | gcloud secrets create SLACK_BOT_TOKEN --data-file=-
```

Add a secret version if needed:

```bash
echo -n "$SLACK_BOT_TOKEN" | gcloud secrets versions add SLACK_BOT_TOKEN --data-file=-
```

Then bind the secret to the Cloud Run service via `--set-secrets` or configure it in the Cloud Console.

7. Healthchecks & logging

- Add a `/health` endpoint that returns 200 for readiness checks (Cloud Run health probes rely on traffic; having a simple endpoint is useful for load balancers).
- Use Cloud Logging and set structured logs for events and errors.

8. Rollback

- Use `gcloud run services update --image` to roll back to a previous tag or redeploy a prior image tag.

9. Optional: Domain mapping & HTTPS

- Map a custom domain via `gcloud beta run domain-mappings create --service support-bot --domain your.domain.com` and update Slack request URLs accordingly.

10. Example full flow (dry-run, manual confirmation recommended):

```bash
# build
docker build -t "$IMAGE" .
# push
docker push "$IMAGE"
# deploy
gcloud run deploy support-bot --image "$IMAGE" --region us-central1 --platform managed --allow-unauthenticated --set-env-vars ENVIRONMENT=production,PORT=8080
```

### Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| Bot not responding | Check Socket Mode enabled, verify tokens in `.env` |
| "Socket connection failed" | Ensure `SLACK_APP_TOKEN` starts with `xapp-` |
| Tools not executing | Verify `GOOGLE_API_KEY` is set, run `make test` |
| Module import errors | Run `pip install -e .` |

## Knowledge Base

The agent has access to these articles:

- 🔐 Password Reset
- 💰 Expense Reports
- 🏖️ Vacation & PTO Policy
- 🏠 Remote Work Policy
- 🛠️ IT Support Contacts

Try asking the agent about any of these topics!

## Learning Outcomes

After working with this implementation, you'll understand:

✅ How to build ADK agents with tools
✅ How to structure tools to return proper formats
✅ How to implement knowledge base search
✅ How to integrate with Slack using Slack Bolt
✅ How to test agents comprehensively
✅ How to deploy agents to Cloud Run

## Next Steps

1. **Extend the Knowledge Base**: Add more articles to KNOWLEDGE_BASE in `agent.py`
2. **Add More Tools**: Implement additional tools for ticket management, user lookup
3. **Slack Integration**: Add the bot.py file to handle Slack events
4. **Production Deployment**: Deploy to Cloud Run using HTTP mode
5. **Advanced Features**: Add rich Slack blocks, interactive buttons, scheduled messages

## Troubleshooting

### Issue: Imports fail

```bash
# Make sure package is installed in development mode
pip install -e .
```

### Issue: Tests fail

```bash
# Install test dependencies
pip install pytest pytest-cov
make test
```

### Issue: ADK web doesn't find agent

```bash
# Agent must be installed as package
pip install -e .
adk web  # Not 'adk web support_bot'
```

## Resources

- 📚 [ADK Documentation](https://google.github.io/adk-docs/)
- 💬 [Slack Bolt Documentation](https://docs.slack.dev/tools/bolt-python/)
- 🤖 [Gemini API](https://ai.google.dev/gemini-api/docs)
- 📖 [Tutorial 33 Full Guide](../../docs/tutorial/33_slack_adk_integration.md)

## Contributing

Found an issue? Please report it or submit a PR to the [ADK Training Repository](https://github.com/raphaelmansuy/adk_training).

---

**Last Updated**: October 18, 2025

**Tested With**:

- google-adk >= 1.16.0
- slack-bolt >= 1.26.0
- google-genai >= 1.45.0
- Python 3.9+
