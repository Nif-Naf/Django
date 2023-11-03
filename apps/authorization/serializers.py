
from rest_framework import fields
from rest_framework.serializers import ModelSerializer

from apps.authorization.models import User


class SignUpSerializer(ModelSerializer):
    """Сериализатор для регистрации пользователя."""
    password = fields.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        ]
