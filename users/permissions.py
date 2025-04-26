from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin

class IsVendor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_vendor()

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_customer()

class IsVendorOwner(permissions.BasePermission):
    """
    Permission to check if user is the vendor owner of an object
    """
    def has_object_permission(self, request, view, obj):
        # Check if obj has vendor attribute directly
        if hasattr(obj, 'vendor'):
            return obj.vendor.user == request.user
        
        # For order items, check if product belongs to vendor
        if hasattr(obj, 'product') and hasattr(obj.product, 'vendor'):
            return obj.product.vendor.user == request.user
            
        return False

class CanManageProduct(permissions.BasePermission):
    """
    Admin can do everything
    Vendor can only manage their own products
    Customer can only view products
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        if request.user.is_admin:
            return True
            
        if request.user.is_vendor and request.method not in ['DELETE']:
            return True
            
        if request.user.is_customer and request.method in permissions.SAFE_METHODS:
            return True
            
        return False
        
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
            
        if request.user.is_vendor:
            # Check if product belongs to the vendor
            try:
                return obj.vendor.user == request.user
            except:
                return False
                
        if request.user.is_customer and request.method in permissions.SAFE_METHODS:
            return True
            
        return False

class CanManageOrder(permissions.BasePermission):
    """
    Admin can do everything
    Vendor can view orders containing their products
    Customer can create orders and view their own orders
    """
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        if request.user.is_admin:
            return True
            
        if request.user.is_vendor and request.method in permissions.SAFE_METHODS:
            return True
            
        if request.user.is_customer:
            if request.method == 'POST':  # Allow customers to create orders
                return True
            if request.method in permissions.SAFE_METHODS:  # Allow customers to view their orders
                return True
                
        return False
        
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
            
        if request.user.is_vendor:
            # Check if any product in order belongs to the vendor
            vendor_products = request.user.vendor_profile.products.all()
            order_items = obj.items.all()
            
            for item in order_items:
                if item.product in vendor_products:
                    return True
            return False
            
        if request.user.is_customer:
            return obj.customer == request.user
            
        return False