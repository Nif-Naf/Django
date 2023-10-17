from django.contrib import admin
from django.urls import (
    path,
    include,
)

from .settings import DEBUG
from .swagger import urlpatterns as docs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/storage/', include('apps.storage.urls')),
]

if DEBUG:
    urlpatterns += docs
