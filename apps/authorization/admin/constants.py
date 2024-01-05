LIST_DISPLAY = (
    "username",
    "first_name",
    "last_name",
    "email",
    "is_superuser",
    "is_staff",
)

FIELDSETS = [
    (
        "Системные данные",
        {
            "fields": [
                "username",
                "email",
                "is_verified_email",
            ],
        },
    ),
    (
        "Персональные данные",
        {
            "fields": [
                "first_name",
                "last_name",
            ],
        },
    ),
    (
        "Права",
        {
            "fields": [
                "is_superuser",
                "is_staff",
                "user_permissions",
            ],
        },
    ),
    (
        "ВНИМАНИЕ. Изменение пароля.",
        {
            "fields": [
                "password1",
                "password2",
                "confirmation",
            ],
        },
    ),
]
ADD_FIELDSETS = [
    (
        "Обязательные поля",
        {
            "classes": ["wide"],
            "fields": [
                "username",
                "email",
                "password1",
                "password2",
            ],
        },
    ),
    (
        "Опциональные поля",
        {
            "classes": ["wide"],
            "fields": [
                "first_name",
                "last_name",
            ],
        },
    ),
]
