from django.contrib import admin

from apps.authorization.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.reqister(User, UserAdmin)
