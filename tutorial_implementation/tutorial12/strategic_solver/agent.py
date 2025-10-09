"""
Strategic Problem Solver - Tutorial 12: Planners & Thinking Configuration

This agent demonstrates advanced reasoning capabilities using:
- BuiltInPlanner with extended thinking
- PlanReActPlanner for structured reasoning
- Custom BasePlanner for domain-specific workflows

The agent solves complex business problems using market analysis, ROI calculations,
risk assessment, and strategic planning tools.
"""

from datetime import datetime
from typing import Dict, Any, List, Optional

from google.adk.agents import Agent
from google.adk.planners import BuiltInPlanner, PlanReActPlanner, BasePlanner
from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.models.llm_request import LlmRequest
from google.genai import types


# ============================================================================
# BUSINESS ANALYSIS TOOLS
# ============================================================================

def analyze_market(
    industry: str,
    region: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Analyze market conditions for strategic planning.

    Args:
        industry: The industry sector to analyze
        region: Geographic region for analysis
        tool_context: ADK tool context

    Returns:
        Dict with market analysis results
    """
    try:
        # Simulate market analysis (in production, this would call real APIs)
        # Using deterministic but realistic data for testing
        market_data = {
            'healthcare': {
                'growth_rate': '8.5%',
                'competition': 'High',
                'trends': ['Digital transformation', 'AI adoption', 'Telemedicine'],
                'opportunities': ['Emerging markets', 'Specialized AI solutions'],
                'threats': ['Regulatory changes', 'Data privacy concerns']
            },
            'finance': {
                'growth_rate': '6.2%',
                'competition': 'Very High',
                'trends': ['FinTech innovation', 'Blockchain', 'Open banking'],
                'opportunities': ['AI-driven insights', 'Personalized services'],
                'threats': ['Cybersecurity risks', 'Regulatory compliance']
            },
            'retail': {
                'growth_rate': '4.1%',
                'competition': 'High',
                'trends': ['E-commerce growth', 'Omnichannel retail', 'Sustainability'],
                'opportunities': ['Direct-to-consumer models', 'Personalization'],
                'threats': ['Supply chain disruptions', 'Economic uncertainty']
            }
        }

        # Default data for unknown industries
        if industry.lower() not in market_data:
            analysis = {
                'industry': industry,
                'region': region,
                'growth_rate': '5.0%',
                'competition': 'Medium',
                'trends': ['Digital transformation', 'Innovation'],
                'opportunities': ['Market expansion', 'Technology adoption'],
                'threats': ['Competition', 'Economic factors']
            }
        else:
            analysis = market_data[industry.lower()]
            analysis.update({
                'industry': industry,
                'region': region
            })

        analysis['timestamp'] = datetime.now().isoformat()

        return {
            'status': 'success',
            'report': f'Completed market analysis for {industry} in {region}',
            'analysis': analysis
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Failed to analyze market: {str(e)}'
        }


def calculate_roi(
    investment: float,
    annual_return: float,
    years: int,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Calculate return on investment for financial planning.

    Args:
        investment: Initial investment amount
        annual_return: Expected annual return rate (percentage)
        years: Investment time horizon
        tool_context: ADK tool context

    Returns:
        Dict with ROI calculation results
    """
    try:
        # Validate inputs
        if investment <= 0:
            raise ValueError("Investment must be positive")
        if annual_return < -100:
            raise ValueError("Annual return cannot be less than -100%")
        if years <= 0:
            raise ValueError("Years must be positive")

        # Calculate compound growth
        annual_rate = annual_return / 100
        total_return = investment * ((1 + annual_rate) ** years)
        profit = total_return - investment
        roi_percentage = (profit / investment) * 100

        # Calculate annual growth details
        annual_growth = []
        for year in range(1, years + 1):
            year_end_value = investment * ((1 + annual_rate) ** year)
            year_profit = year_end_value - investment
            annual_growth.append({
                'year': year,
                'value': round(year_end_value, 2),
                'profit': round(year_profit, 2),
                'roi': round((year_profit / investment) * 100, 2)
            })

        result = {
            'initial_investment': investment,
            'annual_return_rate': f"{annual_return}%",
            'years': years,
            'final_value': round(total_return, 2),
            'total_profit': round(profit, 2),
            'roi_percentage': round(roi_percentage, 2),
            'annual_breakdown': annual_growth,
            'timestamp': datetime.now().isoformat()
        }

        return {
            'status': 'success',
            'report': f'ROI calculation: {roi_percentage:.1f}% return over {years} years',
            'calculation': result
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Failed to calculate ROI: {str(e)}'
        }


def assess_risk(
    factors: List[str],
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Assess business risks based on provided factors.

    Args:
        factors: List of risk factors to evaluate
        tool_context: ADK tool context

    Returns:
        Dict with risk assessment results
    """
    try:
        # Risk scoring system (higher = more risky)
        risk_scores = {
            'market_volatility': 7,
            'regulatory_changes': 6,
            'competition': 8,
            'technology_disruption': 7,
            'economic_uncertainty': 6,
            'supply_chain_issues': 5,
            'cybersecurity_threats': 8,
            'talent_shortage': 4,
            'geopolitical_risks': 6,
            'climate_change': 5,
            'pandemic_risks': 7,
            'currency_fluctuation': 5,
            'interest_rate_changes': 4,
            'customer_behavior': 6,
            'vendor_reliability': 5
        }

        # Calculate risk scores
        assessed_factors = {}
        total_score = 0

        for factor in factors:
            # Find closest matching factor
            factor_lower = factor.lower().replace(' ', '_')
            score = 5  # Default medium risk

            for risk_factor, risk_score in risk_scores.items():
                if risk_factor in factor_lower or factor_lower in risk_factor:
                    score = risk_score
                    break

            assessed_factors[factor] = score
            total_score += score

        # Calculate overall risk level
        avg_score = total_score / len(factors) if factors else 5

        if avg_score >= 7:
            risk_level = 'High'
            mitigation_priority = 'Critical'
        elif avg_score >= 5:
            risk_level = 'Medium'
            mitigation_priority = 'Important'
        else:
            risk_level = 'Low'
            mitigation_priority = 'Monitor'

        # Generate mitigation suggestions
        mitigation_suggestions = []
        for factor, score in assessed_factors.items():
            if score >= 7:
                mitigation_suggestions.append(f"Immediate action needed for: {factor}")
            elif score >= 5:
                mitigation_suggestions.append(f"Develop contingency plan for: {factor}")

        assessment = {
            'factors_assessed': factors,
            'factor_scores': assessed_factors,
            'total_score': total_score,
            'average_score': round(avg_score, 2),
            'risk_level': risk_level,
            'mitigation_priority': mitigation_priority,
            'mitigation_suggestions': mitigation_suggestions[:5],  # Top 5
            'timestamp': datetime.now().isoformat()
        }

        return {
            'status': 'success',
            'report': f'Risk assessment complete: {risk_level} risk level (avg: {avg_score:.1f}/10)',
            'assessment': assessment
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Failed to assess risk: {str(e)}'
        }


async def save_strategy_report(
    problem: str,
    strategy: str,
    tool_context: ToolContext
) -> Dict[str, Any]:
    """
    Save strategic plan as an artifact.

    Args:
        problem: The business problem being solved
        strategy: The recommended strategy
        tool_context: ADK tool context

    Returns:
        Dict with save operation results
    """
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create markdown report
        report_content = f"""# Strategic Business Plan
Generated: {timestamp}

## Problem Statement
{problem}

## Recommended Strategy
{strategy}

## Analysis Tools Used
- Market Analysis
- ROI Calculations
- Risk Assessment

## Generated By
- Agent: Strategic Problem Solver
- Framework: Google ADK
- Model: Gemini 2.0 Flash
- Planners: BuiltInPlanner, PlanReActPlanner, StrategicPlanner
"""

        # In a real implementation, this would save to artifact service
        # For demo purposes, we'll simulate saving
        filename = f"strategy_{problem[:30].replace(' ', '_').replace('/', '_')}.md"

        # Store in tool context for demo purposes
        if not hasattr(tool_context, 'saved_reports'):
            tool_context.saved_reports = []

        tool_context.saved_reports.append({
            'filename': filename,
            'content': report_content,
            'timestamp': timestamp
        })

        return {
            'status': 'success',
            'report': f'Strategy saved as {filename}',
            'filename': filename,
            'content_length': len(report_content),
            'timestamp': timestamp
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Failed to save strategy report: {str(e)}'
        }


# ============================================================================
# CUSTOM PLANNER IMPLEMENTATION
# ============================================================================

class StrategicPlanner(BasePlanner):
    """
    Custom planner for strategic business problem solving.

    This planner implements a domain-specific workflow for business strategy:
    1. ANALYSIS: Gather market, financial, and risk data
    2. EVALUATION: Assess opportunities and threats
    3. STRATEGY: Develop comprehensive recommendations
    4. VALIDATION: Review and refine the strategy
    """

    def build_planning_instruction(
        self,
        readonly_context: ReadonlyContext,
        llm_request: LlmRequest,
    ) -> Optional[str]:
        """Build strategic planning instruction."""
        return """
You are a strategic business consultant using a systematic approach to solve complex problems.

Follow this structured methodology:

<ANALYSIS>
Gather comprehensive data about the business problem:
- Market conditions and trends
- Financial implications and ROI
- Risk factors and mitigation strategies
- Stakeholder impacts and requirements
Use available tools to collect objective data.

<EVALUATION>
Analyze the collected data:
- Identify key opportunities and threats
- Evaluate financial viability
- Assess risk levels and mitigation needs
- Consider strategic implications

<STRATEGY>
Develop a comprehensive business strategy:
- Define clear objectives and goals
- Outline specific action steps
- Address identified risks
- Include success metrics and timelines

<VALIDATION>
Review and validate the strategy:
- Ensure all aspects of the problem are addressed
- Verify financial and risk assumptions
- Confirm stakeholder alignment
- Identify potential implementation challenges

<FINAL_RECOMMENDATION>
Provide a complete strategic recommendation with:
- Executive summary
- Detailed implementation plan
- Risk mitigation strategies
- Success metrics and monitoring approach

Always use available tools to gather data before making recommendations.
Be data-driven and objective in your analysis.
"""

    def process_planning_response(
        self,
        callback_context: CallbackContext,
        response_parts: List[types.Part],
    ) -> Optional[List[types.Part]]:
        """Process strategic planning response."""
        # For this custom planner, we don't modify the response parts
        # but could add metadata or validation here if needed
        return response_parts


# ============================================================================
# AGENT IMPLEMENTATIONS
# ============================================================================

# BuiltInPlanner Agent - Uses Gemini's native thinking capabilities
builtin_planner_agent = Agent(
    name="builtin_planner_strategic_solver",
    model="gemini-2.0-flash",
    description="Strategic business consultant using BuiltInPlanner with transparent thinking",
    instruction="""You are an expert strategic consultant who thinks deeply before providing recommendations.

When solving business problems:
1. Use analyze_market to understand industry conditions
2. Use calculate_roi for financial analysis
3. Use assess_risk to evaluate potential threats
4. Use save_strategy_report to document your final recommendations

Think step-by-step about market opportunities, financial implications, and risk factors.
Provide data-driven recommendations with clear reasoning.
Always show your analytical process and assumptions.""",
    tools=[
        FunctionTool(analyze_market),
        FunctionTool(calculate_roi),
        FunctionTool(assess_risk),
        FunctionTool(save_strategy_report)
    ],
    planner=BuiltInPlanner(
        thinking_config=types.ThinkingConfig(include_thoughts=True)
    ),
    generate_content_config=types.GenerateContentConfig(
        temperature=0.3,  # Lower temperature for strategic thinking
        max_output_tokens=3000
    ),
    output_key="builtin_strategy_result"
)

# PlanReActPlanner Agent - Uses structured Plan → Reason → Act → Observe → Replan
plan_react_agent = Agent(
    name="plan_react_strategic_solver",
    model="gemini-2.0-flash",
    description="Strategic business consultant using PlanReActPlanner for structured reasoning",
    instruction="""You are a systematic strategic consultant who follows a structured problem-solving approach.

When analyzing business problems:
1. PLAN your analysis approach using available tools
2. REASON about market conditions, financials, and risks
3. ACT by using tools to gather specific data
4. OBSERVE results and adjust your understanding
5. REPLAN if your initial approach needs modification

Always use the structured format with planning tags.
Be thorough and methodical in your analysis.""",
    tools=[
        FunctionTool(analyze_market),
        FunctionTool(calculate_roi),
        FunctionTool(assess_risk),
        FunctionTool(save_strategy_report)
    ],
    planner=PlanReActPlanner(),
    generate_content_config=types.GenerateContentConfig(
        temperature=0.4,
        max_output_tokens=3000
    ),
    output_key="plan_react_strategy_result"
)

# Custom StrategicPlanner Agent - Domain-specific business strategy workflow
strategic_planner_agent = Agent(
    name="strategic_planner_solver",
    model="gemini-2.0-flash",
    description="Strategic business consultant using custom StrategicPlanner for domain-specific analysis",
    instruction="""You are a specialized business strategy consultant following a proven methodology.

Use the structured strategic planning framework:
- ANALYSIS: Gather market, financial, and risk data
- EVALUATION: Analyze opportunities and threats
- STRATEGY: Develop comprehensive recommendations
- VALIDATION: Review and refine your approach

Leverage all available tools to build data-driven strategies.
Focus on actionable recommendations with clear implementation steps.""",
    tools=[
        FunctionTool(analyze_market),
        FunctionTool(calculate_roi),
        FunctionTool(assess_risk),
        FunctionTool(save_strategy_report)
    ],
    planner=StrategicPlanner(),
    generate_content_config=types.GenerateContentConfig(
        temperature=0.3,
        max_output_tokens=3000
    ),
    output_key="strategic_planner_result"
)

# Default agent - showcases all planner types
# Uses PlanReActPlanner as default for most structured business problems
root_agent = plan_react_agent


# ============================================================================
# DEMO FUNCTIONS
# ============================================================================

async def demo_strategic_planning():
    """Demonstrate strategic planning with different planner types."""

    from google.adk.runners import InMemoryRunner

    problems = [
        "Should we expand into the Asian healthcare market?",
        "Is this $2M investment in AI technology worth the risk?",
        "How should we mitigate cybersecurity threats in our fintech startup?"
    ]

    agents = [
        ("BuiltInPlanner", builtin_planner_agent),
        ("PlanReActPlanner", plan_react_agent),
        ("StrategicPlanner", strategic_planner_agent)
    ]

    for problem in problems:
        print(f"\n{'='*80}")
        print(f"PROBLEM: {problem}")
        print(f"{'='*80}")

        for agent_name, agent in agents:
            print(f"\n--- {agent_name} Analysis ---")

            try:
                runner = InMemoryRunner(agent=agent, app_name=f"strategic_solver_{agent_name.lower()}")
                events = []
                async for event in runner.run_async(
                    user_id="demo_user",
                    session_id=f"demo_session_{agent_name.lower()}",
                    new_message={"role": "user", "parts": [{"text": problem}]}
                ):
                    events.append(event)
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if part.text:
                                print(part.text[:500] + "..." if len(part.text) > 500 else part.text)
                                break  # Only print first part
            except Exception as e:
                print(f"Error with {agent_name}: {e}")

        print(f"\n{'='*80}")


if __name__ == "__main__":
    # For direct execution
    import asyncio
    asyncio.run(demo_strategic_planning())


if __name__ == "__main__":
    # For direct execution
    import asyncio
    asyncio.run(demo_strategic_planning())