Vikmo Assignment(Django REST API)

Overview
This project implements a backend Order Management System using Django and Django REST Framework.
It manages products, inventory, dealers, and orders, with a complete order lifecycle: draft → confirmation → inventory update → locked state.

The focus is on correct business logic, data integrity, and clean API design.
Core Features
- Product management with unique SKU
- Inventory tracking (per product)
- Dealer management
- Order creation with multiple items
- Automatic pricing (unit price, line total, order total)
- Stock validation before confirmation
- Inventory deduction on confirmation
- Order locking after confirmation (no further edits)

Tech Stack
- Python
- Django
- Django REST Framework
- SQLite

Data Model (Summary)
- Product: name, SKU (unique), price
- Inventory: one-to-one with Product, quantity
- Dealer: name, email (unique), phone
- Order: dealer, status (draft/confirmed/delivered), order_number, total_amount
- OrderItem: order, product, quantity, unit_price, line_total

Key Design Decisions
- Orders start as draft and move to confirmed via a dedicated endpoint
- Stock validation happens before confirmation
- Inventory is reduced only after confirmation
- Totals are calculated on the backend
- Confirmed orders are not editable
- Order numbers are auto-generated

API Endpoints
- GET/POST /api/products/
- GET/POST /api/inventory/
- GET/POST /api/dealers/
- GET/POST /api/orders/
- POST /api/orders/{id}/confirm/

Order Workflow
1. Create product and set inventory
2. Create dealer
3. Create order (draft)
4. Add items
5. Confirm order
6. Inventory is reduced
7. Order is locked

Sample Request (Create Order)
json code:
{
  "dealer": 1,
  "items": [
    {
      "product": 1,
      "quantity": 2
    }
  ]
}

Business Rules
-Orders cannot be confirmed if stock is insufficient
-Inventory is reduced only after confirmation
-Confirmed orders cannot be modified
-All totals are calculated on the backend

Setup Instructions
-git clone <your-repo-link>
-cd vikmo_assignment
-python -m venv venv
-venv\Scripts\activate
-pip install django djangorestframework
-python manage.py makemigrations
-python manage.py migrate
-python manage.py runserver

Testing
-Use browser (DRF UI) or Postman
-Test order creation, confirmation, and inventory deduction

Author
Ameena Khanam