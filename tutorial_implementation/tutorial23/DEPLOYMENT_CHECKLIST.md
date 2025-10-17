# Deployment Checklist: Step-by-Step Verification

**Use this checklist to verify your ADK deployment is production-ready.**

---

## Pre-Deployment (Before You Deploy)

### Security & Configuration
- [ ] API keys stored in Secret Manager (not .env or code)
- [ ] No hardcoded credentials anywhere
- [ ] Environment variables configured correctly
- [ ] CORS origins set to specific domains (never `*`)
- [ ] Authentication enabled (if needed)
- [ ] Request timeouts configured (30s recommended)
- [ ] Max token limits set
- [ ] Resource limits defined (memory, CPU)

### Code Quality
- [ ] Code reviewed and tested locally
- [ ] All tests passing: `pytest tests/ -v`
- [ ] No security warnings
- [ ] Dependencies up to date
- [ ] Error handling implemented

### Documentation
- [ ] Deployment instructions documented
- [ ] API endpoints documented
- [ ] Configuration options documented
- [ ] Runbooks prepared

---

## Deployment (Cloud Run Example)

### Step 1: Build & Push Image

```bash
# Build
gcloud builds submit --tag gcr.io/YOUR_PROJECT/agent

# Verify image
gcloud container images describe gcr.io/YOUR_PROJECT/agent
```

- [ ] Build completed successfully
- [ ] Image scanned for vulnerabilities (check Cloud Console)
- [ ] Image signing enabled (if using Binary Authorization)

### Step 2: Deploy

```bash
gcloud run deploy agent \
  --image gcr.io/YOUR_PROJECT/agent \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --max-instances 100 \
  --set-env-vars GOOGLE_CLOUD_PROJECT=YOUR_PROJECT
```

- [ ] Deployment completed
- [ ] Service is ready (check console)
- [ ] No deployment errors

### Step 3: Configure Permissions

```bash
# Set service account
gcloud run services update agent \
  --service-account agent-sa@YOUR_PROJECT.iam.gserviceaccount.com \
  --region us-central1

# Set authentication requirement
gcloud run services update agent \
  --no-allow-unauthenticated \
  --region us-central1
```

- [ ] Service account assigned
- [ ] Proper IAM permissions set
- [ ] Authentication required (if needed)

---

## Post-Deployment: Verification (Essential)

### Health Check

```bash
# Get service URL
SERVICE_URL=$(gcloud run services describe agent \
  --region us-central1 \
  --format 'value(status.url)')

# Test health endpoint
curl $SERVICE_URL/health
```

- [ ] Health endpoint responds (200 OK)
- [ ] Response includes status, uptime, request count
- [ ] No error responses

### Agent Invocation

```bash
# Test agent invocation
curl -X POST $SERVICE_URL/invoke \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello agent!", "temperature": 0.5}'
```

- [ ] Invocation successful (200 OK)
- [ ] Response includes agent response
- [ ] Response time < 5 seconds
- [ ] No errors in logs

### Security Verification

```bash
# 1. Check HTTPS
curl -I $SERVICE_URL/health | grep -i "https"

# 2. Test authentication
curl $SERVICE_URL/health  # Should fail with 401 or redirect

# 3. Check CORS headers
curl -H "Origin: https://yourdomain.com" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS $SERVICE_URL/invoke
```

- [ ] HTTPS enforced (no HTTP)
- [ ] Authentication required (if configured)
- [ ] CORS headers present and correct
- [ ] No wildcard (`*`) in CORS origins
- [ ] Security headers present

### Monitoring & Logging

```bash
# View recent logs
gcloud logging read "resource.service.name=agent" \
  --limit 10 \
  --format json | jq .

# View Cloud Monitoring dashboard
# https://console.cloud.google.com/monitoring/dashboards
```

- [ ] Logs appearing in Cloud Logging
- [ ] No error messages in logs
- [ ] Request/response patterns normal
- [ ] Error rate < 1%
- [ ] Latency < 2 seconds (p99)

### Cost Verification

```bash
# Estimate cost
echo "Monthly estimate for 1M requests:"
echo "Cloud Run: ~\$40 (+ storage)"
echo "Agent Engine: ~\$50 (+ storage)"
```

- [ ] Cost estimate reviewed
- [ ] Within budget
- [ ] Scaling limits set appropriately
- [ ] Auto-scaling working

---

## Post-Deployment: Configuration (One-Time)

### Monitoring Setup

```bash
# Create alert for error rate
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="Agent Error Rate Alert" \
  --condition-display-name="Error rate > 5%" \
  --condition-threshold-value=0.05
```

- [ ] Cloud Monitoring configured
- [ ] Alerting set up (email/PagerDuty)
- [ ] Dashboards created
- [ ] Log retention set

### Logging Setup

```bash
# Export logs to BigQuery (optional, for analysis)
gcloud logging sinks create agent-bigquery \
  bigquery.googleapis.com/projects/YOUR_PROJECT/datasets/agent_logs \
  --log-filter='resource.type="cloud_run_revision"'
```

- [ ] Log export configured
- [ ] Log retention policy set
- [ ] Log filtering working

### Scaling Configuration

```bash
# Review scaling settings
gcloud run services describe agent --region us-central1
```

- [ ] Min instances set (if needed)
- [ ] Max instances set appropriately
- [ ] CPU allocation correct
- [ ] Memory allocation correct
- [ ] Concurrency set

---

## Ongoing: Daily Verification

### Daily Checks (5 minutes)

```bash
# Check service health
curl $SERVICE_URL/health | jq '.error_rate'

# Check recent errors
gcloud logging read "resource.service.name=agent AND severity=ERROR" \
  --limit 10 \
  --recent-first
```

- [ ] No critical errors
- [ ] Error rate normal
- [ ] Response times normal
- [ ] No unusual patterns

### Weekly Checks (15 minutes)

- [ ] Review logs for warnings
- [ ] Check alert history (any triggered?)
- [ ] Verify cost within budget
- [ ] Review metrics for anomalies

### Monthly Checks (1 hour)

- [ ] Review performance metrics
- [ ] Update monitoring dashboards
- [ ] Review security logs (audit trail)
- [ ] Test disaster recovery procedure
- [ ] Update runbooks if needed

---

## Common Issues & Fixes

### "Service returns 401 Unauthorized"

**Causes**:
- Authentication required but not provided
- Token expired or invalid
- Service account permissions missing

**Fix**:
```bash
# Check if authentication is required
gcloud run services describe agent --format='value(spec.template.spec.serviceAccountName)'

# For testing, temporarily allow unauthenticated:
gcloud run services update agent --allow-unauthenticated
```

### "High Latency (> 5 seconds)"

**Causes**:
- Insufficient CPU
- Too many requests (throttled)
- Agent query too complex

**Fix**:
```bash
# Increase CPU
gcloud run services update agent --cpu 4

# Check if model load is slow
# Try gemini-2.0-flash instead of larger models
```

### "Out of Memory"

**Causes**:
- Memory limit too low
- Large requests
- Memory leak in code

**Fix**:
```bash
# Increase memory
gcloud run services update agent --memory 4Gi

# Check logs for memory issues
gcloud logging read "resource.service.name=agent AND memory" --limit 5
```

### "CORS Errors"

**Causes**:
- CORS origin not configured
- Frontend origin not in allow-list

**Fix**:
```bash
# Update CORS origins in code
# Then redeploy with new configuration

# Verify CORS headers
curl -H "Origin: https://yourdomain.com" \
     -X OPTIONS $SERVICE_URL/invoke -v
```

---

## Rollback Procedure

If something goes wrong:

```bash
# Get previous revision
PREVIOUS=$(gcloud run revisions list \
  --service=agent \
  --region=us-central1 \
  --sort-by=^ACTIVE \
  --limit=2 \
  --format='value(name)' | tail -1)

# Rollback to previous version
gcloud run services update-traffic agent \
  --to-revisions=$PREVIOUS=100 \
  --region=us-central1
```

- [ ] Rollback completed
- [ ] Service responding
- [ ] Error rate returned to normal

---

## Migration Checklist (If Moving to Different Platform)

### Cloud Run → Agent Engine

```bash
# 1. Deploy to Agent Engine
adk deploy agent_engine \
  --project YOUR_PROJECT \
  --region us-central1

# 2. Test Agent Engine deployment
curl https://AGENT_ID-REGION.endpoints.PROJECT_ID.cloud.goog/health

# 3. Update API client endpoints
# Update application to use new Agent Engine endpoint

# 4. Monitor for issues
# Let traffic run 10% for 30 minutes

# 5. Route 100% traffic to Agent Engine
# Decommission Cloud Run

# 6. Delete Cloud Run service
gcloud run services delete agent --region us-central1
```

- [ ] New platform deployed and verified
- [ ] Gradual traffic migration complete
- [ ] No errors in new environment
- [ ] Old platform decommissioned

---

## Final Sign-Off

- [ ] All security checks passed
- [ ] Health and performance verified
- [ ] Monitoring and alerting configured
- [ ] Runbooks documented
- [ ] Team trained on deployment
- [ ] Backup/recovery procedures tested
- [ ] Cost estimates validated
- [ ] **DEPLOYMENT READY FOR PRODUCTION** ✅
