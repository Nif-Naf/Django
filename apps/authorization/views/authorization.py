import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authorization.business.authorization import (
    checking_email_and_username_for_uniqueness,
    create_user,
)
from apps.authorization.serializers import SignUpSerializer

logger = logging.getLogger(__name__)


class SignUpAPIView(APIView):
    """Регистрация пользователя."""

    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary="Авторизация.",
        operation_description="Создание пользователя.",
        tags=[
            "authorization",
        ],
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Успешное создание нового пользователя.",
            ),
            status.HTTP_409_CONFLICT: openapi.Response(
                description="Конфликт при создание нового пользователя.",
            ),
        },
    )
    def post(self, request: Request):
        """Создание нового пользователя."""
        serializer: SignUpSerializer
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        email = serializer.validated_data["email"]
        conflict = checking_email_and_username_for_uniqueness(username, email)
        if conflict:
            return Response(
                status=status.HTTP_409_CONFLICT,
                data={
                    "data": None,
                    "errors": conflict,
                    "description": "New user not created.",
                },
            )
        create_user(**serializer.validated_data)
        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "data": serializer.data,
                "errors": None,
                "description": "New user created.",
            },
        )
