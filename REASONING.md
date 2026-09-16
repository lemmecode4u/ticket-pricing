# Reasoning

## 1. Problem Understanding
The project models a **multiplex ticket-pricing system** where:
- Different ticket tiers (Silver, Gold, Recliner) have different prices.
- Each tier has limited availability.
- Customers may receive a **festival discount**.
- Members may receive a **capped member discount**.
- A **per-ticket convenience fee** is applied.
- **GST** is charged on the subtotal plus convenience fee.
- All calculations must be accurate to the **paisa (two decimal places)**.
- Customers receive a **transparent line-by-line bill breakdown**.

## 2. Requirements Interpretation
**Implemented functional requirements:**
- Ticket tier validation and availability checks.
- Base ticket subtotal calculation.
- Festival discount application.
- Member discount with cap enforcement.
- Convenience fee per ticket.
- GST calculation on subtotal + fee.
- Exact Decimal-based monetary calculations.
- Line-by-line bill breakdown.

**Assumptions:**
- Festival discount is applied before member discount.
- Current numeric values in configuration are **sample/demo values** only.

## 3. Architecture
- **pricing_models.py**: Defines core domain models (BookingRequest, PricingResult, BillLineItem, etc.).
- **pricing_config.py**: Centralized configuration for ticket prices, discounts, fees, and GST.
- **money.py**: Utility functions for safe Decimal-based monetary calculations.
- **ticket_service.py**: Validates booking requests and calculates base ticket subtotal.
- **discount_service.py**: Applies festival and member discounts.
- **tax_service.py**: Calculates convenience fee, GST, and final total.
- **pricing_service.py**: Orchestrates all services to produce a complete PricingResult.
- **main.py**: Simple CLI demo for user interaction.

**Separation of responsibilities** ensures clarity, testability, and maintainability.

## 4. Ticket Pricing and Availability
- Ticket tier validated against supported enums.
- Quantity must be a positive integer.
- Sold-out tiers (availability = 0) are rejected.
- Requested quantity cannot exceed availability.
- Base subtotal = unit price × quantity.

## 5. Discount Strategy
- **Festival discount**: Applied if enabled, percentage-based, capped at subtotal.
- **Member discount**: Applied if customer is a member, percentage-based, capped by configuration and remaining amount.
- **Member discount cap**: Ensures discount never exceeds configured maximum.
- **Protection**: Discounts never exceed subtotal or remaining amount.

**Ordering assumption**: Festival discount is applied first, then member discount on the remaining amount.

## 6. Convenience Fee and GST
- **Convenience fee**: Calculated per ticket.
- **GST**: Applied on (amount after discounts + convenience fee).
- **Final total**: amount after discounts + convenience fee + GST.

## 7. Monetary Precision
- All calculations use **Decimal** to avoid floating-point errors.
- Values are finalized to **two decimal places** using quantization with `ROUND_HALF_UP`.

## 8. Line-by-Line Billing
- **PricingResult** aggregates all values.
- **BillLineItem** provides detailed breakdown:
  - Ticket subtotal
  - Festival discount
  - Member discount
  - Convenience fee
  - GST
  - Final total

This ensures transparency for customers.

## 9. Error Handling
Validation errors raise clear `ValueError` messages:
- Invalid ticket tier
- Non-integer or non-positive quantity
- Sold-out tier
- Quantity exceeding availability
- Missing ticket price
- Negative configuration values

## 10. Testing Strategy
Unit tests cover:
- Ticket pricing and availability
- Discounts (festival, member, capped)
- Convenience fee
- GST
- Final totals
- Precision handling
- Validation errors
- Line-by-line breakdown

The suite contains **40 tests** ensuring comprehensive coverage.

## 11. Configuration
- All business values centralized in `pricing_config.py`.
- Current numeric values are **sample/demo values** only.
- Real-world deployments must replace these with actual business requirements.

## 12. Assumptions and Limitations
- **Assumption**: Festival discount applied before member discount.
- **Limitation**: Current numeric values are placeholders, not official requirements.
- **Requirement distinction**: All implemented features follow the problem statement; assumptions are explicitly documented.

---
