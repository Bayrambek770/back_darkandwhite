from django.contrib import admin
from .models import Product, Review, ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "brand", "category", "price", "stock", "created_at")
    list_filter = ("category", "brand")
    search_fields = ("name", "description", "brand")
    readonly_fields = ("created_at", "how_many_sold")


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "alt_text", "is_primary", "order")


ProductAdmin.inlines = [ProductImageInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "user", "rating", "created_at")
    search_fields = ("product__name", "user__username", "comment")
from django.contrib import admin

# Register your models here.
