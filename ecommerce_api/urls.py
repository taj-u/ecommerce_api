# ecommerce_api/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import RegisterView, UserListView
from vendors.views import VendorViewSet
from products.views import ProductViewSet
from orders.views import OrderViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'vendors', VendorViewSet, basename='vendor')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    
    # User management
    path('api/users/', UserListView.as_view(), name='user-list'),
    
    # Include DRF router URLs
    path('api/', include(router.urls)),
]