"""
Metadata schema and utilities for File Search document organization.

Defines metadata structure for different policy types and provides utilities
for adding, filtering, and managing metadata.
"""

from typing import Any, Dict, List
from enum import Enum
from datetime import datetime


class PolicyDepartment(str, Enum):
    """Supported policy departments."""

    HR = "HR"
    IT = "IT"
    LEGAL = "Legal"
    SAFETY = "Safety"
    GENERAL = "General"


class PolicyType(str, Enum):
    """Supported policy types."""

    HANDBOOK = "handbook"
    PROCEDURE = "procedure"
    CODE_OF_CONDUCT = "code_of_conduct"
    GUIDELINE = "guideline"
    COMPLIANCE = "compliance"


class Sensitivity(str, Enum):
    """Data sensitivity levels."""

    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"


class MetadataSchema:
    """Metadata schema for File Search documents."""

    @staticmethod
    def get_schema() -> Dict[str, str]:
        """
        Get metadata schema definition.

        Returns:
            dict: Schema mapping field names to types
        """
        return {
            "department": "string",  # HR, IT, Legal, Safety, General
            "policy_type": "string",  # handbook, procedure, code_of_conduct, guideline
            "effective_date": "date",  # YYYY-MM-DD
            "jurisdiction": "string",  # US, EU, CA, etc.
            "sensitivity": "string",  # public, internal, confidential
            "version": "numeric",  # 1, 2, 3, etc.
            "owner": "string",  # Email of policy owner
            "review_cycle_months": "numeric",  # Months between reviews
        }

    @staticmethod
    def create_metadata(
        department: str,
        policy_type: str,
        effective_date: str = None,
        jurisdiction: str = "US",
        sensitivity: str = "internal",
        version: int = 1,
        owner: str = "hr@company.com",
        review_cycle_months: int = 12,
    ) -> List[Dict[str, Any]]:
        """
        Create metadata list for File Search import.

        Args:
            department: Policy department (HR, IT, Legal, Safety, General)
            policy_type: Type of policy (handbook, procedure, etc.)
            effective_date: Date when policy becomes effective (YYYY-MM-DD)
            jurisdiction: Legal jurisdiction (US, EU, CA, etc.)
            sensitivity: Data sensitivity (public, internal, confidential)
            version: Policy version number
            owner: Email of policy owner
            review_cycle_months: Months between policy reviews

        Returns:
            list: Metadata items suitable for File Search import_file()
        """
        if effective_date is None:
            effective_date = datetime.now().strftime("%Y-%m-%d")

        metadata = [
            {"key": "department", "string_value": department},
            {"key": "policy_type", "string_value": policy_type},
            {"key": "effective_date", "string_value": effective_date},
            {"key": "jurisdiction", "string_value": jurisdiction},
            {"key": "sensitivity", "string_value": sensitivity},
            {"key": "version", "numeric_value": version},
            {"key": "owner", "string_value": owner},
            {"key": "review_cycle_months", "numeric_value": review_cycle_months},
        ]

        return metadata

    @staticmethod
    def hr_metadata(version: int = 1) -> List[Dict[str, Any]]:
        """Create metadata for HR policy."""
        return MetadataSchema.create_metadata(
            department="HR",
            policy_type="handbook",
            jurisdiction="US",
            sensitivity="internal",
            version=version,
            owner="hr@company.com",
            review_cycle_months=12,
        )

    @staticmethod
    def it_metadata(version: int = 1) -> List[Dict[str, Any]]:
        """Create metadata for IT security policy."""
        return MetadataSchema.create_metadata(
            department="IT",
            policy_type="procedure",
            jurisdiction="US",
            sensitivity="confidential",
            version=version,
            owner="security@company.com",
            review_cycle_months=6,
        )

    @staticmethod
    def remote_work_metadata(version: int = 1) -> List[Dict[str, Any]]:
        """Create metadata for remote work policy."""
        return MetadataSchema.create_metadata(
            department="HR",
            policy_type="procedure",
            jurisdiction="US",
            sensitivity="internal",
            version=version,
            owner="hr@company.com",
            review_cycle_months=12,
        )

    @staticmethod
    def code_of_conduct_metadata(version: int = 1) -> List[Dict[str, Any]]:
        """Create metadata for code of conduct."""
        return MetadataSchema.create_metadata(
            department="General",
            policy_type="code_of_conduct",
            jurisdiction="US",
            sensitivity="internal",
            version=version,
            owner="legal@company.com",
            review_cycle_months=24,
        )

    @staticmethod
    def build_metadata_filter(
        department: str = None,
        policy_type: str = None,
        sensitivity: str = None,
        jurisdiction: str = None,
    ) -> str:
        """
        Build AIP-160 metadata filter string for File Search queries.

        Args:
            department: Filter by department
            policy_type: Filter by policy type
            sensitivity: Filter by sensitivity level
            jurisdiction: Filter by jurisdiction

        Returns:
            str: AIP-160 filter string (e.g., 'department="HR" AND sensitivity="internal"')
        """
        filters = []

        if department:
            filters.append(f'department="{department}"')
        if policy_type:
            filters.append(f'policy_type="{policy_type}"')
        if sensitivity:
            filters.append(f'sensitivity="{sensitivity}"')
        if jurisdiction:
            filters.append(f'jurisdiction="{jurisdiction}"')

        return " AND ".join(filters) if filters else ""
