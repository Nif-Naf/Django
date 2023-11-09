from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.authorization.views.authentication import (
    SignInView,
    UpdateSignInView,
)
from apps.authorization.views.authorization import SignUpAPIView

authorization = [
    # Создание нового пользователя.
    path("sign_up", SignUpAPIView.as_view(), name="sign_up"),
]

authentication = [
    # Получения access_token, refresh_token.
    path("sign_in", SignInView.as_view(), name="login"),
    # Обновление access_token.
    path("update_sign_in", UpdateSignInView.as_view(), name="update_sign_in"),
]

user_router = DefaultRouter()

urlpatterns = [
    *authorization,
    *authentication,
    *user_router.urls,
]
