# Migration Guide: Move Your Agent Between Deployment Platforms

**Move your ADK agent from one platform to another with zero downtime.**

---

## Overview

Each platform has strengths. You may want to migrate:

- **Local → Cloud Run**: Started locally, moving to production
- **Cloud Run → Agent Engine**: Need FedRAMP compliance or managed infrastructure
- **Cloud Run → GKE**: Need advanced orchestration or on-premises option
- **GKE → Cloud Run**: Simplifying from Kubernetes back to serverless

This guide covers each migration path.

---

## Architecture: What Stays the Same

Your ADK agent core stays **100% unchanged**:

```
┌──────────────────────────────────┐
│  Your ADK Agent Code             │  ← Same everywhere
│  (agent.py, tools, logic)        │
└──────────────────────────────────┘
         ↑ Unchanged ↑
    ┌────┴────┬────────┬────────┐
    ↓         ↓        ↓        ↓
  Local     Cloud     Agent    GKE
   Dev      Run       Engine
```

Only the **deployment layer** changes.

---

## Migration Path 1: Local → Cloud Run

**Time**: 15 minutes  
**Complexity**: Easy  
**Downtime**: None (launch parallel)

### Step 1: Prepare for Cloud Run

#### 1.1 Create Dockerfile (if not existing)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY agent/ ./agent/
COPY server.py .

ENV PORT=8080
EXPOSE 8080

CMD ["python", "server.py"]
```

#### 1.2 Update requirements.txt

```bash
pip freeze > requirements.txt
```

Verify:
- google-genai >= 1.15.0
- fastapi
- uvicorn[standard]

### Step 2: Deploy to Cloud Run

```bash
# 1. Build image
gcloud builds submit --tag gcr.io/YOUR_PROJECT/agent \
  --region=us-central1

# 2. Deploy
gcloud run deploy agent \
  --image gcr.io/YOUR_PROJECT/agent \
  --region us-central1 \
  --memory 2Gi \
  --timeout 3600 \
  --max-instances 100 \
  --allow-unauthenticated

# 3. Get URL
SERVICE_URL=$(gcloud run services describe agent \
  --region us-central1 --format 'value(status.url)')
echo $SERVICE_URL
```

### Step 3: Test Cloud Run

```bash
# Test health
curl $SERVICE_URL/health

# Test invocation
curl -X POST $SERVICE_URL/invoke \
  -H "Content-Type: application/json" \
  -d '{"query": "hello"}'
```

### Step 4: Update DNS (if applicable)

```bash
# Update your domain to point to Cloud Run URL
# Option A: CNAME to *.run.app
# Option B: Use Cloud DNS

gcloud dns record-sets create agent.yourdomain.com \
  --ttl 300 \
  --type CNAME \
  --rrdatas your-service.run.app
```

### Step 5: Decommission Local

```bash
# Once Cloud Run is verified:
# - Stop local deployment
# - Delete local server processes
# - Archive local Dockerfile
```

---

## Migration Path 2: Cloud Run → Agent Engine

**Time**: 30 minutes  
**Complexity**: Medium  
**Downtime**: None (parallel launch possible)

### Step 1: Package as Agent

#### 1.1 Create Agent Descriptor

Agent Engine requires specific structure. Create `agent_config.yaml`:

```yaml
spec:
  display_name: "Your Agent Name"
  agent:
    model: "projects/YOUR_PROJECT/locations/us-central1/models/gemini-2.5-flash"
    tools:
      - name: "tool_name"
        description: "Tool description"
        input_schema:
          type: "object"
          properties:
            param: 
              type: "string"
      - name: "another_tool"
        # ... more tools
```

#### 1.2 Export Agent Definition

From your existing Cloud Run agent:

```bash
# Get current agent configuration
gcloud ai agents describe YOUR_AGENT \
  --format yaml > agent_config.yaml
```

### Step 2: Deploy to Agent Engine

```bash
# Create agent
gcloud ai agents create YOUR_AGENT \
  --config agent_config.yaml \
  --region us-central1 \
  --display-name "Your Agent"

# Note: Agent Engine deployment is different from Cloud Run
# Tools are registered with Agent Engine directly
```

### Step 3: Migrate Tools

Agent Engine registers tools differently:

```bash
# Register each tool
gcloud ai agents register-tool YOUR_AGENT \
  --tool-definition tool_config.json \
  --region us-central1
```

Tool config format:
```json
{
  "name": "tool_name",
  "description": "What tool does",
  "input_schema": {
    "type": "object",
    "properties": {
      "param": {"type": "string"}
    }
  },
  "function_declaration": {
    "name": "tool_name"
  }
}
```

### Step 4: Test Agent Engine

```bash
# Create test conversation
gcloud ai agents conversations create \
  --agent YOUR_AGENT \
  --region us-central1

# Send message
gcloud ai agents conversations send-message \
  --conversation YOUR_CONVERSATION \
  --message "hello" \
  --region us-central1
```

### Step 5: Setup OAuth (Agent Engine only)

```bash
# Agent Engine requires OAuth 2.0
gcloud oauth2l fetch --credentials=YOUR_CREDENTIALS \
  cloud-platform
```

### Step 6: Decommission Cloud Run (optional)

Once Agent Engine is working:

```bash
# Option A: Keep Cloud Run for backwards compatibility
# Option B: Delete Cloud Run service
gcloud run services delete agent --region us-central1
```

---

## Migration Path 3: Cloud Run → GKE

**Time**: 60 minutes  
**Complexity**: Complex  
**Downtime**: Can achieve zero-downtime with blue-green

### Step 1: Prepare GKE Cluster

#### 1.1 Create Cluster

```bash
gcloud container clusters create agent-cluster \
  --zone us-central1-a \
  --num-nodes 2 \
  --machine-type n1-standard-2 \
  --enable-ip-alias \
  --enable-stackdriver-kubernetes \
  --addons HorizontalPodAutoscaling,HttpLoadBalancing
```

#### 1.2 Create Workload Identity

```bash
# Create service account
gcloud iam service-accounts create agent-workload \
  --display-name="Agent Workload"

# Bind to Kubernetes service account
gcloud iam service-accounts add-iam-policy-binding \
  agent-workload@YOUR_PROJECT.iam.gserviceaccount.com \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:YOUR_PROJECT.svc.id.goog[default/agent-sa]"

# Create K8s service account
kubectl create serviceaccount agent-sa
kubectl annotate serviceaccount agent-sa \
  iam.gke.io/gcp-service-account=agent-workload@YOUR_PROJECT.iam.gserviceaccount.com
```

### Step 2: Create Kubernetes Manifests

#### 2.1 Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agent
  template:
    metadata:
      labels:
        app: agent
    spec:
      serviceAccountName: agent-sa
      containers:
      - name: agent
        image: gcr.io/YOUR_PROJECT/agent:latest
        ports:
        - containerPort: 8080
        env:
        - name: PORT
          value: "8080"
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 1000m
            memory: 2Gi
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
```

#### 2.2 Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: agent-service
spec:
  selector:
    app: agent
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

#### 2.3 Network Policy

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: agent-policy
spec:
  podSelector:
    matchLabels:
      app: agent
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 443
```

### Step 3: Deploy to GKE

```bash
# Get credentials
gcloud container clusters get-credentials agent-cluster \
  --zone us-central1-a

# Apply manifests
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f network-policy.yaml

# Get service URL
kubectl get service agent-service
```

### Step 4: Test GKE

```bash
# Port forward to test
kubectl port-forward service/agent-service 8080:80

# Test locally
curl localhost:8080/health
curl -X POST localhost:8080/invoke \
  -H "Content-Type: application/json" \
  -d '{"query": "hello"}'
```

### Step 5: Setup Ingress (optional)

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: agent-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - agent.yourdomain.com
    secretName: agent-tls
  rules:
  - host: agent.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: agent-service
            port:
              number: 80
```

### Step 6: Blue-Green Migration (zero downtime)

```bash
# 1. Keep Cloud Run running (Blue)
# 2. Deploy to GKE (Green)
# 3. Route 5% traffic to GKE
kubectl set env deployment/agent TRAFFIC_SPLIT=5

# 4. Monitor errors
kubectl logs -f deployment/agent

# 5. Gradually increase traffic
kubectl set env deployment/agent TRAFFIC_SPLIT=50
# ... wait 5 min ...
kubectl set env deployment/agent TRAFFIC_SPLIT=100

# 6. Delete Cloud Run
gcloud run services delete agent --region us-central1
```

---

## Migration Path 4: GKE → Cloud Run

**Time**: 15 minutes  
**Complexity**: Easy  
**Downtime**: None (can parallel deploy)

### Step 1: Export Your Agent

```bash
# Get running container image
kubectl get deployment agent -o yaml | grep image:

# Example: gcr.io/YOUR_PROJECT/agent:abc123
```

### Step 2: Deploy to Cloud Run

```bash
gcloud run deploy agent \
  --image gcr.io/YOUR_PROJECT/agent:abc123 \
  --region us-central1 \
  --memory 2Gi
```

### Step 3: Test Cloud Run

```bash
SERVICE_URL=$(gcloud run services describe agent \
  --region us-central1 --format 'value(status.url)')

curl $SERVICE_URL/health
```

### Step 4: Delete GKE (optional)

```bash
# Once Cloud Run is working
gcloud container clusters delete agent-cluster
```

---

## Rollback Procedures

### If Cloud Run Migration Fails

```bash
# Revert DNS to previous service
gcloud dns record-sets update agent.yourdomain.com \
  --rrdatas old-service.run.app

# Keep Cloud Run service (don't delete yet)
# Restore old infrastructure
```

### If Agent Engine Migration Fails

```bash
# Revert to Cloud Run
# Agent Engine and Cloud Run can coexist

# Delete failed agent
gcloud ai agents delete YOUR_AGENT

# Keep Cloud Run running
```

### If GKE Migration Fails

```bash
# Keep Cloud Run service online during GKE deployment
# Only delete Cloud Run after GKE verified for 24+ hours

# Rollback: Point DNS back to Cloud Run
gcloud dns record-sets update agent.yourdomain.com \
  --rrdatas original-cloud-run.run.app
```

---

## Migration Checklist

Before each migration:

- [ ] Backup current configuration
- [ ] Document current metrics/performance
- [ ] Create migration runbook (this guide!)
- [ ] Test in staging first
- [ ] Notify users of potential brief maintenance window
- [ ] Monitor new deployment for 30 minutes
- [ ] Have rollback plan ready
- [ ] Archive old deployment configuration (don't delete)

After each migration:

- [ ] Verify all endpoints working
- [ ] Check error logs for issues
- [ ] Confirm security settings applied
- [ ] Update DNS/load balancer
- [ ] Monitor for 24 hours
- [ ] Document what went well
- [ ] Document issues encountered

---

## Side-by-Side Comparison

| Aspect | Cloud Run | Agent Engine | GKE |
|--------|-----------|--------------|-----|
| **Migration Time** | 15 min | 30 min | 60 min |
| **Downtime** | None | None | None (blue-green) |
| **Complexity** | Easy | Medium | Hard |
| **Rollback Time** | 5 min | 10 min | 20 min |
| **Cost Impact** | Same | Similar | Similar |
| **Scaling** | Auto | Auto | Manual/HPA |
| **Learning Curve** | Low | Medium | High |

---

## Common Migration Issues

### Issue: Agent connects to APIs before

**Problem**: After migration, agent can't reach external APIs

**Solution**:
```bash
# Check firewall rules
# Verify secret manager access
# Confirm API quotas

# Cloud Run: Add Egress VPC connector
# GKE: Verify NetworkPolicy allows egress
```

### Issue: Different performance

**Problem**: New platform is slower/faster than old

**Solution**:
```bash
# Cloud Run: Adjust memory allocation
# GKE: Adjust resource requests
# Check model response time vs inference time
```

### Issue: Secrets not accessible

**Problem**: Environment variables/secrets not loading

**Solution**:
```bash
# Cloud Run: Re-bind Secret Manager
gcloud run services update agent \
  --set-env-vars KEY=projects/YOUR_PROJECT/secrets/KEY/versions/latest

# GKE: Create secret from Secret Manager
gcloud secrets versions access latest --secret=KEY | \
  kubectl create secret generic agent-secrets \
    --from-file=key=/dev/stdin
```

### Issue: Monitoring not working

**Problem**: Can't see metrics/logs after migration

**Solution**:
```bash
# Verify Cloud Logging is connected
gcloud logging sinks list

# Verify proper service account permissions
gcloud projects get-iam-policy YOUR_PROJECT \
  --flatten="bindings[].members" \
  --filter="bindings.members:serviceAccount:*"
```

---

**✅ Complete this migration guide to move safely between platforms.**
