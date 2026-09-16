# src/main.py

from decimal import Decimal
from src.config.pricing_config import create_pricing_config, validate_pricing_config
from src.models.pricing_models import BookingRequest, TicketTier
from src.services.pricing_service import calculate_pricing


def main():
    print("🎟️ Multiplex Ticket Pricing Demo")
    print("Available tiers: Silver, Gold, Recliner")

    tier_input = input("Enter ticket tier: ").strip().capitalize()
    quantity_input = input("Enter quantity: ").strip()
    member_input = input("Are you a member? (y/n): ").strip().lower()

    # Validate tier
    try:
        ticket_tier = TicketTier[tier_input.upper()]
    except KeyError:
        print("❌ Invalid ticket tier. Please choose Silver, Gold, or Recliner.")
        return

    # Validate quantity
    try:
        quantity = int(quantity_input)
    except ValueError:
        print("❌ Quantity must be an integer.")
        return

    is_member = member_input == "y"

    # Load configuration
    config = create_pricing_config()
    try:
        validate_pricing_config(config)
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return

    # Create booking request
    request = BookingRequest(ticket_tier=ticket_tier, quantity=quantity, is_member=is_member)

    # Run pricing service
    try:
        result = calculate_pricing(request, config)
    except ValueError as e:
        print(f"❌ Booking error: {e}")
        return

    # Print bill
    print("\n🧾 Bill Breakdown")
    print(f"Ticket Tier: {result.ticket_tier.value}")
    print(f"Quantity: {result.quantity}")
    print(f"Unit Price: {result.unit_price:.2f}")
    print(f"Ticket Subtotal: {result.ticket_subtotal:.2f}")
    if result.festival_discount > Decimal("0.00"):
        print(f"Festival Discount: -{result.festival_discount:.2f}")
    if result.member_discount > Decimal("0.00"):
        print(f"Member Discount: -{result.member_discount:.2f}")
    print(f"Amount After Discounts: {result.amount_after_discounts:.2f}")
    if result.convenience_fee > Decimal("0.00"):
        print(f"Convenience Fee: {result.convenience_fee:.2f}")
    if result.gst > Decimal("0.00"):
        print(f"GST: {result.gst:.2f}")
    print(f"Final Total: {result.final_total:.2f}")


if __name__ == "__main__":
    main()
