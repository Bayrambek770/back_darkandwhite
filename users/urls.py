from django.urls import path
from .views import SignupView, ProfileView, LogoutView

urlpatterns = [
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/profile/", ProfileView.as_view(), name="profile"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
]
