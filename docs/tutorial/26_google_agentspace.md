---
id: google_agentspace
title: "Tutorial 26: Google AgentSpace - Enterprise Agent Platform"
description: "Deploy and manage agents on Google AgentSpace for enterprise-grade agent orchestration, collaboration, and governance."
sidebar_label: "26. Google AgentSpace"
sidebar_position: 26
tags: ["advanced", "agentspace", "enterprise", "platform", "governance"]
keywords: ["google agentspace", "enterprise platform", "agent governance", "collaboration", "orchestration"]
status: "draft"
difficulty: "advanced"
estimated_time: "2 hours"
prerequisites: ["Tutorial 23: Production Deployment", "Google Cloud enterprise account"]
learning_objectives:
  - "Deploy agents to Google AgentSpace"
  - "Configure enterprise agent governance"
  - "Build agent collaboration systems"
  - "Implement enterprise security and compliance"
implementation_link: "https://github.com/raphaelmansuy/adk_training/tree/main/tutorial_implementation/tutorial26"
---

# Tutorial 26: Google AgentSpace - Enterprise Agent Management

**Goal**: Deploy and manage AI agents at enterprise scale using Google Cloud's AgentSpace platform

**Prerequisites**:
- Tutorial 01 (Hello World Agent)
- Tutorial 02 (Function Tools)
- Tutorial 06 (Agents & Orchestration)
- Google Cloud account with billing enabled

**What You'll Learn**:
- Understanding Google AgentSpace architecture
- Deploying ADK agents to AgentSpace
- Using pre-built Google agents (Idea Generation, Deep Research, NotebookLM)
- Building custom agents with Agent Designer
- Managing agents at scale with governance and orchestration
- Integrating enterprise data sources (SharePoint, Drive, OneDrive)
- AgentSpace pricing and licensing
- Best practices for enterprise agent management

---

## What is Google AgentSpace?

**AgentSpace** is Google Cloud's **enterprise platform for managing AI agents at scale**.

**Source**: https://cloud.google.com/products/agentspace?hl=en

**Relationship to ADK**:
- **ADK (Agent Development Kit)**: Framework for *building* agents
- **AgentSpace**: Platform for *deploying and managing* agents
- Think: **ADK = Development** | **AgentSpace = Operations**

```
┌─────────────────────────────────────────────────────────┐
│                   GOOGLE AGENTSPACE                      │
│                  (Cloud Platform Layer)                  │
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Pre-built    │  │ Custom       │  │ ADK-built    │  │
│  │ Agents       │  │ Agents       │  │ Agents       │  │
│  │ (Google)     │  │ (Designer)   │  │ (Deployed)   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                                                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │        Governance & Orchestration               │    │
│  │  - Access control  - Usage tracking             │    │
│  │  - Compliance      - Cost management            │    │
│  └─────────────────────────────────────────────────┘    │
│                                                           │
│  ┌─────────────────────────────────────────────────┐    │
│  │          Data Connectors                        │    │
│  │  SharePoint · Drive · OneDrive · HubSpot · AEM  │    │
│  └─────────────────────────────────────────────────┘    │
│                                                           │
└─────────────────────────────────────────────────────────┘
         ▲                                           ▲
         │                                           │
    Deploy from ADK                             Access via Web
```

**Why Use AgentSpace?**

| Need | AgentSpace Solution |
|------|---------------------|
| Deploy ADK agents to production | Managed hosting with auto-scaling |
| Manage multiple agents | Agent Gallery with discovery and sharing |
| Control agent access | Role-based access control (RBAC) |
| Monitor agent usage | Built-in observability and analytics |
| Connect to enterprise data | Pre-built connectors (SharePoint, Drive, etc.) |
| Ensure compliance | Governance policies and audit logs |
| Low-code agent creation | Agent Designer for non-developers |
| Quick start | Pre-built Google agents (Idea Generation, etc.) |

---

## 1. Pre-built Google Agents

AgentSpace includes **production-ready agents** built by Google:

### Idea Generation Agent

**What it does**: Generates creative ideas based on prompts and context.

**Use cases**:
- Marketing campaigns
- Product brainstorming
- Content creation
- Strategic planning

**Example**:
```
User: "Generate 5 marketing campaign ideas for our new sustainable product line"

Agent: 
1. "Green Future Challenge" - Social media campaign encouraging users to share sustainability wins
2. "Carbon Countdown" - Interactive calculator showing environmental impact of switching products
3. "Eco-Warriors Program" - Loyalty program with sustainability incentives
4. "Nature's Return" - Augmented reality experience showing environmental restoration
5. "Sustainable Stories" - Video series featuring customers' sustainability journeys
```

### Deep Research Agent

**What it does**: Conducts comprehensive research by searching, analyzing, and synthesizing information.

**Use cases**:
- Market research
- Competitive analysis
- Due diligence
- Literature reviews
- Technical investigations

**Data sources**:
- Google Search
- Connected enterprise documents
- Public datasets
- News articles
- Research papers

**Example**:
```
User: "Research emerging trends in electric vehicle battery technology"

Agent:
[REPORT] RESEARCH REPORT: EV Battery Technology Trends (2025)

Key Findings:
1. Solid-state batteries: 50% range improvement, commercial by 2026
2. Lithium-iron-phosphate (LFP): Cost reduction 30% since 2023
3. Silicon anodes: Energy density increase 20-40%
4. Dry electrode coating: Manufacturing cost down 15%
5. Battery-as-a-service models emerging

Market Leaders:
- QuantumScape (solid-state)
- CATL (LFP innovation)
- Panasonic (silicon anode)
- Tesla (4680 cells)

Sources: [15 citations from research papers, industry reports, news]
```

### NotebookLM Enterprise

**What it does**: AI-powered notebook for research, note-taking, and knowledge synthesis.

**Features**:
- Document upload and analysis
- Interactive Q&A with documents
- Automated summarization
- Citation tracking
- Collaborative workspace

**Use cases**:
- Legal document review
- Research paper analysis
- Meeting notes and action items
- Knowledge base creation

**Example workflow**:
1. Upload 10 technical whitepapers
2. Ask: "What are the common security vulnerabilities across these papers?"
3. NotebookLM analyzes all documents
4. Provides synthesized answer with citations
5. Generate summary report

---

## 2. Agent Designer (Low-Code)

**Agent Designer** lets you build custom agents **without coding**.

### How It Works

1. **Define Agent Purpose**: Describe what the agent should do
2. **Select Data Sources**: Connect to enterprise data
3. **Configure Tools**: Choose from pre-built tool library
4. **Set Instructions**: Define agent behavior and personality
5. **Test & Iterate**: Try agent with sample queries
6. **Deploy**: Publish to Agent Gallery

### Example: Customer Support Agent

**Step 1: Purpose**
```
Name: "Customer Support Specialist"
Description: "Helps customers with product questions, troubleshooting, and returns"
```

**Step 2: Data Sources**
- Knowledge Base (Drive folder)
- Product Documentation (SharePoint)
- FAQ Database
- Order History (Salesforce)

**Step 3: Tools**
- Knowledge Search
- Product Lookup
- Order Tracking
- Return Processing

**Step 4: Instructions**
```
You are a friendly and helpful customer support agent.

Guidelines:
- Always greet customers warmly
- Search the knowledge base before answering
- If unsure, say so and escalate to human
- Offer next steps at the end of each interaction
- Be empathetic to frustrated customers

Tone: Professional yet conversational
Response length: Concise (2-3 paragraphs max)
```

**Step 5: Test**
```
Test Query: "My order #12345 arrived damaged. What should I do?"

Agent Response:
"I'm sorry to hear your order arrived damaged! Let me help you with that.

I've looked up order #12345, and I can start a return for you right away. 
You have two options:
1. Free return shipping with a full refund (7-10 days)
2. Immediate replacement with expedited shipping (2-3 days)

Which would you prefer? I'll also include a 15% discount code for your next 
purchase as an apology for the inconvenience."
```

**Step 6: Deploy**
- Click "Publish to Gallery"
- Set access permissions (team-wide, company-wide, or private)
- Configure usage limits
- Enable monitoring

---

## 3. Agent Gallery

**Agent Gallery** is AgentSpace's **marketplace for discovering and sharing agents**.

### Features

**For Users**:
- Browse available agents
- Search by category (Marketing, Engineering, Sales, HR)
- View agent ratings and reviews
- Try agents before deploying
- One-click installation

**For Creators**:
- Publish agents to company gallery
- Track usage metrics
- Receive feedback
- Update agents without breaking deployments
- Monetization (enterprise tier)

### Example Categories

**Marketing**:
- Content Generator
- SEO Optimizer
- Campaign Planner
- Social Media Scheduler
- Brand Voice Analyzer

**Sales**:
- Lead Qualifier
- Proposal Writer
- Competitive Intel
- CRM Assistant
- Email Drafter

**Engineering**:
- Code Reviewer
- Documentation Generator
- Bug Analyzer
- Test Case Creator
- Architecture Advisor

**HR**:
- Resume Screener
- Interview Scheduler
- Onboarding Assistant
- Policy Explainer
- Performance Review Helper

### Using Gallery Agents

```python
# Conceptual example - actual API may differ
from google.cloud import agentspace

# Initialize AgentSpace client
client = agentspace.AgentSpaceClient(project='your-project')

# Browse gallery
agents = client.list_gallery_agents(category='marketing')
for agent in agents:
    print(f"{agent.name}: {agent.rating}⭐ - {agent.installs} installs")

# Deploy agent from gallery
deployed = client.deploy_agent(
    agent_id='content-generator-v2',
    permissions=['marketing-team@company.com']
)

# Use deployed agent
response = client.query_agent(
    agent_id=deployed.id,
    query="Generate blog post outline about AI in healthcare"
)
print(response.content)
```

---

## 4. Deploying ADK Agents to AgentSpace

**Build locally with ADK → Deploy to AgentSpace for production**

### Deployment Process

**Step 1: Build Agent with ADK** (local development)

```python
# agent.py
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

def analyze_sales_data(quarter: str, region: str) -> dict:
    """Analyze sales performance for specific quarter and region."""
    # Your business logic
    return {
        'revenue': 1250000,
        'growth': '+15%',
        'top_products': ['Product A', 'Product B']
    }

sales_agent = Agent(
    model='gemini-2.5-flash',
    name='sales_analyst',
    description='Analyzes sales data and provides insights',
    instruction="""
You are a sales data analyst.
Provide clear, actionable insights.
Highlight trends and opportunities.
    """.strip(),
    tools=[FunctionTool(analyze_sales_data)]
)
```

**Step 2: Test Locally**

```python
from google.adk.agents import Runner

runner = Runner()
result = await runner.run_async(
    "What were our Q4 sales in the North region?",
    agent=sales_agent
)
print(result.content.parts[0].text)
```

**Step 3: Package for Deployment**

```bash
# Create deployment package
adk package \
  --agent agent.py:sales_agent \
  --requirements requirements.txt \
  --output sales-agent-v1.zip
```

**Step 4: Deploy to AgentSpace**

```bash
# Deploy via gcloud CLI
gcloud agentspace agents deploy sales-agent-v1.zip \
  --project=your-project \
  --region=us-central1 \
  --name="Sales Analyst Agent" \
  --description="Q4 sales analysis" \
  --permissions=sales-team@company.com

# Output:
# Deployed: sales-analyst-prod (agent-abc123)
# URL: https://agentspace.google.com/agents/agent-abc123
```

**Step 5: Configure Production Settings**

```yaml
# agentspace.yaml
name: sales-analyst-prod
version: 1.0.0
scaling:
  min_instances: 1
  max_instances: 10
  target_concurrency: 5
monitoring:
  alerts:
    - metric: error_rate
      threshold: 5%
      notification: ops-team@company.com
    - metric: latency_p95
      threshold: 2s
      notification: ops-team@company.com
governance:
  data_residency: us
  compliance: [SOC2, GDPR]
  audit_logging: true
connectors:
  - type: bigquery
    dataset: sales_data
    permissions: read
```

**Step 6: Monitor in AgentSpace Dashboard**

- Real-time usage metrics
- Error rates and logs
- Cost tracking
- User feedback
- Performance trends

---

## 5. Data Connectors

AgentSpace provides **pre-built connectors** for enterprise data sources.

### Available Connectors

| Connector | Description | Use Cases |
|-----------|-------------|-----------|
| **Google Drive** | Access Drive files and folders | Document search, content analysis |
| **SharePoint** | Connect to SharePoint sites | Knowledge base, policy documents |
| **OneDrive** | Access OneDrive for Business | Personal files, team documents |
| **HubSpot** | CRM and marketing data | Lead management, customer insights |
| **Salesforce** | Sales and CRM data | Opportunity analysis, forecasting |
| **Adobe AEM** | Digital asset management | Content discovery, asset metadata |
| **BigQuery** | Data warehouse queries | Analytics, reporting, insights |
| **Looker** | Business intelligence | Dashboard data, metrics |

### Configuring Connectors

**Example: SharePoint Connector**

```yaml
# connector-config.yaml
connectors:
  - name: company-sharepoint
    type: sharepoint
    config:
      site_url: https://company.sharepoint.com/sites/knowledge-base
      authentication:
        type: oauth2
        client_id: ${SHAREPOINT_CLIENT_ID}
        client_secret: ${SHAREPOINT_CLIENT_SECRET}
      permissions:
        - read:documents
        - read:lists
    filters:
      - include: /Documents/**
      - exclude: /Documents/Archive/**
      - file_types: [.docx, .pdf, .xlsx]
    indexing:
      enabled: true
      schedule: daily
      incremental: true
```

**Using Connectors in Agents**

```python
from google.adk.agents import Agent
from google.adk.tools import url_context

policy_agent = Agent(
    model='gemini-2.5-flash',
    name='policy_assistant',
    instruction="""
You help employees understand company policies.
Always cite the specific policy document when answering.
If policy doesn't cover the question, say so clearly.
    """.strip(),
    tools=[
        url_context(
            name='company_policies',
            connector='company-sharepoint',
            path='/Documents/Policies/'
        )
    ]
)

# AgentSpace automatically handles:
# - Authentication to SharePoint
# - Document indexing
# - Search and retrieval
# - Permissions enforcement
```

---

## 6. Governance & Orchestration

**Enterprise-grade controls** for managing agents at scale.

### Access Control

**Role-Based Access Control (RBAC)**:

```yaml
# access-control.yaml
agents:
  - id: sales-analyst
    permissions:
      - role: sales-team
        access: [use, view_metrics]
      - role: sales-managers
        access: [use, view_metrics, edit_config]
      - role: admins
        access: [all]
  
  - id: hr-assistant
    permissions:
      - role: hr-team
        access: [use, view_metrics, edit_config]
      - role: employees
        access: [use]
      - role: contractors
        access: []  # No access
```

**Data Access Controls**:

```yaml
data_governance:
  pii_handling:
    mode: strict
    allowed_fields: [name, email, department]
    redacted_fields: [ssn, salary, medical_info]
  
  data_residency:
    primary: us-central1
    replicas: [europe-west1]
    prohibited_regions: [asia-pacific]
  
  retention:
    conversations: 90_days
    logs: 1_year
    audit_trail: 7_years
```

### Usage Monitoring

**Built-in Metrics**:
- Queries per day/hour
- Average response time
- Error rates
- Token usage
- Cost per query
- User satisfaction scores

**Custom Dashboards**:

```python
# Conceptual example
from google.cloud.agentspace import monitoring

# Create custom dashboard
dashboard = monitoring.Dashboard('Sales Agent Analytics')

dashboard.add_widget(
    monitoring.TimeSeriesChart(
        metric='agent_queries',
        agent_id='sales-analyst',
        aggregation='sum',
        group_by='user_department'
    )
)

dashboard.add_widget(
    monitoring.ScoreCard(
        metric='average_satisfaction',
        agent_id='sales-analyst',
        threshold_good=4.0,
        threshold_warning=3.0
    )
)
```

### Cost Management

**Budget Controls**:

```yaml
budgets:
  - agent: sales-analyst
    monthly_limit: $500
    alerts:
      - threshold: 80%
        action: notify_owner
      - threshold: 100%
        action: pause_agent
  
  - team: marketing-team
    monthly_limit: $2000
    alerts:
      - threshold: 90%
        action: notify_manager
```

**Cost Optimization**:
- Model selection (2.5-flash for routine, 2.5-pro for complex)
- Caching frequently accessed data
- Batching queries when possible
- Setting token limits per query
- Auto-scaling based on demand

---

## 7. Pricing & Plans

**AgentSpace Pricing** (as of 2025):

**Base License**: **$25 USD per seat per month**

**What's Included**:
- Access to pre-built Google agents
- Agent Designer (low-code builder)
- Agent Gallery access
- Up to 10 deployed agents per seat
- Standard data connectors
- Basic monitoring and analytics
- Community support

**Enterprise Add-ons**:

| Feature | Additional Cost |
|---------|----------------|
| Advanced connectors (Salesforce, AEM) | $10/connector/month |
| Custom data residency | $50/month |
| Advanced governance & audit logs | $100/month |
| Dedicated support | $500/month |
| SLA guarantees (99.9% uptime) | 20% of license cost |

**Usage-Based Costs** (on top of license):
- **Model inference**: Same as Vertex AI pricing
  - gemini-2.5-flash: ~$0.075/1M input tokens
  - gemini-2.5-pro: ~$1.25/1M input tokens
- **Storage**: $0.023/GB/month
- **Data egress**: Standard Cloud pricing

**Example Calculation**:

**Scenario**: 50-person marketing team using AgentSpace

```
Base licenses:        50 seats × $25    = $1,250/month
SharePoint connector:  1 × $10          =    $10/month
Drive connector:       1 × $10          =    $10/month
Advanced governance:   1 × $100         =   $100/month
                                        ────────────
Monthly fixed cost:                     $1,370

Estimated usage:
- 10,000 queries/month
- Avg 500 tokens/query (input + output)
- Using gemini-2.5-flash

Model cost: 10,000 × 500 × $0.075/1M  =    $0.38/month

Total monthly cost: ~$1,370
Per-seat cost: $1,370 / 50 = $27.40/seat/month
```

---

## 8. Real-World Example: Multi-Team Agent System

**Scenario**: Deploy agent ecosystem for entire company.

### Architecture

```
Company Agent Ecosystem (AgentSpace)
├── Marketing Team (10 seats)
│   ├── Content Generator Agent
│   ├── SEO Optimizer Agent
│   └── Campaign Planner Agent
├── Sales Team (25 seats)
│   ├── Lead Qualifier Agent (ADK-built)
│   ├── Proposal Writer Agent
│   └── Competitive Intel Agent (ADK-built)
├── Engineering Team (40 seats)
│   ├── Code Reviewer Agent (ADK-built)
│   ├── Documentation Generator
│   └── Bug Analyzer Agent
└── HR Team (5 seats)
    ├── Resume Screener Agent
    ├── Interview Scheduler
    └── Onboarding Assistant (ADK-built)

Data Connectors:
- SharePoint (company policies, knowledge base)
- Google Drive (team documents)
- Salesforce (CRM data)
- BigQuery (analytics data)
- GitHub (code repositories)

Governance:
- Role-based access control
- Data residency: US only
- Compliance: SOC2, GDPR
- Audit logging: All agent interactions
```

### Implementation

**1. Deploy Custom ADK Agents**

```python
# lead_qualifier.py (built with ADK)
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.models import GoogleGenAI

def check_company_size(company_name: str) -> dict:
    """Look up company size from database."""
    # Integration with company database
    return {'employees': 250, 'revenue': '50M'}

def score_lead(company_size: int, industry: str, budget: str) -> int:
    """Score lead from 0-100."""
    # Lead scoring logic
    score = 0
    if company_size > 100: score += 30
    if industry in ['technology', 'finance']: score += 30
    if budget == 'enterprise': score += 40
    return score

lead_qualifier = Agent(
    model='gemini-2.5-flash',
    name='lead_qualifier',
    description='Qualifies sales leads automatically',
    instruction="""
You qualify sales leads based on company profile.

Qualification criteria:
- Company size > 100 employees
- Industries: Technology, Finance, Healthcare
- Budget: Enterprise tier

Provide:
1. Lead score (0-100)
2. Key qualification factors
3. Recommended next steps
4. Potential objections
    """.strip(),
    tools=[
        FunctionTool(check_company_size),
        FunctionTool(score_lead)
    ]
)

# Deploy to AgentSpace
if __name__ == '__main__':
    from google.adk.deployment import deploy_to_agentspace
    
    deploy_to_agentspace(
        agent=lead_qualifier,
        project='company-agentspace',
        region='us-central1',
        permissions=['sales-team@company.com'],
        connectors=['salesforce-crm']
    )
```

**2. Configure Data Connectors**

```yaml
# agentspace-connectors.yaml
connectors:
  - name: salesforce-crm
    type: salesforce
    config:
      instance_url: https://company.my.salesforce.com
      authentication:
        type: oauth2
        client_id: ${SALESFORCE_CLIENT_ID}
        client_secret: ${SALESFORCE_CLIENT_SECRET}
      objects:
        - Lead
        - Opportunity
        - Account
        - Contact
  
  - name: company-sharepoint
    type: sharepoint
    config:
      site_url: https://company.sharepoint.com
      authentication:
        type: oauth2
      paths:
        - /Policies/**
        - /ProductDocs/**
  
  - name: engineering-github
    type: github
    config:
      organization: company-org
      authentication:
        type: personal_access_token
        token: ${GITHUB_TOKEN}
      repositories:
        - main-product
        - api-backend
        - mobile-app
```

**3. Set Governance Policies**

```yaml
# governance.yaml
global_policies:
  data_residency: us-central1
  compliance: [SOC2, GDPR, HIPAA]
  audit_logging: all_interactions
  pii_protection: enabled

team_permissions:
  - team: marketing-team@company.com
    agents: [content-generator, seo-optimizer, campaign-planner]
    data_access: [sharepoint:marketing/**, drive:marketing/**]
  
  - team: sales-team@company.com
    agents: [lead-qualifier, proposal-writer, competitive-intel]
    data_access: [salesforce:*, sharepoint:sales/**]
  
  - team: engineering-team@company.com
    agents: [code-reviewer, doc-generator, bug-analyzer]
    data_access: [github:*, bigquery:analytics_db]
  
  - team: hr-team@company.com
    agents: [resume-screener, interview-scheduler, onboarding-assistant]
    data_access: [sharepoint:hr/**, drive:hr/**]
    pii_access: [name, email, phone, resume]

budgets:
  - team: marketing-team
    monthly_limit: $500
  - team: sales-team
    monthly_limit: $1500
  - team: engineering-team
    monthly_limit: $2000
  - team: hr-team
    monthly_limit: $300
```

**4. Monitor System-Wide**

```python
# monitoring_dashboard.py
from google.cloud.agentspace import monitoring

# Create executive dashboard
exec_dashboard = monitoring.Dashboard('Company Agent Metrics')

# Add widgets
exec_dashboard.add_widget(
    monitoring.MetricCard('Total Queries Today', metric='total_queries')
)

exec_dashboard.add_widget(
    monitoring.BarChart(
        title='Queries by Team',
        metric='queries',
        group_by='team',
        time_range='today'
    )
)

exec_dashboard.add_widget(
    monitoring.LineChart(
        title='Cost Trend',
        metric='total_cost',
        time_range='30_days',
        group_by='team'
    )
)

exec_dashboard.add_widget(
    monitoring.Table(
        title='Most Used Agents',
        columns=['agent_name', 'queries', 'avg_satisfaction', 'cost'],
        sort_by='queries',
        limit=10
    )
)

# Publish dashboard
exec_dashboard.publish(viewers=['executives@company.com'])
```

---

## 9. Best Practices

### Development Workflow

**✅ DO**:
1. **Build locally with ADK** → Test thoroughly → Deploy to AgentSpace
2. **Version your agents** (v1.0, v1.1, etc.) for rollback capability
3. **Use staging environment** before production deployment
4. **Monitor metrics** after each deployment
5. **Collect user feedback** continuously
6. **Document agent capabilities** in Agent Gallery

**❌ DON'T**:
1. Deploy untested agents directly to production
2. Give all agents access to all data
3. Ignore cost monitoring
4. Skip governance configuration
5. Hard-code credentials
6. Deploy without rollback plan

### Security

**Agent Access**:
- Use least-privilege principle for data connectors
- Regularly audit agent permissions
- Rotate API keys and credentials
- Enable MFA for AgentSpace access
- Monitor for unusual query patterns

**Data Protection**:
- Enable PII redaction for sensitive fields
- Configure data residency requirements
- Implement data retention policies
- Enable audit logging for compliance
- Regular security reviews

### Cost Optimization

**Model Selection**:
```python
# Use 2.5-flash for routine queries
routine_agent = Agent(model='gemini-2.5-flash')  # Cheaper

# Use 2.5-pro only for complex reasoning
complex_agent = Agent(model='gemini-2.5-pro')    # More expensive
```

**Caching**:
- Cache frequently accessed documents
- Use connector indexing for faster search
- Implement response caching for common queries

**Query Optimization**:
- Set max token limits
- Use concise instructions
- Batch similar queries when possible
- Disable streaming when not needed

### Monitoring & Alerts

**Key Metrics to Track**:
1. **Usage**: Queries per day, peak hours
2. **Performance**: Average response time, error rate
3. **Cost**: Daily/monthly spend by team
4. **Quality**: User satisfaction, task completion rate
5. **Errors**: Failed queries, timeout rate

**Alert Configuration**:
```yaml
alerts:
  - name: High Error Rate
    condition: error_rate > 5%
    notification: ops-team@company.com
    severity: warning
  
  - name: Budget Exceeded
    condition: monthly_cost > budget_limit
    notification: finance-team@company.com
    severity: critical
  
  - name: Slow Response
    condition: p95_latency > 3s
    notification: eng-team@company.com
    severity: warning
```

---

## Summary

You've learned how to deploy and manage agents at enterprise scale with Google AgentSpace:

**Key Takeaways**:

- ✅ **AgentSpace** is Google Cloud's enterprise platform for agent operations
- ✅ **ADK builds agents** locally → **AgentSpace deploys** to production
- ✅ **Pre-built agents** available (Idea Generation, Deep Research, NotebookLM)
- ✅ **Agent Designer** for low-code agent creation
- ✅ **Agent Gallery** for discovering and sharing agents
- ✅ **Data connectors** for SharePoint, Drive, Salesforce, etc.
- ✅ **Governance & orchestration** for enterprise controls
- ✅ **Pricing**: $25/seat/month + usage-based model costs
- ✅ Deploy ADK agents with `adk package` and `gcloud agentspace deploy`
- ✅ Monitor with built-in dashboards and custom metrics

**When to Use AgentSpace**:

| Use Case | AgentSpace? |
|----------|-------------|
| Prototyping new agent | ❌ Use ADK locally |
| Production deployment | ✅ Deploy to AgentSpace |
| Personal project | ❌ Run locally or Cloud Run |
| Enterprise with 50+ users | ✅ AgentSpace with governance |
| Need pre-built agents | ✅ Use Gallery agents |
| Custom agent with complex logic | [FLOW] Build with ADK → Deploy to AgentSpace |
| Manage multiple teams | ✅ AgentSpace with RBAC |
| Need enterprise data connectors | ✅ SharePoint, Drive, Salesforce connectors |

**Production Deployment Checklist**:

- [ ] Agent tested thoroughly in local ADK environment
- [ ] Agent versioned (v1.0.0, v1.1.0, etc.)
- [ ] Data connectors configured with proper permissions
- [ ] Governance policies defined (RBAC, data residency)
- [ ] Budget limits set per team/agent
- [ ] Monitoring and alerts configured
- [ ] PII protection enabled for sensitive data
- [ ] Audit logging enabled for compliance
- [ ] Rollback plan documented
- [ ] User documentation published to Agent Gallery
- [ ] Staging environment tested before production
- [ ] Cost estimates reviewed and approved

**Next Steps**:

- **Tutorial 27**: Integrate third-party framework tools (LangChain, CrewAI)
- **Tutorial 28**: Use other LLMs with LiteLLM (OpenAI, Claude, Ollama)
- **Tutorial 19**: Implement Artifacts & File Management
- **Tutorial 18**: Master Events & Observability

**Resources**:

- [Google AgentSpace](https://cloud.google.com/products/agentspace?hl=en)
- [AgentSpace Documentation](https://cloud.google.com/agentspace/docs)
- [Pricing Calculator](https://cloud.google.com/products/calculator)
- [ADK Deployment Guide](https://google.github.io/adk-docs/deployment/)
- [Data Connectors](https://cloud.google.com/agentspace/docs/connectors)

---

**Congratulations!** You now understand how to scale ADK agents to enterprise production with Google AgentSpace. You can deploy custom agents, use pre-built agents, manage governance, and monitor operations at scale.
