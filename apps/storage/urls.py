from rest_framework.routers import DefaultRouter

from apps.storage.views import (
    FilesViewSet,
    UploadViewSet,
)

file_router = DefaultRouter()

# Загрузка файла.
file_router.register(
    prefix='upload',
    viewset=UploadViewSet,
    basename='uploaded_file',
)

# Выгрузка всех файлов.
file_router.register(
    prefix='files',
    viewset=FilesViewSet,
    basename='get_list_of_files',
)

urlpatterns = file_router.urls
