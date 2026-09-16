# src/services/ticket_service.py

from decimal import Decimal
from src.models.pricing_models import BookingRequest, TicketPricingConfig, TicketTier
from src.utils import money


def process_booking(request: BookingRequest, config: TicketPricingConfig) -> dict:
    """
    Validate a booking request and calculate the base ticket subtotal.
    Does not apply discounts, fees, or GST.
    """
    # Ensure the ticket tier is a valid TicketTier
    if not isinstance(request.ticket_tier, TicketTier):
        raise ValueError("Unsupported ticket tier.")

    # Validate quantity
    if not isinstance(request.quantity, int):
        raise ValueError("Quantity must be an integer.")
    if request.quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")

    # Validate availability
    availability = config.availability.get(request.ticket_tier)
    if availability is None:
        raise ValueError("Availability not configured for this tier.")
    if availability == 0:
        raise ValueError(f"{request.ticket_tier.value} tier is sold out.")
    if request.quantity > availability:
        raise ValueError("Requested quantity exceeds availability.")

    # Validate ticket price separately
    unit_price = config.ticket_prices.get(request.ticket_tier)
    if unit_price is None:
        raise ValueError("Ticket price not configured for this tier.")

    # Calculate subtotal
    subtotal = money.multiply(unit_price, request.quantity)

    return {
        "ticket_tier": request.ticket_tier,
        "quantity": request.quantity,
        "unit_price": unit_price,
        "subtotal": subtotal,
    }

