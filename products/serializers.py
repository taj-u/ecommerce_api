from rest_framework import serializers
from .models import Product
from vendors.models import Vendor

class ProductSerializer(serializers.ModelSerializer):
    vendor_name = serializers.ReadOnlyField(source='vendor.business_name')
    
    class Meta:
        model = Product
        fields = ['id', 'vendor', 'vendor_name', 'name', 'description', 'price', 'stock', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'vendor_name']
        
    def create(self, validated_data):
        # If user is a vendor, assign the product to their vendor profile
        user = self.context['request'].user
        if user.is_vendor():
            validated_data['vendor'] = user.vendor_profile
        
        product = Product.objects.create(**validated_data)
        return product
        
    def validate_vendor(self, value):
        # Only admin can change the vendor
        user = self.context['request'].user
        if not user.is_admin() and self.instance:
            # If not admin and updating an existing product, 
            # ensure vendor isn't changed
            if self.instance.vendor != value:
                raise serializers.ValidationError("You cannot change the vendor of this product.")
        return value