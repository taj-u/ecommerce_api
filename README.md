# ecommerce_api
### Advanced Multi-Tenant E-commerce API with Role-Based Access Control  (RBAC).


## Table of Contents
- [Requirements and Features](#need-to-create-a-django-rest-framework-drf-api-for-a-multi-tenant-e-commerce-system-where-multiple-vendors-can-register-and-manage-their-own-products-orders-and-customers-have-to-implement-role-based-access-control-rbac-to-restrict-permissions)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
- [Auth and User Management](#authentication--user-management)
    - [User Registration](#1-user-registration)
    - [Obtain Token](#2-obtain-token)
    - [Refresh Token](#3-refresh-token)
    - [List Users](#4-list-users)

---
##### Need to create a Django REST Framework (DRF) API for a multi-tenant e-commerce system where multiple vendors can register and manage their own products, orders, and customers. Have to Implement role-based access control (RBAC) to restrict permissions.

### Requirements:
1. User Roles & Authentication
    - Use JWT authentication (djangorestframework-simplejwt)
    - Users should have different roles: Admin, Vendor, Customer
    - Implement role-based access:
        - Admin: Can view all vendors, products, and orders
        - Vendor: Can manage only their own products and orders
        - Customer: Can place orders but cannot modify products

2. Models (Use Django ORM)
    - User (AbstractBaseUser or Django’s built-in User)
    - Vendor (ForeignKey to User)
    - Product (Each product belongs to a Vendor)
    - Order (Each order belongs to a Customer and contains multiple products)
    - OrderItem (Many-to-Many relation between Order & Product)

3. API Endpoints (Use Django Viewsets & Serializers)
    - Auth API (Register, Login, Logout)
    - Vendor API (List vendors, retrieve a vendor’s details)
    - Product API (CRUD operations, but vendors can manage only their
    products)
    - Order API (Customers can place orders; vendors can view orders containing
    their products)

4. Advanced Requirements:
    - Implement Throttling & Rate Limiting for API requests
    - Optimize queries to avoid N+1 problems
    - Use pagination for large datasets
    - Custom permissions to enforce role-based access
    - Implement a search and filtering feature for products

5. Fun to do
- Implement Django Signals to notify vendors when a new order is placed
- Use Redis or Cache to optimize performance for frequently accessed data


## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository
```bash
git clone https://github.com/taj-u/ecommerce_api.git
cd ecommerce_api
```

2. Create and activate virtual environment

For Windows:
```bash
python -m venv virtual_env_name
cd virtual_env_name\Scripts\activate
```

For Unix/MacOS:
```bash
python -m venv virtual_env_name
source virtual_env_name/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Authentication & User Management

### 1. User Registration
**Endpoint:** `POST /api/register`

**Body:**
```json
{
    "username": "user1",
    "password": "admin@1234",
    "password2": "admin@123",
    "role": "ADMIN", //  Admin, Vendor, Customer
    "phone number": "+880 1234-123456",
    "adress": "xx, yyy, z"
}
```

**Success Response:** (HTTP 201 Created)
```json
{
    "username": "user4",
    "email": "user@example.com",
    "role": "ADMIN",
    "phone_number": "+8801325698888",
    "address": "0"
}
```

### 2. Obtain Token
**Endpoint:** `POST /api/token/` 

**Body:**
```json
{
    "username": "user1",
    "password": "admin@123"
}
```

**Success Response:** (HTTP 200 OK)
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NTc2MjM2NiwiaWF0IjoxNzQ1Njc1OTY2LCJqdGkiOiJlMmEzYmM5YzI3N2Q0ODllYjBiYmU0ZDQzNmYzMTU0OCIsInVzZXJfaWQiOiJ1c2VyMiJ9.8owAV8LnIcGE-6xmJ-oDDjC5x-DiMQ6v_t8qn7SomMI",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ1NjgzMTY2LCJpYXQiOjE3NDU2NzU5NjYsImp0aSI6ImNlZjQyOTRjOTUyNDQ3ZjNhNTc4OWUzZWY5MzNhMDEwIiwidXNlcl9pZCI6InVzZXIyIn0.S0lkcH7b8D4Y7WhWMtFEOKwfP4qToqAudsPVOvQyefw"
}
```

### 3. Refresh Token
**Endpoint:** `POST /api/token/refresh/`

**Body:**
```json
{
    "refresh": "your_refresh_token_here"
}
```

**Success Response:** (HTTP 200 OK)
```json
{
    "access": "new_access_token_here",
    "refresh": "new_refresh_token"
}
```

### 4. List Users
**Endpoint:** `GET /api/users`

**Authorization:** Bearer Token required

**Success Response:** (HTTP 200 OK)
```json
[
    {
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "username": "user",
            "email": "user@user.com",
            "role": "ADMIN",
            "phone_number": "+8801325698162",
            "address": "0, xx, yyy"
        },
        {
            "id": 3,
            "username": "user1",
            "email": "user1@user.com",
            "role": "VENDOR",
            "phone_number": "+8801325698162",
            "address": "gkjkgj"
        },
        {
            "id": 1,
            "username": "admin",
            "email": "admin@admin.com",
            "role": "CUSTOMER",
            "phone_number": null,
            "address": null
        },
]
```