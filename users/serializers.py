from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from orders.models import Order


User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Username already taken.")],
    )
    email = serializers.EmailField(
        required=False,
        allow_blank=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email already in use.")],
    )
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    password_confirm = serializers.CharField(write_only=True, trim_whitespace=False)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "password_confirm",
        ]
        read_only_fields = ["id"]

    def validate_password(self, value: str):
        # Run Django's password validators
        validate_password(value)
        return value

    def validate(self, attrs):
        pwd = attrs.get('password')
        pwd2 = attrs.pop('password_confirm', None)
        if pwd2 is None:
            raise serializers.ValidationError({"password_confirm": "Please confirm your password."})
        if pwd != pwd2:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class OrderSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "status", "total_price", "created_at"]


class ProfileSerializer(serializers.ModelSerializer):
    shipping_address = serializers.CharField(source="profile.shipping_address", allow_blank=True, required=False)
    orders = OrderSummarySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "shipping_address", "orders"]
        read_only_fields = ["id", "username", "email", "orders"]
