from django.urls import path
from .views import PublicOfferView, ContactCreateView

urlpatterns = [
    path("public-offer/", PublicOfferView.as_view(), name="public-offer"),
    path("contact/", ContactCreateView.as_view(), name="contact"),
]
