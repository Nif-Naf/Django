from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.authorization.views.authorization import SignUpAPIView

authorization = [
    # Создание нового пользователя.
    path('sign_up', SignUpAPIView.as_view(), name='sign_up'),
]

user_router = DefaultRouter()

urlpatterns = [
    *authorization,
    *user_router.urls,
]
