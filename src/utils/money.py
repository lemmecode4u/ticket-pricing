"""
Money utility module.

Provides Decimal-based money handling with:
- Explicit rounding (ROUND_HALF_UP for paisa precision)
- Money arithmetic helpers
- Percentage calculations
- Validation and safety checks
"""

from decimal import Decimal, ROUND_HALF_UP, getcontext
from typing import Union


# Configure Decimal precision for currency operations
getcontext().prec = 28


def round_to_paisa(amount: Decimal) -> Decimal:
    """
    Round a Decimal amount to paisa precision (2 decimal places).
    
    Uses ROUND_HALF_UP: 0.005 rounds to 0.01 (standard accounting rounding).
    
    Args:
        amount: Decimal amount to round.
    
    Returns:
        Amount rounded to 2 decimal places (paisa).
    
    Example:
        >>> round_to_paisa(Decimal('100.126'))
        Decimal('100.13')
        >>> round_to_paisa(Decimal('100.124'))
        Decimal('100.12')
    """
    return amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def to_decimal(value: Union[int, float, str, Decimal]) -> Decimal:
    """
    Safely convert a value to Decimal.
    
    Args:
        value: Value to convert (int, float, str, or Decimal).
    
    Returns:
        Decimal representation of the value.
    
    Raises:
        TypeError: If value cannot be converted to Decimal.
    
    Example:
        >>> to_decimal('100.50')
        Decimal('100.50')
        >>> to_decimal(100)
        Decimal('100')
    """
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def add(*amounts: Union[int, float, str, Decimal]) -> Decimal:
    """
    Add multiple monetary amounts with rounding.
    
    Args:
        *amounts: Variable number of amounts to add.
    
    Returns:
        Sum of all amounts, rounded to paisa.
    
    Example:
        >>> add(Decimal('100.50'), Decimal('50.25'), Decimal('25.10'))
        Decimal('175.85')
    """
    total = sum(to_decimal(amount) for amount in amounts)
    return round_to_paisa(total)


def subtract(minuend: Union[int, float, str, Decimal],
             subtrahend: Union[int, float, str, Decimal]) -> Decimal:
    """
    Subtract one amount from another with rounding.
    
    Args:
        minuend: Amount to subtract from.
        subtrahend: Amount to subtract.
    
    Returns:
        Difference, rounded to paisa.
    
    Example:
        >>> subtract(Decimal('100.50'), Decimal('25.25'))
        Decimal('75.25')
    """
    result = to_decimal(minuend) - to_decimal(subtrahend)
    return round_to_paisa(result)


def multiply(amount: Union[int, float, str, Decimal],
             factor: Union[int, float, str, Decimal]) -> Decimal:
    """
    Multiply a monetary amount by a factor with rounding.
    
    Args:
        amount: Base amount to multiply.
        factor: Multiplication factor (e.g., 2, 3.5, quantity).
    
    Returns:
        Product, rounded to paisa.
    
    Example:
        >>> multiply(Decimal('250'), 3)
        Decimal('750.00')
    """
    result = to_decimal(amount) * to_decimal(factor)
    return round_to_paisa(result)


def apply_percentage(base: Union[int, float, str, Decimal],
                     percent: Union[int, float, str, Decimal]) -> Decimal:
    """
    Calculate a percentage of a base amount with rounding.
    
    Args:
        base: Base amount.
        percent: Percentage to apply (e.g., 10 for 10%).
    
    Returns:
        Percentage of base, rounded to paisa.
    
    Example:
        >>> apply_percentage(Decimal('1000'), Decimal('18'))
        Decimal('180.00')
        >>> apply_percentage(Decimal('250.50'), Decimal('10'))
        Decimal('25.05')
    """
    base_dec = to_decimal(base)
    percent_dec = to_decimal(percent)
    result = (base_dec * percent_dec) / Decimal('100')
    return round_to_paisa(result)


def cap_amount(amount: Union[int, float, str, Decimal],
               maximum: Union[int, float, str, Decimal]) -> Decimal:
    """
    Ensure an amount does not exceed a maximum value.
    
    Args:
        amount: Amount to cap.
        maximum: Maximum allowed value.
    
    Returns:
        min(amount, maximum), rounded to paisa.
    
    Example:
        >>> cap_amount(Decimal('600'), Decimal('500'))
        Decimal('500.00')
        >>> cap_amount(Decimal('300'), Decimal('500'))
        Decimal('300.00')
    """
    amount_dec = to_decimal(amount)
    max_dec = to_decimal(maximum)
    return round_to_paisa(min(amount_dec, max_dec))


def ensure_non_negative(amount: Union[int, float, str, Decimal]) -> Decimal:
    """
    Ensure an amount is not negative (clamp to 0).
    
    Args:
        amount: Amount to check.
    
    Returns:
        max(amount, 0), rounded to paisa.
    
    Example:
        >>> ensure_non_negative(Decimal('-100'))
        Decimal('0.00')
        >>> ensure_non_negative(Decimal('100'))
        Decimal('100.00')
    """
    amount_dec = to_decimal(amount)
    return round_to_paisa(max(amount_dec, Decimal('0')))
