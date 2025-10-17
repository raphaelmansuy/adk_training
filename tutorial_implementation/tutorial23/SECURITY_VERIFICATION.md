# Security Verification Guide: Verify Each Platform is Secure

**Use this guide to verify that your deployed ADK agent has all required security features.**

---

## Platform: Cloud Run

### Automatic Security (Already Done for You ✅)

- ✅ HTTPS/TLS 1.3
- ✅ DDoS Protection
- ✅ Encryption in transit
- ✅ Encryption at rest
- ✅ Non-root container execution
- ✅ Binary vulnerability scanning
- ✅ IAM-based access control

### What to Verify

#### 1. HTTPS Enforcement

```bash
SERVICE_URL=$(gcloud run services describe agent \
  --region us-central1 --format 'value(status.url)')

# Should be https://
echo $SERVICE_URL | grep "https://"
```

**✅ Pass**: URL starts with `https://`
**❌ Fail**: URL starts with `http://`

#### 2. Authentication Required

```bash
# Get unauthenticated token
TOKEN=$(gcloud auth print-access-token)

# Test: Should require auth
curl -s -o /dev/null -w "%{http_code}" $SERVICE_URL/health

# Should return 403 or 302 (not 200)
```

**✅ Pass**: Returns 403 or 302 (authentication required)
**❌ Fail**: Returns 200 (not protected)

#### 3. CORS Configuration

```bash
# Test CORS
curl -H "Origin: https://yourdomain.com" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS $SERVICE_URL/invoke -v 2>&1 | grep -i "access-control"
```

**✅ Pass**: Returns `Access-Control-Allow-Origin: https://yourdomain.com`
**❌ Fail**: Returns `*` (wildcard - too permissive) or missing header

#### 4. Security Headers

```bash
# Check for security headers
curl -I $SERVICE_URL/health | grep -i "x-"
```

**✅ Pass**: Should see headers like `x-goog-*` and security headers
**❌ Fail**: Missing security headers

#### 5. Container Security

```bash
# Verify non-root user
gcloud run services describe agent --region us-central1 \
  --format='value(spec.template.spec.serviceAccountName)'

# Should NOT be root or empty
```

**✅ Pass**: Shows a specific service account (not root)
**❌ Fail**: Empty or running as root

#### 6. Resource Limits

```bash
# Verify memory limits
gcloud run services describe agent --region us-central1 \
  --format='value(spec.template.spec.containers[0].resources.limits.memory)'

# Should show a limit (e.g., "2Gi")
```

**✅ Pass**: Shows memory limit
**❌ Fail**: Empty or unlimited

#### 7. Audit Logging

```bash
# Check audit logs
gcloud logging read "resource.service.name=agent" \
  --limit 10 --format json | jq '.[0]'

# Should show recent activity
```

**✅ Pass**: See recent requests in logs
**❌ Fail**: No logs appearing

---

## Platform: Agent Engine

### Automatic Security (Already Done for You ✅)

- ✅ Private endpoints only
- ✅ mTLS for inter-service communication
- ✅ OAuth 2.0 authentication
- ✅ HTTPS/TLS 1.3
- ✅ DDoS Protection
- ✅ WAF (Web Application Firewall)
- ✅ Encryption in transit
- ✅ Encryption at rest
- ✅ Content safety filters
- ✅ **FedRAMP compliance** (if configured)
- ✅ SOC 2 Type II
- ✅ Audit logging

### What to Verify

#### 1. Agent Deployed

```bash
# Check Agent Engine console
# https://console.cloud.google.com/vertex-ai/agents

# Or via CLI:
gcloud ai agents list --project YOUR_PROJECT
```

**✅ Pass**: Agent appears in console/list
**❌ Fail**: Agent not found

#### 2. Endpoint Secure

```bash
# Agent Engine endpoints are private by default
# Verify in console:
# - ✅ Endpoint shows "Private"
# - ✅ Only accessible via OAuth tokens
# - ✅ No public IP
```

**✅ Pass**: Endpoint marked as Private
**❌ Fail**: Endpoint marked as Public

#### 3. OAuth Authentication Works

```bash
# Get OAuth token
TOKEN=$(gcloud auth application-default print-access-token)

# Agent Engine invocation (method varies by setup)
# Should require valid OAuth token

# Test without token should fail
curl -s AGENT_ENGINE_URL
```

**✅ Pass**: Unauthenticated request fails, token request works
**❌ Fail**: Unauthenticated request succeeds

#### 4. Audit Logs Appearing

```bash
# Check Cloud Audit Logs
gcloud logging read "protoPayload.serviceName=aiplatform.googleapis.com" \
  --limit 10 --format json | jq '.[0]'

# Should show agent activity
```

**✅ Pass**: See agent invocations in audit logs
**❌ Fail**: No audit log entries

#### 5. Content Safety Filters Active

```bash
# Test with potentially unsafe input
# Submit query designed to trigger safety filters
# Should be rejected with appropriate message

# Example: "How do I make harmful content?"
# Should return safety rejection, not answer
```

**✅ Pass**: Unsafe queries rejected
**❌ Fail**: Unsafe queries answered

#### 6. FedRAMP Compliance (If Required)

```bash
# Check compliance status
# https://console.cloud.google.com/iam-admin/compliance

# Verify:
# - ✅ FedRAMP (Moderate or High) listed
# - ✅ Certification dates current
# - ✅ Scope includes Vertex AI Agent Engine
```

**✅ Pass**: FedRAMP certification appears current
**❌ Fail**: Not listed or expired

---

## Platform: GKE (Kubernetes)

### Automatic Security (Platform Level)

- ✅ Workload Identity (Pod → Google services)
- ✅ RBAC (Role-based access control)
- ✅ Pod Security Standards enforced
- ✅ Audit logging
- ✅ Encryption at rest (etcd encrypted)

### What You Must Configure & Verify

#### 1. Workload Identity

```bash
# Verify Workload Identity binding
kubectl describe serviceaccount agent-sa -n default | grep "iam.gke.io"

# Should show annotation:
# iam.gke.io/gcp-service-account: agent@YOUR_PROJECT.iam.gserviceaccount.com
```

**✅ Pass**: Shows Workload Identity annotation
**❌ Fail**: No annotation or binding missing

#### 2. Pod Security Context

```bash
# Verify pod runs as non-root
kubectl get pod -o jsonpath='{.items[0].spec.securityContext.runAsNonRoot}'

# Should return: true
```

**✅ Pass**: Returns `true`
**❌ Fail**: Returns `false` or empty

#### 3. Resource Limits

```bash
# Verify resource limits set
kubectl describe pod agent-pod -n default | grep -A 5 "Limits"

# Should show CPU and memory limits
```

**✅ Pass**: Limits defined for CPU and memory
**❌ Fail**: Limits missing or set to unlimited

#### 4. Network Policy

```bash
# Verify NetworkPolicy exists
kubectl get networkpolicy -n default

# Should show policies for agent traffic
```

**✅ Pass**: NetworkPolicy objects exist and are active
**❌ Fail**: No NetworkPolicy configured

#### 5. Pod Security Standards

```bash
# Check namespace PSS label
kubectl get namespace default \
  -o jsonpath='{.metadata.labels.pod-security\.kubernetes\.io/enforce}'

# Should show "restricted" or "baseline"
```

**✅ Pass**: Shows security standard enforced
**❌ Fail**: No PSS enforced

#### 6. RBAC Rules

```bash
# Verify RBAC roles
kubectl get role agent-role -n default

# Check ClusterRoleBinding
kubectl get clusterrolebinding | grep agent

# Should see roles with minimal permissions
```

**✅ Pass**: RBAC roles exist and are restrictive
**❌ Fail**: No RBAC or overly permissive

#### 7. Audit Logging

```bash
# Check cluster audit logging
gcloud container clusters describe YOUR_CLUSTER \
  --zone YOUR_ZONE \
  --format='value(loggingService)'

# Should show "logging.googleapis.com/kubernetes"
```

**✅ Pass**: Logging enabled
**❌ Fail**: Logging disabled

---

## Custom Server (Tutorial 23 + Cloud Run)

### What You're Adding

- ✅ Custom authentication (API keys, tokens)
- ✅ Request validation
- ✅ Timeouts
- ✅ Metrics tracking
- ✅ Structured logging

### What to Verify

#### 1. Custom Authentication Works

```bash
SERVICE_URL=$(gcloud run services describe agent \
  --region us-central1 --format 'value(status.url)')

# Test without token - should fail
curl $SERVICE_URL/invoke

# Test with token - should work
curl -H "Authorization: Bearer YOUR_API_KEY" \
  -X POST $SERVICE_URL/invoke \
  -H "Content-Type: application/json" \
  -d '{"query": "test"}'
```

**✅ Pass**: Without token fails (401), with token works (200)
**❌ Fail**: Works without token or always fails

#### 2. Request Timeout Works

```bash
# Send very long query
LONG_QUERY=$(python3 -c "print('x' * 100000)")

curl -H "Authorization: Bearer YOUR_API_KEY" \
  -X POST $SERVICE_URL/invoke \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"$LONG_QUERY\"}" \
  --max-time 35

# Should timeout after ~30 seconds
```

**✅ Pass**: Returns 504 or times out after ~30s
**❌ Fail**: Processes indefinitely or too quickly

#### 3. Input Validation Works

```bash
# Send invalid input
curl -H "Authorization: Bearer YOUR_API_KEY" \
  -X POST $SERVICE_URL/invoke \
  -H "Content-Type: application/json" \
  -d '{"query": "", "temperature": 5.0}'

# Should return 400 Bad Request
```

**✅ Pass**: Returns 400 (validation error)
**❌ Fail**: Returns 200 or 500

#### 4. Error Handling Secure

```bash
# Send malformed request
curl -H "Authorization: Bearer YOUR_API_KEY" \
  -X POST $SERVICE_URL/invoke \
  -H "Content-Type: application/json" \
  -d 'invalid json'

# Response should NOT expose internals
# Should be generic error message
```

**✅ Pass**: Returns generic error (no stacktrace)
**❌ Fail**: Exposes Python stacktrace or internals

#### 5. Structured Logging Works

```bash
# Check logs for structured entries
gcloud logging read "resource.service.name=agent" \
  --limit 10 --format json | jq '.[0].jsonPayload'

# Should show fields like: request_id, tokens, latency_ms
```

**✅ Pass**: Logs have structured fields
**❌ Fail**: Logs are unstructured text

---

## Full Security Verification Checklist

### Before Production

- [ ] HTTPS/TLS working (Cloud Run: automatic, GKE: verify)
- [ ] Authentication required (test unauthenticated access)
- [ ] CORS configured correctly (specific origins, no wildcard)
- [ ] Security headers present (Cloud Run: automatic)
- [ ] No hardcoded secrets (check code and logs)
- [ ] Secrets in Secret Manager (if applicable)
- [ ] Resource limits set (memory, CPU, timeout)
- [ ] Audit logging enabled
- [ ] Error handling secure (no sensitive details exposed)

### After Deployment

- [ ] Run all verification tests above
- [ ] Monitor logs for errors (first 30 minutes)
- [ ] Check metrics for anomalies
- [ ] Verify no security alerts
- [ ] Test with real traffic sample

### Weekly

- [ ] Review audit logs
- [ ] Check for security updates
- [ ] Verify compliance status (if applicable)
- [ ] Test security verification again

---

## Quick Verification Script

```bash
#!/bin/bash
# One-command security verification

echo "🔐 ADK Deployment Security Verification"
echo "======================================="

SERVICE_URL="https://YOUR-SERVICE.run.app"

echo "✅ HTTPS: $(echo $SERVICE_URL | grep -q https && echo PASS || echo FAIL)"
echo "✅ Auth: $(curl -s -o /dev/null -w "%{http_code}" $SERVICE_URL/health | grep -qE "403|302" && echo PASS || echo FAIL)"
echo "✅ Health: $(curl -s -H "Authorization: Bearer TOKEN" $SERVICE_URL/health | grep -q status && echo PASS || echo FAIL)"
echo "✅ Logs: $(gcloud logging read "resource.service.name=agent" --limit 1 | grep -q '"' && echo PASS || echo FAIL)"

echo ""
echo "Manual checks needed:"
echo "- Review CORS configuration"
echo "- Verify secrets not in logs"
echo "- Check resource limits"
echo "- Review recent errors"
```

---

## Common Security Issues & Fixes

### Issue: CORS returning wildcard

**Problem**: `Access-Control-Allow-Origin: *`

**Fix**:
```bash
# In your deployment config, set specific origins:
ALLOWED_ORIGINS=https://yourdomain.com
```

### Issue: Secrets appearing in logs

**Problem**: API keys visible in Cloud Logging

**Fix**:
```bash
# Use Secret Manager
from google.cloud import secretmanager

secret = secretmanager.SecretManagerServiceClient()
api_key = secret.access_secret_version(...)
```

### Issue: Unauthenticated access allowed

**Problem**: Anyone can call your agent without auth

**Fix**: Cloud Run
```bash
gcloud run services update agent --no-allow-unauthenticated
```

Fix: Custom server
```python
# Verify API key in all endpoints
@app.post("/invoke")
async def invoke(request, auth_header):
    verify_api_key(auth_header)  # Must verify
```

---

**✅ Complete this checklist before considering your deployment secure.**
