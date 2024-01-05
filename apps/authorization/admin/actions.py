from django.contrib.admin.decorators import action


@action(description="Приостановить доступ к аккаунту(ам).")
def suspend_access(self, request, queryset):  # noqa
    queryset.update(is_active=False)
