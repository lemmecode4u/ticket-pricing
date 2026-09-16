# src/config/pricing_config.py

from decimal import Decimal
from src.models.pricing_models import (
    TicketTier,
    FestivalDiscountConfig,
    TicketPricingConfig,
)


def create_pricing_config() -> TicketPricingConfig:
    """
    Factory function to create a TicketPricingConfig instance.
    NOTE: All numeric values here are SAMPLE/DEMO configuration only.
    Replace them with actual business values as required.
    """

    ticket_prices = {
        TicketTier.SILVER: Decimal("150.00"),   # Example/demo value
        TicketTier.GOLD: Decimal("250.00"),     # Example/demo value
        TicketTier.RECLINER: Decimal("400.00"), # Example/demo value
    }

    availability = {
        TicketTier.SILVER: 100,   # Example/demo value
        TicketTier.GOLD: 50,      # Example/demo value
        TicketTier.RECLINER: 20,  # Example/demo value
    }

    festival_discount = FestivalDiscountConfig(
        enabled=True,             # Example/demo setting
        percentage=Decimal("0.10")  # 10% demo discount
    )

    return TicketPricingConfig(
        ticket_prices=ticket_prices,
        availability=availability,
        festival_discount=festival_discount,
        member_percentage_discount=Decimal("0.05"),  # 5% demo discount
        member_discount_cap=Decimal("100.00"),       # Demo cap
        convenience_fee_per_ticket=Decimal("20.00"), # Demo fee
        gst_rate=Decimal("0.18"),                    # 18% demo GST
    )


def validate_pricing_config(config: TicketPricingConfig) -> None:
    """
    Basic validation to ensure configuration values are sensible.
    Raises ValueError if invalid.
    """
    for tier, price in config.ticket_prices.items():
        if price < Decimal("0.00"):
            raise ValueError(f"Ticket price for {tier} cannot be negative.")

    for tier, qty in config.availability.items():
        if qty < 0:
            raise ValueError(f"Availability for {tier} cannot be negative.")

    if config.festival_discount:
        if config.festival_discount.percentage < Decimal("0.00") or config.festival_discount.percentage > Decimal("1.00"):
            raise ValueError("Festival discount percentage must be between 0 and 1.")

    if config.member_percentage_discount < Decimal("0.00") or config.member_percentage_discount > Decimal("1.00"):
        raise ValueError("Member discount percentage must be between 0 and 1.")

    if config.member_discount_cap < Decimal("0.00"):
        raise ValueError("Member discount cap cannot be negative.")

    if config.convenience_fee_per_ticket < Decimal("0.00"):
        raise ValueError("Convenience fee cannot be negative.")

    if config.gst_rate < Decimal("0.00") or config.gst_rate > Decimal("1.00"):
        raise ValueError("GST rate must be between 0 and 1.")
