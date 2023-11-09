from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Менеджер модели User."""

    def create_user(self, username, email, password=None, **extra_fields):
        """Создание пользователя."""
        if username is None:
            raise TypeError("Users must have a username.")

        if email is None:
            raise TypeError("Users must have an email address.")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """Создание администратора."""
        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(username, email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
