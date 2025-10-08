"""
Finance Assistant Agent - Tutorial 02: Function Tools

This agent demonstrates how to create function tools that become LLM-callable.
It provides three financial calculation tools:
- Compound interest calculations
- Loan payment calculations
- Monthly savings goal calculations

The agent showcases automatic tool selection, parallel execution, and
structured returns with human-readable reports.
"""

from typing import Dict, Any
from google.adk.agents import Agent


def calculate_compound_interest(
    principal: float,
    annual_rate: float,
    years: int,
    compounds_per_year: int = 1
) -> Dict[str, Any]:
    """
    Calculate compound interest growth for an investment.

    This function computes how much an initial investment will grow to
    over time with compound interest. It uses the standard compound interest
    formula: A = P(1 + r/n)^(nt)

    Args:
        principal: Initial investment amount (e.g., 10000 for $10,000)
        annual_rate: Annual interest rate as decimal (e.g., 0.06 for 6%)
        years: Number of years to compound
        compounds_per_year: How often interest compounds per year (default: 12 for monthly)

    Returns:
        Dict with calculation results and formatted report

    Example:
        >>> calculate_compound_interest(10000, 0.06, 5)
        {
            'status': 'success',
            'final_amount': 13488.50,
            'interest_earned': 3488.50,
            'report': 'After 5 years at 6% annual interest...'
        }
    """
    try:
        # Validate inputs
        if principal <= 0:
            return {
                'status': 'error',
                'error': 'Principal must be positive',
                'report': 'Error: Investment principal must be greater than zero.'
            }

        if annual_rate < 0 or annual_rate > 1:
            return {
                'status': 'error',
                'error': 'Invalid interest rate',
                'report': 'Error: Annual interest rate must be between 0 and 1 (e.g., 0.06 for 6%).'
            }

        if years <= 0:
            return {
                'status': 'error',
                'error': 'Invalid time period',
                'report': 'Error: Investment period must be positive.'
            }

        # Calculate compound interest
        rate_per_period = annual_rate / compounds_per_year
        total_periods = years * compounds_per_year

        final_amount = principal * (1 + rate_per_period) ** total_periods
        interest_earned = final_amount - principal

        # Format human-readable report
        report = (
            f"After {years} years at {annual_rate*100:.1f}% annual interest "
            f"(compounded {compounds_per_year} times per year), "
            f"your ${principal:,.0f} investment will grow to "
            f"${final_amount:,.2f}. That's ${interest_earned:,.2f} in interest!"
        )

        return {
            'status': 'success',
            'final_amount': round(final_amount, 2),
            'interest_earned': round(interest_earned, 2),
            'report': report
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Error calculating compound interest: {str(e)}'
        }


def calculate_loan_payment(
    loan_amount: float,
    annual_rate: float,
    years: int
) -> Dict[str, Any]:
    """
    Calculate monthly loan payments using the standard amortization formula.

    This function computes the monthly payment required to pay off a loan
    over a specified period at a given interest rate. It uses the formula:
    M = P[r(1+r)^n]/[(1+r)^n-1] where r is monthly rate and n is months.

    Args:
        loan_amount: Total loan amount (e.g., 300000 for $300,000)
        annual_rate: Annual interest rate as decimal (e.g., 0.045 for 4.5%)
        years: Loan term in years

    Returns:
        Dict with payment calculation results and formatted report

    Example:
        >>> calculate_loan_payment(300000, 0.045, 30)
        {
            'status': 'success',
            'monthly_payment': 1520.06,
            'total_paid': 547221.60,
            'total_interest': 247221.60,
            'report': 'For a $300,000 loan at 4.5% over 30 years...'
        }
    """
    try:
        # Validate inputs
        if loan_amount <= 0:
            return {
                'status': 'error',
                'error': 'Invalid loan amount',
                'report': 'Error: Loan amount must be positive.'
            }

        if annual_rate < 0 or annual_rate > 1:
            return {
                'status': 'error',
                'error': 'Invalid interest rate',
                'report': 'Error: Annual interest rate must be between 0 and 1 '
                          '(e.g., 0.045 for 4.5%).'
            }

        if years <= 0:
            return {
                'status': 'error',
                'error': 'Invalid loan term',
                'report': 'Error: Loan term must be positive.'
            }

        # Convert to monthly calculations
        monthly_rate = annual_rate / 12
        total_months = years * 12

        # Handle zero interest rate case
        if monthly_rate == 0:
            monthly_payment = loan_amount / total_months
            total_paid = loan_amount
            total_interest = 0
        else:
            # Standard loan payment formula
            monthly_payment = loan_amount * (
                monthly_rate * (1 + monthly_rate) ** total_months
            ) / ((1 + monthly_rate) ** total_months - 1)

            total_paid = monthly_payment * total_months
            total_interest = total_paid - loan_amount

        # Format human-readable report
        report = (
            f"For a ${loan_amount:,.0f} loan at {annual_rate*100:.1f}% interest "
            f"over {years} years, your monthly payment will be "
            f"${monthly_payment:,.2f}. Over the life of the loan, you'll pay "
            f"${total_paid:,.2f} total, with ${total_interest:,.2f} being interest."
        )

        return {
            'status': 'success',
            'monthly_payment': round(monthly_payment, 2),
            'total_paid': round(total_paid, 2),
            'total_interest': round(total_interest, 2),
            'report': report
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Error calculating loan payment: {str(e)}'
        }


def calculate_monthly_savings(
    target_amount: float,
    years: int,
    annual_return: float = 0.05
) -> Dict[str, Any]:
    """
    Calculate monthly savings needed to reach a financial goal.

    This function determines how much you need to save each month to reach
    a savings goal, assuming compound growth at a specified annual return.
    It uses the present value of annuity formula rearranged for payment amount.

    Args:
        target_amount: Target savings amount (e.g., 50000 for $50,000)
        years: Number of years to save
        annual_return: Expected annual return as decimal (default: 0.05 for 5%)

    Returns:
        Dict with savings calculation results and formatted report

    Example:
        >>> calculate_monthly_savings(50000, 3, 0.05)
        {
            'status': 'success',
            'monthly_savings': 1315.07,
            'total_contributed': 47342.52,
            'interest_earned': 2657.48,
            'report': 'To reach $50,000 in 3 years with 5% annual return...'
        }
    """
    try:
        # Validate inputs
        if target_amount <= 0:
            return {
                'status': 'error',
                'error': 'Invalid target amount',
                'report': 'Error: Savings target must be positive.'
            }

        if years <= 0:
            return {
                'status': 'error',
                'error': 'Invalid time period',
                'report': 'Error: Savings period must be positive.'
            }

        if annual_return < 0:
            return {
                'status': 'error',
                'error': 'Invalid return rate',
                'report': 'Error: Annual return rate cannot be negative.'
            }

        # Convert to monthly calculations
        monthly_return = annual_return / 12
        total_months = years * 12

        # Handle zero return case
        if monthly_return == 0:
            monthly_savings = target_amount / total_months
            total_contributed = target_amount
            interest_earned = 0
        else:
            # Correct formula for monthly savings to reach future value
            # PMT = FV * (r / ((1 + r)^n - 1)) where r is monthly rate, n is months
            monthly_savings = target_amount * (
                monthly_return / ((1 + monthly_return) ** total_months - 1)
            )

            total_contributed = monthly_savings * total_months
            # Calculate actual future value to verify
            future_value = 0
            for month in range(1, total_months + 1):
                future_value += monthly_savings * (1 + monthly_return) ** (total_months - month)
            interest_earned = future_value - total_contributed

        # Format human-readable report
        report = (
            f"To reach ${target_amount:,.0f} in {years} years with a "
            f"{annual_return*100:.1f}% annual return, you need to save "
            f"${monthly_savings:,.2f} per month. You'll contribute "
            f"${total_contributed:,.2f} total, with the rest coming from investment returns."
        )

        return {
            'status': 'success',
            'monthly_savings': round(monthly_savings, 2),
            'total_contributed': round(total_contributed, 2),
            'interest_earned': round(interest_earned, 2),
            'report': report
        }

    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'report': f'Error calculating monthly savings: {str(e)}'
        }


# Create the finance assistant agent
root_agent = Agent(
    name="finance_assistant",
    model="gemini-2.0-flash",
    description="""
    A financial calculation assistant that can help with:
    - Compound interest calculations for investments
    - Loan payment calculations for mortgages or other loans
    - Monthly savings calculations to reach financial goals

    I can perform multiple calculations simultaneously for comparison purposes.
    All calculations include detailed explanations and formatted reports.
    """,
    tools=[
        calculate_compound_interest,
        calculate_loan_payment,
        calculate_monthly_savings
    ]
)


if __name__ == "__main__":
    # Example usage for testing
    print("Finance Assistant Agent")
    print("=" * 50)

    # Test compound interest
    result = calculate_compound_interest(10000, 0.06, 5)
    print("Compound Interest Test:")
    print(result['report'])
    print()

    # Test loan payment
    result = calculate_loan_payment(300000, 0.045, 30)
    print("Loan Payment Test:")
    print(result['report'])
    print()

    # Test monthly savings
    result = calculate_monthly_savings(50000, 3, 0.05)
    print("Monthly Savings Test:")
    print(result['report'])
    print()

    print("Agent created successfully with 3 financial tools!")
