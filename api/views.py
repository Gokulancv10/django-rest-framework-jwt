from datetime import datetime, time, timedelta

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics, serializers, status, views
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .serializers import (
    CustomJwtTokenObtainPairSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
)


class CustomJwtObtainPairView(TokenObtainPairView):
    """
    Custom Json Web Token obtain pair view

    Returns:
        JWT access and refresh tokens.
    """

    serializer_class = CustomJwtTokenObtainPairSerializer


class HomeView(generics.GenericAPIView):
    """
    Home page API
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        message = f"Hello, {request.user.first_name} {request.user.last_name}"
        return Response({"message": message})


class UserRegisterView(generics.GenericAPIView):
    """
    User Registration API

    Returns:
        [JSON]: User's username and email
    """

    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(generics.GenericAPIView):
    """
    User Login API

    Returns:
        [JSON]: Logged-in user's data, access token and refresh token
    """

    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        # Validating user credential
        user = authenticate(username=username, password=password)

        if user:
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Incorrect username and password"},
            status=status.HTTP_400_BAD_REQUEST,
        )
