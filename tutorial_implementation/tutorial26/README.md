# Tutorial 26: Gemini Enterprise - Enterprise Agent Platform

**Deploy and manage ADK agents at enterprise scale using Gemini Enterprise (formerly Google AgentSpace)**

## Overview

This tutorial demonstrates building production-ready ADK agents designed for deployment to **Gemini Enterprise**, Google Cloud's platform for enterprise-grade agent orchestration, governance, and collaboration.

**What You'll Learn:**
- Building enterprise-ready agents with ADK
- Designing tools for enterprise integration
- Lead qualification and scoring patterns
- Deploying agents to Gemini Enterprise via Vertex AI Agent Builder
- Enterprise governance and security patterns

**Key Concepts:**
- Enterprise agent architecture
- Tool design for CRM integration
- Lead scoring algorithms
- Competitive intelligence gathering
- Production deployment workflows

## Quick Start

```bash
# 1. Setup
make setup

# 2. Configure authentication
export GOOGLE_API_KEY=your_api_key_here

# 3. Run demo
make demo

# 4. Start development server
make dev
```

## Project Structure

```
tutorial26/
├── enterprise_agent/           # Agent implementation
│   ├── __init__.py            # Package initialization
│   ├── agent.py               # Enterprise lead qualifier agent
│   └── .env.example           # Environment template
├── tests/                     # Comprehensive test suite
│   ├── __init__.py
│   ├── test_agent.py          # Agent configuration tests
│   ├── test_tools.py          # Tool function tests (28 tests)
│   ├── test_imports.py        # Import validation tests
│   └── test_structure.py      # Project structure tests
├── pyproject.toml             # Modern Python packaging
├── requirements.txt           # Python dependencies
├── Makefile                   # Development commands
└── README.md                  # This documentation
```

## What This Tutorial Implements

### Enterprise Lead Qualifier Agent

A production-ready agent that demonstrates enterprise deployment patterns:

**Agent Capabilities:**
- **Company Intelligence**: Look up company size, revenue, and industry
- **Lead Scoring**: Score leads 0-100 based on objective criteria
- **Competitive Analysis**: Provide intel for sales positioning

**Scoring Criteria:**
- Company size > 100 employees: **+30 points**
- Target industries (Technology, Finance, Healthcare): **+30 points**
- Enterprise budget tier: **+40 points**

**Qualification Thresholds:**
- **70-100**: HIGHLY QUALIFIED → Schedule demo immediately
- **40-69**: QUALIFIED → Nurture with targeted content
- **0-39**: UNQUALIFIED → Add to newsletter for future follow-up

### Tool Functions

#### 1. `check_company_size(company_name: str)`
Looks up company information from enterprise database.

**In Production:** Would integrate with:
- CRM systems (Salesforce, HubSpot)
- Company intelligence APIs (Clearbit, ZoomInfo)
- Internal databases

**Returns:**
```python
{
    "status": "success",
    "company_name": "TechCorp",
    "data": {
        "employees": 250,
        "revenue": "50M",
        "industry": "technology"
    },
    "report": "Found company data: 250 employees, $50M revenue"
}
```

#### 2. `score_lead(company_size: int, industry: str, budget: str)`
Scores a sales lead from 0-100 based on qualification criteria.

**Scoring Logic:**
- Large company (>100 employees): +30 points
- Target industry (tech/finance/healthcare): +30 points
- Enterprise budget: +40 points (Business: +20 points)

**Returns:**
```python
{
    "status": "success",
    "score": 100,
    "qualification": "HIGHLY QUALIFIED",
    "factors": [
        "✅ Company size > 100 employees (+30 points)",
        "✅ Target industry: technology (+30 points)",
        "✅ Enterprise budget tier (+40 points)"
    ],
    "recommendation": "Schedule demo immediately",
    "report": "Lead scored 100/100 - HIGHLY QUALIFIED. Schedule demo immediately"
}
```

#### 3. `get_competitive_intel(company_name: str, competitor: str)`
Provides competitive intelligence for sales positioning.

**In Production:** Would integrate with:
- Market intelligence platforms
- News aggregation APIs
- Social listening tools
- Financial data providers

**Returns:**
```python
{
    "status": "success",
    "data": {
        "company": "TechCorp",
        "competitor": "CompetitorX",
        "differentiators": [...],
        "competitor_weaknesses": [...],
        "recent_news": [...]
    },
    "report": "Competitive Analysis: TechCorp vs CompetitorX\n..."
}
```

## Usage Examples

### Example 1: Qualify a Lead

```python
from enterprise_agent import root_agent
from google.adk.agents import Runner

runner = Runner()
result = await runner.run_async(
    "Qualify TechCorp as a sales lead with enterprise budget",
    agent=root_agent
)
print(result.content.parts[0].text)
```

**Example Output:**
```
TechCorp Lead Qualification:

Company Profile:
- Size: 250 employees
- Revenue: $50M
- Industry: Technology

Lead Score: 100/100 - HIGHLY QUALIFIED

Qualification Factors:
✅ Company size > 100 employees (+30 points)
✅ Target industry: technology (+30 points)
✅ Enterprise budget tier (+40 points)

Recommendation: Schedule demo immediately

This is an ideal prospect matching all our qualification criteria.
Priority: High - Contact within 24 hours.
```

### Example 2: Compare to Competitor

```python
result = await runner.run_async(
    "Compare us to CompetitorX for the TechCorp opportunity",
    agent=root_agent
)
```

### Example 3: Score Multiple Leads

```python
result = await runner.run_async(
    "Score these leads: FinanceGlobal (business budget), RetailMart (startup budget)",
    agent=root_agent
)
```

## Testing

Run the comprehensive test suite:

```bash
make test
```

**Test Coverage:**
- ✅ Agent configuration and setup (8 tests)
- ✅ Tool function logic (28 tests)
  - Company lookup functionality
  - Lead scoring algorithm
  - Competitive intelligence gathering
  - Complete qualification workflows
- ✅ Import validation (9 tests)
- ✅ Project structure validation (14 tests)
- **Total: 59+ comprehensive tests**

## Deployment to Gemini Enterprise

### Option 1: Deploy via ADK CLI

```bash
# Deploy to Vertex AI Agent Engine
adk deploy agent_engine \
  --agent-path ./enterprise_agent \
  --project your-gcp-project \
  --region us-central1 \
  --display-name "Enterprise Lead Qualifier"
```

### Option 2: Deploy via Python API

```python
from google.adk.deployment import deploy_to_agent_engine

deploy_to_agent_engine(
    agent=root_agent,
    project='your-gcp-project',
    region='us-central1',
    permissions=['sales-team@company.com'],
    connectors=['salesforce-crm']
)
```

### Option 3: Package and Deploy Manually

```bash
# Create deployment package
adk package \
  --agent agent.py:root_agent \
  --requirements requirements.txt \
  --output lead-qualifier-v1.zip

# Deploy via gcloud
gcloud ai agent-builder agents create \
  --project=your-project \
  --region=us-central1 \
  --display-name="Lead Qualifier" \
  --description="Enterprise sales lead qualification"
```

## Enterprise Configuration

### Production Settings

Create `agentspace.yaml` for production configuration:

```yaml
name: lead-qualifier-prod
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
  - type: salesforce
    dataset: crm_data
    permissions: read
  - type: bigquery
    dataset: company_intel
    permissions: read
```

### Data Connectors

Configure enterprise data sources in Gemini Enterprise console:

**Salesforce Integration:**
- CRM data access (Leads, Opportunities, Accounts)
- OAuth2 authentication
- Real-time sync

**Company Intelligence APIs:**
- Clearbit or ZoomInfo integration
- Company firmographic data
- Industry and size information

**Analytics Platform:**
- BigQuery for historical analysis
- Lead scoring model training data
- Performance metrics

## Gemini Enterprise Features

### What You Get

**Agent Management:**
- Web-based agent console
- Agent Gallery for discovery and sharing
- Agent Designer for no-code agent creation
- Version control and rollback

**Governance:**
- Role-based access control
- Data residency controls
- Compliance (SOC2, GDPR, HIPAA, FedRAMP)
- Audit logging
- PII protection

**Collaboration:**
- Multi-agent orchestration
- Cross-team agent sharing
- Usage monitoring and cost tracking
- Performance analytics

**Data Connectors:**
- Google Workspace (Drive, Docs, Sheets)
- Microsoft 365 (SharePoint, OneDrive)
- Salesforce CRM
- BigQuery and Cloud Storage
- GitHub repositories

### Pricing (October 2025)

**Gemini Business** - $21/seat/month
- Pre-built Google agents
- Agent Designer (no-code builder)
- Basic data connectors
- 25 GiB storage per seat (pooled)
- Up to 300 seats

**Gemini Enterprise Standard** - $30/seat/month
- Everything in Business
- Bring your own ADK agents
- Advanced security (VPC-SC, CMEK)
- Enhanced compliance (HIPAA, FedRAMP)
- 75 GiB storage per seat (pooled)
- Unlimited seats

**Usage Costs** (all editions):
- Model inference: Standard Vertex AI pricing
  - gemini-2.0-flash: ~$0.075/1M input tokens
  - gemini-2.5-flash: ~$0.075/1M input tokens
  - gemini-2.5-pro: ~$1.25/1M input tokens
- Storage: $0.023/GB/month (above quota)

## Development

### Running Locally

```bash
# Start ADK web interface
make dev

# Open http://localhost:8000
# Select 'lead_qualifier' from agent dropdown
```

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_tools.py -v

# Run with coverage
pytest tests/ --cov=enterprise_agent --cov-report=html
```

### Making Changes

1. Edit `enterprise_agent/agent.py`
2. Run tests: `make test`
3. Test locally: `make dev`
4. Deploy to staging environment
5. Monitor and validate
6. Promote to production

## Production Considerations

### Security

- Use service account authentication for production
- Enable VPC Service Controls for data isolation
- Implement customer-managed encryption keys (CMEK)
- Regular security audits and penetration testing
- API rate limiting and abuse prevention

### Performance

- Model selection: Use gemini-2.0-flash for routine queries
- Implement caching for company data lookups
- Batch processing for bulk lead scoring
- Auto-scaling based on demand
- Connection pooling for database access

### Monitoring

- Cloud Monitoring dashboards
- Error rate alerting (>5% threshold)
- Latency monitoring (P95 < 2s)
- Cost tracking and budget alerts
- User satisfaction metrics

### Compliance

- Enable audit logging for all agent interactions
- Configure data residency requirements
- Implement PII redaction policies
- Regular compliance reviews (SOC2, GDPR, HIPAA)
- Data retention and deletion policies

## Troubleshooting

### Common Issues

**Issue:** Agent not appearing in ADK web interface
```bash
# Solution: Install package in editable mode
pip install -e .
```

**Issue:** Authentication errors
```bash
# Solution: Set API key
export GOOGLE_API_KEY=your_key_here

# Or for Vertex AI:
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
export GOOGLE_CLOUD_PROJECT=your-project
```

**Issue:** Import errors
```bash
# Solution: Install dependencies
make setup
```

## Links

- **Tutorial**: [Tutorial 26: Gemini Enterprise](../../docs/tutorial/26_google_agentspace.md)
- **Gemini Enterprise**: [cloud.google.com/gemini-enterprise](https://cloud.google.com/gemini-enterprise)
- **ADK Documentation**: [google.github.io/adk-docs/](https://google.github.io/adk-docs/)
- **Vertex AI Agent Builder**: [cloud.google.com/agent-builder](https://cloud.google.com/agent-builder)
- **Previous Tutorial**: [Tutorial 25 Implementation](../tutorial25/)

## Contributing

This implementation follows the established tutorial pattern:

1. **Working Code First**: Complete implementation before documentation
2. **Comprehensive Testing**: 59+ tests covering all functionality
3. **User-Friendly Setup**: Simple `make setup && make dev` workflow
4. **Clear Documentation**: Step-by-step guides and architecture explanations
5. **Production Ready**: Real-world patterns for enterprise deployment

---

_Built with ❤️ for the ADK community_
