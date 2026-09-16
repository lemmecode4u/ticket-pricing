# src/services/discount_service.py

"""
Discount Service

This module handles discount calculations for ticket pricing.

ASSUMPTION:
Discounts are applied in the following order:
1. Festival discount on the base subtotal.
2. Member discount on the remaining amount after festival discount.

This ordering is chosen because the problem statement did not explicitly define
discount ordering. It is documented here for clarity.
"""

from decimal import Decimal
from src.models.pricing_models import TicketPricingConfig
from src.utils import money


def calculate_discounts(
    base_subtotal: Decimal,
    config: TicketPricingConfig,
    is_member: bool,
) -> dict:
    """
    Calculate applicable discounts based on configuration and membership status.

    Args:
        base_subtotal (Decimal): The base ticket subtotal (before discounts).
        config (TicketPricingConfig): Pricing configuration.
        is_member (bool): Whether the customer is a member.

    Returns:
        dict: {
            "festival_discount": Decimal,
            "member_discount": Decimal,
            "total_discount": Decimal,
            "amount_after_discounts": Decimal,
        }
    """

    # Ensure base_subtotal is finalized to 2 decimal places
    subtotal = money.finalize(base_subtotal)

    # Festival discount
    festival_discount = Decimal("0.00")
    if config.festival_discount and config.festival_discount.enabled:
        festival_discount = money.percentage(subtotal, config.festival_discount.percentage)
        # Never exceed subtotal
        if festival_discount > subtotal:
            festival_discount = subtotal

    remaining_after_festival = subtotal - festival_discount

    # Member discount
    member_discount = Decimal("0.00")
    if is_member and config.member_percentage_discount > Decimal("0.00"):
        member_discount = money.percentage(
            remaining_after_festival, config.member_percentage_discount
        )
        # Apply cap
        if member_discount > config.member_discount_cap:
            member_discount = config.member_discount_cap
        # Never exceed remaining amount
        if member_discount > remaining_after_festival:
            member_discount = remaining_after_festival

    total_discount = money.add(festival_discount, member_discount)
    amount_after_discounts = subtotal - total_discount
    amount_after_discounts = money.finalize(amount_after_discounts)

    return {
        "festival_discount": festival_discount,
        "member_discount": member_discount,
        "total_discount": total_discount,
        "amount_after_discounts": amount_after_discounts,
    }
