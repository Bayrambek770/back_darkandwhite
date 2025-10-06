from django.db import models
from django.contrib.auth import get_user_model


class Product(models.Model):
	CATEGORY_CHOICES = [
		("CPU", "CPU"),
		("GPU", "GPU"),
		("Monoblock", "Monoblock"),
		("Monitor", "Monitor"),
	]

	name = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	brand = models.CharField(max_length=255)
	category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
	image = models.ImageField(upload_to="products/", blank=True, null=True)
	stock = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	how_many_sold = models.PositiveIntegerField(default=0, blank=True, null=True)

	def __str__(self) -> str:
		return f"{self.name} ({self.category})"


class Review(models.Model):
	user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
	rating = models.PositiveSmallIntegerField()
	comment = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self) -> str:
		return f"Review {self.rating} by {self.user} on {self.product}"


class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
	image = models.ImageField(upload_to="products/")
	alt_text = models.CharField(max_length=255, blank=True)
	is_primary = models.BooleanField(default=False)
	order = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["order", "id"]

	def __str__(self) -> str:
		return f"Image for {self.product.name} ({self.id})"

# Create your models here.
