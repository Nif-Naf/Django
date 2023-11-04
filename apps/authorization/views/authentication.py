import logging

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

logger = logging.getLogger(__name__)


class SignInView(TokenObtainPairView):
    """Вход в систему."""
    permission_classes = (AllowAny, )

    @swagger_auto_schema(
        operation_summary='Аутентификация.',
        operation_description='Вход в систему.',
        tags=['authentication', ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Успешное получение токена.',
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description='Ошибка при валидации.',
            ),
        }
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'data': None,
                    'error': str(e),
                    'description': 'You are not authorized.',
                },
            )
        return Response(
            status=status.HTTP_200_OK,
            data={
                'data': serializer.validated_data,
                'errors': None,
                'description': 'You are authorized.',
            },
        )


class UpdateSignInView(TokenRefreshView):
    """Обновляет доступ к системе."""
    permission_classes = (AllowAny, )

    @swagger_auto_schema(
        operation_summary='Аутентификация.',
        operation_description='Обновление токена.',
        tags=['authentication', ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Успешное обновление токена доступа.',
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description='Ошибка при валидации.',
            ),
        }
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    'data': None,
                    'error': str(e),
                    'description': 'You have not updated your access token.',
                },
            )
        return Response(
            status=status.HTTP_200_OK,
            data={
                'data': serializer.validated_data,
                'errors': None,
                'description': 'You have updated your access token.',
            },
        )
