from __future__ import annotations

import logging

from django.conf import settings
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.test import APITestCase

from apps.authorization.models import User

logger = logging.getLogger("testing")

ERRORS = {
    "not_authorization": "User not authorization.",
    "authorization_without_username": "User authorization without username.",
    "authorization_without_email": "User authorization without email.",
    "authorization_without_password": "User authorization without password.",
    "authorization_with_non_unique_username": "User authorization with non "
    "unique field: username.",
    "authorization_with_non_unique_email": "User authorization with non "
    "unique field: email.",
    "not_authenticated": "User not authenticated.",
    "authenticated_with_wrong_email": "User authenticated with wrong email.",
    "authenticated_without_email": "User authenticated without email.",
    "authenticated_with_wrong_password": "User authenticated with wrong "
    "password.",
    "authenticated_without_password": "User authenticated without password.",
    "not_updated_access": "User not update access in system.",
    "not_csrf_token": "CSRF token not passed.",
    "not_access_token": "Access token not passed.",
    "not_updated_access_token": "Access token has not updated.",
    "updated_access_token": "Access token updated.",
    "not_updated_refresh_token": "Refresh token has not updated.",
    "not_refresh_token": "Refresh token not passed.",
}
USER = {
    "email": "Polina@yandex.ru",
    "username": "Kaban",
    "password": "KabanovaPolina08",
    "first_name": "Полина",
    "last_name": "Кабанова",
}
BASE_URL = f"http://localhost:8000/{settings.API_BASE_URL}auth/"


class SuccessAuthTestCase(APITestCase):
    def test_success_auth(self):
        """Success authorization, authentication, update access in system."""
        logger.debug("Start test: test_success_auth.")
        client = self.client_class()

        # Authorization.
        path = BASE_URL + "sign_up"
        param = USER
        logger.debug("Request. Url: %s, Params: %s", path, param)
        response = client.post(path=path, data=param, format="json")
        status, data = response.status_code, response.data
        # Check response.
        logger.debug("Response. Status: %s, Data: %s", status, data)
        self.assertEqual(status, HTTP_201_CREATED, ERRORS["not_authorization"])

        # Authenticated.
        path = BASE_URL + "sign_in"
        param = {"email": USER["email"], "password": USER["password"]}
        logger.debug("Request. Url: %s, Params: %s", path, param)
        response = self.client.post(path=path, data=param, format="json")
        status, data = response.status_code, response.data
        # Check response.
        logger.debug("Response. Status: %s, Data: %s", status, data)
        self.assertEqual(status, HTTP_200_OK, ERRORS["not_authenticated"])
        # Check tokens.
        csrf_token = response.cookies.get("csrf").value
        first_access_token = response.cookies.get("access").value
        first_refresh_token = response.cookies.get("refresh").value
        logger.debug("CSRF token: %s", csrf_token)
        logger.debug("First access token: %s", first_access_token)
        logger.debug("First refresh token: %s", first_refresh_token)
        self.assertTrue(csrf_token, ERRORS["not_csrf_token"])
        self.assertTrue(first_access_token, ERRORS["not_access_token"])
        self.assertTrue(first_refresh_token, ERRORS["not_refresh_token"])

        # Update access.
        path = BASE_URL + "update_sign_in"
        param = {"refresh": f"{first_refresh_token}"}
        logger.debug("Request. Url: %s, Params: %s", path, param)
        response = self.client.post(path=path, data=param, format="json")
        status, data = response.status_code, response.data
        # Check response.
        logger.debug("Response. Status: %s, Data: %s", status, data)
        self.assertEqual(status, HTTP_200_OK, ERRORS["not_updated_access"])
        # Check tokens.
        if settings.SIMPLE_JWT["ROTATE_REFRESH_TOKENS"]:
            logger.debug("ROTATE_REFRESH_TOKENS enable.")
            two_access_token = response.cookies.get("access").value
            two_refresh_token = response.cookies.get("refresh").value
            logger.debug("Two access token: %s", two_access_token)
            logger.debug("Two refresh token: %s", two_refresh_token)
            self.assertTrue(two_access_token, ERRORS["not_access_token"])
            self.assertTrue(two_refresh_token, ERRORS["not_refresh_token"])
            self.assertNotEquals(
                first_access_token,
                two_access_token,
                ERRORS["not_updated_access_token"],
            )
            self.assertNotEquals(
                first_refresh_token,
                two_refresh_token,
                ERRORS["not_updated_refresh_token"],
            )
        else:
            logger.debug("ROTATE_REFRESH_TOKENS disable.")
            two_access_token = response.cookies.get("access").value
            logger.debug("Two access token: %s", two_access_token)
            self.assertTrue(two_access_token, ERRORS["not_access_token"])
            self.assertNotEquals(
                first_access_token,
                two_access_token,
                ERRORS["not_updated_access_token"],
            )

        # Update access attempt two.
        logger.debug("Request. Url: %s, Params: %s", path, param)
        response = self.client.post(path=path, data=param, format="json")
        status, data = response.status_code, response.data
        # Check response.
        logger.debug("Response. Status: %s, Data: %s", status, data)
        if settings.SIMPLE_JWT["ROTATE_REFRESH_TOKENS"]:
            logger.debug("ROTATE_REFRESH_TOKENS enable.")
            if settings.SIMPLE_JWT["BLACKLIST_AFTER_ROTATION"]:
                logger.debug("BLACKLIST_AFTER_ROTATION enable.")
                self.assertEqual(
                    status,
                    HTTP_400_BAD_REQUEST,
                    ERRORS["updated_access_token"],
                )
            else:
                logger.debug("BLACKLIST_AFTER_ROTATION disable.")
                self.assertEqual(
                    status,
                    HTTP_200_OK,
                    ERRORS["not_updated_access"],
                )
                three_access_token = response.cookies.get("access").value
                three_refresh_token = response.cookies.get("refresh").value
                logger.debug("Three access token: %s", three_access_token)
                logger.debug("Three refresh token: %s", three_refresh_token)
                self.assertTrue(three_access_token, ERRORS["not_access_token"])
                self.assertTrue(
                    three_refresh_token,
                    ERRORS["not_refresh_token"],
                )
                self.assertNotEquals(
                    two_access_token,
                    three_access_token,
                    ERRORS["not_updated_access_token"],
                )
                self.assertNotEquals(
                    two_refresh_token,  # noqa
                    three_refresh_token,
                    ERRORS["not_updated_refresh_token"],
                )
        else:
            logger.debug("ROTATE_REFRESH_TOKENS disable.")
            logger.debug("BLACKLIST_AFTER_ROTATION disable.")
            self.assertEqual(status, HTTP_200_OK, ERRORS["not_updated_access"])
            three_access_token = response.cookies.get("access").value
            logger.debug("Three access token: %s", three_access_token)
            self.assertTrue(three_access_token, ERRORS["not_access_token"])
            self.assertNotEquals(
                two_access_token,
                three_access_token,
                ERRORS["not_updated_access_token"],
            )


class NotAuthorizationTestCase(APITestCase):
    def setUp(self) -> None:
        """Create user."""
        User.objects.create_user(**USER)

    def test_attempt_auth_without_email(self):
        """Attempt authorization user without req field: email."""
        logger.debug("Start test: test_attempt_auth_without_email.")
        client = self.client_class()
        path = BASE_URL + "sign_up"
        param = {
            "username": USER["username"],
            "password": USER["password"],
            "first_name": USER["first_name"],
            "last_name": USER["last_name"],
        }
        logger.debug("Request. Url: %s, Params: %s", path, param)
        response = client.post(path=path, data=param, format="json")
        status, data = response.status_code, response.data
        # Check response.
        logger.debug("Response. Status: %s, Data: %s", status, data)
        self.assertEqual(
            status,
            HTTP_400_BAD_REQUEST,
            ERRORS["authorization_without_email"],
        )

    def test_attempt_auth_without_username(self):
        """Attempt authorization user without req field: username."""
        logger.debug("Start test: test_attempt_auth_without_username.")
        client = self.client_class()
        path = BASE_URL + "sign_up"
        param = {
            "email": USER["email"],
            "password": USER["password"],
            "first_name": USER["first_name"],
            "last_name": USER["last_name"],
        }
        logger.debug("Request. Url: %s, Params: %s", path, param)
        response = client.post(path=path, data=param, format="json")
        status, data = response.status_code, response.data
        # Check response.
        logger.debug("Response. Status: %s, Data: %s", status, data)
        self.assertEqual(
            status,
            HTTP_400_BAD_REQUEST,
            ERRORS["authorization_without_username"],
        )

    def test_attempt_auth_without_password(self):
        """Attempt authorization user without req field: password."""
        logger.debug("Start test: test_attempt_auth_without_password.")
        client = self.client_class()
        path = BASE_URL + "sign_up"
        param = {
            "username": USER["username"],
            "email": USER["email"],
            "first_name": USER["first_name"],
            "last_name": USER["last_name"],
        }
        logger.debug("Request. Url: %s, Params: %s", path, param)
        response = client.post(path=path, data=param, format="json")
        status, data = response.status_code, response.data
        # Check response.
        logger.debug("Response. Status: %s, Data: %s", status, data)
        self.assertEqual(
            status,
            HTTP_400_BAD_REQUEST,
            ERRORS["authorization_without_password"],
        )

    def test_attempt_auth_with_non_uniq_username(self):
        """Attempt authorization user with a non-unique field: username."""
        logger.debug("Start test: test_attempt_auth_with_non_uniq_username.")
        client = self.client_class()
        path = BASE_URL + "sign_up"
        param = {
            "username": USER["username"],
            "email": "Someemail@yandex.ru",
            "password": USER["password"],
            "first_name": USER["first_name"],
            "last_name": USER["last_name"],
        }
        logger.debug("Request. Url: %s, Params: %s", path, param)
        response = client.post(path=path, data=param, format="json")
        status, data = response.status_code, response.data
        # Check response.
        logger.debug("Response. Status: %s, Data: %s", status, data)
        self.assertEqual(
            status,
            HTTP_400_BAD_REQUEST,
            ERRORS["authorization_with_non_unique_username"],
        )

    def test_attempt_auth_with_non_uniq_email(self):
        """Attempt authorization user with a non-unique field: email."""
        logger.debug("Start test: test_attempt_auth_with_non_uniq_email.")
        client = self.client_class()
        path = BASE_URL + "sign_up"
        param = {
            "username": "some_username",
            "email": USER["email"],
            "password": USER["password"],
            "first_name": USER["first_name"],
            "last_name": USER["last_name"],
        }
        logger.debug("Request. Url: %s, Params: %s", path, param)
        response = client.post(path=path, data=param, format="json")
        status, data = response.status_code, response.data
        # Check response.
        logger.debug("Response. Status: %s, Data: %s", status, data)
        self.assertEqual(
            status,
            HTTP_400_BAD_REQUEST,
            ERRORS["authorization_with_non_unique_email"],
        )


class NotAuthenticationTestCase(APITestCase):
    def setUp(self) -> None:
        """Create user."""
        User.objects.create_user(**USER)

    def test_attempt_auth_with_wrong_email(self):
        """Attempt authenticated user with wrong email."""
        logger.debug("Start test: test_attempt_auth_with_wrong_email.")
        path = BASE_URL + "sign_in"
        param = {"email": "Someemail@yande.ru", "password": USER["password"]}
        logger.debug("Request. Url: %s, Params: %s", path, param)
        response = self.client.post(path=path, data=param, format="json")
        status, data = response.status_code, response.data
        # Check response.
        logger.debug("Response. Status: %s, Data: %s", status, data)
        self.assertEqual(
            status,
            HTTP_400_BAD_REQUEST,
            ERRORS["authenticated_with_wrong_email"],
        )

    def test_attempt_auth_without_email(self):
        """Attempt authenticated user without req field: email."""
        logger.debug("Start test: test_attempt_auth_without_email.")
        path = BASE_URL + "sign_in"
        param = {"password": USER["password"]}
        logger.debug("Request. Url: %s, Params: %s", path, param)
        response = self.client.post(path=path, data=param, format="json")
        status, data = response.status_code, response.data
        # Check response.
        logger.debug("Response. Status: %s, Data: %s", status, data)
        self.assertEqual(
            status,
            HTTP_400_BAD_REQUEST,
            ERRORS["authenticated_without_email"],
        )

    def test_attempt_auth_with_wrong_password(self):
        """Attempt authenticated user with wrong password."""
        logger.debug("Start test: test_attempt_auth_with_wrong_password.")
        path = BASE_URL + "sign_in"
        param = {"email": USER["email"], "password": "some_password"}
        logger.debug("Request. Url: %s, Params: %s", path, param)
        response = self.client.post(path=path, data=param, format="json")
        status, data = response.status_code, response.data
        # Check response.
        logger.debug("Response. Status: %s, Data: %s", status, data)
        self.assertEqual(
            status,
            HTTP_400_BAD_REQUEST,
            ERRORS["authenticated_with_wrong_password"],
        )

    def test_attempt_auth_without_password(self):
        """Attempt authenticated user without req field: password."""
        logger.debug("Start test: test_attempt_auth_without_password.")
        path = BASE_URL + "sign_in"
        param = {"email": USER["email"]}
        logger.debug("Request. Url: %s, Params: %s", path, param)
        response = self.client.post(path=path, data=param, format="json")
        status, data = response.status_code, response.data
        # Check response.
        logger.debug("Response. Status: %s, Data: %s", status, data)
        self.assertEqual(
            status,
            HTTP_400_BAD_REQUEST,
            ERRORS["authenticated_without_password"],
        )
