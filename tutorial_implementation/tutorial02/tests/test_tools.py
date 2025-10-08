"""
Test suite for financial calculation tools - Tutorial 02: Function Tools

Tests the three financial calculation functions:
- calculate_compound_interest
- calculate_loan_payment
- calculate_monthly_savings

Covers accuracy, error handling, edge cases, and input validation.
"""

import pytest
from finance_assistant.agent import (
    calculate_compound_interest,
    calculate_loan_payment,
    calculate_monthly_savings
)


class TestCompoundInterest:
    """Test compound interest calculations."""

    def test_basic_compound_interest(self):
        """Test basic compound interest calculation."""
        result = calculate_compound_interest(1000, 0.05, 1)

        assert result['status'] == 'success'
        assert result['final_amount'] == 1050.00
        assert result['interest_earned'] == 50.00
        assert 'grow to $1,050' in result['report']

    def test_compound_interest_with_monthly_compounding(self):
        """Test compound interest with monthly compounding."""
        result = calculate_compound_interest(10000, 0.06, 5, 12)

        assert result['status'] == 'success'
        assert abs(result['final_amount'] - 13488.50) < 0.01  # Allow small rounding difference
        assert abs(result['interest_earned'] - 3488.50) < 0.01
        assert '$10,000' in result['report']
        assert '6.0%' in result['report']

    def test_zero_principal_error(self):
        """Test error handling for zero principal."""
        result = calculate_compound_interest(0, 0.05, 1)

        assert result['status'] == 'error'
        assert 'Principal must be positive' in result['error']
        assert 'greater than zero' in result['report']

    def test_negative_principal_error(self):
        """Test error handling for negative principal."""
        result = calculate_compound_interest(-1000, 0.05, 1)

        assert result['status'] == 'error'
        assert 'Principal must be positive' in result['error']

    def test_invalid_interest_rate_high(self):
        """Test error handling for interest rate > 100%."""
        result = calculate_compound_interest(1000, 1.5, 1)

        assert result['status'] == 'error'
        assert 'Invalid interest rate' in result['error']
        assert 'between 0 and 1' in result['report']

    def test_invalid_interest_rate_negative(self):
        """Test error handling for negative interest rate."""
        result = calculate_compound_interest(1000, -0.05, 1)

        assert result['status'] == 'error'
        assert 'Invalid interest rate' in result['error']

    def test_zero_years_error(self):
        """Test error handling for zero years."""
        result = calculate_compound_interest(1000, 0.05, 0)

        assert result['status'] == 'error'
        assert 'Invalid time period' in result['error']
        assert 'must be positive' in result['report']

    def test_negative_years_error(self):
        """Test error handling for negative years."""
        result = calculate_compound_interest(1000, 0.05, -1)

        assert result['status'] == 'error'
        assert 'Invalid time period' in result['error']

    def test_quarterly_compounding(self):
        """Test compound interest with quarterly compounding."""
        result = calculate_compound_interest(1000, 0.04, 2, 4)

        assert result['status'] == 'success'
        assert result['final_amount'] > 1000  # Should have grown
        assert result['interest_earned'] > 0

    def test_high_precision_calculation(self):
        """Test calculation with high precision requirements."""
        result = calculate_compound_interest(12345.67, 0.0725, 7, 12)

        assert result['status'] == 'success'
        assert isinstance(result['final_amount'], float)
        assert isinstance(result['interest_earned'], float)
        assert result['final_amount'] > result['interest_earned']  # Final should be
        # principal + interest


class TestLoanPayment:
    """Test loan payment calculations."""

    def test_basic_loan_payment(self):
        """Test basic loan payment calculation."""
        result = calculate_loan_payment(100000, 0.05, 10)

        assert result['status'] == 'success'
        assert result['monthly_payment'] > 0
        assert result['total_paid'] > 100000  # Should include interest
        assert result['total_interest'] > 0
        assert result['total_paid'] == pytest.approx(127278.62, abs=0.01)

    def test_30_year_mortgage(self):
        """Test 30-year mortgage calculation."""
        result = calculate_loan_payment(300000, 0.045, 30)

        assert result['status'] == 'success'
        assert abs(result['monthly_payment'] - 1520.06) < 0.01
        assert abs(result['total_paid'] - 547220.13) < 0.01
        assert abs(result['total_interest'] - 247220.13) < 0.01

    def test_zero_loan_amount_error(self):
        """Test error handling for zero loan amount."""
        result = calculate_loan_payment(0, 0.05, 10)

        assert result['status'] == 'error'
        assert 'Invalid loan amount' in result['error']
        assert 'must be positive' in result['report']

    def test_negative_loan_amount_error(self):
        """Test error handling for negative loan amount."""
        result = calculate_loan_payment(-100000, 0.05, 10)

        assert result['status'] == 'error'
        assert 'Invalid loan amount' in result['error']

    def test_invalid_interest_rate_high(self):
        """Test error handling for interest rate > 100%."""
        result = calculate_loan_payment(100000, 1.2, 10)

        assert result['status'] == 'error'
        assert 'Invalid interest rate' in result['error']

    def test_zero_interest_rate(self):
        """Test loan payment with zero interest rate."""
        result = calculate_loan_payment(120000, 0.0, 10)

        assert result['status'] == 'success'
        assert result['monthly_payment'] == 120000 / (10 * 12)  # Simple division
        assert result['total_interest'] == 0
        assert result['total_paid'] == 120000

    def test_zero_years_error(self):
        """Test error handling for zero years."""
        result = calculate_loan_payment(100000, 0.05, 0)

        assert result['status'] == 'error'
        assert 'Invalid loan term' in result['error']

    def test_high_interest_rate(self):
        """Test loan payment with high interest rate."""
        result = calculate_loan_payment(50000, 0.15, 5)

        assert result['status'] == 'success'
        assert result['monthly_payment'] > 50000 / (5 * 12)  # Should be more than simple division
        assert result['total_interest'] > 0


class TestMonthlySavings:
    """Test monthly savings calculations."""

    def test_basic_savings_calculation(self):
        """Test basic monthly savings calculation."""
        result = calculate_monthly_savings(10000, 2, 0.05)

        assert result['status'] == 'success'
        assert result['monthly_savings'] > 0
        assert result['total_contributed'] > 0
        assert result['interest_earned'] >= 0  # Could be 0 for simple case

    def test_down_payment_goal(self):
        """Test savings calculation for down payment goal."""
        result = calculate_monthly_savings(50000, 3, 0.05)

        assert result['status'] == 'success'
        assert abs(result['monthly_savings'] - 1290.21) < 0.01
        assert result['total_contributed'] > 0
        assert '$50,000' in result['report']

    def test_zero_target_amount_error(self):
        """Test error handling for zero target amount."""
        result = calculate_monthly_savings(0, 5, 0.05)

        assert result['status'] == 'error'
        assert 'Invalid target amount' in result['error']
        assert 'must be positive' in result['report']

    def test_negative_target_amount_error(self):
        """Test error handling for negative target amount."""
        result = calculate_monthly_savings(-10000, 5, 0.05)

        assert result['status'] == 'error'
        assert 'Invalid target amount' in result['error']

    def test_zero_years_error(self):
        """Test error handling for zero years."""
        result = calculate_monthly_savings(10000, 0, 0.05)

        assert result['status'] == 'error'
        assert 'Invalid time period' in result['error']

    def test_negative_return_rate_error(self):
        """Test error handling for negative return rate."""
        result = calculate_monthly_savings(10000, 5, -0.05)

        assert result['status'] == 'error'
        assert 'Invalid return rate' in result['error']
        assert 'cannot be negative' in result['report']

    def test_zero_return_rate(self):
        """Test savings calculation with zero return rate."""
        result = calculate_monthly_savings(12000, 2, 0.0)

        assert result['status'] == 'success'
        assert result['monthly_savings'] == 12000 / (2 * 12)  # Simple division
        assert result['interest_earned'] == 0

    def test_high_return_rate(self):
        """Test savings calculation with high return rate."""
        result = calculate_monthly_savings(100000, 10, 0.08)

        assert result['status'] == 'success'
        assert result['monthly_savings'] > 0
        assert result['total_contributed'] > 0


class TestIntegration:
    """Integration tests for multiple calculations."""

    def test_multiple_calculations_consistency(self):
        """Test that multiple calculations work together."""
        # Test compound interest
        ci_result = calculate_compound_interest(10000, 0.06, 5)
        assert ci_result['status'] == 'success'

        # Test loan payment
        lp_result = calculate_loan_payment(200000, 0.04, 15)
        assert lp_result['status'] == 'success'

        # Test savings
        ms_result = calculate_monthly_savings(25000, 4, 0.03)
        assert ms_result['status'] == 'success'

    def test_error_handling_integration(self):
        """Test error handling across all functions."""
        functions = [
            lambda: calculate_compound_interest(-1000, 0.05, 1),
            lambda: calculate_loan_payment(100000, 0.05, 0),
            lambda: calculate_monthly_savings(10000, 5, -0.1)
        ]

        for func in functions:
            result = func()
            assert result['status'] == 'error'
            assert 'error' in result
            assert 'report' in result

    def test_real_world_scenarios(self):
        """Test real-world financial scenarios."""
        # Retirement savings
        retirement = calculate_monthly_savings(500000, 30, 0.07)
        assert retirement['status'] == 'success'
        assert retirement['monthly_savings'] > 0

        # Car loan
        car_loan = calculate_loan_payment(35000, 0.06, 5)
        assert car_loan['status'] == 'success'
        assert car_loan['monthly_payment'] > 0

        # Investment growth
        investment = calculate_compound_interest(25000, 0.08, 20, 12)
        assert investment['status'] == 'success'
        assert investment['final_amount'] > 25000


if __name__ == "__main__":
    pytest.main([__file__])
