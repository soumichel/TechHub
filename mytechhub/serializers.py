from rest_framework import serializers
from .models import Product, Order, OrderItem, SupplierProfile
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source="supplier.company_name", read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'supplier_name']

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'quantity', 'price', 'subtotal']

    def create(self, validated_data):
        price = validated_data['price']
        quantity = validated_data['quantity']
        validated_data['subtotal'] = price * quantity
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=False)

    class Meta:
        model = Order
        fields = ['id', 'status', 'created_at', 'updated_at', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

    def validate(self, data):
        if not data.get('items'):
            raise serializers.ValidationError("Um pedido precisa conter ao menos um item.")
        return data

class SupplierProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierProfile
        fields = ['company_name', 'phone', 'address']

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
