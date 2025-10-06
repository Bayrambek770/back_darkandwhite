from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "items",
            "total_price",
            "status",
            "created_at",
            "shipping_name",
            "shipping_address",
            "billing_name",
            "billing_address",
        ]
        read_only_fields = ["id", "user", "items", "total_price", "status", "created_at"]
