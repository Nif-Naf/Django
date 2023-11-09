from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.authorization.models.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя."""

    REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = "email"
    objects = UserManager()

    ##########################################
    # Системно важные поля.
    ##########################################
    username = models.CharField(
        db_index=True,
        max_length=255,
        unique=True,
    )
    email = models.EmailField(
        db_index=True,
        unique=True,
    )

    #########################################
    # О пользователе.
    #########################################
    first_name = models.CharField(
        null=True,
        max_length=255,
    )
    last_name = models.CharField(
        null=True,
        max_length=255,
    )
    # gender = models.CharField(
    #     null=True,
    #     choices=(('male', 'Мужской'), ('female', 'Женский')),
    #     max_length=6,
    # )

    #########################################
    # Сервисные поля.
    #########################################
    is_active = models.BooleanField(
        default=True,
        help_text="Активная ли учетная запись.",
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Может ли получить доступ к административной панели.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Дата создания пользователя.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Последнее обновление пользователя.",
    )

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name = "пользователя"
        verbose_name_plural = "пользователи"
