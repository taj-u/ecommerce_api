from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from django.db import transaction

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'subtotal']
        read_only_fields = ['id', 'price', 'subtotal', 'product_name']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.ReadOnlyField(source='customer.username')
    
    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_name', 'status', 'items', 'total_amount', 'shipping_address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'customer', 'total_amount', 'created_at', 'updated_at', 'customer_name']

class OrderCreateSerializer(serializers.ModelSerializer):
    items = serializers.ListField(
        child=serializers.DictField(), 
        write_only=True
    )
    
    class Meta:
        model = Order
        fields = ['shipping_address', 'items']
    
    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        customer = self.context['request'].user
        
        # Create order
        order = Order.objects.create(
            customer=customer,
            **validated_data
        )
        
        # Create order items
        total_amount = 0
        for item_data in items_data:
            product_id = item_data.get('product')
            quantity = item_data.get('quantity', 1)
            
            try:
                product = Product.objects.get(id=product_id, is_active=True)
                
                # Check if there's enough stock
                if product.stock < quantity:
                    raise serializers.ValidationError(f"Not enough stock for {product.name}")
                
                # Create order item
                order_item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )
                
                # Update stock
                product.stock -= quantity
                product.save()
                
                # Add to total
                total_amount += order_item.subtotal
                
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with id {product_id} not found or not active")
        
        # Update order total
        order.total_amount = total_amount
        order.save()
        
        return order