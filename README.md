# E-commerce Backend (Django + DRF)

A Django REST Framework backend for an e-commerce site selling CPUs, GPUs, Monoblocks, and Monitors. Secured with JWT auth and designed for a React + TypeScript frontend.

## Quickstart

- Python 3.12, Django 5
- Activate venv and install deps:

```bash
pip install -r requirements.txt
```

- Run migrations and start server:

```bash
python manage.py migrate
python manage.py runserver
```

## Auth

- POST /api/auth/signup/
- POST /api/token/  -> obtain access/refresh
- POST /api/token/refresh/
- POST /api/auth/logout/ -> blacklist refresh
- GET  /api/auth/profile/

## Products

- GET /api/products/
  - query: category=CPU|GPU|Monoblock|Monitor, search, ordering
- GET /api/products/{id}/
- GET/POST /api/products/{id}/reviews/

## Cart

- GET /api/cart/
- POST /api/cart/add/ { product_id, quantity }
- PATCH /api/cart/items/{item_id}/ { quantity }
- DELETE /api/cart/items/{item_id}/remove/

## Orders

- POST /api/orders/ { shipping_name, shipping_address, billing_name, billing_address }
- GET  /api/orders/{id}/
- PATCH /api/orders/{id}/ { status } (admin only)

## News

- GET /api/news/
- GET /api/news/{id}/

## Pages

- GET /api/public-offer/
- POST /api/contact/ { name, email, message }

## Admin

- /admin/ to manage products, orders, news, and messages.

## Notes

- Pagination: Default page size 12.
- Permissions: Auth required for cart/order/review create; admin for order status changes.
- Images: Uses ImageField paths; configure MEDIA if uploading.
  - Install Pillow if not already: `pip install Pillow`
# back_darkandwhite
