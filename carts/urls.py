from django.urls import path
from .views import CartDetailView, CartAddItemView, CartUpdateItemView, CartRemoveItemView

urlpatterns = [
    path("cart/", CartDetailView.as_view(), name="cart-detail"),
    path("cart/add/", CartAddItemView.as_view(), name="cart-add"),
    path("cart/items/<int:item_id>/", CartUpdateItemView.as_view(), name="cart-update"),
    path("cart/items/<int:item_id>/remove/", CartRemoveItemView.as_view(), name="cart-remove"),
]
