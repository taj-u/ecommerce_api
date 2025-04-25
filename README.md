# ecommerce_api
Advanced Multi-Tenant E-commerce API with Role-Based Access Control  (RBAC).


Task: Advanced Multi-Tenant E-commerce API with Role-Based Access Control
(RBAC)

Need to create a Django REST Framework (DRF) API for a multi-tenant e-commerce system where
multiple vendors can register and manage their own products, orders, and customers.
Have to Implement role-based access control (RBAC) to restrict permissions.

Requirements:
1. User Roles & Authentication
    ○ Use JWT authentication (djangorestframework-simplejwt)
    ○ Users should have different roles: Admin, Vendor, Customer
    ○ Implement role-based access:
        ■ Admin: Can view all vendors, products, and orders
        ■ Vendor: Can manage only their own products and orders
        ■ Customer: Can place orders but cannot modify products
2. Models (Use Django ORM)
    ○ User (AbstractBaseUser or Django’s built-in User)
    ○ Vendor (ForeignKey to User)
    ○ Product (Each product belongs to a Vendor)
    ○ Order (Each order belongs to a Customer and contains multiple products)
    ○ OrderItem (Many-to-Many relation between Order & Product)

3. API Endpoints (Use Django Viewsets & Serializers)
    ○ Auth API (Register, Login, Logout)
    ○ Vendor API (List vendors, retrieve a vendor’s details)
    ○ Product API (CRUD operations, but vendors can manage only their
    products)
    ○ Order API (Customers can place orders; vendors can view orders containing
    their products)

4. Advanced Requirements:
○ Implement Throttling & Rate Limiting for API requests
○ Optimize queries to avoid N+1 problems
○ Use pagination for large datasets
○ Custom permissions to enforce role-based access
○ Implement a search and filtering feature for products

5. Fun to do
Implement Django Signals to notify vendors when a new order is placed
○ Use Redis or Cache to optimize performance for frequently accessed data

