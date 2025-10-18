# Production Deployment Guide: Support Bot to Google Cloud Run

This guide walks you through deploying the ADK Support Bot to Google Cloud Run for 24/7 availability.

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **gcloud CLI** installed and authenticated:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```
3. **Docker** installed locally
4. **Slack App** created and configured with Socket Mode (see Tutorial 33 README step 1-4)
5. **Secrets ready**:
   - `SLACK_BOT_TOKEN` (starts with `xoxb-`)
   - `SLACK_APP_TOKEN` (starts with `xapp-`)
   - `GOOGLE_API_KEY` (Gemini API key)

## Step 1: Enable Required Google Cloud APIs

```bash
gcloud services enable run.googleapis.com \
  iam.googleapis.com \
  artifactregistry.googleapis.com \
  cloudresourcemanager.googleapis.com
```

## Step 2: Create Secrets in Secret Manager

Store secrets securely instead of hardcoding them in environment variables.

```bash
# Create secrets (one-time setup)
echo -n "YOUR_SLACK_BOT_TOKEN" | \
  gcloud secrets create SLACK_BOT_TOKEN --data-file=-

echo -n "YOUR_SLACK_APP_TOKEN" | \
  gcloud secrets create SLACK_APP_TOKEN --data-file=-

echo -n "YOUR_GOOGLE_API_KEY" | \
  gcloud secrets create GOOGLE_API_KEY --data-file=-
```

To update a secret later:
```bash
echo -n "NEW_TOKEN" | \
  gcloud secrets versions add SLACK_BOT_TOKEN --data-file=-
```

## Step 3: Configure Secret Permissions

Grant Cloud Run service account access to secrets:

```bash
PROJECT_ID=$(gcloud config get-value project)
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
SERVICE_ACCOUNT="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

# Grant Secret Accessor role
for secret in SLACK_BOT_TOKEN SLACK_APP_TOKEN GOOGLE_API_KEY; do
  gcloud secrets add-iam-policy-binding $secret \
    --member=serviceAccount:${SERVICE_ACCOUNT} \
    --role=roles/secretmanager.secretAccessor
done
```

## Step 4: Build and Push Container Image

Set your project ID and region:

```bash
export PROJECT_ID=$(gcloud config get-value project)
export REGION=us-central1  # or your preferred region
export IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/support-bot/bot:latest"
```

Build the Docker image:

```bash
docker build -t ${IMAGE} .
```

Push to Artifact Registry:

```bash
# First, ensure you can push (configure Docker auth)
gcloud auth configure-docker ${REGION}-docker.pkg.dev

# Push the image
docker push ${IMAGE}
```

Alternatively, use **Container Registry (GCR)**:

```bash
export IMAGE="gcr.io/${PROJECT_ID}/support-bot:latest"
docker build -t ${IMAGE} .
docker push ${IMAGE}
```

## Step 5: Deploy to Cloud Run

Deploy the service with secret references:

```bash
gcloud run deploy support-bot \
  --image ${IMAGE} \
  --region ${REGION} \
  --platform managed \
  --allow-unauthenticated \
  --port 8080 \
  --set-secrets SLACK_BOT_TOKEN=SLACK_BOT_TOKEN:latest \
  --set-secrets SLACK_APP_TOKEN=SLACK_APP_TOKEN:latest \
  --set-secrets GOOGLE_API_KEY=GOOGLE_API_KEY:latest \
  --set-env-vars ENVIRONMENT=production,PORT=8080 \
  --memory 512Mi \
  --cpu 1 \
  --timeout 3600
```

Key options:
- `--allow-unauthenticated`: Slack must reach the service publicly. If you need authentication, use IAP instead.
- `--set-secrets`: Maps environment variable names to Secret Manager secrets.
- `--memory 512Mi --cpu 1`: Adjust based on your workload.
- `--timeout 3600`: Set timeout to 1 hour (max for Cloud Run).

## Step 6: Get the Service URL

After deployment, retrieve the Cloud Run service URL:

```bash
SERVICE_URL=$(gcloud run services describe support-bot \
  --region ${REGION} \
  --platform managed \
  --format='value(status.url)')

echo "Service URL: ${SERVICE_URL}"
```

## Step 7: Configure Slack Event Subscription

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Select your app
3. Click **Event Subscriptions**
4. Set **Request URL** to:
   ```
   ${SERVICE_URL}/slack/events
   ```
5. Click **Verify URL** (Slack will POST a verification request to your service)
6. Save changes

If verification fails:
- Ensure `--allow-unauthenticated` is set
- Check Cloud Run logs: `gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=support-bot" --limit 50`

## Step 8: Test the Bot

In your Slack workspace, mention the bot:

```
@Support Bot help
@Support Bot What is the password reset procedure?
@Support Bot Create a ticket for my laptop is slow
```

Expected behavior:
- Bot responds within 1-2 seconds (Cloud Run cold starts can be ~5 seconds)
- Responses appear in the channel or thread

## Monitoring & Logging

### View Cloud Run Logs

```bash
gcloud logging read \
  "resource.type=cloud_run_revision AND \
   resource.labels.service_name=support-bot" \
  --limit 50 --format json
```

### Set Up Alerts

Use Cloud Monitoring to alert on:
- High error rates
- Slow response times
- High memory usage

### Stream Logs in Real-Time

```bash
gcloud logging read \
  "resource.type=cloud_run_revision AND \
   resource.labels.service_name=support-bot" \
  --follow --format='table(timestamp,textPayload)'
```

## Updating the Bot

To redeploy a new version:

```bash
# Rebuild the image with a new tag
docker build -t ${IMAGE} .
docker push ${IMAGE}

# Redeploy
gcloud run deploy support-bot \
  --image ${IMAGE} \
  --region ${REGION} \
  --platform managed \
  [... same options as before ...]
```

Cloud Run automatically routes traffic to the new revision gradually (no downtime).

## Rollback

If something goes wrong, roll back to a previous revision:

```bash
gcloud run rollbacks run support-bot \
  --region ${REGION} \
  --platform managed
```

Or manually redeploy an older image tag.

## Cost Optimization

- **Free tier**: Up to 2M requests/month, 360,000 GB-seconds of compute per month
- **Usage pricing**: ~$0.40 per 1M requests + compute time
- **Tips**:
  - Use `--memory 256Mi` if your bot is lightweight
  - Set `--timeout 60` if most requests complete quickly
  - Use concurrency settings to tune request handling

## Troubleshooting

### Slack can't verify the URL

- Ensure `--allow-unauthenticated` is set in the deployment
- Check that the `/slack/events` endpoint is implemented in your bot
- View Cloud Run logs to see the verification request

### Bot doesn't respond

- Check secrets are correctly bound (verify environment variables in Cloud Run service details)
- Check agent imports: `python -m support_bot.agent` should work locally
- Review logs for errors

### Timeout errors

- Increase `--timeout` (e.g., to 300 for 5 minutes)
- Check if agent is making long-running external calls
- Profile the agent locally to optimize response time

### Out of memory

- Increase `--memory` (try 512Mi or 1Gi)
- Check if the agent is loading large knowledge bases

## Next Steps

1. **Add a Dockerfile** if not already present
2. **Set up CI/CD** (Cloud Build) to auto-deploy on git push
3. **Add monitoring dashboards** for request rates, latency, errors
4. **Schedule periodic restarts** for security (use Cloud Scheduler)
5. **Enable VPC connector** if you need to access private resources

## Further Reading

- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Secret Manager Guide](https://cloud.google.com/secret-manager/docs)
- [Slack Bolt Documentation](https://docs.slack.dev/tools/bolt-python/)
- [ADK Documentation](https://google.github.io/adk-docs/)

---

**Last Updated**: October 18, 2025  
**Status**: Ready for production deployment
