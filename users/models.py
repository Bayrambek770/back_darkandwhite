from django.db import models
from django.contrib.auth import get_user_model


class UserProfile(models.Model):
	user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="profile")
	shipping_address = models.TextField(blank=True)

	def __str__(self) -> str:
		return f"Profile of {self.user}"

# Create your models here.
