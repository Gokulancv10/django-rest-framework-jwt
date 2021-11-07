from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken


class CustomJwtTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customizing JSON Web Token data
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add few more user Information
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email if user.email else "",
        }
        token["user_data"] = user_data
        return token


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=69, min_length=6, required=True)
    email = serializers.EmailField(required=True, allow_null=False)
    password = serializers.CharField(max_length=69, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def validate_username(self, value):
        username = User.objects.filter(username=value).exists()
        if username:
            raise serializers.ValidationError(
                {"username": "The username is already in use"}
            )
        return value

    def validate_email(self, value):
        email = User.objects.filter(email=value).exists()
        if email:
            raise serializers.ValidationError(
                {"email": "The email is already in use"}
            )
        return value


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, min_length=3, max_length=69)
    password = serializers.CharField(required=True, write_only=True,
        min_length=3, max_length=69)
    token = serializers.SerializerMethodField("get_simple_jwt_token")

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "token")
        read_only_fields = ["token", "email"]

    def get_pyjwt_token(self, obj):
        """
        Generate JSON Web Token for a logged in user using pyjwt library

        Returns:
            User data and JWT access token

        Sample Data:
            {
                "id": 1,
                "username": "TestUser",
                "email": "",
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.
                    eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6IlRlc3RVc2VyIiwiZW1haWwiOiIiLCJpYXQiOjE2MzYyMDc3MTMsImV4cCI6MTYzNjIwODAxM30.
                    4-UKnDl5HO2RiEzCcaCc4VjBO-k63OHfWiReV3Tg-9U"
            }
        """
        user_data = {
            "user_id": obj.id,
            "username": obj.username,
            "email": obj.email,
            "iat": datetime.now(tz=timezone.utc),
            "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=5),
        }
        encoded_jwt = jwt.encode(user_data, key=settings.SECRET_KEY, algorithm="HS256")
        return encoded_jwt

    def get_simple_jwt_token(self, obj):
        """
        Generate access and refresh token for the logged-in user

        Returns:
            [JSON]: Access token and refresh token
        """
        refresh_token = RefreshToken.for_user(obj)
        json_data = {
            "refresh": str(refresh_token),
            "access": str(refresh_token.access_token),
        }
        return json_data
