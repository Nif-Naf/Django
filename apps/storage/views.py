import logging

from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
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
    """Манипуляция с файлом(ами)."""
    queryset = File.objects.all()
    serializer_class = FileModelSerializer
    pagination_class = LimitOffsetPagination
    http_method_names = ['get']

    @swagger_auto_schema(
        operation_summary='Список файлов.',
        operation_description='Получить список файлов в зависимости от '
                              'параметров пагинации.',
        tags=['storage', ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='The files have been received.',
                schema=FileModelSerializer,
            ),
        }
    )
    def list(self, request, *args, **kwargs):
        """Получение файлов.
        Получить список файлов в зависимости от параметров пагинации.

        Returns: Список файлов.
        """
        return super().list(self, request, *args, **kwargs)


class UploadViewSet(ViewSet):
    serializer_class = FileSerializer
    http_method_names = ['post']

    @swagger_auto_schema(
        operation_summary='Загрузка файла в файловое хранилище.',
        operation_description='Создание в БД записи об этом файле. '
                              'С полями которые содержат информацию о нем.',
        tags=['storage', ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['file', ],
            properties={
                'file': openapi.Schema(type=openapi.TYPE_FILE),
            },
        ),
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='File uploaded success.',
                schema=FileModelSerializer,
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description='File not uploaded. Unknown error.',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'data': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            )
        },
    )
    def create(self, request):
        """Загрузка файла в файловое хранилище.
        Создание в БД записи об этом файле. С полями которые содержат информацию
        о нем.

        Args:
            request: POST-запрос с сообщением в теле.

        Returns:
            В случае успешного сохранения файла отдается сообщение с информацией
            о сохраненном файле и стутусом 201. Если сохранение файла произошло
            с ошибкой, то отдается сообщение с конкретной ошибкой и статусом
            500.

        """
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
