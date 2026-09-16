# src/services/tax_service.py

from decimal import Decimal
from src.models.pricing_models import TicketPricingConfig
from src.utils import money


def calculate_taxes(amount_after_discounts: Decimal, quantity: int, config: TicketPricingConfig) -> dict:
    """
    Calculate convenience fee and GST after discounts.

    Args:
        amount_after_discounts (Decimal): Amount after discounts.
        quantity (int): Number of tickets.
        config (TicketPricingConfig): Pricing configuration.

    Returns:
        dict: {
            "amount_after_discounts": Decimal,
            "convenience_fee": Decimal,
            "taxable_amount": Decimal,
            "gst": Decimal,
            "final_total": Decimal,
        }
    """

    # Validation
    if not isinstance(quantity, int):
        raise ValueError("Quantity must be an integer.")
    if quantity <= 0:
        raise ValueError("Quantity must be a positive integer.")
    if amount_after_discounts < Decimal("0.00"):
        raise ValueError("Amount after discounts cannot be negative.")
    if config.convenience_fee_per_ticket < Decimal("0.00"):
        raise ValueError("Convenience fee cannot be negative.")
    if config.gst_rate < Decimal("0.00"):
        raise ValueError("GST rate cannot be negative.")

    # Convenience fee
    convenience_fee = money.multiply(config.convenience_fee_per_ticket, quantity)

    # Taxable amount
    taxable_amount = money.add(amount_after_discounts, convenience_fee)

    # GST
    gst = money.percentage(taxable_amount, config.gst_rate)

    # Final total
    final_total = money.add(taxable_amount, gst)

    return {
        "amount_after_discounts": money.finalize(amount_after_discounts),
        "convenience_fee": convenience_fee,
        "taxable_amount": taxable_amount,
        "gst": gst,
        "final_total": final_total,
    }
