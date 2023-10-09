import logging

import requests
from django.test import TestCase

logger = logging.getLogger(__name__)


class FilesViewSetApiTests(TestCase):
    url = 'http://localhost:8000/api/v1/storage/files/'

    def test_success_retrieve_files(self):
        request = requests.get(
            url=self.url,
            timeout=10,
            params={
                'offset': 0,
                'limit': 10,
            },
        )
        self.assertEqual(request.status_code, 200)

    def test_send_req_with_incorrect_method(self):
        request = requests.post(
            url=self.url,
            timeout=10,
        )
        self.assertEqual(request.status_code, 405)


class UploadViewSetApiTests(TestCase):
    url = 'http://localhost:8000/api/v1/storage/upload/'

    def test_send_req_with_incorrect_method(self):
        request = requests.get(
            url=self.url,
            timeout=10,
        )
        self.assertEqual(request.status_code, 405)
