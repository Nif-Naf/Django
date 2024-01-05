import logging

from django import forms
from django.core.exceptions import ValidationError

from apps.authorization.models import User

logger = logging.getLogger(__name__)


class UserChangeForm(forms.ModelForm):
    """Форма для изменения пользователей."""

    confirmation_choices = (
        (False, "Не подтверждаю"),
        (True, "Подтверждаю"),
    )

    password1 = forms.CharField(
        required=False,
        label="Новый пароль.",
        help_text="Изменение существующего пароля пользователя.",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        required=False,
        label="Проверка нового пароля.",
        help_text="Проверка нового пароля пользователя.",
        widget=forms.PasswordInput,
    )
    confirmation = forms.ChoiceField(
        choices=confirmation_choices,
        initial="",
        label="Подтвердите смену пароля",
        help_text="При изменении пароля необходимо подтверждение.",
        widget=forms.Select,
    )

    class Meta:
        model = User
        exclude = [
            "password",
        ]

    def clean(self):
        cleaned_data = super().clean()
        confirmation = cleaned_data.get("confirmation")
        password_one = cleaned_data.get("password1")
        password_two = cleaned_data.get("password2")
        if confirmation == "True":
            if not password_one:
                raise ValidationError("Пароль отсутствует")
            elif not password_two:
                raise ValidationError("Подтверждение пароля отсутствует")
            elif password_one != password_two:
                raise ValidationError("Пароли не совпадают")
        elif confirmation == "False" and any((password_one, password_two)):
            raise ValidationError("Изменение пароля без подтверждения.")

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data["confirmation"] == "True":
            new_password = self.cleaned_data["password1"]
            user.set_password(new_password)
        if commit:
            user.save()
        return user
