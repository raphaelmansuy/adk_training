"""
Core tools for Policy Navigator.

Implements File Search integration tools for uploading, searching,
filtering, analyzing, and reporting on policy documents.
"""

import os
from typing import Any, Dict, List, Optional
from google import genai
from google.genai import types
from loguru import logger

from policy_navigator.config import Config
from policy_navigator.metadata import MetadataSchema
from policy_navigator.stores import StoreManager


class PolicyTools:
    """Collection of tools for policy management and analysis."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize PolicyTools.

        Args:
            api_key: Google API key (uses Config.GOOGLE_API_KEY if not provided)
        """
        self.api_key = api_key or Config.GOOGLE_API_KEY
        self.client = genai.Client(api_key=self.api_key)
        self.store_manager = StoreManager(api_key)

    def upload_policy_documents(
        self,
        file_paths: str,
        store_name: str,
    ) -> Dict[str, Any]:
        """
        Upload policy documents to File Search Store with upsert semantics.

        If a document with the same name already exists, it will be replaced.

        Args:
            file_paths: Comma-separated file paths to upload
            store_name: Target File Search Store name

        Returns:
            dict with status, uploaded count, and details
        """
        # Parse comma-separated file paths
        paths = [p.strip() for p in file_paths.split(",")]
        try:
            logger.info(f"Uploading {len(paths)} documents to {store_name}...")

            uploaded = 0
            failed = 0
            details = []

            for file_path in paths:
                if not os.path.exists(file_path):
                    logger.error(f"File not found: {file_path}")
                    failed += 1
                    details.append({"file": file_path, "status": "error", "reason": "File not found"})
                    continue

                try:
                    display_name = os.path.basename(file_path)

                    # Use upsert instead of upload to replace existing documents
                    if self.store_manager.upsert_file_to_store(
                        file_path, store_name, display_name, None
                    ):
                        uploaded += 1
                        details.append(
                            {"file": file_path, "status": "success", "mode": "upsert"}
                        )
                    else:
                        failed += 1
                        details.append(
                            {"file": file_path, "status": "error", "reason": "Upsert failed"}
                        )

                except Exception as e:
                    logger.error(f"Failed to upsert {file_path}: {str(e)}")
                    failed += 1
                    details.append(
                        {"file": file_path, "status": "error", "reason": str(e)}
                    )

            return {
                "status": "success" if uploaded > 0 else "error",
                "uploaded": uploaded,
                "failed": failed,
                "total": len(paths),
                "details": details,
                "report": f"Upserted {uploaded}/{len(paths)} documents successfully",
            }

        except Exception as e:
            logger.error(f"Upload failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "report": f"Failed to upload documents: {str(e)}",
            }

    def search_policies(
        self,
        query: str,
        store_name: str,
        metadata_filter: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Search policies using semantic search with File Search.

        Args:
            query: Search query (user question about policies)
            store_name: File Search Store display name or full name
            metadata_filter: Optional AIP-160 metadata filter

        Returns:
            dict with answer, citations, and metadata
        """
        try:
            logger.info(f"Searching policies: {query}")

            # Resolve store name if it's a display name
            full_store_name = store_name
            if not store_name.startswith("fileSearchStores/"):
                resolved_name = self.store_manager.get_store_by_display_name(store_name)
                if not resolved_name:
                    return {
                        "status": "error",
                        "error": f"File Search store '{store_name}' not found",
                        "report": f"Store '{store_name}' not found. Create it first using demo_upload.py",
                    }
                full_store_name = resolved_name

            # Build File Search tool config
            file_search_tool_config = {
                "file_search_store_names": [full_store_name]
            }
            if metadata_filter:
                file_search_tool_config["metadata_filter"] = metadata_filter

            # Execute search
            try:
                response = self.client.models.generate_content(
                    model=Config.DEFAULT_MODEL,
                    contents=query,
                    config=types.GenerateContentConfig(
                        tools=[{
                            "file_search": file_search_tool_config
                        }]
                    ),
                )
            except Exception as e:
                # If File Search stores don't exist, provide helpful message
                if "not found" in str(e).lower() or "fileSearchStore" in str(e):
                    logger.warning(f"File Search store '{store_name}' not found. Create it first using: client.file_search_stores.create()")
                raise

            # Extract citations
            citations = []
            grounding = response.candidates[0].grounding_metadata if response.candidates else None

            if grounding and hasattr(grounding, "grounding_chunks"):
                for chunk in grounding.grounding_chunks:
                    citations.append({
                        "source": str(chunk),
                        "text": getattr(chunk, "text", "")[:200] + "..."
                    })

            return {
                "status": "success",
                "answer": response.text,
                "citations": citations,
                "source_count": len(citations),
                "report": f"Found answer with {len(citations)} source(s)",
            }

        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "report": f"Search failed: {str(e)}",
            }

    def filter_policies_by_metadata(
        self,
        store_name: str,
        department: Optional[str] = None,
        policy_type: Optional[str] = None,
        sensitivity: Optional[str] = None,
        jurisdiction: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Filter policies by metadata attributes.

        Args:
            store_name: File Search Store display name or full name
            department: Filter by department (HR, IT, Legal, Safety)
            policy_type: Filter by policy type (handbook, procedure, etc.)
            sensitivity: Filter by sensitivity (public, internal, confidential)
            jurisdiction: Filter by jurisdiction (US, EU, etc.)

        Returns:
            dict with filtered policy query and filter used
        """
        try:
            # Resolve store name if it's a display name
            full_store_name = store_name
            if not store_name.startswith("fileSearchStores/"):
                resolved_name = self.store_manager.get_store_by_display_name(store_name)
                if not resolved_name:
                    return {
                        "status": "error",
                        "error": f"File Search store '{store_name}' not found",
                        "report": f"Store '{store_name}' not found. Create it first using demo_upload.py",
                    }
                full_store_name = resolved_name

            metadata_filter = MetadataSchema.build_metadata_filter(
                department=department,
                policy_type=policy_type,
                sensitivity=sensitivity,
                jurisdiction=jurisdiction,
            )

            logger.info(f"Filtering policies with: {metadata_filter}")

            # Execute filtered search
            query = f"Show me all {policy_type or 'policies'} from {department or 'all departments'}"
            response = self.client.models.generate_content(
                model=Config.DEFAULT_MODEL,
                contents=query,
                config=types.GenerateContentConfig(
                    tools=[{
                        "file_search": {
                            "file_search_store_names": [full_store_name],
                            **({"metadata_filter": metadata_filter} if metadata_filter else {})
                        }
                    }]
                ),
            )

            return {
                "status": "success",
                "query": query,
                "filter": metadata_filter,
                "results": response.text,
                "report": "Filtered policies retrieved successfully",
            }

        except Exception as e:
            logger.error(f"Filtering failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "report": f"Filtering failed: {str(e)}",
            }

    def compare_policies(
        self,
        query: str,
        store_names: List[str],
    ) -> Dict[str, Any]:
        """
        Compare policies across multiple documents or stores.

        Args:
            query: Comparison query (e.g., "Compare vacation policies")
            store_names: List of File Search Store display names or full names

        Returns:
            dict with comparison results and analysis
        """
        try:
            logger.info(f"Comparing policies: {query}")

            # Resolve all store names
            full_store_names = []
            for store_name in store_names:
                if store_name.startswith("fileSearchStores/"):
                    full_store_names.append(store_name)
                else:
                    resolved_name = self.store_manager.get_store_by_display_name(store_name)
                    if not resolved_name:
                        return {
                            "status": "error",
                            "error": f"File Search store '{store_name}' not found",
                            "report": f"Store '{store_name}' not found. Create it first using demo_upload.py",
                        }
                    full_store_names.append(resolved_name)

            response = self.client.models.generate_content(
                model=Config.DEFAULT_MODEL,
                contents=query,
                config=types.GenerateContentConfig(
                    tools=[{
                        "file_search": {
                            "file_search_store_names": full_store_names
                        }
                    }]
                ),
            )

            return {
                "status": "success",
                "query": query,
                "comparison": response.text,
                "stores_compared": len(store_names),
                "report": "Policy comparison completed successfully",
            }

        except Exception as e:
            logger.error(f"Comparison failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "report": f"Comparison failed: {str(e)}",
            }

    def check_compliance_risk(
        self,
        query: str,
        store_name: str,
    ) -> Dict[str, Any]:
        """
        Check compliance and assess risks based on policies.

        Args:
            query: Risk assessment query
            store_name: File Search Store display name or full name

        Returns:
            dict with risk assessment and recommendations
        """
        try:
            logger.info(f"Assessing compliance risk: {query}")

            # Resolve store name if it's a display name
            full_store_name = store_name
            if not store_name.startswith("fileSearchStores/"):
                resolved_name = self.store_manager.get_store_by_display_name(store_name)
                if not resolved_name:
                    return {
                        "status": "error",
                        "error": f"File Search store '{store_name}' not found",
                        "report": f"Store '{store_name}' not found. Create it first using demo_upload.py",
                    }
                full_store_name = resolved_name

            # Add compliance context to query
            compliance_query = f"""
            Based on company policies, assess the following compliance question:
            {query}
            
            Provide:
            1. Direct policy answer
            2. Risk level (Low/Medium/High)
            3. Specific policy references
            4. Recommendations for compliance
            """

            response = self.client.models.generate_content(
                model=Config.DEFAULT_MODEL,
                contents=compliance_query,
                config=types.GenerateContentConfig(
                    tools=[{
                        "file_search": {
                            "file_search_store_names": [full_store_name]
                        }
                    }]
                ),
            )

            return {
                "status": "success",
                "query": query,
                "assessment": response.text,
                "report": "Compliance risk assessment completed",
            }

        except Exception as e:
            logger.error(f"Risk assessment failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "report": f"Risk assessment failed: {str(e)}",
            }

    def extract_policy_requirements(
        self,
        query: str,
        store_name: str,
    ) -> Dict[str, Any]:
        """
        Extract specific requirements from policies.

        Args:
            query: Query for specific requirements (e.g., "password requirements")
            store_name: File Search Store display name or full name

        Returns:
            dict with extracted requirements in structured format
        """
        try:
            logger.info(f"Extracting requirements: {query}")

            # Resolve store name if it's a display name
            full_store_name = store_name
            if not store_name.startswith("fileSearchStores/"):
                resolved_name = self.store_manager.get_store_by_display_name(store_name)
                if not resolved_name:
                    return {
                        "status": "error",
                        "error": f"File Search store '{store_name}' not found",
                        "report": f"Store '{store_name}' not found. Create it first using demo_upload.py",
                    }
                full_store_name = resolved_name

            extraction_query = f"""
            Extract the specific requirements for: {query}
            
            Format as a structured list with:
            - Requirement description
            - Policy source
            - Enforcement mechanism
            - Exceptions (if any)
            """

            response = self.client.models.generate_content(
                model=Config.DEFAULT_MODEL,
                contents=extraction_query,
                config=types.GenerateContentConfig(
                    tools=[{
                        "file_search": {
                            "file_search_store_names": [full_store_name]
                        }
                    }]
                ),
            )

            return {
                "status": "success",
                "query": query,
                "requirements": response.text,
                "report": "Requirements extracted successfully",
            }

        except Exception as e:
            logger.error(f"Extraction failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "report": f"Extraction failed: {str(e)}",
            }

    def generate_policy_summary(
        self,
        query: str,
        store_name: str,
    ) -> Dict[str, Any]:
        """
        Generate a summary of policy information.

        Args:
            query: Topic to summarize (e.g., "remote work benefits")
            store_name: File Search Store display name or full name

        Returns:
            dict with summary and key points
        """
        try:
            logger.info(f"Generating summary: {query}")

            # Resolve store name if it's a display name
            full_store_name = store_name
            if not store_name.startswith("fileSearchStores/"):
                resolved_name = self.store_manager.get_store_by_display_name(store_name)
                if not resolved_name:
                    return {
                        "status": "error",
                        "error": f"File Search store '{store_name}' not found",
                        "report": f"Store '{store_name}' not found. Create it first using demo_upload.py",
                    }
                full_store_name = resolved_name

            summary_query = f"""
            Create a concise summary of: {query}
            
            Include:
            1. Key points (3-5 bullets)
            2. Who it applies to
            3. Process or requirements
            4. Important notes
            
            Keep it brief and actionable.
            """

            response = self.client.models.generate_content(
                model=Config.DEFAULT_MODEL,
                contents=summary_query,
                config=types.GenerateContentConfig(
                    tools=[{
                        "file_search": {
                            "file_search_store_names": [full_store_name]
                        }
                    }]
                ),
            )

            return {
                "status": "success",
                "query": query,
                "summary": response.text,
                "report": "Summary generated successfully",
            }

        except Exception as e:
            logger.error(f"Summary generation failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "report": f"Summary generation failed: {str(e)}",
            }

    def create_audit_trail(
        self,
        action: str,
        user: str,
        query: str,
        result_summary: str,
    ) -> Dict[str, Any]:
        """
        Create an audit trail entry for policy access.

        Args:
            action: Type of action (search, upload, update)
            user: User performing the action
            query: Query or action details
            result_summary: Summary of the result

        Returns:
            dict with audit trail entry
        """
        try:
            from datetime import datetime

            audit_entry = {
                "timestamp": datetime.now().isoformat(),
                "action": action,
                "user": user,
                "query": query,
                "result_summary": result_summary,
                "status": "logged",
            }

            logger.info(f"Audit trail created: {action} by {user}")

            return {
                "status": "success",
                "audit_entry": audit_entry,
                "report": "Audit trail entry created",
            }

        except Exception as e:
            logger.error(f"Audit trail creation failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "report": f"Audit trail creation failed: {str(e)}",
            }


# Global instance
_policy_tools: Optional[PolicyTools] = None


def _get_tools() -> PolicyTools:
    """Get or create PolicyTools instance."""
    global _policy_tools
    if _policy_tools is None:
        _policy_tools = PolicyTools()
    return _policy_tools


# Export tool functions
def upload_policy_documents(
    file_paths: str,
    store_name: str,
) -> Dict[str, Any]:
    """Upload policy documents to File Search store."""
    return _get_tools().upload_policy_documents(file_paths, store_name)


def search_policies(
    query: str,
    store_name: str,
    metadata_filter: Optional[str] = None,
) -> Dict[str, Any]:
    """Search policies using semantic search."""
    return _get_tools().search_policies(query, store_name, metadata_filter)


def filter_policies_by_metadata(
    store_name: str,
    department: Optional[str] = None,
    policy_type: Optional[str] = None,
    sensitivity: Optional[str] = None,
    jurisdiction: Optional[str] = None,
) -> Dict[str, Any]:
    """Filter policies by metadata."""
    return _get_tools().filter_policies_by_metadata(
        store_name, department, policy_type, sensitivity, jurisdiction
    )


def compare_policies(
    query: str,
    store_names: List[str],
) -> Dict[str, Any]:
    """Compare policies across stores."""
    return _get_tools().compare_policies(query, store_names)


def check_compliance_risk(
    query: str,
    store_name: str,
) -> Dict[str, Any]:
    """Check compliance and assess risks."""
    return _get_tools().check_compliance_risk(query, store_name)


def extract_policy_requirements(
    query: str,
    store_name: str,
) -> Dict[str, Any]:
    """Extract specific requirements from policies."""
    return _get_tools().extract_policy_requirements(query, store_name)


def generate_policy_summary(
    query: str,
    store_name: str,
) -> Dict[str, Any]:
    """Generate policy summary."""
    return _get_tools().generate_policy_summary(query, store_name)


def create_audit_trail(
    action: str,
    user: str,
    query: str,
    result_summary: str,
) -> Dict[str, Any]:
    """Create audit trail entry."""
    return _get_tools().create_audit_trail(action, user, query, result_summary)
