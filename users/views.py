from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from .serializers import SignupSerializer, ProfileSerializer


class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = serializer.instance
        shipping = serializer.validated_data.get('profile', {}).get('shipping_address')
        if shipping is not None:
            user.profile.shipping_address = shipping
            user.profile.save(update_fields=["shipping_address"])
        user.save()


class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh token required"}, status=400)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response({"detail": "Invalid token"}, status=400)
        return Response(status=status.HTTP_205_RESET_CONTENT)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Accept either username or email in the username field."""
    def validate(self, attrs):
        username_or_email = attrs.get(self.username_field)
        User = get_user_model()
        if username_or_email:
            # If value looks like an email, try email first
            candidate_username = None
            if '@' in username_or_email:
                try:
                    user = User.objects.get(email__iexact=username_or_email)
                    candidate_username = user.username
                except User.DoesNotExist:
                    candidate_username = None
            # If not found via email, or not an email, try username then email
            if not candidate_username:
                try:
                    user = User.objects.get(username=username_or_email)
                    candidate_username = user.username
                except User.DoesNotExist:
                    try:
                        user = User.objects.get(email__iexact=username_or_email)
                        candidate_username = user.username
                    except User.DoesNotExist:
                        candidate_username = None
            if candidate_username:
                attrs[self.username_field] = candidate_username
        return super().validate(attrs)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
from django.shortcuts import render

# Create your views here.
