"""
Research Agent - Official ADK A2A Implementation

This agent specializes in web research, fact-checking, and information gathering.
To be served via: uvicorn research_agent.agent:a2a_app --host localhost --port 8001
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.genai import types
from google.adk.a2a.utils.agent_to_a2a import to_a2a


def research_topic(topic: str) -> dict:
    """
    Research a specific topic and provide detailed findings.
    
    Args:
        topic: The topic to research
        
    Returns:
        Dict with research findings, sources, and analysis
    """
    # Simulate comprehensive research process
    topic_lower = topic.lower()
    
    if "quantum" in topic_lower:
        return {
            "status": "success",
            "topic": topic,
            "findings": {
                "overview": "Quantum computing represents a paradigm shift in computational capabilities",
                "current_trends": [
                    "Major tech companies have operational quantum computers",
                    "Error correction progress enabling practical applications", 
                    "Hybrid quantum-classical algorithms showing promise"
                ],
                "key_developments": [
                    "Google achieved quantum supremacy in 2019",
                    "IBM's quantum network has over 200 members",
                    "Microsoft's Azure Quantum cloud platform launched"
                ],
                "challenges": [
                    "Quantum decoherence and error rates",
                    "Limited qubit stability and connectivity",
                    "Need for extreme cooling requirements"
                ]
            },
            "sources": [
                "Nature: Quantum computing progress and challenges (2024)",
                "MIT Technology Review: Quantum advantage roadmap",
                "Google AI Research: Quantum error correction breakthroughs"
            ],
            "confidence": "high",
            "last_updated": "2024"
        }
        
    elif "ai" in topic_lower or "artificial intelligence" in topic_lower:
        return {
            "status": "success", 
            "topic": topic,
            "findings": {
                "overview": "AI adoption is accelerating across industries with transformative impact",
                "current_trends": [
                    "Generative AI market projected to reach $1.3T by 2030",
                    "Enterprise AI spending increased 30% year-over-year",
                    "Foundation models becoming more accessible and specialized"
                ],
                "key_developments": [
                    "Large Language Models (LLMs) achieving human-level performance",
                    "Multimodal AI systems integrating text, image, and audio",
                    "AI agents and autonomous systems deployment"
                ],
                "applications": [
                    "Healthcare: Drug discovery and diagnostic assistance",
                    "Finance: Algorithmic trading and risk assessment", 
                    "Education: Personalized learning and tutoring systems"
                ]
            },
            "sources": [
                "McKinsey Global AI Survey 2024",
                "Stanford AI Index Annual Report 2024",
                "Gartner AI Market Forecast and Trends"
            ],
            "confidence": "high",
            "last_updated": "2024"
        }
        
    elif topic:
        return {
            "status": "success",
            "topic": topic,
            "findings": {
                "overview": f"Research analysis for: {topic}",
                "current_trends": [
                    "Significant growth and innovation in the field",
                    "Increasing adoption across various sectors",
                    "Emerging technologies driving transformation"
                ],
                "key_insights": [
                    "Market expansion and investment opportunities",
                    "Technological advancements and breakthroughs",
                    "Regulatory developments and policy changes"
                ]
            },
            "sources": [
                "Industry Research Reports 2024",
                "Academic Publications and Studies",
                "Market Analysis and Expert Opinions"
            ],
            "confidence": "medium",
            "last_updated": "2024"
        }
    else:
        return {
            "status": "error",
            "message": "Please provide a specific topic to research",
            "suggestions": ["quantum computing", "artificial intelligence", "blockchain", "renewable energy"]
        }


def fact_check(claim: str) -> dict:
    """
    Fact-check a specific claim or statement.
    
    Args:
        claim: The claim to verify
        
    Returns:
        Dict with verification results and sources
    """
    return {
        "status": "success",
        "claim": claim,
        "verification": {
            "accuracy": "requires_verification",
            "confidence": "medium",
            "methodology": "Cross-reference with authoritative sources",
            "notes": f"Fact-checking analysis for: {claim}"
        },
        "sources_checked": [
            "Academic databases and peer-reviewed journals",
            "Government and institutional reports",
            "Reputable news organizations and fact-checkers"
        ],
        "recommendation": "Further verification recommended with primary sources"
    }


# Main research agent that will be served via A2A
root_agent = Agent(
    model="gemini-2.0-flash",
    name="research_specialist", 
    description="Conducts web research and fact-checking",
    instruction="""
You are a research specialist focused on gathering, analyzing, and verifying information.

**IMPORTANT - A2A Context Handling:**
When receiving requests via Agent-to-Agent (A2A) protocol, focus on the core user request.
Ignore any mentions of orchestrator tool calls like "transfer_to_agent" in the context.
Extract the main research task from the conversation and complete it directly.

**Your capabilities:**
- Comprehensive topic research with detailed findings
- Fact-checking and verification of claims
- Source citation and credibility assessment
- Current trends and market analysis

**Research process:**
1. Identify the core research request from the user (e.g., "research AI trends")
2. Use research_topic for comprehensive topic analysis
3. Use fact_check for verifying specific claims
4. Provide detailed findings with sources and confidence levels
5. Focus on accuracy, recency, and relevance

**When working via A2A:**
- Focus on the actual research request from the user
- Ignore orchestrator mechanics and tool calls in the context
- Provide direct, helpful research services
- If the request is unclear, ask for clarification about what to research

Always provide sources and indicate confidence levels in your findings.
Format responses clearly with structured information.
    """,
    tools=[
        FunctionTool(research_topic),
        FunctionTool(fact_check)
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.3,  # Lower temperature for more focused research
        max_output_tokens=1500
    )
)

# Create A2A application using the official ADK to_a2a() function
a2a_app = to_a2a(root_agent, port=8001)