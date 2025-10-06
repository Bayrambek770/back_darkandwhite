from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product


class Cart(models.Model):
	user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="cart")
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return f"Cart of {self.user}"

	@property
	def total_price(self):
		return sum(item.subtotal for item in self.items.all())


class CartItem(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=1)

	class Meta:
		unique_together = ("cart", "product")

	def __str__(self) -> str:
		return f"{self.quantity} x {self.product.name}"

	@property
	def subtotal(self):
		return self.product.price * self.quantity

# Create your models here.
