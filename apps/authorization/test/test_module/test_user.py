from django.test import TestCase

from apps.authorization.models import User


class CreateUserTestsCase(TestCase):
    """Classes for created users."""

    USER = {
        "email": "Polina@yandex.ru",
        "username": "Kaban",
        "password": "KabanovaPolina08",
        "first_name": "Полина",
        "last_name": "Кабанова",
    }
    SUPER_USER = {
        "email": "Roman@yandex.ru",
        "username": "RomKa",
        "password": "ChickenFucker",
        "first_name": "Роман",
        "last_name": "Ахмадулин",
    }
    ERRORS = {
        "not_created": "User not created.",
        "not_super": "User is not staff.",
    }

    def test_create_user(self):
        """Create user."""
        user = User.objects.create_user(**self.USER)
        self.assertIsInstance(user, User, self.ERRORS["not_created"])

    def test_create_superuser(self):
        """Create super-user."""
        user = User.objects.create_superuser(**self.SUPER_USER)
        self.assertIsInstance(user, User, self.ERRORS["not_created"])
        self.assertEqual(user.is_staff, True, self.ERRORS["not_super"])

    def test_create_superuser_without_password(self):
        """Attempt to create a super-user without req field: password."""
        with self.assertRaises(TypeError):
            User.objects.create_superuser(
                email=self.SUPER_USER["email"],
                username=self.SUPER_USER["username"],
                first_name=self.SUPER_USER["first_name"],
                last_name=self.SUPER_USER["last_name"],
            )

    def test_create_user_without_username(self):
        """Attempt to create a user without req field: username."""
        with self.assertRaises(TypeError):
            User.objects.create_user(
                email="Katerina@yandex.ru",
                password="ShablinskayaKate",
                first_name="Екатерина",
                last_name="Шаблинская",
            )

    def test_create_user_without_email(self):
        """Attempt to create a user without req field: email."""
        with self.assertRaises(TypeError):
            User.objects.create_user(
                username="Kate",
                password="ShablinskayaKate",
                first_name="Екатерина",
                last_name="Шаблинская",
            )

    def test_create_user_with_non_uniq_username(self):
        """Attempt to create a user with a non-unique field: username."""
        with self.assertRaises(TypeError):
            User.objects.create_user(
                email="Katerina@yandex.ru",
                password="ShablinskayaKate",
                first_name="Екатерина",
                last_name="Шаблинская",
            )

    def test_create_user_with_non_uniq_email(self):
        """Attempt to create a user with a non-unique field: email."""
        with self.assertRaises(TypeError):
            User.objects.create_user(
                username="Kate",
                password="ShablinskayaKate",
                first_name="Екатерина",
                last_name="Шаблинская",
            )
