import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from apps.authorization.serializers import SignUpSerializer
from apps.authorization.models import User

logger = logging.getLogger(__name__)


class SignUpAPIView(APIView):
    """Регистрация пользователя."""
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_summary='Авторизация.',
        operation_description='Создание пользователя.',
        tags=['authorization', ],
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Успешное создание нового пользователя.',
            ),
            status.HTTP_409_CONFLICT: openapi.Response(
                description='Конфликт при создание нового пользователя.',
            ),
        }
    )
    def post(self, request: Request):
        """Создание нового пользователя."""
        serializer: SignUpSerializer
        serializer = self.serializer_class(request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        conflict = self.__check_email_and_username(username, email)
        if conflict:
            return Response(
                status=status.HTTP_409_CONFLICT,
                data={
                    'data': None,
                    'errors': conflict,
                    'description': 'New user not created.',
                },
            )
        User.objects.create_user(**serializer.validated_data)
        return Response(
            status=status.HTTP_201_CREATED,
            data={
                'data': serializer.data,
                'errors': None,
                'description': 'New user created.',
            },
        )

    def __check_email_and_username(self, username, email) -> dict:
        """Проверка уникальности имени пользователя и электронной почты."""
        conflict = {}
        if self.__is_not_free_this_username(username):
            conflict.update(
                {'username': f'This username: {username} is already taken.'},
            )
        if self.__is_not_free_this_email(email):
            conflict.update(
                {'email': f'This email: {email} is already taken.'},
            )
        return conflict

    def __is_not_free_this_username(self, username: str) -> bool:
        """Занято ли такое имя пользователя."""
        return self.queryset().filter(username=username).exists()

    def __is_not_free_this_email(self, email: str) -> bool:
        """Занято ли такая электронная почта."""
        return self.queryset().filter(email=email).exists()
