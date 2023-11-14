from __future__ import annotations

from django.conf import settings
from rest_framework.response import Response


class JWTResponse(Response):
    """Ответ созданный специально для JWT Auth."""

    __CSRF_COOKIE_NAME = "csrf"
    __CSRF_TOKEN = settings.SECRET_KEY
    __ACCESS_KEY = "access"
    __ACCESS_EXPIRATION = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]
    __REFRESH_KEY = "refresh"
    __REFRESH_EXPIRATION = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]
    __SECURE = settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"]
    __HTTP_ONLY = settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"]
    __SAME_SITE = settings.SIMPLE_JWT["AUTH_COOKIE_SAME_SITE"]

    def __init__(self, data: dict, status: int):
        super().__init__(data, status)

    # А если добавлю два раза???
    def add_to_cookie_csrf_token(self, token: str) -> None:
        self.set_cookie(
            key=self.__CSRF_COOKIE_NAME,
            value=token,
            secure=False,
            httponly=False,
            samesite="Lax",
        )

    def add_to_cookie_access_token(self, token: str) -> None:
        self.set_cookie(
            key=self.__ACCESS_KEY,
            value=token,
            expires=self.__ACCESS_EXPIRATION,
            secure=self.__SECURE,
            httponly=self.__HTTP_ONLY,
            samesite=self.__SAME_SITE,
        )

    def add_to_cookie_refresh_token(self, token: str) -> None:
        self.set_cookie(
            key=self.__REFRESH_KEY,
            value=token,
            expires=self.__REFRESH_EXPIRATION,
            secure=self.__SECURE,
            httponly=self.__HTTP_ONLY,
            samesite=self.__SAME_SITE,
        )
