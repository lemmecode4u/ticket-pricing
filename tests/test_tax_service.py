# tests/test_tax_service.py

import pytest
from decimal import Decimal
from src.models.pricing_models import TicketPricingConfig
from src.services.tax_service import calculate_taxes


@pytest.fixture
def base_config():
    return TicketPricingConfig(
        ticket_prices={}, availability={},
        festival_discount=None,
        member_percentage_discount=Decimal("0.00"),
        member_discount_cap=Decimal("0.00"),
        convenience_fee_per_ticket=Decimal("10.00"),
        gst_rate=Decimal("0.18"),
    )


def test_zero_convenience_fee_and_zero_gst(base_config):
    base_config.convenience_fee_per_ticket = Decimal("0.00")
    base_config.gst_rate = Decimal("0.00")
    result = calculate_taxes(Decimal("100.00"), 1, base_config)
    assert result["convenience_fee"] == Decimal("0.00")
    assert result["gst"] == Decimal("0.00")
    assert result["final_total"] == Decimal("100.00")


def test_convenience_fee_one_ticket(base_config):
    result = calculate_taxes(Decimal("100.00"), 1, base_config)
    assert result["convenience_fee"] == Decimal("10.00")


def test_convenience_fee_multiple_tickets(base_config):
    result = calculate_taxes(Decimal("100.00"), 3, base_config)
    assert result["convenience_fee"] == Decimal("30.00")


def test_gst_calculation(base_config):
    result = calculate_taxes(Decimal("100.00"), 1, base_config)
    # taxable = 110, gst = 19.80
    assert result["gst"] == Decimal("19.80")


def test_gst_after_convenience_fee(base_config):
    result = calculate_taxes(Decimal("200.00"), 2, base_config)
    # convenience fee = 20, taxable = 220, gst = 39.60
    assert result["gst"] == Decimal("39.60")
    assert result["taxable_amount"] == Decimal("220.00")


def test_final_total(base_config):
    result = calculate_taxes(Decimal("100.00"), 1, base_config)
    # subtotal=100, fee=10, gst=19.80, final=129.80
    assert result["final_total"] == Decimal("129.80")


def test_exact_decimal_precision(base_config):
    result = calculate_taxes(Decimal("33.333"), 1, base_config)
    # amount_after_discounts finalized to 33.33
    assert result["amount_after_discounts"] == Decimal("33.33")


def test_negative_amount_validation(base_config):
    with pytest.raises(ValueError, match="cannot be negative"):
        calculate_taxes(Decimal("-100.00"), 1, base_config)


def test_invalid_quantity_validation(base_config):
    with pytest.raises(ValueError, match="positive integer"):
        calculate_taxes(Decimal("100.00"), 0, base_config)
    with pytest.raises(ValueError, match="integer"):
        calculate_taxes(Decimal("100.00"), 1.5, base_config)
