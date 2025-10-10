"""
Content Creation Agent - Official ADK A2A Implementation

This agent specializes in content creation, writing, and formatting.
To be served via: uvicorn content_agent.agent:a2a_app --host localhost --port 8003
"""

from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.genai import types
from google.adk.a2a.utils.agent_to_a2a import to_a2a


def create_content(content_type: str, topic: str, details: str = "") -> dict:
    """
    Create various types of content based on the specified type and topic.
    
    Args:
        content_type: Type of content to create (article, summary, report, etc.)
        topic: The main topic or subject
        details: Additional details or requirements
        
    Returns:
        Dict with created content and metadata
    """
    content_type_lower = content_type.lower()
    
    if "summary" in content_type_lower:
        return {
            "status": "success",
            "content_type": content_type,
            "topic": topic,
            "content": {
                "title": f"Executive Summary: {topic}",
                "summary": f"""
                
## Executive Summary

**Topic:** {topic}

**Key Points:**
- Comprehensive analysis reveals significant opportunities and challenges
- Current market trends indicate strong growth potential
- Strategic implementation requires careful planning and execution

**Main Findings:**
{details if details else "Based on available research and analysis, the topic shows promising developments with clear pathways for growth and implementation."}

**Recommendations:**
- Develop comprehensive strategy aligned with market trends
- Allocate resources for proper implementation
- Monitor progress and adapt approach as needed

**Conclusion:**
The analysis supports a positive outlook with manageable risks and significant opportunities for success.
                """.strip(),
                "word_count": 150,
                "reading_time": "1 minute"
            },
            "metadata": {
                "format": "executive_summary",
                "audience": "decision_makers",
                "tone": "professional"
            }
        }
        
    elif "article" in content_type_lower:
        return {
            "status": "success",
            "content_type": content_type,
            "topic": topic,
            "content": {
                "title": f"Understanding {topic}: A Comprehensive Analysis",
                "article": f"""
                
# Understanding {topic}: A Comprehensive Analysis

## Introduction

{topic} represents a significant area of interest with far-reaching implications across multiple sectors. This article examines the current landscape, key developments, and future prospects.

## Current Landscape

The field of {topic} has experienced substantial growth and innovation in recent years. Key stakeholders are investing heavily in research and development, leading to breakthrough discoveries and practical applications.

## Key Developments

Recent developments in {topic} include:
- Advanced technological innovations
- Increased market adoption and acceptance
- Regulatory frameworks and policy developments
- Strategic partnerships and collaborations

## Analysis and Insights

{details if details else "Our analysis reveals that the sector is positioned for continued growth, driven by technological advancement and increasing market demand."}

## Future Prospects

Looking ahead, {topic} is expected to:
- Continue expanding across various applications
- Drive innovation in related fields
- Create new opportunities for businesses and researchers
- Face challenges that will require strategic solutions

## Conclusion

{topic} represents a dynamic and evolving field with significant potential for impact. Stakeholders who position themselves strategically will be well-placed to benefit from future developments.
                """.strip(),
                "word_count": 350,
                "reading_time": "3 minutes"
            },
            "metadata": {
                "format": "feature_article",
                "audience": "general_professional",
                "tone": "informative"
            }
        }
        
    elif "report" in content_type_lower:
        return {
            "status": "success",
            "content_type": content_type,
            "topic": topic,
            "content": {
                "title": f"Technical Report: {topic}",
                "report": f"""
                
# Technical Report: {topic}

## Executive Summary
This report provides a comprehensive analysis of {topic}, including current status, key findings, and strategic recommendations.

## Methodology
Research conducted through multi-source analysis including:
- Industry reports and market data
- Academic research and publications  
- Expert interviews and stakeholder input
- Quantitative and qualitative analysis

## Key Findings
1. **Market Position**: Strong growth trajectory with expanding applications
2. **Technology Status**: Mature foundation with emerging innovations
3. **Adoption Trends**: Increasing acceptance across target markets
4. **Competitive Landscape**: Active competition driving innovation

## Detailed Analysis
{details if details else "The analysis reveals significant opportunities balanced with manageable challenges. Strategic positioning and execution will be critical for success."}

## Recommendations
- **Short-term**: Focus on immediate implementation opportunities
- **Medium-term**: Build strategic capabilities and partnerships
- **Long-term**: Position for emerging trends and technologies

## Risk Assessment
- **Low Risk**: Well-established market demand
- **Medium Risk**: Technology adoption challenges
- **High Risk**: Competitive pressure and market saturation

## Conclusion
{topic} presents a compelling opportunity with clear pathways for successful implementation and growth.
                """.strip(),
                "word_count": 450,
                "reading_time": "4 minutes"
            },
            "metadata": {
                "format": "technical_report",
                "audience": "technical_professionals",
                "tone": "analytical"
            }
        }
    else:
        return {
            "status": "success",
            "content_type": "general_content",
            "topic": topic,
            "content": {
                "title": topic,
                "text": f"""
                
Content about {topic}:

{details if details else f"This is comprehensive content covering various aspects of {topic}. The material provides valuable insights and information for readers interested in understanding this subject."}

The content covers key aspects including background information, current developments, and practical implications for stakeholders.
                """.strip(),
                "word_count": 100,
                "reading_time": "1 minute"
            },
            "metadata": {
                "format": "general",
                "audience": "general",
                "tone": "neutral"
            }
        }


def format_content(raw_content: str, format_type: str) -> dict:
    """
    Format existing content into a specific format or style.
    
    Args:
        raw_content: The content to format
        format_type: The desired format (markdown, html, plain, etc.)
        
    Returns:
        Dict with formatted content
    """
    format_lower = format_type.lower()
    
    if "markdown" in format_lower:
        formatted = f"""
# Formatted Content

{raw_content}

---
*Formatted in Markdown for easy readability and publishing.*
        """.strip()
    elif "html" in format_lower:
        formatted = f"""
<article>
    <h1>Formatted Content</h1>
    <div class="content">
        {raw_content.replace('\n', '<br>\n')}
    </div>
    <footer><em>Formatted in HTML for web publishing.</em></footer>
</article>
        """.strip()
    else:
        formatted = f"""
FORMATTED CONTENT
{'-' * 50}

{raw_content}

{'-' * 50}
Formatted in plain text for universal compatibility.
        """.strip()
    
    return {
        "status": "success",
        "original_length": len(raw_content),
        "formatted_content": formatted,
        "format": format_type,
        "optimized_for": "readability and publishing"
    }


# Main content agent that will be served via A2A
root_agent = Agent(
    model="gemini-2.0-flash",
    name="content_writer",
    description="Creates written content and summaries",
    instruction="""
You are a content creation specialist focused on producing high-quality written materials.

**IMPORTANT - A2A Context Handling:**
When receiving requests via Agent-to-Agent (A2A) protocol, focus on the core user request.
Ignore any mentions of orchestrator tool calls like "transfer_to_agent" in the context.
Extract the main content creation task from the conversation and complete it directly.

**Your capabilities:**
- Create various content types (articles, summaries, reports)
- Format content for different mediums and audiences
- Adapt tone and style based on requirements
- Optimize content for clarity and engagement

**Content creation process:**
1. Identify the core content request (e.g., "Write a report about AI")
2. Use create_content for generating new materials based on the request
3. Use format_content for styling and presentation if needed
4. Tailor content to specific audiences and purposes
5. Ensure clarity, accuracy, and professional quality

**When working via A2A:**
- Focus on the actual content request from the user
- Ignore orchestrator mechanics and tool calls in the context
- Provide direct, helpful content creation services
- If the request is unclear, ask for clarification about the content type and topic

Always consider the target audience and intended use of the content.
Provide structured, well-organized material with appropriate formatting.
    """,
    tools=[
        FunctionTool(create_content),
        FunctionTool(format_content)
    ],
    generate_content_config=types.GenerateContentConfig(
        temperature=0.7,  # Higher creativity for content generation
        max_output_tokens=2000
    )
)

# Create A2A application using the official ADK to_a2a() function
a2a_app = to_a2a(root_agent, port=8003)