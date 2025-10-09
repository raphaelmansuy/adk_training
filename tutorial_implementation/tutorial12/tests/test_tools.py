"""
Test business analysis tools for Strategic Problem Solver.
"""

import pytest
from unittest.mock import MagicMock

from strategic_solver.agent import (
    analyze_market,
    calculate_roi,
    assess_risk,
    save_strategy_report
)


class TestAnalyzeMarket:
    """Test market analysis tool."""

    def test_analyze_market_healthcare(self):
        """Test market analysis for healthcare industry."""
        mock_context = MagicMock()
        result = analyze_market("healthcare", "North America", mock_context)

        assert result["status"] == "success"
        assert "healthcare" in result["report"].lower()
        assert "analysis" in result
        assert result["analysis"]["industry"] == "healthcare"
        assert result["analysis"]["region"] == "North America"
        assert "growth_rate" in result["analysis"]
        assert "competition" in result["analysis"]

    def test_analyze_market_finance(self):
        """Test market analysis for finance industry."""
        mock_context = MagicMock()
        result = analyze_market("finance", "Europe", mock_context)

        assert result["status"] == "success"
        assert result["analysis"]["industry"] == "finance"
        assert result["analysis"]["region"] == "Europe"
        assert "fintech" in str(result["analysis"]["trends"]).lower()

    def test_analyze_market_unknown_industry(self):
        """Test market analysis for unknown industry."""
        mock_context = MagicMock()
        result = analyze_market("unknown", "Global", mock_context)

        assert result["status"] == "success"
        assert result["analysis"]["industry"] == "unknown"
        assert result["analysis"]["growth_rate"] == "5.0%"
        assert result["analysis"]["competition"] == "Medium"

    def test_analyze_market_error_handling(self):
        """Test error handling in market analysis."""
        mock_context = MagicMock()
        # The function doesn't actually use context in a way that fails,
        # so this test should just verify it doesn't crash
        result = analyze_market("test", "test", mock_context)
        assert result["status"] == "success"  # Function handles all inputs gracefully
        assert "analysis" in result


class TestCalculateROI:
    """Test ROI calculation tool."""

    def test_calculate_roi_positive(self):
        """Test ROI calculation with positive returns."""
        mock_context = MagicMock()
        result = calculate_roi(10000, 8, 5, mock_context)

        assert result["status"] == "success"
        assert result["calculation"]["initial_investment"] == 10000
        assert result["calculation"]["annual_return_rate"] == "8%"
        assert result["calculation"]["years"] == 5
        assert result["calculation"]["roi_percentage"] > 0
        assert "annual_breakdown" in result["calculation"]

    def test_calculate_roi_zero_years(self):
        """Test ROI calculation with zero years (should error)."""
        mock_context = MagicMock()
        result = calculate_roi(10000, 8, 0, mock_context)

        assert result["status"] == "error"
        assert "positive" in result["error"]

    def test_calculate_roi_negative_investment(self):
        """Test ROI calculation with negative investment (should error)."""
        mock_context = MagicMock()
        result = calculate_roi(-1000, 8, 5, mock_context)

        assert result["status"] == "error"
        assert "positive" in result["error"]

    def test_calculate_roi_high_returns(self):
        """Test ROI calculation with high return rates."""
        mock_context = MagicMock()
        result = calculate_roi(50000, 25, 3, mock_context)

        assert result["status"] == "success"
        assert result["calculation"]["roi_percentage"] > 50  # Should be significant

    def test_calculate_roi_annual_breakdown(self):
        """Test that annual breakdown is calculated correctly."""
        mock_context = MagicMock()
        result = calculate_roi(1000, 10, 2, mock_context)

        breakdown = result["calculation"]["annual_breakdown"]
        assert len(breakdown) == 2
        assert breakdown[0]["year"] == 1
        assert breakdown[1]["year"] == 2
        assert breakdown[1]["value"] > breakdown[0]["value"]


class TestAssessRisk:
    """Test risk assessment tool."""

    def test_assess_risk_high_risk_factors(self):
        """Test risk assessment with high-risk factors."""
        mock_context = MagicMock()
        factors = ["market_volatility", "competition", "cybersecurity_threats"]
        result = assess_risk(factors, mock_context)

        assert result["status"] == "success"
        assert result["assessment"]["risk_level"] in ["High", "Medium"]
        assert len(result["assessment"]["factor_scores"]) == len(factors)
        assert "mitigation_suggestions" in result["assessment"]

    def test_assess_risk_low_risk_factors(self):
        """Test risk assessment with low-risk factors."""
        mock_context = MagicMock()
        factors = ["talent_shortage", "interest_rate_changes"]
        result = assess_risk(factors, mock_context)

        assert result["status"] == "success"
        assert result["assessment"]["risk_level"] == "Low"
        assert result["assessment"]["average_score"] < 5

    def test_assess_risk_empty_factors(self):
        """Test risk assessment with empty factors list."""
        mock_context = MagicMock()
        result = assess_risk([], mock_context)

        assert result["status"] == "success"
        assert result["assessment"]["average_score"] == 5.0  # Default

    def test_assess_risk_mixed_factors(self):
        """Test risk assessment with mixed risk factors."""
        mock_context = MagicMock()
        factors = ["market_volatility", "talent_shortage", "regulatory_changes"]
        result = assess_risk(factors, mock_context)

        assert result["status"] == "success"
        assert 5 <= result["assessment"]["average_score"] <= 7  # Medium range

    def test_assess_risk_unknown_factors(self):
        """Test risk assessment with unknown factors."""
        mock_context = MagicMock()
        factors = ["completely_unknown_factor", "another_unknown"]
        result = assess_risk(factors, mock_context)

        assert result["status"] == "success"
        # Unknown factors should get default score of 5
        assert all(score == 5 for score in result["assessment"]["factor_scores"].values())


@pytest.mark.asyncio
class TestSaveStrategyReport:
    """Test strategy report saving tool."""

    async def test_save_strategy_report_success(self):
        """Test successful strategy report saving."""
        mock_context = MagicMock()
        mock_context.saved_reports = []

        result = await save_strategy_report(
            "Test business problem",
            "Test strategy recommendation",
            mock_context
        )

        assert result["status"] == "success"
        assert "filename" in result
        assert "strategy_" in result["filename"]
        assert result["filename"].endswith(".md")
        assert len(mock_context.saved_reports) == 1

    async def test_save_strategy_report_content(self):
        """Test that saved report contains correct content."""
        mock_context = MagicMock()
        mock_context.saved_reports = []

        problem = "Market expansion problem"
        strategy = "Expand to Asia with local partnerships"

        await save_strategy_report(problem, strategy, mock_context)

        saved_report = mock_context.saved_reports[0]
        assert problem in saved_report["content"]
        assert strategy in saved_report["content"]
        assert "Strategic Business Plan" in saved_report["content"]
        assert "Generated:" in saved_report["content"]

    async def test_save_strategy_report_error_handling(self):
        """Test error handling in strategy report saving."""
        mock_context = MagicMock()
        # Simulate an error
        mock_context.saved_reports = None
        mock_context.side_effect = Exception("Save failed")

        result = await save_strategy_report("test", "test", mock_context)

        assert result["status"] == "error"
        assert "error" in result