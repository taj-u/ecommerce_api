from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer
from users.permissions import CanManageProduct

class ProductPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [CanManageProduct]
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['vendor', 'is_active', 'price']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'name']
    
    def get_queryset(self):
        user = self.request.user
        
        # Optimize query with select_related
        queryset = Product.objects.select_related('vendor', 'vendor__user')
        
        # Admin can see all products
        if user.is_admin:
            return queryset
            
        # Vendor can see only their products
        if user.is_vendor:
            return queryset.filter(vendor__user=user)
            
        # Customer can see only active products
        return queryset.filter(is_active=True)