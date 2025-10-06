from rest_framework import serializers
from .models import Product, Review, ProductImage


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "user", "product", "rating", "comment", "created_at"]
        read_only_fields = ["id", "user", "product", "created_at"]

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_comment(self, value):
        # If comment present, avoid all-whitespace
        if value is not None and isinstance(value, str) and value.strip() == "":
            return ""
        return value


class ProductSerializer(serializers.ModelSerializer):
    reviews_count = serializers.IntegerField(source="reviews.count", read_only=True)
    main_image = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "brand",
            "category",
            "image",
            "main_image",
            "images",
            "how_many_sold",
            "stock",
            "created_at",
            "reviews_count",
        ]
        read_only_fields = ["id", "created_at", "reviews_count", "how_many_sold"]

    def get_main_image(self, obj):
        primary = obj.images.filter(is_primary=True).first() or obj.images.first()
        if primary and primary.image:
            request = self.context.get('request')
            url = primary.image.url
            return request.build_absolute_uri(url) if request else url
        # fallback to legacy single image field
        if obj.image:
            request = self.context.get('request')
            url = obj.image.url
            return request.build_absolute_uri(url) if request else url
        return None

    def get_images(self, obj):
        out = []
        request = self.context.get('request')
        for img in obj.images.all():
            if not img.image:
                continue
            url = img.image.url
            url = request.build_absolute_uri(url) if request else url
            out.append({
                'id': img.id,
                'url': url,
                'alt_text': img.alt_text,
                'is_primary': img.is_primary,
                'order': img.order,
            })
        # include legacy single image if present and no images added yet
        if not out and obj.image:
            url = obj.image.url
            url = request.build_absolute_uri(url) if request else url
            out.append({'id': None, 'url': url, 'alt_text': '', 'is_primary': True, 'order': 0})
        return out
