from __future__ import annotations

import logging

from django.conf import settings
from django.middleware import csrf
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.authorization.business.authentication import JWTResponse

logger = logging.getLogger(__name__)


class SignInView(TokenObtainPairView):
    """Вход в систему."""

    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Аутентификация.",
        operation_description="Вход в систему.",
        tags=[
            "authentication",
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Успешное получение токена.",
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Ошибка при валидации.",
            ),
        },
    )
    def post(self, request: Request) -> Response | JWTResponse:
        """Получение всех необходимых токенов для авторизации.

        Args:
            request.data.email (str): Электронная почта.
            request.data.password (str): Пароль пользователя.

        Returns:
            В cookies access_token, refresh_token, csrf_token.
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "data": None,
                    "error": str(e),
                    "description": "You are not authorized.",
                },
            )
        csrf_token = csrf.get_token(request)
        access_token = serializer.validated_data["access"]
        refresh_token = serializer.validated_data["refresh"]
        response = JWTResponse(
            status=status.HTTP_200_OK,
            data={
                "data": None,
                "errors": None,
                "description": "You are authorized.",
            },
        )
        response.add_to_cookie_csrf_token(csrf_token)
        response.add_to_cookie_access_token(access_token)
        response.add_to_cookie_refresh_token(refresh_token)
        return response


class UpdateSignInView(TokenRefreshView):
    """Обновляет доступ к системе."""

    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Аутентификация.",
        operation_description="Обновление токена.",
        tags=[
            "authentication",
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Успешное обновление токена доступа.",
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Ошибка при валидации.",
            ),
        },
    )
    def post(self, request: Request) -> Response | JWTResponse:
        """Обновление access_token для возобновления доступа к системе.

        Args:
            request.COOKIE.refresh_token (str): Токен обновления.

        Returns:
            В cookies новый access_token.
        """
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "data": None,
                    "error": str(e),
                    "description": "You have not updated your access token.",
                },
            )
        access_token = serializer.validated_data["access"]
        response = JWTResponse(
            status=status.HTTP_200_OK,
            data={
                "data": None,
                "errors": None,
                "description": "You have updated your access system.",
            },
        )
        response.add_to_cookie_access_token(access_token)
        if settings.SIMPLE_JWT["ROTATE_REFRESH_TOKENS"]:
            refresh_token = serializer.validated_data["refresh"]
            response.add_to_cookie_refresh_token(refresh_token)
        return response
