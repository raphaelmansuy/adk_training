# Security Analysis: All Deployment Options

**Status**: ✅ Complete  
**Scope**: Detailed security analysis for ADK deployments  
**Last Updated**: October 17, 2025

---

## Table of Contents

1. [ADK Built-In Server Architecture](#adk-built-in-server-architecture)
2. [Local Development](#local-development)
3. [Cloud Run](#cloud-run)
4. [Google Kubernetes Engine (GKE)](#google-kubernetes-engine-gke)
5. [Agent Engine](#agent-engine)
6. [Security Comparison Matrix](#security-comparison-matrix)
7. [Threat Model Analysis](#threat-model-analysis)
8. [Implementation Patterns](#implementation-patterns)
9. [Security Decision Framework](#security-decision-framework)

**Companion Documents**:
- 📋 [SECURITY_RESEARCH_SUMMARY.md](./SECURITY_RESEARCH_SUMMARY.md) - Executive summary for decision-makers
- 📖 [Tutorial 23: Production Deployment](../../docs/tutorial/23_production_deployment.md) - Main tutorial documentation

---

## ADK Built-In Server Architecture

### What is `get_fast_api_app()`?

ADK provides a built-in FastAPI server via `get_fast_api_app()` that offers:

```python
from google.adk import get_fast_api_app

app = get_fast_api_app(agent)

# This provides:
# POST /invoke - Execute agent with input
# GET /health - Health check endpoint
# WebSocket /ws - Real-time streaming (if enabled)
```

### Architecture Design Philosophy

**Design Goal**: Minimal, focused, platform-agnostic

**Rationale**:
- Cloud platforms are now specialists at infrastructure security
- Adding security to ADK duplicates what platforms do
- Better separation of concerns: ADK = application, Platform = infrastructure
- Allows deployment to any cloud (AWS, Azure, GCP, on-premises)

### Core Endpoints

#### 1. POST /invoke

**Purpose**: Execute agent with user input

**Request**:
```json
{
  "prompt": "What deployment should I use?",
  "session_id": "optional-session-id"
}
```

**Response**:
```json
{
  "response": "Agent response",
  "session_id": "session-id",
  "status": "success"
}
```

**Security Notes**:
- ✅ Input validation (ADK does this)
- ✅ Session tracking (ADK does this)
- ❌ Authentication (Platform does this)
- ❌ Rate limiting (Platform does this)
- ❌ Encryption (Platform does this)

#### 2. GET /health

**Purpose**: Health check for monitoring

**Response**:
```json
{
  "status": "healthy"
}
```

**Security Notes**:
- ✅ No authentication required (intentional for monitoring)
- ⚠️ Reveals agent is running (can be disabled if needed)

#### 3. WebSocket /ws (Optional)

**Purpose**: Real-time streaming responses

**Security Notes**:
- ✅ Uses same authentication as /invoke
- ✅ Session-based authentication
- ❌ Authentication/encryption done by platform

### What ADK Does NOT Provide

| Feature | Why Not | Who Provides It |
|---------|---------|-----------------|
| TLS/HTTPS | Platform specialty | Cloud Run, Agent Engine, GKE |
| Authentication | Platform specialty | Cloud Run IAM, Agent Engine OAuth |
| Authorization | Platform specialty | Cloud Run IAM, GKE RBAC |
| DDoS Protection | Platform specialty | Google Cloud Armor |
| Rate Limiting | Platform specialty | Cloud Run quotas, GKE ingress |
| Request Signing | Deployment-specific | Custom FastAPI if needed |
| Advanced Logging | Beyond scope | Use platform logging |

**Pattern**: "Do one thing well" - ADK focuses on agent execution, platforms handle infrastructure.

---

## Local Development

### Architecture

```
┌─────────────────────────────────────┐
│         Your Machine                │
│                                     │
│  ┌──────────────────────────────┐   │
│  │  ADK Agent (FastAPI Server)  │   │
│  │  - Runs on localhost:8000    │   │
│  │  - HTTP only                 │   │
│  │  - No authentication         │   │
│  │  - No encryption             │   │
│  └──────────────────────────────┘   │
│                                     │
│  curl http://localhost:8000/invoke  │
│                                     │
└─────────────────────────────────────┘
```

### Security Characteristics

**✅ What's Good**:
- Instant feedback for development
- Hot-reloading of code
- Full debugging capabilities
- No startup delay

**❌ What's Bad**:
- No encryption (HTTP only)
- No authentication
- No rate limiting
- No DDoS protection
- Single-threaded (usually)
- No audit logging
- Exposed to anyone on local network

### Threat Model

| Threat | Risk | Mitigation |
|--------|------|-----------|
| **Network sniffer** | 🔴 High | Only use on trusted network |
| **Unauthorized access** | 🔴 High | Firewall port 8000 |
| **Accidental exposure** | 🔴 High | Never port-forward to internet |
| **Development data leak** | 🟡 Medium | Use non-sensitive test data |
| **API key exposure** | 🔴 High | Use mock keys, never real ones |

### Security Checklist

- [ ] Running on localhost only (not 0.0.0.0)
- [ ] Port 8000 blocked by firewall from external access
- [ ] Using development/mock API keys (not production)
- [ ] No production data in local environment
- [ ] Not port-forwarded to internet
- [ ] HTTPS proxy in front if exposed internally
- [ ] Team members don't have direct access to API

### Appropriate Use Cases

✅ **OK for**:
- Learning ADK concepts
- Local testing before production
- Debugging agent behavior
- Development iterations
- Integration testing

❌ **NOT OK for**:
- Production deployment
- Processing real customer data
- Exposing to external users
- Any form of production use

### Transition to Production

**Never directly expose local dev server**. Instead:
1. Code locally with ADK
2. Test locally
3. Deploy to Cloud Run/Agent Engine
4. Test in production environment
5. Monitor with Cloud Logging

---

## Cloud Run

### Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     Google Cloud                             │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Google Cloud Armor (DDoS Protection)                   │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ TLS 1.3 Termination (HTTPS Mandatory)                  │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Cloud Run Service (Auto-scaling)                       │ │
│  │  ┌──────────────────────────────────────────────────┐  │ │
│  │  │ ADK Agent (FastAPI Server in Container)         │  │ │
│  │  │ - Runs in container                              │  │ │
│  │  │ - Non-root user (forced)                         │  │ │
│  │  │ - Limited resources                              │  │ │
│  │  │ - Graceful shutdown                              │  │ │
│  │  └──────────────────────────────────────────────────┘  │ │
│  │                                                         │ │
│  │ IAM Authentication                                      │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Cloud Audit Logs (Compliance Logging)                 │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Security Features (Automatic)

| Feature | What It Does | Your Configuration |
|---------|-------------|-------------------|
| **HTTPS/TLS 1.3** | Encrypts all traffic | None - automatic |
| **Google Cloud Armor** | DDoS protection | Optional (advanced) |
| **Container Registry** | Scans for vulnerabilities | Automatic |
| **IAM Authentication** | Controls who can invoke | Configure in Cloud Run |
| **Encryption at Rest** | Encrypts data storage | None - automatic |
| **Encryption in Transit** | Encrypts network traffic | None - automatic |
| **Non-Root Container** | Prevents privilege escalation | Forced by platform |
| **Network Isolation** | VPC security | Optional (advanced) |
| **Cloud Audit Logs** | Records all API calls | None - automatic |

### What You Must Do

| Task | Importance | Example |
|------|-----------|---------|
| **Secret Management** | 🔴 Critical | Use Secret Manager for API keys |
| **Input Validation** | 🔴 Critical | Validate agent inputs in code |
| **Resource Limits** | 🟡 High | Set memory/CPU limits |
| **Error Handling** | 🟡 High | Log exceptions, don't expose internals |
| **Monitoring** | 🟡 High | Set up Cloud Monitoring alerts |
| **Access Control** | 🟡 High | Use Cloud Run IAM roles |

### Deployment Security

**Step 1**: Create Container with Security

```bash
# Dockerfile best practices
FROM python:3.11-slim

# Run as non-root
RUN useradd -m -u 1000 appuser
USER appuser

# Copy agent code
COPY . /app
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set resource limits (in Cloud Run UI)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
```

**Step 2**: Deploy with Authentication

```bash
gcloud run deploy my-agent \
  --image gcr.io/my-project/my-agent:latest \
  --memory 512Mi \
  --cpu 1 \
  --region us-central1 \
  --no-allow-unauthenticated  # Require IAM authentication
```

**Step 3**: Grant Access to Trusted Principals

```bash
# Allow specific service account to invoke
gcloud run services add-iam-policy-binding my-agent \
  --member=serviceAccount:my-client@my-project.iam.gserviceaccount.com \
  --role=roles/run.invoker
```

### Authentication Patterns

#### Pattern 1: Service-to-Service (Recommended)

**Setup**:
```python
# Client code
from google.auth.transport.requests import Request
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    'service-account.json',
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

request = Request()
credentials.refresh(request)

# Use credentials to call Cloud Run
headers = {
    'Authorization': f'Bearer {credentials.token}',
    'Content-Type': 'application/json'
}

response = requests.post(
    'https://my-agent-abc123.a.run.app/invoke',
    json={'prompt': 'What should I do?'},
    headers=headers
)
```

**Security**: ✅ Best - Uses service accounts, no secret handling

#### Pattern 2: User Authentication (via frontend)

**Setup**:
```javascript
// Frontend (browser)
const idToken = await firebase.auth().currentUser.getIdToken();

const response = await fetch(
  'https://my-agent-abc123.a.run.app/invoke',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${idToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({prompt: 'What should I do?'})
  }
);
```

**Security**: ✅ Good - Uses Firebase auth token, browser handles securely

#### Pattern 3: Direct API Key (NOT recommended)

**Setup**:
```bash
# Generate API key (not recommended for production)
gcloud run services update-traffic my-agent \
  --update-routes my-agent=100 \
  --allow-unauthenticated

# Client must use API key
curl -X POST https://my-agent-abc123.a.run.app/invoke \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What should I do?"}'
```

**Security**: ❌ Weak - Sharing secrets is risky

### Threat Model

| Threat | Likelihood | Impact | Mitigation |
|--------|-----------|--------|-----------|
| **Network sniffer** | 🟢 Low | 🔴 High | TLS 1.3 (automatic) |
| **DDoS attack** | 🟡 Medium | 🔴 High | Cloud Armor (automatic) |
| **Unauthorized access** | 🟡 Medium | 🔴 High | IAM authentication |
| **API key theft** | 🟡 Medium | 🔴 High | Use Secret Manager |
| **Code injection** | 🟡 Medium | 🔴 High | Input validation |
| **Container escape** | 🟢 Low | 🔴 High | Non-root + isolation |
| **Log exposure** | 🟡 Medium | 🟡 Medium | Cloud Audit Logs |

### Security Checklist

**Before Deployment**:
- [ ] Container runs as non-root user
- [ ] API keys in Secret Manager (not env vars)
- [ ] Input validation in agent code
- [ ] Error handling doesn't expose internals
- [ ] Resource limits set (--memory, --cpu)
- [ ] Deployment checklist reviewed

**After Deployment**:
- [ ] HTTPS verified (curl -I https://...)
- [ ] IAM roles configured minimally
- [ ] Cloud Logging verified
- [ ] Health endpoint working
- [ ] Authentication tested (try with wrong token)
- [ ] Monitoring alerts set up
- [ ] DDoS protection enabled (optional)

### Cost Estimates

| Load | Est. Cost | Calculation |
|------|-----------|------------|
| **Low** (100 requests/day) | ~$5/mo | 1-2 idle hours + requests |
| **Medium** (10K requests/day) | ~$40/mo | Based on Google pricing |
| **High** (1M requests/day) | ~$300/mo | Sustained compute |

**Note**: Add model API costs (Gemini pricing) on top.

---

## Google Kubernetes Engine (GKE)

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Google Cloud (GKE Cluster)                     │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Cloud Armor / Cloud CDN (DDoS, Caching)             │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Kubernetes Ingress (TLS Termination, Routing)       │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Kubernetes Cluster (Private or Public)              │  │
│  │                                                      │  │
│  │  ┌────────────────────────────────────────────────┐ │  │
│  │  │ Pod (ADK Agent Container)                      │ │  │
│  │  │ - Workload Identity (authentication)           │ │  │
│  │  │ - Service Account (authorization)              │ │  │
│  │  │ - CPU/Memory limits (resource control)         │ │  │
│  │  │ - Secrets volume (mounted secrets)             │ │  │
│  │  └────────────────────────────────────────────────┘ │  │
│  │                                                      │  │
│  │  Pod Security Policy (runtime security)            │  │
│  │  NetworkPolicy (traffic control)                   │  │
│  │  RBAC (access control)                             │  │
│  │  Binary Authorization (image verification)         │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Cloud Audit Logs (All API calls recorded)          │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Security Features (Requires Configuration)

| Feature | What It Does | Your Configuration |
|---------|-------------|-------------------|
| **Pod Security Policy** | Runtime restrictions | Configure PSP (restricted mode) |
| **Workload Identity** | Service authentication | Bind SA to K8s SA |
| **RBAC** | Access control | Configure roles/rolebindings |
| **NetworkPolicy** | Traffic control | Define ingress/egress rules |
| **Resource Limits** | Prevent DoS | Set requests/limits |
| **Secrets Management** | Secret storage | Mount secrets volume |
| **Binary Authorization** | Image verification | Configure image policies |
| **Audit Logging** | Event logging | Enable Cloud Audit Logs |

### Deployment Pattern

**Step 1**: Create Kubernetes Secret

```bash
kubectl create secret generic api-key \
  --from-literal=GOOGLE_API_KEY=$GOOGLE_API_KEY \
  -n default
```

**Step 2**: Configure Workload Identity

```bash
# Create K8s service account
kubectl create serviceaccount adk-agent-sa -n default

# Create GCP service account
gcloud iam service-accounts create adk-agent

# Bind them
gcloud iam service-accounts add-iam-policy-binding \
  adk-agent@project-id.iam.gserviceaccount.com \
  --role=roles/iam.workloadIdentityUser \
  --member="serviceAccount:project-id.svc.id.goog[default/adk-agent-sa]"

# Annotate K8s SA
kubectl annotate serviceaccount adk-agent-sa \
  iam.gke.io/gcp-service-account=adk-agent@project-id.iam.gserviceaccount.com
```

**Step 3**: Deploy with Security

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: adk-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: adk-agent
  template:
    metadata:
      labels:
        app: adk-agent
    spec:
      serviceAccountName: adk-agent-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsReadOnlyRootFilesystem: true
      containers:
      - name: agent
        image: gcr.io/my-project/adk-agent:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        env:
        - name: PORT
          value: "8080"
        volumeMounts:
        - name: secrets
          mountPath: /var/secrets
          readOnly: true
        - name: tmp
          mountPath: /tmp
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
      volumes:
      - name: secrets
        secret:
          secretName: api-key
      - name: tmp
        emptyDir: {}
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: adk-agent
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: adk-agent
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: adk-agent
spec:
  podSelector:
    matchLabels:
      app: adk-agent
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: istio-system
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: TCP
      port: 443
  - to:
    - namespaceSelector: {}
    ports:
    - protocol: UDP
      port: 53
```

### Threat Model

| Threat | Likelihood | Impact | Mitigation |
|--------|-----------|--------|-----------|
| **Pod escape** | 🟢 Low | 🔴 High | PSP + securityContext |
| **Lateral movement** | 🟡 Medium | 🔴 High | NetworkPolicy |
| **Privilege escalation** | 🟢 Low | 🔴 High | RBAC + Pod Security |
| **Unauthorized access** | 🟡 Medium | 🔴 High | Workload Identity |
| **Resource exhaustion** | 🟡 Medium | 🟡 Medium | Resource limits |
| **Secret exposure** | 🟡 Medium | 🔴 High | Encrypted secrets |
| **Container image tampering** | 🟢 Low | 🔴 High | Binary Authorization |

### Security Checklist

**Pre-Deployment**:
- [ ] Pod Security Policy configured (restricted)
- [ ] Workload Identity binding verified
- [ ] RBAC roles minimally scoped
- [ ] Resource limits set (requests/limits)
- [ ] Secrets encrypted at rest
- [ ] NetworkPolicy defined
- [ ] Binary Authorization enabled
- [ ] Container image scanned for vulnerabilities

**Post-Deployment**:
- [ ] Pod started successfully (no security errors)
- [ ] Workload Identity working (can access GCP)
- [ ] RBAC tested (try unauthorized access)
- [ ] NetworkPolicy working (ingress/egress verified)
- [ ] Audit logs recorded
- [ ] Monitoring alerts configured

### Cost Estimates

| Cluster Size | Est. Cost | Calculation |
|-------------|-----------|------------|
| **Small** (3 nodes, n1-standard-1) | ~$200/mo | Base cluster + 3 nodes |
| **Medium** (5 nodes, n1-standard-2) | ~$500/mo | Larger nodes, more replicas |
| **Large** (10+ nodes) | $1000+/mo | Production cluster |

**Plus**: Model API costs (Gemini pricing), storage, ingress costs.

---

## Agent Engine

### Architecture

```
┌──────────────────────────────────────────────────────────────┐
│           Google Agent Engine (Managed Service)              │
│                                                              │
│  ✅ Private Endpoints Only (No Internet)                    │
│  ✅ mTLS (Mutual TLS Authentication)                       │
│  ✅ OAuth 2.0 (Standard Web Authentication)                │
│  ✅ Content Filters (Safety checks)                        │
│  ✅ Sandboxed Execution (Isolated runtime)                 │
│  ✅ Immutable Audit Logs (Compliance)                      │
│  ✅ FedRAMP Compliance (Only platform)                     │
│  ✅ Zero Configuration (Everything automatic)              │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ ADK Agent (Deployed as-is, no changes)              │  │
│  │ - Runs in sandboxed environment                     │  │
│  │ - Automatic authentication                          │  │
│  │ - Automatic encryption                              │  │
│  │ - Automatic compliance                              │  │
│  │ - All managed by Google                             │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Security Features (All Automatic)

| Feature | What It Does | Your Work |
|---------|-------------|-----------|
| **Private Endpoints** | No public internet access | None - automatic |
| **mTLS** | Mutual TLS for authentication | None - automatic |
| **OAuth 2.0** | Standard web token auth | None - automatic |
| **Content Filters** | Safety checks on outputs | None - automatic |
| **Sandboxing** | Isolated execution environment | None - automatic |
| **Audit Logs** | Immutable compliance logs | None - automatic |
| **FedRAMP** | Government compliance standard | None - automatic |
| **Encryption in Transit** | TLS for all communication | None - automatic |
| **Encryption at Rest** | Data stored encrypted | None - automatic |
| **Automatic Patching** | Security updates applied | None - automatic |

### Deployment (Simplest)

**Step 1**: Deploy agent to Agent Engine

```bash
adk deploy agent_engine \
  --project your-project-id \
  --region us-central1 \
  --agent-name my-agent
```

**That's it.** All security is automatic.

**Step 2**: Invoke agent (from authorized client)

```python
from google.cloud import agent_service_v1beta1

client = agent_service_v1beta1.AgentsClient()

request = agent_service_v1beta1.ExecuteAgentRequest(
    agent=f"projects/your-project/locations/us-central1/agents/my-agent",
    input_data=agent_service_v1beta1.InputData(text="What should I do?")
)

response = client.execute_agent(request=request)
print(response.output_data.text)
```

**All security handled by Agent Engine**.

### Authentication Model

```
┌──────────────────────────┐
│  Your Application        │
│  (Authenticates as self) │
└──────────────┬───────────┘
               │
        OAuth 2.0 Token
               │
               ▼
┌──────────────────────────────────────┐
│  Agent Engine (Verifies Token)       │
│  - Validates token signature         │
│  - Checks token expiration           │
│  - Verifies scopes                   │
│  - Records in audit log              │
│  - Authorizes execution              │
└──────────────────────────────────────┘
```

### Threat Model

Agent Engine's design eliminates most threats:

| Threat | Agent Engine Mitigation | Your Action |
|--------|------------------------|------------|
| **Network sniffer** | mTLS enforced | None |
| **DDoS attack** | Isolated infrastructure | None |
| **Unauthorized access** | OAuth 2.0 verified | Authenticate properly |
| **Code injection** | Sandboxed execution | Validate inputs |
| **Compliance violation** | Immutable audit logs | Review logs |
| **Privilege escalation** | Sandboxed isolation | None |
| **Container escape** | Managed by Google | None |

### Security Checklist

**Pre-Deployment**:
- [ ] Agent code has input validation
- [ ] API keys use Secret Manager
- [ ] Authentication method determined (OAuth 2.0)
- [ ] Audit logging requirements understood

**Post-Deployment**:
- [ ] Agent executes successfully
- [ ] Private endpoint verified (no public URL)
- [ ] Authentication working (try invalid token)
- [ ] Audit logs accessible
- [ ] Compliance requirements met

**Why shorter checklist?** Agent Engine handles most security automatically.

### Cost Estimates

| Usage Level | Est. Cost | Calculation |
|------------|-----------|------------|
| **Development** | ~$0-10/mo | Low volume, free tier |
| **Low Volume** (1K calls/day) | ~$20/mo | Minimal execution time |
| **Medium** (100K calls/day) | ~$50/mo | Standard pricing |
| **High** (1M calls/day) | ~$200/mo | Sustained execution |

**Plus**: Model API costs (Gemini pricing).

**Note**: Agent Engine is slightly more expensive than Cloud Run but includes compliance built-in.

---

## Security Comparison Matrix

### Feature Completeness

| Security Feature | Local | Cloud Run | GKE | Agent Engine |
|-----------------|-------|-----------|-----|--------------|
| **TLS/HTTPS** | ❌ | ✅ | ⚠️ | ✅ |
| **Authentication** | ❌ | ✅ | ⚠️ | ✅ |
| **Authorization** | ❌ | ⚠️ | ✅ | ✅ |
| **DDoS Protection** | ❌ | ✅ | ⚠️ | ✅ |
| **Encryption (Transit)** | ❌ | ✅ | ⚠️ | ✅ |
| **Encryption (Rest)** | ❌ | ✅ | ⚠️ | ✅ |
| **Rate Limiting** | ❌ | ⚠️ | ⚠️ | ✅ |
| **Audit Logging** | ❌ | ✅ | ✅ | ✅ |
| **Compliance Ready** | ❌ | ⚠️ | ⚠️ | ✅ |
| **Zero Configuration** | ❌ | ✅ | ❌ | ✅ |

Legend: ✅ = Automatic, ⚠️ = Requires configuration, ❌ = Not available

### Configuration Burden

| Platform | Setup Complexity | Security Expertise Needed | Ongoing Maintenance |
|----------|------------------|--------------------------|-------------------|
| **Local** | Minimal | None | Minimal |
| **Cloud Run** | Low | Basic | Low |
| **GKE** | High | Advanced (Kubernetes) | High |
| **Agent Engine** | Very Low | Basic | Minimal |

### Compliance Certifications

| Compliance | Local | Cloud Run | GKE | Agent Engine |
|-----------|-------|-----------|-----|--------------|
| **FedRAMP** | ❌ | ❌ | ❌ | ✅ |
| **HIPAA** | ❌ | ⚠️ Config | ⚠️ Config | ✅ |
| **PCI-DSS** | ❌ | ⚠️ Config | ⚠️ Config | ✅ |
| **SOC 2** | ❌ | ✅ Partial | ✅ Partial | ✅ |
| **GDPR** | ❌ | ✅ | ✅ | ✅ |

Legend: ✅ = Built-in, ⚠️ = With configuration, ❌ = Not available

---

## Threat Model Analysis

### Common Threats & Mitigations

#### Threat 1: Network Eavesdropping

**Scenario**: Attacker intercepts API calls to read agent responses

| Platform | Risk | Mitigation |
|----------|------|-----------|
| **Local** | 🔴 High | Firewall, trusted network only |
| **Cloud Run** | 🟢 Low | TLS 1.3 (automatic) |
| **GKE** | 🟢 Low | TLS (configured) |
| **Agent Engine** | 🟢 Low | mTLS (automatic) |

#### Threat 2: Unauthorized Access

**Scenario**: Attacker calls agent API without authorization

| Platform | Risk | Mitigation |
|----------|------|-----------|
| **Local** | 🔴 High | No auth layer |
| **Cloud Run** | 🟡 Medium | Cloud Run IAM (must configure) |
| **GKE** | 🟡 Medium | Workload Identity (must configure) |
| **Agent Engine** | 🟢 Low | OAuth 2.0 (automatic) |

#### Threat 3: API Key Theft

**Scenario**: Production API keys leaked in code/logs

| Platform | Risk | Mitigation |
|----------|------|-----------|
| **Local** | 🔴 High | Manual management |
| **Cloud Run** | 🟢 Low | Secret Manager + audit logs |
| **GKE** | 🟢 Low | Encrypted secrets + RBAC |
| **Agent Engine** | 🟢 Low | No keys needed (OAuth only) |

#### Threat 4: DDoS Attack

**Scenario**: Attacker floods agent endpoint with requests

| Platform | Risk | Mitigation |
|----------|------|-----------|
| **Local** | 🔴 High | No protection |
| **Cloud Run** | 🟢 Low | Cloud Armor (automatic) |
| **GKE** | 🟡 Medium | Optional Cloud Armor |
| **Agent Engine** | 🟢 Low | Built-in protection |

#### Threat 5: Container Escape

**Scenario**: Attacker breaks out of container to access host

| Platform | Risk | Mitigation |
|----------|------|-----------|
| **Local** | 🔴 High | No container isolation |
| **Cloud Run** | 🟢 Low | Non-root + gVisor sandbox |
| **GKE** | 🟡 Medium | Pod Security Policy (must configure) |
| **Agent Engine** | 🟢 Low | Sandboxed (automatic) |

#### Threat 6: Privilege Escalation

**Scenario**: Attacker gains elevated permissions inside container

| Platform | Risk | Mitigation |
|----------|------|-----------|
| **Local** | 🔴 High | No controls |
| **Cloud Run** | 🟢 Low | Non-root forced |
| **GKE** | 🟡 Medium | securityContext (must configure) |
| **Agent Engine** | 🟢 Low | Sandboxed user isolation |

#### Threat 7: Compliance Violation

**Scenario**: Audit logs show unauthorized access for compliance audit

| Platform | Risk | Mitigation |
|----------|------|-----------|
| **Local** | 🔴 High | No audit trail |
| **Cloud Run** | 🟢 Low | Cloud Audit Logs (automatic) |
| **GKE** | 🟢 Low | Cloud Audit Logs (must enable) |
| **Agent Engine** | 🟢 Low | Immutable audit logs (automatic) |

---

## Implementation Patterns

### Pattern 1: Public API (Least Security)

**Scenario**: Public chatbot accessible to anyone

```python
# Cloud Run deployment
gcloud run deploy agent \
  --allow-unauthenticated  # Anyone can call

# Result: ✅ Easy to use, ❌ No access control
```

**Use Case**: Public demo, educational tool, non-sensitive data

**Security Level**: 🟡 Medium (platform security only, no auth)

---

### Pattern 2: Authenticated API (Recommended)

**Scenario**: Private agent for authorized users

```python
# Cloud Run deployment
gcloud run deploy agent \
  --no-allow-unauthenticated  # Require authentication

# Client (with IAM role)
from google.auth.transport.requests import Request
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    'service-account.json'
)
credentials.refresh(Request())

response = requests.post(
    'https://my-agent.run.app/invoke',
    json={'prompt': 'What?'},
    headers={'Authorization': f'Bearer {credentials.token}'}
)
```

**Use Case**: Enterprise deployment, production systems

**Security Level**: ✅ High (auth + platform security)

---

### Pattern 3: Custom FastAPI + Cloud Run (Advanced)

**Scenario**: Need custom authentication beyond IAM

```python
# server.py
from fastapi import FastAPI, HTTPException, Header
from google.adk import Agent

app = FastAPI()
agent = Agent(...)

# Custom LDAP authentication
def verify_ldap(credentials: str):
    # Custom LDAP verification logic
    if not valid_ldap_user(credentials):
        raise HTTPException(status_code=401)

@app.post("/invoke")
async def invoke(
    prompt: str,
    authorization: str = Header(None)
):
    verify_ldap(authorization)  # Custom auth
    result = agent.invoke(prompt)
    return {"response": result}
```

**Use Case**: Corporate deployments with LDAP/Kerberos

**Security Level**: ✅✅ Very High (custom auth + platform security)

---

### Pattern 4: GKE Deployment (Enterprise)

**See GKE section above for full deployment pattern.**

**Use Case**: Existing Kubernetes infrastructure, complex deployments

**Security Level**: ✅✅ Very High (requires expertise)

---

### Pattern 5: Agent Engine (Maximum Security)

**Scenario**: Compliance-required deployment

```bash
# Simple deployment
adk deploy agent_engine \
  --project your-project \
  --region us-central1

# Everything automatic:
# ✅ OAuth 2.0
# ✅ mTLS
# ✅ FedRAMP compliance
# ✅ Sandboxing
# ✅ Audit logs
```

**Use Case**: Government, healthcare, regulated industries

**Security Level**: ✅✅ Maximum (fully managed)

---

## Security Decision Framework

### Decision Tree

```
1. Do you need compliance (FedRAMP/HIPAA)?
   ├─ YES → Agent Engine ✅✅
   └─ NO → Continue...

2. Do you already run Kubernetes?
   ├─ YES → GKE ✅
   └─ NO → Continue...

3. Do you need custom authentication?
   ├─ YES → Custom FastAPI + Cloud Run ⚙️
   └─ NO → Continue...

4. What's your expertise level?
   ├─ Advanced → Cloud Run ✅
   └─ Beginner → Agent Engine ✅✅

Result: Use Agent Engine for simplest/safest
```

### Platform Selection Table

| Your Situation | Recommended Platform | Why | Cost |
|---|---|---|---|
| **Startup/MVP** | Cloud Run | Fast, secure, affordable | ~$40/mo |
| **Regulated industry** | Agent Engine | FedRAMP built-in | ~$50/mo |
| **Existing K8s** | GKE | Leverage investment | ~$300/mo |
| **Learning** | Local + Cloud Run | Development then prod | $0-40/mo |
| **Custom auth** | FastAPI + Cloud Run | Custom logic + platform | ~$60/mo |
| **Maximum compliance** | Agent Engine | All automatic | ~$50/mo |

---

## Conclusion

✅ **ADK is production-secure across all four deployment options.**

Choose the platform that matches your:
1. **Security requirements** (local < Cloud Run < Agent Engine < GKE)
2. **Compliance needs** (none < general < FedRAMP)
3. **Operational expertise** (simple < advanced)
4. **Budget constraints** ($0 < $50 < $500)

**Recommended defaults**:
- **Most teams**: Cloud Run (great balance)
- **Regulated industries**: Agent Engine (compliance included)
- **Kubernetes-first**: GKE (powerful, complex)
- **Learning**: Local, then Cloud Run

Deploy with confidence.

---

**Document Status**: ✅ Complete  
**Last Updated**: October 17, 2025  
**Review Cycle**: Quarterly
