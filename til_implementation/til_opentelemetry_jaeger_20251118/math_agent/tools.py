"""
Simple math tools for the ADK agent.
"""


def add_numbers(a: float, b: float) -> float:
    """
    Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of a and b
    """
    return a + b


def subtract_numbers(a: float, b: float) -> float:
    """
    Subtract b from a.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Difference (a - b)
    """
    return a - b


def multiply_numbers(a: float, b: float) -> float:
    """
    Multiply two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Product of a and b
    """
    return a * b


def divide_numbers(a: float, b: float) -> float:
    """
    Divide a by b.
    
    Args:
        a: Numerator
        b: Denominator
        
    Returns:
        Quotient (a / b)
        
    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
