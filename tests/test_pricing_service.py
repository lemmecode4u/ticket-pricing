# tests/test_pricing_service.py

import pytest
from decimal import Decimal
from src.models.pricing_models import BookingRequest, TicketPricingConfig, TicketTier, FestivalDiscountConfig
from src.services.pricing_service import calculate_pricing


@pytest.fixture
def base_config():
    return TicketPricingConfig(
        ticket_prices={
            TicketTier.SILVER: Decimal("100.00"),
            TicketTier.GOLD: Decimal("200.00"),
            TicketTier.RECLINER: Decimal("300.00"),
        },
        availability={
            TicketTier.SILVER: 10,
            TicketTier.GOLD: 5,
            TicketTier.RECLINER: 2,
        },
        festival_discount=FestivalDiscountConfig(enabled=True, percentage=Decimal("0.10")),
        member_percentage_discount=Decimal("0.20"),
        member_discount_cap=Decimal("50.00"),
        convenience_fee_per_ticket=Decimal("10.00"),
        gst_rate=Decimal("0.18"),
    )


def test_basic_silver_booking(base_config):
    request = BookingRequest(ticket_tier=TicketTier.SILVER, quantity=1)
    result = calculate_pricing(request, base_config)
    assert result.ticket_subtotal == Decimal("100.00")
    assert result.final_total > Decimal("100.00")


def test_multiple_tickets(base_config):
    request = BookingRequest(ticket_tier=TicketTier.GOLD, quantity=2)
    result = calculate_pricing(request, base_config)
    assert result.ticket_subtotal == Decimal("400.00")
    assert result.quantity == 2


def test_festival_discount(base_config):
    request = BookingRequest(ticket_tier=TicketTier.SILVER, quantity=1)
    result = calculate_pricing(request, base_config)
    assert result.festival_discount == Decimal("10.00")


def test_member_discount(base_config):
    request = BookingRequest(ticket_tier=TicketTier.SILVER, quantity=1, is_member=True)
    result = calculate_pricing(request, base_config)
    assert result.member_discount > Decimal("0.00")


def test_festival_and_member_discount(base_config):
    request = BookingRequest(ticket_tier=TicketTier.GOLD, quantity=1, is_member=True)
    result = calculate_pricing(request, base_config)
    assert result.festival_discount > Decimal("0.00")
    assert result.member_discount > Decimal("0.00")


def test_member_discount_cap(base_config):
    request = BookingRequest(ticket_tier=TicketTier.RECLINER, quantity=2, is_member=True)
    result = calculate_pricing(request, base_config)
    assert result.member_discount <= base_config.member_discount_cap


def test_convenience_fee(base_config):
    request = BookingRequest(ticket_tier=TicketTier.SILVER, quantity=2)
    result = calculate_pricing(request, base_config)
    assert result.convenience_fee == Decimal("20.00")


def test_gst(base_config):
    request = BookingRequest(ticket_tier=TicketTier.SILVER, quantity=1)
    result = calculate_pricing(request, base_config)
    assert result.gst > Decimal("0.00")


def test_final_total(base_config):
    request = BookingRequest(ticket_tier=TicketTier.SILVER, quantity=1)
    result = calculate_pricing(request, base_config)
    assert result.final_total == result.breakdown[-1].amount


def test_line_by_line_breakdown(base_config):
    request = BookingRequest(ticket_tier=TicketTier.SILVER, quantity=1, is_member=True)
    result = calculate_pricing(request, base_config)
    descriptions = [item.description for item in result.breakdown]
    assert "Ticket Subtotal" in descriptions
    assert "Final Total" in descriptions


def test_sold_out_tier(base_config):
    base_config.availability[TicketTier.SILVER] = 0
    request = BookingRequest(ticket_tier=TicketTier.SILVER, quantity=1)
    with pytest.raises(ValueError, match="sold out"):
        calculate_pricing(request, base_config)


def test_quantity_greater_than_availability(base_config):
    request = BookingRequest(ticket_tier=TicketTier.GOLD, quantity=10)
    with pytest.raises(ValueError, match="exceeds availability"):
        calculate_pricing(request, base_config)


def test_invalid_quantity(base_config):
    request = BookingRequest(ticket_tier=TicketTier.SILVER, quantity=0)
    with pytest.raises(ValueError, match="greater than zero"):
        calculate_pricing(request, base_config)
