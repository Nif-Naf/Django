from django.db import models


class File(models.Model):
    file = models.FileField(
        upload_to='uploads/',
        verbose_name='Файл.',
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата загрузки.',
    )
    processed = models.BooleanField(
        default=False,
        verbose_name='Обработан ли файл.',
    )

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
