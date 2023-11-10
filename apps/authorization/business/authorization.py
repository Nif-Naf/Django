from typing import OrderedDict

from apps.authorization.models import User


def checking_email_and_username_for_uniqueness(
    username: str,
    email: str,
) -> dict:
    """Проверка уникальности имени пользователя и электронной почты.

    В случае если email или username, или оба сразу заняты. Тогда
    возвращается словарь с предупреждением, о том что это не уникальный(ые)
    параметр(ы). Если данные параметры уникальны, то возвращается
    пустой словарь.
    """
    conflict = {}
    if is_this_user_exist(username=username):
        conflict.update(
            {"username": f"This username: {username} is already taken."},
        )
    if is_this_user_exist(email=email):
        conflict.update(
            {"email": f"This email: {email} is already taken."},
        )
    return conflict


def create_user(**kwargs: OrderedDict or dict) -> User:
    """Создание пользователя."""
    return User.objects.create_user(**kwargs)


def is_this_user_exist(**kwargs: OrderedDict or dict) -> bool:
    """Существует ли пользователь в системе с такими полями."""
    return User.objects.filter(**kwargs).exists()
