from rest_framework.fields import FileField
from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
)

from apps.storage.models import File


class FileSerializer(Serializer):
    """Сериализатор для загрузки файлов."""
    file = FileField()


class FileModelSerializer(ModelSerializer):
    """Сериализатор для просмотра информации о файлах."""

    class Meta:
        model = File
        fields = '__all__'
