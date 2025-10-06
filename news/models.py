from django.db import models


class News(models.Model):
	title = models.CharField(max_length=255)
	content = models.TextField()
	image = models.ImageField(upload_to="news/", blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self) -> str:
		return self.title
