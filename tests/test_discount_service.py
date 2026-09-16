# tests/test_discount_service.py

import pytest
from decimal import Decimal
from src.models.pricing_models import TicketPricingConfig, FestivalDiscountConfig
from src.services.discount_service import calculate_discounts


@pytest.fixture
def base_config():
    return TicketPricingConfig(
        ticket_prices={},  # not used here
        availability={},   # not used here
        festival_discount=FestivalDiscountConfig(enabled=True, percentage=Decimal("0.10")),
        member_percentage_discount=Decimal("0.20"),
        member_discount_cap=Decimal("50.00"),
        convenience_fee_per_ticket=Decimal("0.00"),
        gst_rate=Decimal("0.00"),
    )


def test_no_discounts(base_config):
    config = TicketPricingConfig(
        ticket_prices={}, availability={},
        festival_discount=None,
        member_percentage_discount=Decimal("0.00"),
        member_discount_cap=Decimal("0.00"),
        convenience_fee_per_ticket=Decimal("0.00"),
        gst_rate=Decimal("0.00"),
    )
    result = calculate_discounts(Decimal("100.00"), config, is_member=False)
    assert result["total_discount"] == Decimal("0.00")
    assert result["amount_after_discounts"] == Decimal("100.00")


def test_festival_discount_disabled(base_config):
    base_config.festival_discount.enabled = False
    result = calculate_discounts(Decimal("100.00"), base_config, is_member=False)
    assert result["festival_discount"] == Decimal("0.00")
    assert result["amount_after_discounts"] == Decimal("100.00")


def test_festival_discount_enabled(base_config):
    result = calculate_discounts(Decimal("100.00"), base_config, is_member=False)
    assert result["festival_discount"] == Decimal("10.00")
    assert result["amount_after_discounts"] == Decimal("90.00")


def test_non_member(base_config):
    result = calculate_discounts(Decimal("100.00"), base_config, is_member=False)
    assert result["member_discount"] == Decimal("0.00")


def test_member_below_cap(base_config):
    result = calculate_discounts(Decimal("100.00"), base_config, is_member=True)
    # Festival discount = 10, remaining = 90, member discount = 18 (below cap)
    assert result["member_discount"] == Decimal("18.00")
    assert result["amount_after_discounts"] == Decimal("72.00")


def test_member_reaches_cap(base_config):
    # Subtotal large enough that member discount hits cap
    result = calculate_discounts(Decimal("1000.00"), base_config, is_member=True)
    assert result["member_discount"] == Decimal("50.00")  # capped
    assert result["amount_after_discounts"] < Decimal("1000.00")


def test_member_exceeds_cap(base_config):
    # Force cap by setting cap lower
    base_config.member_discount_cap = Decimal("10.00")
    result = calculate_discounts(Decimal("200.00"), base_config, is_member=True)
    assert result["member_discount"] == Decimal("10.00")  # capped


def test_festival_and_member_discount(base_config):
    result = calculate_discounts(Decimal("200.00"), base_config, is_member=True)
    # Festival = 20, remaining = 180, member = 36
    assert result["festival_discount"] == Decimal("20.00")
    assert result["member_discount"] == Decimal("36.00")
    assert result["total_discount"] == Decimal("56.00")
    assert result["amount_after_discounts"] == Decimal("144.00")


def test_discounts_cannot_exceed_subtotal(base_config):
    # Configure extreme discounts
    base_config.festival_discount.percentage = Decimal("1.00")  # 100%
    base_config.member_percentage_discount = Decimal("1.00")
    base_config.member_discount_cap = Decimal("9999.00")
    result = calculate_discounts(Decimal("100.00"), base_config, is_member=True)
    assert result["festival_discount"] == Decimal("100.00")
    assert result["member_discount"] == Decimal("0.00")
    assert result["amount_after_discounts"] == Decimal("0.00")


def test_zero_discount_configuration(base_config):
    base_config.festival_discount.percentage = Decimal("0.00")
    base_config.member_percentage_discount = Decimal("0.00")
    base_config.member_discount_cap = Decimal("0.00")
    result = calculate_discounts(Decimal("100.00"), base_config, is_member=True)
    assert result["total_discount"] == Decimal("0.00")
    assert result["amount_after_discounts"] == Decimal("100.00")
