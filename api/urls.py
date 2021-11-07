from os import name

from django.conf import settings
from django.conf.urls import url
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import CustomJwtObtainPairView, HomeView, UserLoginView, UserRegisterView

schema_view = get_schema_view(
    openapi.Info(
        title="Django-JWT API",
        default_version="v1",
        description="Django-JWT project API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

token_urls = [
    # path('', TokenObtainPairView.as_view(), name="token_obtain_pair_view"),
    path("", CustomJwtObtainPairView.as_view(), name="token_obtain_pair_view"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh_view"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify_view"),
]

api_urls = [
    path("home/", HomeView.as_view(), name="api_home"),
    path("user/register/", UserRegisterView.as_view(), name="user_register"),
    path("user/login/", UserLoginView.as_view(), name="user_login"),
]

urlpatterns = [
    path("token/", include((token_urls, "api"), namespace="token")),
    path("", include((api_urls, "api"), namespace="")),
]

if settings.DEBUG == True:
    urlpatterns = [
        url(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        url(
            r"^swagger/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        url(
            r"^redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ] + urlpatterns
