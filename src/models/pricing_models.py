# src/models/pricing_models.py

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import List, Optional


class TicketTier(Enum):
    SILVER = "Silver"
    GOLD = "Gold"
    RECLINER = "Recliner"


@dataclass
class BookingRequest:
    ticket_tier: TicketTier
    quantity: int
    is_member: bool = False


@dataclass
class FestivalDiscountConfig:
    enabled: bool
    percentage: Decimal  # e.g., 0.10 for 10%


@dataclass
class TicketPricingConfig:
    ticket_prices: dict[TicketTier, Decimal]
    availability: dict[TicketTier, int]
    festival_discount: Optional[FestivalDiscountConfig] = None
    member_percentage_discount: Decimal = Decimal("0.00")
    member_discount_cap: Decimal = Decimal("0.00")
    convenience_fee_per_ticket: Decimal = Decimal("0.00")
    gst_rate: Decimal = Decimal("0.00")  # e.g., 0.18 for 18%


class LineItemType(Enum):
    CHARGE = "Charge"
    DISCOUNT = "Discount"


@dataclass
class BillLineItem:
    description: str
    amount: Decimal
    item_type: LineItemType = LineItemType.CHARGE


@dataclass
class PricingResult:
    ticket_tier: TicketTier
    quantity: int
    unit_price: Decimal
    ticket_subtotal: Decimal
    festival_discount: Decimal
    member_discount: Decimal
    amount_after_discounts: Decimal
    convenience_fee: Decimal
    gst: Decimal
    final_total: Decimal
    breakdown: List[BillLineItem] = field(default_factory=list)
