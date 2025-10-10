"""
Data Analysis Agent - Official ADK A2A Implementation

This agent specializes in data analysis, statistics, and generating insights.
To be served via: uvicorn analysis_agent.agent:a2a_app --host localhost --port 8002
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.genai import types
from google.adk.a2a.utils.agent_to_a2a import to_a2a


def analyze_data(data_description: str) -> dict:
    """
    Analyze data and generate insights and recommendations.
    
    Args:
        data_description: Description of the data to analyze
        
    Returns:
        Dict with analysis results, insights, and recommendations
    """
    data_lower = data_description.lower()
    
    if "quantum" in data_lower:
        return {
            "status": "success",
            "data_analyzed": data_description,
            "analysis": {
                "key_metrics": {
                    "market_size": "$1.3B (2024) → $5.3B (2029)",
                    "growth_rate": "32.1% CAGR",
                    "investment_total": "$2.4B in 2024"
                },
                "trends": [
                    "Exponential growth in quantum computing investments",
                    "Government initiatives driving public sector adoption",
                    "Hardware improvements reducing error rates"
                ],
                "patterns": [
                    "Tech giants dominating quantum research (Google, IBM, Microsoft)",
                    "Increasing collaboration between academia and industry",
                    "Focus shifting from research to practical applications"
                ]
            },
            "insights": [
                "Quantum advantage expected in optimization and simulation by 2026",
                "Financial services and drug discovery are early adoption areas",
                "Talent shortage is a significant bottleneck for growth"
            ],
            "recommendations": [
                "Invest in quantum-safe cryptography now",
                "Explore hybrid quantum-classical algorithms",
                "Build quantum computing expertise and partnerships"
            ],
            "confidence": "high"
        }
        
    elif "ai" in data_lower or "artificial intelligence" in data_lower:
        return {
            "status": "success",
            "data_analyzed": data_description,
            "analysis": {
                "key_metrics": {
                    "market_size": "$136.6B (2024) → $826.7B (2030)",
                    "growth_rate": "37.3% CAGR",
                    "enterprise_adoption": "72% of companies"
                },
                "trends": [
                    "Generative AI driving massive market expansion",
                    "Multimodal AI systems gaining traction",
                    "Edge AI deployment increasing for real-time processing"
                ],
                "patterns": [
                    "Cloud providers offering AI-as-a-Service platforms",
                    "Open-source models democratizing AI access",
                    "Regulatory frameworks emerging globally"
                ]
            },
            "insights": [
                "AI productivity gains averaging 20-30% across industries",
                "Skills gap widening between AI capabilities and workforce",
                "Ethical AI and explainability becoming competitive advantages"
            ],
            "recommendations": [
                "Develop AI governance and ethics frameworks",
                "Invest in employee AI literacy and training",
                "Focus on human-AI collaboration workflows"
            ],
            "confidence": "high"
        }
        
    elif data_description:
        return {
            "status": "success",
            "data_analyzed": data_description,
            "analysis": {
                "key_metrics": {
                    "data_quality": "Analysis in progress",
                    "sample_size": "Determining significance",
                    "variables": "Identifying key factors"
                },
                "trends": [
                    "Identifying temporal patterns in the data",
                    "Analyzing correlation and causation relationships",
                    "Detecting outliers and anomalies"
                ],
                "patterns": [
                    "Statistical patterns and distributions",
                    "Seasonal or cyclical behaviors",
                    "Growth trajectories and inflection points"
                ]
            },
            "insights": [
                "Data reveals interesting behavioral patterns",
                "Multiple factors appear to influence outcomes",
                "Further analysis recommended for deeper insights"
            ],
            "recommendations": [
                "Collect additional data points for validation",
                "Consider external factors and variables",
                "Implement continuous monitoring and analysis"
            ],
            "confidence": "medium"
        }
    else:
        return {
            "status": "error",
            "message": "Please provide data description for analysis",
            "available_analyses": [
                "Market trend analysis",
                "Performance metrics evaluation",
                "Statistical pattern recognition",
                "Predictive modeling insights"
            ]
        }


def generate_insights(topic: str) -> dict:
    """
    Generate strategic insights and recommendations for a topic.
    
    Args:
        topic: The topic to generate insights for
        
    Returns:
        Dict with strategic insights and actionable recommendations
    """
    return {
        "status": "success",
        "topic": topic,
        "strategic_insights": {
            "opportunities": [
                f"Market opportunities in {topic}",
                "Technology adoption potential",
                "Competitive advantage possibilities"
            ],
            "challenges": [
                "Implementation complexity",
                "Resource requirements", 
                "Market acceptance factors"
            ],
            "recommendations": [
                "Develop phased implementation strategy",
                "Build partnerships for capability enhancement",
                "Monitor market trends and adjust approach"
            ]
        },
        "risk_assessment": "Medium - manageable with proper planning",
        "success_probability": "High with strategic execution"
    }


# Main analysis agent that will be served via A2A
root_agent = Agent(
    model="gemini-2.0-flash",
    name="data_analyst",
    description="Analyzes data and generates insights",
    instruction="""
You are a data analysis specialist focused on extracting insights from information and data.

**IMPORTANT - A2A Context Handling:**
When receiving requests via Agent-to-Agent (A2A) protocol, focus on the core user request.
Ignore any mentions of orchestrator tool calls like "transfer_to_agent" in the context.
Extract the main analysis task from the conversation and complete it directly.

**Your capabilities:**
- Comprehensive data analysis with statistical insights
- Trend identification and pattern recognition
- Strategic recommendations and actionable insights
- Risk assessment and opportunity analysis

**Analysis process:**
1. Identify the core analysis request from the user (e.g., "analyze AI trends")
2. Use analyze_data for comprehensive data examination
3. Use generate_insights for strategic recommendations
4. Provide quantitative metrics and qualitative insights
5. Focus on actionable recommendations and next steps

**When working via A2A:**
- Focus on the actual analysis request from the user
- Ignore orchestrator mechanics and tool calls in the context
- Provide direct, helpful analytical services
- If the request is unclear, ask for clarification about what to analyze

Always provide confidence levels and explain your analytical methodology.
Structure responses with clear metrics, trends, and recommendations.
    """,
    tools=[
        FunctionTool(analyze_data),
        FunctionTool(generate_insights)
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.4,  # Balanced for analytical thinking
        max_output_tokens=1500
    )
)

# Create A2A application using the official ADK to_a2a() function
a2a_app = to_a2a(root_agent, port=8002)