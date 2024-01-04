from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.authorization.models.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя."""

    REQUIRED_FIELDS = ["email"]
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    objects = UserManager()

    ##########################################
    # Системно важные поля.
    ##########################################
    username = models.CharField(
        unique=True,
        max_length=20,
        verbose_name="Псевдоним",
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
    )
    is_verified_email = models.BooleanField(
        default=False,
        verbose_name="Верифицирована ли почта",
        help_text="Если почта подтверждена, то пользователю будут доступны "
        "некоторые дополнительные функции.",
    )

    #########################################
    # О пользователе.
    #########################################
    first_name = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        verbose_name="Фамилия",
    )
    gender = models.CharField(
        null=True,
        blank=True,
        max_length=6,
        choices=(("male", "Мужской"), ("female", "Женский")),
        verbose_name="Пол",
    )

    #########################################
    # Сервисные поля.
    #########################################
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активная ли учетная запись",
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Сотрудник",
        help_text="Может ли получить доступ к административной панели",
        db_comment="Может ли получить доступ к административной панели",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания пользователя",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Последнее обновление пользователя",
    )

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name = "пользователя"
        verbose_name_plural = "пользователи"
