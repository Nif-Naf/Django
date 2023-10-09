import logging

from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import (
    GenericViewSet,
    ViewSet,
)
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from apps.storage.models import File
from apps.storage.serializer import (
    FileModelSerializer,
    FileSerializer,
)
from apps.storage.tasks.processing import upload_file


logger = logging.getLogger(__name__)


class FilesViewSet(GenericViewSet, ListModelMixin):
    queryset = File.objects.all()
    serializer_class = FileModelSerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ['get']


class UploadViewSet(ViewSet):
    serializer_class = FileSerializer
    http_method_names = ['post']

    def create(self, request):
        """Загрузка файла."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            new_file = File.objects.create(**serializer.validated_data)
        except Exception as error:
            logger.debug('Error saving file. Error: %s.', error)
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                data=str(error),
            )
        logger.debug('File created.')
        upload_file.delay(new_file.id)
        serialized_new_file = FileModelSerializer(new_file)
        return Response(
            status=HTTP_201_CREATED,
            data=serialized_new_file.data,
        )
