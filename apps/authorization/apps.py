from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.authorization"
    label = "authorization"
    verbose_name = "Администрирование пользователей."
