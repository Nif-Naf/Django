from django import forms
from django.core.exceptions import ValidationError

from apps.authorization.models import User


class UserCreationForm(forms.ModelForm):
    """Форма для создания новых пользователей."""

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "gender",
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user