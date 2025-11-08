"""
Policy Navigator - Enterprise Compliance & Policy Navigator
Tutorial 37: Google ADK with Gemini File Search API

A production-ready multi-agent system for searching and analyzing company policies
using Google's Gemini File Search API for native Retrieval Augmented Generation (RAG).
"""

__version__ = "0.1.0"
__author__ = "Google ADK Training"
__description__ = "Enterprise Compliance & Policy Navigator using Gemini File Search"

from policy_navigator.agent import root_agent
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
from policy_navigator.stores import (
    create_policy_store,
    get_store_info,
    list_stores,
    delete_store,
)

__all__ = [
    "root_agent",
    "upload_policy_documents",
    "search_policies",
    "filter_policies_by_metadata",
    "compare_policies",
    "check_compliance_risk",
    "extract_policy_requirements",
    "generate_policy_summary",
    "create_audit_trail",
    "create_policy_store",
    "get_store_info",
    "list_stores",
    "delete_store",
]
