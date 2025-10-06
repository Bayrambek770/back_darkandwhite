from rest_framework import views, status
from rest_framework.response import Response
from django.conf import settings

from .serializers import ContactSerializer


class PublicOfferView(views.APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        text = getattr(settings, "PUBLIC_OFFER_TEXT", "Terms & Conditions will be provided here.")
        return Response({"text": text})


class ContactCreateView(views.APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
from django.shortcuts import render

# Create your views here.
