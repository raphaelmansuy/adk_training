"""
Tutorial 26: Gemini Enterprise - Enterprise Agent Deployment

This tutorial demonstrates building ADK agents that can be deployed to
Gemini Enterprise (formerly Google AgentSpace) for enterprise-scale
agent management with governance, orchestration, and collaboration.

Key Concepts:
- Building enterprise-ready agents with ADK
- Enterprise agent architecture patterns
- Lead qualification and scoring logic
- Tool design for enterprise integration
- Production-ready agent configuration

This agent would be deployed to Gemini Enterprise using:
  adk deploy agent_engine --agent-path . --project your-project
"""

from __future__ import annotations

from typing import Dict, Any

from google.adk.agents import Agent
from google.adk.tools import FunctionTool


# ============================================================================
# Enterprise Tool Functions
# ============================================================================

def check_company_size(company_name: str) -> Dict[str, Any]:
    """
    Look up company size from enterprise database.
    
    In production, this would integrate with:
    - CRM systems (Salesforce, HubSpot)
    - Company intelligence APIs (Clearbit, ZoomInfo)
    - Internal databases
    
    Args:
        company_name: Name of the company to look up
        
    Returns:
        Dictionary with company information including employee count and revenue
    """
    # Simulated company database lookup
    # In production, this would call actual APIs or databases
    company_db = {
        "TechCorp": {"employees": 250, "revenue": "50M", "industry": "technology"},
        "FinanceGlobal": {"employees": 1200, "revenue": "500M", "industry": "finance"},
        "HealthPlus": {"employees": 450, "revenue": "120M", "industry": "healthcare"},
        "RetailMart": {"employees": 50, "revenue": "5M", "industry": "retail"},
        "StartupXYZ": {"employees": 15, "revenue": "1M", "industry": "technology"},
    }
    
    # Default for unknown companies
    company_data = company_db.get(
        company_name,
        {"employees": 0, "revenue": "Unknown", "industry": "unknown"}
    )
    
    return {
        "status": "success",
        "company_name": company_name,
        "data": company_data,
        "report": f"Found company data: {company_data['employees']} employees, ${company_data['revenue']} revenue"
    }


def score_lead(company_size: int, industry: str, budget: str) -> Dict[str, Any]:
    """
    Score a sales lead from 0-100 based on qualification criteria.
    
    Scoring criteria:
    - Company size: 30 points if > 100 employees
    - Industry fit: 30 points for target industries
    - Budget level: 40 points for enterprise budget
    
    Args:
        company_size: Number of employees
        industry: Industry sector (technology, finance, healthcare, etc.)
        budget: Budget category (startup, business, enterprise)
        
    Returns:
        Dictionary with lead score and qualification details
    """
    score = 0
    factors = []
    
    # Company size scoring
    if company_size > 100:
        score += 30
        factors.append("✅ Company size > 100 employees (+30 points)")
    else:
        factors.append("❌ Company size < 100 employees (0 points)")
    
    # Industry fit scoring
    target_industries = ['technology', 'finance', 'healthcare']
    if industry.lower() in target_industries:
        score += 30
        factors.append(f"✅ Target industry: {industry} (+30 points)")
    else:
        factors.append(f"❌ Non-target industry: {industry} (0 points)")
    
    # Budget tier scoring
    if budget.lower() == 'enterprise':
        score += 40
        factors.append("✅ Enterprise budget tier (+40 points)")
    elif budget.lower() == 'business':
        score += 20
        factors.append("⚠️  Business budget tier (+20 points)")
    else:
        factors.append("❌ Startup budget tier (0 points)")
    
    # Determine qualification status
    if score >= 70:
        status = "HIGHLY QUALIFIED"
        recommendation = "Schedule demo immediately"
    elif score >= 40:
        status = "QUALIFIED"
        recommendation = "Nurture lead with targeted content"
    else:
        status = "UNQUALIFIED"
        recommendation = "Add to newsletter list for future follow-up"
    
    return {
        "status": "success",
        "score": score,
        "qualification": status,
        "factors": factors,
        "recommendation": recommendation,
        "report": f"Lead scored {score}/100 - {status}. {recommendation}"
    }


def get_competitive_intel(company_name: str, competitor: str) -> Dict[str, Any]:
    """
    Get competitive intelligence comparing company to competitor.
    
    In production, this would integrate with:
    - Market intelligence platforms
    - News aggregation APIs
    - Social listening tools
    - Financial data providers
    
    Args:
        company_name: Name of the prospect company
        competitor: Name of the competitor to compare against
        
    Returns:
        Dictionary with competitive analysis
    """
    # Simulated competitive intelligence
    # In production, this would call real market intelligence APIs
    intel = {
        "company": company_name,
        "competitor": competitor,
        "differentiators": [
            "Better enterprise support and SLAs",
            "More flexible pricing for mid-market",
            "Stronger data security and compliance features",
            "Better integration with Google Cloud ecosystem"
        ],
        "competitor_weaknesses": [
            "Higher pricing for similar features",
            "Limited customization options",
            "Slower support response times"
        ],
        "recent_news": [
            f"{competitor} raised Series C funding last quarter",
            f"{company_name} won industry award for innovation",
            f"{competitor} facing customer retention challenges"
        ]
    }
    
    report = f"""
Competitive Analysis: {company_name} vs {competitor}

Our Differentiators:
{chr(10).join(f'  • {d}' for d in intel['differentiators'])}

Competitor Weaknesses:
{chr(10).join(f'  • {w}' for w in intel['competitor_weaknesses'])}

Recent Market Activity:
{chr(10).join(f'  • {n}' for n in intel['recent_news'])}
    """.strip()
    
    return {
        "status": "success",
        "data": intel,
        "report": report
    }


# ============================================================================
# Enterprise Agent Definition
# ============================================================================

root_agent = Agent(
    model="gemini-2.0-flash",
    name="lead_qualifier",
    description="Enterprise sales lead qualification agent with company intelligence and scoring",
    instruction="""
You are an enterprise sales lead qualification specialist.

Your role is to:
1. Analyze sales leads based on company profile and fit
2. Score leads from 0-100 using objective criteria
3. Provide competitive intelligence when relevant
4. Recommend next steps for sales team

Qualification Criteria:
- Company size > 100 employees (30 points)
- Target industries: Technology, Finance, Healthcare (30 points)
- Enterprise budget tier (40 points)

Scoring Thresholds:
- 70+: HIGHLY QUALIFIED - Schedule demo immediately
- 40-69: QUALIFIED - Nurture with targeted content
- <40: UNQUALIFIED - Add to newsletter for future follow-up

When analyzing a lead:
1. Use check_company_size to get company information
2. Use score_lead with the company data to calculate qualification score
3. If competitor mentioned, use get_competitive_intel for positioning
4. Provide clear recommendations with specific next steps

Always be professional, data-driven, and focused on helping sales teams
prioritize their efforts on the most promising opportunities.
    """.strip(),
    tools=[
        FunctionTool(check_company_size),
        FunctionTool(score_lead),
        FunctionTool(get_competitive_intel)
    ]
)

# Deployment Configuration (for reference)
# This agent would be deployed to Gemini Enterprise using:
#
# adk deploy agent_engine \
#   --agent-path ./enterprise_agent \
#   --project your-gcp-project \
#   --region us-central1 \
#   --display-name "Enterprise Lead Qualifier"
#
# Or via Python API:
# from google.adk.deployment import deploy_to_agent_engine
# deploy_to_agent_engine(
#     agent=root_agent,
#     project='your-project',
#     region='us-central1',
#     permissions=['sales-team@company.com'],
#     connectors=['salesforce-crm']
# )
