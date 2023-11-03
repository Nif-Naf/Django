from django.contrib import admin
from django.conf import settings
from django.urls import (
    path,
    include,
)

from core.swagger import urlpatterns as docs

urlpatterns = [
    path('admin/', admin.site.urls),
    path(settings.API_BASE_URL + 'auth/', include('apps.authorization.urls'), name='authorization'),
]

if settings.DEBUG:
    urlpatterns += docs
