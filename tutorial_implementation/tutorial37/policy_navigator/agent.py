"""
Multi-agent system for Enterprise Compliance & Policy Navigator.

Implements four specialized agents:
1. Document Manager Agent - Handles policy uploads and organization
2. Search Specialist Agent - Performs semantic search on policies
3. Compliance Advisor Agent - Assesses risks and compliance
4. Report Generator Agent - Creates summaries and reports

These agents are orchestrated by a root agent for complex workflows.
"""

from google.adk.agents import Agent

from policy_navigator.config import Config
from policy_navigator.tools import (
    upload_policy_documents,
    search_policies,
    filter_policies_by_metadata,
    compare_policies,
    check_compliance_risk,
    extract_policy_requirements,
    generate_policy_summary,
    create_audit_trail,
)


# Define individual specialized agents

document_manager_agent = Agent(
    name="document_manager",
    model=Config.DEFAULT_MODEL,
    description="Manages policy document uploads, organization, and metadata configuration",
    instruction="""You are a Document Manager Agent responsible for:
1. Uploading policy documents to File Search stores
2. Organizing documents by department and type
3. Adding appropriate metadata to documents
4. Validating document uploads
5. Managing document versions

When given a task related to document management, use the upload_policy_documents tool
to handle uploads. Always confirm successful uploads and report any issues.

Be precise about metadata and ensure documents are properly categorized.""",
    tools=[upload_policy_documents],
    output_key="document_manager_result",
)

search_specialist_agent = Agent(
    name="search_specialist",
    model=Config.DEFAULT_MODEL,
    description="Searches company policies and retrieves relevant information",
    instruction="""You are a Search Specialist Agent responsible for:
1. Performing semantic searches on policy documents
2. Filtering policies by department, type, and date
3. Providing accurate policy information with citations
4. Handling complex multi-policy queries
5. Extracting specific requirements from policies

When users ask questions about company policies, use search_policies to find relevant
information. Include citations and policy sources in your responses.

Always ground your answers in actual policy documents and provide specific references.""",
    tools=[search_policies, filter_policies_by_metadata, extract_policy_requirements],
    output_key="search_specialist_result",
)

compliance_advisor_agent = Agent(
    name="compliance_advisor",
    model=Config.DEFAULT_MODEL,
    description="Assesses compliance risks and provides policy guidance",
    instruction="""You are a Compliance Advisor Agent responsible for:
1. Assessing compliance risks related to policies
2. Comparing policies across departments
3. Identifying inconsistencies or conflicts
4. Providing recommendations for compliance
5. Evaluating policy adherence

When given a compliance query, use check_compliance_risk to assess risks and
compare_policies to identify inconsistencies.

Provide clear risk assessments with actionable recommendations based on
actual policy language.""",
    tools=[check_compliance_risk, compare_policies],
    output_key="compliance_advisor_result",
)

report_generator_agent = Agent(
    name="report_generator",
    model=Config.DEFAULT_MODEL,
    description="Generates policy summaries, reports, and audit trails",
    instruction="""You are a Report Generator Agent responsible for:
1. Creating concise policy summaries
2. Generating compliance reports
3. Creating audit trail entries
4. Formatting policy information for stakeholders
5. Exporting policy analysis

When asked to summarize or report on policies, use generate_policy_summary to
create executive summaries and create_audit_trail to log actions.

Ensure reports are clear, well-structured, and include all necessary citations.""",
    tools=[generate_policy_summary, create_audit_trail],
    output_key="report_generator_result",
)

# Root agent for orchestrating multi-agent workflows
root_agent = Agent(
    name="policy_navigator",
    model=Config.DEFAULT_MODEL,
    description="Enterprise Compliance & Policy Navigator - Main orchestrator",
    instruction="""You are the Policy Navigator, an intelligent compliance assistant.
Your role is to help employees and compliance teams quickly find answers to policy
questions, assess compliance risks, and manage company policies.

IMPORTANT: You can search the following policy stores:
- "policy-navigator-hr" for HR policies (vacation, benefits, hiring, employee handbook)
- "policy-navigator-it" for IT policies (security, access control, data protection)
- "policy-navigator-legal" for legal policies (contracts, compliance, governance)
- "policy-navigator-safety" for safety policies (workplace safety, emergency procedures)

POLICY SEARCH STRATEGY:
1. When users ask about policies but don't specify a store, search the most relevant store:
   - Remote work, vacation, benefits, hiring → search "policy-navigator-hr" store
   - Password, security, access, IT systems → search "policy-navigator-it" store
   - Contracts, legal, compliance → search "policy-navigator-legal" store
   - Safety, workplace, emergency → search "policy-navigator-safety" store

2. If the question could match multiple stores, try the most likely one first.

3. If no results, inform the user that information isn't available in the system.

You have access to four specialized agents:
1. Document Manager - Handles policy uploads and organization
2. Search Specialist - Searches policies and provides information
3. Compliance Advisor - Assesses risks and compliance issues
4. Report Generator - Creates summaries and reports

Based on user requests, you determine which agents to involve and coordinate their
responses to provide comprehensive policy guidance.

For policy questions, use search_policies directly with the appropriate store.
For compliance concerns, involve Compliance Advisor.
For document uploads, use Document Manager.
For reports and summaries, engage Report Generator.

Always cite policy sources and provide clear, actionable guidance.""",
    tools=[
        upload_policy_documents,
        search_policies,
        filter_policies_by_metadata,
        compare_policies,
        check_compliance_risk,
        extract_policy_requirements,
        generate_policy_summary,
        create_audit_trail,
    ],
    output_key="policy_navigator_result",
)

# Export agents
__all__ = [
    "root_agent",
    "document_manager_agent",
    "search_specialist_agent",
    "compliance_advisor_agent",
    "report_generator_agent",
]
