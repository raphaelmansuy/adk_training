# Tutorial 34: Document Processing Agent with Sub-Agents
# Uses multiple specialized agents (as tools) for different document types
# Each agent enforces JSON output using Pydantic output schemas

from __future__ import annotations

from pydantic import BaseModel, Field
from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool


# ============================================================================
# Structured Output Schemas (Pydantic Models)
# ============================================================================

class EntityExtraction(BaseModel):
    """Extracted entities from document content."""
    
    dates: list[str] = Field(
        default_factory=list,
        description="List of dates found in the document (e.g., 2024-10-08)"
    )
    currency_amounts: list[str] = Field(
        default_factory=list,
        description="Currency values found (e.g., $1,200.50)"
    )
    percentages: list[str] = Field(
        default_factory=list,
        description="Percentage values found (e.g., 35%)"
    )
    numbers: list[str] = Field(
        default_factory=list,
        description="Significant numbers found in the document"
    )


class DocumentSummary(BaseModel):
    """Concise summary of document content."""
    
    main_points: list[str] = Field(
        description="Top 3-5 main points from the document"
    )
    key_insight: str = Field(
        description="The most important takeaway from the document"
    )
    summary: str = Field(
        description="A 1-2 sentence summary of the entire document"
    )


# ============================================================================
# Document Type-Specific Output Schemas
# ============================================================================

class FinancialAnalysisOutput(BaseModel):
    """Structured output for financial document analysis."""
    
    summary: DocumentSummary
    entities: EntityExtraction
    financial_metrics: dict = Field(
        description="Key financial metrics (revenue, profit, margins, etc.)"
    )
    fiscal_periods: list[str] = Field(
        default_factory=list,
        description="Fiscal periods mentioned (quarters, years)"
    )
    recommendations: list[str] = Field(
        default_factory=list,
        description="Financial recommendations"
    )


class TechnicalAnalysisOutput(BaseModel):
    """Structured output for technical document analysis."""
    
    summary: DocumentSummary
    entities: EntityExtraction
    technologies: list[str] = Field(
        description="Technologies and frameworks mentioned"
    )
    components: list[str] = Field(
        description="System components or services discussed"
    )
    recommendations: list[str] = Field(
        default_factory=list,
        description="Technical recommendations"
    )


class SalesAnalysisOutput(BaseModel):
    """Structured output for sales document analysis."""
    
    summary: DocumentSummary
    entities: EntityExtraction
    deals: list[dict] = Field(
        default_factory=list,
        description="Deal information (customer, value, stage)"
    )
    pipeline_value: str = Field(
        default="",
        description="Total pipeline value"
    )
    recommendations: list[str] = Field(
        default_factory=list,
        description="Sales recommendations"
    )


class MarketingAnalysisOutput(BaseModel):
    """Structured output for marketing document analysis."""
    
    summary: DocumentSummary
    entities: EntityExtraction
    campaigns: list[str] = Field(
        default_factory=list,
        description="Marketing campaigns mentioned"
    )
    metrics: dict = Field(
        description="Marketing metrics (engagement, conversion, reach)"
    )
    recommendations: list[str] = Field(
        default_factory=list,
        description="Marketing recommendations"
    )


# ============================================================================
# Sub-Agents for Each Document Type (Using JSON Output Enforcement)
# ============================================================================

financial_agent = LlmAgent(
    name="financial_analyzer",
    model="gemini-2.5-flash",
    description="Analyzes financial documents and reports",
    instruction=(
        "You are an expert financial analyst. Analyze the provided financial document "
        "and extract all relevant information including metrics, periods, and recommendations. "
        "Return results in valid JSON format matching the specified schema."
    ),
    output_schema=FinancialAnalysisOutput,
)

technical_agent = LlmAgent(
    name="technical_analyzer",
    model="gemini-2.5-flash",
    description="Analyzes technical documents and specifications",
    instruction=(
        "You are an expert technical analyst. Analyze the provided technical document "
        "and extract technologies, components, and technical recommendations. "
        "Return results in valid JSON format matching the specified schema."
    ),
    output_schema=TechnicalAnalysisOutput,
)

sales_agent = LlmAgent(
    name="sales_analyzer",
    model="gemini-2.5-flash",
    description="Analyzes sales documents and pipeline information",
    instruction=(
        "You are an expert sales analyst. Analyze the provided sales document "
        "and extract deal information, pipeline value, and sales recommendations. "
        "Return results in valid JSON format matching the specified schema."
    ),
    output_schema=SalesAnalysisOutput,
)

marketing_agent = LlmAgent(
    name="marketing_analyzer",
    model="gemini-2.5-flash",
    description="Analyzes marketing documents and campaign information",
    instruction=(
        "You are an expert marketing analyst. Analyze the provided marketing document "
        "and extract campaign information, metrics, and marketing recommendations. "
        "Return results in valid JSON format matching the specified schema."
    ),
    output_schema=MarketingAnalysisOutput,
)


# ============================================================================
# Wrap Sub-Agents as Tools for the Coordinator Agent
# ============================================================================

financial_tool = AgentTool(financial_agent)
technical_tool = AgentTool(technical_agent)
sales_tool = AgentTool(sales_agent)
marketing_tool = AgentTool(marketing_agent)


# ============================================================================
# Root Coordinator Agent
# ============================================================================

root_agent = LlmAgent(
    name="pubsub_processor",
    model="gemini-2.5-flash",
    description="Event-driven document processing coordinator that routes to specialized analyzers",
    instruction=(
        "You are a document routing and coordination agent for event-driven processing pipelines. "
        "Your role is to:\n"
        "1. Analyze the incoming document to determine its type\n"
        "2. Route it to the appropriate specialized analyzer\n"
        "3. Return the structured analysis results\n\n"
        
        "Document types and routing:\n"
        "- FINANCIAL: Use financial_analyzer for financial reports, earnings, budgets\n"
        "- TECHNICAL: Use technical_analyzer for specs, architecture, deployment docs\n"
        "- SALES: Use sales_analyzer for pipeline, deals, forecasts, contracts\n"
        "- MARKETING: Use marketing_analyzer for campaigns, engagement, strategy\n\n"
        
        "Guidelines:\n"
        "- Always identify the primary document type first\n"
        "- Route to the most appropriate analyzer\n"
        "- Ensure all extracted information is accurate and complete\n"
        "- Return the JSON structured output from the selected analyzer\n\n"
        
        "Decision framework:\n"
        "- Look for financial keywords (revenue, profit, budget, fiscal, quarterly, earnings)\n"
        "- Look for technical keywords (API, deployment, database, configuration, architecture)\n"
        "- Look for sales keywords (deal, pipeline, customer, forecast, contract, closed)\n"
        "- Look for marketing keywords (campaign, engagement, conversion, reach, audience)\n"
    ),
    tools=[financial_tool, technical_tool, sales_tool, marketing_tool],
)
