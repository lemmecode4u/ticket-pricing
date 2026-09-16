# src/services/pricing_service.py

from src.models.pricing_models import (
    BookingRequest,
    TicketPricingConfig,
    BillLineItem,
    LineItemType,
    PricingResult,
)
from src.services import ticket_service, discount_service, tax_service


def calculate_pricing(request: BookingRequest, config: TicketPricingConfig) -> PricingResult:
    """
    Main pricing orchestration function.

    Steps:
    1. Ticket service → validate booking and calculate base subtotal.
    2. Discount service → apply festival and member discounts.
    3. Tax service → apply convenience fee and GST.
    4. Build line-by-line breakdown.
    5. Return PricingResult.

    Errors from lower-level services propagate naturally.
    """

    # Step 1 — Base ticket price
    ticket_result = ticket_service.process_booking(request, config)
    ticket_tier = ticket_result["ticket_tier"]
    quantity = ticket_result["quantity"]
    unit_price = ticket_result["unit_price"]
    ticket_subtotal = ticket_result["subtotal"]

    # Step 2 — Discounts
    discount_result = discount_service.calculate_discounts(
        ticket_subtotal, config, request.is_member
    )
    festival_discount = discount_result["festival_discount"]
    member_discount = discount_result["member_discount"]
    amount_after_discounts = discount_result["amount_after_discounts"]

    # Step 3 — Fee and GST
    tax_result = tax_service.calculate_taxes(amount_after_discounts, quantity, config)
    convenience_fee = tax_result["convenience_fee"]
    gst = tax_result["gst"]
    final_total = tax_result["final_total"]

    # Step 4 — Breakdown
    breakdown = []
    breakdown.append(BillLineItem(description="Ticket Subtotal", amount=ticket_subtotal))
    if festival_discount > 0:
        breakdown.append(
            BillLineItem(
                description="Festival Discount",
                amount=festival_discount,
                item_type=LineItemType.DISCOUNT,
            )
        )
    if member_discount > 0:
        breakdown.append(
            BillLineItem(
                description="Member Discount",
                amount=member_discount,
                item_type=LineItemType.DISCOUNT,
            )
        )
    if convenience_fee > 0:
        breakdown.append(
            BillLineItem(description="Convenience Fee", amount=convenience_fee)
        )
    if gst > 0:
        breakdown.append(BillLineItem(description="GST", amount=gst))
    breakdown.append(BillLineItem(description="Final Total", amount=final_total))

    # Step 5 — Return PricingResult
    return PricingResult(
        ticket_tier=ticket_tier,
        quantity=quantity,
        unit_price=unit_price,
        ticket_subtotal=ticket_subtotal,
        festival_discount=festival_discount,
        member_discount=member_discount,
        amount_after_discounts=amount_after_discounts,
        convenience_fee=convenience_fee,
        gst=gst,
        final_total=final_total,
        breakdown=breakdown,
    )
