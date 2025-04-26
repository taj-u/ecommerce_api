from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer
from users.permissions import CanManageOrder
from django.db.models import Q, Prefetch
from products.models import Product

class OrderPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [CanManageOrder]
    pagination_class = OrderPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'created_at']
    ordering_fields = ['created_at', 'total_amount']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        # Optimize query with prefetch_related and select_related
        queryset = Order.objects.select_related('customer').prefetch_related(
            Prefetch('items', queryset=OrderItem.objects.select_related('product'))
        )
        
        # Admin can see all orders
        if user.is_admin:
            return queryset
            
        # Vendor can see orders containing their products
        if user.is_vendor:
            # Get the vendor's products
            vendor_products = Product.objects.filter(vendor__user=user)
            
            # Get orders that contain any of the vendor's products
            order_ids = OrderItem.objects.filter(product__in=vendor_products).values_list('order_id', flat=True)
            
            return queryset.filter(id__in=order_ids)
            
        # Customer can see only their own orders
        return queryset.filter(customer=user)
