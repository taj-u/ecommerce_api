from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count, Sum
from .models import Vendor
from .serializers import VendorSerializer, VendorCreateSerializer
from users.permissions import IsAdmin, IsVendor

class VendorViewSet(viewsets.ModelViewSet):
    serializer_class = VendorSerializer
    filterset_fields = ['business_name']
    search_fields = ['business_name', 'business_description']
    
    def get_queryset(self):
        user = self.request.user
        
        # Admin can see all vendors
        if user.is_admin:
            return Vendor.objects.all().select_related('user')
            
        # Vendor can see only their own profile
        if user.is_vendor:
            return Vendor.objects.filter(user=user).select_related('user')
            
        # Customers can see all vendors but with limited info
        return Vendor.objects.all().select_related('user')
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsVendor()]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return VendorCreateSerializer
        return VendorSerializer
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get vendor statistics - only for admin or the vendor owner"""
        vendor = self.get_object()
        
        # Check if user is admin or the vendor owner
        if not (request.user.is_admin() or vendor.user == request.user):
            return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        
        # Get statistics
        product_count = vendor.products.count()
        active_products = vendor.products.filter(is_active=True).count()
        
        # Calculate orders for vendor's products
        from orders.models import OrderItem
        order_items = OrderItem.objects.filter(product__vendor=vendor)
        total_sales = order_items.aggregate(total=Sum('price'))['total'] or 0
        orders_count = order_items.values('order').distinct().count()
        
        return Response({
            "product_count": product_count,
            "active_products": active_products,
            "total_sales": total_sales,
            "orders_count": orders_count
        })