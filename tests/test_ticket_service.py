# tests/test_ticket_service.py

import pytest
from decimal import Decimal
from src.models.pricing_models import BookingRequest, TicketPricingConfig, TicketTier
from src.services.ticket_service import process_booking


@pytest.fixture
def sample_config():
    return TicketPricingConfig(
        ticket_prices={
            TicketTier.SILVER: Decimal("100.00"),
            TicketTier.GOLD: Decimal("200.00"),
            TicketTier.RECLINER: Decimal("300.00"),
        },
        availability={
            TicketTier.SILVER: 10,
            TicketTier.GOLD: 5,
            TicketTier.RECLINER: 1,
        },
    )


def test_one_silver_ticket(sample_config):
    request = BookingRequest(ticket_tier=TicketTier.SILVER, quantity=1)
    result = process_booking(request, sample_config)
    assert result["subtotal"] == Decimal("100.00")


def test_multiple_gold_tickets(sample_config):
    request = BookingRequest(ticket_tier=TicketTier.GOLD, quantity=3)
    result = process_booking(request, sample_config)
    assert result["subtotal"] == Decimal("600.00")


def test_one_recliner_ticket(sample_config):
    request = BookingRequest(ticket_tier=TicketTier.RECLINER, quantity=1)
    result = process_booking(request, sample_config)
    assert result["subtotal"] == Decimal("300.00")


def test_sold_out_tier(sample_config):
    sample_config.availability[TicketTier.SILVER] = 0
    request = BookingRequest(ticket_tier=TicketTier.SILVER, quantity=1)
    with pytest.raises(ValueError, match="sold out"):
        process_booking(request, sample_config)


def test_quantity_greater_than_availability(sample_config):
    request = BookingRequest(ticket_tier=TicketTier.GOLD, quantity=10)
    with pytest.raises(ValueError, match="exceeds availability"):
        process_booking(request, sample_config)


def test_zero_quantity(sample_config):
    request = BookingRequest(ticket_tier=TicketTier.SILVER, quantity=0)
    with pytest.raises(ValueError, match="greater than zero"):
        process_booking(request, sample_config)


def test_negative_quantity(sample_config):
    request = BookingRequest(ticket_tier=TicketTier.SILVER, quantity=-1)
    with pytest.raises(ValueError, match="greater than zero"):
        process_booking(request, sample_config)


def test_missing_ticket_price(sample_config):
    del sample_config.ticket_prices[TicketTier.GOLD]
    request = BookingRequest(ticket_tier=TicketTier.GOLD, quantity=1)
    with pytest.raises(ValueError, match="Ticket price not configured"):
        process_booking(request, sample_config)
