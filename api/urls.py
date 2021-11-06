from os import name

from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from .views import (CustomJwtObtainPairView, HomeView, UserLoginView,
                    UserRegisterView)

token_urls = [
    # path('', TokenObtainPairView.as_view(), name="token_obtain_pair_view"),
    path('', CustomJwtObtainPairView.as_view(), name="token_obtain_pair_view"),
    path('refresh/', TokenRefreshView.as_view(), name="token_refresh_view"),
    path('verify/', TokenVerifyView.as_view(), name="token_verify_view"),
]

api_urls = [
    path('home/', HomeView.as_view(), name="api_home"),
    path('user/register/', UserRegisterView.as_view(), name="user_register"),
    path('user/login/', UserLoginView.as_view(), name="user_login"),
]

urlpatterns = [
    path('token/', include((token_urls, 'api'), namespace='token')),
    path('', include((api_urls, 'api'), namespace='')),
]
