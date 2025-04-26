from rest_framework import serializers
from .models import Vendor
from users.serializers import UserSerializer

class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Vendor
        fields = ['id', 'user', 'business_name', 'business_description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class VendorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['business_name', 'business_description']
        
    def create(self, validated_data):
        # Get the current user
        user = self.context['request'].user
        
        # Create vendor profile
        vendor = Vendor.objects.create(
            user=user,
            **validated_data
        )
        
        # Update user role
        user.role = 'VENDOR'
        user.save()
        
        return vendor