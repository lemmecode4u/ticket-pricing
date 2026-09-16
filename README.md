# ticket-pricing
Multiplex ticket pricing engine
# 🎟️ Ticket Pricing Engine (Python)

## Overview

This project implements a configurable **multiplex ticket-pricing engine** in Python.

The engine handles ticket tiers, availability, discounts, convenience fees, GST, and exact monetary calculations while providing a clear line-by-line bill breakdown.

---

## ✨ Key Features

* Configurable ticket tiers:

  * Silver
  * Gold
  * Recliner
* Ticket availability validation
* Sold-out tier handling
* Base ticket pricing
* Festival percentage discount
* Capped member discount
* Per-ticket convenience fee
* GST calculation
* Exact monetary calculations using Python `Decimal`
* Two-decimal/paisa precision
* Line-by-line bill breakdown
* Unit tests using `pytest`
* Configuration-driven design suitable for different cinema counters

---

## 🏗️ Architecture

```text
Booking Request
      ↓
Ticket Service
      ↓
Base Ticket Subtotal
      ↓
Discount Service
      ↓
Amount After Discounts
      ↓
Tax/Fee Service
      ↓
Convenience Fee + GST
      ↓
Pricing Service
      ↓
Final Bill
```

The application separates ticket validation, discount calculation, tax/fee calculation, and orchestration so that each responsibility can be tested independently.

---

## 📂 Project Structure

```text
ticket-pricing/
│
├── src/
│   ├── config/
│   │   └── pricing_config.py
│   │
│   ├── models/
│   │   └── pricing_models.py
│   │
│   ├── services/
│   │   ├── ticket_service.py
│   │   ├── discount_service.py
│   │   ├── tax_service.py
│   │   └── pricing_service.py
│   │
│   ├── utils/
│   │   └── money.py
│   │
│   └── main.py
│
├── tests/
│   ├── test_ticket_service.py
│   ├── test_discount_service.py
│   ├── test_tax_service.py
│   └── test_pricing_service.py
│
├── README.md
├── REASONING.md
├── AI_LOGS.md
├── requirements.txt
└── .gitignore
```

---

## 🔧 Prerequisites

* Python 3.9 or later
* pip
* Git

---

## ⚙️ Setup

Clone the repository:

```bash
git clone <repository-url>
cd ticket-pricing
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Linux/macOS/GitHub Codespaces:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Run the application from the repository root:

```bash
python -m src.main
```

The CLI accepts:

* Ticket tier
* Ticket quantity
* Membership status

The application then displays the calculated ticket price and a line-by-line billing breakdown.

---

## 🧪 Running Tests

Run the complete test suite:

```bash
python -m pytest -v
```

The tests cover ticket validation, availability, discounts, discount caps, convenience fees, GST, final totals, and billing breakdowns.

---

## 🛠️ Debugging / Troubleshooting

### Virtual environment is not active

For GitHub Codespaces/Linux:

```bash
source .venv/bin/activate
```

### Dependencies are missing

Run:

```bash
pip install -r requirements.txt
```

### Import errors

Run the application from the repository root using:

```bash
python -m src.main
```

instead of:

```bash
python src/main.py
```

### Tests are failing

Run:

```bash
python -m pytest -v
```

The test output identifies the failing test and assertion. Pricing calculations use `Decimal`, so expected monetary values should also be represented using `Decimal`.

---

## ⚙️ Configuration

Pricing configuration is centralized in:

```text
src/config/pricing_config.py
```

The configuration includes:

* Ticket prices
* Ticket availability
* Festival discount
* Member discount percentage
* Member discount cap
* Convenience fee per ticket
* GST rate

The numeric values currently present in the configuration are **sample/demo values only**, because the provided problem statement does not specify the actual numerical business values.

They should be replaced with the applicable business requirements before production use.

---

## 💰 Money Handling

The project uses Python's `Decimal` type for monetary calculations instead of floating-point numbers.

The money utility provides:

* Safe Decimal conversion
* Addition
* Subtraction
* Multiplication
* Percentage calculation
* Final two-decimal-place rounding

This prevents common floating-point precision problems and ensures monetary results are represented to exact paisa precision.

---

## 📋 Pricing Flow

The pricing engine follows this sequence:

1. Validate the requested ticket tier.
2. Validate the requested quantity.
3. Check ticket availability.
4. Calculate the base ticket subtotal.
5. Apply the festival discount when enabled.
6. Apply the member discount when applicable, subject to the configured cap.
7. Calculate the convenience fee based on ticket quantity.
8. Calculate GST on the discounted amount plus convenience fee.
9. Produce the final total.
10. Generate a line-by-line bill breakdown.

---

## 📌 Assumptions

The problem statement does not explicitly define the ordering of multiple discounts.

This implementation applies:

```text
Base Ticket Subtotal
        ↓
Festival Discount
        ↓
Member Discount
        ↓
Convenience Fee
        ↓
GST
        ↓
Final Total
```

The member discount is calculated on the amount remaining after the festival discount and is limited by the configured member discount cap.

This ordering is an implementation assumption and can be changed if the actual business specification defines a different order.

---

## 🚀 Design Approach

The engine is intentionally separated into small services:

* `ticket_service.py` — ticket validation, availability, and base subtotal
* `discount_service.py` — festival and member discounts
* `tax_service.py` — convenience fee and GST
* `pricing_service.py` — orchestration and final bill generation
* `money.py` — reusable monetary operations
* `pricing_config.py` — configurable business values

This separation makes the pricing rules easier to test, maintain, and extend for different cinema counters or shows.
