from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from apps.authorization.models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        exclude = '__all__'


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
        "is_superuser",
    ]
    list_filter = ["is_superuser", ]
    fieldsets = [
        ("Системные данные", {
            "fields": [
                "username",
                "email",
                "password",
            ]
        }),
        ("Персональные данные", {
            "fields": [
                "first_name",
                "last_name",
            ]
        }),
        ("Права", {
            "fields": [
                "is_superuser",
                "user_permissions",
            ]
        }),
    ]
    add_fieldsets = [
        ("Обязательные поля",
         {
             "classes": ["wide"],
             "fields": [
                 "username",
                 "email",
                 "password1",
                 "password2",
             ],
         }),
        ("Опциональные поля",
         {
             "classes": ["wide"],
             "fields": [
                 "first_name",
                 "last_name",
             ],
         }),
    ]
    search_fields = ["username", "email", "first_name"]
    ordering = ["username"]
    filter_horizontal = []


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
