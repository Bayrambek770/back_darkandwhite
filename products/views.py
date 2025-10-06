from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Product, Review
from .serializers import ProductSerializer, ReviewSerializer
from django.db.models.functions import Coalesce
from django.db.models import IntegerField


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "brand"]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at", "name"]

    @action(detail=False, methods=["get"], url_path="most-sold")
    def most_sold(self, request):
        """
        Returns the top 6 products by how_many_sold (descending).
        Tie-breaker: newer products first by created_at desc.
        """
        qs = (
            Product.objects.all()
            .annotate(_sold=Coalesce("how_many_sold", 0, output_field=IntegerField()))
            .order_by("-_sold", "-created_at")
        )
        qs = qs[:6]
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="recommended")
    def recommended(self, request):
        """
        Returns 6 random products for recommendation.
        Implementation uses DB-level random ordering; for large datasets,
        consider alternative strategies (e.g., sampling IDs) for performance.
        """
        qs = Product.objects.all().order_by("?")[:6]
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get", "post"], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def reviews(self, request, pk=None):
        product = self.get_object()
        if request.method == "GET":
            qs = product.reviews.all()
            page = self.paginate_queryset(qs)
            serializer = ReviewSerializer(page or qs, many=True)
            if page is not None:
                return self.get_paginated_response(serializer.data)
            return Response(serializer.data)

        # POST - create review
        # Accept common aliases for the comment field sent by frontends
        data = request.data.copy()
        if 'comment' not in data:
            for alias in ('text', 'message', 'content', 'review'):
                if alias in data and data.get(alias):
                    data['comment'] = data.get(alias)
                    break
        serializer = ReviewSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # Persist review; product and user are set explicitly from context
        Review.objects.create(
            user=request.user,
            product=product,
            rating=serializer.validated_data["rating"],
            comment=serializer.validated_data.get("comment", "").strip(),
        )
        return Response({"detail": "Review added."}, status=status.HTTP_201_CREATED)

from django.shortcuts import render

# Create your views here.
