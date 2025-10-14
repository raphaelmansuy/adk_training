"""
Test suite for Tutorial 26: Enterprise agent tool functions.
"""

import pytest
from enterprise_agent.agent import (
    check_company_size,
    score_lead,
    get_competitive_intel
)


class TestCheckCompanySize:
    """Test the check_company_size tool function."""

    def test_check_company_size_known_company(self):
        """Test looking up a known company."""
        result = check_company_size("TechCorp")
        
        assert result["status"] == "success"
        assert result["company_name"] == "TechCorp"
        assert "data" in result
        assert result["data"]["employees"] == 250
        assert result["data"]["revenue"] == "50M"
        assert result["data"]["industry"] == "technology"

    def test_check_company_size_finance(self):
        """Test looking up a finance company."""
        result = check_company_size("FinanceGlobal")
        
        assert result["status"] == "success"
        assert result["data"]["employees"] == 1200
        assert result["data"]["industry"] == "finance"

    def test_check_company_size_healthcare(self):
        """Test looking up a healthcare company."""
        result = check_company_size("HealthPlus")
        
        assert result["status"] == "success"
        assert result["data"]["employees"] == 450
        assert result["data"]["industry"] == "healthcare"

    def test_check_company_size_unknown_company(self):
        """Test looking up an unknown company returns defaults."""
        result = check_company_size("UnknownCompany")
        
        assert result["status"] == "success"
        assert result["company_name"] == "UnknownCompany"
        assert result["data"]["employees"] == 0
        assert result["data"]["revenue"] == "Unknown"

    def test_check_company_size_has_report(self):
        """Test that function returns human-readable report."""
        result = check_company_size("TechCorp")
        
        assert "report" in result
        assert len(result["report"]) > 0


class TestScoreLead:
    """Test the score_lead tool function."""

    def test_score_lead_highly_qualified(self):
        """Test scoring a highly qualified lead (70+ points)."""
        result = score_lead(
            company_size=250,
            industry="technology",
            budget="enterprise"
        )
        
        assert result["status"] == "success"
        assert result["score"] >= 70
        assert result["qualification"] == "HIGHLY QUALIFIED"
        assert "demo" in result["recommendation"].lower()

    def test_score_lead_qualified(self):
        """Test scoring a qualified lead (40-69 points)."""
        result = score_lead(
            company_size=150,
            industry="retail",
            budget="business"
        )
        
        assert result["status"] == "success"
        assert 40 <= result["score"] < 70
        assert result["qualification"] == "QUALIFIED"

    def test_score_lead_unqualified(self):
        """Test scoring an unqualified lead (<40 points)."""
        result = score_lead(
            company_size=20,
            industry="retail",
            budget="startup"
        )
        
        assert result["status"] == "success"
        assert result["score"] < 40
        assert result["qualification"] == "UNQUALIFIED"

    def test_score_lead_large_company_bonus(self):
        """Test that large companies get bonus points."""
        result = score_lead(
            company_size=150,
            industry="other",
            budget="startup"
        )
        
        # Should get 30 points for company size
        assert result["score"] == 30

    def test_score_lead_target_industry_bonus(self):
        """Test that target industries get bonus points."""
        result = score_lead(
            company_size=50,
            industry="finance",
            budget="startup"
        )
        
        # Should get 30 points for finance industry
        assert result["score"] == 30

    def test_score_lead_healthcare_industry(self):
        """Test healthcare as target industry."""
        result = score_lead(
            company_size=50,
            industry="healthcare",
            budget="startup"
        )
        
        # Should get 30 points for healthcare industry
        assert result["score"] == 30

    def test_score_lead_enterprise_budget(self):
        """Test enterprise budget tier scoring."""
        result = score_lead(
            company_size=50,
            industry="retail",
            budget="enterprise"
        )
        
        # Should get 40 points for enterprise budget
        assert result["score"] == 40

    def test_score_lead_business_budget(self):
        """Test business budget tier scoring."""
        result = score_lead(
            company_size=50,
            industry="retail",
            budget="business"
        )
        
        # Should get 20 points for business budget
        assert result["score"] == 20

    def test_score_lead_perfect_score(self):
        """Test perfect qualification (100 points)."""
        result = score_lead(
            company_size=500,
            industry="finance",
            budget="enterprise"
        )
        
        assert result["score"] == 100
        assert result["qualification"] == "HIGHLY QUALIFIED"

    def test_score_lead_has_factors(self):
        """Test that scoring provides detailed factors."""
        result = score_lead(
            company_size=250,
            industry="technology",
            budget="enterprise"
        )
        
        assert "factors" in result
        assert len(result["factors"]) > 0
        assert isinstance(result["factors"], list)

    def test_score_lead_has_report(self):
        """Test that scoring returns human-readable report."""
        result = score_lead(
            company_size=250,
            industry="technology",
            budget="enterprise"
        )
        
        assert "report" in result
        assert len(result["report"]) > 0
        assert str(result["score"]) in result["report"]


class TestGetCompetitiveIntel:
    """Test the get_competitive_intel tool function."""

    def test_get_competitive_intel_basic(self):
        """Test getting competitive intelligence."""
        result = get_competitive_intel("OurCompany", "CompetitorX")
        
        assert result["status"] == "success"
        assert "data" in result
        assert result["data"]["company"] == "OurCompany"
        assert result["data"]["competitor"] == "CompetitorX"

    def test_get_competitive_intel_has_differentiators(self):
        """Test that competitive intel includes differentiators."""
        result = get_competitive_intel("OurCompany", "CompetitorX")
        
        assert "differentiators" in result["data"]
        assert len(result["data"]["differentiators"]) > 0

    def test_get_competitive_intel_has_weaknesses(self):
        """Test that competitive intel includes competitor weaknesses."""
        result = get_competitive_intel("OurCompany", "CompetitorX")
        
        assert "competitor_weaknesses" in result["data"]
        assert len(result["data"]["competitor_weaknesses"]) > 0

    def test_get_competitive_intel_has_news(self):
        """Test that competitive intel includes recent news."""
        result = get_competitive_intel("OurCompany", "CompetitorX")
        
        assert "recent_news" in result["data"]
        assert len(result["data"]["recent_news"]) > 0

    def test_get_competitive_intel_has_report(self):
        """Test that competitive intel returns formatted report."""
        result = get_competitive_intel("OurCompany", "CompetitorX")
        
        assert "report" in result
        assert len(result["report"]) > 0
        assert "OurCompany" in result["report"]
        assert "CompetitorX" in result["report"]


class TestToolIntegration:
    """Test that tools work together for lead qualification workflow."""

    def test_full_qualification_workflow(self):
        """Test complete lead qualification workflow."""
        # Step 1: Check company size
        company_result = check_company_size("TechCorp")
        assert company_result["status"] == "success"
        
        # Step 2: Score the lead
        company_data = company_result["data"]
        score_result = score_lead(
            company_size=company_data["employees"],
            industry=company_data["industry"],
            budget="enterprise"
        )
        assert score_result["status"] == "success"
        assert score_result["score"] == 100  # TechCorp: 250 employees, tech, enterprise
        
        # Step 3: Get competitive intel
        intel_result = get_competitive_intel("TechCorp", "CompetitorX")
        assert intel_result["status"] == "success"

    def test_tools_return_consistent_format(self):
        """Test that all tools return consistent response format."""
        tools = [
            check_company_size("TechCorp"),
            score_lead(250, "technology", "enterprise"),
            get_competitive_intel("OurCompany", "CompetitorX")
        ]
        
        for result in tools:
            assert "status" in result
            assert result["status"] == "success"
            assert "report" in result
            assert len(result["report"]) > 0
