# src/utils/money.py

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import Union

# Define the quantization unit for two decimal places (paisa precision)
PAISA = Decimal("0.01")


def to_decimal(value: Union[str, int, Decimal]) -> Decimal:
    """
    Safely convert an input value to Decimal for monetary calculations.
    Rejects floats to avoid precision issues.
    """
    if isinstance(value, float):
        raise TypeError("Float values are not allowed for monetary calculations.")
    try:
        return Decimal(str(value)).quantize(PAISA, rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError) as e:
        raise ValueError(f"Invalid monetary input: {value}") from e


def add(amount1: Decimal, amount2: Decimal) -> Decimal:
    """Add two monetary amounts and round to 2 decimal places."""
    return (amount1 + amount2).quantize(PAISA, rounding=ROUND_HALF_UP)


def subtract(amount1: Decimal, amount2: Decimal) -> Decimal:
    """Subtract two monetary amounts and round to 2 decimal places."""
    return (amount1 - amount2).quantize(PAISA, rounding=ROUND_HALF_UP)


def multiply(amount: Decimal, quantity: int) -> Decimal:
    """Multiply a monetary amount by an integer quantity and round to 2 decimal places."""
    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")
    return (amount * Decimal(quantity)).quantize(PAISA, rounding=ROUND_HALF_UP)


def percentage(amount: Decimal, rate: Decimal) -> Decimal:
    """
    Calculate a percentage of a monetary amount.
    Example: amount=Decimal("100"), rate=Decimal("0.10") → Decimal("10.00")
    """
    return (amount * rate).quantize(PAISA, rounding=ROUND_HALF_UP)


def finalize(amount: Decimal) -> Decimal:
    """Round/finalize a monetary amount to exactly 2 decimal places."""
    return amount.quantize(PAISA, rounding=ROUND_HALF_UP)
