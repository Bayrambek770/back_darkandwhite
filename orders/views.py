from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Order, OrderItem
from .serializers import OrderSerializer
from carts.models import Cart, CartItem


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            cart = request.user.cart  # OneToOne
        except Cart.DoesNotExist:
            return Response({"detail": "Cart is empty."}, status=400)
        items = cart.items.select_related("product")
        if not items.exists():
            return Response({"detail": "Cart is empty."}, status=400)

        data = request.data
        required = ["shipping_name", "shipping_address", "billing_name", "billing_address"]
        if any(not data.get(f) for f in required):
            return Response({"detail": "Missing shipping/billing fields."}, status=400)

        order = Order.objects.create(
            user=request.user,
            shipping_name=data["shipping_name"],
            shipping_address=data["shipping_address"],
            billing_name=data["billing_name"],
            billing_address=data["billing_address"],
        )

        total = 0
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            total += item.product.price * item.quantity
        order.total_price = total
        order.save()

        # Clear cart
        items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all().prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def patch(self, request, *args, **kwargs):
        # Only admins can update status
        order = self.get_object()
        if not request.user.is_staff:
            return Response({"detail": "Not allowed"}, status=403)
        status_value = request.data.get("status")
        if status_value not in dict(Order.STATUS_CHOICES):
            return Response({"detail": "Invalid status"}, status=400)
        order.status = status_value
        order.save(update_fields=["status"])
        return Response(OrderSerializer(order).data)
from django.shortcuts import render

# Create your views here.
