from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product


class Order(models.Model):
	STATUS_PENDING = "Pending"
	STATUS_PAID = "Paid"
	STATUS_SHIPPED = "Shipped"
	STATUS_COMPLETED = "Completed"
	STATUS_CHOICES = [
		(STATUS_PENDING, "Pending"),
		(STATUS_PAID, "Paid"),
		(STATUS_SHIPPED, "Shipped"),
		(STATUS_COMPLETED, "Completed"),
	]

	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="orders")
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
	total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	# Shipping and billing info (minimal fields)
	shipping_name = models.CharField(max_length=255)
	shipping_address = models.TextField()
	billing_name = models.CharField(max_length=255)
	billing_address = models.TextField()

	def __str__(self) -> str:
		return f"Order #{self.id} by {self.user} - {self.status}"


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
	product = models.ForeignKey(Product, on_delete=models.PROTECT)
	quantity = models.PositiveIntegerField(default=1)
	price = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self) -> str:
		return f"{self.quantity} x {self.product.name} @ {self.price}"

# Create your models here.
