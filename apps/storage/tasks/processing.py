import logging
from time import sleep

from apps.storage.models import File
from apps.storage.workers.regular import storage_regular

logger = logging.getLogger(__name__)


@storage_regular.task
def upload_file(pk) -> dict:
    """Начать обработку файла в Celery."""
    logger.debug('Start upload receive file.')
    try:
        file = File.objects.get(id=pk)
    except File.DoesNotExist:
        logger.error(f'The file {pk} not found.')
        return {
            'status operation': 'Failed',
            'description': f'The file {pk} not found.',
        }
    sleep(30)
    file.processed = True
    file.save(update_fields=['processed'])
    logger.error(f'The file {pk} updated.')
    return {
        'status operation': 'Success',
        'description': 'File updated.',
    }
