from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from apps.authorization.admin.actions import suspend_access
from apps.authorization.admin.constants import (
    ADD_FIELDSETS,
    FIELDSETS,
    LIST_DISPLAY,
)
from apps.authorization.admin.forms.add import UserCreationForm
from apps.authorization.admin.forms.change import UserChangeForm
from apps.authorization.models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_per_page = 10
    list_max_show_all = 50
    actions = (suspend_access,)
    list_display = LIST_DISPLAY
    list_filter = (
        "is_superuser",
        "is_staff",
    )
    readonly_fields = ("is_verified_email",)
    fieldsets = FIELDSETS
    add_fieldsets = ADD_FIELDSETS
    search_fields = ("username", "email", "first_name")
    ordering = ("username",)
    filter_horizontal = []

    def delete_queryset(self, request, queryset):  # noqa
        """Удаление пользователь через админ-панель запрещено."""
        ...


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
